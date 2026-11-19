"""Validate the limited atlas metadata change for the ranks 2--4 edition.

Historical build receipts remain frozen.  Their atlas binding is accepted only
through a saved, byte-identical predecessor and a comparison that permits the
new manuscript metadata and its three direct checksum references to change.
Classification records, research dates and every other atlas field must match.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

RECEIPT = "data/manuscript_editions/2026-11-19/receipt.json"
ATLAS = "site/dist/data/atlas.json"
EDITABLE_PATHS = (
    ("current_documents", "sha256"),
    ("current_publication_documents", "sha256"),
    ("reader_resources", "files", "manuscript_page_counts.json", "sha256"),
    ("reader_resources", "page_totals"),
    ("manuscript_edition",),
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def unchanged_projection(value):
    value = deepcopy(value)
    for keys in EDITABLE_PATHS:
        parent = value
        for key in keys[:-1]:
            parent = parent[key]
        parent.pop(keys[-1], None)
    return value


def verified_predecessor(repo):
    """Return the old atlas hash only after checking the edition's exact scope."""
    repo = Path(repo)
    receipt = read(repo / RECEIPT)
    if receipt.get("schema") != "manuscript-edition-atlas/v1":
        return None
    if receipt.get("date") != "2026-11-19" or receipt.get("path") != ATLAS:
        return None
    prior_path = "data/manuscript_editions/2026-11-19/prior_atlas.json"
    if receipt.get("prior_path") != prior_path:
        return None
    prior = repo / prior_path
    current = repo / ATLAS
    if digest(prior) != receipt["before_sha256"] or digest(current) != receipt["after_sha256"]:
        return None
    old, new = read(prior), read(current)
    old_fixed = json.dumps(unchanged_projection(old), sort_keys=True, separators=(",", ":"), allow_nan=False)
    new_fixed = json.dumps(unchanged_projection(new), sort_keys=True, separators=(",", ":"), allow_nan=False)
    if old_fixed != new_fixed:
        return None
    if (repo / "data/atlas.json").read_bytes() != current.read_bytes():
        return None
    lower = read(repo / "data/current_document_revision.json")
    publication = read(repo / "data/current_publication_revision.json")
    pages = read(repo / "data/manuscript_page_counts.json")
    edition = new.get("manuscript_edition")
    if not edition or edition.get("date") != receipt["date"]:
        return None
    if any(value.get("manuscript_edition") != edition for value in (lower, publication, pages)):
        return None
    bindings = (
        (new["current_documents"]["sha256"], "data/current_document_revision.json"),
        (new["current_publication_documents"]["sha256"], "data/current_publication_revision.json"),
        (new["reader_resources"]["files"]["manuscript_page_counts.json"]["sha256"],
         "data/manuscript_page_counts.json"),
    )
    if any(value != digest(repo / path) for value, path in bindings):
        return None
    if new["reader_resources"]["page_totals"] != pages["totals"]:
        return None
    return receipt["before_sha256"]


def matches(relative, expected, repo):
    """Chain the narrow edition successor to the unchanged frontier receipt."""
    repo = Path(repo)
    if relative != ATLAS or not (repo / RECEIPT).is_file():
        return False
    before = verified_predecessor(repo)
    if before is None:
        return False
    frontier = read(repo / "evidence/frontier/publication_replacements.json")
    entry = frontier["files"][ATLAS]
    if before != entry["after_sha256"]:
        return False
    if expected != before and expected not in entry["prior_sha256"]:
        return False
    return all(digest(repo / name) == value
               for name, value in frontier["immutable_decisions"].items())
