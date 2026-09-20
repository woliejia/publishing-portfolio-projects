#!/usr/bin/env python3
"""Build a deterministic, vendor-neutral skill ZIP with SKILL.md at its root."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parent.parent
FILES = (
    "SKILL.md",
    "LICENSE",
    "references/esa-pages.md",
    "references/platform-compatibility.md",
    "references/verification.md",
    "scripts/check-portability.mjs",
    "scripts/check-release.mjs",
)


def build(output: Path) -> str:
    missing = [relative for relative in FILES if not (ROOT / relative).is_file()]
    if missing:
        raise SystemExit(f"Missing package files: {', '.join(missing)}")

    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in FILES:
            data = (ROOT / relative).read_bytes()
            entry = ZipInfo(relative, date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            archive.writestr(entry, data)

    return hashlib.sha256(output.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=ROOT / "dist" / "publishing-portfolio-projects-universal.zip",
    )
    args = parser.parse_args()
    output = args.output.resolve()
    digest = build(output)
    print(f"PASS {output}")
    print(f"SHA256 {digest}")


if __name__ == "__main__":
    main()
