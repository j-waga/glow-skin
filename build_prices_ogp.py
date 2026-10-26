# -*- coding: utf-8 -*-
"""glow_prices.html の OGP 画像（1200×630）を prices.json の実数から組む。
⛔️商品画像は使わない。⛔️Amazonの価格は出さない。★数字はすべて prices.json から。"""
import json, os, datetime
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 630
BG = (251, 249, 247)
INK = (42, 39, 36)
SUB = (109, 103, 95)
ACC = (192, 57, 43)
GOLD = (201, 168, 108)
LINE = (236, 231, 226)
FP = "/usr/share/fonts/opentype/noto/NotoSansCJK-%s.ttc"
FS = "/usr/share/fonts/opentype/noto/NotoSerifCJK-%s.ttc"


def F(sz, w="Regular", serif=False):
    return ImageFont.truetype((FS if serif else FP) % w, sz, index=0)


def tw(d, t, f):
    b = d.textbbox((0, 0), t, font=f)
    return b[2] - b[0], b[3] - b[1]


def main():
    d = json.load(open(os.path.join(HERE, "prices.json"), encoding="utf-8"))
    items = d["items"]
    gen = datetime.datetime.fromisoformat(d["generated_at"])
    asof = f"{gen.year}年{gen.month}月{gen.day}日 調べ"
    rak = sum(1 for v in items.values() if v["live"]["media"] == "楽天")
    yah = len(items) - rak
    moved = sum(1 for v in items.values()
                if v["live"].get("prev_note") or v["live"]["total"] != v["live"]["prev"])
    lo = min(items.values(), key=lambda v: v["live"]["total"])["live"]["total"]
    hi = max(items.values(), key=lambda v: v["live"]["total"])["live"]["total"]

    img = Image.new("RGB", (W, H), BG)
    dr = ImageDraw.Draw(img)

    dr.rectangle([0, 0, W, 10], fill=ACC)

    # ブランド
    # ロゴの菱形（★フォントに無い記号は使わず図形で描く）
    cx, cy, r = 74, 68, 11
    dr.polygon([(cx, cy - r), (cx + r * .42, cy - r * .42), (cx + r, cy),
                (cx + r * .42, cy + r * .42), (cx, cy + r), (cx - r * .42, cy + r * .42),
                (cx - r, cy), (cx - r * .42, cy - r * .42)], fill=GOLD)
    fg = F(30, "Bold", serif=True)
    dr.text((96, 52), "Glow", font=fg, fill=ACC)
    gw, _ = tw(dr, "Glow", fg)
    dr.text((96 + gw + 18, 60), "glow.stats-log.net", font=F(20, "Regular"), fill=SUB)

    # 見出し
    dr.text((64, 132), f"スキンケア{len(items)}品は、", font=F(62, "Black", serif=True), fill=INK)
    dr.text((64, 212), "いまどこが安いのか", font=F(62, "Black", serif=True), fill=INK)

    dr.line([(64, 318), (W - 64, 318)], fill=LINE, width=2)

    dr.text((64, 344), "楽天市場とYahoo!ショッピングを、送料込みの総額でそろえて毎週記録",
            font=F(27, "Medium"), fill=SUB)

    # 数字
    cards = [(f"{len(items)}", "記録した品目"),
             (f"{rak} / {yah}", "楽天 / Yahoo!"),
             (f"{moved}", "先週から動いた品"),
             (f"{lo:,}〜{hi:,}円", "総額のはば")]
    x = 64
    for n, l in cards:
        fn = F(44, "Black")
        wv, _ = tw(dr, n, fn)
        fl = F(21, "Medium")
        wl, _ = tw(dr, l, fl)
        bw = max(wv, wl) + 56
        dr.rounded_rectangle([x, 414, x + bw, 548], radius=16, fill=(255, 255, 255), outline=LINE, width=2)
        dr.text((x + (bw - wv) // 2, 440), n, font=fn, fill=INK)
        dr.text((x + (bw - wl) // 2, 500), l, font=fl, fill=SUB)
        x += bw + 18

    dr.text((64, 578), asof + "／価格・在庫は変動します／PR（アフィリエイトを含みます）",
            font=F(20, "Regular"), fill=SUB)

    out = os.path.join(HERE, "ogp_prices.png")
    img.save(out, optimize=True)
    print(f"★{out}  {img.size[0]}x{img.size[1]}  {os.path.getsize(out):,} バイト")


if __name__ == "__main__":
    main()
