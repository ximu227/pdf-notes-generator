#!/usr/bin/env python3
"""
HTML 笔记渲染为 PNG 图片
用法: python3 render_notes.py <html_path> <output_png> [--width 1080]
依赖: playwright + chromium
"""
import sys
import argparse
import time
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright


def _find_chromium() -> str | None:
    """自动探测可用的 chromium 可执行文件路径"""
    candidates = [
        shutil.which("chromium-browser"),
        shutil.which("chromium"),
        shutil.which("google-chrome"),
        "/usr/local/bin/chromium-browser",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    return None


def render_html_to_png(html_path: str, output_path: str, width: int = 1080, wait_ms: int = 1500):
    """将 HTML 文件全页截图为 PNG"""
    html_file = Path(html_path).resolve()
    output_file = Path(output_path).resolve()

    executable = _find_chromium()
    launch_kwargs = {"args": ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]}
    if executable:
        launch_kwargs["executable_path"] = executable

    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page(viewport={"width": width, "height": 800})
        page.goto(f"file://{html_file}", wait_until="networkidle")

        # 等待 KaTeX/MathJax 渲染完成
        time.sleep(wait_ms / 1000.0)
        try:
            page.wait_for_selector(".katex, .MathJax", timeout=3000)
            time.sleep(0.5)
        except Exception:
            pass  # 没有公式也正常

        # 等待字体加载
        page.evaluate("document.fonts && document.fonts.ready")
        time.sleep(0.3)

        # 全页截图
        page.screenshot(path=str(output_file), full_page=True, type="png")
        browser.close()

    size_kb = output_file.stat().st_size / 1024
    print(f"[OK] 截图完成: {output_file} ({size_kb:.1f} KB)", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="HTML 笔记渲染为 PNG")
    parser.add_argument("html_path", help="HTML 文件路径")
    parser.add_argument("output_png", help="输出 PNG 路径")
    parser.add_argument("--width", type=int, default=1080, help="页面宽度（默认 1080px）")
    parser.add_argument("--wait", type=int, default=1500, help="等待渲染毫秒数（默认 1500）")
    args = parser.parse_args()

    try:
        render_html_to_png(args.html_path, args.output_png, args.width, args.wait)
    except Exception as e:
        print(f"[ERROR] 渲染失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
