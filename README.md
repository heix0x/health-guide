# 健康指南

两本给普通人看的健康读物，同一个仓库。

它们不解决「怎么活得更久」，只解决「现在这个状况算不算事、能做什么」。都能查、能打印，不用从头读到尾。

## 两本书

| 书 | 目录 | 写给谁 | 体量 |
| --- | --- | --- | --- |
| 《高中生身体健康指北》 | [`student-health/`](student-health/) | 高中生，尤其寄宿 | 七章，A4 二十三页 |
| 《一根烟的事》 | [`smoke/`](smoke/) | 抽烟的人，和每天闻得到烟的人 | 七章 + 前言与结语，A4 二十二页 |

两本各自独立：各自一个 `index.html`，各自一份 `dist/pdf/`，各自一套构建脚本。**根目录不放正文。**

## 线上

| 页面 | 地址 |
| --- | --- |
| 索引（两本择一） | https://teen-gut-health-guide.app.workbuddy.host/?sharecode=YED3TRN3YC |
| 《高中生身体健康指北》 | https://teen-gut-health-guide.app.workbuddy.host/student-health/?sharecode=YED3TRN3YC |
| 《一根烟的事》 | https://teen-gut-health-guide.app.workbuddy.host/smoke/?sharecode=YED3TRN3YC |

`?sharecode=` 不能省。转发请整条复制。

线上是 `public/` 的副本，`public/` 由 `portal/index.html` 加两本书组装而成，**每次都要重新生成再发布**。为什么是两个子路径而不是两个应用、为什么不放 PDF，写在 [`docs/adr/0004`](docs/adr/0004-一个应用两个地址.md)；具体步骤与排错在 [`docs/部署与发布.md`](docs/部署与发布.md)。

## 打开

进目录，双击 `index.html`。没有构建步骤，不需要联网。

## 打印

```bash
cd student-health && python tools/build_pdfs.py
cd ../smoke && python tools/build_pdfs.py
```

成品在各自的 `dist/pdf/`。细节见每本书的 README。

## 目录结构

```
README.md              这份索引
AGENTS.md              写作与交付约定（全仓库共用一份）
GLOSSARY.md            跨项目术语，只定义一次
CHANGELOG.md           仓库级结构变更
portal/index.html      线上索引页（选哪本书）
tools/assemble_public.py   组装 public/，发布用
public/                发布产物，每次重建，不进库
docs/
  adr/                 跨项目的结构决策（0001 分家 / 0002 读者 / 0003 不谈自己 / 0004 一个应用两个地址）
  部署与发布.md          地址、发布步骤、排错
  版本管理.md            分支、提交、PDF 与 tag、备份
  待办-根目录改名.md      改名已执行，留档
student-health/        子项目一：高中生身体健康指北
  index.html
  README.md
  CHANGELOG.md
  docs/                决策台账、内容依据台账、审阅报告
  tools/build_pdfs.py
  dist/pdf/
smoke/                 子项目二：一根烟的事
  index.html
  README.md
  CHANGELOG.md
  docs/
  tools/build_pdfs.py
  dist/pdf/
```

## 共同约定

- **写作**：`AGENTS.md` 里的十四条。它不是风格指南，是刹车记录。
- **术语**：`GLOSSARY.md`。同一个概念只用一个词，两本书不许各说各话。
- **文档分层**：通用的（AGENTS、术语、结构 ADR）放根目录；每本书自己的决策台账、内容依据台账、CHANGELOG 放各自目录。不重复。
- **发布**：`public/` 是产物，改了正文必须重跑组装再发布。见 [`docs/部署与发布.md`](docs/部署与发布.md)。
- **版本**：只在 `main` 上写；一次提交一件事；PDF 只在定版提交里更新。见 [`docs/版本管理.md`](docs/版本管理.md)。

## 免责

两本书都是健康科普，不构成诊疗建议或用药指导。持续不适请就医。
