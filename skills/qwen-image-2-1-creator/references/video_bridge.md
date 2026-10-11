# Qwen Image 2.1 → 视频模型交接设计

Qwen Image 2.1 负责：人物/道具一致性母图、场景 Hero Shot、编辑换装、分镜、首帧、按镜头制作静帧。

外部 Wan2.2 / MiniMax H3 或其它已部署视频模型负责：视频时间轴、帧间运动、镜头运动、声音/嘴型（若目标模型支持）、视频解码。

| 请求 | 上游 Qwen 任务 | 下游视频任务 |
|---|---|---|
| 纯文生视频 | Qwen 可选用于 concept still | 直接 T2V |
| 单图动效 | T2I / single_edit 构建首帧 | I2V |
| 双图身份+服装动画 | multi_edit 合成母图 | I2V |
| 角色连续短片 | identity + storyboard 镜头帧 | shot-wise I2V + 合成 |
| 广告产品片 | 多图商品布景、Hero Shot | I2V 加运镜和镜头衔接 |

视频提示词必须给出：主体运动、镜头运动、背景变化、物理约束、时间长度、帧率/分辨率（平台支持时）、身份锁定、停顿/转场、负面异常；镜头间继承上一个关键帧或同一身份母图。

`scripts/video_handoff.py` 只写外部模型输入清单，不生成真实视频、不能代替实际 ComfyUI 视频工作流连接，也不自动调用 RunningHub API。
