#!/usr/bin/env python3
"""fal.ai batch image generator (Kilo global tool).

- Default model: fal-ai/flux/schnell (cheapest tier on fal ~ $0.003/MP).
- Python standard library only (no pip deps).
- API key: FAL_KEY from this dir's .env (or an env var).
- Job list: the JSON passed to --manifest (defaults + images[]).
  output_dir is resolved relative to the manifest file's directory.

Usage:
  python3 fal_gen.py --manifest path/to/manifest.json            # generate all (skip existing)
  python3 fal_gen.py --manifest ... --only id1,id2               # only the given ids
  python3 fal_gen.py --manifest ... --force                      # overwrite existing
  python3 fal_gen.py --manifest ... --dry-run                    # validate + estimate cost, no API call
"""

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUEUE_BASE = "https://queue.fal.run"

# fal public prices ($/megapixel, may change; budget hint only)
PRICING_PER_MP = {
    "fal-ai/flux/schnell": 0.003,
    "fal-ai/flux/schnell-lora": 0.003,
}
PRESET_SIZES = {
    "square": (512, 512),
    "square_hd": (1024, 1024),
    "portrait": (512, 768),
    "portrait_4_3": (768, 1024),
    "landscape": (768, 512),
    "landscape_16_9": (1024, 576),
}


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def request(url: str, key: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method="POST" if data is not None else "GET",
        headers={
            "Authorization": f"Key {key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "fal-gen/1.0"})
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as f:
        while chunk := resp.read(1 << 16):
            f.write(chunk)


def build_payload(item: dict, defaults: dict) -> dict:
    payload = {
        "prompt": item["prompt"],
        "output_format": defaults.get("output_format", "png"),
    }
    if item.get("negative_prompt") or defaults.get("negative_prompt"):
        payload["negative_prompt"] = (
            item.get("negative_prompt") or defaults["negative_prompt"]
        )
    size = item.get("image_size", defaults.get("image_size", "square_hd"))
    if isinstance(size, list):  # [w, h]
        payload.update({"image_size": "custom", "width": size[0], "height": size[1]})
    else:
        payload["image_size"] = size
    for k in ("num_inference_steps", "guidance_scale", "seed"):
        if k in item:
            payload[k] = item[k]
        elif k in defaults:
            payload[k] = defaults[k]
    return payload


def estimate_usd(model: str, payload: dict) -> float:
    rate = PRICING_PER_MP.get(model, 0.003)
    if payload.get("image_size") == "custom":
        w, h = payload.get("width", 1024), payload.get("height", 1024)
    else:
        w, h = PRESET_SIZES.get(payload.get("image_size", "square_hd"), (1024, 1024))
    return (w * h) / 1_000_000 * rate


def generate(key: str, model: str, payload: dict, dest: Path, timeout: int) -> None:
    submit = request(f"{QUEUE_BASE}/{model}", key, payload)
    status_url, response_url = submit["status_url"], submit["response_url"]
    deadline = time.monotonic() + timeout
    seen = None
    while time.monotonic() < deadline:
        st = request(status_url, key)
        status = st.get("status") or st.get("queue_status")
        if status != seen:
            print(f"    [{status}]", flush=True)
            seen = status
        if status == "COMPLETED":
            break
        if status in ("FAILED", "ERROR"):
            raise RuntimeError(f"{model} generation failed: {json.dumps(st)[:400]}")
        time.sleep(2)
    else:
        raise TimeoutError(f"{model} did not finish within {timeout}s")
    result = st
    images = st.get("images") or (st.get("response") or {}).get("images") or []
    if not images:
        result = request(response_url, key)
        images = result.get("images") or []
    if not images:
        raise RuntimeError(f"No images in response: {json.dumps(result)[:400]}")
    download(images[0]["url"], dest)


def main() -> int:
    ap = argparse.ArgumentParser(description="fal.ai batch image generation")
    ap.add_argument("--manifest", required=True, help="manifest JSON path")
    ap.add_argument("--only", help="comma-separated id list")
    ap.add_argument("--force", action="store_true", help="overwrite existing outputs")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--timeout", type=int, default=300)
    args = ap.parse_args()

    load_env(HERE / ".env")
    key = os.environ.get("FAL_KEY", "")
    if not args.dry_run and not key:
        print(
            f"Error: FAL_KEY not found. Put it in {HERE / '.env'} "
            "fal.ai using the API key from https://fal.ai/dashboard/keys.",
            file=sys.stderr,
        )
        return 2

    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    defaults = manifest.get("defaults", {})
    out_dir = manifest_path.parent / manifest.get("output_dir", "generated")
    only = set(args.only.split(",")) if args.only else None

    total = 0.0
    done = skipped = 0
    for item in manifest["images"]:
        if only and item["id"] not in only:
            continue
        model = item.get("model", defaults.get("model", "fal-ai/flux/schnell"))
        payload = build_payload(item, defaults)
        dest = out_dir / item.get("output", f"{item['id']}.png")
        cost = estimate_usd(model, payload)
        total += cost
        tag = f"[{item['id']}] {model} ~${cost:.4f}"
        if dest.exists() and not args.force:
            print(f"skip (exists) {tag} -> {dest.name}")
            skipped += 1
            continue
        if args.dry_run:
            print(f"dry-run {tag} -> {dest.relative_to(out_dir.parent)}")
            skipped += 1
            continue
        print(f"generate {tag} -> {dest.name}", flush=True)
        generate(key, model, payload, dest, args.timeout)
        done += 1
    print(f"\nDone: generated {done} / skipped {skipped}; budget cap ≈ ${total:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
