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
NOVELVERSE = "https://novelverse.ink"
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
    # Shields.io splits the path on "-" and reads "_" as a space, so both have to
    # be doubled. Without this, "U-Net" renders as two badges reading "U" "Net".
    esc = text.replace("_", "__").replace("-", "--")
    return f"https://img.shields.io/badge/{quote(esc, safe='')}-{colour}?style={style}"


def bullets(items, key):
    out = []
    for i in items:
        img = f'<img alt="{i}" src="{badge(i, BULLET[key])}">'
        # A few entries are techniques rather than products and have nowhere to
        # point; those stay unlinked rather than inventing a destination.
        out.append(f"[{img}]({LINKS[i]})" if LINKS.get(i) else img)
    return " ".join(out)


def line(name, key, items):
    head = f'<img alt="{name} line" src="{badge(name.upper(), BULLET[key], "for-the-badge")}">'
    return f"{head}\n\n{bullets(items, key)}"


# Every badge that names a product links to that product. Checked for HTTP 200
# by scripts/check_links.py; a dead link on a hiring page is worse than none.
LINKS = {
    # Languages
    "TypeScript": "https://www.typescriptlang.org",
    "Python": "https://www.python.org",
    "JavaScript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
    "PHP": "https://www.php.net",
    "Java": "https://dev.java",
    "C": "https://en.cppreference.com/w/c",
    # Web
    "Next.js": "https://nextjs.org",
    "React": "https://react.dev",
    "NestJS": "https://nestjs.com",
    "FastAPI": "https://fastapi.tiangolo.com",
    "Laravel": "https://laravel.com",
    "Tailwind CSS": "https://tailwindcss.com",
    "Node.js": "https://nodejs.org",
    "Better Auth": "https://www.better-auth.com",
    "Socket.IO": "https://socket.io",
    "Yjs": "https://yjs.dev",
    "Hocuspocus": "https://tiptap.dev/docs/hocuspocus/getting-started/overview",
    "Tiptap": "https://tiptap.dev",
    "TanStack Query": "https://tanstack.com/query",
    "Zustand": "https://zustand.docs.pmnd.rs",
    "shadcn/ui": "https://ui.shadcn.com",
    "Radix UI": "https://www.radix-ui.com",
    "BullMQ": "https://bullmq.io",
    "Fastify": "https://fastify.dev",
    "Serwist": "https://serwist.pages.dev",
    "Resend": "https://resend.com",
    "Bootstrap": "https://getbootstrap.com",
    "CodeIgniter": "https://codeigniter.com",
    "Alpine.js": "https://alpinejs.dev",
    # AI & ML
    "LangGraph": "https://langchain-ai.github.io/langgraph/",
    "LangChain": "https://www.langchain.com",
    "PyTorch": "https://pytorch.org",
    "TensorFlow": "https://www.tensorflow.org",
    "OpenCV": "https://opencv.org",
    "Hugging Face": "https://huggingface.co",
    "Ollama": "https://ollama.com",
    "Anthropic": "https://www.anthropic.com",
    "OpenAI": "https://openai.com",
    "Google Gemini": "https://ai.google.dev",
    "Groq": "https://groq.com",
    "Cerebras": "https://www.cerebras.ai",
    "Mistral": "https://mistral.ai",
    "OpenRouter": "https://openrouter.ai",
    "NVIDIA NIM": "https://build.nvidia.com",
    "Workers AI": "https://developers.cloudflare.com/workers-ai/",
    "Voyage AI": "https://www.voyageai.com",
    "Cohere": "https://cohere.com",
    "Jina AI": "https://jina.ai",
    "ZeroEntropy": "https://www.zeroentropy.dev",
    "tiktoken": "https://github.com/openai/tiktoken",
    "HyDE": "https://arxiv.org/abs/2212.10496",
    "ElevenLabs": "https://elevenlabs.io",
    "Cartesia": "https://cartesia.ai",
    "Fish Audio": "https://fish.audio",
    "Speechmatics": "https://www.speechmatics.com",
    "YOLO": "https://docs.ultralytics.com",
    "U-Net": "https://arxiv.org/abs/1505.04597",
    "ArcFace": "https://arxiv.org/abs/1801.07698",
    "RetinaFace": "https://arxiv.org/abs/1905.00641",
    # Data
    "PostgreSQL": "https://www.postgresql.org",
    "pgvector": "https://github.com/pgvector/pgvector",
    "Neo4j": "https://neo4j.com",
    "Redis": "https://redis.io",
    "MySQL": "https://www.mysql.com",
    "Drizzle ORM": "https://orm.drizzle.team",
    "Neon": "https://neon.com",
    "SQLite": "https://www.sqlite.org",
    "ltree": "https://www.postgresql.org/docs/current/ltree.html",
    "Cloudflare R2": "https://developers.cloudflare.com/r2/",
    "MinIO": "https://www.min.io",
    "Drizzle Kit": "https://orm.drizzle.team/docs/kit-overview",
    # Cloud
    "Oracle Cloud": "https://www.oracle.com/cloud/",
    "AWS": "https://aws.amazon.com",
    "Cloudflare": "https://www.cloudflare.com",
    "Vercel": "https://vercel.com",
    "Docker": "https://www.docker.com",
    "Caddy": "https://caddyserver.com",
    "OCI Ampere A1": "https://www.oracle.com/cloud/compute/arm/",
    "AWS S3": "https://aws.amazon.com/s3/",
    "AWS KMS": "https://aws.amazon.com/kms/",
    "AWS Rekognition": "https://aws.amazon.com/rekognition/",
    "Cloudflare Tunnel": "https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/",
    "Turnstile": "https://www.cloudflare.com/products/turnstile/",
    "systemd": "https://systemd.io",
    "GHCR": "https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry",
    "Docker Buildx": "https://github.com/docker/buildx",
    # Tooling
    "GitHub Actions": "https://github.com/features/actions",
    "Dependabot": "https://docs.github.com/en/code-security/dependabot",
    "Turborepo": "https://turborepo.com",
    "pnpm": "https://pnpm.io",
    "Playwright": "https://playwright.dev",
    "Vitest": "https://vitest.dev",
    "Sentry": "https://sentry.io",
    "Infisical": "https://infisical.com",
    "ESLint": "https://eslint.org",
    "pytest": "https://docs.pytest.org",
    "Ruff": "https://docs.astral.sh/ruff/",
    "mypy": "https://mypy-lang.org",
    "Sightengine": "https://sightengine.com",
    "Arachnid Shield": "https://projectarachnid.ca/en/",
    "Arduino": "https://www.arduino.cc",
    "ESP32": "https://www.espressif.com/en/products/socs/esp32",
    "Raspberry Pi": "https://www.raspberrypi.com",
    "Coral Edge TPU": "https://coral.ai",
}

