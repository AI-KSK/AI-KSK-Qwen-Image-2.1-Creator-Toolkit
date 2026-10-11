# AI-KSK · Qwen Image 2.1 Creator Skill

**版本 3.0.0** ｜ [English README](README_EN.md)

> 本仓库是一个**技能包（Skill）仓库**，核心内容只有一项：`skills/qwen-image-2-1-creator/`。
> 仓库**不包含**模型权重、生成图片或视频、GPU 实测结果，也不需要 GPU 即可完成安装与静态校验。

---

## 1. 项目简介

**AI-KSK Qwen Image 2.1 Creator Skill** 面向 Codex 等兼容 Skill 机制的 Agent 环境，把 Qwen Image 2.1 的创作流程与 ComfyUI 工程流程固化为一份**可复用的执行协议**，并附带只用 Python 标准库即可运行的校验脚本、示例任务与参考资料。

**它解决什么问题**

- 让 Agent 按固定规范产出 Qwen Image 2.1 的提示词与任务 JSON，而不是每次临时发挥。
- 让 ComfyUI 工作流的提示词注入与改动审计有据可查（改了什么、没改什么）。
- 让"结构控制（ControlNet Union）"与"内容参考（reference image）"的职责不被混为一谈。
- 让需要交给外部视频模型的任务产出可执行的交接单，而不是把分镜 JSON 谎报成视频。

**适用场景**

| 场景 | 说明 |
| --- | --- |
| 提示词工程 | 按官方 PE-T2I / PE-I2I 规范起草、校对 T2I 与编辑指令 |
| 图像创作与编辑 | 文生图、单图/多图编辑、局部重绘、透明图、扩图、文字海报、主体一致性、分镜 |
| ComfyUI 工程 | 任务 JSON 校验、指定提示词节点注入、工作流 diff 审计 |
| 结构化控制 | ControlNet Union + AIO 预处理路线的规则与提示词模板 |
| 视频接力 | 为 Wan / H3 等**外部**视频模型准备图生视频、文生视频交接单 |

**这不是什么**

- 不是模型，不是权重包，不是推理服务，不是 Web 界面。
- 不是 GPU 性能测试项目；仓库内没有任何实测出图或耗时数据。

---

## 2. 技能能力

任务路由与产物（完整矩阵见 [`references/capabilities.md`](skills/qwen-image-2-1-creator/references/capabilities.md)）：

| 路由 | 输入 | 产物 | 说明 |
| --- | --- | --- | --- |
| `t2i` | 无参考图 | 提示词 + `wh_ratio` + 图 | 英文成片观察式描述 |
| `single_edit` | 1 张图 | 编辑指令 + 图 | 动作式修改说明 |
| `multi_edit` | 2–10 张图 | 指令 + 图 | 必须用 `<image1>`…`<imageN>` 明确角色 |
| `local_edit` | 1 张图 + 遮罩 | 图 | 需真实存在 mask / inpaint 输入 |
| `transparent` | 0 或 1–10 张图 | RGBA PNG | 必须保留 alpha，禁用 JPEG |
| `outpaint` | 1 张图 | 图 | 明确扩展边与目标画幅 |
| `typography` | 0 或 1+ 张图 | 图 | 逐字锁定文字并人工核验 |
| `identity` | 1–10 张图 | 图 | 人物/服装/商品一致性与场景变体 |
| `storyboard` | 0 或 1–10 张图 | 图 | 静态多格分镜，非视频 |
| `benchmark` | 0–10 张图 | JSON | Skill 编排的参数/质量审计 |
| CN 变体：`cn_t2i` / `cn_single_ref` / `cn_multi_ref` / `cn_inpaint_ref` | 参考图 + 控制图（+ mask） | 图 | 通过现有 mode 追加 `control_image` 字段表达；**没有独立的 `cn_*` 校验模式** |
| `video_t2v` / `video_i2v` / `video_storyboard` | 0 或 1+ 张图 | **交接 JSON** | 由外部视频模型执行 |

**明确的能力限制（请勿夸大）**

- Qwen Image 2.1 是**图像**生成/编辑模型，**不原生生成视频**；`video_*` 路由只产出交接单。
- 内置 Python 工具**只做**输入规范检查、指定节点提示词写入、工作流 diff 审计、视频交接单生成；**不会**下载模型、执行 PE-VLM 推理、部署节点、自动接通 2–10 个图像端口或生成图片。
- 官方"支持 1–10 张参考图"是**模型能力**，不代表你手上的 ComfyUI 工作流真的暴露了 1–10 个图像输入端口；必须以实际节点为准。
- ControlNet Union 路线需要真实安装 T8 Union 节点；环境不具备时 Skill 应直接说明无法运行，而不是绕过。
- 未在真实 GPU 环境验证过的内容，一律标注为 `runtime_pending`，不会写成"已实测"。

