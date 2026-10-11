# 环境与依赖安装｜Codex / ComfyUI / 模型

本文件说明两件事：**Skill 装到哪里**，以及**要让 Skill 的 ComfyUI 路线真正跑起来需要装什么**。

本仓库只含 **Codex Skill、文档、示例任务 JSON、Python 标准库校验脚本**；不含权重文件、商业 API 密钥、RunningHub 账户配置或测试原图。

---

## 1. 安装 Skill（Codex 等兼容环境）

安装源就是仓库里的 `skills/qwen-image-2-1-creator/` 目录，**没有另行发布的 ZIP 包**。完整命令见根目录 [`README.md`](../README.md#3-安装方法)，要点：

- 把 `skills/qwen-image-2-1-creator/` 复制到 `$CODEX_HOME/skills/`（未设置时用 `~/.codex/skills/`）。
- 目标目录名保持 `qwen-image-2-1-creator`。
- 只复制该子目录，不要把整个仓库当作一个 Skill。
- 这一步**不需要** GPU、模型权重或联网。

---

## 2. ComfyUI 与扩展节点

只在你要真正出图时才需要本节内容。

- ComfyUI：建议 **0.37.0 或更新**，需包含原生 Qwen Image 2.1 支持。RunningHub 等平台是否具备相同节点，必须按实际环境核查。
- Python：ComfyUI 使用自己的 Python 环境；仓库内 `skills/qwen-image-2-1-creator/scripts/` 的静态校验只需要 Python 3.10+。

推荐在 **ComfyUI Manager** 搜索安装以下扩展：

1. `Qwen Image 2.1 Fun ControlNet Union (T8)`：<https://github.com/T8mars/Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8>
2. `comfyui_controlnet_aux`：<https://github.com/Fannovel16/comfyui_controlnet_aux>

如需 Git 克隆，请在 ComfyUI 的 `custom_nodes/` 目录下执行：

```bash
git clone https://github.com/T8mars/Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8.git
git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git
```

依赖按各插件自己的 README 安装，装完**重启 ComfyUI**。

ControlNet Union 路线依赖的节点类型：`QwenImage21UnionLoader`、`QwenImage21UnionApply`、`QwenImage21UnionLatentFromImage`。若环境中不存在这些节点，Skill 会（也应当）直接说明当前环境不具备该流程运行条件。

---

## 3. 模型下载与放置目录

| 组件 | 示例文件名（本地文件名可不同） | 目录 | 参考来源 |
| --- | --- | --- | --- |
| 基础扩散模型 | `Qwen-Image_2.1.safetensors` | `ComfyUI/models/diffusion_models/` | [Comfy-Org Qwen Image 2.1](https://huggingface.co/Comfy-Org/Qwen-Image-2.1) |
| Qwen3-VL 文本编码器 | `qwen3vl_8b_int8_convrot.safetensors` | `ComfyUI/models/text_encoders/` | [Comfy-Org Qwen Image 2.1](https://huggingface.co/Comfy-Org/Qwen-Image-2.1) |
| 图像 VAE | `qwen_image_2.1_vae_bf16.safetensors` | `ComfyUI/models/vae/` | [Comfy-Org Qwen Image 2.1](https://huggingface.co/Comfy-Org/Qwen-Image-2.1) |
| Union 控制权重 | `Qwen-Image-2.1-Fun-Controlnet-Union-ComfyUI.safetensors` | `ComfyUI/models/controlnet/` | [t8star Union weights](https://huggingface.co/t8star/Qwen-Image-2.1-Fun-Controlnet-Union-Comfy) |
| Depth Anything V2 Base | `depth_anything_v2_vitb.pth` | 由 `comfyui_controlnet_aux` 决定 | [Depth Anything V2 Base](https://huggingface.co/depth-anything/Depth-Anything-V2-Base) |
| PE-T2I / PE-I2I（可选） | 官方 PE checkpoint | 按官方仓库说明部署 | [QwenLM/Qwen-Image-2.1](https://github.com/QwenLM/Qwen-Image-2.1) |
| 第三方 Turbo LoRA（**不随本仓库分发**） | `qwen_image_2.1_turbo_lora_avg_rank_178_bf16.safetensors` | `ComfyUI/models/loras/` | 无公开来源，需自备；见下方说明 |

**关于 `skills/qwen-image-2-1-creator/assets/reference_11groups.json` 里的 LoRA**

该模板含 11 个 `LoraLoaderModelOnly` 节点，全部指向第三方的 `qwen_image_2.1_turbo_lora_avg_rank_178_bf16.safetensors`。这个权重**不随本仓库分发，也没有在本文档中给出公开下载地址**。请二选一：

1. 自行获取同名 LoRA 并放入 `ComfyUI/models/loras/`；或
2. 直接删除这 11 个 LoRA 节点，改用官方 Turbo checkpoint（`Qwen/Qwen-Image-2.1-Turbo`，自带 8 步 sigma 调度）或 Base 25 步路线。

**不要**把第三方 Turbo LoRA 路线表述成官方 Turbo checkpoint，两者的采样计划不同。

**重要：** 官方 T8 样例使用的扩散模型文件名与上表可能不同。表中名称只是**示例**，不代表同一权重文件。必须确认你安装的权重与当前节点及 Union patch 兼容；**不要仅靠重命名强行匹配下拉框**。以插件作者列出的兼容组合为优先。

**这些权重都不随本仓库分发**，其授权完全受上游条款约束，见 [`LICENSES_AND_ATTRIBUTION_CN.md`](LICENSES_AND_ATTRIBUTION_CN.md)。

---

## 4. 在 ComfyUI 中接入 Skill 路线

本仓库不附带独立的实验工作流 JSON。Skill 自带的示例模板起点是：

`skills/qwen-image-2-1-creator/assets/reference_11groups.json`

接入步骤：

1. 重启 ComfyUI，确认上述节点已存在。
2. 打开该模板（或你自己的工作流），确认 `UNETLoader`、`CLIPLoader`、`VAELoader`、`QwenImage21UnionLoader` 的文件名都能从下拉框真实选中。
3. 在 `LoadImage` 中**手动选择你有权使用的本地图片**；模板里遗留的文件名来自作者本地环境，不随仓库提供。
4. 确认 ControlNet Union 路线所需的 `control_image` 与 `reference_image` 输入端口真实存在——**端口不存在就不能靠提示词绕过**。
5. 用 Skill 的注入脚本写入提示词，而不是手工替换整个 JSON：

   ```bash
   python skills/qwen-image-2-1-creator/scripts/inject_comfyui.py \
       --workflow skills/qwen-image-2-1-creator/assets/reference_11groups.json \
       --task skills/qwen-image-2-1-creator/examples/t2i_poster.json \
       --node-title 'T2I-01｜正向提示词' --output updated.json
   ```

6. 用审计脚本确认除目标节点外没有其他改动：

   ```bash
   python skills/qwen-image-2-1-creator/scripts/audit_comfyui.py \
       --original skills/qwen-image-2-1-creator/assets/reference_11groups.json \
       --updated updated.json --allowed-titles 'T2I-01｜正向提示词'
   ```

7. 真实推理后记录环境与结果；**没有实际运行过就不要标记为已实测**，按 `runtime_pending` 处理。

---

## 5. 关于 RunningHub 等云端平台

平台需**实际安装且支持所有自定义节点**才能运行。即使工作流 JSON 可以导入，也不代表云端已经具备所有权重或允许安装扩展。请分别核对本地与平台镜像的模型目录；**不要强行套用另一台机器的模型文件名**。

---

## 6. 静态校验（不需要 GPU）

```bash
cd skills/qwen-image-2-1-creator
python scripts/validate_task.py --task examples/multi_edit.json
python scripts/video_handoff.py --task examples/video_storyboard.json --output video_handoff.json
python -m unittest discover -s tests -v
```
