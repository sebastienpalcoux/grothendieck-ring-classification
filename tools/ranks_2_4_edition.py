"""The 19 November manuscript edition, separate from frontier decisions.

Apply this small overlay after the existing publication/frontier renderers.
The historical generators and the higher-rank classification account retain
their own dates, inputs and scope.
"""
import json
from pathlib import Path
import re

DATE = "2026-11-19"

README_EDITION = """## Revised series: ranks 2, 3 and 4

**19 November 2026 · Grothendieck rings of complex fusion categories.**
Three independently readable papers classify the based rings without assuming a pivotal structure and prove sphericality in each rank.

| Rank | Paper | Source | Pages | Proof |
|---:|---|---|---:|---|
| 2 | [PDF](manuscripts/rank2.pdf) | [TeX](manuscripts/rank2.tex) | 3 | Computer-free; 2 based rings |
| 3 | [PDF](manuscripts/rank3.pdf) | [TeX](manuscripts/rank3.tex) | 10 | Computer-free; 5 based rings |
| 4 | [PDF](manuscripts/rank4.pdf) | [TeX](manuscripts/rank4.tex) | 50 | Computer-assisted spherical descent; 15 based rings |

[Submission sources and revision letter](manuscripts/hexagon/README.md) ·
[Rank-four proof and exact replay](manuscripts/rank4/README.md).
The rank-four paper proves sphericality before applying Dong–Palcoux–Plessis's pivotal classification. Its compact [verification package](supplements/rank4/sphericality/README.md) regenerates the 1,692-ring ordinary census and eliminates every remaining nonspherical candidate by local signed descent. Earlier rank-four computations remain available as historical evidence.

"""

MANUSCRIPTS_EDITION = """**19 November 2026: revised ranks 2–4 series.** The three current papers are *Grothendieck rings of complex fusion categories: rank 2*, *rank 3* and *rank 4*, by Sébastien Palcoux. They have 3, 10 and 50 pages. Ranks two and three are computer-free; rank four uses exact computation to prove sphericality before invoking the pivotal classification. [Submission sources and revision letter](hexagon/README.md) · [Revised rank-four verifier](../supplements/rank4/sphericality/README.md).

"""

PIVOTAL_RELATION = """## Related pivotal rank-four paper

Jingcheng Dong, Sébastien Palcoux and Arnaud Plessis,
[*Classifying Grothendieck rings of pivotal fusion categories of rank four*](https://github.com/sebastienpalcoux/pivotal-fusion-categories-rank-four/blob/main/manuscript.pdf):
the authors' revision of 9 November 2026 ·
[TeX](https://github.com/sebastienpalcoux/pivotal-fusion-categories-rank-four/blob/main/manuscript.tex) ·
[Code, data and certificates](https://github.com/sebastienpalcoux/pivotal-fusion-categories-rank-four) ·
[arXiv record](https://arxiv.org/abs/2609.33272).
This paper assumes pivotality and is separate from the atlas manuscripts
counted above. Its finite verification covers **8,977 rings: 8,962 exclusions
and 15 models**.

"""

VERIFY_EDITION = """## Revised ranks 2–4 series (19 November 2026)

Ranks two and three have computer-free proofs. The rank-four paper has a compact local sphericality replay, followed mathematically by the cited pivotal classification. After cloning the repository:

```sh
cd supplements/rank4/sphericality
python3 verify.py --manuscript ../../../manuscripts/rank4.tex
```

Use Python 3.10 or later, SymPy and a C++17 compiler. This freshly regenerates the 1,692-ring ordinary census, checks the local descent to zero nonspherical candidates, verifies the analytic estimates, and checks all fifteen model tensors and the printed model table. See the [complete scope](../supplements/rank4/sphericality/README.md) and [paper](../manuscripts/rank4.pdf).

## Earlier atlas and frontier verification

The following workflow retains its separate atlas and frontier scope. """

SUPPLEMENT_ROW = "| 4 | [Current guide](rank4/README.md) · [sphericality replay](rank4/sphericality/README.md) · [earlier replay](rank4/unrestricted/README.md) | Unrestricted classification via spherical descent and the pivotal theorem; local descent leaves zero nonspherical candidates. Earlier finite censuses are preserved. |"


def active(repo):
    """Historical snapshots without this edition retain their old rendering."""
    path = Path(repo) / "data/current_publication_revision.json"
    if not path.is_file():
        return False
    return json.loads(path.read_text()).get("manuscript_edition", {}).get("date") == DATE


def _replace_once(text, before, after):
    if text.count(before) != 1:
        raise ValueError("Unexpected manuscript-edition documentation: " + before[:80])
    return text.replace(before, after, 1)


def revise_document(name, text, repo):
    """Update only the edition's four generated entry points."""
    if not active(repo):
        return text
    if name == "README.md":
        if "## Revised series: ranks 2, 3 and 4\n" not in text:
            text = _replace_once(text, "# Grothendieck ring classification\n\n",
                                 "# Grothendieck ring classification\n\n" + README_EDITION)
    elif name == "manuscripts/README.md":
        if MANUSCRIPTS_EDITION not in text:
            text = _replace_once(text, "# Manuscripts\n\n", "# Manuscripts\n\n" + MANUSCRIPTS_EDITION)
            text = _replace_once(text,
                                 "Each current mathematical manuscript appears once, in rank order.",
                                 "The following inventory lists the atlas manuscripts once, in rank order.")
            inventory = json.loads((Path(repo) / "data/current_manuscript_page_counts.json").read_text())
            papers = [r for r in inventory["documents"] if r["kind"] == "mathematical_manuscript"]
            pages = sum(r["pages"] for r in papers)
            summary = (f"**{len(papers)} current mathematical manuscripts, {pages} pages.** "
                       "The revised ranks 2–4 series occupies 63 pages. Older rank-four articles "
                       "and verification guides remain in the [historical papers directory]"
                       "(rank4/papers/README.md); they are not dependencies of the revised sphericality verifier.")
            text, count = re.subn(r"\*\*\d+ mathematical manuscripts, [^\n]+", summary, text)
            if count != 1:
                raise ValueError("Expected one historical manuscript-count paragraph")
            text = _replace_once(text, "## Scope\n\n", PIVOTAL_RELATION + "## Scope\n\n")
    elif name == "docs/VERIFY.md":
        if "## Revised ranks 2–4 series (19 November 2026)\n" not in text:
            text = _replace_once(text, "After cloning the classification repository:\n\n",
                                 VERIFY_EDITION + "After cloning the classification repository:\n\n")
    elif name == "supplements/README.md":
        text, count = re.subn(r"^\| 4 \|[^\n]+$", SUPPLEMENT_ROW, text, flags=re.M)
        if count != 1:
            raise ValueError("Expected one rank-four supplement row")
    else:
        return text
    return text.rstrip("\n") + "\n\n"
