"""Interchange: the stack drawn as a transit diagram.

Six lines (stack layers) converge on one interchange (NovelVerse).
Emits four SVGs: wide/narrow x dark/light. Backgrounds stay transparent so
the diagram sits on GitHub's own canvas in any theme variant.
"""
import os
from typeset import Face

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "assets")
os.makedirs(OUT, exist_ok=True)

REG = Face(os.path.join(HERE, "fonts", "Overpass-400.ttf"))
BOLD = Face(os.path.join(HERE, "fonts", "Overpass-700.ttf"))

# GitHub Primer's accessible hues: every line clears 4.5:1 on its own ground.
THEMES = {
    "dark": {
        "ink": "#E6EDF3", "muted": "#8B949E", "rule": "#8B949E",
        "languages": "#FF6B5E", "web": "#58A6FF", "ai": "#A78BFA",
        "data": "#3FD9A4", "cloud": "#FFB224", "tooling": "#F778BA",
    },
    "light": {
        "ink": "#1F2328", "muted": "#59636E", "rule": "#59636E",
        "languages": "#CF222E", "web": "#0969DA", "ai": "#6639BA",
        "data": "#04804D", "cloud": "#BC4C00", "tooling": "#BF3989",
    },
}

# Every station here has to be something NovelVerse actually runs, because every
# line terminates at the NovelVerse interchange. Verified against the manifests:
# nv-web/package.json, nv-ai/requirements.txt, and the GitHub language stats.
# PHP and PyTorch are real skills but belong to other work, so they live in the
# README's Stack section instead, where nothing claims they ship here.
# (label, key, wide stations, narrow stations)
LINES = [
    ("LANGUAGES", "languages", ["TypeScript", "Python", "JavaScript"], ["TypeScript", "Python"]),
    ("WEB", "web", ["Next.js", "React", "NestJS"], ["Next.js", "NestJS"]),
    ("AI & ML", "ai", ["LangGraph", "Anthropic", "Voyage"], ["LangGraph", "Voyage"]),
    ("DATA", "data", ["PostgreSQL", "Neo4j", "Redis"], ["PostgreSQL", "Neo4j"]),
    ("CLOUD", "cloud", ["Oracle Cloud", "AWS", "Cloudflare"], ["Oracle Cloud", "Cloudflare"]),
    ("TOOLING", "tooling", ["Docker", "Turborepo", "Playwright"], ["Docker", "Turborepo"]),
]

# The NovelVerse open-book mark, lifted from novelverse-web's brand directory
# (assets/brand/novelverse-mark.svg holds the original). Drawn in ink rather than
# the brand violet: the interchange belongs to all six lines, and violet is
# already spoken for by the AI & ML line.
MARK_VIEWBOX = 1254
MARK = [
    "M624 125C615 128 610 151 603 171C588 215 558 249 513 267L482 279C473 283 473 296 484 "
    "304C526 316 559 340 584 371C604 397 610 419 615 442C617 451 633 452 639 441C647 413 661 "
    "383 680 358C703 333 733 315 769 304C782 300 779 281 768 277C722 264 686 237 666 201C651 "
    "175 644 151 639 133C636 123 628 124 624 125Z",
    "M218 358C350 358 470 409 566 497C593 526 608 558 608 593V1059C608 1065 605 1067 601 "
    "1063C494 959 380 926 216 923C208 923 203 917 203 909V373C203 364 209 358 218 358Z",
    "M1035 358C905 358 784 409 690 495C662 527 646 560 646 588V1060C646 1065 649 1067 653 "
    "1063C762 959 876 927 1035 923C1044 923 1050 916 1050 907V373C1050 364 1044 358 1035 358Z",
    "M139 443H154C162 443 167 447 167 455V940C167 953 177 962 190 962H245C355 964 468 986 545 "
    "1047C547 1049 545 1052 542 1051C454 1033 382 1024 303 1024H136C127 1024 121 1018 121 "
    "1009V458C121 449 129 443 139 443Z",
    "M1092 444H1116C1125 444 1132 449 1132 458V1009C1132 1018 1127 1024 1118 1024H948C878 1024 "
    "799 1034 712 1050C709 1051 706 1050 708 1048C781 987 895 964 1003 962H1062C1075 962 1085 "
    "953 1085 940V457C1085 449 1088 444 1092 444Z",
]

HUB = "NOVELVERSE"
HUB_SUB = "Multi-service AI platform"
HUB_SUB2 = "Next.js  ·  NestJS  ·  FastAPI"

BLEED = []


def txt(face, s, size, x, y, fill, tracking=0.0, anchor="start", canvas_w=None):
    if canvas_w is not None:
        w = face.width(s, size, tracking)
        left = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
        if left < 0 or left + w > canvas_w:
            BLEED.append((s, round(left, 1), round(left + w, 1), canvas_w))
    d = face.path(s, size, x, y, tracking=tracking, anchor=anchor)
    return f'<path d="{d}" fill="{fill}"/>' if d else ""


def mark(x, y, size, fill):
    """The NovelVerse mark, scaled from its 1254 unit box to `size` px at (x, y)."""
    s = size / MARK_VIEWBOX
    # The second through fifth paths carry the original's translate/scale.
    inner = f'<g transform="translate(0 14) scale(1 .98)">' \
            + "".join(f'<path d="{d}"/>' for d in MARK[1:]) + "</g>"
    return (f'<g transform="translate({x} {y}) scale({s:.5f})" fill="{fill}">'
            f'<path d="{MARK[0]}"/>{inner}</g>')


