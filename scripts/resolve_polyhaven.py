#!/usr/bin/env python3
"""Resolve Poly Haven assets in an animation manifest.

Usage:
  python scripts/resolve_polyhaven.py examples/10sec-polyhaven.json
  python scripts/resolve_polyhaven.py input.json -o resolved.json

The resolver uses the official Poly Haven public API:
  /search -> /info/{id} -> /files/{id}
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request

API = "https://api.polyhaven.com"


def get(path: str, params: dict | None = None):
    url = API + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


def choose_search(results: dict, asset_type: str) -> str:
    ranked = results.get("results", [])
    if not ranked:
        raise RuntimeError(f"No Poly Haven asset found for type={asset_type}")
    return ranked[0]["slug"]


def choose_file(files: dict, asset_type: str, resolution: str | None):
    # Prefer Blender-native/package formats, then glTF.
    preferred = {
        "models": ["blend", "gltf", "fbx", "usd"],
        "textures": ["blend", "gltf", "mtlx"],
        "hdris": ["hdri"],
    }[asset_type]

    def walk(node, path=()):
        if isinstance(node, dict):
            if "url" in node:
                yield path, node
            for key, value in node.items():
                yield from walk(value, path + (key,))
        elif isinstance(node, list):
            for i, value in enumerate(node):
                yield from walk(value, path + (str(i),))

    candidates = list(walk(files))
    if resolution:
        candidates.sort(key=lambda x: (resolution not in x[0],))
    for fmt in preferred:
        for path, item in candidates:
            if fmt in path:
                return item
    raise RuntimeError(f"No supported file found for type={asset_type}")


def resolve_asset(asset):
    asset_type = asset["type"]
    if asset.get("polyhaven_id"):
        asset_id = asset["polyhaven_id"]
    else:
        query = asset.get("query")
        if not query:
            raise ValueError(f"Asset {asset['id']} needs query or polyhaven_id")
        result = get("/search", {
            "q": query,
            "t": asset_type,
            "limit": 5,
        })
        asset_id = choose_search(result, asset_type)

    info = get(f"/info/{urllib.parse.quote(asset_id, safe='')}")
    files = get(f"/files/{urllib.parse.quote(asset_id, safe='')}")
    selected = choose_file(files, asset_type, asset.get("resolution"))

    return {
        **asset,
        "polyhaven_id": asset_id,
        "name": info.get("name"),
        "category": info.get("category"),
        "thumbnail_url": info.get("thumbnail_url"),
        "file_format": next(
            (fmt for fmt in ["blend", "gltf", "fbx", "usd", "hdri", "mtlx"]
             if fmt in str(selected)),
            asset.get("file_format"),
        ),
        "url": selected["url"],
        "size": selected.get("size"),
        "checksum": selected.get("md5"),
        "provenance": {
            "api": API,
            "info": f"{API}/info/{urllib.parse.quote(asset_id, safe='')}",
            "files": f"{API}/files/{urllib.parse.quote(asset_id, safe='')}",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()

    with open(args.manifest, encoding="utf-8") as f:
        manifest = json.load(f)

    manifest["assets"] = [resolve_asset(asset) for asset in manifest.get("assets", [])]

    output = args.output or args.manifest.replace(".json", ".resolved.json")
    with open(output, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(output)


if __name__ == "__main__":
    main()
