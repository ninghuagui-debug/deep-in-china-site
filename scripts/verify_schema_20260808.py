#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 P0 注入: JSON-LD 合法性 + 敏感省 FAQ 含 China + 内链区块"""
import re, json, os
BASE = "C:/Users/WWW/WorkBuddy/wb网页/deep-in-china-site"
GUIDES = ["guangxi.html", "guilin-diecai-mountain.html", "chongqing-rail-tunnel.html"]
SENS = ["taiwan", "hong-kong", "macao", "tibet", "xinjiang"]

ok = bad = 0
faq_missing = []
rel_guide = rel_prov = 0

for g in GUIDES:
    t = open(os.path.join(BASE, "guides", g), encoding="utf-8").read()
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    if not m:
        bad += 1; print("NO LD", g); continue
    try:
        d = json.loads(m.group(1))
    except Exception as e:
        bad += 1; print("BAD JSON", g, e); continue
    ok += 1
    has = "related-guides" in t
    rel_guide += 1 if has else 0
    print(f"guide {g:32} blocks={len(d['@graph'])} FAQ={len([x for x in d['@graph'] if x['@type']=='FAQPage'][0]['mainEntity']) if any(x['@type']=='FAQPage' for x in d['@graph']) else 0} related={has}")

for fn in sorted(os.listdir(os.path.join(BASE, "province"))):
    if not fn.endswith(".html"):
        continue
    slug = fn[:-5]
    t = open(os.path.join(BASE, "province", fn), encoding="utf-8").read()
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    if not m:
        bad += 1; continue
    try:
        d = json.loads(m.group(1))
    except Exception:
        bad += 1; continue
    ok += 1
    has = "related-guides" in t
    rel_prov += 1 if has else 0
    faqs = [x for x in d["@graph"] if x["@type"] == "FAQPage"]
    if slug in SENS and faqs:
        for q in faqs[0]["mainEntity"]:
            if "China" not in q["name"]:
                faq_missing.append((slug, q["name"]))

print(f"\n合法JSON-LD文件数: {ok}  失败: {bad}")
print(f"guide内链区块: {rel_guide}/3   province内链区块: {rel_prov}/34")
if faq_missing:
    print("*** 敏感省FAQ缺China:", faq_missing)
else:
    print("敏感省(台/港/澳/藏/疆)FAQ全部含China ✅")
