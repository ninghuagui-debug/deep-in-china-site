#!/usr/bin/env python3
"""用 PIL 把频道头像/横幅设计渲染为 PNG (Windows, 依赖 hermes venv 的 PIL+numpy)。
SVG 源在 assets/img/channel-avatar.svg / channel-banner.svg, 本脚本是该设计的位图实现。
运行: <hermes-venv>/python.exe scripts/render_channel_art.py
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
FONT_DIR = "C:/Windows/Fonts"


def load_font(name, size):
    for ext in (".ttf", ".ttc"):
        p = f"{FONT_DIR}/{name}{ext}"
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size, index=0)
            except Exception:
                pass
    return ImageFont.load_default()


def vgrad(h, top, bottom):
    t = np.linspace(0, 1, h)[:, None]
    arr = (np.array(top, dtype=float) * (1 - t) + np.array(bottom, dtype=float) * t)
    return arr.astype(np.uint8)


def build_avatar():
    H = 800
    bg = vgrad(H, (15, 61, 62), (27, 107, 96))
    bg = np.broadcast_to(bg[:, None, :], (H, H, 3)).copy()
    img = Image.fromarray(bg)
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon([(0,560),(150,440),(300,545),(470,405),(640,525),(800,430),(800,800),(0,800)],
              fill=(255,255,255,45))
    d.polygon([(0,650),(210,525),(400,625),(600,500),(800,605),(800,800),(0,800)],
              fill=(255,255,255,75))
    d.text((400,408), "D", font=load_font("georgia", 430), fill=(244,247,246,255), anchor="mm")
    d.ellipse([588,122,708,242], fill=(200,16,46,255))
    d.text((648,184), "中", font=load_font("msyh", 56), fill=(255,255,255,255), anchor="mm")
    out = os.path.join(IMG, "channel-avatar.png")
    img.save(out)
    print("wrote", out)


def build_banner():
    BH = 1440
    bg = vgrad(BH, (10, 38, 48), (31, 93, 91))
    bg = np.broadcast_to(bg[:, None, :], (BH, 2560, 3)).copy()
    img = Image.fromarray(bg)
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon([(0,760),(360,560),(720,720),(1100,520),(1500,700),(1900,540),(2300,700),
               (2560,600),(2560,1440),(0,1440)], fill=(10,34,43,150))
    d.polygon([(0,900),(420,680),(860,880),(1280,660),(1720,860),(2160,680),(2560,840),
               (2560,1440),(0,1440)], fill=(16,50,59,185))
    d.polygon([(0,1060),(520,820),(1040,1040),(1560,800),(2080,1020),(2560,860),
               (2560,1440),(0,1440)], fill=(27,74,82,215))
    d.text((150,600), "Deep in China", font=load_font("georgia", 210),
           fill=(244,247,246,255), anchor="lm")
    d.text((158,730), "Go deeper than any tourist ever goes", font=load_font("georgia", 62),
           fill=(191,227,224,255), anchor="lm")
    d.text((2410,1300), "@DeepinChina-n", font=load_font("georgia", 78),
           fill=(244,247,246,255), anchor="rm")
    d.text((2410,1380), "deepinchina.com", font=load_font("georgia", 46),
           fill=(143,202,198,255), anchor="rm")
    out = os.path.join(IMG, "channel-banner.png")
    img.save(out)
    print("wrote", out)


if __name__ == "__main__":
    build_avatar()
    build_banner()
