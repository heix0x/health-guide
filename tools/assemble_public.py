#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""组装发布目录 public/。

源 → 产物，单向。public/ 每次清空重建，不要手改 public/ 里的任何文件，
改了也会在下一次运行时被覆盖（见 AGENTS.md 第 12 条「产物不是源」）。

产出结构：
    public/index.html               书目索引（源：portal/index.html）
    public/student-health/index.html
    public/smoke/index.html

只复制 index.html，不复制 docs/、tools/、dist/ —— 私人素材和中间产物不上传。

用法：
    python tools/assemble_public.py
"""

import re
import shutil
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "public"

# 子项目目录名 → 在 public/ 里的路径
BOOKS = ["student-health", "smoke"]

# 页面里出现这些，说明有外部依赖，上线后会白屏或走失
EXTERNAL = re.compile(r'(?:src|href)\s*=\s*["\'](?:https?:|//)')


def fail(msg):
    print(f"✗ {msg}")
    sys.exit(1)


def check(path, require_anchors=False):
    """抽内容验证，不只看文件在不在（AGENTS.md 第 11 条）。"""
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) < 20000:
        fail(f"{path.relative_to(BASE)} 只有 {len(text)} 字符，疑似被截断")
    if "<style" not in text:
        fail(f"{path.relative_to(BASE)} 没有内联样式，样式可能被拆出去了")
    if EXTERNAL.search(text):
        fail(f"{path.relative_to(BASE)} 引用了外部资源，静态托管下会失效")
    if require_anchors and "#ch1" not in text:
        fail(f"{path.relative_to(BASE)} 找不到章节锚点 #ch1，可能不是正文页")
    return len(text)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    # 索引页
    src = BASE / "portal" / "index.html"
    if not src.exists():
        fail("portal/index.html 不存在")
    dst = OUT / "index.html"
    shutil.copyfile(src, dst)
    for book in BOOKS:
        if f'href="{book}/"' not in dst.read_text(encoding="utf-8"):
            fail(f"portal/index.html 里没有指向 {book}/ 的链接")
    print(f"  public/index.html  {dst.stat().st_size:>7,} B")

    # 两本书
    for book in BOOKS:
        src = BASE / book / "index.html"
        if not src.exists():
            fail(f"{book}/index.html 不存在")
        chars = check(src, require_anchors=True)
        dst = OUT / book / "index.html"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        print(f"  public/{book}/index.html  {dst.stat().st_size:>7,} B  ({chars:,} 字符)")

    total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"\n✓ public/ 就绪，{len(list(OUT.rglob('*.html')))} 个页面，合计 {total:,} B")
    print("  部署：以 public/ 为目录发布（不要把仓库根目录直接上传，docs/资料库 含真实姓名）")


if __name__ == "__main__":
    main()
