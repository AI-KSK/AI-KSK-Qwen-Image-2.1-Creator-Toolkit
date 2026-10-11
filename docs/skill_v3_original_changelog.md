# Qwen21 Full Creator Skill v3.0.0

## 新增

- ControlNet Union + 参考图编辑规则
- AIO Preprocessor 使用建议
- CN + 单参考图 / 多参考图 / Inpaint 三个示例任务
- `references/cn_and_reference_rules.md` 专题文档

## 更新

- `README.md` 升级为 v3.0.0
- `SKILL.md` 增加 2.5 节：ControlNet Union + 参考图编辑规则
- `references/capabilities.md` 新增 CN 能力矩阵
- `references/official_sources.md` 增补 ControlNet / AIO 来源
- `assets/task_schema_example.json` 增加 `control_image` 与 `control_mode` 示例字段

## 校验

- `python -m unittest discover -s tests -v` 通过
