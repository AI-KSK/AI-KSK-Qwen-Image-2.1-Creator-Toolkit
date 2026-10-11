---
name: qwen-image-2-1-creator
description: Qwen Image 2.1 全功能创作与 ComfyUI 工程 Skill。支持文生图(T2I)、单图/双图/多图编辑(1-10参考图)、ControlNet Union 结构控制、AIO 预处理、透明RGBA、圈选/遮罩局部编辑、扩图、文字海报、商品和人物一致性、连续分镜、批量测评及衔接Wan/H3等外部视频模型；先三角色交叉评审，再执行/验收，最后更新Skill。Use for Qwen Image 2.1 creation, editing, multi-reference, ControlNet Union, AIO preprocessing, prompt rewriting, ComfyUI integration, benchmarks, image-to-video handoff. Do not claim native video generation by Qwen Image 2.1.
compatibility: Python 3.10+ standard library for validators and manifests. GPU execution requires separately provisioned Qwen/ComfyUI/RunningHub or external video model. Prompt Enhancer model execution requires the official separate PE-T2I and PE-I2I weights/services.
metadata:
  version: "3.0.0"
  author: "AI-KSK"
---

# Qwen Image 2.1 全功能创作工程 Skill

## 0. 优先执行顺序（必遵守）

**研究资料 → A/B/C 三角色交叉评审 → 执行实际任务 → 静态与运行时验收（标注实测边界）→ 再修改或封装 Skill。** 当前 SKILL.md 是可复用执行协议；不要在未执行用户请求时只产出新的 SKILL.md。

**三角色评审：** A 负责 Qwen 官方能力、PE 提示词与视觉意图；B 负责 ComfyUI/RunningHub 工作流、模型和版本、资源占用、节点连接；C 负责 QA、对比公平性、身份和文字保真、安全边界。A/B/C 必须互相质疑：A 问 B 是否真的有参考图/遮罩输入，B 问 C 是否可复现测评，C 问 A 是否遵守多图指代和固定文字。记录决议与否决。若平台存在真实子代理，用真实子代理分别执行；若没有，只能注明“单助手三角色审查”，绝不虚称三个独立 Agent。

## 1. 先识别任务：原生图像 vs 外部视频

官方模型 Qwen-Image-2.1 是 **图像生成+图像编辑模型**，不原生生成视频文件。官方确认图像编辑可接收 **1-10 张**参考图，支持 RGBA 透明、局部标记（圈选/涂画/遮罩）、主体和商品保真、海报文字、分镜/全景等。每一种玩法先根据部署环境确认输入节点能力；“官方模型支持10张”不代表用户当前 ComfyUI 工作流里一定暴露10个图像端口。

| 路由 | 模型边界 | 输出 |
|---|---|---|
| `t2i` | 原生，无输入图片 | 成片描述 + `wh_ratio` + 图像 |
| `single_edit` | 原生，1张图 | 精准编辑指令 + `ratio_follow` / `wh_ratio` |
| `multi_edit` | 原生，2-10张图 | 明确 `<image1>`…`<imageN>` 的角色 |
| `local_edit` | 原生能力；圈选、绘制标记或 mask 的实际图形管道需验收 | 目标区强修改，非目标区锁定 |
| `transparent` | 原生 RGBA，可生透明图、主体提取和透明图编辑 | 必须保留 alpha 通道，不可 JPEG 破坏 |
| `outpaint` | 原生编辑任务 | 明确扩展边、画幅及连续补全 |
| `typography` | 原生 T2I / 编辑 | 精确逐字记录目标文字并验证 |
| `identity` | 原生单/多图编辑应用 | 人像、服装、商品 ID 与场景变体 |
| `storyboard` | 原生静态图像场景 | 多格分镜、三视图、连贯场景静态图 |
| `benchmark` | Skill 编排，不是模型新能力 | 多组参数/质量/性能审计 |
| `video_t2v` | **外部** Wan/H3 等视频模型 | 视频提示词和调用交接单 |
| `video_i2v` | **外部**视频模型，以 Qwen 生图/编辑结果为首帧/参考 | 视频交接单 |
| `video_storyboard` | Qwen 生成多格分镜，再外部视频模型逐镜头生成 | 镜头列表、关联图片、参数交接单 |