CORE = [
    ("Languages", "languages", ["TypeScript", "Python", "JavaScript", "PHP", "Java", "C"]),
    ("Web", "web", ["Next.js", "React", "NestJS", "FastAPI", "Laravel", "Tailwind CSS", "Node.js"]),
    ("AI & ML", "ai", ["LangGraph", "LangChain", "PyTorch", "TensorFlow", "OpenCV",
                       "Hugging Face", "Ollama"]),
    ("Data", "data", ["PostgreSQL", "pgvector", "Neo4j", "Redis", "MySQL", "Drizzle ORM"]),
    ("Cloud", "cloud", ["Oracle Cloud", "AWS", "Cloudflare", "Vercel", "Docker", "Caddy"]),
    ("Tooling", "tooling", ["GitHub Actions", "Turborepo", "pnpm", "Playwright", "Vitest",
                            "Sentry", "Infisical"]),
]

FULL = [
    ("Web & realtime", "web", ["Better Auth", "Socket.IO", "Yjs", "Hocuspocus", "Tiptap",
                               "TanStack Query", "Zustand", "shadcn/ui", "Radix UI", "BullMQ",
                               "Fastify", "Serwist", "Resend", "Alpine.js", "Bootstrap",
                               "CodeIgniter"]),
    ("Model providers", "ai", ["Anthropic", "OpenAI", "Google Gemini", "Groq", "Cerebras",
                               "Mistral", "OpenRouter", "NVIDIA NIM", "Workers AI"]),
    ("Retrieval & ranking", "ai", ["Voyage AI", "Cohere", "Jina AI", "ZeroEntropy", "tiktoken",
                                   "RRF hybrid search", "HyDE"]),
    ("Speech", "ai", ["ElevenLabs", "Cartesia", "Fish Audio", "Speechmatics"]),
    ("Vision & biometrics", "ai", ["YOLO", "U-Net", "ArcFace", "RetinaFace"]),
    ("Data & storage", "data", ["Neon", "SQLite", "ltree", "Cloudflare R2", "MinIO", "Drizzle Kit"]),
    ("Cloud & infrastructure", "cloud", ["OCI Ampere A1", "AWS S3", "AWS KMS", "AWS Rekognition",
                                         "Cloudflare Tunnel", "Turnstile", "systemd", "GHCR",
                                         "Docker Buildx", "Blue-green deploys"]),
    ("Quality & safety", "tooling", ["ESLint", "pytest", "Ruff", "mypy", "Dependabot",
                                     "Sightengine", "Arachnid Shield"]),
    ("Hardware", "tooling", ["Arduino", "ESP32", "Raspberry Pi", "Coral Edge TPU"]),
]


