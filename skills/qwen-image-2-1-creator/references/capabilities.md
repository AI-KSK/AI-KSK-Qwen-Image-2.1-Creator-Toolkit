# 功能矩阵与技术依赖

| 任务 | 参考图 | 典型提示词 | 产物 | 注意事项 |
|---|---:|---|---|---|
| t2i | 0 | 英文成片观察式 | PNG | `wh_ratio` 单独保存；不得让 image 进入 T2I PE |
| single_edit | 1 | 动作式修改说明 | PNG | ratio 默认继承原图 |
| multi_edit | 2~10 | `<image1>`/`<image2>` 引用与任务角色 | PNG | ComfyUI 真正多图节点连线取决于版本 |
| local_edit | 1+遮罩 | 明确对象与局部边界 | PNG | 单有 prompt 不等于实现 mask 输入 |
| transparent | 0 或 1~10 | alpha/transparent background | RGBA PNG | 解码和保存必须保留 alpha |
| outpaint | 1 | 扩展方向、背景延续、目标比例 | PNG | 不可继承旧比例又指定新比例 |
| typography | 0 或1+ | 可读字符串原样放双引号 | PNG | 文字逐字人工验收 |
| identity | 1~10 | 锁定主体/几何/纹理/服装替换角色 | PNG | 多图 ID 不能假定 100% 稳定 |
| storyboard | 0 或1~10 | 分镜结构 / 连贯性角色 | PNG | 不是原生视频 |
| benchmark | 0~10 | 固定 prompt, seed 与可控变量 | JSON | 检查 CFG/steps/sigma 差异 |
| video_t2v | 0 | 镜头/动作/时长/运镜提示 | 交接 JSON | Wan/H3等视频模型必须独立运行 |
| video_i2v | 1+ | 首帧 + 动作 / 镜头 | 交接 JSON | Qwen 负责源图，视频模型负责帧序列 |
| video_storyboard | 1+ | 多镜头静态图 + 动态镜头描述 | 交接 JSON | 后期镜头一致性另测 |

官方上限10图指核心模型能力，不保证任一旧 ComfyUI 工作流动态端口存在；在目标节点上核验 `images.image_1 ... images.image_10`。


## ControlNet Union 变体（用现有 mode 表达，不是独立校验模式）

`scripts/validate_task.py` 只认 **13 个 mode**：10 个图像 mode（`t2i` / `single_edit` / `multi_edit` / `local_edit` / `transparent` / `outpaint` / `typography` / `identity` / `storyboard` / `benchmark`）+ 3 个视频 mode（`video_t2v` / `video_i2v` / `video_storyboard`）。

**没有 `cn_*` 校验模式。** ControlNet Union 路线是给现有 mode 追加 `control_image` 与 `control_mode` 字段来表达的：

| CN 变体 | 实际使用的 mode | 校验器强制的参考图数量 | 关键字段 | 示例 |
|---|---|---|---|---|
| CN + T2I | `t2i` | 0 | `control_image`, `control_mode` | — |
| CN + 单图参考 | `single_edit` | 恰好 1 | `control_image`, `control_mode` | `examples/cn_single_ref.json` |
| CN + 多图参考 | `multi_edit` | 2~10（提示词须逐个写出 `<imageN>` 角色） | `control_image`, `control_mode` | `examples/cn_multi_ref.json` |
| CN + 局部重绘 | `local_edit` | 恰好 1，另需 `mask_path` 或 `visual_annotation` | `control_image`, `control_mode`, 可选 `reference_images` | `examples/cn_inpaint_ref.json` |

注意：`reference_images`、`control_image`、`control_mode` 属于**附加字段**，`scripts/validate_task.py` 只检查其存在与形态，**不校验文件是否存在，也不限制张数**。局部重绘路线的主输入图仍受 `local_edit` 的"恰好 1 张"约束；要接更多参考图，属于节点连线改造，必须另行测试。

## ControlNet + 参考图补充规则

- `control_image` 负责几何、姿态、轮廓、建筑结构、深度；不要把它当内容参考图。
- `reference_image` / `reference_image_2` / `reference_image_3` 负责主体身份、服装、风格或场景来源。
- AIO 适合快速切换；若需阈值精调，改用独立预处理器。
- 编辑任务优先使用参考图编码得到的 latent；无关 Empty Latent 会破坏保真度。
