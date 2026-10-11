# 授权、依赖与署名

本页说明四层不同的授权关系。核对日期：2026-10-11（上游条款可能随时更新，请以原始链接为准）。

## 四个不同法律层次

1. **本仓库原创资料**：AI-KSK 制作的 Skill 文档、参考资料、示例任务、原创辅助脚本、CI 与配置文件；采用 **Apache-2.0**，条款见 [`../LICENSE`](../LICENSE)，覆盖范围与署名见 [`../NOTICE`](../NOTICE)。该许可**不覆盖**下述第 2、3、4 层。决策记录见 [`../LICENSE-DECISION.md`](../LICENSE-DECISION.md)。

2. **第三方节点代码**：T8 Qwen Image 2.1 Fun Union 插件有独立代码许可，其 README 载明原始适配代码为 MIT、打包分发的 ComfyUI Union 兼容件为 GPL-3.0（**以分发件整体为准时为 GPL-3.0**）；我们**只链接安装，不复制其 Python 源码**。`comfyui_controlnet_aux` 由其上游许可证管理。本仓库 JSON 中出现节点类型名称，不代表对这些项目的再授权。

3. **模型权重**：Qwen Image 2.1 Fun Union 受 **Qwen Research License** 限制，上游模型卡说明**仅非商业研究与评估**，商业用途需另外获得合法许可。公开 GitHub 仓库不能自动取消该限制。本仓库**没有捆绑模型权重**。

4. **ComfyUI 官方工作流模板材料（MIT）**：`skills/qwen-image-2-1-creator/assets/reference_11groups.json` 派生自 ComfyUI / Comfy-Org 官方工作流模板，并保留了模板自带的 `properties.models` 模型下载元数据与 `cnr_id` 注册表元数据。上游项目 <https://github.com/Comfy-Org/workflow_templates>，其 MIT 许可全文与 `Copyright (c) 2023-present Comfy Org` 署名已按 MIT 要求完整收录于 [`../NOTICE`](../NOTICE)。该上游材料**不在**本仓库 Apache-2.0 授权范围内；AI-KSK 仅主张其修改与新增部分的著作权。JSON 中残留的第三方扩展标识与节点名称（如 `cnr_id`、扩展节点类型）仅为兼容你本地环境而保留。

## 必须注意的文件版权

- 外部提供的二次元原图 / 绘画参考：**不收录**。上传到公开仓库前必须确认版权所有者同意。
- 部署镜像、节点及模型打包：必须分别核对对应许可证，不能仅根据仓库 README 推断所有依赖均可商业使用。
- 任何复用或分发第三方模型权重的行为，遵循其原始协议与必要署名要求。
- 不得移除 `NOTICE` 中的上游署名，否则会违反 MIT 的署名保留要求。
- 本项目不声称与 Qwen、ComfyUI、Comfy Org、T8 或 RunningHub 存在官方从属关系。

## 外部条款入口（请以最新原始协议为准）

- Qwen Image 2.1 Base：<https://huggingface.co/Qwen/Qwen-Image-2.1>
- Union 源模型：<https://huggingface.co/alibaba-pai/Qwen-Image-2.1-Fun-Controlnet-Union>
- T8 改造的 Union 权重：<https://huggingface.co/t8star/Qwen-Image-2.1-Fun-Controlnet-Union-Comfy>
- T8 代码、许可证和修改声明：<https://github.com/T8mars/Comfyui-Qwen-Image-2.1-Fun-Controlnet-Union-T8>
- ComfyUI：<https://github.com/comfyanonymous/ComfyUI>
- ControlNet Aux：<https://github.com/Fannovel16/comfyui_controlnet_aux>
- ComfyUI 官方工作流模板（MIT）：<https://github.com/Comfy-Org/workflow_templates>
- Comfy-Org Qwen 权重：<https://huggingface.co/Comfy-Org/Qwen-Image-2.1>

**说明：** 以上信息来自作者模型卡 / 仓库说明，不构成法律意见。商用前请咨询版权持有人或法律专业人士。
