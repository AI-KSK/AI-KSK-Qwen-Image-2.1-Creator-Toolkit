# AI-KSK · Qwen Image 2.1 Creator Skill

**Version 3.0.0** ｜ [中文 README](README.md)

> This repository is a **Skill package** repository. Its core content is one directory: `skills/qwen-image-2-1-creator/`.
> It ships **no** model weights, generated images or video, and no GPU benchmark results. Installing it and running its static checks requires no GPU.

---

## 1. Overview

**AI-KSK Qwen Image 2.1 Creator Skill** targets Codex and other Agent environments that support the Skill mechanism. It turns the Qwen Image 2.1 creation workflow and the surrounding ComfyUI engineering workflow into a **reusable execution protocol**, together with validation scripts that need nothing but the Python standard library, example tasks, and reference material.

**What it is for**

- Making an Agent produce Qwen Image 2.1 prompts and task JSON to a fixed specification instead of improvising each time.
- Making prompt injection into ComfyUI workflows and the resulting change audit traceable — what changed and what did not.
- Keeping *structural control* (`ControlNet Union`) and *content reference* (`reference_image`) responsibilities separate.
- Producing an executable handoff for an external video model instead of presenting storyboard JSON as a finished video.

**Typical use cases**

| Use case | Description |
| --- | --- |
| Prompt engineering | Draft and review T2I / edit instructions per the official PE-T2I and PE-I2I specifications |
| Image creation and editing | Text-to-image, single/multi-image editing, inpainting, transparency, outpainting, typography posters, subject consistency, storyboards |
| ComfyUI engineering | Task JSON validation, targeted prompt-node injection, workflow diff audit |
| Structural control | Rules and prompt templates for the ControlNet Union + AIO preprocessing route |
| Video handoff | Preparing image-to-video and text-to-video handoff sheets for **external** models such as Wan / H3 |

**What it is not**

- Not a model, not a weight package, not an inference service, not a web UI.
- Not a GPU benchmarking project; the repository contains no measured output or timing data.

---

## 2. Capabilities

Task routes and outputs (full matrix in [`references/capabilities.md`](skills/qwen-image-2-1-creator/references/capabilities.md)):

| Route | Input | Output | Notes |
| --- | --- | --- | --- |
| `t2i` | no reference image | prompt + `wh_ratio` + image | Observational English description of the finished frame |
| `single_edit` | 1 image | edit instruction + image | Instruction-led modification |
| `multi_edit` | 2–10 images | instruction + image | `<image1>`…`<imageN>` roles are mandatory |
| `local_edit` | 1 image + mask | image | Requires a real mask / inpaint input |
| `transparent` | 0 or 1–10 images | RGBA PNG | Alpha must survive; JPEG is not acceptable |
| `outpaint` | 1 image | image | Extension edges and target ratio must be explicit |
| `typography` | 0 or 1+ images | image | Text is locked literally and verified by a human |
| `identity` | 1–10 images | image | Person / outfit / product consistency and scene variants |
| `storyboard` | 0 or 1–10 images | image | Static multi-panel storyboard, not video |
| `benchmark` | 0–10 images | JSON | Skill-orchestrated parameter and quality audit |
| CN variants: `cn_t2i` / `cn_single_ref` / `cn_multi_ref` / `cn_inpaint_ref` | reference image(s) + control image (+ mask) | image | Expressed by adding a `control_image` field to an existing mode; there is **no dedicated `cn_*` validator mode** |
| `video_t2v` / `video_i2v` / `video_storyboard` | 0 or 1+ images | **handoff JSON** | Executed by an external video model |

**Explicit limitations (do not overstate)**

- Qwen Image 2.1 is an **image** generation/editing model and does **not** generate video natively; the `video_*` routes only produce a handoff sheet.
- The bundled Python tools **only** validate task input, inject prompt text into an explicitly named node, audit workflow diffs, and generate video handoff sheets. They do **not** download models, run PE-VLM inference, install nodes, wire up 2–10 image ports automatically, or generate images.
- The official "up to 10 reference images" is a **model** capability. It does not mean your ComfyUI workflow actually exposes 1–10 image input ports; verify against your real nodes.
- The ControlNet Union route requires the T8 Union nodes to be genuinely installed. When the environment lacks them, the Skill must say so rather than work around it.
- Anything not verified on real GPU hardware is labelled `runtime_pending` and is never described as tested.

