# 公开使用许可决策记录 / License decision record

**状态：已由维护者确认（2026-10-11）。** 维护者确认 AI-KSK 原创部分采用 **Apache-2.0**。许可条款见 [`LICENSE`](LICENSE)；版权归属、覆盖范围与第三方非覆盖清单见 [`NOTICE`](NOTICE)。

**Status: confirmed by the maintainer on 2026-10-11.** The maintainer confirmed **Apache-2.0** for the AI-KSK-authored materials. The terms are in [`LICENSE`](LICENSE); attribution, scope and the third-party carve-out are in [`NOTICE`](NOTICE).

## 决策与确认过程 / How this decision was made and confirmed

1. 在公开发布准备阶段，维护者被要求为 AI-KSK 原创部分选择许可方式，候选为：暂不提供 LICENSE、MIT、Apache-2.0。
2. 维护者选择 **Apache-2.0**。
3. 随后对仓库执行了一次许可与版权审计。审计指出：先前的记录把授权表述得过于笼统，且覆盖范围清单仍列有已被移出主分支的文件。
4. 维护者于 2026-10-11 **再次明确确认** Apache-2.0。
5. 本记录、`NOTICE`、`README.md` / `README_EN.md` 与相关文档据此更正。

## 范围 / Scope

Apache-2.0 覆盖 `NOTICE` 中列明的 AI-KSK 原创材料：`skills/qwen-image-2-1-creator/` 技能目录、仓库级文档、示例、CI 与配置文件。

它**不覆盖**任何第三方材料：模型权重、T8 Union 节点及其上游示例工作流、`comfyui_controlnet_aux`、派生进 `skills/qwen-image-2-1-creator/assets/reference_11groups.json` 的 ComfyUI 官方模板材料（MIT，Copyright (c) 2023-present Comfy Org），以及任何第三方素材。完整清单与上游条款原文见 [`NOTICE`](NOTICE) 与 [`docs/LICENSES_AND_ATTRIBUTION_CN.md`](docs/LICENSES_AND_ATTRIBUTION_CN.md)。

## 已考虑的备选 / Options considered

- **MIT**：广泛复用与商用较宽松，需保留版权与许可证声明。
- **Apache-2.0**：宽松复用且有明确的专利授权框架。← 已选定并确认 / selected and confirmed
- **自定义非商业许可**：不等同于 OSI 认可的开源许可，应由权利人拟定并审阅。
- **保留所有权**：可以公开展示与阅读，但他人没有获得一般再分发/修改授权；不适合希望社区贡献的项目。

## 维护者提示 / Maintainer note

本文件记录许可决策与其确认过程，不构成法律意见，也不改变任何第三方模型权重、节点或工作流模板的上游条款。如需变更许可，应同步更新 `LICENSE`、`NOTICE`、`README.md`、`README_EN.md`、`CONTRIBUTING.md` 与 GitHub About 说明。