支持官方 Base、官方 Turbo 8-step checkpoint；第三方 **Turbo LoRA + Base** 是另一条单独的测试路线，必须单独标记。不能把 LoRA 路线表述成官方完整 Turbo checkpoint；官方 Turbo 的 sigma 调度也不等同 `Euler + simple` 的任意设置。

## 2. PE 提示词规范（两套必须分开）

**T2I (`Qwen/Qwen-Image-2.1-PE-T2I`):** 以英文描述最终完成画面（观察式），先锁定用户明确指定的对象/数量/色彩/布局/文本，再决定场景、构图、材质、光影；图片上可读的文字加英文直引号 `"..."` 并逐字符保留原文，不允许改写品牌、数字、语言；不堆砌 `masterpiece`, `8K`, `best quality`；把 `wh_ratio` 放元数据，别混进 rewritten_prompt。

**编辑 (`Qwen/Qwen-Image-2.1-PE-I2I`):** 用动作指令开头，说清改什么和不改什么。只单图时自然提图像，不用 `<image1>`；多图时 **必须** 用 `<image1>`, `<image2>`…，逐一规定背景/主体/服装/材质/风格来源。编辑描述语言若用户以中文指令要求，应优先中文，英文指令用英文；图中的文字以用户明确的目标语言和字面为准。`wh_ratio` 与 `ratio_follow` 必须互斥。局部编辑禁止私自“清理”未指定部分；单纯换背景不许顺手改脸，换服装不许私自改姿态。

PE 模型并非普通 Qwen3-VL 文本编码器；没有部署 PE checkpoint 时，可由 Agent 遵照官方公开规范起草/校对，但 **不得宣称执行了 PE 模型推理**。PE 正式 JSON 输出包含 `rewritten_prompt`, `wh_ratio`, `ratio_follow`（官方批处理还包装记录），核对语义再交给生成模型。官方执行文件：仓库 `prompt_rewrite/run_transformers.py`, `run_vllm.py`, `client.py`。

编辑场景所说的“提高分辨率/4K”是效果目标，不可承诺潜变量工作流必然输出真 4K；应执行图像尺寸和文件 alpha 校验。


## 2.5. ControlNet Union + 参考图编辑规则（v3 新增）

当任务同时包含 **结构控制** 与 **内容参考** 时，必须区分各输入职责，不得把所有图像都视为同一种 conditioning：

- `control_image`：只负责结构、姿态、轮廓、深度、透视或建筑线条。
- `reference_image`：主参考图，通常负责主体身份、原图画幅与主要保真目标。
- `reference_image_2` / `reference_image_3`：次参考图，负责服装、第二人物、场景、材质或风格来源。
- `inpaint_image + mask`：局部编辑时指定可修改区域；白色/选中区域为编辑区。

### 2.5.1 连线与 latent 规则

1. 图像编辑路线必须使用 **参考图编码节点** 产出的 latent 接 sampler；不要为了凑尺寸私接无关的 `Empty Latent`。
2. 控制图尺寸应尽量与目标画布比例一致；若控制图被拉伸，最终构图与姿态会偏移。
3. 结构控制不保证精确的人脸或服装复制；主体身份、服装、商品、场景语义应由参考图与提示词共同约束。
4. 如果同一流程有 Base 与 Turbo LoRA 两条采样路线，两路应共用相同的参考图、控制图、提示词与种子，只比较模型/采样差异。

### 2.5.2 AIO 预处理器规则

`AIO Aux Preprocessor` 可作为默认快速入口，适合在 Skill 中统一切换以下模式：

