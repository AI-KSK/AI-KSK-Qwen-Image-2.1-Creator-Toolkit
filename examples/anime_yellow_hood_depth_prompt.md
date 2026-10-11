# 深度教学案例：黄色兜帽厚涂动漫人物（仅文字，不附带参考原图）

适合观察前景膝盖、躯干、头部、蓬松兜帽的远近层次。若你使用不同图片，请根据你实际输入图重新写 Prompt；**75 个 ControlNet 分支共享同一组编码输出**。

## 正向提示词（建议）

```text
An expressive anime-style digital painting of a seated young adult woman with her knees drawn upward in the foreground, wearing an oversized bright golden-yellow hooded jacket with large angular fabric folds. Tousled dark blue-black hair with cobalt highlights frames pale blue-gray eyes and a calm, slightly melancholic expression. The composition uses strong foreground foreshortening, a nearly white uncluttered background, bold painterly brushwork and broad, irregular opaque color shapes. Maintain the vibrant yellow-and-deep-blue contrast, intentional stylization, economical shading, clean visual hierarchy and natural seated anatomy. Avoid photorealistic textures, unnecessary microdetails and decorative clutter. Follow the supplied depth map for the body silhouette, raised knees, torso, head placement, hood volume and spatial perspective.
```

## 负向提示词（建议）

```text
photorealism, glossy 3D, plastic skin, excessive hair strands, chaotic microtexture, clutter, dense ornament, noisy highlights, extra limbs, malformed knees, broken anatomy, flattened perspective, distorted face, watermark, unwanted text
```

## 注意

Depth 是**空间结构控制**，不是艺术风格保真。上述内容描述的是输出图视觉目标，不是要求 Qwen 编辑模型像素级保留输入图。如果要做严格 ID / 画风保持，需使用额外参考图编码链并重新设计对照条件。
