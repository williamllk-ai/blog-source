#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Recover Hexo source content from:
  1) VS Code Local History recovery folder
  2) cloned GitHub Pages static archive

READS ONLY:
  C:\Users\williamllk\Desktop\BlogFiles_Recovered
  D:\Blog_Website_Archive

WRITES ONLY:
  D:\BlogFiles_New

Dependencies:
  python -m pip install beautifulsoup4 markdownify
"""

from __future__ import annotations

import html
import json
import re
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify as md

RECOVERED_ROOT = Path(r"C:\Users\williamllk\Desktop\BlogFiles_Recovered")
ARCHIVE_ROOT = Path(r"D:\Blog_Website_Archive")
NEW_ROOT = Path(r"D:\BlogFiles_New")
POSTS_ROOT = NEW_ROOT / "source" / "_posts"

ORIGINAL_POSTS = [
    "Basic-Algorithms.md",
    "Basic-Data-Structure-Else.md",
    "Classic-3D-Reconstruction.md",
    "CV-1.md",
    "Fast-and-Slow-Pointers.md",
    "Graph-Problems.md",
    "MIT-18-065-Lecture-1-2-Notes.md",
    "mmengine-register.md",
    "Normal-Equation.md",
    "paper-notes-GSSLAM.md",
    "SLAM-LECTURE-1.md",
    "SLAM-LECTURE-2.md",
    "SLAM-LECTURE-3.md",
    "SLAM-LECTURE-4.md",
    "SLAM-LECTURE-5.md",
    "SLAM-LECTURE-7.md",
    "SVD-Decomposition.md",
]

RECONSTRUCT = {
    "Self-Introduction.md":
        Path("2025/12/04/Self-Introduction/index.html"),
    "Basic-Data-Structure.md":
        Path("2026/02/18/Basic-Data-Structure/index.html"),
    "LU-Decomposition-and-Cholesky-Decomposition.md":
        Path("2026/04/04/LU-Decomposition-and-Cholesky-Decomposition/index.html"),
    "QR-Decomposition.md":
        Path("2026/05/01/QR-Decomposition/index.html"),
    "paper-notes-3dgs.md":
        Path("2026/07/19/paper-notes-3dgs/index.html"),
    "paper-notes-SplaTAM.md":
        Path("2026/07/21/paper-notes-SplaTAM/index.html"),
}

ASSETS = {
    Path("2026/01/27/SLAM-LECTURE-4/slam4-1.png"):
        Path("SLAM-LECTURE-4/slam4-1.png"),
    Path("2026/07/19/paper-notes-3dgs/3dgs-all.png"):
        Path("paper-notes-3dgs/3dgs-all.png"),
    Path("2026/07/19/paper-notes-3dgs/rectification.png"):
        Path("paper-notes-3dgs/rectification.png"),
    Path("2026/07/21/paper-notes-SplaTAM/pipeline.png"):
        Path("paper-notes-SplaTAM/pipeline.png"),
}

CN_TZ = timezone(timedelta(hours=8))


def find_unique(root: Path, filename: str) -> Path:
    matches = [p for p in root.rglob(filename) if p.is_file()]
    if not matches:
        raise FileNotFoundError(f"Cannot find recovered source: {filename}")
    # Prefer a path that visibly belonged to source/_posts.
    preferred = [
        p for p in matches
        if "_posts" in [part.lower() for part in p.parts]
    ]
    if preferred:
        matches = preferred
    if len(matches) > 1:
        # Use newest copy only as a deterministic fallback.
        matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        print(f"[WARN] Multiple copies of {filename}; using {matches[0]}")
    return matches[0]


def meta_content(soup: BeautifulSoup, *, prop=None, name=None):
    attrs = {}
    if prop is not None:
        attrs["property"] = prop
    if name is not None:
        attrs["name"] = name
    node = soup.find("meta", attrs=attrs)
    return node.get("content", "").strip() if node else ""


def published_local_time(soup: BeautifulSoup) -> str:
    raw = meta_content(soup, prop="article:published_time")
    if not raw:
        return ""
    # Example: 2026-07-21T04:07:36.000Z
    dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    return dt.astimezone(CN_TZ).strftime("%Y-%m-%d %H:%M:%S")


def yaml_quote(value: str) -> str:
    # JSON double-quoted string is also a valid YAML scalar.
    return json.dumps(value, ensure_ascii=False)


def code_placeholder_preprocess(body: BeautifulSoup):
    placeholders = {}

    # Hexo highlight.js commonly emits figure.highlight + a gutter/code table.
    for idx, fig in enumerate(list(body.select("figure.highlight"))):
        classes = fig.get("class", [])
        lang = next((c for c in classes if c != "highlight"), "")
        code_node = fig.select_one("td.code pre") or fig.find("pre")
        if not code_node:
            continue

        line_nodes = code_node.select(".line")
        if line_nodes:
            code = "\n".join(x.get_text("", strip=False) for x in line_nodes)
        else:
            code = code_node.get_text("", strip=False)

        token = f"@@HEXORECOVER_CODE_{idx}@@"
        placeholders[token] = f"```{lang}\n{code.rstrip()}\n```"
        fig.replace_with(NavigableString(f"\n\n{token}\n\n"))

    # Plain pre/code blocks not covered above.
    for idx, pre in enumerate(list(body.find_all("pre")), start=len(placeholders)):
        code_node = pre.find("code")
        code = (code_node or pre).get_text("", strip=False)
        lang = ""
        if code_node:
            for cls in code_node.get("class", []):
                if cls.startswith("language-"):
                    lang = cls[len("language-"):]
                    break
        token = f"@@HEXORECOVER_CODE_{idx}@@"
        placeholders[token] = f"```{lang}\n{code.rstrip()}\n```"
        pre.replace_with(NavigableString(f"\n\n{token}\n\n"))

    return placeholders


def math_preprocess(body: BeautifulSoup):
    placeholders = {}
    counter = 0

    # MathJax v3 / KaTeX-style MathML often retains the original TeX
    # in <annotation encoding="application/x-tex">...</annotation>.
    for outer in list(body.select("mjx-container, .katex-display, span.katex")):
        if outer.parent and outer.parent.select_one(":scope > .katex-display") is outer:
            # Avoid processing inner katex twice where possible.
            pass
        ann = outer.find("annotation", attrs={"encoding": "application/x-tex"})
        if not ann:
            continue
        tex = ann.get_text("", strip=False)
        display = (
            outer.name == "mjx-container" and outer.get("display") == "true"
        ) or "katex-display" in outer.get("class", [])
        token = f"@@HEXORECOVER_MATH_{counter}@@"
        placeholders[token] = (
            f"$$\n{tex.strip()}\n$$" if display else f"${tex.strip()}$"
        )
        counter += 1
        outer.replace_with(NavigableString(token))

    # Older MathJax form.
    for script in list(body.find_all("script")):
        typ = script.get("type", "")
        if not typ.startswith("math/tex"):
            continue
        tex = script.get_text("", strip=False)
        display = "mode=display" in typ
        token = f"@@HEXORECOVER_MATH_{counter}@@"
        placeholders[token] = (
            f"$$\n{tex.strip()}\n$$" if display else f"${tex.strip()}$"
        )
        counter += 1
        script.replace_with(NavigableString(token))

    return placeholders


def normalize_images(body: BeautifulSoup, slug: str):
    for img in body.find_all("img"):
        src = img.get("data-src") or img.get("src") or ""
        src = html.unescape(src)

        # Convert deployed post asset URL back to post-local path.
        # /2026/07/21/paper-notes-SplaTAM/pipeline.png -> pipeline.png
        if f"/{slug}/" in src:
            src = src.split(f"/{slug}/", 1)[1]

        # Avoid accidentally restoring Fluid's lazy-load placeholder.
        if src.endswith("/img/loading.gif") and img.get("data-src"):
            src = img["data-src"]

        img["src"] = src
        for attr in ("data-src", "data-original"):
            img.attrs.pop(attr, None)


def reconstruct_one(html_path: Path, output_path: Path):
    text = html_path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(text, "html.parser")
    body = soup.select_one(".markdown-body")
    if body is None:
        raise RuntimeError(f".markdown-body not found in {html_path}")

    title = meta_content(soup, prop="og:title")
    date = published_local_time(soup)
    tags = [
        n.get("content", "").strip()
        for n in soup.find_all("meta", attrs={"property": "article:tag"})
        if n.get("content", "").strip()
    ]

    # Remove Fluid heading anchor "§".
    for a in body.select("a.header-anchor, a.anchorjs-link"):
        a.decompose()

    # Remove elements that are clearly not article source content.
    for bad in body.select("script, style"):
        bad.decompose()

    slug = output_path.stem
    normalize_images(body, slug)
    math_tokens = math_preprocess(body)
    code_tokens = code_placeholder_preprocess(body)

    markdown = md(
        str(body),
        heading_style="ATX",
        bullets="-",
        strip=["div"],
    )

    # Restore protected blocks.
    for token, value in {**math_tokens, **code_tokens}.items():
        markdown = markdown.replace(token, value)

    # Cleanup typical renderer/converter noise, but keep meaningful blank lines.
    markdown = markdown.replace("\r\n", "\n")
    markdown = re.sub(r"[ \t]+\n", "\n", markdown)
    markdown = re.sub(r"\n{4,}", "\n\n\n", markdown)
    markdown = markdown.strip() + "\n"

    front = ["---"]
    front.append(f"title: {yaml_quote(title or output_path.stem)}")
    if date:
        front.append(f"date: {date}")
    if tags:
        front.append("tags:")
        front.extend(f"  - {yaml_quote(tag)}" for tag in tags)
    front.append("---")
    front.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(front) + markdown, encoding="utf-8")


def main():
    if not RECOVERED_ROOT.exists():
        raise FileNotFoundError(RECOVERED_ROOT)
    if not ARCHIVE_ROOT.exists():
        raise FileNotFoundError(ARCHIVE_ROOT)
    NEW_ROOT.mkdir(parents=True, exist_ok=True)
    POSTS_ROOT.mkdir(parents=True, exist_ok=True)

    report = []

    print("\n=== 1. Copying 17 recovered original Markdown files ===")
    copied = 0
    for name in ORIGINAL_POSTS:
        src = find_unique(RECOVERED_ROOT, name)
        dst = POSTS_ROOT / name
        shutil.copy2(src, dst)
        copied += 1
        print(f"[COPY] {name}")
    report.append(f"Original Markdown copied: {copied}/17")

    # Hexo init creates this file; don't let it pollute the recovered set.
    hello = POSTS_ROOT / "hello-world.md"
    if hello.exists():
        hello.unlink()
        print("[CLEAN] removed default hello-world.md")

    print("\n=== 2. Restoring 4 original post images from deployed archive ===")
    assets_ok = 0
    for archive_rel, post_rel in ASSETS.items():
        src = ARCHIVE_ROOT / archive_rel
        dst = POSTS_ROOT / post_rel
        if not src.exists():
            raise FileNotFoundError(src)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        assets_ok += 1
        print(f"[ASSET] {post_rel}")
    report.append(f"Post images restored: {assets_ok}/4")

    print("\n=== 3. Reconstructing 6 missing Markdown files from deployed HTML ===")
    rebuilt = 0
    for name, archive_rel in RECONSTRUCT.items():
        src = ARCHIVE_ROOT / archive_rel
        dst = POSTS_ROOT / name
        if not src.exists():
            raise FileNotFoundError(src)
        reconstruct_one(src, dst)
        rebuilt += 1
        print(f"[REBUILD] {name}")
    report.append(f"Markdown reconstructed from HTML: {rebuilt}/6")

    md_files = sorted(POSTS_ROOT.glob("*.md"))
    report.append(f"Top-level post Markdown count: {len(md_files)}")
    report.append("")
    report.append("IMPORTANT:")
    report.append("- The 17 copied Markdown files are recovered source files.")
    report.append("- The 6 rebuilt Markdown files are semantic reconstructions from deployed HTML.")
    report.append("- Do NOT deploy yet. Audit formulas/code/images against the archived HTML first.")
    report.append("")
    report.append("Markdown files:")
    report.extend(f"- {p.name}" for p in md_files)

    report_path = NEW_ROOT / "_recovery_report.txt"
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")

    print("\n=== DONE ===")
    print(f"Markdown count: {len(md_files)} (expected 23)")
    print(f"Report: {report_path}")
    if len(md_files) != 23:
        print("[WARN] Markdown count is not 23. Stop and inspect before proceeding.")
    else:
        print("[OK] Content skeleton is complete. Do not deploy yet.")


if __name__ == "__main__":
    main()
