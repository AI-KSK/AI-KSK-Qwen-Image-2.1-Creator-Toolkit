# GitHub 发布检查清单

## A. 仓库准备

- [ ] 确定仓库名称（推荐 `AI-KSK-Qwen-Image-2.1-Creator-Toolkit`）。
- [ ] 选择 Public/Private；如果准备允许复用，先确认根目录 `LICENSE`，见 `LICENSE-DECISION.md`。
- [ ] 确定版权作者/署名及对外联络渠道（不要误填未经授权的邮箱）。
- [ ] 添加 GitHub About 简介、Topics、语言及项目用途；可使用本文件末尾的草案。
- [ ] 封面、截图、横评结果、教程视频请在获得版权及人物许可后再上传。
- [ ] 若以后要发布模型权重，请先检查研究许可和大小限制，勿直接用普通 Git 上传。

## B. 代码/文件审计

- [ ] `python scripts/check_depth75.py` 通过。
- [ ] `python -m unittest discover -s tests -v` 通过。
- [ ] `python -m unittest discover -s skills/qwen-image-2-1-creator/tests -v` 通过。
- [ ] `.gitignore` 有效：不提交 `.env`、真实 token、权重、缓存、日志及个人参考图。
- [ ] 搜索 `Rh-Comfy-Auth`、`cos_url`、`Bearer`、`token=`、`apikey`、API Key 和私人 IP；误命中需人工复核。
- [ ] 拖入 5 格 JSON：节点加载、模型下拉有效，运行 baseline 与第一行 5 格。
- [ ] 若需发布“已验证可运行”，先提供真实 Runtime 截图、GPU/ComfyUI/插件版本和运行日志。
- [ ] 75 格需分层执行并记录耗时、VRAM、Seed 和各组结果；无实际记录不写实测数据。

## C. 上传 GitHub 的两种方式

**网页上传（最简单）**：

1. 在 GitHub 新建仓库，推荐不要预先自动添加 README（本包已有）。
2. 在本地**解压**本仓库 ZIP。
3. 在仓库页面点击 **Add file → Upload files**，将解压后最外层目录里的**全部文件/文件夹**拖入；确保上传后仓库根目录能直接看到 `README.md`、`skills/`、`workflows/`。ZIP 本体直接上传只会成为一个压缩文件，GitHub 不会自动展开成可浏览的代码树。
4. 写 Commit message（例如 `Initial public toolkit packaging`），选择分支，提交。
5. 打开 GitHub Actions，确认 CI 静态校验通过。
6. 检查文件目录、README 链接、Issue 模板与 Release 下载。

**Git 命令上传（推荐维护更新）**：在**解压后的仓库根目录**执行：

```bash
git init
git add .
git commit -m "Initial AI-KSK Qwen Image 2.1 creator toolkit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/AI-KSK-Qwen-Image-2.1-Creator-Toolkit.git
git push -u origin main
```

将 `YOUR_USERNAME` 改为你的 GitHub 用户名；如远端已经包含初始 README 或 Git 提交，需先合并处理，**不要直接强制 push 覆盖**。需要事先完成 `git config user.name` / `user.email` 和 GitHub 身份认证。

## D. 发布包与版本管理

- [ ] 首个版本建议 `v0.1.0`，发布状态标记 **Runtime verification pending**。
- [ ] 在 GitHub Releases 提供 ZIP、更新日志、兼容 ComfyUI/节点版本、依赖下载链接和已知限制。
- [ ] 上传“横评样片”前确认内容版权；对任何性能比较给出统一测试条件。
- [ ] 后续每次修改 JSON 都要运行结构校验，并在 CHANGELOG 记录变更。

## GitHub About / Topics 建议

**Description：** `AI-KSK Qwen Image 2.1 Creator Skill + ComfyUI Depth ControlNet Union 75-case benchmark, workflow templates and validators.`

**Topics：** `comfyui`, `qwen-image`, `controlnet`, `depth-anything`, `workflow`, `benchmark`, `ai-image-generation`, `codex-skill`

**首发 Release title：** `v0.1.0 — Qwen Image 2.1 Creator Skill v3 + Depth Control 75-grid benchmark (static verified)`
