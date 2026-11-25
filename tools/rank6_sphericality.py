"""Add the standalone sphericality paper to the repository reading routes."""
from pathlib import Path
import re


PAPER = "manuscripts/rank6/sphericality/Sphericality_in_Rank_Six"
CHECKS = "supplements/rank6/sphericality/README.md"
ROOT_INDEX = "README.md"
MANUSCRIPT_INDEX = "manuscripts/README.md"
SUPPLEMENT_INDEX = "supplements/README.md"


def revise_document(name, text, repo):
    if name not in (ROOT_INDEX, MANUSCRIPT_INDEX, SUPPLEMENT_INDEX):
        return text
    if not (Path(repo) / (PAPER + ".tex")).is_file():
        return text
    if "rank6/sphericality/Sphericality_in_Rank_Six.pdf)" in text:
        return text

    if name == SUPPLEMENT_INDEX:
        heading = "Restore the source datasets with"
        paragraph = (
            "The [rank-six sphericality supplement](rank6/sphericality/README.md) "
            "reproduces the finite arithmetic checks in "
            f"[*Spherical structures on fusion categories of rank six*](../{PAPER}.pdf).\n\n"
        )
    else:
        if name == ROOT_INDEX:
            heading = "## Revised series:"
            paper, checks = PAPER, CHECKS
        else:
            heading = "## Related pivotal rank-four paper"
            paper, checks = PAPER.removeprefix("manuscripts/"), "../" + CHECKS
            text = re.sub(r"(\*\*\d+) current mathematical manuscripts, (\d+ pages\.\*\*)",
                          r"\1 atlas classification manuscripts, \2", text, count=1)
        paragraph = (
            "## Spherical structures in rank six\n\n"
            f"[*Spherical structures on fusion categories of rank six*]({paper}.pdf) "
            "proves that every complex fusion category of rank six admits a spherical structure. "
            "The theorem holds at every fusion multiplicity.\n\n"
            f"[Single-file TeX source]({paper}.tex) · [Arithmetic checks and certificates]({checks})\n\n"
        )
    if text.count(heading) != 1:
        raise ValueError(f"Could not locate the rank-six sphericality reading route in {name}")
    return text.replace(heading, paragraph + heading, 1)
