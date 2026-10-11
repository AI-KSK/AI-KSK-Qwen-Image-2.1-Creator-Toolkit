# 更新日志 / Changelog

## [0.2.0] - 2026-10-11 — 公开发布整理（以 Creator Skill 为核心）

本次为**仓库整理**，不是新一轮 Skill 研发：Creator Skill v3.0.0 的功能、路由、脚本、示例与测试均未改动。

**变更**

- 仓库定位调整为公开 Creator Skill 仓库，唯一核心项目为 `skills/qwen-image-2-1-creator/`。
- 将 Depth ControlNet Union 75 格实验内容（3 个工作流 JSON、参数矩阵、专用校验脚本、专用测试、专项文档）移出主发布内容；原状态完整保存在 git tag `archive/depth75-v0.1.0`，可随时取回。
- 重写中英文 README：项目简介、能力与限制、Windows PowerShell 与 Linux/macOS 安装步骤、Codex 调用示例、文件结构职责、环境与依赖矩阵、版权许可边界、作者与项目地址。
- 修正技能 `README.md` 中引用**不存在的 ZIP 包**的安装步骤，改为直接从本仓库 `skills/qwen-image-2-1-creator/` 安装。
- CI 改为 Skill 静态检查：脚本编译、全部示例任务校验、视频交接单生成、SKILL.md frontmatter 检查、单元测试。
- 更新 `CONTRIBUTING.md`、Issue / PR 模板、排障与 FAQ 文档，移除 75 格专属内容并修正失效引用。
- 保留第三方模型与 ControlNet Union 的技术说明与授权边界（`docs/TECHNICAL_SOURCES.md`、`docs/LICENSES_AND_ATTRIBUTION_CN.md`），但不再把横评作为安装 Skill 的前置条件。
- 重新生成 `SHA256SUMS.txt` 清单。
- 更新授权文档：`NOTICE` 补齐可核查的覆盖范围清单、限定许可授权对象，并按 MIT 要求完整收录 ComfyUI 官方工作流模板的署名与许可全文（`assets/reference_11groups.json` 派生自该模板）；`LICENSE-DECISION.md` 改为可追溯的决策与确认记录（维护者 2026-10-11 确认 Apache-2.0）。
- 修正不准确的能力声明：`cn_*` 明确为「用现有 mode 表达的 CN 变体」而非独立校验模式；`benchmark` 产物更正为 JSON；补充 `--check-file-existence` 的实际检查范围。
- 修正技能文档中引用不存在的 ZIP 包、未说明的工作目录、以及会被误读为本仓库文件的官方路径。

**未完成（按设计不在本次范围）**

- ComfyUI / RunningHub 真实 GPU 推理、平台版本兼容性验收、性能数据与样片。

## [0.1.0] - 2026-10-11 — 首次公开打包

- 将 AI-KSK Qwen Image 2.1 Creator Skill v3 整理为 GitHub 仓库中的 `skills/` 子目录。
- 同时打包了 Qwen Image 2.1 Depth ControlNet Union 75 格实验的工作流、参数矩阵、静态检查脚本与相关文档。
- 补齐中英文 README、依赖下载清单、排障文档、授权说明与发布流程文档。
- 该版本的 75 格实验部分已在 0.2.0 中移出主分支，见 tag `archive/depth75-v0.1.0`。
