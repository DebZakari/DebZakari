"""Generate the profile README in the Interchange world.

Badges are line bullets: colour encodes the stack layer, never the vendor.
Fills are chosen so white type clears 4.5:1 on the badge itself, which lets one
static badge set sit correctly on GitHub's light and dark canvases alike.
"""
import os
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "README.md")

USER = "DebZakari"
SITE = "https://debzakari.vercel.app"
EMAIL = "mdavezachary@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/dave-zachary-macarayo-002304282/"

BULLET = {
    "languages": "C22B24",
    "web":       "0B5FD0",
    "ai":        "6D3EE8",
    "data":      "04804D",
    "cloud":     "B4530A",
    "tooling":   "B32D77",
}

# Deliberately outside the six line colours.
NEUTRAL = "57606A"

THEME = {
    "dark":  {"ink": "E6EDF3", "muted": "8B949E", "accent": "A78BFA", "line": "58A6FF"},
    "light": {"ink": "1F2328", "muted": "59636E", "accent": "6639BA", "line": "0969DA"},
}


def badge(text, colour, style="flat-square"):
    return f"https://img.shields.io/badge/{quote(text, safe='')}-{colour}?style={style}"


def bullets(items, key):
    return " ".join(f'<img alt="{i}" src="{badge(i, BULLET[key])}">' for i in items)


def line(name, key, items):
    head = f'<img alt="{name} line" src="{badge(name.upper(), BULLET[key], "for-the-badge")}">'
    return f"{head}\n\n{bullets(items, key)}"


CORE = [
    ("Languages", "languages", ["TypeScript", "Python", "JavaScript", "PHP", "Java", "C"]),
    ("Web", "web", ["Next.js", "React", "NestJS", "FastAPI", "Laravel", "Tailwind CSS", "Node.js"]),
    ("AI & ML", "ai", ["LangGraph", "LangChain", "PyTorch", "TensorFlow", "OpenCV",
                       "Hugging Face", "Ollama"]),
    ("Data", "data", ["PostgreSQL", "pgvector", "Neo4j", "Redis", "MySQL", "Drizzle ORM"]),
    ("Cloud", "cloud", ["Oracle Cloud", "AWS", "Cloudflare", "Vercel", "Docker", "Caddy"]),
    ("Tooling", "tooling", ["Turborepo", "pnpm", "Playwright", "Vitest", "Sentry", "Infisical"]),
]

FULL = [
    ("Web & realtime", "web", ["Better Auth", "Socket.IO", "Yjs", "Hocuspocus", "Tiptap",
                               "TanStack Query", "Zustand", "shadcn/ui", "Radix UI", "BullMQ",
                               "Fastify", "Serwist", "Resend", "Bootstrap", "CodeIgniter"]),
    ("Model providers", "ai", ["Anthropic", "OpenAI", "Google Gemini", "Groq", "Cerebras",
                               "Mistral", "OpenRouter", "NVIDIA NIM", "Workers AI"]),
    ("Retrieval & ranking", "ai", ["Voyage AI", "Cohere", "Jina AI", "ZeroEntropy", "tiktoken",
                                   "RRF hybrid search", "HyDE"]),
    ("Speech", "ai", ["ElevenLabs", "Cartesia", "Fish Audio", "Speechmatics"]),
    ("Vision & biometrics", "ai", ["YOLO", "U-Net", "ArcFace", "RetinaFace"]),
    ("Data & storage", "data", ["Neon", "SQLite", "ltree", "Cloudflare R2", "MinIO", "Drizzle Kit"]),
    ("Cloud & infrastructure", "cloud", ["OCI Ampere A1", "AWS S3", "AWS KMS", "AWS Rekognition",
                                         "Cloudflare Tunnel", "Turnstile", "systemd",
                                         "Blue-green deploys"]),
    ("Quality & safety", "tooling", ["ESLint", "pytest", "Ruff", "mypy", "Sightengine",
                                     "Arachnid Shield"]),
    ("Hardware", "tooling", ["Arduino", "ESP32", "Raspberry Pi"]),
]


def picture(dark_src, light_src, alt, extra_dark=None, extra_light=None, width=None):
    w = f' width="{width}"' if width else ""
    src = []
    if extra_dark:
        src.append(f'  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" '
                   f'srcset="{extra_dark}">')
    if extra_light:
        src.append(f'  <source media="(prefers-color-scheme: light) and (max-width: 600px)" '
                   f'srcset="{extra_light}">')
    src.append(f'  <source media="(prefers-color-scheme: dark)" srcset="{dark_src}">')
    body = "\n".join(src)
    return (f'<picture>\n{body}\n  <img alt="{alt}" src="{light_src}"{w}>\n</picture>')


def stat(url_tpl, alt):
    return picture(url_tpl.format(**THEME["dark"]),
                   url_tpl.format(**THEME["light"]), alt)


STREAK = ("https://streak-stats.demolab.com?user=" + USER +
          "&hide_border=true&background=00000000&stroke={muted}&ring={accent}&fire={accent}"
          "&currStreakNum={ink}&sideNums={ink}&currStreakLabel={muted}&sideLabels={muted}"
          "&dates={muted}&excludeDaysLabel={muted}")
