# Public release status

Last updated: 2026-10-11 (reorganized as a Skill-focused repository)

## Scope

This repository is positioned as a **public Creator Skill repository**. The single core deliverable is `skills/qwen-image-2-1-creator/` (Skill v3.0.0).

## Included

- The complete AI-KSK Qwen Image 2.1 Creator Skill v3.0.0: `SKILL.md`, `README.md`, `references/`, `examples/`, `scripts/`, `tests/`, `assets/`.
- Documentation: environment/dependency setup, troubleshooting, FAQ, upstream source mapping, licensing and attribution.
- Repository-level files: license, notice, contributing, security, changelog, CI, issue and PR templates, reproduction log template.

## Not included

- Any model weight or checkpoint.
- Any generated image or video, GPU output, benchmark timing, or screenshot.
- Any original image, private sample, signed media URL, API credential, cookie or account configuration.
- The former Depth ControlNet Union 75-grid experiment (workflow JSONs, parameter matrix, its verifier and its documentation). It was moved out of the main release content and is preserved at the git tag `archive/depth75-v0.1.0`.

## Offline verified

- Skill unit tests: 12/12 pass (Python 3.10+ standard library only).
- All example task JSON files validate against the Skill's task rules.
- Video handoff generation produces the expected handoff JSON.
- Python scripts compile cleanly and import standard library only.
- Documentation links, install commands and referenced paths resolve on disk.
- No credentials, private IPs, personal data or third-party assets are present.

## Runtime status

**NOT VERIFIED in ComfyUI, RunningHub or any GPU environment.** Do not claim tested output images, measured VRAM, timing or cross-version compatibility. Anything unverified is treated as `runtime_pending`.

## Licensing

Original AI-KSK materials are published under the terms in the root `LICENSE`. The maintainer confirmed Apache-2.0 on 2026-10-11; the authoritative scope statement and third-party carve-out are in `NOTICE`, and the confirmation record is in `LICENSE-DECISION.md`. That license does not extend to third-party nodes or model weights; the Qwen Image 2.1 Fun Union weights remain under their own research / non-commercial terms and are not bundled here. `skills/qwen-image-2-1-creator/assets/reference_11groups.json` is derived from a Comfy-Org workflow template; its upstream MIT notice is retained in `NOTICE` and that material is not relicensed by this repository's grant.
