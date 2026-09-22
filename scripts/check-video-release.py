#!/usr/bin/env python3
"""检查静态作品集中的同源视频、封面和平台单文件上限。"""

from __future__ import annotations

import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class VideoParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.videos: list[dict[str, object]] = []
        self.current: dict[str, object] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name.lower(): (value if value is not None else True) for name, value in attrs}
        if tag.lower() == "video":
            self.current = {"attrs": values, "sources": []}
            self.videos.append(self.current)
        elif tag.lower() == "source" and self.current is not None:
            sources = self.current["sources"]
            assert isinstance(sources, list)
            sources.append(values)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "video":
            self.current = None


def local_path(root: Path, value: str) -> Path | None:
    parts = urlsplit(value)
    if parts.scheme or parts.netloc or value.startswith("//"):
        return None
    relative = unquote(parts.path).lstrip("/")
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def check_site(root: Path, max_bytes: int) -> list[str]:
    errors: list[str] = []
    html_files = sorted(root.rglob("*.html"))
    if not html_files:
        return ["未找到 HTML 文件"]

    video_count = 0
    for html_file in html_files:
        parser = VideoParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for index, video in enumerate(parser.videos, start=1):
            video_count += 1
            label = f"{html_file.relative_to(root)} 的第 {index} 个视频"
            attrs = video["attrs"]
            sources = video["sources"]
            assert isinstance(attrs, dict) and isinstance(sources, list)

            for required in ("controls", "playsinline"):
                if required not in attrs:
                    errors.append(f"{label} 缺少 {required}")
            if attrs.get("preload") != "metadata":
                errors.append(f"{label} 应设置 preload=\"metadata\"")

            poster = attrs.get("poster")
            if not isinstance(poster, str):
                errors.append(f"{label} 缺少 poster")
            else:
                poster_path = local_path(html_file.parent, poster)
                if poster_path is None:
                    errors.append(f"{label} 的封面必须使用同源相对路径：{poster}")
                elif not poster_path.is_file() or poster_path.stat().st_size == 0:
                    errors.append(f"{label} 的封面不存在或为空：{poster}")

            candidates = []
            if isinstance(attrs.get("src"), str):
                candidates.append({"src": attrs["src"], "type": attrs.get("type")})
            candidates.extend(sources)
            if not candidates:
                errors.append(f"{label} 缺少视频源")
                continue

            for source in candidates:
                src = source.get("src")
                if not isinstance(src, str):
                    errors.append(f"{label} 存在没有 src 的 source")
                    continue
                path = local_path(html_file.parent, src)
                if path is None:
                    errors.append(f"{label} 的视频必须使用同源相对路径：{src}")
                    continue
                if not path.is_file():
                    errors.append(f"{label} 的视频文件不存在：{src}")
                    continue
                size = path.stat().st_size
                if size > max_bytes:
                    errors.append(f"{label} 超过单文件上限：{size} > {max_bytes} 字节")
                header = path.read_bytes()[:12]
                if len(header) < 8 or header[4:8] != b"ftyp":
                    errors.append(f"{label} 不是可识别的 MP4：{src}")
                if source.get("type") not in (None, "video/mp4"):
                    errors.append(f"{label} 的 type 应为 video/mp4：{src}")

    if video_count == 0:
        errors.append("HTML 中没有找到 video 元素")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("public_dir", type=Path, help="最终静态发布目录")
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=25_000_000,
        help="平台单文件上限，默认 25000000 字节；部署前按平台实际限制调整",
    )
    args = parser.parse_args()
    root = args.public_dir.resolve()
    if not root.is_dir():
        print(f"FAIL: 发布目录不存在：{root}")
        return 2

    errors = check_site(root, args.max_bytes)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: 视频发布检查通过，单文件上限 {args.max_bytes} 字节。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
