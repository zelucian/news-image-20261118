"""Render the November 18, 2026 news page; Pillow is build-time only."""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SCALE = 2
PAPER = "#f7f2e7"
INK = "#141414"
RED = "#a31e22"
RULE = "#b9b2a5"
image = Image.new("RGB", (1024 * SCALE, 1024 * SCALE), PAPER)
canvas = ImageDraw.Draw(image)


def font(size, family="sans", bold=False):
    stem = "DejaVuSerif" if family == "serif" else "DejaVuSans"
    filename = stem + ("-Bold" if bold else "") + ".ttf"
    candidates = [
        Path("/usr/share/fonts/truetype/dejavu") / filename,
        Path("/usr/share/fonts/dejavu") / filename,
        Path("/usr/local/share/fonts") / filename,
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size * SCALE)
    try:
        return ImageFont.truetype(filename, size * SCALE)
    except OSError:
        return ImageFont.load_default(size=size * SCALE)


def text(position, value, size, family="sans", bold=False, fill=INK):
    canvas.text(tuple(coordinate * SCALE for coordinate in position), value,
                font=font(size, family, bold), fill=fill, anchor="lt")


def width(value, size, family="sans", bold=False):
    return canvas.textlength(value, font=font(size, family, bold)) / SCALE


def wrapped(position, value, max_width, size, leading, family="sans", bold=False,
            bottom=None, fill=INK):
    lines = []
    for paragraph in value.split("\n"):
        current = ""
        for word in paragraph.split():
            proposed = f"{current} {word}".strip()
            if width(proposed, size, family, bold) > max_width:
                if not current:
                    raise ValueError(f"Word exceeds column: {word}")
                lines.append(current)
                current = word
            else:
                current = proposed
        lines.append(current)
    x_position, y_position = position
    if bottom is not None and y_position + len(lines) * leading > bottom:
        raise ValueError(f"Text exceeds panel: {value!r}")
    for line_number, line_value in enumerate(lines):
        text((x_position, y_position + line_number * leading), line_value,
             size, family, bold, fill)
    return y_position + len(lines) * leading


def line(points, fill=INK, thickness=1):
    canvas.line([(int(x * SCALE), int(y * SCALE)) for x, y in points],
                fill=fill, width=max(1, int(thickness * SCALE)))


def rectangle(bounds, fill=None, outline=INK, thickness=1):
    canvas.rectangle(tuple(int(value * SCALE) for value in bounds), fill=fill,
                     outline=outline, width=max(1, int(thickness * SCALE)))


def ellipse(bounds, fill=None, outline=INK, thickness=1):
    canvas.ellipse(tuple(int(value * SCALE) for value in bounds), fill=fill,
                   outline=outline, width=max(1, int(thickness * SCALE)))


def polygon(points, fill=INK):
    canvas.polygon([(int(x * SCALE), int(y * SCALE)) for x, y in points], fill=fill)


def waves(x_position, y_position, span, rows=2):
    for row in range(rows):
        points = [(x_position + offset, y_position + row * 8 +
                   2 * math.sin(offset * math.pi / 15))
                  for offset in range(span + 1)]
        line(points, thickness=1.5)


def burst(center_x, center_y, radius, fill=RED):
    points = []
    for index in range(24):
        angle = index * math.pi / 12
        distance = radius if index % 2 == 0 else radius * 0.47
        points.append((center_x + math.cos(angle) * distance,
                       center_y + math.sin(angle) * distance))
    polygon(points, fill)


def gulf_icon(x_position, y_position):
    arc = [(x_position + offset, y_position + 30 -
            30 * math.sin(offset / 98 * math.pi)) for offset in range(99)]
    line(arc, RED, 2)
    polygon([(x_position + 98, y_position + 30),
             (x_position + 86, y_position + 23),
             (x_position + 91, y_position + 18)], RED)
    burst(x_position + 98, y_position + 48, 19)
    waves(x_position, y_position + 74, 125, 3)


