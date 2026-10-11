# FAQ

**Q：75 格是 75 张同时生成吗？** 不是，每格都有一条独立采样链；是否并发由实际执行环境决定，成本较高。

**Q：可以不用 Depth Anything V2 吗？** 可以使用 `03_manual_depth_first_row_5.json` 上传事先准备好的 Depth 图，但应确保控制图与目标画幅比例一致。

**Q：预览标题里的 S/E/W 是什么？** `S` = start_percent；`E` = end_percent；`W` = strength。

**Q：为什么输入图变画风了？** 75 格基线是纯 Depth，不连接图像参考编码，结构可约束，风格不保证。

**Q：是否已经 RunningHub 验收？** 没有。仅完成了离线静态结构检查。按 INSTALL_CN.md 自行验证后才能标记运行成功。

**Q：ZIP 上传 GitHub 为何变成一个文件？** GitHub Web 的“Upload files”不会自动解压压缩包。先解压，再把项目**内部文件和子目录**上传到仓库根目录。

**Q：能商业使用 ControlNet 权重吗？** 不能仅因代码上传 GitHub 就推断权重允许商用，Union 模型卡说明非商业研究许可限制，需另查合法商业授权。
