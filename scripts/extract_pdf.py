#!/usr/bin/env python3
"""
PDF 文本提取脚本
用法: python3 extract_pdf.py <pdf_path> [--output <txt_path>]
输出: 提取的文本内容（打印到 stdout 或写入文件）
"""
import sys
import argparse
import pdfplumber


def extract_pdf_text(pdf_path: str) -> tuple[str, int]:
    """提取 PDF 全部文本，返回 (文本, 页数)"""
    all_text = []
    page_count = 0
    with pdfplumber.open(pdf_path) as pdf:
        page_count = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            if text.strip():
                all_text.append(f"--- 第 {i+1} 页 ---\n{text.strip()}")
    return "\n\n".join(all_text), page_count


def main():
    parser = argparse.ArgumentParser(description="提取 PDF 文本内容")
    parser.add_argument("pdf_path", help="PDF 文件路径")
    parser.add_argument("--output", "-o", help="输出文本文件路径（默认打印到 stdout）")
    args = parser.parse_args()

    try:
        text, page_count = extract_pdf_text(args.pdf_path)
    except Exception as e:
        print(f"[ERROR] PDF 提取失败: {e}", file=sys.stderr)
        sys.exit(1)

    if not text.strip():
        print("[WARN] 未从 PDF 中提取到任何文本（可能是扫描版/图片型 PDF）", file=sys.stderr)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[OK] 已提取 {page_count} 页，写入 {args.output}（{len(text)} 字符）", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