---

## 3. Installation

**The install source is the `skills/qwen-image-2-1-creator/` directory of this repository. There is no separately published ZIP.**
Installing means copying that subdirectory into your Codex skills directory. Do **not** copy the whole repository as a single Skill.

### Windows PowerShell

```powershell
git clone https://github.com/AI-KSK/AI-KSK-Qwen-Image-2.1-Creator-Toolkit.git
Set-Location AI-KSK-Qwen-Image-2.1-Creator-Toolkit

$src  = Join-Path (Get-Location) 'skills\qwen-image-2-1-creator'
$dest = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $env:USERPROFILE '.codex\skills' }

New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Recurse -Force $src (Join-Path $dest 'qwen-image-2-1-creator')

# Verify: SKILL.md should be listed
Get-ChildItem (Join-Path $dest 'qwen-image-2-1-creator') | Select-Object Name
```

### Linux / macOS

```bash
git clone https://github.com/AI-KSK/AI-KSK-Qwen-Image-2.1-Creator-Toolkit.git
cd AI-KSK-Qwen-Image-2.1-Creator-Toolkit

src="$PWD/skills/qwen-image-2-1-creator"
dest="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$dest"
cp -R "$src" "$dest/qwen-image-2-1-creator"

# Verify: SKILL.md should be listed
ls "$dest/qwen-image-2-1-creator"
```

**Installation notes**

- The destination directory name must stay `qwen-image-2-1-creator`, matching `name` in the `SKILL.md` frontmatter.
- An older skill directory (for example `qwen-image-2-1-t2i-creator`) is not removed automatically; retire it yourself if you want to replace it.
- Installing the Skill needs **Python 3.10+** only — no GPU, no model weights, no network access.
- Optional ComfyUI / Union node / model setup is documented in [`docs/INSTALL_CN.md`](docs/INSTALL_CN.md) (Chinese).

---

## 4. Usage

### Calling it from Codex

```
$qwen-image-2-1-creator Review this as three roles (A: prompt, B: workflow engineering, C: QA), then build a Qwen Image 2.1 two-image outfit-transfer workflow: image 1 is the person, image 2 is the garment. Preserve the person's identity strictly, and verify every input port and PreviewImage afterwards.
```

```
$qwen-image-2-1-creator Turn this character turnaround sheet into a continuous four-shot storyboard, and output an image-to-video handoff for Wan2.2. Do not claim Qwen itself generates video.
```

```
$qwen-image-2-1-creator Use ControlNet Union for structural control: this photo is the reference subject, this line art is the control image. Change the pose only, keep identity and outfit, and write the prompt per the cn_single_ref rules.
```

### Local static checks (no GPU required)

Run these **from inside the skill directory**; the example paths are relative to it:

```bash
cd skills/qwen-image-2-1-creator

python scripts/validate_task.py --task examples/multi_edit.json
python scripts/validate_task.py --task examples/t2i_poster.json
python scripts/validate_task.py --task examples/video_storyboard.json
python scripts/video_handoff.py  --task examples/video_storyboard.json --output video_handoff.json
python -m unittest discover -s tests -v
```

Workflow injection and audit:

```bash
python scripts/inject_comfyui.py --workflow assets/reference_11groups.json \
    --task examples/t2i_poster.json --node-title 'T2I-01｜正向提示词' --output updated.json
python scripts/audit_comfyui.py --original assets/reference_11groups.json \
    --updated updated.json --allowed-titles 'T2I-01｜正向提示词'
```

The injection script rewrites only the explicitly named prompt node and **never overwrites your original workflow**; it fails outright when the node is missing or the title is ambiguous, and it will not guess node IDs.

---

## 5. Repository layout

```text
AI-KSK-Qwen-Image-2.1-Creator-Toolkit/
├── README.md / README_EN.md        # Chinese and English entry points
├── LICENSE / NOTICE                # License and copyright boundaries
├── LICENSE-DECISION.md             # License decision record
├── CHANGELOG.md / CONTRIBUTING.md / SECURITY.md
├── docs/                           # Environment setup, troubleshooting, FAQ, upstream sources, licensing
├── examples/REPRO_LOG_TEMPLATE.csv # Reproduction log template
├── skills/qwen-image-2-1-creator/  # ★ the Skill itself
└── .github/                        # CI and issue / PR templates
```

### Skill directory responsibilities