def bridge_icon(x_position, y_position):
    for offset in (8, 70):
        line([(x_position + offset, y_position + 18),
              (x_position + offset, y_position + 67)], thickness=4)
    line([(x_position, y_position + 30), (x_position + 30, y_position + 30)], thickness=5)
    line([(x_position + 62, y_position + 30),
          (x_position + 84, y_position + 30)], thickness=5)
    line([(x_position + 30, y_position + 49),
          (x_position + 66, y_position + 70)], thickness=5)
    line([(x_position + 8, y_position + 18),
          (x_position + 30, y_position + 29)], thickness=1.5)
    line([(x_position + 70, y_position + 18),
          (x_position + 62, y_position + 29)], thickness=1.5)
    waves(x_position, y_position + 70, 84)
    for bounds, start, end in (((50, 60, 63, 75), 190, 280),
                               ((66, 59, 80, 75), 260, 350),
                               ((59, 56, 71, 69), 200, 340)):
        canvas.arc(tuple(int(value * SCALE) for value in
                         (x_position + bounds[0], y_position + bounds[1],
                          x_position + bounds[2], y_position + bounds[3])),
                   start, end, fill=INK, width=2 * SCALE)


def summit_icon(x_position, y_position):
    for index in range(3):
        left = x_position + index * 29
        top = y_position + (0 if index == 1 else 12)
        line([(left, top), (left, y_position + 87)], thickness=1.5)
        if index == 0:
            rectangle((left + 1, top, left + 25, top + 25), RED, None)
            burst(left + 7, top + 6, 3.5, "#f7de82")
        elif index == 1:
            for stripe, color in enumerate(("#ffffff", "#34547b", "#a31e22")):
                rectangle((left + 1, top + stripe * 9,
                           left + 25, top + stripe * 9 + 9), color, None)
        else:
            for stripe in range(7):
                rectangle((left + 1, top + stripe * 4,
                           left + 25, top + stripe * 4 + 4),
                          RED if stripe % 2 == 0 else PAPER, None)
            rectangle((left + 1, top, left + 12, top + 15), "#34547b", None)
    line([(x_position - 3, y_position + 87),
          (x_position + 86, y_position + 87)], thickness=2)


def ballot_icon(x_position, y_position):
    rectangle((x_position + 15, y_position + 1, x_position + 57, y_position + 42), PAPER, INK, 2)
    line([(x_position + 25, y_position + 20),
          (x_position + 32, y_position + 27),
          (x_position + 48, y_position + 11)], RED, 3)
    rectangle((x_position + 1, y_position + 36, x_position + 77, y_position + 85), PAPER, INK, 2)
    line([(x_position + 20, y_position + 43),
          (x_position + 58, y_position + 43)], thickness=3)
    text((x_position + 6, y_position + 57), "56–44", 20, bold=True)


def health_icon(x_position, y_position):
    center_x, center_y = x_position + 33, y_position + 34
    for index in range(10):
        angle = index * math.pi / 5
        outer_x, outer_y = center_x + 30 * math.cos(angle), center_y + 30 * math.sin(angle)
        line([(center_x + 20 * math.cos(angle), center_y + 20 * math.sin(angle)),
              (outer_x, outer_y)], RED, 2)
        ellipse((outer_x - 3, outer_y - 3, outer_x + 3, outer_y + 3), RED, None)
    ellipse((center_x - 21, center_y - 21, center_x + 21, center_y + 21), PAPER, RED, 2)
    for offset_x, offset_y in ((-8, -6), (6, -9), (3, 7)):
        ellipse((center_x + offset_x - 2, center_y + offset_y - 2,
                 center_x + offset_x + 2, center_y + offset_y + 2), RED, None)
    ellipse((x_position + 56, y_position + 53, x_position + 79, y_position + 76), INK, None)
    polygon([(x_position + 57, y_position + 69),
             (x_position + 78, y_position + 69),
             (x_position + 67.5, y_position + 89)])
    ellipse((x_position + 63, y_position + 60, x_position + 72, y_position + 69), PAPER, None)


def voyager_icon(x_position, y_position):
    ellipse((x_position + 11, y_position + 11, x_position + 48, y_position + 27), PAPER, INK, 3)
    line([(x_position + 29, y_position + 19), (x_position + 40, y_position + 39),
          (x_position + 55, y_position + 44)], thickness=3)
    rectangle((x_position + 36, y_position + 32, x_position + 49, y_position + 43), INK)
    line([(x_position + 44, y_position + 35), (x_position + 77, y_position + 14)], thickness=2.5)
    line([(x_position + 40, y_position + 40), (x_position + 14, y_position + 55)], thickness=2.5)
    for star_x, star_y in ((4, 4), (73, 45), (58, 1), (92, 27)):
        line([(x_position + star_x - 3, y_position + star_y),
              (x_position + star_x + 3, y_position + star_y)], thickness=1.5)
        line([(x_position + star_x, y_position + star_y - 3),
              (x_position + star_x, y_position + star_y + 3)], thickness=1.5)


