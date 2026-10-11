# 官方 PE 模型调用（需要单独部署，不由静态脚本代替）

核心仓库：https://github.com/QwenLM/Qwen-Image-2.1/tree/main/prompt_rewrite

官方有两个同架构但权重和 system prompt 不同的检查点：

- T2I：`Qwen/Qwen-Image-2.1-PE-T2I`
- Editing：`Qwen/Qwen-Image-2.1-PE-I2I`

离线单任务，官方 `run_transformers.py`：

```bash
python run_transformers.py --task t2i --ckpt Qwen/Qwen-Image-2.1-PE-T2I --input data/t2i_example.jsonl --output out_t2i.jsonl
python run_transformers.py --task edit --ckpt Qwen/Qwen-Image-2.1-PE-I2I --input data/edit_example.jsonl --output out_edit.jsonl
```

大规模批处理可用 `run_vllm.py`；服务器可用 `serve.sh + client.py`。不同框架的 transformers/vLLM 版本、显存、端口和 checkpoint 必须分别验收。

输入：T2I 每条只有 `prompt` 不带图片；Edit 每条有 `prompt` 和 `input_images`，图片顺序决定 `<image1>`、`<image2>`。输出提取 `positive_prompt` 或 `rewritten_prompt`、`wh_ratio`、`ratio_follow`，保持原样再交给 Qwen Image 2.1 生成模型。注意：`wh_ratio` 需要转为实际尺寸/latent，`ratio_follow` 需要下游 workflow 真正实现比例继承。

把通用 Qwen3VL 编码器接上 TextGenerate 不代表调用了 PE-I2I checkpoint。此技能不宣称默认已安装 PE 权重。
