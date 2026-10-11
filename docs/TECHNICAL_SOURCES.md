# 上游来源与技术对照 / Technical sources

| 组件 | 原始项目 | 此仓库使用情况 |
| --- | --- | --- |
| Qwen Image 2.1 Base | <https://huggingface.co/Qwen/Qwen-Image-2.1> | 通过 ComfyUI 外部加载；不分发模型 |
| Comfy-Org Qwen 2.1 权重 | <https://huggingface.co/Comfy-Org/Qwen-Image-2.1> | 兼容文件名和目录参考 |
| T8 Qwen2.1 Fun Union nodes | <https://github.com/T8mars/Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8> | 75 格工作流使用 `QwenImage21UnionLoader`、`QwenImage21UnionApply`、`QwenImage21UnionLatentFromImage` |
| T8 原作者单组 Depth 示例 | <https://github.com/T8mars/Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8/blob/main/workflows/qwen21_union_depth.json> | 参考节点类型、输入输出、widgets 顺序；本仓库矩阵为另行组合 |
| Union 转换权重 | <https://huggingface.co/t8star/Qwen-Image-2.1-Fun-Controlnet-Union-Comfy> | 仅提供下载地址，不附带权重 |
| 原 Union 模型 | <https://huggingface.co/alibaba-pai/Qwen-Image-2.1-Fun-Controlnet-Union> | 上游模型、许可来源 |
| ComfyUI | <https://github.com/comfyanonymous/ComfyUI> | 执行平台 |
| Aux 预处理器 | <https://github.com/Fannovel16/comfyui_controlnet_aux> | `DepthAnythingV2Preprocessor` |
| Depth Anything V2 Base | <https://huggingface.co/depth-anything/Depth-Anything-V2-Base> | `depth_anything_v2_vitb.pth` |

本仓库**未捆绑**以上项目的 Python 节点实现、模型权重或上游示例图片；如果用户另行下载它们，其授权完全受上游条款约束。验证脚本属于离线结构检查，不调用任何模型推理 API。
