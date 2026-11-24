"""The 24 November rank-five edition, after the ranks-two-through-four overlay.

Only current reading routes and classification summaries change. Historical
censuses, higher-rank decisions and research-status disclosures retain their
own scope and text.
"""
import json
from pathlib import Path
import re

from ranks_2_4_edition import MANUSCRIPTS_EDITION, README_EDITION

DATE = "2026-11-24"
TARGETS = {
    "README.md", "manuscripts/README.md", "docs/VERIFY.md",
    "supplements/README.md", "docs/PROJECT_GUIDE.md", "docs/PROVENANCE.md",
}

VERIFY_EDITION = """## Rank-five sharp classification (24 November 2026)

The current rank-five paper proves sphericality and Galois pseudo-unitarity
and classifies all seventeen based rings, without an initial pivotality
assumption. From the repository root:

```sh
python3 -m pip install sympy==1.14.0 numpy==2.3.5
cd supplements/rank5/sharp
python3 verify.py
```

Use Python 3.12 and a C++17 `g++` compiler with OpenMP support. Run ordinary
Python with assertions enabled, without `-O`. The replay checks eighteen
structural calculations, regenerates 269 rings of multiplicity at most four,
retains 114 within the sharp dimension bound, and verifies 97 exclusions
and seventeen model identifications. The categorical reductions and finite
search bounds are proved in the paper; matching model tensors does not
replace the cited categorical constructions. See the
[reading guide](../manuscripts/rank5/README.md),
[paper](../manuscripts/rank5.pdf) and
[exact replay and optional checks](../supplements/rank5/sharp/README.md).

"""

SUPPLEMENT_ROW = "| 5 | [Current reading guide](../manuscripts/rank5/README.md) · [sharp-bound replay](rank5/sharp/README.md) · [historical census and replay](rank5/README.md) | Unrestricted: 17 rings; sphericality and Galois pseudo-unitarity. Sharp bounds μ ≤ 4 and FPdim ≤ 48 + 24√3. The earlier census through 20 retains 40,999 inputs, 40,982 exclusions and 17 models. |"

PROJECT_EDITION = """## Rank-five classification (24 November 2026)

The current series gives unrestricted classifications at ranks 2–5, without
assuming a pivotal structure. At rank five, every complex fusion category
has a pseudo-unitary Galois conjugate and admits a spherical structure.
Exactly seventeen based rings occur, each with a unitary realization; the
sharp bounds are μ ≤ 4 and FPdim ≤ 48 + 24√3.

Start with the [rank-five reading guide](../manuscripts/rank5/README.md),
[canonical paper](../manuscripts/rank5.pdf) and
[exact replay](../supplements/rank5/sharp/README.md).
The [earlier census through multiplicity twenty](../supplements/rank5/README.md)
remains separate historical evidence: 40,999 inputs, 40,982 exclusions and
17 models. Its original counts and records are preserved.

"""


def active(repo):
    """Do not change historical snapshots without the exact edition gate."""
    path = Path(repo) / "data/current_publication_revision.json"
    if not path.is_file():
        return False
    return json.loads(path.read_text()).get("rank5_edition", {}).get("date") == DATE


def _replace_once(text, before, after):
    if text.count(before) != 1:
        raise ValueError("Unexpected rank-five edition documentation: " + before[:80])
    return text.replace(before, after, 1)


def _pages(repo):
    inventory = json.loads(
        (Path(repo) / "data/current_manuscript_page_counts.json").read_text())
    rows = [r for r in inventory["documents"]
            if r["path"] == "manuscripts/rank5.pdf"
            and r["kind"] == "mathematical_manuscript"]
    if len(rows) != 1 or type(rows[0]["pages"]) is not int or rows[0]["pages"] < 1:
        raise ValueError("Expected one current canonical rank-five page count")
    return rows[0]["pages"]