---

## 3. 安装方法

**安装源就是本仓库的 `skills/qwen-image-2-1-creator/` 目录，没有另行发布的 ZIP 包。**
安装 = 把该子目录复制到 Codex 的 skills 目录下，**不要**把整个仓库当作一个 Skill 复制进去。

### Windows PowerShell

```powershell
git clone https://github.com/AI-KSK/AI-KSK-Qwen-Image-2.1-Creator-Toolkit.git
Set-Location AI-KSK-Qwen-Image-2.1-Creator-Toolkit

$src  = Join-Path (Get-Location) 'skills\qwen-image-2-1-creator'
$dest = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $env:USERPROFILE '.codex\skills' }

New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Recurse -Force $src (Join-Path $dest 'qwen-image-2-1-creator')

# 确认安装结果：应能看到 SKILL.md
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

# 确认安装结果：应能看到 SKILL.md
ls "$dest/qwen-image-2-1-creator"
```

**安装要点**

- 目标目录名必须保持 `qwen-image-2-1-creator`，与 `SKILL.md` frontmatter 中的 `name` 一致。
- 旧版技能目录（如 `qwen-image-2-1-t2i-creator`）不会被自动删除；如需替换请自行停用或移出。
- 安装 Skill 只需要 **Python 3.10+**，不需要 GPU、不需要模型权重、不需要联网。
- 可选的 ComfyUI / Union 节点 / 模型安装见 [`docs/INSTALL_CN.md`](docs/INSTALL_CN.md)。

---

## 4. 如何调用

### 在 Codex 中调用

```
$qwen-image-2-1-creator 按 A 提示词 / B 工作流工程 / C 质量验收三角色交叉讨论，制作 Qwen Image 2.1 双图换装工作流：图1人物、图2服装；严格保持人物 ID，完成后检查每一个输入端口和 PreviewImage。
```

```
$qwen-image-2-1-creator 根据这张角色三视图建立连续四镜头分镜，并输出给 Wan2.2 的图生视频任务交接单；不要宣称 Qwen 本身能生成视频。
```

```
$qwen-image-2-1-creator 用 ControlNet Union 做结构控制：这张照片是参考主体，这张线稿是 control image。只改姿态，不改身份和服装，并按 cn_single_ref 规则写提示词。
```

### 本地静态验证（不需要 GPU）

命令需要**在技能目录内**执行（示例路径相对于该目录）：

```bash
cd skills/qwen-image-2-1-creator

python scripts/validate_task.py --task examples/multi_edit.json
python scripts/validate_task.py --task examples/t2i_poster.json
python scripts/validate_task.py --task examples/video_storyboard.json
python scripts/video_handoff.py  --task examples/video_storyboard.json --output video_handoff.json
python -m unittest discover -s tests -v
```

工作流注入与审计：

```bash
python scripts/inject_comfyui.py --workflow assets/reference_11groups.json \
    --task examples/t2i_poster.json --node-title 'T2I-01｜正向提示词' --output updated.json
python scripts/audit_comfyui.py --original assets/reference_11groups.json \
    --updated updated.json --allowed-titles 'T2I-01｜正向提示词'
```

注入脚本只会改写明确指定的提示词节点文本，**绝不覆盖原工作流**；节点不存在或标题重复时直接失败，不会猜测节点。

---

## 5. 文件结构

```text
AI-KSK-Qwen-Image-2.1-Creator-Toolkit/
├── README.md / README_EN.md        # 中英文入口
├── LICENSE / NOTICE                # 许可与版权边界
├── LICENSE-DECISION.md             # 许可证决策记录
├── CHANGELOG.md / CONTRIBUTING.md / SECURITY.md
├── docs/                           # 环境依赖、排障、FAQ、上游来源、授权说明
├── examples/REPRO_LOG_TEMPLATE.csv # 复现记录表模板
├── skills/qwen-image-2-1-creator/  # ★ Skill 本体
└── .github/                        # CI 与 Issue / PR 模板
```

### Skill 目录职责

