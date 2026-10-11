# AI-KSK · Qwen Image 2.1 Creator Toolkit

[中文 README](README.md)

This is a GitHub-ready source repository containing a **75-case Qwen Image 2.1 Fun Union Depth ControlNet benchmark** and the Chinese **AI-KSK Qwen Image 2.1 Creator Skill v3**.

**Status: static checks passed; GPU/RunningHub inference not verified. No model weights or third-party source images are included.**

## Start here

1. Install [ComfyUI](https://github.com/comfyanonymous/ComfyUI) with Qwen Image 2.1 support (the T8 extension recommends ComfyUI >= 0.37.0).
2. Install [T8 Qwen Image 2.1 Fun Union nodes](https://github.com/T8mars/Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8) and [comfyui_controlnet_aux](https://github.com/Fannovel16/comfyui_controlnet_aux) for automatic depth preprocessing.
3. Download the Qwen Image 2.1 backbone, Qwen3-VL encoder, VAE, Qwen Image 2.1 Fun Union weights, and Depth Anything V2 Base weights. See [installation details](docs/INSTALL_CN.md).
4. Drag [`workflows/depth75/01_first_row_5_previews.json`](workflows/depth75/01_first_row_5_previews.json) into ComfyUI.
5. Select a locally available image in `LoadImage`, verify all checkpoint dropdowns, set a suitable positive prompt, and run the baseline plus the five enabled cells.
6. Once verified on your machine, load [`02_all_75_previews.json`](workflows/depth75/02_all_75_previews.json).

The benchmark varies **control strength** [0.2,0.4,0.6,0.8,1.0], **end percent** [0.6,0.7,0.8,0.9,1.0], and **start percent** [0.0,0.25,0.5], giving 3 × 5 × 5 = 75 outputs plus one no-ControlNet baseline. All cells use seed 9527, Euler, 25 steps, CFG 3.5, Simple scheduler, denoise 1.0; only the three control parameters vary. This is **not** the official 8-step Turbo sigma schedule.

## Skill

The skill itself is in [`skills/qwen-image-2-1-creator/`](skills/qwen-image-2-1-creator/), with instructions, examples and Python stdlib validation tools. Copy just that folder into your Codex skills directory. The skill can validate/manipulate tasks and workflows, but it does **not** install models, guarantee ten connected reference images, run image inference, or generate native video with Qwen Image 2.1.

## Validate offline

```bash
python scripts/check_depth75.py
python -m unittest discover -s tests -v
python -m unittest discover -s skills/qwen-image-2-1-creator/tests -v
```

## Licensing and rights

The model weights and upstream custom node implementation are NOT included. The Qwen Image 2.1 Fun Union weights have **non-commercial research-use restrictions** under the Qwen Research License unless you obtain separate rights. Third-party artwork is not redistributed. The AI-KSK-authored contents of this repository (skill documents, original helper scripts, parameter manifest and authored workflow JSON) are licensed under **Apache-2.0** — see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE). That license does **not** extend to model weights or third-party nodes. No endorsement or affiliation with Qwen, T8 or ComfyUI is implied.

Additional Chinese docs: [benchmark methodology](docs/DEPTH_75_BENCHMARK_CN.md), [troubleshooting](docs/TROUBLESHOOTING_CN.md), [GitHub publishing checklist](docs/GITHUB_PUBLISH_CHECKLIST_CN.md), [source credits](docs/TECHNICAL_SOURCES.md).
