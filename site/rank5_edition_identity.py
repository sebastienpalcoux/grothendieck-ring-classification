"""Validate the narrowly scoped 24 November rank-five publication successor.

The prior release files and the 19 November receipt have fixed identities.
Only the rank-five display scope, its additive theorem metadata and its new
document/page identities can change.  Every historical document entry, atlas
classification row and other-rank field remains fixed.  The predecessor's own
checks run on authenticated archived files before any historical hash is
accepted for the new edition.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path


DATE = "2026-11-24"
ARCHIVE = "data/manuscript_editions/" + DATE
RECEIPT = ARCHIVE + "/receipt.json"
PRIOR_COMMIT = "d35cb684d2f27cca18f89ab24c769af756c16160"
PREDECESSOR = "data/manuscript_editions/2026-11-19/receipt.json"
PREDECESSOR_SHA256 = "1bf09e20200aea9c299eedd5de6a95223332283269f182efcde95fafaa11a057"
ATLAS = "site/dist/data/atlas.json"
STATUS = "site/dist/data/classification_status.json"
LOWER = "data/current_document_revision.json"
PUBLICATION = "data/current_publication_revision.json"
PAGES = "data/manuscript_page_counts.json"
FULL_PAGES = "data/current_manuscript_page_counts.json"
FRONTIER = "evidence/frontier/publication_replacements.json"
FRONTIER_SHA256 = "ceff3c0e4b09b86df39d443a4e5927a7162ece55207ee2ac2a99396efc2d7805"

# These byte identities are the publication at PRIOR_COMMIT, not values that
# a new receipt may redefine.  The old atlas also binds the three old manifests.
PRIOR_FILES = {
    ATLAS: ("prior_atlas.json", "f556b7069f6a0738d695fd82daae49b0c29cb095f84a7c71f7070dfd57d0201b"),
    STATUS: ("prior_classification_status.json", "c74efefe06d616bba8919e7e33736aca6b471b449be63132a6aabde8452d5c92"),
    LOWER: ("prior_document_revision.json", "272a5024110448e4dbc360d05c15929742684dc81e09c509d5a3c39e2e2b9fee"),
    PUBLICATION: ("prior_publication_revision.json", "e33aaf118afd40a674ee6d15098ff2d0f78696e884cacc0e6d200fde2f85ba86"),
    PAGES: ("prior_manuscript_page_counts.json", "e2738d98a9e8112d429b15ccf80df3498ff466be5ae9568ddcdb717fab491295"),
    FULL_PAGES: ("prior_current_manuscript_page_counts.json", "ef61aee39ad51a52cf6dc4c84a1fa19c6dcc8b325b40b1b5786e28d993a06984"),
}
MIRRORS = {
    ATLAS: ("data/atlas.json",),
    STATUS: ("data/classification_status.json",),
    LOWER: ("site/dist/data/current_document_revision.json",),
    PUBLICATION: ("site/dist/data/current_publication_revision.json",),
    PAGES: ("site/dist/downloads/manuscript_page_counts.json",),
    FULL_PAGES: ("site/dist/downloads/current_manuscript_page_counts.json",),
}
ALIASES = {alias: canonical for canonical, aliases in MIRRORS.items()
           for alias in (canonical,) + aliases}
EDITION = {
    "date": DATE,
    "title": "Grothendieck rings of complex fusion categories: rank 5",
    "manuscript": "manuscripts/rank5.pdf",
    "source": "manuscripts/rank5.tex",
    "verification": "supplements/rank5/sharp/",
    "verification_commit": "b479c65c702c6a09a674df7c2f8468b1a48915d3",
    "source_archive": "manuscripts/hexagon/hexagon-rank-5-source.zip",
    "classification_scope": "unrestricted",
    "models": 17,
    "maximum_multiplicity": 4,
    "dimension_bound": "48+24√3",
    "hexagon_status": "prepared; not submitted",
    "historical_manuscript": "manuscripts/rank5/papers/manuscript.pdf",
}
THEOREM = {
    "manuscript": EDITION["manuscript"],
    "source": EDITION["source"],
    "scope": ("Unrestricted complex classification: 17 Grothendieck rings, each with a "
              "unitary realization; every categorification admits a spherical structure "
              "and has a pseudo-unitary Galois conjugate."),
    "maximum_multiplicity": 4,
    "dimension_bound": EDITION["dimension_bound"],
    "generated_census": 269,
    "bounded_census": 114,
    "excluded": 97,
    "models": 17,
    "unresolved": 0,
    "verification": "supplements/rank5/sharp/README.md",
}
NEW_DOCUMENTS = {
    EDITION["manuscript"], EDITION["source"], EDITION["source_archive"],
    "manuscripts/hexagon/rank5-publication-letter.tex",
    "manuscripts/hexagon/rank5-publication-letter.pdf",
}
HISTORICAL_PAPERS = (
    EDITION["historical_manuscript"],
    "manuscripts/rank5/papers/verification_guide.pdf",
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError("Non-finite JSON number: " + value)


def read(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=_unique_object,
                      parse_constant=_invalid_constant)


def _same(left, right):
    """Compare JSON values without treating true, 1 and 1.0 as identical."""
    options = dict(sort_keys=True, separators=(",", ":"), allow_nan=False)
    return json.dumps(left, **options) == json.dumps(right, **options)


def _without(value, *keys):
    value = deepcopy(value)
    for key in keys:
        value.pop(key, None)
    return value


def _file_entry(repo, path, entry):
    if set(entry) != {"bytes", "sha256"} or type(entry["bytes"]) is not int:
        return False
    content = (repo / path).read_bytes()
    return len(content) == entry["bytes"] and hashlib.sha256(content).hexdigest() == entry["sha256"]


def _documents_valid(repo, old, new, publication=False):
    editable = ["rank5_edition", "documents", "web_copies"]
    if publication:
        editable.append("base_document_manifest")
    if not _same(_without(old, *editable), _without(new, *editable)):
        return False
    old_docs, new_docs = old["documents"], new["documents"]
    additions = set(new_docs) - set(old_docs)
    required = {EDITION[key] for key in ("source", "manuscript", "source_archive")}
    if not required <= additions <= NEW_DOCUMENTS:
        return False
    if not _same(old_docs, {key: value for key, value in new_docs.items() if key not in additions}):
        return False
    if not all(_file_entry(repo, path, entry) for path, entry in new_docs.items()):
        return False
    web = deepcopy(old["web_copies"])
    web["papers/rank5.pdf"] = EDITION["manuscript"]
    if not _same(new["web_copies"], web):
        return False
    if (repo / "site/dist/papers/rank5.pdf").read_bytes() != (repo / EDITION["manuscript"]).read_bytes():
        return False
    if publication:
        base = deepcopy(old["base_document_manifest"])
        base["sha256"] = digest(repo / LOWER)
        base["bytes"] = (repo / LOWER).stat().st_size
        if not _same(new["base_document_manifest"], base):
            return False
    return _same(new.get("rank5_edition"), EDITION)


def _pages_valid(repo, old, new):
    editable = ("rank5_edition", "documents", "historical_documents", "document_counts",
                "totals", "classification_scope", "counting_rule")
    if not _same(_without(old, *editable), _without(new, *editable)):
        return False
    expected_rule = old["counting_rule"].replace(
        "superseded rank-four papers", "superseded rank-four and rank-five papers")
    if new["counting_rule"] != expected_rule:
        return False
    old_papers = [row for row in old["documents"] if row["path"] in HISTORICAL_PAPERS]
    if [row["path"] for row in old_papers] != list(HISTORICAL_PAPERS):
        return False
    new_papers = [row for row in new["documents"] if row["path"] == EDITION["manuscript"]]
    if len(new_papers) != 1:
        return False
    paper = new_papers[0]
    if (set(paper) != set(old_papers[0]) or paper["kind"] != "mathematical_manuscript"
            or paper["title"] not in ("Rank five", EDITION["title"])
            or type(paper["pages"]) is not int or paper["pages"] <= 0
            or not _file_entry(repo, paper["path"], {key: paper[key] for key in ("bytes", "sha256")})):
        return False
    expected_documents = []
    for row in old["documents"]:
        if row["path"] == HISTORICAL_PAPERS[0]:
            expected_documents.append(paper)
        elif row["path"] != HISTORICAL_PAPERS[1]:
            expected_documents.append(row)
    if not _same(new["documents"], expected_documents):
        return False
    historical = deepcopy(old["historical_documents"])
    for row in old_papers:
        historical.append(dict(row, status="historical", superseded_by=EDITION["manuscript"]))
    if not _same(new["historical_documents"], historical):
        return False
    classification = dict(old["classification_scope"], rank5=THEOREM["scope"])
    if not _same(new["classification_scope"], classification):
        return False
    kinds = {"mathematical_manuscript": "mathematical_manuscripts",
             "verification_guide": "verification_guides", "research_status_report": "research_status_reports"}
    totals = {kind: sum(row["pages"] for row in new["documents"] if row["kind"] == kind)
              for kind in kinds}
    counts = {plural: sum(row["kind"] == kind for row in new["documents"])
              for kind, plural in kinds.items()}
    totals["mathematical_manuscripts_and_guides"] = totals["mathematical_manuscript"] + totals["verification_guide"]
    totals["all_distinct_documents"] = totals["mathematical_manuscripts_and_guides"] + totals["research_status_report"]
    return (_same(new["totals"], totals) and _same(new["document_counts"], counts)
            and _same(new.get("rank5_edition"), EDITION))


def _atlas_valid(repo, old, new, pages):
    expected = deepcopy(old)
    expected["rank5_edition"] = EDITION
    candidates = [index for index, row in enumerate(old["scope"]) if row["rank"] == 5]
    if len(candidates) != 1:
        return False
    index = candidates[0]
    note = new["scope"][index]["note"]
    if not isinstance(note, str) or not note.strip():
        return False
    expected["scope"][index].update(
        kind="unrestricted", through=None, rings=None, analyzed_through=20,
        positive=17, unresolved=0, paper=EDITION["title"], note=note)
    expected["current_documents"]["sha256"] = digest(repo / LOWER)
    expected["current_publication_documents"]["sha256"] = digest(repo / PUBLICATION)
    expected["reader_resources"]["files"]["manuscript_page_counts.json"]["sha256"] = digest(repo / PAGES)
    expected["reader_resources"]["page_totals"] = pages["totals"]
    return _same(new, expected)


def _status_valid(old, new):
    expected = deepcopy(old)
    expected["inputs"]["rank5"].update(
        classification_scope="unrestricted", general_classified_through="all",
        unrestricted_theorem=THEOREM)
    return _same(new, expected)


def _verified_receipt(repo):
    receipt = read(repo / RECEIPT)
    if (receipt["schema"] != "rank5-manuscript-edition/v1" or receipt["date"] != DATE
            or receipt["prior_commit"] != PRIOR_COMMIT
            or receipt["predecessor_receipt"] != PREDECESSOR
            or receipt["predecessor_receipt_sha256"] != PREDECESSOR_SHA256
            or digest(repo / PREDECESSOR) != PREDECESSOR_SHA256
            or digest(repo / FRONTIER) != FRONTIER_SHA256
            or set(receipt["files"]) != set(PRIOR_FILES)):
        return None
    old, new, snapshots = {}, {}, {}
    for path, (filename, before) in PRIOR_FILES.items():
        entry = receipt["files"][path]
        prior_path = ARCHIVE + "/" + filename
        if (set(entry) != {"prior_path", "before_sha256", "after_sha256"}
                or entry["prior_path"] != prior_path or entry["before_sha256"] != before
                or digest(repo / prior_path) != before
                or digest(repo / path) != entry["after_sha256"]):
            return None
        content = (repo / path).read_bytes()
        if any((repo / alias).read_bytes() != content for alias in MIRRORS[path]):
            return None
        old[path], new[path] = read(repo / prior_path), read(repo / path)
        snapshots[path] = prior_path

    from manuscript_edition_identity import verified_predecessor
    predecessor = verified_predecessor(
        repo, current_paths={path: snapshots[path] for path in (ATLAS, LOWER, PUBLICATION, PAGES)})
    frontier = read(repo / FRONTIER)
    if (predecessor != frontier["files"][ATLAS]["after_sha256"]
            or PRIOR_FILES[STATUS][1] != frontier["files"][STATUS]["after_sha256"]
            or not all(digest(repo / path) == value for path, value in frontier["immutable_decisions"].items())):
        return None
    if not (_documents_valid(repo, old[LOWER], new[LOWER])
            and _documents_valid(repo, old[PUBLICATION], new[PUBLICATION], publication=True)
            and _pages_valid(repo, old[PAGES], new[PAGES])
            and _pages_valid(repo, old[FULL_PAGES], new[FULL_PAGES])
            and _atlas_valid(repo, old[ATLAS], new[ATLAS], new[PAGES])
            and _status_valid(old[STATUS], new[STATUS])):
        return None
    lower_paper = next(row for row in new[PAGES]["documents"] if row["path"] == EDITION["manuscript"])
    full_paper = next(row for row in new[FULL_PAGES]["documents"] if row["path"] == EDITION["manuscript"])
    if not _same(lower_paper, full_paper):
        return None
    return receipt


def verified_receipt(repo):
    """Return the receipt only after all frozen and current bindings validate."""
    try:
        return _verified_receipt(Path(repo))
    except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError, StopIteration):
        return None


def matches(relative, expected, repo):
    """Recognize an old hash only through this exact publication successor."""
    canonical = ALIASES.get(relative)
    if canonical is None or not (Path(repo) / RECEIPT).is_file():
        return False
    receipt = verified_receipt(repo)
    if receipt is None:
        return False
    if expected == receipt["files"][canonical]["before_sha256"]:
        return True
    frontier_path = "site/dist/" + canonical if canonical.startswith("data/") else canonical
    entry = read(Path(repo) / FRONTIER)["files"].get(frontier_path)
    return bool(entry and (expected == entry["after_sha256"] or expected in entry["prior_sha256"]))
