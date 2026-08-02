"""Language distribution panel, drawn in the Interchange world.

Replaces github-readme-stats/top-langs, whose shared instance answers 503.
Runs in CI against the GitHub API; segments carry Linguist's own colours, which
readers already recognise from every repo page.
"""
import json
import os
import subprocess
import sys
from typeset import Face

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

FONTS = os.path.join(HERE, "fonts")
REG = Face(os.path.join(FONTS, "Overpass-400.ttf"))
SEMI = Face(os.path.join(FONTS, "Overpass-600.ttf"))
BOLD = Face(os.path.join(FONTS, "Overpass-700.ttf"))

THEMES = {
    "dark":  {"ink": "#E6EDF3", "muted": "#8B949E", "gap": "#0D1117"},
    "light": {"ink": "#1F2328", "muted": "#59636E", "gap": "#FFFFFF"},
}

# Linguist's published colours, so a segment matches what GitHub shows on the repo.
LINGUIST = {
    "TypeScript": "#3178c6", "Python": "#3572A5", "Blade": "#f7523f",
    "JavaScript": "#f1e05a", "PHP": "#4F5D95", "CSS": "#663399",
    "HTML": "#e34c26", "EJS": "#a91e50", "Shell": "#89e051",
    "Dockerfile": "#384d54", "Java": "#b07219", "C": "#555555",
    "C++": "#f34b7d", "Jupyter Notebook": "#DA5B0B", "SCSS": "#c6538c",
    "Vue": "#41b883", "Go": "#00ADD8", "Rust": "#dea584", "Ruby": "#701516",
    "Kotlin": "#A97BFF", "Swift": "#F05138", "Dart": "#00B4AB",
    "Makefile": "#427819", "PowerShell": "#012456", "Batchfile": "#C1F12E",
}
OTHER = "#8B949E"


def gh(path, allow_fail=False):
    r = subprocess.run(["gh", "api", path, "--paginate"], capture_output=True, text=True)
    if r.returncode != 0:
        if allow_fail:
            return None
        sys.exit(f"gh api {path} failed: {r.stderr.strip()}")
    return r.stdout


def collect(listing):
    import re
    names = [l for l in listing.splitlines() if l]
    repos = []
    for chunk in names:
        try:
            data = json.loads(chunk)
        except json.JSONDecodeError:
            continue
        repos.extend(data if isinstance(data, list) else [data])
    full = [r["full_name"] for r in repos if not r.get("fork")]

    totals = {}
    for name in full:
        raw = gh(f"repos/{name}/languages")
        for obj in re.findall(r"\{[^{}]*\}", raw):
            try:
                for k, v in json.loads(obj).items():
                    totals[k] = totals.get(k, 0) + v
            except json.JSONDecodeError:
                pass
    return totals, len(full)


def bucket(totals, floor=1.0):
    grand = sum(totals.values()) or 1
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    keep, rest = [], 0.0
    for name, n in ranked:
        pct = n / grand * 100
        (keep.append((name, pct)) if pct >= floor else None)
        if pct < floor:
            rest += pct
    if rest >= 0.05:
        keep.append(("Other", rest))
    return keep


def txt(face, s, size, x, y, fill, tracking=0.0, anchor="start"):
    d = face.path(s, size, x, y, tracking=tracking, anchor=anchor)
    return f'<path d="{d}" fill="{fill}"/>' if d else ""


def panel(langs, repo_count, theme, wide=True):
    c = THEMES[theme]
    W = 1000 if wide else 440
    pad = 0
    bar_y, bar_h, gap = (34, 16, 3) if wide else (32, 14, 2.5)
    # Keep the legend on one row when it fits; a lone wrapped chip reads as a mistake.
    cols = min(len(langs), 7) if wide else 2
    rows = -(-len(langs) // cols)
    leg_top = bar_y + bar_h + (30 if wide else 26)
    leg_step = 22 if wide else 20
    H = int(leg_top + (rows - 1) * leg_step + (18 if wide else 16))

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" fill="none" role="img">']

    head = f"LANGUAGES BY VOLUME  ·  {repo_count} REPOSITORIES"
    p.append(txt(SEMI, head, 11 if wide else 10, pad, 16, c["muted"],
                 tracking=0.14))

    total = sum(pct for _, pct in langs) or 100.0
    usable = W - gap * (len(langs) - 1)
    r = bar_h / 2

    # One rounded mask over the whole run. Every segment is then a plain rect of
    # identical height, so no segment can render shorter than its neighbours;
    # hand-rolling the rounded end caps per segment is what broke that before.
    p.append(f'<defs><clipPath id="bar"><rect x="{pad}" y="{bar_y}" '
             f'width="{W - pad}" height="{bar_h}" rx="{r}"/></clipPath></defs>')
    p.append('<g clip-path="url(#bar)">')
    x = float(pad)
    for name, pct in langs:
        w = max(usable * pct / total, 2.0)
        p.append(f'<rect x="{x:.2f}" y="{bar_y}" width="{w:.2f}" height="{bar_h}" '
                 f'fill="{LINGUIST.get(name, OTHER)}"/>')
        x += w + gap
    p.append('</g>')

    col_w = W / cols
    for i, (name, pct) in enumerate(langs):
        cx = pad + (i % cols) * col_w
        cy = leg_top + (i // cols) * leg_step
        p.append(f'<circle cx="{cx + 5}" cy="{cy - 4}" r="5" '
                 f'fill="{LINGUIST.get(name, OTHER)}"/>')
        p.append(txt(SEMI, name, 12.5 if wide else 12, cx + 17, cy, c["ink"]))
        nw = SEMI.width(name, 12.5 if wide else 12)
        p.append(txt(REG, f"{pct:.1f}%", 12.5 if wide else 12, cx + 17 + nw + 7, cy,
                     c["muted"]))

    p.append("</svg>")
    return "\n".join(s for s in p if s)


if __name__ == "__main__":
    # /user/repos is the only listing that includes private repositories, and it
    # needs a user-scoped token. Actions' default GITHUB_TOKEN gets 403 here.
    # Rebuilding from public repos alone would quietly replace the real
    # distribution with a worse one, so skip instead.
    listing = gh("user/repos?per_page=100&affiliation=owner", allow_fail=True)
    if listing is None:
        print("::notice::No token that can list private repositories "
              "(add a PAT with repo scope as the STATS_TOKEN secret). "
              "Leaving the existing panel unchanged.")
        sys.exit(0)

    totals, repo_count = collect(listing)
    langs = bucket(totals)
    print("  ".join(f"{n} {p:.1f}%" for n, p in langs))
    for theme in ("dark", "light"):
        for tag, wide in (("wide", True), ("narrow", False)):
            path = os.path.join(OUT, f"langs-{tag}-{theme}.svg")
            with open(path, "w") as f:
                f.write(panel(langs, repo_count, theme, wide))
            print(f"  {os.path.basename(path):26} {os.path.getsize(path)/1024:5.1f} KB")
