# Qwen Image 2.1：ControlNet Union + 参考图编辑规则

## 1. 目的

本文件专门服务于 Qwen Image 2.1 的 **结构控制 + 多图参考编辑** 场景，用于回答以下问题：

1. 能否同时使用 ControlNet 与参考图编辑？
2. control map、reference image、mask 各自负责什么？
3. AIO 预处理器适合放在哪一层？
4. 提示词应如何表达 `<image1>`、`<image2>` 与 control map 的关系？

答案：**可以同时使用**。但必须区分输入职责，不能把结构图与内容参考图混为一谈。

## 2. 输入角色划分

### 2.1 `control_image`

负责姿态、边缘、线稿、深度、建筑线条、几何结构或整体布局。

### 2.2 `reference_image`

主参考图，通常负责：

- 主体身份
- 原图比例与保真主体
- 核心商品或人物

### 2.3 `reference_image_2` / `reference_image_3`

次参考图，通常负责：

- 服装
- 第二人物
- 风格
- 环境/场景
- 商品摆放环境

### 2.4 `inpaint_image` + `mask`

在局部编辑场景中：

- `inpaint_image`：原始待编辑图片
- `mask`：允许修改的区域

Skill 必须要求：未遮罩区域保持不变。

## 3. AIO 预处理器建议

AIO 适合默认快速路线，支持一键切换常用预处理器。若要求更细阈值和更强可控性，则切换到独立节点。

推荐默认枚举：

- `canny`
- `depth`
- `hed`
- `lineart`
- `mlsd`
- `pose`
- `scribble`
- `none`

## 4. 提示词写法

### 单参考图 + ControlNet

Preserve the identity, facial features, hairstyle, body proportions, and key outfit characteristics of the reference image. Follow the provided control map for the final pose, composition, or structural layout. Keep the subject recognizable and coherent.

### 双参考图 + ControlNet

Use `<image1>` as the primary subject reference and preserve its identity, anatomy, and core recognizable features. Use `<image2>` as the secondary reference for the outfit, style, environment, or product context. Follow the provided control map for the final pose, composition, or structural arrangement. Transfer only the requested attributes from `<image2>` while preserving the protected features from `<image1>`.

### 三参考图 + ControlNet

Use `<image1>` as the primary subject reference, `<image2>` as the secondary appearance or outfit reference, and `<image3>` as the environment or style reference. Follow the provided control map for the final pose, arrangement, or scene structure. Preserve the protected identity and major visual traits from `<image1>`, transfer only the requested elements from `<image2>`, and integrate them naturally into the scene or style of `<image3>`.

### Inpaint + ControlNet + 参考图

Edit only the masked region of the source image while preserving all unmasked regions unchanged. Use `<image1>` as the main appearance or content reference inside the edited area, and follow the provided control map for the structural layout within the edited region. Keep the result seamlessly integrated in lighting, perspective, texture, and edge transitions.

## 5. 常见错误

1. 把控制图也写成 `<image2>` 的内容来源。
2. 用不相关的 `Empty Latent` 覆盖参考图编码输出。
3. 让 AIO 生成的控制图比例与最终画布不一致。
4. 在局部重绘任务中漏接 `mask`。
5. 误以为 ControlNet 可以自动精确复制另一张图中的脸或服装。
