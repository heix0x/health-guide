#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 index.html 渲染成 PDF：全册一份、每章各一份。

用法（在 student-health 目录）：
    python tools/build_pdfs.py

产物在 dist/pdf/。PDF 是产出的副产物，源永远是 index.html——
改了正文字句或版式之后要重跑一次，否则 PDF 是旧的。

页码不在这里做。它由 index.html 打印样式里的 @page 边距盒生成，
Chrome 直接印进 PDF。这个脚本只干两件事：

1. 逐章渲染、数页数，推出每章在全册里从第几页开始，把页码写回
   index.html 封面那张「纸面索引」的 data-pg 占位符（屏幕上隐藏，只有打印才出现）。
2. 渲染全册，检查有没有空白页，以及只剩一行页脚的「薄页」。
"""

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "dist" / "pdf"

FULL_NAME = "全册.pdf"

# (输出文件名, ?print= 的值)　顺序必须与正文里的章节顺序一致
CHAPTERS = [
    ("00-写在前面.pdf", "start"),
    ("01-你的胃，最先撑不住.pdf", "ch1"),
    ("02-吃：一天三顿，能救回来.pdf", "ch2"),
    ("03-睡：熄灯之后.pdf", "ch3"),
    ("04-心：脑子停不下来.pdf", "ch4"),
    ("05-动：你每天都在跑.pdf", "ch5"),
    ("06-眼与身体：坐 14 小时之后.pdf", "ch6"),
    ("07-生病了，去哪儿.pdf", "ch7"),
]

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def find_browser():
    for p in BROWSERS:
        if Path(p).exists():
            return p
    sys.exit("没找到 Edge 或 Chrome，无法渲染 PDF。请改 BROWSERS 里的路径。")


def render(browser, url, dest):
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",      # 去掉浏览器自带的 URL 和日期页眉
        "--virtual-time-budget=6000",  # 等脚本跑完再截
        f"--print-to-pdf={dest}",
        url,
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def inspect(path):
    """返回 (页数, 空白页, 薄页)。

    空白页 = 几乎没有文字，属于事故（上次「30 页全白」那个坑）。
    薄页   = 一页只剩一两行字，读者会以为书印坏了。
    """
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    lengths = [len((p.extract_text() or "").strip()) for p in reader.pages]
    blanks = [i + 1 for i, n in enumerate(lengths) if n < 20]
    thins = [i + 1 for i, n in enumerate(lengths) if 20 <= n < 80]
    return len(reader.pages), blanks, thins


# ---------- 纸面索引：把页码写回 index.html ----------

def read_published():
    """读出 index.html 里当前写着的页码，形如 {'ch1': 3, ...}。"""
    html = SRC.read_text(encoding="utf-8")
    found = {}
    for key, val in re.findall(r'<i class="pg" data-pg="(\w+)">([^<]*)</i>', html):
        found[key] = int(val) if val.strip().isdigit() else None
    return found


def patch_published(starts):
    """把页码写进占位符。已经是这个数就不动文件，免得平白改一次 mtime。"""
    html = SRC.read_text(encoding="utf-8")
    new = html
    for key, page in starts.items():
        # 占位符可能还是「–」，所以这里匹配 [^<]*，不能只匹配数字
        new = re.sub(
            rf'(<i class="pg" data-pg="{key}">)[^<]*(</i>)',
            rf"\g<1>{page}\g<2>",
            new,
        )
    if new == html:
        return False
    with open(SRC, "w", encoding="utf-8", newline="") as fh:
        fh.write(new)
    return True


# ---------- 主流程 ----------

def main():
    try:
        import pypdf  # noqa: F401
    except ImportError:
        sys.exit("缺少 pypdf，先跑：python -m pip install pypdf")

    if not SRC.exists():
        sys.exit(f"找不到 {SRC}")

    browser = find_browser()
    OUT.mkdir(parents=True, exist_ok=True)
    base = SRC.as_uri()

    counts = []
    # 页码变了正文会跟着挪，所以最多再来一遍，直到稳定
    for _ in range(3):
        counts = []
        for name, scope in CHAPTERS:
            dest = OUT / name
            print(f"  渲染 {name} ...", end="", flush=True)
            render(browser, f"{base}?print={scope}", dest)
            pages, blanks, thins = inspect(dest)
            counts.append((name, scope, pages, blanks, thins))
            print(f" {pages} 页")

        starts, acc = {}, 1
        for name, scope, pages, _, _ in counts:
            starts[scope] = acc
            acc += pages

        wanted = {k: v for k, v in starts.items() if k != "start"}
        published = read_published()
        if all(published.get(k) == v for k, v in wanted.items()):
            break
        print(f"  封面索引页码更新：{wanted}")
        patch_published(wanted)

    total = acc - 1

    full = OUT / FULL_NAME
    print(f"  渲染 {FULL_NAME} ...", end="", flush=True)
    render(browser, base, full)
    full_pages, full_blanks, full_thins = inspect(full)
    print(f" {full_pages} 页")

    # 版权页不属任何一章，全册比各章相加多出 1 页是正常的
    if full_pages not in (total, total + 1):
        print(f"  警告：全册 {full_pages} 页，各章相加 {total} 页——封面页码可能已偏，请重跑一次")

    rows = []
    for name, scope, pages, blanks, thins in counts:
        state = f"起于第 {starts[scope]} 页"
        if blanks:
            state = f"空白页 {blanks}"
        elif thins:
            state = f"薄页 {thins}（只剩一两行）"
        rows.append((name, pages, state))

    state = "OK"
    if full_blanks:
        state = f"空白页 {full_blanks}"
    elif full_thins:
        state = f"薄页 {full_thins}（只剩页脚）"
    rows.append((FULL_NAME, full_pages, state))

    print("\n" + "=" * 56)
    for name, pages, state in rows:
        print(f"{name:<28} {str(pages):>3} 页  {state}")
    print("=" * 56)
    print(f"输出目录：{OUT}")

    bad = [r[0] for r in rows if "空白页" in r[2]]
    thin = [r[0] for r in rows if "薄页" in r[2]]
    if bad:
        sys.exit(f"\n有空白页：{bad}　先把分页修好。")
    if thin:
        print(f"\n提醒：{thin} 的末页只剩一两行，调版时把它并回上一页。")


if __name__ == "__main__":
    main()