def panel(x_position, y_position, kicker, headline, summary, icon):
    text((x_position, y_position), kicker, 17, bold=True, fill=RED)
    headline_end = wrapped((x_position, y_position + 27), headline, 350,
                           29, 33, "serif", True, bottom=y_position + 96)
    wrapped((x_position, headline_end + 9), summary, 351, 19, 23,
            bottom=y_position + 166)
    icon(x_position + 370, y_position + 31)


text((36, 29), "THE WORLD IN ONE DAY", 16, bold=True)
line([(36, 55), (988, 55)], RED, 3)
for date_line, date_y in (("WEDNESDAY 18", 66), ("NOVEMBER 2026", 123)):
    text(((1024 - width(date_line, 54, "serif", True)) / 2, date_y),
         date_line, 54, "serif", True)
line([(36, 185), (988, 185)], thickness=1.5)

text((36, 198), "GULF / U.S. & IRAN", 17, bold=True, fill=RED)
wrapped((36, 224), "U.S. strikes Iran;\nTehran hits back in Gulf", 800,
        36, 41, "serif", True, bottom=307)
gulf_icon(850, 207)
wrapped((36, 312),
        "U.S. hit a Qeshm Island missile site Tuesday; Iran answered with drones at "
        "U.S.-linked targets in Bahrain and Kuwait, and attacks on shipping near the Strait of Hormuz.",
        952, 19, 23, bottom=381)
line([(36, 385), (988, 385)], thickness=1.5)

panel(36, 397, "UKRAINE", "Kerch Bridge\nspan collapses",
      "Ukraine hits for a second day;\nroad span falls into the strait.", bridge_icon)
panel(532, 397, "CHINA / DIPLOMACY", "Xi and Putin meet\nin Shenzhen",
      "Donald Trump arrives ahead of\nThursday’s trilateral summit.", summit_icon)
line([(512, 398), (512, 734)], RULE)
line([(36, 565), (988, 565)], RULE)
panel(36, 579, "U.S. SENATE", "Peltola wins Alaska\nSenate seat",
      "Mary Peltola gives Democrats\na 56–44 Senate majority.", ballot_icon)
panel(532, 579, "HEALTH / DR CONGO", "Ebola passes\n11,000 cases",
      "Second-largest outbreak;\nchildren hit hardest.", health_icon)
line([(36, 749), (988, 749)], RED, 2)

text((36, 762), "ALSO TODAY", 17, bold=True, fill=RED)
text((36, 790), "VOYAGER 1 REACHES ONE LIGHT-DAY", 28, "serif", True)
text((36, 825), "From Earth: about 16 billion miles. A first for any human-made object.", 19)
voyager_icon(882, 778)
line([(36, 853), (988, 853)], RULE)

briefs = [
    ("MEASLES", "U.S. loses elimination status after 26 years; over 5,400 cases in 2026."),
    ("NVIDIA", "Record $115.8B quarter; board rejects Huang’s return as CEO."),
    ("OPENAI", "GPT-6.2 Astra and Sol launch."),
    ("CYCLONE XAVIER", "Category 5 hits the Northern Cook Islands."),
    ("SIBERIA", "Russian military plane crashes; 19 killed."),
    ("CAMBRIDGE", "Word of the Year 2026: “Human”."),
]
for brief_index, (label, clause) in enumerate(briefs):
    brief_y = 864 + brief_index * 22
    label_text = label + " · "
    label_width = width(label_text, 19, bold=True)
    if label_width + width(clause, 19) > 952:
        raise ValueError(f"Brief exceeds column: {label}")
    text((36, brief_y), label_text, 19, bold=True)
    text((36 + label_width, brief_y), clause, 19)
line([(36, 1001), (988, 1001)], thickness=1)

image = image.resize((1024, 1024), Image.Resampling.LANCZOS)
image.save(ROOT / "entry.png", format="PNG", optimize=True)
print(f"Wrote {ROOT / 'entry.png'}")
