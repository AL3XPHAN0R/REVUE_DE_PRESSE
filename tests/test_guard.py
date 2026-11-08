"""Offline tests for the Stage 02 output guard: python -m unittest discover tests"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "stages" / "02_curate"))
from guard import clean, is_valid  # noqa: E402

ARCHIVE = ROOT / "stages" / "03_send" / "output"


class GuardOnBrokenArchives(unittest.TestCase):
    def test_nov7_analysis_is_trimmed_then_rejected(self):
        digest = clean((ARCHIVE / "2026-11-07.md").read_text(encoding="utf-8"))
        self.assertTrue(digest.startswith("📰 *Revue de presse"))
        self.assertNotIn("**Analysis:**", digest)
        self.assertFalse(is_valid(digest))  # header but zero 🔗 lines

    def test_nov8_request_for_text_is_rejected(self):
        digest = clean((ARCHIVE / "2026-11-08.md").read_text(encoding="utf-8"))
        self.assertFalse(digest.startswith("📰"))
        self.assertFalse(is_valid(digest))


class GuardOnGoodDigests(unittest.TestCase):
    def test_nov6_archive_is_accepted(self):
        digest = clean((ARCHIVE / "2026-11-06.md").read_text(encoding="utf-8"))
        self.assertTrue(is_valid(digest))

    def test_code_fence_is_unwrapped(self):
        body = "📰 *Revue de presse — x*\n" + "\n".join(f"🔗 https://e.com/{i}" for i in range(3))
        self.assertTrue(is_valid(clean("```\n" + body + "\n```")))

    def test_two_links_is_not_enough(self):
        body = "📰 *Revue de presse — x*\n🔗 https://e.com/1\n🔗 https://e.com/2"
        self.assertFalse(is_valid(clean(body)))


if __name__ == "__main__":
    unittest.main()
