# CHANGELOG · 健康指南（仓库）

只记结构级变更。书的内容变更，在各自目录的 `CHANGELOG.md`。

---

## v2.2 · 2026-11-02 · 公开

**仓库公开，允许别人读、也允许别人按规矩再分。**

- 公开到 `github.com/heix0x/health-guide`，首次 Release 附两本全册 PDF（`student-health-guide-v2.2.pdf`、`smoke-guide-v2.2.pdf`，附件名用 ASCII——中文名经 API 上传会被截成 `-v2.2.pdf`）。
- 新增 `LICENSE`：CC BY-NC-SA 4.0 官方全文 + 中文摘要。README 末尾加「许可」一节。
- 「为什么不用 MIT」写进 `docs/部署与发布.md`：CC 四个维度、MIT 放在书上的三个后果、双许可为什么最后没拆。
- `docs/待办-根目录改名.md` 的 5 处绝对路径（含 `C:\Users\<用户名>`）改为 `$env:USERPROFILE` 占位符——公开前唯一必须处理的隐私点。
- 推送前改写了一版历史（`filter-branch --tree-filter`），把这 5 处从旧提交里一并清掉；此前所有 commit hash 变化，改写前的镜像备份留在仓库外。`docs/版本管理.md` 已注明以新 hash 为准。
- `docs/版本管理.md`：「远程」从「无」改为已配置，备份单点风险解除。

## v2.1 · 2026-11-02 · 上线

**两本书各有一个线上地址，共用一个应用。**

- 新增 `portal/index.html`：线上索引页，两本择一。页尾一小段脚本把 `?sharecode=` 带到子路径上——不带参数的子页面会返回「链接不完整」。
- 新增 `tools/assemble_public.py`：把索引页与两本书组装成 `public/`，只复制 `index.html`，不复制 `docs/`、`dist/`。脚本带四项检查（体积、内联样式、外部引用、`#ch1` 锚点），不过关不生成。
- `public/` 列入 `.gitignore`：产物不进库。
- 发布形态定为「一个应用 + `/student-health/`、`/smoke/` 两个子路径」，而非两个独立应用——一个工作区只对应一个应用，实测两次子目录发布互相覆盖。理由与被否方案见 `docs/adr/0004`。
- 新增 `docs/部署与发布.md`（地址、步骤、排错）与 `docs/版本管理.md`（分支、提交粒度、PDF 与 tag、远程备份）。
- 根 `README.md` 加线上地址表；`AGENTS.md` 第 14 条补上 `portal/` 与 `tools/assemble_public.py` 的位置。
- `docs/待办-根目录改名.md` 标记完成：目录已是 `health-guide`。

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