| Path | Responsibility |
| --- | --- |
| `SKILL.md` | Main protocol: execution order, task routing, PE prompt specification, ControlNet Union rules, workflow scheduling, acceptance red lines. **The primary document for both users and Agents.** |
| `README.md` | Short skill description and invocation examples. |
| `references/` | Capability matrix, official sources, three-role review, PE inference boundaries, CN + reference rules, video handoff, quality rubric. |
| `examples/` | Task JSON files directly checkable with `scripts/validate_task.py`, covering T2I, editing, inpainting, transparency, outpainting, typography, identity, storyboard, video handoff and the CN routes. |
| `scripts/` | Python standard-library scripts: task validation, ComfyUI prompt injection, workflow diff audit, video handoff generation. |
| `tests/` | Skill unit tests verifying route rules and example consistency. |
| `assets/` | Task JSON schema example, legacy prompt reference, and the 11-group A/B ComfyUI template starting point. |

---

## 6. Environment and model dependencies

| Task type | Required environment | GPU needed |
| --- | --- | --- |
| Installing the Skill, reading docs | none (file copy only) | no |
| Task JSON validation, example checks, unit tests | Python 3.10+ standard library | no |
| Video handoff generation | Python 3.10+ standard library | no |
| ComfyUI workflow injection and diff audit | Python 3.10+ standard library + your workflow JSON | no |
| Real text-to-image / editing / ControlNet Union | ComfyUI with Qwen Image 2.1 support + model weights, or a platform such as RunningHub | **yes** |
| PE-T2I / PE-I2I prompt model inference | separately deployed official PE weights or service | depends |
| Image-to-video / text-to-video | an **external** video model (e.g. Wan / H3), deployed separately | **yes** |

Concrete download locations, file names and target directories for models and nodes are documented in [`docs/INSTALL_CN.md`](docs/INSTALL_CN.md) (Chinese); upstream source mapping is in [`docs/TECHNICAL_SOURCES.md`](docs/TECHNICAL_SOURCES.md).

---

## 7. Copyright and license

**Original content in this repository** is licensed under **Apache-2.0**, confirmed by the maintainer on 2026-10-11. See [`LICENSE`](LICENSE) for the terms; **the authoritative scope statement and third-party carve-out are in [`NOTICE`](NOTICE)**; the decision and confirmation record is in [`LICENSE-DECISION.md`](LICENSE-DECISION.md).

**That license does not cover the following third-party material**, which remains under its own upstream terms:

- **Model weights** — Qwen Image 2.1 weights are not distributed with this repository.
- **T8 Qwen Image 2.1 Fun ControlNet Union** — the custom node code and the converted weights have their own licenses; the converted weights carry research / non-commercial use restrictions that publishing this repository does **not** remove.
- **comfyui_controlnet_aux / Depth Anything V2** and other third-party nodes and preprocessors.
- **ComfyUI official workflow-template material (MIT, Copyright (c) 2023-present Comfy Org)** — `skills/qwen-image-2-1-creator/assets/reference_11groups.json` is derived from a ComfyUI workflow template and retains its model-download and registry metadata. The upstream MIT attribution and full license text are reproduced in [`NOTICE`](NOTICE) as MIT requires; that material is **not** relicensed by this repository's Apache-2.0 grant.
- **Third-party assets** — this repository contains no portraits, illustrations, screenshots or copyrighted images belonging to others.

**Not included in this repository**: model weights, API keys, cookies, signed URLs, RunningHub account configuration, private test images, or GPU output.

Check each upstream license before commercial use. Nothing in this section or in `NOTICE` is legal advice. The layered breakdown is in [`docs/LICENSES_AND_ATTRIBUTION_CN.md`](docs/LICENSES_AND_ATTRIBUTION_CN.md) (Chinese).

---

## 8. Author and project

- **Maintainer**: AI-KSK
- **Project home**: <https://github.com/AI-KSK/AI-KSK-Qwen-Image-2.1-Creator-Toolkit>
- **Skill directory**: [`skills/qwen-image-2-1-creator/`](skills/qwen-image-2-1-creator/)
- **Feedback**: open an issue using the [issue template](.github/ISSUE_TEMPLATE/bug_report.md). Strip tokens, cookies, signed URLs and personal data from logs first; see [`SECURITY.md`](SECURITY.md).

Forks and further development on top of the existing structure are welcome. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) first.