- `canny`
- `depth`
- `hed`
- `lineart`
- `mlsd`
- `pose`
- `scribble`
- `grayscale`（若目标实现提供）

AIO 的优点是切换方便；缺点是通常不能逐一暴露各预处理器的细阈值。若任务对线条密度、边缘阈值、建筑线提取强度或姿态细节有严格要求，应改用独立预处理节点，而不是只用 AIO。

### 2.5.3 CN + 参考图的提示词写法

- 多图编辑时，必须在提示词中明确引用 `<image1>`, `<image2>`, `<image3>`。
- 不要把 control image 当作 `<imageX>` 文本描述对象；control map 是结构条件，不是内容语义参考。
- 提示词顺序建议：
  1. 先写保留什么；
  2. 再写从哪个参考图转移什么；
  3. 再写 “follow the provided control map” 之类的结构约束；
  4. 最后写不要改动的部分。

#### 单参考图 + CN
Preserve the identity, facial features, hairstyle, body proportions, and key outfit characteristics of the reference image. Follow the provided control map for the final pose, composition, or structural layout. Keep the subject recognizable and coherent.

#### 双参考图 + CN
Use `<image1>` as the primary subject reference and preserve its identity, anatomy, and core recognizable features. Use `<image2>` as the secondary reference for the outfit, style, environment, or product context. Follow the provided control map for the final pose, composition, or structural arrangement. Transfer only the requested attributes from `<image2>` while preserving the protected features from `<image1>`.

#### 三参考图 + CN
Use `<image1>` as the primary subject reference, `<image2>` as the secondary appearance or outfit reference, and `<image3>` as the environment or style reference. Follow the provided control map for the final pose, arrangement, or scene structure. Preserve the protected identity and major visual traits from `<image1>`, transfer only the requested elements from `<image2>`, and integrate them naturally into the scene or style of `<image3>`.

#### Inpaint + CN + 参考图
Edit only the masked region of the source image while preserving all unmasked regions unchanged. Use `<image1>` as the main appearance or content reference inside the edited area, and follow the provided control map for the structural layout within the edited region. Keep the result seamlessly integrated in lighting, perspective, texture, and edge transitions.

### 2.5.4 执行边界

- 若用户只有普通照片，没有控制图，则可先通过 AIO 生成控制图，再送入 Union。
- 若用户已提供手工绘制控制图，不应再次使用 AIO 覆盖它。
- 若平台没有安装 T8 Union 节点或等效原生 Union 支持，Agent 必须明确说明“当前环境不具备该流程运行条件”。
- 若任务依赖局部重绘，必须核实真实存在 `mask` / `inpaint_image` 输入；仅凭文本提示不代表工作流具备局部编辑能力。

## 3. 工作任务调度

输入：用户需求、源图路径（若有）、参考图顺序/角色、控制图路径（若有）、mask 路径（若有）、锁定主体及不可改项、文字逐字内容、目标画幅、模型变体、ComfyUI JSON（若有）、显存/运行环境。若信息不足，优先在不改变 ID 和已有工作流的前提下做可执行默认。

