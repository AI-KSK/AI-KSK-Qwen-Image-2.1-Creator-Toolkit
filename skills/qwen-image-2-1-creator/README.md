# AI-KSK Qwen Image 2.1 Creator Skill — v3.0.0

**一个 Skill，覆盖文生图、1~10 张多参考图编辑、ControlNet Union 结构控制、AIO 预处理、局部编辑/遮罩、RGBA 透明图、扩图、文字海报、人物/产品一致性、分镜、横评，以及 Wan/H3 等视频模型接力。**

> 本目录就是技能本体。**安装源就是这个目录，没有另外发布的 ZIP 包。**

## 安装

安装 = 把本目录复制到 Codex 的 skills 目录下，目标目录名保持 `qwen-image-2-1-creator`（与 `SKILL.md` frontmatter 的 `name` 一致）。
只复制本目录，**不要**把整个仓库当作一个 Skill。

### Windows PowerShell

```powershell
git clone https://github.com/AI-KSK/AI-KSK-Qwen-Image-2.1-Creator-Toolkit.git
Set-Location AI-KSK-Qwen-Image-2.1-Creator-Toolkit

$src  = Join-Path (Get-Location) 'skills\qwen-image-2-1-creator'
$dest = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $env:USERPROFILE '.codex\skills' }

New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Recurse -Force $src (Join-Path $dest 'qwen-image-2-1-creator')
```

### Linux / macOS

```bash
git clone https://github.com/AI-KSK/AI-KSK-Qwen-Image-2.1-Creator-Toolkit.git
cd AI-KSK-Qwen-Image-2.1-Creator-Toolkit

dest="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$dest"
cp -R skills/qwen-image-2-1-creator "$dest/qwen-image-2-1-creator"
```

安装只需要 Python 3.10+，不需要 GPU、模型权重或联网。旧技能目录（如 `qwen-image-2-1-t2i-creator`）不会被自动删除，如需替换请自行停用或移出。

## v3.0 新增：ControlNet + 参考图编辑

本版新增 **Qwen Image 2.1 + ControlNet Union + 参考图编辑** 的执行规则，覆盖：

- `control_image` 结构控制（Canny / Depth / HED / Lineart / MLSD / Pose / Scribble / Grayscale）
- `reference_image` / `reference_image_2` / `reference_image_3` 内容参考
- `inpaint_image + mask` 局部重绘
- `AIO Aux Preprocessor` 快速预处理路由
- CN + 单图参考、CN + 双图参考、CN + 三图参考、CN + Inpaint 四类提示词模板

重点文档：

- `references/cn_and_reference_rules.md`
- `references/capabilities.md`
- `examples/cn_single_ref.json`
- `examples/cn_multi_ref.json`
- `examples/cn_inpaint_ref.json`

## 在 Codex 中调用

`$qwen-image-2-1-creator 请先按A模型/提示词、B工作流工程、C质量验收三角色交叉讨论，再制作Qwen Image 2.1双图换装工作流：图1人物、图2服装；严格保持人物ID，完成后检查每一个输入端口和PreviewImage。`

`$qwen-image-2-1-creator 根据这张角色三视图建立连续四镜头分镜，并输出给Wan2.2的图生视频任务交接单；不要宣称Qwen本身能生成视频。`

## 只运行本地静态检查

在**本目录内**执行（示例路径相对于本目录）：

```powershell
python scripts/validate_task.py --task examples/multi_edit.json
python scripts/validate_task.py --task examples/t2i_poster.json
python scripts/video_handoff.py --task examples/video_storyboard.json --output handoff.json
python -m unittest discover -s tests -v
```

不需要联网也可执行静态校验；生成图像/视频仍需你部署模型、上传素材、运行实际 workflow。所有示例图片路径都是占位符，不是附带真实照片。

## 不要混用以下模型

- `Qwen/Qwen-Image-2.1`: Base 生成+编辑。
- `Qwen/Qwen-Image-2.1-Turbo`: 官方 8 步完整 checkpoint，加载自带采样计划。
- `qwen_image_2.1_turbo_lora_avg_rank_178_bf16.safetensors`: 第三方 Turbo LoRA 加速路线，必须单独测试与标记，不能当作官方 Turbo checkpoint。
- `Qwen/Qwen-Image-2.1-PE-T2I`: 官方提示词增强模型，仅用于 T2I prompt 改写。
- `Qwen/Qwen-Image-2.1-PE-I2I`: 官方编辑指令增强模型，仅用于图像编辑 prompt 改写。

参考资料与支持范围：`SKILL.md`、`references/capabilities.md`、`references/official_sources.md`、`references/cn_and_reference_rules.md`。三角色交叉审查：`references/three_role_review.md`。质量验收：`references/benchmark_rubric.md`。

## 注意

本技能的内置 Python 工具负责输入规范检查、指定节点提示词写入、工作流差异审计与视频外部模型交接清单；**不会自动下载模型、执行 PE-VLM 推理、部署节点、自动连接任意10图输入、生成图片或视频。** 这些步骤应由接入该 Skill 的 Agent 在有对应工具和授权的真实环境中执行，并提供可验证日志。模板起点在 `assets/reference_11groups.json`，仅作为示例。

## 许可与署名

- 本 Skill 的原创内容采用 **Apache-2.0**。完整覆盖范围与第三方非覆盖清单见仓库根目录 `LICENSE` 与 `NOTICE`。
- `assets/reference_11groups.json` **派生自 ComfyUI 官方工作流模板**（MIT，Copyright (c) 2023-present Comfy Org），并保留其模型下载与注册表元数据。上游署名与 MIT 许可全文已收录于仓库根目录 `NOTICE`；该材料不在本仓库的 Apache-2.0 授权范围内。
- 模型权重与节点安装、上游来源与授权边界说明见仓库根目录的 `docs/INSTALL_CN.md`、`docs/TECHNICAL_SOURCES.md` 与 `docs/LICENSES_AND_ATTRIBUTION_CN.md`。

仓库地址：<https://github.com/AI-KSK/AI-KSK-Qwen-Image-2.1-Creator-Toolkit>
