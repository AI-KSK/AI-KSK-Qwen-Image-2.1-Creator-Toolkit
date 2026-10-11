# 常见问题与排查

本页只保留与 Skill 及其 ControlNet Union 路线相关的问题。**模型权重、节点与上游工作流的问题由各自上游项目负责。**

## 1. `QwenImage21UnionApply` / `QwenImage21UnionLoader` 缺失

安装 T8 插件并重启 ComfyUI；确认版本包含上述具体节点类型。不要用其它厂商的旧 Qwen ControlNet 节点强接。

## 2. Union checkpoint 不在下拉菜单 / 模型无效

T8 Union Loader 只接受约定前缀的 `Qwen-Image-2.1-Fun-Controlnet-Union*.safetensors`，并会校验 block 数、形状与权重结构。请放入 `models/controlnet/`；**不要把 `.safetensors` 改名当作修复手段**。

## 3. `DepthAnythingV2Preprocessor` missing

安装 `comfyui_controlnet_aux`，确认 Depth Anything V2 Base 可用；或改为自行提供一张已经预处理好的深度图作为 `control_image`。

## 4. Loader 节点显示"文件名不存在"

工作流里保留的文件名来自作者本地环境，与你下载的权重文件名未必一致。打开节点下拉框，**选择真实存在且架构兼容的权重**。

## 5. 输入图打不开

`assets/reference_11groups.json` 里 `LoadImage` 的文件名来自作者本地环境；示例任务 JSON 里则是 `images/...` 一类的占位路径。**两者都不随仓库提供**，请手动上传或选择一张你有权使用的图片。

## 6. 一直没有图像输出 / Bypass 下游失效

检查当前启用的 `PreviewImage`、Sampler、Decode、Union Apply 是否处于同一条有效执行链。Bypass 不等于性能优化保证，其传播行为在不同节点框架中可能不同。

## 7. Turbo 8 步与 `Euler + simple` 混淆

官方 Turbo checkpoint 使用**自带的 sigma 时间表**，不能不加区分地套用 `Euler + simple` 的任意 8 步设置。第三方 Turbo LoRA + Base 是**另一条独立路线**，必须单独标记，不能表述成官方 Turbo。

## 8. 多参考图：官方支持 10 张，但工作流只有 2 个输入口

官方 1–10 张是**模型能力**，不等于你的 ComfyUI 工作流暴露了 1–10 个图像输入端口。请核对目标节点实际存在的 `images.image_1 ... images.image_10`。**增加端口属于节点连线改造，需要另行测试**，不能用提示词替代。

## 9. 结构控制没有锁住画风

`control_image` 只负责几何、姿态、轮廓、深度等结构信息，**不负责身份、服装和画风**。要锁定主体或画风，应由 `reference_image` 与提示词共同约束；这属于 CN + 参考图的组合路线，而不是纯结构控制。

## 10. 局部编辑没有生效

仅写出"只改某区域"的提示词**不等于**工作流具备局部编辑能力。必须核实真实存在 `inpaint_image` / `mask` 输入，并确认白色（选中）区域语义与你的预期一致。

## 11. PE 提示词看起来"没有真正跑过模型"

本 Skill 不附带 PE 权重。没有部署 PE-T2I / PE-I2I 时，Agent 只能按官方公开规范起草与校对提示词，此时**不得宣称执行了 PE 模型推理**。

## 12. RunningHub 无法安装插件

取决于平台镜像权限与已有模型。JSON 语法正确并不能保证云端提供 T8 Union、DepthAnythingV2 或所需权重。

## 13. 提交日志前的安全检查

提交报错前请去掉：`Rh-Comfy-Auth`、cookie、token、`cos_url` 签名查询、私有 IP、账户信息、授权付费图片链接。不要上传 `.env`、权重或含私有凭据的原工作流。