流程：
1. 使用 `references/capabilities.md` 与 `references/official_sources.md` 选路由，检查 ComfyUI 节点真实能力和必需模型。
2. 用 `references/three_role_review.md` 审议真实任务；执行前形成审查决议。
3. 建立符合 `assets/task_schema_example.json` 的任务 JSON。交给 `scripts/validate_task.py` 校验；如需外部视频，交给 `scripts/video_handoff.py`。
4. T2I 提示词由创作 Agent / PE-T2I 生成，Edit 由编辑 Agent / PE-I2I 生成；**示例脚本仅负责规范、验证与交接，不会凭空分析图像或运行模型**。
5. 若对 ComfyUI JSON 注入，先打开原文件检查节点、模板、引用，再运行 `scripts/inject_comfyui.py`。仅修改明确指定的 `PrimitiveStringMultiline` 类提示词节点文本，其他端口由用户实际模板承担。**任务 JSON 内引用了2-10张图，不等于单靠这个脚本会自动接好2-10个输入端口。**
6. 执行 `scripts/audit_comfyui.py` 对照原图验证：节点/连接/模型/Seed/尺寸/采样未变；如用户允许编辑模型参数，列出例外。
7. 用户的 ComfyUI / RunningHub 环境真实推理后，评估一致性、构图、文字、遮罩、alpha、速度；没有 GPU 实测就标为 `runtime_pending`。
8. 需要视频时仅创建可执行交接清单，后续外部视频模型要单独部署、运行和验收；不能把产生分镜 JSON 冒充视频生成成功。
9. 用户要求把验证后的工作沉淀为长期 Skill 时才更新 Skill 内容，版本记录保留。

## 4. 脚本及使用

**静态演示不运行 GPU：**

```bash
python scripts/validate_task.py --task examples/multi_edit.json
python scripts/validate_task.py --task examples/t2i_poster.json
python scripts/validate_task.py --task examples/video_storyboard.json
python scripts/video_handoff.py --task examples/video_storyboard.json --output video_handoff.json
python -m unittest discover -s tests -v
```

**已确定提示词要写入 ComfyUI JSON 时：**

```bash
python scripts/inject_comfyui.py --workflow assets/reference_11groups.json --task examples/t2i_poster.json --node-title 'T2I-01｜正向提示词' --output updated.json
python scripts/audit_comfyui.py --original assets/reference_11groups.json --updated updated.json --allowed-titles 'T2I-01｜正向提示词'
```

`examples/t2i_poster.json` 的示例文本是**固定测试输入，不是独立 PE 模型推理输出**。注入脚本从 `positive_prompt` 读取内容，保留其它配置不变。指定不存在/重复节点时直接失败；严禁在未知工作流中猜节点。需要改变参考图数量、sampler、LoRA、mask 或 latent 必须进行专门节点连线改造并另行测试。

## 5. 重点产品化玩法

- 人像 IP：母图 → 保留脸型/眉眼/发丝的 1 图编辑 → 双图衣服迁移 → 多张场景复用 → 分镜 → 视频模型动效（单独路由）。
- 电商：产品原照 + 背景 + 道具多图组合 → 商标/商品几何锁定 → Hero Shot → RGBA 抠图 → 广告图 → 动态版。
- 图文海报：指定中英文逐字、分区、主次层级、背景留白 → 文字 OCR/人工核验 → 输出 16:9/3:4 两版。
- 漫剧/连续画面：角色设定/三视图 → 多图角色一致性 → 分镜板 → 外部视频镜头 → 后期拼接。
- 局部重绘：独立遮罩/标注/圈选 → 保持非目标区 → 前后相同画幅滑块对照。
- 透明图：精确提示 transparent RGBA、clean alpha → 打开 RGBA 原生路径，查 PNG alpha 与边缘溢色。
- 模型评测：Base 25步、官方 Turbo checkpoint 8步、第三方 Turbo LoRA 8步、Detail Fix LoRA 25步分别登记路线；不得合并为“一种加速”。

## 6. 验收红线

1. 原创提示词的文字、数量、品牌、角色 ID 不得静默修改；用户要求锁定已有工作流时只改获授权字段。
2. 所有对照实验写清 Base/Turbo/LoRA 具体文件及权重、seed、sampler、scheduler、CFG、steps、分辨率、推理耗时、显存和执行平台；其它差异不能被掩盖。
3. 不把 ComfyUI 节点截图或静态 JSON 当实际跑图；不把 image-to-video 提示词当视频模型真实输出。
4. 绝不覆盖用户原 JSON，生成新文件并附 diff 审计。
5. 官方性能、部署方式、模型限制以 `references/official_sources.md` 最新查询为准；不确定的第三方节点能力先确认。
