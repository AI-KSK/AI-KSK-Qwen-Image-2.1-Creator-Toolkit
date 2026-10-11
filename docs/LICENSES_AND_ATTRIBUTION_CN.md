# 授权、依赖与署名（上传 GitHub 前必读）

## 三个不同法律层次

1. **本仓库原创资料**：AI-KSK 制作的 Skill 文档、原创辅助脚本、参数表与自定义工作流；权利人已选定 **Apache-2.0**，条款见 [`../LICENSE`](../LICENSE)，版权与范围说明见 [`../NOTICE`](../NOTICE)。该许可**不覆盖**下述第 2、3 层的第三方节点代码与模型权重。决策记录见 [`../LICENSE-DECISION.md`](../LICENSE-DECISION.md)。
2. **第三方节点代码**：T8 Qwen Image 2.1 Fun Union 插件有独立代码许可，README 提到 MIT 原始适配与 GPL-3.0 打包组件；我们**只链接安装，不复制其 Python 源码**。`comfyui_controlnet_aux` 由其上游许可证管理。本仓库的 JSON 使用节点名称不意味着重新授权这些项目。
3. **模型权重**：Qwen Image 2.1 Fun Union 受 **Qwen Research License** 限制，上游说明**仅非商业研究与评估**，商业用途需另外获得合法许可。公开 GitHub 仓库不能自动取消限制。本仓库**没有捆绑模型权重**。

## 必须注意的文件版权

- 外部提供的二次元原图 / 绘画参考：**不收录**。上传到公开仓库前必须确认版权所有者同意。
- 部署镜像、节点及模型打包：必须分别核对对应许可证，不能仅根据仓库 README 推断所有依赖均可商业使用。
- 任何复用或分发第三方模型权重的行为，遵循其原始协议与必要署名要求。
- 本项目不声称与 Qwen、ComfyUI、T8 或 RunningHub 存在官方从属关系。

## 外部条款入口（请以最新原始协议为准）

- Qwen Image 2.1 Base：<https://huggingface.co/Qwen/Qwen-Image-2.1>
- Union 源模型：<https://huggingface.co/alibaba-pai/Qwen-Image-2.1-Fun-Controlnet-Union>
- T8 改造的 Union 权重：<https://huggingface.co/t8star/Qwen-Image-2.1-Fun-Controlnet-Union-Comfy>
- T8 代码、许可证和修改声明：<https://github.com/T8mars/Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8>
- ComfyUI：<https://github.com/comfyanonymous/ComfyUI>
- ControlNet Aux：<https://github.com/Fannovel16/comfyui_controlnet_aux>

**说明：** 以上信息来自作者模型卡/仓库说明，不构成法律意见。商用前请咨询版权持有人或法律专业人士。
