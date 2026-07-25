#!/usr/bin/env python3
"""
Deep in China — 频道最新视频同步脚本 (零 API key 版)
读取 YouTube 频道 RSS, 生成 data/videos.json 供网站首页展示。

依赖: 仅 Python 标准库 (urllib / xml / json / re)

用法:
  python scripts/update_site_videos.py                  # 自动解析频道并生成
  python scripts/update_site_videos.py --channel-id UCxxxx   # 指定频道 ID (首次或自动解析失败时用)
  python scripts/update_site_videos.py --limit 12       # 控制条数 (默认 12)
  python scripts/update_site_videos.py --dry-run        # 只打印不写文件

建议触发方式:
  - Hermes 每次上传完视频后调用本脚本 (写 videos.json)
  - 或定时任务 (cron) 每天跑一次, 保持首页最新
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
META_PATH = os.path.join(DATA_DIR, "channel_meta.json")
OUT_PATH = os.path.join(DATA_DIR, "videos.json")

HANDLE = "DeepinChina-n"                       # 频道 handle (不含 @)
CHANNEL_URL = f"https://www.youtube.com/@{HANDLE}"
SEED_VIDEO = "vHnChq2XrBE"                     # 已知视频 ID, 用于 oembed 兜底确认
UA = "Mozilla/5.0"

ATOM = "{http://www.w3.org/2005/Atom}"
YT = "{http://www.youtube.com/xml/schemas/2015}"
MEDIA = "{http://search.yahoo.com/mrss/}"


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def _save_meta(cid):
    try:
        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump({
                "channel_id": cid,
                "handle": HANDLE,
                "updated": datetime.now(timezone.utc).isoformat(),
            }, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def resolve_channel_id(arg_id=None):
    """按优先级拿 channel_id: 参数 > 缓存 > 抓主页解析 > 报错指引。"""
    if arg_id:
        return arg_id
    if os.path.exists(META_PATH):
        try:
            with open(META_PATH, encoding="utf-8") as f:
                cid = json.load(f).get("channel_id")
                if cid:
                    return cid
        except Exception:
            pass
    try:
        html = fetch(CHANNEL_URL)
        m = re.search(r'channelId"\s*:\s*"(UC[0-9A-Za-z_-]{22})"', html)
        if m:
            cid = m.group(1)
            _save_meta(cid)
            return cid
    except Exception as e:
        print(f"[warn] 频道主页解析失败: {e}", file=sys.stderr)
    raise SystemExit(
        "无法自动获取 channel_id。请二选一:\n"
        "  a) 在 YouTube Studio → 自定义频道 → 设置/网址 里复制 UC 开头的频道 ID, 然后运行:\n"
        "       python scripts/update_site_videos.py --channel-id UCxxxx\n"
        "  b) 直接把 UCxxxx 发给我, 我写进 data/channel_meta.json\n"
        "(之后本脚本会自动缓存, 无需再次指定)"
    )


def parse_feed(xml_text):
    root = ET.fromstring(xml_text)
    out = []
    for entry in root.findall(ATOM + "entry"):
        vid = (entry.findtext(YT + "videoId") or "").strip()
        title = (entry.findtext(ATOM + "title") or "").strip()
        published = (entry.findtext(ATOM + "published") or "").strip()
        link = ""
        for l in entry.findall(ATOM + "link"):
            if l.get("rel") == "alternate":
                link = l.get("href") or ""
        thumb = ""
        group = entry.find(MEDIA + "group")
        if group is not None:
            t = group.find(MEDIA + "thumbnail")
            if t is not None:
                thumb = t.get("url") or ""
        if not thumb and vid:
            thumb = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
        if not link and vid:
            link = f"https://www.youtube.com/watch?v={vid}"
        if published:
            published = published[:10]  # 取 YYYY-MM-DD
        out.append({
            "id": vid,
            "title": title,
            "thumbnail": thumb,
            "published": published,
            "url": link,
        })
    return out


def main():
    p = argparse.ArgumentParser(description="Sync latest YouTube videos to data/videos.json")
    p.add_argument("--channel-id", help="YouTube channel ID (UCxxxx), 首次/解析失败时使用")
    p.add_argument("--limit", type=int, default=12, help="保留最新条数 (默认 12)")
    p.add_argument("--dry-run", action="store_true", help="只打印不写文件")
    args = p.parse_args()

    cid = resolve_channel_id(args.channel_id)
    print(f"[info] channel_id = {cid}")

    feed_url = ("https://www.youtube.com/feeds/videos.xml?channel_id="
                + urllib.parse.quote(cid))
    xml_text = fetch(feed_url)
    videos = parse_feed(xml_text)
    videos = videos[: args.limit]
    print(f"[info] 解析到 {len(videos)} 条视频")

    if args.dry_run:
        print(json.dumps(videos, indent=2, ensure_ascii=False))
        return

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)
    print(f"[ok] 已写入 {OUT_PATH} ({len(videos)} 条)")


if __name__ == "__main__":
    main()
