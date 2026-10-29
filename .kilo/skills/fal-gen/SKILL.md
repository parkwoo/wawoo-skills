---
name: fal-gen
description: Batch-generate design images (avatars / illustrations / backgrounds / textures) with fal.ai. Use when a task needs generated or filled-in design assets, bulk image generation, or when the user mentions fal.ai / FAL_KEY / flux. Defaults to the cheapest model, flux/schnell.
---

# fal-gen — fal.ai batch image generation

Generate the images a design phase needs (avatars, medical illustrations, hero backgrounds, textures, ...) in batches with this skill.
Default model **`fal-ai/flux/schnell`** = fal's cheapest tier (≈ $0.003/MP, 4 inference steps); a typical batch of 5 images ≈ $0.01. The script uses only the Python standard library.

## One-time setup (API key)

The user writes the key into `.env` in this skill directory (if missing, copy the template and ask the user to fill it — **do not** invent a key):

```bash
cp .env.example .env
# edit: FAL_KEY=key_id:secret_value
# get one: https://fal.ai/dashboard/keys
```

`.env` contains a secret: never commit it or echo its contents.

## Usage

Write a manifest JSON inside the project (see `templates/manifest.example.json`), then:

```bash
S=.kilo/skills/fal-gen
python3 $S/fal_gen.py --manifest <project>/fal-manifest.json --dry-run   # validate + estimate cost
python3 $S/fal_gen.py --manifest <project>/fal-manifest.json             # generate (skip existing)
python3 $S/fal_gen.py --manifest ... --only id1,id2                      # selected ids only
python3 $S/fal_gen.py --manifest ... --force                             # regenerate
```

- `output_dir` is resolved relative to the manifest file (e.g. manifest at `docs/demo/ui-pro/`, `"output_dir": "generated"` → `docs/demo/ui-pro/generated/`).
- Existing outputs are skipped by default → idempotent and safe to re-run.

## Manifest format

```json
{
  "output_dir": "generated",
  "defaults": {
    "model": "fal-ai/flux/schnell",
    "image_size": "square_hd",
    "output_format": "png",
    "num_inference_steps": 4,
    "negative_prompt": "text, watermark, logo, blurry, deformed hands"
  },
  "images": [
    { "id": "hero", "prompt": "...", "image_size": [1024, 576] },
    { "id": "avatar", "prompt": "...", "image_size": "square", "seed": 42 }
  ]
}
```

- `image_size`: `square|square_hd|portrait|portrait_4_3|landscape|landscape_16_9` or `[width,height]`.
- Prompts work best in English; to avoid text, keep `text, watermark` in `negative_prompt`.
- Higher quality (pricier): `fal-ai/flux/dev` (≈$0.025/MP) or `fal-ai/flux-pro/v1.1`; override `model` per item as needed.

## Working rules

1. Run `--dry-run` first and show the cost estimate; generate only after the user confirms (generation costs real money).
2. Inspect each generated image; if it is not good, adjust prompt/seed and regenerate with `--force --only <id>`.
3. Put outputs in the project's design-asset directory (e.g. `docs/demo/**/generated/`), not in `lib/`.

## Attribution

Authored in this repository — **MIT**, Copyright (c) 2026 **wawoo.jp**.
