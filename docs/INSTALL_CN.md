# 安装指南｜ComfyUI / RunningHub / 模型下载

本仓库只含 **工作流 JSON、Codex Skill、文档、Python 标准库校验脚本**；不含权重文件、商业 API 密钥、RunningHub 账户配置或测试原图。

## 环境前提

- ComfyUI：T8 Union 插件建议 **0.37.0 或更新**，含原生 Qwen Image 2.1 支持；RunningHub 是否具备相同节点要按实际环境核查。
- Python：工作流由 ComfyUI 自己的 Python 环境运行；`scripts/` 目录中的静态校验只需要 Python 3.10+。
- 显存：无统一保证。75 张图不是一次大 batch，而是 75 路独立采样与解码，GPU 运算时间可能很长。

## 扩展安装

推荐在 **ComfyUI Manager** 搜索和安装：

1. `Qwen Image 2.1 Fun ControlNet Union (T8)`：<https://github.com/T8mars/Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8>
2. `comfyui_controlnet_aux`：<https://github.com/Fannovel16/comfyui_controlnet_aux>

如果选择 Git 克隆，在 ComfyUI 的 `custom_nodes/` 下执行：

```bash
git clone https://github.com/T8mars/Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8.git
git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git
```

注意：以上命令需在 `ComfyUI/custom_nodes/` 目录执行，依赖和环境按照各插件自己的 README 安装。重启 ComfyUI。

## 下载模型及放置目录

| 组件 | 当前 JSON 里预设文件名（本地文件名可更改） | 目录 | 参考来源 |
| --- | --- | --- | --- |
| 基础扩散模型 | `Qwen-Image_2.1.safetensors` | `ComfyUI/models/diffusion_models/` | [Comfy-Org Qwen Image 2.1](https://huggingface.co/Comfy-Org/Qwen-Image-2.1) |
| Qwen3-VL 文本编码器 | `qwen3vl_8b_int8_convrot.safetensors` | `ComfyUI/models/text_encoders/` | [Comfy-Org Qwen Image 2.1](https://huggingface.co/Comfy-Org/Qwen-Image-2.1) |
| 图像 VAE | `qwen_image_2.1_vae_bf16.safetensors` | `ComfyUI/models/vae/` | [Comfy-Org Qwen Image 2.1](https://huggingface.co/Comfy-Org/Qwen-Image-2.1) |
| Union 控制权重 | `Qwen-Image-2.1-Fun-Controlnet-Union-ComfyUI.safetensors` | `ComfyUI/models/controlnet/` | [t8star Union weights](https://huggingface.co/t8star/Qwen-Image-2.1-Fun-Controlnet-Union-Comfy) |
| Depth Anything V2 Base | `depth_anything_v2_vitb.pth` | 由 `comfyui_controlnet_aux` 安装/自动缓存目录决定 | [Depth Anything V2 Base](https://huggingface.co/depth-anything/Depth-Anything-V2-Base) |

**重要：** 官方 T8 样例的扩散模型文件名是 `qwen_image_2.1_int8_convrot.safetensors`，但本仓库沿用了用户原始工作流中 `Qwen-Image_2.1.safetensors` 的名称。**这是本地文件名差异，不是同一权重文件的证明。** 必须检查你装的权重是否兼容当前节点与 Union patch，不要仅靠重命名强行匹配。以插件作者列出的兼容模型为优先验收组合。

## 第一次运行（建议从 5 格版开始）

1. 重启 ComfyUI，确认所有节点已经存在。
2. 把 `workflows/depth75/01_first_row_5_previews.json` 拖到画布。
3. 左侧 `INPUT｜上传原图` 的 `LoadImage` 手动选择一张你的本地图（原始测试文件名仅为模板遗留值）。
4. 检查 DepthAnythingV2Preprocessor 的 `depth_anything_v2_vitb.pth` 是否存在；如预处理失败可使用 `03_manual_depth_first_row_5.json`。
5. 检查四个模型加载节点文件名，尤其 Union Loader 的 checkpoint。
6. 修改提示词使其与输入图相符。若保持动画插画的原画风，提示词必须明确指定原画风；仅用 Depth 不能锁死画风。
7. 先跑 5 格 + baseline，检查视觉差异与模型日志。
8. 通过后再使用 `02_all_75_previews.json`，建议先分批启用以控制耗时。

## 关于 RunningHub

平台需**实际安装且支持所有自定义节点**才能运行。即使工作流 JSON 可导入，也不代表云端已经有所有权重或允许安装扩展。请核对本地安装和平台镜像各自的模型目录；**不要强行套用另一台机器的模型文件名**。
