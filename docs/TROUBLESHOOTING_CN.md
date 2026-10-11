# 常见问题与排查

## 1. KSampler 报 `cfg: Failed to convert ... FLOAT`，采样器/调度器 Value not in list

常见根因是原始工作流漏掉 `control_after_generate`，使 `widgets_values` 错位。**这次仓库附带的修正版已经是：**

```json
[9527, "fixed", 25, 3.5, "euler", "simple", 1.0]
```

不要再用旧的 `[9527,25,3.5,"euler","simple",1]`。`scripts/check_depth75.py` 会扫描所有 76 个 KSampler。

## 2. `QwenImage21UnionApply` 或 `UnionLoader` missing

安装 T8 插件并重启；版本应包含上述具体节点类型。不要用另一家旧 Qwen1.x ControlNet 节点强接。

## 3. Union checkpoint 不在下拉菜单 / 模型无效

T8 Union Loader 只接受约定前缀的 `Qwen-Image-2.1-Fun-Controlnet-Union*.safetensors`，还会验证 16-block、形状和权重结构。放在 `models/controlnet/`；不要把 `.safetensors` 粗暴改名作为修复。

## 4. `DepthAnythingV2Preprocessor` missing

安装 `comfyui_controlnet_aux`，确认 Depth Anything V2 Base 可用；或者换成 `03_manual_depth_first_row_5.json`，自己上传一张已经预处理好的深度图。

## 5. Loader 节点文件名不存在

当前 JSON 使用原用户环境文件名，与你下载的 Comfy-Org 文件名未必一致。打开节点下拉，**选真实存在且架构兼容的权重**。

## 6. 输入图打不开

`LoadImage` 默认文件名来自作者本地测试，并不随仓库提供。请手动上传 / 选择一张你有权使用的图片。

## 7. 原图画风变化

这是纯 Depth 结构横评，原图只经过深度预处理，**没有进入 `QwenImage21UnionReferenceEncode`**，所以不能用来宣称原画风保真。正向提示词可提高风格一致性，但仍不保证；若想锁画风，需要做新的 CN + 图像参考联合实验。

## 8. 一次性 75 格耗时过长或显存不足

先运行 5 格版，固定其他变量，再分批运行。必要时降低共同输出分辨率以做快速预检，正式实验再统一提高；不可比较混合分辨率的结果。

## 9. 一直没有图像输出 / Bypass 下游失效

检查当前启用的 `PreviewImage`、Sampler、Decode、Union Apply 处于同一有效执行链。Bypass 不是计算性能优化的保证；在不同节点框架可能有不同传播机制。

## 10. Turbo 8 步和 Simple 调度混淆

该 Depth 75 是 25 步 Qwen 2.1 Base 实验，**不是 Turbo**。官方 Turbo 使用自己的 sigma 时间表，不能不加区分复用 `Euler + simple` 的 8 步。

## 11. RunningHub 无法安装插件

这取决于 RunningHub 镜像权限及现有模型。JSON 语法正确并不能保证云端提供 T8 Union、DepthAnythingV2 或所需模型。

## 12. 公开日志是否安全

提交报错前去掉：`Rh-Comfy-Auth`、cookie、token、`cos_url` 签名查询、私有 IP、账户信息、授权付费图片链接。不要上传 `.env`、权重或含私有凭据的原工作流。
