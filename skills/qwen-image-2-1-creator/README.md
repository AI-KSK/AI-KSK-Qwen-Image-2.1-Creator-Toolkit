# AI-KSK Qwen Image 2.1 Creator Skill — v3.0.0

**一个 Skill，覆盖文生图、1~10张多参考图编辑、ControlNet Union 结构控制、AIO 预处理、局部编辑/遮罩、RGBA透明图、扩图、文字海报、人物/产品一致性、分镜、横评，以及 Wan/H3 等视频模型接力。**

## 安装（Windows PowerShell）

把 `Qwen21_Full_Creator_Skill.zip` 放到 Downloads：

```powershell
$zip = Join-Path $env:USERPROFILE 'Downloads\Qwen21_Full_Creator_Skill.zip'
$dest = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $env:USERPROFILE '.codex\skills' }
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Expand-Archive -LiteralPath $zip -DestinationPath $dest -Force
```

如希望替换旧 Skill，可自行停用/移出旧 `qwen-image-2-1-t2i-creator` 目录。新技能名是 `qwen-image-2-1-creator`，不会自动删除旧目录。


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
- `qwen_image_2.1_turbo_lora_avg_rank_178_bf16.safetensors`: 用户既有 LoRA 加速路线，在当前 workflow 适配下另测。
- `Qwen/Qwen-Image-2.1-PE-T2I`: 官方提示词增强模型，仅用于 T2I prompt 改写。
- `Qwen/Qwen-Image-2.1-PE-I2I`: 官方编辑指令增强模型，仅用于图像编辑 prompt 改写。

参考资料与支持范围：`SKILL.md`、`references/capabilities.md`、`references/official_sources.md`、`references/cn_and_reference_rules.md`。三角色交叉审查：`references/three_role_review.md`。质量验收：`references/benchmark_rubric.md`。

## 注意

本技能的内置 Python 工具负责输入规范检查、指定节点提示词写入、工作流差异审计与视频外部模型交接清单；**不会自动下载模型、执行 PE-VLM 推理、部署节点、自动连接任意10图输入、生成图片或视频。** 这些步骤应由接入该 Skill 的 Agent 在有对应工具和授权的真实环境中执行，并提供可验证日志。此前的 11 组 A/B ComfyUI 模板在 `assets/reference_11groups.json`，仅作为示例起点。
