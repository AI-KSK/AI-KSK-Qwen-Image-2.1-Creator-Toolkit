# 上游来源与技术对照 / Technical sources

| 组件 | 原始项目 | 此仓库使用情况 |
| --- | --- | --- |
| Qwen Image 2.1 Base | <https://huggingface.co/Qwen/Qwen-Image-2.1> | 通过 ComfyUI 外部加载；**不分发模型** |
| Comfy-Org Qwen 2.1 权重 | <https://huggingface.co/Comfy-Org/Qwen-Image-2.1> | 兼容文件名与目录参考 |
| T8 Qwen2.1 Fun Union 节点 | <https://github.com/T8mars/Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8> | Skill 的 CN 路线引用其节点类型：`QwenImage21UnionLoader`、`QwenImage21UnionApply`、`QwenImage21UnionLatentFromImage`；本仓库**不复制其 Python 源码** |
| T8 原作者 Depth 示例工作流 | <https://github.com/T8mars/Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8/blob/main/workflows/qwen21_union_depth.json> | 仅作为节点类型、输入输出与 widgets 顺序的参考来源 |
| Union 转换权重 | <https://huggingface.co/t8star/Qwen-Image-2.1-Fun-Controlnet-Union-Comfy> | 仅提供下载地址，**不附带权重** |
| 原 Union 模型 | <https://huggingface.co/alibaba-pai/Qwen-Image-2.1-Fun-Controlnet-Union> | 上游模型、许可来源 |
| ComfyUI | <https://github.com/comfyanonymous/ComfyUI> | 执行平台 |
| Aux 预处理器 | <https://github.com/Fannovel16/comfyui_controlnet_aux> | AIO Aux Preprocessor、`DepthAnythingV2Preprocessor` 等 |
| Depth Anything V2 Base | <https://huggingface.co/depth-anything/Depth-Anything-V2-Base> | `depth_anything_v2_vitb.pth` |
| ComfyUI 官方工作流模板 | <https://github.com/Comfy-Org/workflow_templates> | `skills/qwen-image-2-1-creator/assets/reference_11groups.json` **派生自该模板**（MIT，Copyright (c) 2023-present Comfy Org）；保留其 `properties.models` 模型下载元数据与 `cnr_id` 注册表元数据，上游署名与许可全文见 [`../NOTICE`](../NOTICE) |
| rgthree ComfyUI 扩展 | <https://github.com/rgthree/rgthree-comfy> | 工作流中引用其 `Image Comparer (rgthree)` 节点类型；**不复制其代码** |
| Wan 视频生成 | <https://github.com/Wan-Video/Wan2.2> | Skill 的 `video_*` 路由**只生成交接单**，由该外部模型实际执行 |

本仓库**未捆绑**以上项目的 Python 节点实现、模型权重或上游示例图片与工作流文件；如果用户另行下载它们，其授权完全受上游条款约束。

Skill 内置脚本属于**离线结构检查与文本规范工具**，不调用任何模型推理 API，也不包含上游代码的复制品。
