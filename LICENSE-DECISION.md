# 公开使用许可决策 / License selection

**决策已记录（2026-10-11）：** 仓库所有者已为 AI-KSK 原创部分选定 **Apache-2.0**。实际条款见根目录 [`LICENSE`](LICENSE)，版权归属与第三方边界见 [`NOTICE`](NOTICE)。

**Decision recorded (2026-10-11):** the repository owner has selected **Apache-2.0** for the AI-KSK-authored materials. The full terms are in the root [`LICENSE`](LICENSE); attribution and third-party scope are in [`NOTICE`](NOTICE).

## 决策背景 / Background

This repository contains authored workflow JSON, documentation and Python helper scripts originally assembled for AI-KSK. The owner has now **explicitly selected and published** a license, as required before inviting reuse, forks, or commercial redistribution. GitHub public visibility alone is not an open-source license — the root `LICENSE` file is what grants rights.

## 范围 / Scope

Apache-2.0 covers **only** the AI-KSK original materials in this repository: skill documents and assets, authored ComfyUI workflow JSON, the parameter manifest, the Python helper/verifier scripts, tests and documentation.

It does **not** cover third-party components. In particular the Qwen Image 2.1 Fun Union ControlNet weights are distributed upstream under the Qwen Research License (non-commercial research and evaluation use only) and are **not bundled here**. Third-party node packages (`Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8`, `comfyui_controlnet_aux`) keep their own upstream licenses. See [`NOTICE`](NOTICE) and [`docs/LICENSES_AND_ATTRIBUTION_CN.md`](docs/LICENSES_AND_ATTRIBUTION_CN.md).

## 已考虑的备选 / Options considered

- **MIT**：广泛复用与商用较宽松，需保留版权与许可证声明。
- **Apache-2.0**：宽松复用且有明确的专利授权框架。← 已选定 / selected
- **自定义非商业许可**：不等同于 OSI 认可的开源许可，应由权利人拟定并审阅。
- **保留所有权**：可以公开展示与阅读，但他人没有获得一般再分发/修改授权；不适合希望社区贡献的项目。

## 维护者提示 / Maintainer note

本文件仅记录所有者的许可决策，不构成法律意见，也不改变任何第三方权重或依赖的条款。如需变更许可，应同步更新根目录 `LICENSE`、`NOTICE`、`README.md`、`README_EN.md` 与 GitHub About 说明。
