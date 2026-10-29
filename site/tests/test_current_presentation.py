"""Regression checks for a single current, reproducible reader account."""
from pathlib import Path
import importlib.util
import tempfile
import unittest
import json

SITE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("current_presentation", SITE / "current_presentation.py")
presentation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(presentation)


class CurrentPresentationTests(unittest.TestCase):
    def test_consolidation_is_idempotent_and_keeps_current_routes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "dist").mkdir()
            for name in ("index.html", "review.html", "unresolved.html"):
                (root / "dist" / name).write_bytes((SITE / "dist" / name).read_bytes())
            (root/'dist/downloads').mkdir(exist_ok=True)
            (root/'dist/downloads/current_manuscript_page_counts.json').write_text(json.dumps({'totals':{'mathematical_manuscript':675,'mathematical_manuscripts_and_guides':693,'all_distinct_documents':700}}))
            presentation.apply(root)
            first = {p.name: p.read_bytes() for p in (root / "dist").glob("*.html")}
            presentation.apply(root)
            self.assertEqual(first, {p.name: p.read_bytes() for p in (root / "dist").glob("*.html")})
            home = (root / "dist/index.html").read_text()
            review = (root / "dist/review.html").read_text()
            self.assertEqual(home.count('id="frontier-update"'), 1)
            self.assertNotIn('id="correctness-update"', home)
            self.assertNotIn("Earlier manuscript inventory", home)
            self.assertIn("Current classification · 6 open questions", review)
            self.assertIn("4,404 general exclusions", review)
            self.assertIn("3,508 exclusions", review)
            self.assertNotIn("Seven rings remain open", review)
            self.assertNotIn("prepublication-review-2026-10-27.pdf", review)
            for route in ("./papers/frontier.pdf", "./downloads/current_remaining_cases.py",
                          "./downloads/Fusion-Ring-Frontier-Proofs-and-Checks.zip"):
                self.assertIn(route, review)
            self.assertIn(presentation.PROOFS, review)
            for identifier in ("R6_4_155", "R6_8_1660", "R8_3_928", "R8_3_941", "R8_3_1154", "R9_2_137"):
                self.assertIn("case.html?id=" + identifier, review)


if __name__ == "__main__":
    unittest.main()
