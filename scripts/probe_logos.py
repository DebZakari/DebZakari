"""Find a working shields.io logo slug for each stack entry.

shields.io follows simple-icons, whose catalog shifts (Amazon, Oracle and Java
were dropped over trademark policy), so every slug is confirmed against the live
service rather than against a vendored list.
"""
import concurrent.futures as cf
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_readme import CORE, FULL

# Where an entry is a feature of a larger product, the parent's logo is accurate
# and better than a bare badge. Where nothing honest exists, the value is None.
OVERRIDE = {
    "Tailwind CSS": "tailwindcss", "Hugging Face": "huggingface",
    "GitHub Actions": "githubactions", "Google Gemini": "googlegemini",
    "Drizzle ORM": "drizzle", "Drizzle Kit": "drizzle",
    "TanStack Query": "tanstack", "Mistral": "mistralai", "NVIDIA NIM": "nvidia",
    "Better Auth": "betterauth", "Radix UI": "radixui", "shadcn/ui": "shadcnui",
    "Raspberry Pi": "raspberrypi", "Fish Audio": "fishaudio",
    # Postgres extensions
    "pgvector": "postgresql", "ltree": "postgresql",
    # Cloudflare's product family
    "Cloudflare R2": "cloudflare", "Cloudflare Tunnel": "cloudflare",
    "Turnstile": "cloudflare", "Workers AI": "cloudflareworkers",
    # GitHub and Docker product family
    "GHCR": "github", "Docker Buildx": "docker",
    # Techniques and papers: no product, no logo.
    "RRF hybrid search": None, "HyDE": None, "Blue-green deploys": None,
    "U-Net": None, "ArcFace": None, "RetinaFace": None, "OCI Ampere A1": None,
}


def slugify(t):
    t = t.lower().replace("+", "plus").replace("&", "and")
    t = re.sub(r"(?<=[a-z0-9])\.(?=[a-z0-9])", "dot", t)
    return re.sub(r"[^a-z0-9]", "", t)


def candidates(name):
    if name in OVERRIDE:
        return [OVERRIDE[name]] if OVERRIDE[name] else []
    c = [slugify(name)]
    bare = slugify(re.sub(r"\s*(AI|Cloud)$", "", name))
    if bare not in c:
        c.append(bare)
    return c


UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"


def works(slug):
    # shields.io 403s the default urllib agent.
    url = f"https://img.shields.io/badge/x-333?style=flat-square&logo={slug}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return b"<image" in r.read()
    except Exception:
        return False


def resolve(name):
    for slug in candidates(name):
        if works(slug):
            return name, slug
    return name, None


items = [i for _, _, g in CORE for i in g] + [i for _, _, g in FULL for i in g]
with cf.ThreadPoolExecutor(max_workers=10) as pool:
    found = dict(pool.map(resolve, items))

hit = {k: v for k, v in found.items() if v}
print(f"{len(hit)}/{len(items)} have a logo\n")
print("MISSING:", ", ".join(k for k, v in found.items() if not v))
json.dump(found, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logos.json"), "w"), indent=1)
