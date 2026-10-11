# AI-KSK · Qwen Image 2.1 Creator Toolkit

**中文使用指南 | [English](README_EN.md)**

面向 **ComfyUI / RunningHub / Codex** 的 Qwen Image 2.1 工作流与创作工程工具包：包含一套 **Depth ControlNet Union 75 格三参数教学横评**、**AI-KSK Qwen Image 2.1 Creator Skill v3**，以及可离线运行的输入任务和 JSON 静态校验工具。

> **当前状态：公开仓库候选版（静态校验通过，GPU / RunningHub 运行时验收待完成）。** 下载 JSON 并不代表模型已安装，也不保证每种 ComfyUI / RunningHub 节点版本均兼容。

## 1. 核心内容

| 模块 | 内容 | 使用入口 |
| --- | --- | --- |
| Depth 75 横评（推荐先试） | 3 个 Start × 5 个 End × 5 个 Weight，共 75 个结果 + 1 个无控制 Baseline | [`workflows/depth75/01_first_row_5_previews.json`](workflows/depth75/01_first_row_5_previews.json) |
| Depth 75 全量版 | 75 条独立控制链，75 个 PreviewImage，全部启用 | [`workflows/depth75/02_all_75_previews.json`](workflows/depth75/02_all_75_previews.json) |
| 手动深度图版 | 不调用 Depth Anything V2 节点，直接上传预处理好的深度图；仅先启用 5 格 | [`workflows/depth75/03_manual_depth_first_row_5.json`](workflows/depth75/03_manual_depth_first_row_5.json) |
| Qwen Creator Skill v3 | 图像生成、单图/多图编辑、CN + 参考图、分镜、任务验证、视频交接 | [`skills/qwen-image-2-1-creator/`](skills/qwen-image-2-1-creator/) |
| 静态校验 | JSON 参数、节点连接、75 格矩阵、两版差异核查 | [`scripts/check_depth75.py`](scripts/check_depth75.py) |

**模型边界：** Qwen Image 2.1 是图像生成/编辑模型；Skill 的视频路由只为外部 Wan / H3 模型准备任务交接，不宣称 Qwen 原生生成视频。Skill 的参考图能力取决于实际节点暴露的端口数量；不能把模型理论支持的张数等同于当前模板可直接接入的张数。

## 2. 开始前需要什么

