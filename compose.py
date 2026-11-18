#!/usr/bin/env python3
"""Compose entry.png for news-image-20261117 (round 2 rebuild).

One dense newspaper front page, 1024x1024, summing up Tuesday
17 November 2026 in 43 stories: 3 illustrated leads, 10 illustrated
secondaries, a numbered world map, 30 one-line briefs, a numbers strip
and a sources line. All facts are the brief's fact-locked list.
Run: python3.12 compose.py  -> writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
MX = 28
CW = W - 2 * MX

PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (178, 34, 28)
BLUE = (28, 68, 128)
GREY = (110, 104, 92)
LIGHT = (232, 226, 210)
SEA = (205, 225, 238)
LAND = (232, 216, 184)
LAND_EDGE = (168, 148, 110)
TEAL = (0, 128, 128)
GREEN = (46, 125, 50)
ORANGE = (198, 110, 20)
PURPLE = (106, 62, 158)

FD = "/usr/share/fonts/truetype"
F_TITLE = f"{FD}/noto/NotoSerifDisplay-Black.ttf"
F_SERIFB = f"{FD}/noto/NotoSerif-Bold.ttf"
F_SERIF = f"{FD}/noto/NotoSerif-Regular.ttf"
F_SANSB = f"{FD}/noto/NotoSans-Bold.ttf"
F_SANS = f"{FD}/noto/NotoSans-Regular.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, x, y, fnt, max_w, max_lines, fill, lh=None):
    lines = wrap(draw, text, fnt, max_w)[:max_lines]
    step = lh or int(fnt.size * 1.22)
    for i, ln in enumerate(lines):
        draw.text((x, y + i * step), ln, font=fnt, fill=fill)
    return len(lines)


def fit_font(draw, text, path, size, max_w):
    f = font(path, size)
    while size > 7 and draw.textlength(text, font=f) > max_w:
        size -= 1
        f = font(path, size)
    return f


# ------------------------------------------------------------------ data
LEADS = [
    dict(n=1, kicker="EUROPE · UKRAINE WAR", color=BLUE,
         img="lead1.png", cap="KERCH STRAIT · STRUCK FOR A SECOND DAY",
         head="Ukraine says a Crimea Bridge road span fell into the sea",
         body="Second strike in two days; Zelenskyy hails an \u201cunprecedented operation\u201d. 2 killed, traffic halted."),
    dict(n=2, kicker="MIDDLE EAST · IRAN WAR", color=RED,
         img="lead2.png", cap="STRAIT OF HORMUZ · DRONES DOWNED, US STRIKES",
         head="Iran sends drones at a US radar in Bahrain; US hits back",
         body="Bahrain and the US say all were downed; US jets then strike Qeshm. Iran says tankers hit mines in Hormuz."),
    dict(n=3, kicker="ASIA · DIPLOMACY", color=PURPLE,
         img="lead3.png", cap="QUAD LEADERS\u2019 SUMMIT · MANILA",
         head="Trump holds his first Quad summit, in Manila",
         body="The four unveil critical-minerals deals; Putin reaches Shenzhen for Thursday\u2019s talks with Trump and Xi."),
]

SECOND = [
    dict(n=4, kicker="AFRICA · HEALTH", color=GREEN, cap="DR CONGO · EBOLA",
         head="Ebola cases in DR Congo top 11,000, WHO says",
         body="Cases more than doubled in three months; about 5,400 have died.", art="ebola"),
    dict(n=5, kicker="GLOBAL · CLIMATE", color=TEAL, cap="COP31 ANTALYA · ENDS FRI",
         head="COP31 divided over a fossil-fuel phase-out",
         body="Nations weigh the first draft; the Antalya talks end Friday.", art="cop"),
    dict(n=6, kicker="AMERICAS · HEALTH", color=RED, cap="MEASLES-FREE STATUS LOST",
         head="US, Mexico and Bolivia lose measles-free status",
         body="PAHO cites a year of spread; the US has 5,412 cases in 2026.", art="measles"),
    dict(n=7, kicker="US · BUSINESS", color=INK, cap="NVIDIA QUARTER · WALL STREET",
         head="Nvidia\u2019s quarterly sales double to $115.8bn",
         body="Reported after the close. Earlier the Dow fell 849 points (\u22121.6%).", art="nvidia"),
    dict(n=8, kicker="MIDDLE EAST · GAZA", color=ORANGE, cap="GAZA · WINTER AID HELD UP",
         head="Gaza truce at risk of collapse, UN is told",
         body="Board of Peace report; UN agencies say 1.4m face acute hunger.", art="gaza"),
    dict(n=9, kicker="ASIA · POLITICS", color=BLUE, cap="ULAANBAATAR · GRAFT CLAIM DENIED",
         head="Mongolia\u2019s president says he will resign",
         body="Kh\u00fcrels\u00fckh denies a $25m bribe claim; parliament must accept.", art="mongolia"),
    dict(n=10, kicker="EUROPE · POLITICS", color=BLUE, cap="BELGRADE · PARLIAMENT SWORN IN",
         head="Serbia\u2019s student-led majority takes its seats",
         body="Student List holds 140 of 250; Vu\u010di\u0107\u2019s party goes into opposition.", art="serbia"),
    dict(n=11, kicker="ASIA · LABOUR", color=GREEN, cap="DHAKA · SAVAR · GAZIPUR",
         head="Bangladesh police tear-gas garment workers",
         body="They want Tk 30,000 a month, up from 12,500; 37 factories shut.", art="bangladesh"),
    dict(n=12, kicker="RUSSIA · AIR CRASH", color=GREY, cap="KEMEROVO · ALL 19 ABOARD KILLED",
         head="Russian An-12 crash in Siberia kills all 19",
         body="The air force plane came down near Kemerovo; a fault is suspected.", art="crash"),
    dict(n=13, kicker="AFRICA · JUSTICE", color=TEAL, cap="MAPUTO · SUPREME COURT",
         head="Mozambique puts opposition leader on trial",
         body="Ven\u00e2ncio Mondlane faces 5 charges over deadly 2024 protests.", art="trial"),
]

BRIEFS = [
    (14, "Russia: says it downed a record 1,441 drones overnight"),
    (15, "Kyiv: missiles hit the North and South Dnipro bridges"),
    (16, "UN: Ukraine\u2019s civilian deaths this year top all of 2025"),
    (17, "Prague: two trains collide; 146 injured"),
    (18, "France: public-sector strike; 146,000 march (CGT: 500,000)"),
    (19, "Poland: Tusk\u2019s government survives a no-confidence vote"),
    (20, "Germany: Deutsche Bank shares fall after a huge data leak"),
    (21, "Moldova: shuts its airspace as a drone nears Chi\u0219in\u0103u"),
    (22, "Turkey: police seize opposition broadcaster S\u00f6zc\u00fc TV"),
    (23, "Football: Norway win 3\u20132 in Denmark; Haaland scores twice"),
    (24, "Vatican: Pope Leo XIV returns from his South America tour"),
    (25, "UK: sanctions 8 settlement firms and Tzav 9"),
    (26, "Israel: Eisenkot ally Matan Kahana elected speaker, 66\u201352"),
    (27, "West Bank: settlers kill a woman, 72, near Jericho"),
    (28, "Oman: Iran\u2019s Araghchi holds shipping-safety talks"),
    (29, "India: Cyclone Akvan strengthens; Odisha evacuates"),
    (30, "India: bus falls into an Uttarakhand gorge; 8 dead"),
    (31, "Japan: protests a Russian airspace intrusion near Fukuoka"),
    (32, "China\u2013Canada: more tariff cuts after Carney\u2013Xi talks"),
    (33, "Malaysia: Macron visit seals a strategic partnership"),
    (34, "Thailand: pledges to scrap tariffs on US goods"),
    (35, "South Korea: IMF lifts 2026 growth forecast to 3.9%"),
    (36, "Football: India beat Pakistan 2\u20131 in SAFF final"),
    (37, "Kenya: WFP aids 30,000 who fled Ethiopia clashes"),
    (38, "Football: Togo beat Algeria 3\u20130 in AFCON qualifier"),
    (39, "Haiti: Aristide\u2019s party will field no candidates"),
    (40, "US Senate: Van Hollen challenges Schumer for leader"),
    (41, "Australia: eases planned backpacker visa curbs"),
    (42, "Darwin: M6.6 quake off Indonesia felt; no tsunami"),
    (43, "Apple: Pay, iCloud and App Store outage; not a hack"),
]

NUMBERS = [
    ("11,000+", "Ebola cases · DR Congo"),
    ("$115.8bn", "Nvidia quarter"),
    ("-849", "Dow points"),
    ("1,441", "drones Russia says it downed"),
    ("2m+", "barrels · tanker hit"),
]

# lon/lat of stories 1-13 (pins) and 14-43 (dots)
PINS = {
    1: (33.5, 45.0), 2: (50.5, 26.2), 3: (121.0, 14.6), 4: (23.0, -2.0),
    5: (30.7, 36.9), 6: (-98.0, 39.0), 7: (-74.0, 40.7), 8: (34.5, 31.5),
    9: (106.9, 47.9), 10: (20.5, 44.8), 11: (90.4, 23.8), 12: (86.0, 55.3),
    13: (32.6, -25.9),
}
PIN_COLOR = {1: BLUE, 2: RED, 3: PURPLE, 4: GREEN, 5: TEAL, 6: RED, 7: INK,
             8: ORANGE, 9: BLUE, 10: BLUE, 11: GREEN, 12: GREY, 13: GREEN}
DOTS = {
    14: (37.6, 55.7), 15: (30.5, 50.4), 16: (32.0, 49.0), 17: (14.4, 50.1),
    18: (2.35, 48.85), 19: (21.0, 52.2), 20: (13.4, 52.5), 21: (28.8, 47.0),
    22: (32.8, 39.9), 23: (10.0, 55.7), 24: (12.45, 41.9), 25: (-0.1, 51.5),
    26: (35.2, 31.8), 27: (35.4, 32.0), 28: (58.4, 23.6), 29: (85.8, 20.3),
    30: (79.0, 30.3), 31: (130.4, 33.6), 32: (116.4, 39.9), 33: (101.7, 3.1),
    34: (100.5, 13.75), 35: (127.0, 37.5), 36: (77.2, 28.6), 37: (36.8, -1.3),
    38: (3.0, 36.7), 39: (-72.3, 18.5), 40: (-77.0, 38.9), 41: (149.1, -35.3),
    42: (130.8, -12.5), 43: (-122.0, 37.3),
}

# Simplified continent outlines (lon, lat), equirectangular.
CONTINENTS = [
    # North America
    [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60), (-135, 58),
     (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24),
     (-105, 20), (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9),
     (-79, 9), (-80, 8), (-83, 10), (-87, 13), (-90, 14), (-92, 15),
     (-95, 18), (-97, 22), (-97, 26), (-93, 30), (-89, 30), (-84, 30),
     (-81, 25), (-80, 32), (-76, 35), (-74, 40), (-70, 42), (-68, 45),
     (-65, 44), (-60, 47), (-55, 52), (-60, 55), (-65, 60), (-68, 58),
     (-75, 62), (-80, 66), (-85, 66), (-90, 68), (-95, 69), (-110, 68),
     (-125, 70), (-140, 70), (-155, 71), (-165, 68)],
    # Greenland
    [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-25, 70),
     (-20, 74), (-25, 78), (-35, 80), (-55, 80), (-60, 76), (-62, 70)],
    # South America
    [(-79, 9), (-75, 10), (-72, 12), (-64, 10), (-60, 8), (-55, 6),
     (-52, 5), (-50, 0), (-44, -3), (-38, -5), (-35, -8), (-38, -15),
     (-40, -22), (-48, -28), (-53, -33), (-58, -38), (-62, -41), (-65, -45),
     (-68, -50), (-69, -52), (-71, -54), (-73, -50), (-73, -44), (-73, -37),
     (-71, -30), (-70, -20), (-75, -15), (-79, -8), (-81, -4), (-80, 1),
     (-79, 6)],
    # Africa
    [(-17, 15), (-16, 20), (-15, 27), (-10, 31), (-5, 35), (0, 36),
     (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (35, 28), (37, 22),
     (39, 18), (41, 11), (43, 11), (46, 11), (51, 11), (51, 2), (48, -2),
     (41, -4), (40, -10), (39, -15), (36, -18), (35, -23), (32, -26),
     (28, -33), (20, -35), (17, -32), (15, -27), (12, -18), (13, -10),
     (12, -6), (9, -1), (9, 4), (6, 4), (-8, 4), (-13, 8), (-17, 12)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50), (0, 51),
     (3, 53), (5, 53), (8, 57), (10, 59), (5, 60), (5, 62), (10, 64),
     (12, 66), (18, 69), (25, 71), (30, 70), (40, 68), (50, 69), (60, 69),
     (70, 72), (80, 73), (90, 75), (100, 77), (110, 74), (120, 73),
     (130, 72), (140, 72), (150, 70), (160, 70), (170, 67), (178, 65),
     (178, 62), (170, 60), (162, 56), (158, 52), (150, 59), (142, 55),
     (140, 50), (135, 44), (130, 42), (127, 40), (126, 38), (122, 38),
     (120, 34), (118, 30), (114, 22), (108, 18), (105, 10), (103, 8),
     (100, 7), (98, 10), (97, 15), (94, 17), (92, 21), (89, 22), (86, 20),
     (82, 17), (80, 13), (77, 8), (75, 10), (73, 16), (70, 20), (66, 25),
     (62, 25), (58, 26), (56, 27), (54, 26), (52, 25), (50, 29), (48, 30),
     (48, 24), (50, 26), (52, 28), (54, 29), (56, 26), (57, 25), (59, 22),
     (58, 20), (55, 17), (52, 15), (48, 14), (44, 13), (43, 12), (40, 15),
     (39, 21), (37, 24), (35, 28), (34, 31), (36, 36), (30, 36), (27, 37),
     (23, 36), (22, 37), (19, 42), (15, 44), (12, 45), (8, 44), (3, 42),
     (0, 40), (-2, 37), (-6, 36), (-9, 37)],
    # Australia
    [(114, -22), (113, -26), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (136, -35), (140, -38), (145, -38), (150, -37), (153, -32),
     (153, -27), (150, -23), (146, -19), (142, -15), (142, -11), (137, -12),
     (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    # Japan
    [(130, 31), (132, 33), (134, 34), (137, 35), (139, 36), (140, 38),
     (141, 41), (143, 42), (145, 44), (142, 45), (140, 42), (140, 39),
     (139, 35), (136, 34), (133, 34), (131, 33)],
    # Indonesia (Sumatra-Java arc) + Borneo + New Guinea
    [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (110, -7), (114, -8),
     (119, -9), (122, -10), (120, -10), (116, -8), (112, -7), (108, -6),
     (105, -4), (102, -1), (99, 2), (96, 4)],
    [(109, 1), (112, 3), (116, 5), (118, 2), (117, -2), (114, -3),
     (111, -3), (109, -1)],
    [(131, -1), (135, -2), (138, -4), (141, -8), (138, -8), (135, -5),
     (132, -3)],
    # New Zealand
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
     (174, -41), (172, -43), (169, -46)],
]


# ------------------------------------------------------- secondary art
# Rich schematic panels (flags, charts, buildings, icons) drawn in PIL,
# one per secondary story. Each panel is w x h, bg tinted per story.

def panel_ebola(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    # clinic tent
    d.polygon([(x + 18, y + 52), (x + 52, y + 18), (x + 86, y + 52)], fill=(255, 255, 255), outline=INK)
    d.rectangle([x + 18, y + 52, x + 86, y + 58], fill=INK)
    d.rectangle([x + 47, y + 32, x + 57, y + 42], fill=RED)
    d.rectangle([x + 50, y + 29, x + 54, y + 45], fill=RED)
    # bar chart: cases then vs now
    for i, bh in enumerate([14, 26, 40]):
        bx = x + 108 + i * 22
        d.rectangle([bx, y + 58 - bh, bx + 15, y + 58], fill=(178, 34, 28) if i == 2 else (200, 120, 110))
    d.text((x + 104, y + 60), "11,000+ CASES", font=font(F_SANSB, 10), fill=RED)


def panel_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 238, 232))
    d.ellipse([x + 14, y + 12, x + 62, y + 60], fill=(120, 180, 210), outline=BLUE, width=2)
    d.ellipse([x + 26, y + 22, x + 38, y + 34], fill=GREEN)
    d.ellipse([x + 40, y + 36, x + 54, y + 50], fill=GREEN)
    d.ellipse([x + 22, y + 40, x + 30, y + 48], fill=GREEN)
    # thermometer
    d.rectangle([x + 76, y + 14, x + 86, y + 44], outline=INK, fill=(255, 255, 255))
    d.ellipse([x + 72, y + 40, x + 90, y + 58], fill=RED, outline=INK)
    d.rectangle([x + 79, y + 22, x + 83, y + 44], fill=RED)
    # draft tag
    d.rectangle([x + 104, y + 16, x + 172, y + 36], fill=(255, 255, 255), outline=INK)
    d.text((x + 110, y + 20), "DRAFT", font=font(F_SANSB, 11), fill=INK)
    d.text((x + 104, y + 42), "PHASE OUT?", font=font(F_SANSB, 11), fill=RED)


def panel_measles(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 232, 228))
    # virus
    cx, cy = x + 42, y + 36
    for ang in range(0, 360, 30):
        import math
        ex = cx + int(20 * math.cos(math.radians(ang)))
        ey = cy + int(20 * math.sin(math.radians(ang)))
        d.line([cx, cy, ex, ey], fill=RED, width=3)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=RED)
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=RED)
    d.ellipse([cx - 6, cy - 8, cx + 2, cy, ], fill=(255, 150, 140))
    # three mini flags
    flags = [((200, 40, 40), (255, 255, 255), (40, 60, 160)),
             ((0, 120, 60), (255, 255, 255), (200, 40, 40)),
             ((200, 40, 40), (255, 220, 0), (0, 120, 60))]
    for i, (c1, c2, c3) in enumerate(flags):
        fx = x + 92 + i * 30
        d.rectangle([fx, y + 14, fx + 26, y + 22], fill=c1)
        d.rectangle([fx, y + 22, fx + 26, y + 30], fill=c2)
        d.rectangle([fx, y + 30, fx + 26, y + 38], fill=c3)
    d.text((x + 92, y + 44), "US · MX · BO", font=font(F_SANSB, 10), fill=INK)


def panel_nvidia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 24))
    # chip
    d.rectangle([x + 14, y + 12, x + 62, y + 60], fill=(40, 40, 40), outline=(120, 200, 90), width=2)
    for px in (x + 22, x + 34, x + 46):
        d.line([px, y + 6, px, y + 12], fill=(120, 200, 90), width=2)
        d.line([px, y + 60, px, y + 66], fill=(120, 200, 90), width=2)
    d.text((x + 26, y + 28), "AI", font=font(F_SANSB, 16), fill=(120, 200, 90))
    # bars + down arrow
    for i, bh in enumerate([18, 30, 44]):
        bx = x + 82 + i * 20
        d.rectangle([bx, y + 58 - bh, bx + 13, y + 58], fill=(120, 200, 90))
    d.line([x + 148, y + 16, x + 172, y + 40], fill=RED, width=4)
    d.polygon([(x + 164, y + 40), (x + 180, y + 40), (x + 172, y + 52)], fill=RED)
    d.text((x + 82, y + 60), "$115.8bn   DOW \u2212849", font=font(F_SANSB, 10), fill=(255, 255, 255))


def panel_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 228, 205))
    for i in range(3):
        tx = x + 14 + i * 44
        d.polygon([(tx, y + 50), (tx + 18, y + 26), (tx + 36, y + 50)], fill=(255, 255, 255), outline=INK)
        d.polygon([(tx + 14, y + 50), (tx + 18, y + 38), (tx + 22, y + 50)], fill=(180, 170, 150))
        d.line([tx + 18, y + 26, tx + 18, y + 16], fill=INK, width=2)
    d.line([x + 10, y + 56, x + 146, y + 56], fill=INK, width=1)
    # aid box
    d.rectangle([x + 148, y + 34, x + 176, y + 56], fill=(200, 160, 60), outline=INK)
    d.text((x + 153, y + 38), "AID", font=font(F_SANSB, 11), fill=INK)
    d.text((x + 14, y + 60), "1.4m FACE ACUTE HUNGER", font=font(F_SANSB, 10), fill=RED)


def panel_mongolia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 248))
    # parliament building
    d.polygon([(x + 18, y + 22), (x + 48, y + 8), (x + 78, y + 22)], fill=INK)
    d.rectangle([x + 20, y + 22, x + 76, y + 56], fill=(255, 255, 255), outline=INK)
    for cx in (x + 30, x + 44, x + 58):
        d.rectangle([cx, y + 28, cx + 6, y + 52], fill=INK)
    # resignation tag
    d.rectangle([x + 100, y + 14, x + 176, y + 34], fill=RED)
    d.text((x + 106, y + 18), "RESIGNATION", font=font(F_SANSB, 10), fill=(255, 255, 255))
    # Mongolia flag stripes
    d.rectangle([x + 100, y + 42, x + 124, y + 56], fill=RED)
    d.rectangle([x + 124, y + 42, x + 148, y + 56], fill=BLUE)
    d.rectangle([x + 148, y + 42, x + 172, y + 56], fill=RED)


def panel_serbia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 248))
    # parliament semicircle: 140 red vs 103 blue dots
    import math
    for i in range(14):
        ang = math.pi * (i + 0.5) / 14
        px = x + 48 + int(34 * math.cos(ang))
        py = y + 56 - int(30 * math.sin(ang))
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED if i < 8 else BLUE)
    d.rectangle([x + 96, y + 16, x + 176, y + 32], fill=(255, 255, 255), outline=INK)
    d.text((x + 100, y + 19), "STUDENTS 140", font=font(F_SANSB, 10), fill=RED)
    d.rectangle([x + 96, y + 38, x + 176, y + 54], fill=(255, 255, 255), outline=INK)
    d.text((x + 100, y + 41), "VU\u010cI\u0106 103", font=font(F_SANSB, 10), fill=BLUE)


def panel_bangladesh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 240, 228))
    # factory
    d.rectangle([x + 12, y + 26, x + 78, y + 58], fill=(120, 120, 120), outline=INK)
    d.rectangle([x + 14, y + 10, x + 22, y + 26], fill=INK)
    d.rectangle([x + 30, y + 16, x + 38, y + 26], fill=INK)
    for wx in (x + 20, x + 38, x + 56):
        d.rectangle([wx, y + 34, wx + 12, y + 46], fill=(255, 220, 90))
    # workers + placard
    for i in range(3):
        px = x + 96 + i * 26
        d.ellipse([px, y + 22, px + 10, y + 32], fill=INK)
        d.rectangle([px - 2, y + 32, px + 12, y + 56], fill=(0, 120, 60))
    d.rectangle([x + 96, y + 58, x + 168, y + 70], fill=(255, 255, 255), outline=INK)
    d.text((x + 101, y + 60), "TK 30,000", font=font(F_SANSB, 10), fill=INK)


def panel_crash(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 234, 240))
    # side-view cargo plane, nose right, diving slightly
    d.polygon([(x + 28, y + 34), (x + 140, y + 42), (x + 152, y + 46),
               (x + 140, y + 50), (x + 30, y + 44), (x + 24, y + 39)], fill=INK)
    d.polygon([(x + 34, y + 36), (x + 44, y + 20), (x + 52, y + 36)], fill=INK)
    d.polygon([(x + 76, y + 42), (x + 92, y + 56), (x + 98, y + 44)], fill=INK)
    d.rectangle([x + 118, y + 43, x + 138, y + 47], fill=(255, 255, 255))
    # smoke trail + snow ground
    for i, (sx, sy, r) in enumerate([(158, 50, 6), (168, 44, 8), (178, 38, 5)]):
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=(150, 150, 150))
    d.polygon([(x, y + 62), (x + 60, y + 54), (x + 120, y + 62), (x + 188, y + 56),
               (x + 188, y + 74), (x, y + 74)], fill=(255, 255, 255), outline=INK)


def panel_trial(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 238, 236))
    # gavel
    d.polygon([(x + 24, y + 22), (x + 70, y + 14), (x + 74, y + 26), (x + 28, y + 34)], fill=(120, 70, 20))
    d.line([x + 48, y + 30, x + 70, y + 56], fill=(120, 70, 20), width=5)
    d.rectangle([x + 60, y + 54, x + 84, y + 60], fill=(120, 70, 20))
    # scales
    d.line([x + 128, y + 12, x + 128, y + 52], fill=INK, width=2)
    d.line([x + 104, y + 18, x + 152, y + 18], fill=INK, width=2)
    d.polygon([(x + 98, y + 18), (x + 110, y + 18), (x + 104, y + 34)], fill=INK)
    d.polygon([(x + 146, y + 18), (x + 158, y + 18), (x + 152, y + 34)], fill=INK)
    d.rectangle([x + 104, y + 56, x + 176, y + 70], fill=RED)
    d.text((x + 110, y + 59), "5 CHARGES", font=font(F_SANSB, 10), fill=(255, 255, 255))


ART = {"ebola": panel_ebola, "cop": panel_cop, "measles": panel_measles,
       "nvidia": panel_nvidia, "gaza": panel_gaza, "mongolia": panel_mongolia,
       "serbia": panel_serbia, "bangladesh": panel_bangladesh,
       "crash": panel_crash, "trial": panel_trial}


# ------------------------------------------------------------------ map
def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK)
    lat_top, lat_bot = 75.0, -55.0

    def proj(lon, lat):
        px = x + (lon + 180.0) / 360.0 * w
        py = y + (lat_top - lat) / (lat_top - lat_bot) * h
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND, outline=LAND_EDGE)
    # brief dots first (under pins)
    for n, (lon, lat) in DOTS.items():
        px, py = proj(lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)
    # numbered pins
    fpin = font(F_SANSB, 9)
    for n, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        col = PIN_COLOR[n]
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col, outline=(255, 255, 255), width=1)
        tw = d.textlength(str(n), font=fpin)
        d.text((px - tw / 2, py - 6), str(n), font=fpin, fill=(255, 255, 255))
    return proj


# ------------------------------------------------------------------ page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_kick = font(F_SANSB, 12)
    f_title = font(F_TITLE, 62)
    f_num_v = font(F_SERIFB, 17)
    f_num_l = font(F_SANS, 10)
    f_lead_k = font(F_SANSB, 11)
    f_lead_h = font(F_SERIFB, 19)
    f_lead_b = font(F_SANS, 12)
    f_cap = font(F_SANSB, 9)
    f_sec_k = font(F_SANSB, 9)
    f_sec_h = font(F_SERIFB, 14)
    f_sec_b = font(F_SANS, 10)
    f_head = font(F_SANSB, 11)
    f_src = font(F_SANS, 10)

    # ---- masthead
    d.text((MX, 10), "THE WORLD\u2019S NEWS IN ONE PICTURE", font=f_kick, fill=RED)
    right = "43 STORIES \u00b7 6 CONTINENTS \u00b7 ALL FROM TUESDAY"
    d.text((MX + CW - d.textlength(right, font=f_kick), 10), right, font=f_kick, fill=INK)
    title = "Tuesday 17 November 2026"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 26), title, font=f_title, fill=INK)
    d.line([MX, 94, MX + CW, 94], fill=INK, width=3)

    # ---- numbers strip
    colw = CW / 5
    for i, (val, lab) in enumerate(NUMBERS):
        cx = MX + i * colw
        d.text((cx + 6, 100), val, font=f_num_v, fill=RED)
        d.text((cx + 6, 120), lab, font=f_num_l, fill=GREY)
        if i:
            d.line([cx, 102, cx, 132], fill=LIGHT, width=1)
    d.line([MX, 138, MX + CW, 138], fill=INK, width=2)

    # ---- 3 leads
    lw = (CW - 2 * 16) // 3
    ly = 146
    for i, lead in enumerate(LEADS):
        x0 = MX + i * (lw + 16)
        photo = Image.open(os.path.join(HERE, "assets", lead["img"])).convert("RGB")
        # centre-crop to panel aspect, then resize
        pw, ph = photo.size
        target = lw / 112.0
        if pw / ph > target:
            nw = int(ph * target)
            photo = photo.crop(((pw - nw) // 2, 0, (pw - nw) // 2 + nw, ph))
        else:
            nh = int(pw / target)
            photo = photo.crop((0, (ph - nh) // 2, pw, (ph - nh) // 2 + nh))
        photo = photo.resize((lw, 112), Image.LANCZOS)
        img.paste(photo, (x0, ly))
        d.rectangle([x0, ly, x0 + lw, ly + 112], outline=INK, width=1)
        d.rectangle([x0, ly + 112, x0 + lw, ly + 128], fill=INK)
        d.text((x0 + 6, ly + 115), lead["cap"], font=f_cap, fill=(255, 255, 255))
        d.text((x0, ly + 134), f"{lead['n']}  {lead['kicker']}", font=f_lead_k, fill=lead["color"])
        draw_wrapped(d, lead["head"], x0, ly + 150, f_lead_h, lw, 2, INK, lh=22)
        draw_wrapped(d, lead["body"], x0, ly + 196, f_lead_b, lw, 2, INK, lh=15)
    d.line([MX, 380, MX + CW, 380], fill=INK, width=2)

    # ---- 10 secondaries, 5 x 2
    sw = (CW - 4 * 10) // 5
    for row in range(2):
        y0 = 388 + row * 170
        for col in range(5):
            s = SECOND[row * 5 + col]
            x0 = MX + col * (sw + 10)
            ART[s["art"]](d, x0, y0, sw, 74)
            d.rectangle([x0, y0, x0 + sw, y0 + 74], outline=INK, width=1)
            d.rectangle([x0, y0 + 74, x0 + sw, y0 + 88], fill=INK)
            d.text((x0 + 5, y0 + 77), s["cap"], font=f_cap, fill=(255, 255, 255))
            d.text((x0, y0 + 92), f"{s['n']}  {s['kicker']}", font=f_sec_k, fill=s["color"])
            draw_wrapped(d, s["head"], x0, y0 + 106, f_sec_h, sw, 2, INK, lh=17)
            draw_wrapped(d, s["body"], x0, y0 + 142, f_sec_b, sw, 2, INK, lh=13)
    d.line([MX, 730, MX + CW, 730], fill=INK, width=2)

    # ---- map + briefs
    d.text((MX, 738), "WHERE IT HAPPENED", font=f_head, fill=RED)
    d.text((MX + 312, 738), "ALSO ON TUESDAY 17 NOVEMBER", font=f_head, fill=RED)
    draw_map(d, MX, 758, 296, 108)
    d.text((MX, 872), "Pins: stories 1\u201313 \u00b7 dots: 14\u201343", font=font(F_SANS, 9), fill=GREY)
    d.text((MX, 886), "Red Americas \u00b7 Blue Europe \u00b7 Orange Middle East", font=font(F_SANS, 9), fill=GREY)
    d.text((MX, 900), "Purple Asia \u00b7 Green Africa \u00b7 Teal Global", font=font(F_SANS, 9), fill=GREY)
    d.text((MX, 914), "Every inhabited continent: not one", font=font(F_SANS, 9), fill=GREY)
    d.text((MX, 928), "country\u2019s day is left out.", font=font(F_SANS, 9), fill=GREY)

    bx = MX + 312
    bcw = (CW - 312 - 10) // 2
    for i, (n, text) in enumerate(BRIEFS):
        col = 0 if i < 15 else 1
        r = i % 15
        x0 = bx + col * (bcw + 10)
        y0 = 758 + r * 13
        d.text((x0, y0), str(n), font=font(F_SANSB, 10), fill=PURPLE)
        fnt = fit_font(d, text, F_SANS, 10, bcw - 24)
        d.text((x0 + 22, y0), text, font=fnt, fill=INK)
        d.line([x0, y0 + 12, x0 + bcw, y0 + 12], fill=LIGHT, width=1)

    # ---- sources footer
    d.line([MX, 962, MX + CW, 962], fill=INK, width=2)
    src = ("Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN News. "
           "Every story here happened or was first reported on Tuesday 17 November 2026. "
           "Contested claims are marked as claims.")
    draw_wrapped(d, src, MX, 970, f_src, CW, 2, GREY, lh=14)
    d.line([MX, 1006, MX + CW, 1006], fill=INK, width=2)
    return img


if __name__ == "__main__":
    out = os.path.join(HERE, "entry.png")
    build().save(out, compress_level=6)
    print("wrote", out, os.path.getsize(out), "bytes")
