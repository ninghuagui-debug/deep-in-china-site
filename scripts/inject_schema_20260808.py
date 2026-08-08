#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P0 批量注入 JSON-LD schema + 内链集群 (2026-08-08)
目标: 3篇guides(guangxi/chongqing-rail-tunnel/guilin-diecai-mountain) + 34省页
schema: Article / TravelGuide / BreadcrumbList / FAQPage
- guides: FAQ 从静态 <h2> 转
- province: FAQ 从 province-data JSON(hookData/description) 构造(JS渲染页无静态H2)
保留现有 meta/canonical/OG 不动; 仅在 </head> 前插入 JSON-LD, </body> 前插内链区块。
"""
import re, json, html, os, sys

BASE = "C:/Users/WWW/WorkBuddy/wb网页/deep-in-china-site"
SITE = "https://ninghuagui-debug.github.io/deep-in-china-site"

GUIDES = {
    "guangxi.html": {"province": "guangxi", "related": ["guilin-diecai-mountain.html","guilin-li-river.html","guilin-elephant-trunk-hill.html","yangshuo-west-street.html","longji-rice-terraces.html","liuzhou-luosifen.html","detian-waterfall.html"]},
    "guilin-diecai-mountain.html": {"province": "guangxi", "related": ["guangxi.html","guilin-li-river.html","guilin-elephant-trunk-hill.html","yangshuo-west-street.html"]},
    "chongqing-rail-tunnel.html": {"province": "chongqing", "related": []},
}

PROVINCE_GUIDE_MAP = {
    "guangxi": ["guangxi.html","guilin-li-river.html","guilin-elephant-trunk-hill.html","guilin-diecai-mountain.html","yangshuo-west-street.html","longji-rice-terraces.html","liuzhou-luosifen.html","detian-waterfall.html"],
    "chongqing": ["chongqing-rail-tunnel.html"],
}

def clean(t):
    if not t:
        return ""
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def extract_meta(text):
    title = ""
    m = re.search(r"<title>(.*?)</title>", text, re.S|re.I)
    if m: title = clean(m.group(1))
    desc = ""
    m = re.search(r'<meta\s+name="description"\s+content="(.*?)"', text, re.S|re.I)
    if m: desc = m.group(1)
    canon = ""
    m = re.search(r'<link\s+rel="canonical"\s+href="(.*?)"', text, re.S|re.I)
    if m: canon = m.group(1)
    return title, desc, canon

def name_from_title(title):
    if " | " in title:
        return title.split(" | ")[0].strip()
    return title

def faq_guide(text):
    h2s = list(re.finditer(r"<h2[^>]*>(.*?)</h2>", text, re.S|re.I))
    out = []
    for i, m in enumerate(h2s):
        q = clean(m.group(1))
        start = m.end()
        end = h2s[i+1].start() if i+1 < len(h2s) else len(text)
        seg = text[start:end]
        pm = re.search(r"<p[^>]*>(.*?)</p>", seg, re.S|re.I)
        a = clean(pm.group(1)) if pm else ""
        a = a[:260]
        if q and a:
            out.append((q, a))
    return out

def faq_province(text, slug):
    m = re.search(r'<script id="province-data" type="application/json">(.*?)</script>', text, re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
    except Exception:
        return []
    prov = next((p for p in data if p.get("slug") == slug), None)
    if not prov:
        return []
    name = prov.get("nameEn", "")
    hookData = prov.get("hookData", "")
    desc = prov.get("description", "")
    faqs = []
    if hookData:
        faqs.append((f"What is {name}, China known for?", hookData[:400]))
    if desc:
        faqs.append((f"Why should I visit {name}, China?", desc[:400]))
    return faqs

def breadcrumb(canon, page_type, name):
    if page_type == "guide":
        cat_url, cat_name = SITE + "/guides/", "Travel Guides"
    else:
        cat_url, cat_name = SITE + "/province/", "Provinces"
    return [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": cat_name, "item": cat_url},
        {"@type": "ListItem", "position": 3, "name": name, "item": canon},
    ]

def build_graph(title, desc, canon, page_type, name, faqs):
    article = {
        "@type": "Article",
        "headline": title,
        "description": desc,
        "url": canon,
        "author": {"@type": "Organization", "name": "Deep in China"},
        "publisher": {"@type": "Organization", "name": "Deep in China",
                      "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/channel-avatar.png"}},
        "inLanguage": "en",
    }
    travel = {
        "@type": "TravelGuide",
        "name": name,
        "description": desc,
        "url": canon,
        "author": {"@type": "Organization", "name": "Deep in China"},
        "publisher": {"@type": "Organization", "name": "Deep in China"},
        "inLanguage": "en",
    }
    graph = [article, travel, {"@type": "BreadcrumbList", "itemListElement": breadcrumb(canon, page_type, name)}]
    if faqs:
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ],
        })
    return {"@context": "https://schema.org", "@graph": graph}

def related_guide(province, related):
    items = ""
    for g in related:
        t = g.replace(".html", "").replace("-", " ").title()
        items += f'      <li><a href="../guides/{g}">{t}</a></li>\n'
    items += f'      <li><a href="../province/{province}.html">&larr; Back to {province.title()} province</a></li>\n'
    return ('<section class="related-guides" style="margin-top:2.5rem;padding-top:1.5rem;border-top:1px solid #e5e5e5">\n'
            '  <h2>More travel guides</h2>\n  <ul class="related-list">\n' + items + '  </ul>\n</section>\n')

def related_province(guides_list):
    if not guides_list:
        return ""
    items = ""
    for g in guides_list:
        t = g.replace(".html", "").replace("-", " ").title()
        items += f'      <li><a href="../guides/{g}">{t}</a></li>\n'
    return ('<section class="related-guides" style="margin-top:2.5rem;padding-top:1.5rem;border-top:1px solid #e5e5e5">\n'
            '  <h2>Travel guides for this region</h2>\n  <ul class="related-list">\n' + items + '  </ul>\n</section>\n')

def process(filepath, page_type, slug, meta_dict=None, dry=False):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    if 'application/ld+json' in text:
        print(f"  [SKIP-schema] 已存在 JSON-LD: {filepath}")
        return False
    title, desc, canon = extract_meta(text)
    name = name_from_title(title)
    if page_type == "guide":
        faqs = faq_guide(text)
    else:
        faqs = faq_province(text, slug)
    graph = build_graph(title, desc, canon, page_type, name, faqs)
    ld = '<script type="application/ld+json">\n' + json.dumps(graph, ensure_ascii=False, indent=2) + "\n</script>\n"

    related_html = ""
    if page_type == "guide" and meta_dict:
        related_html = related_guide(meta_dict["province"], meta_dict["related"])
    elif page_type == "province" and slug in PROVINCE_GUIDE_MAP:
        related_html = related_province(PROVINCE_GUIDE_MAP[slug])

    if dry:
        print(f"\n=== DRY: {filepath} ===")
        print(f"  title={title!r} name={name!r} canon={canon!r}")
        print(f"  FAQ条数={len(faqs)}: " + " | ".join(q for q,_ in faqs)[:200])
        print(f"  related区块={'有' if related_html else '无'}")
        return True

    # 注入: </head> 前插 JSON-LD; </body> 前插内链
    if "</head>" in text:
        text = text.replace("</head>", ld + "</head>", 1)
    else:
        text = text.replace("</html>", ld + "</html>", 1)
    if related_html:
        if "</body>" in text:
            text = text.replace("</body>", related_html + "</body>", 1)
        else:
            text = text.replace("</html>", related_html + "</html>", 1)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  [OK] 注入 schema({len(graph['@graph'])}块,FAQ={len(faqs)}) + 内链({'有' if related_html else '无'}): {os.path.basename(filepath)}")
    return True

def main():
    dry = "--dry" in sys.argv
    print(f"模式: {'DRY-RUN(不写文件)' if dry else '实际注入'}")
    # guides
    for g, meta in GUIDES.items():
        fp = os.path.join(BASE, "guides", g)
        if os.path.exists(fp):
            process(fp, "guide", None, meta, dry)
        else:
            print(f"  [MISS] guides/{g}")
    # provinces
    prov_dir = os.path.join(BASE, "province")
    for fn in sorted(os.listdir(prov_dir)):
        if fn.endswith(".html"):
            slug = fn[:-5]
            fp = os.path.join(prov_dir, fn)
            process(fp, "province", slug, None, dry)

if __name__ == "__main__":
    main()
