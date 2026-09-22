import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("check-video-release.py")


class VideoReleaseCheckTests(unittest.TestCase):
    def make_site(self, video_size: int = 32, source: str = "assets/demo.mp4") -> Path:
        root = Path(tempfile.mkdtemp())
        (root / "assets").mkdir()
        prefix = b"\x00\x00\x00\x18ftypisom"
        (root / "assets" / "demo.mp4").write_bytes((prefix + b"0" * video_size)[:video_size])
        (root / "assets" / "poster.jpg").write_bytes(b"\xff\xd8\xff\xe0poster")
        (root / "index.html").write_text(
            f'<video controls preload="metadata" playsinline poster="assets/poster.jpg">'
            f'<source src="{source}" type="video/mp4"></video>',
            encoding="utf-8",
        )
        return root

    def run_check(self, root: Path, max_bytes: int = 100) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(root), "--max-bytes", str(max_bytes)],
            text=True,
            capture_output=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )

    def test_accepts_same_origin_video_with_poster_and_controls(self):
        result = self.run_check(self.make_site())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_video_over_platform_limit(self):
        result = self.run_check(self.make_site(video_size=101))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("超过单文件上限", result.stdout)

    def test_rejects_external_video_source(self):
        result = self.run_check(self.make_site(source="https://video.example/demo.mp4"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("必须使用同源相对路径", result.stdout)


if __name__ == "__main__":
    unittest.main()