def _readme_edition(pages):
    text = README_EDITION.replace(
        "ranks 2, 3 and 4", "ranks 2, 3, 4 and 5").replace(
        "19 November 2026", "24 November 2026").replace(
        "Three independently readable papers", "Four independently readable papers")
    row = (f"\n| 5 | [PDF](manuscripts/rank5.pdf) | [TeX](manuscripts/rank5.tex) | {pages} | "
           "Sphericality and Galois pseudo-unitarity; 17 based rings |")
    text = _replace_once(text, "\n\n[Submission sources", row + "\n\n[Submission sources")
    text = text.replace("[Submission sources and revision letter]",
                        "[Series submission sources and revision letters]")
    return text + """The rank-five paper proves the sharp bounds **μ ≤ 4** and
**FPdim ≤ 48 + 24√3** and gives a unitary realization of every listed ring.
[Rank-five reading guide](manuscripts/rank5/README.md) ·
[Exact structural and classification replay](supplements/rank5/sharp/README.md).

"""


def revise_document(name, text, repo):
    """Apply the current edition after all earlier documentation overlays."""
    if name not in TARGETS or not active(repo):
        return text
    if name == "README.md":
        if "## Revised series: ranks 2, 3, 4 and 5\n" in text:
            return text
        text = _replace_once(text, README_EDITION, _readme_edition(_pages(repo)))
        text = _replace_once(text,
            "Ranks **2–4 have unrestricted classification claims**, with exactly **15 rank-four rings**.\n"
            "Higher ranks have the explicit multiplicity bounds below.",
            "Ranks **2–5 have unrestricted classification claims**, including **15 rank-four rings** "
            "and **17 rank-five rings**.\nHigher ranks retain the explicit census ranges below.")
        text = _replace_once(text,
            "| 5 | Through 20 | **Complete through 20** | Through 20: 40,982 excluded, 17 realized, 0 unresolved. |",
            "| 5 | Through 20 (historical census) | **Unrestricted theorem** | Exactly 17 rings, "
            "each with a unitary realization; sphericality and Galois pseudo-unitarity; "
            "sharp bounds μ ≤ 4 and FPdim ≤ 48 + 24√3. |")
        text = _replace_once(text, "## Read, inspect, reproduce\n\n",
            "The [earlier rank-five census through multiplicity twenty](supplements/rank5/README.md) "
            "is preserved separately: 40,999 inputs, 40,982 exclusions and 17 models.\n\n"
            "## Read, inspect, reproduce\n\n")
        text = _replace_once(text,
            "| **Rank-four theorem** | [Unrestricted classification and reading guide](manuscripts/rank4/README.md) |\n",
            "| **Rank-four theorem** | [Unrestricted classification and reading guide](manuscripts/rank4/README.md) |\n"
            "| **Rank-five theorem** | [Unrestricted classification and reading guide](manuscripts/rank5/README.md) "
            "· [Exact replay](supplements/rank5/sharp/README.md) |\n")
    elif name == "manuscripts/README.md":
        long_label = "| Grothendieck rings of complex fusion categories: rank 5 |"
        if long_label in text:
            text = _replace_once(text, long_label, "| Rank five |")
        if "**24 November 2026: revised ranks 2–5 series.**" in text:
            return text
        pages = _pages(repo)
        edition = (
            "**24 November 2026: revised ranks 2–5 series.** The four current papers are "
            "*Grothendieck rings of complex fusion categories: rank 2*, *rank 3*, *rank 4* "
            f"and *rank 5*. They have 3, 10, 50 and {pages} pages. "
            "All four classify based rings without assuming a pivotal structure and prove sphericality. "
            "Ranks two and three are computer-free; ranks four and five use exact computations. "
            "Rank five also proves Galois pseudo-unitarity and the sharp bounds μ ≤ 4 and "
            "FPdim ≤ 48 + 24√3. [Series submission sources and revision letters](hexagon/README.md) · "
            "[Rank-four verifier](../supplements/rank4/sphericality/README.md) · "
            "[Rank-five reading guide](rank5/README.md) · "
            "[Rank-five exact replay](../supplements/rank5/sharp/README.md).\n\n")
        text = _replace_once(text, MANUSCRIPTS_EDITION, edition)
        text = _replace_once(text,
            "The revised ranks 2–4 series occupies 63 pages.",
            f"The revised ranks 2–5 series occupies {63 + pages} pages.")
        text = _replace_once(text,
            "they are not dependencies of the revised sphericality verifier.",
            "they are not dependencies of the revised sphericality verifier. "
            "The earlier rank-five [19-page census paper](rank5/papers/manuscript.pdf) "
            "([TeX](rank5/papers/manuscript.tex)) and "
            "[4-page verification guide](rank5/papers/verification_guide.pdf) "
            "([TeX](rank5/papers/verification_guide.tex)) are also historical "
            "and excluded from the current-paper totals.")
        text = _replace_once(text,
            "Ranks 2–4 have unrestricted classification claims. Ranks 5–8 use explicit census bounds 20, 9, 5 and 3.",
            "Ranks 2–5 have unrestricted classification claims. Ranks 6–8 use explicit census bounds 9, 5 and 3.")
    elif name == "docs/VERIFY.md":
        if "## Rank-five sharp classification (24 November 2026)\n" in text:
            return text
        heading = "## Revised ranks 2–4 series (19 November 2026)\n"
        text = _replace_once(text, heading, VERIFY_EDITION + heading)
    elif name == "supplements/README.md":
        if SUPPLEMENT_ROW in text:
            return text
        text, count = re.subn(r"^\| 5 \|[^\n]+$", lambda _: SUPPLEMENT_ROW, text, flags=re.M)
        if count != 1:
            raise ValueError("Expected one rank-five supplement row")
    elif name == "docs/PROJECT_GUIDE.md":
        if "## Rank-five classification (24 November 2026)\n" in text:
            return text.rstrip("\n") + "\n"
        text = _replace_once(text, "## Read the project\n\n",
            "## Read the project\n\n"
            "- [Current ranks 2–5 series](../manuscripts/README.md) gives four unrestricted "
            "classifications without an initial pivotality assumption.\n"
            "- [Rank-five paper](../manuscripts/rank5.pdf), "
            "[reading guide](../manuscripts/rank5/README.md) and "
            "[exact replay](../supplements/rank5/sharp/README.md) provide the current rank-five route.\n")
        text = _replace_once(text, "## Two complementary repositories\n\n",
            PROJECT_EDITION + "## Two complementary repositories\n\n")
        return text.rstrip("\n") + "\n"
    elif name == "docs/PROVENANCE.md":
        if "The current [rank-five paper](../manuscripts/rank5.pdf) and\n" in text:
            return text.rstrip("\n") + "\n"
        text = _replace_once(text,
            "| 5 | Through 20 | Complete: 17 models and 40,982 exclusions. |",
            "| 5 | Through 20 (historical census) | Unrestricted: 17 based rings, "
            "each with a unitary realization; sphericality and Galois pseudo-unitarity. "
            "Sharp bounds μ ≤ 4 and FPdim ≤ 48 + 24√3. |")
        text = _replace_once(text,
            "| 8 | Through 2 | Complete: 77 models and 896 exclusions. |\n\n",
            "| 8 | Through 2 | Complete: 77 models and 896 exclusions. |\n\n"
            "The current [rank-five paper](../manuscripts/rank5.pdf) and\n"
            "[sharp replay](../supplements/rank5/sharp/README.md) use eighteen structural\n"
            "checks and a 269-ring census, reduced by the sharp dimension bound to\n"
            "114 rings: 97 exclusions and seventeen models. The multiplicity-twenty\n"
            "ledger below remains a separate historical computation with 40,999 inputs\n"
            "and 40,982 exclusions; its hashes and source identities are unchanged.\n\n")
        return text.rstrip("\n") + "\n"
    return text.rstrip("\n") + "\n\n"
