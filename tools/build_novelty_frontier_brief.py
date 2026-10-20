#!/usr/bin/env python3
"""Rebuild the dated, one-page novelty/frontier brief using ReportLab.

Run from any directory with Python 3 and reportlab installed. The default
output is docs/New_category_candidates_and_open_cases.pdf. DejaVu Sans fonts
are required (Debian/Ubuntu package fonts-dejavu-core); --font-dir overrides
their location. Invariant PDF mode makes repeated builds byte-identical.

The seven provisional construction descriptions are preserved from the
17 October brief. Current open IDs and M5 counts are checked against the
published ledgers so a changed frontier cannot silently produce stale prose.
"""
from argparse import ArgumentParser
from pathlib import Path
import hashlib
import json
from xml.sax.saxutils import escape
from collections import Counter
from rank7_publication import PUBLICATION_DATE_LONG

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


DATE = PUBLICATION_DATE_LONG
REPO = Path(__file__).resolve().parents[1]
GITHUB = "https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/"
OLD = GITHUB + "36cdec23cd351f2e1a6446f4325174bf80c6637e/"
CURRENT = GITHUB + "main/"
INK = colors.HexColor("#17334A")
TEAL = colors.HexColor("#087580")
MUTED = colors.HexColor("#52677C")
PALE = colors.HexColor("#F1F6F8")
RULE = colors.HexColor("#CBD9E2")
AMBER = colors.HexColor("#966008")
OPEN_BG = colors.HexColor("#FFF6E8")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def link(label, url, color="#087580"):
    return '<a href="{}" color="{}">{}</a>'.format(escape(url, {'"': '&quot;'}), color, label)


