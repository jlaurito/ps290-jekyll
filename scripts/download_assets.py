#!/usr/bin/env python3
"""
Download all real assets (images, PDFs) referenced by the ps290.org Jekyll
mirror from their original hosted URLs (files.edl.io CDN, ps290.org, etc.)
into the local assets/ folder, so the site has no dependency on Edlio's
infrastructure once it goes live.

This is a one-time migration script (same pattern used for the mnspta.org
Neon One asset migration) -- run it once before deploying, or before
cancelling/losing access to the current ps290.org site.

Usage:
    pip install requests --break-system-packages   # if not already installed
    python3 scripts/download_assets.py

Reads scripts/asset-manifest.tsv (format: local_path<TAB>source_url) and:
  1. Downloads each source_url to <repo_root><local_path>
  2. Skips files that already exist locally (safe to re-run)
  3. Reports any failures at the end so they can be retried/investigated

Content files already reference the local paths (e.g. /ps290-jekyll/assets/images/...),
so once the download completes, no further find-and-replace is needed --
just build and deploy the site.
"""

import csv
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("This script requires the 'requests' package.")
    print("Install it with: pip install requests --break-system-packages")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
MANIFEST_PATH = SCRIPT_DIR / "asset-manifest.tsv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PS290-asset-migration/1.0)"
}


def load_manifest():
    entries = []
    with open(MANIFEST_PATH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            if len(row) != 2:
                print(f"  Skipping malformed manifest row: {row!r}")
                continue
            local_path, url = row
            entries.append((local_path.strip(), url.strip()))
    return entries


def download_one(local_path: str, url: str) -> tuple[bool, str]:
    dest = REPO_ROOT / local_path.lstrip("/")
    if dest.exists() and dest.stat().st_size > 0:
        return True, "already exists, skipped"

    dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        dest.write_bytes(resp.content)
        return True, f"downloaded ({len(resp.content):,} bytes)"
    except Exception as exc:  # noqa: BLE001 - report and continue
        return False, str(exc)


def main():
    if not MANIFEST_PATH.exists():
        print(f"Manifest not found at {MANIFEST_PATH}")
        sys.exit(1)

    entries = load_manifest()
    print(f"Found {len(entries)} assets to fetch.\n")

    failures = []
    for i, (local_path, url) in enumerate(entries, start=1):
        ok, message = download_one(local_path, url)
        status = "OK" if ok else "FAILED"
        print(f"[{i}/{len(entries)}] {status}: {local_path}  ({message})")
        if not ok:
            failures.append((local_path, url, message))
        time.sleep(0.2)  # be polite to the source server

    print()
    if failures:
        print(f"{len(failures)} asset(s) failed to download:")
        for local_path, url, message in failures:
            print(f"  - {local_path}\n      {url}\n      error: {message}")
        print("\nRe-run this script to retry -- already-downloaded files are skipped.")
        sys.exit(1)
    else:
        print("All assets downloaded successfully.")


if __name__ == "__main__":
    main()