- **ComfyUI**：建议 0.37.0 或更新且支持 Qwen Image 2.1。
- **专用 Union 自定义节点**：[T8 Qwen Image 2.1 Fun ControlNet Union](https://github.com/T8mars/Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8)。必须包含 `QwenImage21UnionLoader`、`QwenImage21UnionApply`、`QwenImage21UnionLatentFromImage`。
- **深度预处理器**（自动版）：[comfyui_controlnet_aux](https://github.com/Fannovel16/comfyui_controlnet_aux)，提供 `DepthAnythingV2Preprocessor`。
- **模型权重**：Qwen Image 2.1 扩散模型、Qwen3-VL 文本编码器、Qwen 2.1 VAE、Qwen Image 2.1 Fun Union ControlNet 权重、Depth Anything V2 Base 权重（自动版）。**仓库不包含模型权重。**
- Python 3.10+：仅用于本仓库的 Skill 验证与辅助脚本；生成图片仍需要 GPU / 有授权的云端平台。

完整下载来源、文件名与安装目录：[`docs/INSTALL_CN.md`](docs/INSTALL_CN.md)。模型授权与非商业限制：[`docs/LICENSES_AND_ATTRIBUTION_CN.md`](docs/LICENSES_AND_ATTRIBUTION_CN.md)。

## 3. 五分钟快速开始

1. 安装并启用 T8 Union 节点；自动深度版再安装 `comfyui_controlnet_aux`。
2. 下载模型权重，放入对应 `ComfyUI/models/...` 目录。重启 ComfyUI。
3. 拖入 `workflows/depth75/01_first_row_5_previews.json`。
4. 在左侧 `LoadImage` 节点**手动选择自己的合法授权测试图片**，不得使用 JSON 中原有的本地图片文件名作为下载地址。
5. 检查 `UNETLoader`、`CLIPLoader`、`VAELoader`、`QwenImage21UnionLoader` 文件名均能从下拉框选中；必要时改成你本地实际文件名。
6. 修改 `TextEncodeQwenImage21` 正向提示词，使其描述输入图想要生成的内容；各格使用同一提示词与 Seed。
7. 先运行 **Baseline + 首行 5 格**，确认无报错，再导入全量版做 75 格。

> 自动 Depth 工作流中，`control_image` 接收的是深度预处理结果，而不是编辑参考图。**结构控制不等于画风/身份复制**。如需严格保留原人物和厚涂画风，应另外设计并验证 `QwenImage21UnionReferenceEncode` 参考图链，作为另一组实验，而不是混进纯 Depth 横评。

参数变量、Preview 排布、如何解读结果：[`docs/DEPTH_75_BENCHMARK_CN.md`](docs/DEPTH_75_BENCHMARK_CN.md)。

## 4. Creator Skill 安装与测试

在 `skills/qwen-image-2-1-creator/` 有完整的 `SKILL.md`、示例 JSON、参考资料和 Python 标准库脚本。复制该文件夹到你的 Codex `skills` 目录即可，**不要复制整个仓库作为单一 Skill**。原版 Skill 说明：[Skill README](skills/qwen-image-2-1-creator/README.md)。

从仓库根目录执行：

```bash
python scripts/check_depth75.py
python -m unittest discover -s tests -v
python -m unittest discover -s skills/qwen-image-2-1-creator/tests -v
python skills/qwen-image-2-1-creator/scripts/validate_task.py --task skills/qwen-image-2-1-creator/examples/multi_edit.json
```

本地测试仅证明数据结构和脚本规则，不证明生成画质、VRAM、执行耗时或 RunningHub 运行通过。

## 5. 项目结构

```text
AI-KSK-Qwen-Image-2.1-Creator-Toolkit/
├── README.md / README_EN.md
├── workflows/depth75/          # 三套 ComfyUI UI JSON，不是 API JSON
├── skills/qwen-image-2-1-creator/  # 原始 v3 Creator Skill（去除 pycache）
├── scripts/check_depth75.py   # 75格结构校验
├── tests/                     # 静态自动化测试
├── data/depth75_matrix.csv    # 75格的精确参数表
├── docs/                      # 安装、复现、排障、授权、发布清单
├── examples/                  # 参考提示词/参数说明（无第三方原图）
├── .github/                   # CI、Issue、PR 模板
├── .gitignore / .gitattributes
├── LICENSE                    # Apache-2.0，仅覆盖 AI-KSK 原创部分
├── NOTICE                     # 版权归属与第三方许可边界
└── LICENSE-DECISION.md        # 许可证决策记录
```

## 6. 研究和交付边界

- **已静态检查**：76 个 KSampler 的参数布局、75 个 Union Apply、75 个 Preview、唯一三维参数组合、链路引用及类型、5 格版本和全量版本的参数一致性。
- **未运行实测**：任何 ComfyUI / RunningHub 的 GPU 出图、控制效果、耗时、显存峰值、不同环境安装兼容性。
- **许可证**：本仓库 AI-KSK 原创部分（Skill 文档与资产、原创辅助脚本、参数表、自定义工作流 JSON）采用 **Apache-2.0**，条款见 [`LICENSE`](LICENSE)，版权与范围见 [`NOTICE`](NOTICE)。该许可**不覆盖**第三方节点与模型权重：本仓库不附带 Qwen / T8 / Depth Anything 权重，T8 Union ControlNet 权重受到非商业研究授权约束，不能因本仓库公开就用于商业生产。决策记录见 [`LICENSE-DECISION.md`](LICENSE-DECISION.md)。
- **素材版权**：不捆绑用户提供的参考肖像、二次元插画或来源不明的第三方作品。示例请自行上传具有使用权的图片。
- **涉及真实账号的临时媒体链接、签名参数和密钥**：不纳入仓库。

## 7. 参与和反馈

节点/流程问题请按照 [Issue 模板](.github/ISSUE_TEMPLATE/bug_report.md) 提交：**ComfyUI 版本、T8 插件版本、模型文件名、工作流版本、报错原文、节点 ID、复现步骤、是否为 RunningHub 环境**。请移除日志中的 Token / Cookie / 签名链接 / 个人身份信息。

贡献说明：[CONTRIBUTING.md](CONTRIBUTING.md) · 安全反馈：[SECURITY.md](SECURITY.md) · 更新日志：[CHANGELOG.md](CHANGELOG.md)。

## 8. 外部技术来源

Qwen-Image-2.1：<https://huggingface.co/Qwen/Qwen-Image-2.1>  
T8 Union 插件及原生工作流：<https://github.com/T8mars/Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8>  
Union 权重：<https://huggingface.co/t8star/Qwen-Image-2.1-Fun-Controlnet-Union-Comfy>  
Depth Anything V2 预处理器：<https://github.com/Fannovel16/comfyui_controlnet_aux>  

详见 [`docs/TECHNICAL_SOURCES.md`](docs/TECHNICAL_SOURCES.md)。本项目是独立的工作流与 Skill 打包项目，**不代表上述官方或第三方团队的背书**。