def route(x0, y0, x_kink, y1, x_end):
    """Horizontal run, 45-degree transition, horizontal run into the hub."""
    dy = y1 - y0
    x_turn = x_kink + abs(dy)
    return (f'M {x0} {y0} L {x_kink} {y0} L {x_turn} {y1} L {x_end} {y1}'
            if dy else f'M {x0} {y0} L {x_end} {y1}')


def build_wide(theme):
    c = THEMES[theme]
    W, H = 1000, 272
    row_y = [30 + i * 44 for i in range(6)]
    hub_y = [85 + i * 22 for i in range(6)]
    dots_x = [236, 372, 508]
    x_start, x_kink, x_hub = 164, 600, 782

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" fill="none" role="img">']

    for i, (label, key, stations, _) in enumerate(LINES):
        col, y, hy = c[key], row_y[i], hub_y[i]
        p.append(txt(BOLD, label, 12, 150, y + 4, col, tracking=0.10, anchor="end"))
        p.append(f'<path d="{route(x_start, y, x_kink, hy, x_hub)}" stroke="{col}" '
                 f'stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
        for j, st in enumerate(stations):
            p.append(f'<circle cx="{dots_x[j]}" cy="{y}" r="4.5" fill="{col}"/>')
            p.append(txt(REG, st, 12.5, dots_x[j], y - 10, c["ink"], anchor="middle",
                         canvas_w=W))

    p.append(f'<rect x="{x_hub - 2.5}" y="{hub_y[0]}" width="5" '
             f'height="{hub_y[-1] - hub_y[0]}" fill="{c["ink"]}"/>')
    for hy in hub_y:
        p.append(f'<circle cx="{x_hub}" cy="{hy}" r="7" fill="{c["ink"]}"/>')
    # Centred over the wordmark, which is the widest line in the hub block.
    p.append(mark(818 + (BOLD.width(HUB, 28, -0.01) - 46) / 2, 62, 46, c["ink"]))
    p.append(txt(BOLD, HUB, 28, 818, 133, c["ink"], tracking=-0.01, canvas_w=W))
    p.append(txt(REG, HUB_SUB, 13, 820, 157, c["muted"], canvas_w=W))
    p.append(txt(REG, HUB_SUB2, 12, 820, 176, c["muted"], canvas_w=W))
    p.append("</svg>")
    return "\n".join(x for x in p if x)


def build_narrow(theme):
    c = THEMES[theme]
    W, H = 440, 382
    row_y = [32 + i * 42 for i in range(6)]
    hub_y = [107 + i * 12 for i in range(6)]
    # Second label must clear the kink: widest is "Oracle Cloud" at ~66px.
    dots_x = [168, 240]
    x_start, x_kink, x_hub = 120, 292, 374

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" fill="none" role="img">']

    for i, (label, key, _, stations) in enumerate(LINES):
        col, y, hy = c[key], row_y[i], hub_y[i]
        p.append(txt(BOLD, label, 10, 108, y + 3.5, col, tracking=0.06, anchor="end"))
        p.append(f'<path d="{route(x_start, y, x_kink, hy, x_hub)}" stroke="{col}" '
                 f'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
        for j, st in enumerate(stations):
            p.append(f'<circle cx="{dots_x[j]}" cy="{y}" r="4" fill="{col}"/>')
            p.append(txt(REG, st, 11, dots_x[j], y + 17, c["ink"], anchor="middle",
                         canvas_w=W))

    p.append(f'<rect x="{x_hub - 2}" y="{hub_y[0]}" width="4" '
             f'height="{hub_y[-1] - hub_y[0]}" fill="{c["ink"]}"/>')
    for hy in hub_y:
        p.append(f'<circle cx="{x_hub}" cy="{hy}" r="6" fill="{c["ink"]}"/>')
    # Clear of the TOOLING station labels, which sit at row_y[5] + 17.
    p.append(mark(202, 274, 36, c["ink"]))
    p.append(txt(BOLD, HUB, 23, 220, 340, c["ink"], tracking=-0.01, anchor="middle",
                 canvas_w=W))
    p.append(txt(REG, HUB_SUB, 11.5, 220, 360, c["muted"], anchor="middle", canvas_w=W))
    p.append(txt(REG, HUB_SUB2, 10.5, 220, 376, c["muted"], anchor="middle", canvas_w=W))
    p.append("</svg>")
    return "\n".join(x for x in p if x)


for theme in ("dark", "light"):
    for name, fn in (("wide", build_wide), ("narrow", build_narrow)):
        path = os.path.join(OUT, f"map-{name}-{theme}.svg")
        with open(path, "w") as f:
            f.write(fn(theme))
        print(f"{os.path.basename(path):26} {os.path.getsize(path) / 1024:6.1f} KB")

if BLEED:
    print("\nTEXT OVERFLOW:")
    for s_, l, r, cw in BLEED:
        print(f"  {s_!r} spans {l}..{r} in canvas 0..{cw}")
else:
    print("\nno text overflow")