def verify_frontier(repo):
    summary = json.loads((repo / "supplements/rank7/output/m5/summary.json").read_text())
    require(summary["new_rings"] == 5805, "Unexpected M5 census size")
    rank7 = json.loads((repo / "supplements/rank7/output/rank7_ledger.json").read_text())
    counts = Counter(r['status'] for r in rank7 if r['multiplicity'] == 5)
    require(all(summary['new_status_counts'].get(key, 0) == counts.get(key, 0)
                for key in set(summary['new_status_counts']) | set(counts)),
            'Summary and rank-seven status counts differ')
    require([r["id"] for r in rank7 if r["status"] == "unresolved"] == summary['unresolved_ids'],
            "Summary and rank-seven ledger differ")
    realized = [r["id"] for r in rank7 if r["multiplicity"] == 5 and r["status"] == "unitarily_realized"]
    require(realized == ["R7_5_5678"], "Update the known-model description")
    rank6 = json.loads((repo / "supplements/rank6/data/decisions.json").read_text())
    require([r["id"] for r in rank6 if r["status"] == "unresolved"] == ["R6_4_155", "R6_8_1660"],
            "Update the dated rank-six frontier")
    return summary


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--font-dir", type=Path, default=Path("/usr/share/fonts/truetype/dejavu"))
    args = parser.parse_args()
    repo = args.repo.resolve()
    summary = verify_frontier(repo)
    rank7_ids = summary['unresolved_ids']
    frontier = 2 + len(rank7_ids)
    output = args.output or repo / "docs/New_category_candidates_and_open_cases.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    for name, filename in (("Brief", "DejaVuSans.ttf"), ("Brief-Bold", "DejaVuSans-Bold.ttf")):
        path = args.font_dir / filename
        require(path.is_file(), "Missing DejaVu font: " + str(path))
        pdfmetrics.registerFont(TTFont(name, str(path)))
    pdfmetrics.registerFontFamily("Brief", normal="Brief", bold="Brief-Bold")
    W, H = A4
    margin = 38
    width = W - 2 * margin
    c = canvas.Canvas(str(output), pagesize=A4, invariant=1, pageCompression=1)
    c.setTitle("Potentially new constructions and unresolved cases - " + DATE)
    c.setAuthor("AI-assisted research project of Sebastien Palcoux")
    c.setSubject(f"Seven provisional novelty candidates; {frontier} open fusion rings; known AGL(1,7) model")
    body = ParagraphStyle("body", fontName="Brief", fontSize=9.05, leading=12.0,
                          textColor=INK, alignment=TA_LEFT)
    small = ParagraphStyle("small", parent=body, fontSize=8.1, leading=10.6, textColor=MUTED)
    compact = ParagraphStyle("compact", parent=body, fontSize=8.75, leading=11.5)
    ids_style = ParagraphStyle("ids", parent=body, fontSize=8.5, leading=12.8)

    def para(text, x, top, w, style=body):
        p = Paragraph(text, style)
        _, h = p.wrap(w, H)
        p.drawOn(c, x, top - h)
        return top - h

    def heading(text, y):
        c.setFillColor(TEAL)
        c.setFont("Brief-Bold", 10.5)
        c.drawString(margin, y, text)
        return y - 13

    def panel(text, top, bg=PALE, stripe=None, style=body):
        p = Paragraph(text, style)
        _, h = p.wrap(width - 22, H)
        box_h = h + 14
        c.setFillColor(bg)
        c.roundRect(margin, top - box_h, width, box_h, 5, fill=1, stroke=0)
        if stripe:
            c.setFillColor(stripe)
            c.rect(margin, top - box_h + 5, 2.3, box_h - 10, fill=1, stroke=0)
        p.drawOn(c, margin + 11, top - 7 - h)
        return top - box_h

    y = H - 39
    c.setFillColor(INK)
    c.setFont("Brief-Bold", 20)
    c.drawString(margin, y, "Potentially new constructions")
    y = para("Low rank Grothendieck rings · Novelty shortlist and unresolved cases · " + DATE,
             margin, y - 10, width, small) - 14
    y = panel("<b>To the best of our current knowledge, these seven constructions are promising candidates "
              "for new tensor categories.</b> Their novelty up to tensor equivalence remains subject to independent verification.", y) - 17
    y = heading("Reported constructions to examine for novelty", y)
    y = para("m denotes maximum fusion multiplicity. Click a census ID for its construction source.",
             margin, y, width, small) - 7

    rows = [
        ("R6_4_249", 6, 4, "manuscripts/rank6/papers/chapters/06.tex",
         "<b>Sign-swap equivariantization</b> of the diagonal-fermion quotient of two identical half-E<sub>6</sub> categories. Known inputs: " + link("Aasen-Lake-Walker", "https://arxiv.org/abs/1709.01941") + "."),
        ("R6_4_322", 6, 4, "manuscripts/rank6/papers/chapters/06.tex",
         "<b>Mixed diagonal-fermion quotient</b> of Ad(E<sub>6</sub>) and PSU(2)<sub>6</sub>. Both input categories are already known."),
        ("R6_6_1712", 6, 6, "manuscripts/rank6/papers/chapters/06.tex",
         "<b>Relative Fibonacci center of TT<sub>3</sub>.</b> The input TT<sub>3</sub> is the known dual even part of 2D2; see " + link("Edie-Michell, Definition 2.5", "https://arxiv.org/html/1904.08909v2") + "."),
        ("R7_4_35", 7, 4, "evidence/unified_20261016/rank7/R35_INVERSION_CONSTRUCTION.md",
         "<b>Inversion descent and reflection Morita dual</b> of an orbifold of NG(C<sub>4</sub> × C<sub>4</sub>,16). Input: " + link("Yu-Zhang", "https://arxiv.org/abs/2412.20763") + "."),
        ("R7_4_2665", 7, 4, "evidence/unified_20261016/rank7/R2665_INVERSION_CONSTRUCTION.md",
         "<b>Analogous inversion/Morita construction</b> from NG(C<sub>16</sub>,16), with different invertibles and duality. Input: Budinski (2021)."),
        ("R8_2_37", 8, 2, "evidence/unified_20261016/rank8/R37_CONSTRUCTION.md",
         "<b>Nonsplit C<sub>2</sub>-extension of 2D2,</b> with an odd invertible a satisfying a² = g. Uses " + link("Grossman-Izumi-Snyder", "https://arxiv.org/abs/2201.11901") + " and Grossman."),
        ("R8_2_575", 8, 2, "evidence/upper_residual_20261002b/r8_integral/r575/PROOF.md",
         "<b>Explicit " + link("Davydov-Runkel", "https://arxiv.org/abs/1207.3611") + " extension</b> of Kashina’s self-dual 16-dimensional Hopf algebra. Simple dimensions: (1,1,1,1,2,2,2,4)."),
    ]
    label_w = 110
    for i, (rid, rank, multiplicity, source, text) in enumerate(rows):
        p = Paragraph(text, body)
        _, h = p.wrap(width - label_w - 17, H)
        row_h = max(35, h + 13)
        c.setFillColor(PALE if i % 2 == 0 else colors.white)
        c.rect(margin, y - row_h, width, row_h, fill=1, stroke=0)
        para("<b>" + link(rid, OLD + source) + "</b>", margin + 9, y - 6, label_w - 12)
        para(f"Rank {rank} · m = {multiplicity}", margin + 9, y - 20, label_w - 12, small)
        p.drawOn(c, margin + label_w + 8, y - 6 - h)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.45)
        c.line(margin, y - row_h, W - margin, y - row_h)
        y -= row_h

    y -= 17
    y = heading("Known model added in the rank-seven extension", y)
    y = para("<b>" + link("R7_5_5678", CURRENT + "evidence/rank7_m5_20261019/models/frobenius42_match.json") +
             " · Rank 7 · m = 5.</b> Rep(AGL(1,7)) = Rep(C<sub>7</sub> ⋊ C<sub>6</sub>), of global dimension 42. "
             "The full fusion tensor is verified. This is a known representation category, not an additional novelty candidate.",
             margin, y, width, compact) - 17
    y = heading(f"OPEN: {frontier} fusion rings with no established categorification", y)
    y = panel("<b>" + link("R6_4_155", OLD + "supplements/rank6/research/frontier/R6_4_155/README.md", "#966008") +
              " · Rank 6 · multiplicity 4.</b> Generalized near-group ring R′(4): four invertibles forming C<sub>2</sub> × C<sub>2</sub>, "
              "and two mutually dual noninvertibles of dimension 4 + 3√2. The ring already appears in " +
              link("Meng-Yu, Theorem 1.1", "https://arxiv.org/html/2608.06064v1", "#966008") + ".",
              y, OPEN_BG, AMBER, compact) - 6
    y = panel("<b>" + link("R6_8_1660", OLD + "supplements/rank6/research/frontier/R6_8_1660/README.md", "#966008") +
              " · Rank 6 · multiplicity 8.</b> Self-dual ring containing an Ising fusion subring. A further simple X "
              "has dimension 3 + 2√2 + 2√3 + √6 and satisfies X² = 1 + [3(1 + g) + 4σ]X, where σ² = 1 + g.",
              y, OPEN_BG, AMBER, compact) - 9
    y = para(f"<b>Rank 7 · multiplicity 5: {len(rank7_ids)} unresolved {'ring' if len(rank7_ids)==1 else 'rings'}.</b> "
             f"Of all 5,805 new rings, {summary['new_status_counts']['excluded']:,} are excluded and one is realized. "
             + (("The remaining census ID is:" if len(rank7_ids)==1 else "The remaining census IDs are:") if rank7_ids else "Every supplied ring in this band has a recorded decision."),
             margin, y, width, compact) - 5
    lines = []
    for start in range(0, len(rank7_ids), 5):
        lines.append(" · ".join(link(rid, CURRENT + "supplements/rank7/output/m5/survivors.json")
                                for rid in rank7_ids[start:start + 5]))
    if lines:
        y = para("<br/>".join(lines), margin + 8, y, width - 16, ids_style) - 7
    y = para(f"All {frontier} remaining cases are open for general complex categorification; no positive model or complete exclusion is established. " +
             link("Exact fusion data", CURRENT + "data/remaining_cases.py") + ".", margin, y, width, small)
    require(y >= 77, f"Brief content overlaps footer: lowest text y={y:.1f}")

    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(margin, 56, W - margin, 56)
    para("<b>AI-generated research · independent verification pending.</b><br/>"
         "Independent human verification and Lean formalization remain pending. Please treat the claims with caution.",
         margin, 48, width, small)
    c.showPage()
    c.save()
    raw = output.read_bytes()
    print(json.dumps({"output": str(output), "pages": 1, "frontier": frontier,
                      "novelty_candidates": 7, "known_new_models": 1,
                      "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}))


if __name__ == "__main__":
    main()
