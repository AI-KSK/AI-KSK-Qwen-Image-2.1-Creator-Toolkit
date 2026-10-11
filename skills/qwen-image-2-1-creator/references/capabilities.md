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
| benchmark | 0~10 | 固定 prompt, seed 与可控变量 | JSON+CSV | 检查 CFG/steps/sigma 差异 |
| cn_t2i | 0 + 1张控制图 | 结构控制 + 成片提示 | PNG | control image 不计入 `<image1>` 引用；需实际 Union/ControlNet 节点 |
| cn_single_ref | 1参考图 + 1控制图 | 保真主体 + follow control map | PNG | 主体由参考图约束，结构由 control image 约束 |
| cn_multi_ref | 2~10参考图 + 1控制图 | `<image1>`… + structure | PNG | 多参考图负责内容分工，control image 负责结构 |
| cn_inpaint_ref | 1~10参考图 + inpaint + mask + 控制图(可选) | 只改遮罩区 | PNG | 必须核实存在 mask / inpaint_image 输入 |
| video_t2v | 0 | 镜头/动作/时长/运镜提示 | 交接 JSON | Wan/H3等视频模型必须独立运行 |
| video_i2v | 1+ | 首帧 + 动作 / 镜头 | 交接 JSON | Qwen 负责源图，视频模型负责帧序列 |
| video_storyboard | 1+ | 多镜头静态图 + 动态镜头描述 | 交接 JSON | 后期镜头一致性另测 |

官方上限10图指核心模型能力，不保证任一旧 ComfyUI 工作流动态端口存在；在目标节点上核验 `images.image_1 ... images.image_10`。


## ControlNet + 参考图补充规则

- `control_image` 负责几何、姿态、轮廓、建筑结构、深度；不要把它当内容参考图。
- `reference_image` / `reference_image_2` / `reference_image_3` 负责主体身份、服装、风格或场景来源。
- AIO 适合快速切换；若需阈值精调，改用独立预处理器。
- 编辑任务优先使用参考图编码得到的 latent；无关 Empty Latent 会破坏保真度。
