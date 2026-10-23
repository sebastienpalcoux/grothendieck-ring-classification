"""Keep the repository entry point concise and retain its full research guide."""
import re

ATLAS = 'https://sebastienpalcoux.github.io/grothendieck-ring-classification/'


def table_after(text, heading):
    section = text.split(heading, 1)[1]
    lines = section.splitlines()
    first = next(i for i, line in enumerate(lines) if line.startswith('|'))
    result = []
    for line in lines[first:]:
        if not line.startswith('|'):
            break
        result.append(line)
    return '\n'.join(result)


def reorganize(full):
    """Move every original paragraph/link to a guide; extract the key tables."""
    counts = table_after(full, '## Grothendieck rings · known realizations at each exact multiplicity')
    scope = table_after(full, '## Classification · what is decided?')
    # The source guide lives one directory below README.md. Internal anchors
    # remain local to the guide; repository-relative links gain one parent.
    def rebase(match):
        target = match.group(1)
        return target if re.match(r'(?:[a-zA-Z][\w+.-]*:|#|/)', target) else '../' + target
    guide = re.sub(r'(?<=\]\()([^\s)]+)(?=\))', rebase, full)
    guide = guide.replace('# Grothendieck ring classification', '# Grothendieck ring classification · project guide', 1)
    guide = guide.replace('\n\n', '\n\n[Repository front page](../README.md) · [Interactive atlas](' + ATLAS + ')\n\n', 1)
    front = f'''# Grothendieck ring classification

**Which low-rank fusion rings admit fusion categories over ℂ?**

[**Explore the atlas →**]({ATLAS}) · [Manuscripts](manuscripts/README.md) · [Open cases]({ATLAS}unresolved.html) · [Verification](docs/VERIFY.md)

> **AI-generated research · independent verification pending.**
> Results and computations remain provisional. [Research status and verification scope](docs/PREPUBLICATION_REVIEW.md).

## Classification at a glance

Ranks **2–4 have unrestricted classification claims**, with exactly **15 rank-four rings**.
Higher ranks have the explicit multiplicity bounds below.

{scope}

**Six open cases:** two at rank six and four at rank eight.
[Explore their status, invariants and research records]({ATLAS}unresolved.html).

<details>
<summary><strong>Known realizations at each exact multiplicity</strong></summary>

Multiplicity is the largest fusion coefficient. `≥` marks a lower bound where
general categorification remains open; a dash marks an unanalyzed band.

{counts}

[Full count data](data/grothendieck_counts.csv) · [Definitions and scope](docs/PROJECT_GUIDE.md#grothendieck-rings--known-realizations-at-each-exact-multiplicity)

</details>

## Read, inspect, reproduce

| Resource | Start here |
|---|---|
| **Rank-four theorem** | [Unrestricted classification and reading guide](manuscripts/rank4/README.md) |
| Mathematics | [Manuscripts by rank](manuscripts/README.md) · [Candidates and open cases · PDF](docs/New_category_candidates_and_open_cases.pdf) |
| Data | [Decision ledger](data/classification_status.csv) · [All fusion rings and enumeration](https://github.com/sebastienpalcoux/fusion-ring-census) |
| Computation | [Replay instructions](docs/VERIFY.md) · [Provenance](docs/PROVENANCE.md) |
| Project details | [Research updates, models, band tables and repository guide](docs/PROJECT_GUIDE.md) |
| Announcement | [Five-page introduction](announcements/hexagon-2026-10/Low_rank_Grothendieck_rings_announcement.pdf) · [Hexagon](https://hexagonmath.org/2610.00300?version=1) |

The companion [Fusion Ring Census](https://github.com/sebastienpalcoux/fusion-ring-census)
enumerates based rings. This repository records their categorifications and exclusions.
'''
    # Derive the live total from the same generated scope table.
    open_rows = [int(n) for n in re.findall(r'(\d+) unresolved\.', scope)]
    total_open = sum(open_rows)
    front = front.replace('**Six open cases:** two at rank six and four at rank eight.',
                          f'**{total_open} open cases.** General categorification remains undecided for these rings.')
    return front, guide
