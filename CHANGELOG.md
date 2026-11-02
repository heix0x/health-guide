# CHANGELOG · 健康指南（仓库）

只记结构级变更。书的内容变更，在各自目录的 `CHANGELOG.md`。

---

## v2.0 · 2026-11-02 · 分家

**根目录从「一本书 + 一个附件」改成「一个健康指南仓库 + 两本平级的书」。**

- 主册迁入 `student-health/`，用 `git mv` 搬，历史保留；根目录不再放正文、`docs/`、`tools/`、`dist/`。
- `smoke/` 定为同级子项目，不再写作「主册的分项目」。它的读者从「高中生」改为「任何抽烟或被动吸烟的人」，场景卡不再设校园。
- 新增根 `GLOSSARY.md`：二手烟、侧流烟、三手烟、TSNA 等跨项目术语只定义一次。
- 新增 `docs/adr/`：0001 记录分家与文档分层，0002 记录 smoke 的读者定位。
- 新增 `docs/待办-根目录改名.md`：把仓库改名为 `health-guide` 的风险、会话记录位置与操作步骤。
- `AGENTS.md` 仍是一份，补了「一书一目录」的结构约定，并把 grep 示例改成 `*/index.html`。
- `.gitignore` 的 `docs/资料库/` 改为 `**/资料库/`——资料库跟着书走，不能因为换目录就进库。

## v1.x 及以前

见 [`student-health/CHANGELOG.md`](student-health/CHANGELOG.md)。2026-10-31 之前的全部版本都记在那里。
