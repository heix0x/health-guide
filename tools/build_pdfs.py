#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 index.html 渲染成 PDF：全册一份，每一章各一份。

用法（在项目根目录）：
    python tools/build_pdfs.py

产物在 dist/pdf/。改了 index.html 的正文字句之后要重跑一次，否则 PDF 是旧的。

原理：调本机 Edge / Chrome 的 headless 打印，逐份访问 index.html?print=<id>。
      页面里那段脚本看到 ?print= 就只给那一章打打印范围，不会弹窗。
"""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "dist" / "pdf"

# (输出文件名, ?print= 的值)；空字符串表示全册
JOBS = [
    ("全册.pdf", ""),
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
    """返回 (页数, 空白页页码)。这是上次「30 页全空白」那个坑的硬检查。"""
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    lengths = [len((p.extract_text() or "").strip()) for p in reader.pages]
    blanks = [i + 1 for i, n in enumerate(lengths) if n < 50]
    return len(reader.pages), blanks


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

    rows, failed = [], 0
    for name, scope in JOBS:
        dest = OUT / name
        url = f"{base}?print={scope}" if scope else base
        print(f"  渲染 {name} ...", end="", flush=True)
        try:
            render(browser, url, dest)
            pages, blanks = inspect(dest)
        except Exception as exc:  # noqa: BLE001
            print(f" 失败：{exc}")
            failed += 1
            rows.append((name, "—", "失败"))
            continue

        if pages == 0 or blanks:
            print(f" 有问题（{pages} 页，空白页 {blanks}）")
            failed += 1
            rows.append((name, pages, f"空白页 {blanks}"))
        else:
            print(f" {pages} 页")
            rows.append((name, pages, "OK"))

    print("\n" + "=" * 46)
    for name, pages, state in rows:
        print(f"{name:<28} {str(pages):>3} 页  {state}")
    print("=" * 46)
    print(f"输出目录：{OUT}")

    if failed:
        sys.exit(f"\n{failed} 份没通过检查，别直接用。")


if __name__ == "__main__":
    main()
