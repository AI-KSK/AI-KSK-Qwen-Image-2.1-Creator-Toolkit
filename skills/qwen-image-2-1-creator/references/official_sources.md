# Qwen Image 2.1 官方来源索引（核对日期：2026-10-10）

- QwenLM 官方仓库：https://github.com/QwenLM/Qwen-Image-2.1 —— 原生文生图/图像编辑、上限10张参考图、局部编辑、透明输出、Turbo 8 steps、示例 pipeline 与 ComfyUI 支持。
- 官方说明博客：https://qwen.ai/blog?id=qwen-image-2.1 —— 能力边界、图像生成与编辑及典型示例。
- PE-T2I 官方规范：https://github.com/QwenLM/Qwen-Image-2.1/blob/main/prompt_rewrite/prompts/system_prompt_t2i.txt —— 英文成片观察式、精确文字、比例元数据。
- PE-I2I 官方规范：https://github.com/QwenLM/Qwen-Image-2.1/blob/main/prompt_rewrite/prompts/system_prompt_edit.txt —— 输入参考图角色、修改/保留边界、编辑语言、多图 `<image1>` 标签、比例继承。
- PE 运行方式：https://github.com/QwenLM/Qwen-Image-2.1/tree/main/prompt_rewrite —— T2I / Edit 各自 checkpoint，Transformer/vLLM/Client。
- 官方 Turbo checkpoint：https://huggingface.co/Qwen/Qwen-Image-2.1-Turbo —— 8-step、带官方调度配置；不要与第三方 Turbo LoRA 混淆。
- Wan 视频生成仓库：https://github.com/Wan-Video/Wan2.2 —— **外部** T2V/I2V/S2V/Animate，不是 Qwen Image 2.1 自身视频能力。

**严禁**将非官方第三方推测当作模型原生能力，也严禁在没有实际 GPU/PE 权重时写“已完成推理”。


## v3 新增：ControlNet Union / AIO / 多图编辑来源

- Qwen 官方 README（Prompt Rewriting / PE-T2I / PE-I2I / 1-10 图编辑）
- alibaba-pai/Qwen-Image-2.1-Fun-Controlnet-Union（单 checkpoint 覆盖 8 种结构控制 + inpainting）
- T8mars/Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8（ComfyUI 原生 Union 节点与工作流）
- Fannovel16/comfyui_controlnet_aux（AIO Aux Preprocessor 及各类预处理器）
