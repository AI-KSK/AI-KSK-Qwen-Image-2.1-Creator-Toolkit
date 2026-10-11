# 必需的三角色交叉评审记录模板

## 初步提案
- 角色 A（模型能力/提示词）：任务类型、官方接口、画面固定约束、PE-T2I或PE-I2I 使用计划。
- 角色 B（工程/部署）：底模、文本编码器、VAE、参考图路径/数量、ComfyUI端口、模型版本、mask/alpha、GPU预算。
- 角色 C（验收/横评）：业务目标、保真指标、对照变量、速度与内存测试、可复现性、风险。

## 强制交叉质询
- A→B：参考图是否真的接入，双图端口存在吗？是否把官方 Turbo checkpoint 和 LoRA 混为一谈？
- B→C：用同 seed 同分辨率吗？比较的是纯 LoRA 效果还是 Base/Turbo 两个完整推理方案？有 GPU 运行日志吗？
- C→A：字面内容、角色 ID、构图与局部保留被明确写进提示词了吗？提示词中文/英文是否符合官方编辑/T2I分路规范？

## 决策记录
```
Review ID:
Task / input count:
A position / issues:
B position / issues:
C position / issues:
Cross-questions and answers:
Approved changes:
Rejected assumptions:
Blockers:
Execution authorization:
Static QA:
Runtime QA: pending|passed|failed
```

没有独立子代理接口时，只写单助手三视角评审；禁止自称真实三 Agent 各自推理。
