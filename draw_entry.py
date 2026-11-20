#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024, JPEG bytes).

Written from scratch in this session with Pillow. Layout: masthead naming
the day, four story panels in a 2x2 grid (each with a flat pictogram, a
bold headline and a short factual caption), and an "Also today" footer
strip. Run: python3 draw_entry.py  -> writes entry.png next to this file.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
PAPER = (248, 244, 233)
INK = (28, 28, 28)
GREY = (96, 92, 82)
RED = (163, 29, 29)
RULE = (60, 58, 52)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spaced_text(draw, cx, y, text, fnt, fill, tracking=4):
    """Draw text centred on cx with extra letter spacing."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def draw_scales(d, cx, top, h, colour):
    """Simple scales of justice, centred on cx, spanning height h."""
    base_y = top + h
    # base and post
    d.rectangle([cx - 52, base_y - 8, cx + 52, base_y], fill=colour)
    d.rectangle([cx - 4, top + 18, cx + 4, base_y - 8], fill=colour)
    # top finial
    d.ellipse([cx - 7, top + 6, cx + 7, top + 20], fill=colour)
    # beam
    d.rectangle([cx - 92, top + 20, cx + 92, top + 27], fill=colour)
    for sign in (-1, 1):
        px = cx + sign * 92
        # hanging strings
        d.line([px - 26, top + 27, px, top + 62], fill=colour, width=3)
        d.line([px + 26, top + 27, px, top + 62], fill=colour, width=3)
        d.line([px, top + 27, px, top + 62], fill=colour, width=3)
        # pan (half-disc)
        d.pieslice([px - 30, top + 56, px + 30, top + 92], 0, 180, fill=colour)
        d.rectangle([px - 30, top + 56, px + 30, top + 60], fill=colour)


def draw_cyclone(d, x, y, w, h, colour, rain=(70, 110, 130)):
    """Spiral storm with rain streaks and sea waves."""
    cx, cy = x + w // 2, y + h // 2 - 6
    for i, r in enumerate(range(12, 62, 10)):
        start = i * 55
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 230,
              fill=colour, width=5)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=colour)
    # rain streaks on both sides
    for rx in (x + 18, x + 44, x + w - 52, x + w - 26):
        for k in range(3):
            yy = y + 8 + k * 26
            d.line([rx, yy, rx - 8, yy + 16], fill=rain, width=3)
    # sea waves at the bottom
    for k, wy in enumerate((y + h - 26, y + h - 12)):
        pts = []
        for xx in range(x + 8, x + w - 8, 12):
            pts.append((xx, wy + (6 if (xx // 12 + k) % 2 else -2)))
        d.line(pts, fill=rain, width=3)


def draw_kyiv(d, x, y, w, h, dark=(52, 52, 52), fire=(217, 108, 30)):
    """City skyline, missile trails and an impact burst."""
    base = y + h - 14
    heights = [58, 84, 66, 96, 72, 108, 62, 88]
    bw = w // len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw + 4
        d.rectangle([bx, base - hh, bx + bw - 8, base], fill=dark)
        # lit windows
        for wy in range(base - hh + 8, base - 8, 16):
            for wx in (bx + 6, bx + bw - 16):
                d.rectangle([wx, wy, wx + 5, wy + 6], fill=(248, 220, 130))
    # missile trails (diagonal, from upper right)
    d.line([x + w - 30, y + 6, x + w - 150, y + 78], fill=(255, 255, 255), width=6)
    d.line([x + w - 60, y + 2, x + w - 190, y + 66], fill=(255, 255, 255), width=4)
    # impact burst
    ex, ey = x + w - 168, y + 82
    for ang in range(0, 360, 30):
        r = 26 if ang % 60 == 0 else 15
        a = math.radians(ang)
        d.line([ex, ey, ex + r * math.cos(a), ey + r * math.sin(a)],
               fill=fire, width=5)
    d.ellipse([ex - 11, ey - 11, ex + 11, ey + 11], fill=(255, 190, 60))
    # smoke
    d.ellipse([ex - 34, ey - 44, ex - 8, ey - 20], fill=(120, 116, 108))
    d.ellipse([ex + 2, ey - 50, ex + 26, ey - 28], fill=(140, 136, 128))


def draw_chart(d, x, y, w, h, colour=(30, 122, 52)):
    """Rising market line with an arrowhead and a value tag."""
    # faint grid (below the value tag and ticker label)
    for gy in (y + 58, y + 86, y + 114):
        d.line([x + 10, gy, x + w - 10, gy], fill=(190, 196, 180), width=1)
    pts = [(x + 14, y + 104), (x + 70, y + 96), (x + 126, y + 100),
           (x + 182, y + 74), (x + 238, y + 78), (x + 294, y + 46),
           (x + 350, y + 50), (x + 406, y + 18)]
    d.line(pts, fill=colour, width=6, joint="curve")
    for px, py in pts[1:-1]:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=colour)
    # arrowhead at the end
    ex, ey = pts[-1]
    d.polygon([(ex, ey - 2), (ex - 16, ey - 12), (ex - 16, ey + 8)],
              fill=colour)
    # value tag
    tag = "+17%"
    tf = font(SANS_B, 34)
    tw = d.textlength(tag, font=tf)
    tx = x + w - tw - 18
    d.rounded_rectangle([tx - 10, y + 8, tx + tw + 10, y + 48],
                        radius=8, fill=colour)
    d.text((tx, y + 10), tag, font=tf, fill=(255, 255, 255))
    d.text((x + 14, y + 8), "ANT  $97.17", font=font(SANS_B, 22),
           fill=(60, 60, 60))


def panel(d, x, y, w, hgt, kicker, tint, pict, headline, caption, accent):
    d.rectangle([x, y, x + w, y + hgt], outline=INK, width=2)
    d.text((x + 16, y + 12), kicker, font=font(SANS_B, 17), fill=RED)
    px, py, pw, ph = x + 16, y + 42, w - 32, 128
    d.rectangle([px, py, px + pw, py + ph], fill=tint)
    pict(d, px, py, pw, ph)
    hy = y + 42 + 128 + 12
    for i, line in enumerate(wrap(d, headline, font(SANS_B, 29), w - 32)):
        d.text((x + 16, hy + i * 34), line, font=font(SANS_B, 29), fill=INK)
    cy = hy + 34 * min(2, len(wrap(d, headline, font(SANS_B, 29), w - 32))) + 6
    for i, line in enumerate(wrap(d, caption, font(SANS, 19), w - 32)):
        d.text((x + 16, cy + i * 24), line, font=font(SANS, 19), fill=(52, 50, 46))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    spaced_text(d, W // 2, 24, "THE WORLD IN ONE IMAGE", font(SANS_B, 24),
                GREY, tracking=6)
    d.text((W // 2, 56), "FRIDAY 20 NOVEMBER 2026", font=font(SERIF_B, 56),
           fill=INK, anchor="ma")
    d.line([28, 128, W - 28, 128], fill=RULE, width=3)
    d.line([28, 134, W - 28, 134], fill=RULE, width=1)
    d.text((W // 2, 146), "Four stories that defined the day — The Hague · Odisha · Kyiv · New York",
           font=font(SANS, 20), fill=GREY, anchor="ma")

    # ---- four panels, 2x2 ----
    pw, ph = 476, 330
    gx, gy = 28, 184
    panel(d, gx, gy, pw, ph, "JUSTICE  ·  THE HAGUE", (232, 228, 216),
          lambda dd, x, y, w, h: draw_scales(dd, x + w // 2, y + 8, h - 24, (46, 64, 87)),
          "UN court: Myanmar committed genocide",
          "World Court rules 9–6 that the 2017 campaign against the Rohingya was genocide; orders reparations.",
          RED)
    panel(d, gx + pw + 16, gy, pw, ph, "WEATHER  ·  INDIA", (220, 235, 232),
          lambda dd, x, y, w, h: draw_cyclone(dd, x, y, w, h, (31, 111, 107)),
          "Cyclone Akvan hits India's east coast",
          "Landfall near Gopalpur by noon; about 300,000 people moved to shelters as winds hit 110 km/h.",
          RED)
    panel(d, gx, gy + ph + 16, pw, ph, "WAR  ·  UKRAINE", (232, 224, 210),
          lambda dd, x, y, w, h: draw_kyiv(dd, x, y, w, h),
          "Missiles strike Kyiv in the early hours",
          "Ballistic missiles hit several districts overnight; fires in Obolonskyi after debris falls.",
          RED)
    panel(d, gx + pw + 16, gy + ph + 16, pw, ph, "MARKETS  ·  NEW YORK", (226, 236, 221),
          lambda dd, x, y, w, h: draw_chart(dd, x, y, w, h),
          "Anthropic's record IPO closes up 17%",
          "$83 a share to $97.17; $81bn raised — the largest listing ever, worth about $1.8 trillion.",
          RED)

    # ---- footer strip ----
    fy = gy + 2 * ph + 16 + 18
    d.line([28, fy, W - 28, fy], fill=RULE, width=2)
    d.text((28, fy + 10), "ALSO TODAY", font=font(SANS_B, 18), fill=RED)
    items = [
        "Houthi missile hits a Riyadh tower",
        "Tanker on fire after mine hit near Hormuz",
        "Genoa airport halts flights over drones",
        "US Senate rejects Iran war-powers vote, 51–48",
        "Trump pardons baseball great Pete Rose",
        "Europe ready for talks with Russia",
    ]
    col_w = (W - 56) // 2
    for i, item in enumerate(items):
        col = i % 2
        row = i // 2
        ix = 28 + col * col_w
        iy = fy + 40 + row * 26
        d.rectangle([ix, iy + 5, ix + 8, iy + 13], fill=RED)
        for j, line in enumerate(wrap(d, item, font(SANS, 17), col_w - 24)):
            d.text((ix + 16, iy + j * 22), line, font=font(SANS, 17), fill=INK)
    d.text((W // 2, H - 26),
           "Drawn from reports by Reuters, BBC, The Hindu and the India Meteorological Department.",
           font=font(SANS, 14), fill=GREY, anchor="ma")

    img.save(OUT, "JPEG", quality=88)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