| 路径 | 职责 |
| --- | --- |
| `SKILL.md` | 技能主协议：执行顺序、任务路由、PE 提示词规范、ControlNet Union 规则、工作流调度、验收红线。**使用者与 Agent 的首要阅读对象。** |
| `README.md` | 技能的简短说明与调用示例。 |
| `references/` | 参考资料：能力矩阵、官方来源、三角色评审、PE 推理边界、CN 与参考图规则、视频接力、质量评分标准。 |
| `examples/` | 可直接用 `scripts/validate_task.py` 校验的示例任务 JSON，覆盖 T2I、编辑、局部编辑、透明图、扩图、文字、一致性、分镜、视频交接与 CN 路线。 |
| `scripts/` | Python 标准库脚本：任务校验、ComfyUI 提示词注入、工作流 diff 审计、视频交接单生成。 |
| `tests/` | 技能单元测试，校验路由规则与示例一致性。 |
| `assets/` | 任务 JSON schema 示例、历史提示词参考、11 组 A/B ComfyUI 模板起点。 |

---

## 6. 环境与模型依赖

| 任务类型 | 需要的环境 | 是否需要 GPU |
| --- | --- | --- |
| 安装 Skill、阅读文档 | 无（仅文件复制） | 否 |
| 任务 JSON 校验、示例检查、单元测试 | Python 3.10+ 标准库 | 否 |
| 视频交接单生成 | Python 3.10+ 标准库 | 否 |
| ComfyUI 工作流注入与 diff 审计 | Python 3.10+ 标准库 + 你的工作流 JSON | 否 |
| 真实文生图 / 图像编辑 / ControlNet Union | ComfyUI（含 Qwen Image 2.1 支持）+ 模型权重，或 RunningHub 等平台 | **是** |
| PE-T2I / PE-I2I 提示词模型推理 | 单独部署的官方 PE 权重或服务 | 取决于部署 |
| 图生视频 / 文生视频 | **外部**视频模型（如 Wan / H3），需独立部署 | **是** |

**模型与节点的具体下载地址、文件名与放置目录**见 [`docs/INSTALL_CN.md`](docs/INSTALL_CN.md)；上游来源对照见 [`docs/TECHNICAL_SOURCES.md`](docs/TECHNICAL_SOURCES.md)。

---

## 7. 版权与许可证

**本仓库原创内容**采用 **Apache-2.0**（维护者已于 2026-10-11 确认授权）。条款见 [`LICENSE`](LICENSE)；**覆盖范围与非覆盖清单以 [`NOTICE`](NOTICE) 为准**；决策与确认过程见 [`LICENSE-DECISION.md`](LICENSE-DECISION.md)。

**该许可不覆盖以下第三方内容**，它们各自适用上游条款：

- **模型权重**：Qwen Image 2.1 系列权重不随本仓库分发。
- **T8 Qwen Image 2.1 Fun ControlNet Union**：自定义节点代码与转换权重各有独立许可；转换权重受研究/非商业使用限制，**公开本仓库不会解除该限制**。
- **comfyui_controlnet_aux / Depth Anything V2** 等第三方节点与预处理器。
- **ComfyUI 官方工作流模板材料（MIT，Copyright (c) 2023-present Comfy Org）**：`skills/qwen-image-2-1-creator/assets/reference_11groups.json` 派生自 ComfyUI 官方模板，保留了其模型下载与注册表元数据；上游 MIT 署名与许可全文已按 MIT 要求完整收录于 [`NOTICE`](NOTICE)，该材料**不在**本仓库的 Apache-2.0 授权范围内。
- **第三方素材**：本仓库不包含任何人物肖像、插画、截图或他人版权图片。

**本仓库不包含**：模型权重、API 密钥、Cookie、签名链接、RunningHub 账户配置、私人测试图或 GPU 输出。

商业使用前请自行核对各上游许可证原文；本节与 `NOTICE` 均不构成法律意见。详细分层说明见 [`docs/LICENSES_AND_ATTRIBUTION_CN.md`](docs/LICENSES_AND_ATTRIBUTION_CN.md)。

---

## 8. 作者与项目地址

- **维护者**：AI-KSK
- **项目主页**：<https://github.com/AI-KSK/AI-KSK-Qwen-Image-2.1-Creator-Toolkit>
- **Skill 目录**：[`skills/qwen-image-2-1-creator/`](skills/qwen-image-2-1-creator/)
- **问题反馈**：请按 [Issue 模板](.github/ISSUE_TEMPLATE/bug_report.md) 提交；提交日志前请移除 token、cookie、签名链接与个人身份信息，参见 [`SECURITY.md`](SECURITY.md)。

欢迎 Fork 并在原有结构上继续开发；贡献前请阅读 [`CONTRIBUTING.md`](CONTRIBUTING.md)。