# hide_title and grid=false strip the widget's own heading and dashed rules, which
# arrive in Segoe UI and read as a foreign object on the page. The axis labels are
# not removable; everything else here is ours.
GRAPH = ("https://github-readme-activity-graph.vercel.app/graph?username=" + USER +
         "&bg_color=00000000&hide_border=true&hide_title=true&grid=false&radius=6"
         "&color={ink}&line={line}&point={accent}&area=true&area_color={line}")

ALT = ("Transit-style diagram of Dave Zachary Macarayo's stack. Six colour-coded lines — "
       "Languages, Web, AI & ML, Data, Cloud and Tooling — run left to right and converge on a "
       "single interchange labelled NovelVerse, a multi-service AI platform built with Next.js, "
       "NestJS and FastAPI.")

CONTRACT = """<!--
THESIS: A stack is a network, not a logo wall. Colour names the line (the
layer), never the vendor, and the stations are where the work connects. Refuses
the category default: gradient banner plus ragged brand-coloured badge rows.
OWN-WORLD: Beck/Vignelli transit diagram. Six line colours on GitHub's own
canvas, transparent ground, Overpass (Highway Gothic lineage) drawn to
outlines, 45-degree kinks, tick stations, circle-and-bar interchange.
STORY: A recruiter reads six layers converging on one real system, sees the
inventory behind it, and leaves with a way to make contact.
FIRST VIEWPORT: Name top-left as a map cartouche; six colour-coded lines run
left to right through their stations and converge on the NOVELVERSE
interchange at right; contact terminates the page.
FORM: Transit line map, candidate 4 of the grounded list, seed key 47501229.
FINISH: unreviewed and undocumented is unfinished; this build ends with the
finish review, the verdict, and DESIGN.md
-->"""

doc = []
A = doc.append

A(CONTRACT)
A(picture("assets/map-wide-dark.svg", "assets/map-wide-light.svg", ALT,
          "assets/map-narrow-dark.svg", "assets/map-narrow-light.svg"))
A("")
A("Computer Engineering graduate building production AI systems end to end — from Postgres")
A("schema and retrieval pipelines, through a multi-provider model router, to the interface")
A(f"people actually read. Based in the Philippines. [Portfolio]({SITE}) · open to opportunities.")
A("")
A("## Stack")
A("")
A("Each line is a layer. Colour marks the line, not the vendor.")
A("")
for name, key, items in CORE:
    A(line(name, key, items))
    A("")
A("<details>")
A("<summary>Full inventory — everything else in production use</summary>")
A("<br>")
A("")
for name, key, items in FULL:
    A(f"**{name}**")
    A("")
    A(bullets(items, key))
    A("")
A("</details>")
A("")
A("## Selected work")
A("")
A("**NovelVerse** — private. A multi-service AI writing platform, built solo. A Turborepo/pnpm")
A("monorepo splitting a Next.js reader and manuscript editor, a NestJS + Fastify business API,")
A("and a FastAPI AI service. Live collaborative editing over Yjs and Hocuspocus; hybrid")
A("retrieval across pgvector and a Neo4j knowledge graph; a multi-provider model router with")
A("circuit breaking and per-provider budgets across nine LLM vendors; a TTS/STT gateway over")
A("four speech providers. Runs on an OCI Ampere A1 host behind Cloudflare, with blue-green")
A("releases, nightly backups and monthly recovery drills.")
A("")
A(f"**[portfolio](https://github.com/{USER}/portfolio)** — a universe-themed Next.js site with a")
A("Canvas 2D galaxy and a black-hole cursor, plus a content-first Focus mode for anyone who")
A(f"would rather just read. Live at [{SITE.split('//')[1]}]({SITE}).")
A("")
A(f"**Biometrics and computer vision** — [iris detection with YOLO]"
  f"(https://github.com/{USER}/Iris-Detection-Using-YOLO), "
  f"[iris segmentation with U-Net](https://github.com/{USER}/UNet-PyTorch-Iris-Segmentation), "
  f"and TensorFlow 2 ports of [ArcFace](https://github.com/{USER}/arcface-tf2-colab) and "
  f"[RetinaFace](https://github.com/{USER}/retinaface-tf2-colab).")
A("")
A("## Activity")
A("")
A(picture("assets/langs-wide-dark.svg", "assets/langs-wide-light.svg",
          "Language distribution across all repositories",
          "assets/langs-narrow-dark.svg", "assets/langs-narrow-light.svg"))
A("")
A(stat(STREAK, "GitHub contribution streak: total contributions since February 2023, "
              "current streak, and longest streak"))
A("")
A(stat(GRAPH, "Daily contribution activity over the past month"))
A("")
A("## Contact")
A("")
A(" ".join([
    f'[<img alt="Email" src="{badge("Email", NEUTRAL, "for-the-badge")}">](mailto:{EMAIL})',
    f'[<img alt="LinkedIn" src="{badge("LinkedIn", NEUTRAL, "for-the-badge")}">]({LINKEDIN})',
    f'[<img alt="Portfolio" src="{badge("Portfolio", NEUTRAL, "for-the-badge")}">]({SITE})',
]))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write("\n".join(doc).rstrip() + "\n")
print(f"README.md  {os.path.getsize(OUT) / 1024:.1f} KB  ({len(doc)} blocks)")
