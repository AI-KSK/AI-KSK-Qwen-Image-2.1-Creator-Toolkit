# 贡献说明 / Contributing

欢迎提交复现报告、节点版本适配、文档修正、测试工具和具备合法授权的样本。请勿提交第三方模型权重、无授权肖像/插画、API 密钥或包含签名链接的日志。

## 提交前

1. 在 issue 里说明目的（错误、兼容版本、性能、对照实验）。
2. 复现报告请写清 Base / Turbo / LoRA 的具体文件与权重、seed、sampler、scheduler、CFG、steps、分辨率与执行平台；不要在“修正 bug”时顺带改动这些变量。
3. 在技能目录内执行静态检查与单元测试：

   ```bash
   cd skills/qwen-image-2-1-creator
   python scripts/validate_task.py --task examples/multi_edit.json
   python -m unittest discover -s tests -v
   ```
4. 对每份改动说明“静态检查”还是“实际 GPU 运行已验证”；不能混用。
5. PR 包含变更概述、受影响节点 ID、复现步骤、插件版本及授权信息。

**许可证状态：** AI-KSK 原创部分已选定 **Apache-2.0**（见 [`LICENSE`](LICENSE) 与 [`NOTICE`](NOTICE)）。除非在提交时另有明确声明，贡献按 Apache-2.0 第 5 条以同一许可授权。任何 PR 合并前应确认贡献者拥有版权，且提交内容不含第三方模型权重、无授权素材或凭据。
