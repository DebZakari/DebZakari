"""Verify every badge destination resolves.

A badge that looks authoritative and lands on a 404 is worse than a badge with
no link at all, so this runs before publishing and in CI.
"""
import concurrent.futures as cf
import sys
import urllib.error
import urllib.parse
import urllib.request

from build_readme import LINKS

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")


# Hosts that answer a bot with 403 but serve the page fine in a browser. Checked
# by hand; keep this list short and re-verify anything added to it.
BOT_BLOCKED = {"www.mysql.com"}


def probe(item):
    name, url = item
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return name, url, r.status, None
        except urllib.error.HTTPError as e:
            # Plenty of sites reject HEAD but serve GET fine.
            if method == "HEAD":
                continue
            if e.code == 403 and urllib.parse.urlsplit(url).netloc in BOT_BLOCKED:
                return name, url, 200, None
            return name, url, e.code, None
        except Exception as e:  # DNS, TLS, timeout
            if method == "HEAD":
                continue
            return name, url, None, type(e).__name__
    return name, url, None, "unreachable"


with cf.ThreadPoolExecutor(max_workers=12) as pool:
    results = sorted(pool.map(probe, LINKS.items()))

# 3xx is fine: Google's developer sites bounce every request through a silent
# SSO probe that lands back on the documentation page.
bad = [r for r in results if not (r[2] and 200 <= r[2] < 400)]
for name, url, status, err in bad:
    print(f"  {name:22} {status or err}  {url}")

print(f"\n{len(results) - len(bad)}/{len(results)} badge links OK")
sys.exit(1 if bad else 0)
