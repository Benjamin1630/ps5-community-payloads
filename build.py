#!/usr/bin/env python3
"""Rebuild payloads.json (itsPLK Payload Manager custom-repository format) from upstream GitHub releases."""
import json, os, re, urllib.request

# repo, release asset (regex), filename on the console, name (= folder under /data/pldmgr/payloads), category
SOURCES = [
    # fixed filename so autoload entries survive updates (the project's README recommends this)
    ("holdmysocks/ps5-tailscale", r"tailscale-[\d.]+\.elf", "tailscale.elf", "Tailscale", "Network"),
    ("notmaj0r/ProsperoMgr", r"ProsperoMgr\.elf", "ProsperoMgr.elf", "ProsperoMgr", "Utilities & Tools"),
]

def api(path):
    req = urllib.request.Request("https://api.github.com/" + path, headers={"Accept": "application/vnd.github+json"})
    if os.environ.get("GH_TOKEN"):
        req.add_header("Authorization", "Bearer " + os.environ["GH_TOKEN"])
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

payloads = []
for repo, pattern, filename, name, category in SOURCES:
    rel = api(f"repos/{repo}/releases/latest")  # newest non-draft, non-prerelease
    asset = next(a for a in rel["assets"] if re.fullmatch(pattern, a["name"]))
    payloads.append({
        "id": name.lower(),
        "name": name,
        "filename": filename,
        "url": asset["browser_download_url"],
        "version": rel["tag_name"],
        "last_update": rel["published_at"][:10],
        "description": api(f"repos/{repo}")["description"],
        "category": category,
        "checksum": (asset.get("digest") or "").removeprefix("sha256:"),
        "author": repo.split("/")[0],
        "source": f"https://github.com/{repo}/releases",
        "details_url": f"https://github.com/{repo}",
    })

# Payload Manager rejects entries with a malformed checksum; fail the build instead of publishing one
for p in payloads:
    assert re.fullmatch(r"[0-9a-f]{64}", p["checksum"]), p
    assert p["url"].startswith("https://"), p

# "repository" must sit between "name" and "payloads": Payload Manager <=0.5.x reads each object from a '{' to
# the next '}', so without an object here the wrapper swallows the first payload and it takes the catalog's name.
catalog = {
    "name": "Community Payloads",
    "repository": {"homepage": "https://github.com/Benjamin1630/ps5-community-payloads"},
    "payloads": payloads,
}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "payloads.json"), "w") as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)
    f.write("\n")