def picture(dark_src, light_src, alt, extra_dark=None, extra_light=None, width=None, href=None):
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
    # A link has to wrap the whole picture: GitHub serves these SVGs through an
    # <img>, and a browser never activates <a> elements inside an image document,
    # so there is no way to make only the interchange clickable.
    tag = f'<picture>\n{body}\n  <img alt="{alt}" src="{light_src}"{w}>\n</picture>'
    return f'<a href="{href}">\n{tag}\n</a>' if href else tag


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

BANNER = SITE + "/api/readme-banner"

ALT = ("Transit-style diagram of Dave Zachary Macarayo's stack. Six colour-coded lines "
       "(Languages, Web, AI & ML, Data, Cloud and Tooling) run left to right and converge on a "
       "single interchange labelled NovelVerse, a multi-service AI platform built with Next.js, "
       "NestJS and FastAPI.")

CONTRACT = """<!--
Generated by scripts/build_readme.py. Edit the script, not this file.

THESIS: a stack is a network, not a logo wall. Colour names the line (the
layer), never the vendor, and the stations are where the work connects.
WORLD: Beck/Vignelli transit diagram. Six line colours on GitHub's own canvas,
transparent ground, Overpass drawn to outlines, 45-degree kinks, tick stations,
circle-and-bar interchange. Documented in DESIGN.md.
RULE: every station on the map is something NovelVerse actually runs, because
every line terminates there. Skills used elsewhere live in Stack instead.
-->"""

doc = []
A = doc.append

A(CONTRACT)
A(f'<a href="{SITE}"><img alt="Dave Zachary Macarayo, Web Developer and AI Engineer" '
  f'src="{BANNER}" width="100%"></a>')
A("")
A("Computer Engineering graduate building production AI systems end to end: Postgres schema")
A("and retrieval pipelines, a multi-provider model router, and the interface people actually")
A(f"read. Based in the Philippines. [Portfolio]({SITE}) · open to opportunities.")
A("")
A("## Stack")
A("")
A(picture("assets/map-wide-dark.svg", "assets/map-wide-light.svg", ALT,
          "assets/map-narrow-dark.svg", "assets/map-narrow-light.svg", href=NOVELVERSE))
A("")
A("Each line is a layer. Colour marks the line, not the vendor. Every station above runs in")
A("NovelVerse; the rest of what I use is below.")
A("")
for name, key, items in CORE:
    A(line(name, key, items))
    A("")
A("<details>")
A("<summary>Full inventory: everything else in production use</summary>")
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
A(f"**[NovelVerse]({NOVELVERSE})** is a multi-service AI writing platform, built solo. The")
A("repository is private. A Turborepo/pnpm monorepo splitting a Next.js reader and manuscript")
A("editor, a NestJS + Fastify business API, and a FastAPI AI service. Live collaborative")
A("editing over Yjs and Hocuspocus; hybrid retrieval across pgvector and a Neo4j knowledge")
A("graph; a multi-provider model router with circuit breaking and per-provider budgets across")
A("nine LLM vendors; a TTS/STT gateway over four speech providers. Runs on an OCI Ampere A1")
A("host behind Cloudflare, with blue-green releases, nightly backups and monthly recovery")
A("drills.")
A("")
A(f"**[portfolio](https://github.com/{USER}/portfolio)** is a universe-themed Next.js site with")
A("a Canvas 2D galaxy and a black-hole cursor, plus a content-first Focus mode for anyone who")
A(f"would rather just read. Live at [{SITE.split('//')[1]}]({SITE}).")
A("")
A(f"**Biometrics and computer vision.** [Iris detection with YOLO]"
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

if __name__ == "__main__":
    # Guarded so check_links.py can import LINKS without rewriting the README.
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write("\n".join(doc).rstrip() + "\n")
    print(f"README.md  {os.path.getsize(OUT) / 1024:.1f} KB  ({len(doc)} blocks)")
