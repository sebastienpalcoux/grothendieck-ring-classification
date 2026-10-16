#!/usr/bin/env python3
"""Build the dated proof bundle and replay its default verifier in isolation."""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
STAGE = "evidence/theoretical_20261016"
PREFIX = "theoretical-update-2026-10-16"
VERIFIER = "tools/verify_theoretical_20261016.py"
REQUIRED = (
    VERIFIER,
    "tools/build_theoretical_20261016_archive.py",
    "supplements/rank6/data/census.json",
    "supplements/rank6/data/decisions.json",
    "supplements/rank7/data/rank7_tables.txt.gz",
    "supplements/rank7/output/rank7_ledger.json",
    "supplements/rank8/data/rank8_tables.txt.gz",
    "supplements/rank8/data/decisions.json",
)
MANUSCRIPTS = (
    "manuscripts/rank6/papers",
    "manuscripts/rank7/papers",
    "manuscripts/rank8/paper",
)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(data):
    return json.loads(data)


def collect(root):
    paths = set(REQUIRED)
    for folder in (STAGE,):
        paths.update(p.relative_to(root).as_posix()
                     for p in (root / folder).rglob("*")
                     if p.is_file() and "__pycache__" not in p.parts
                     and p.suffix != ".pyc")
    for folder in MANUSCRIPTS:
        paths.update(p.relative_to(root).as_posix()
                     for p in (root / folder).rglob("*")
                     if p.is_file() and p.suffix in (".tex", ".pdf"))
    need(all((root / path).is_file() for path in REQUIRED),
         "Missing a required census, ledger, verifier or archive builder")
    payload = {path: (root / path).read_bytes() for path in sorted(paths)}
    manifest_path = STAGE + "/source_files.json"
    need(manifest_path in payload, "Freeze source_files.json before building")
    bound = None
    for node in ast.parse(payload[VERIFIER]).body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "MANIFEST_SHA256"
                for t in node.targets):
            bound = ast.literal_eval(node.value)
    need(bound == sha(payload[manifest_path]),
         "Freeze the proof manifest and its verifier digest before building")
    for path, digest in load(payload[manifest_path]).items():
        need(path in payload and sha(payload[path]) == digest,
             "Missing or changed manifest source: " + path)
    revision = load(payload[STAGE + "/rank6/document_revision.json"])
    for path, meta in revision["documents"].items():
        need(path in payload and sha(payload[path]) == meta["sha256"]
             and len(payload[path]) == meta["bytes"],
             "Freeze the current rank-six document revision: " + path)
    for path in ("manuscripts/rank6/papers/manuscript.pdf",
                 "manuscripts/rank6/papers/verification_guide.pdf",
                 "manuscripts/rank7/papers/manuscript.pdf",
                 "manuscripts/rank8/paper/rank8.pdf"):
        need(path in payload and payload[path].startswith(b"%PDF-"),
             "Missing current manuscript PDF: " + path)
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path,
                        help="Defaults to the repository site's dated download")
    parser.add_argument("--check-only", action="store_true",
                        help="Validate frozen inputs without creating an archive")
    args = parser.parse_args()
    root = args.repo.resolve()
    output = (args.output or root / "site/dist/downloads" / (PREFIX + ".zip")).resolve()
    payload = collect(root)
    decisions = load(payload[STAGE + "/decisions.json"])
    remaining = load(payload[STAGE + "/remaining_ids.json"])
    count = len(decisions)
    need(count == len({record["id"] for record in decisions}) and count > 0,
         "The update requires distinct nonempty decisions")
    need(all(record["status"] == "excluded" and record["scope"] == "general_complex"
             for record in decisions), "The bundle's decision count must use general exclusions")
    if args.check_only:
        print(json.dumps({"status": "PASS", "phase": "frozen-input-check",
                          "files": len(payload), "new_general_exclusions": count,
                          "remaining": {rank: len(ids) for rank, ids in remaining.items()}}, indent=2))
        return
    readme = f"""# Theoretical update — 16 October 2026

This bundle contains {count} new general exclusions, the full dated research
evidence, current rank-six through rank-eight manuscript sources and PDFs, and
the census data and ledgers used by the default verifier. General existence
remains unresolved for {len(remaining['6'])} rank-six, {len(remaining['7'])}
rank-seven and {len(remaining['8'])} rank-eight rings. The precise scope of
additional pivotal and unitary results is retained in the proofs.

From this extracted directory, with Python 3.11+, SymPy 1.14.0 and NumPy 2.3.5
installed, run:

```sh
python3 tools/verify_theoretical_20261016.py
```

This default command is standalone: it checks the frozen proof-source manifest,
replays the exact verifiers, validates the new decisions and unresolved
inventory, and reconstructs the complete prior ledgers to check preservation of
every unchanged record. It prints a JSON receipt whose status must be PASS.
The mathematical proofs are in `evidence/theoretical_20261016/`.

The optional `--historical` and `--spectral` modes require the full repository
because their earlier-stage dependencies are intentionally outside this dated
bundle. Run those modes from a complete repository checkout.

`ARCHIVE_MANIFEST.json` records the byte size and SHA-256 of every bundled
source, manuscript and data file. `SHA256SUMS` additionally covers this README,
the requirements file and the manifest. The ZIP uses a fixed timestamp and
sorted paths; rebuilding identical frozen inputs gives identical ZIP bytes.

Manuscripts: `manuscripts/rank6/papers/manuscript.pdf`,
`manuscripts/rank6/papers/verification_guide.pdf`,
`manuscripts/rank7/papers/manuscript.pdf`, and
`manuscripts/rank8/paper/rank8.pdf`.

Repository: https://github.com/sebastienpalcoux/grothendieck-ring-classification
"""
    manifest = {
        "schema": "theoretical-update-archive/v1", "date": "2026-10-16",
        "new_general_exclusions": count,
        "remaining": {rank: len(ids) for rank, ids in remaining.items()},
        "default_verifier": VERIFIER,
        "files": {path: {"bytes": len(data), "sha256": sha(data)}
                  for path, data in payload.items()},
    }
    payload["README.md"] = readme.encode()
    payload["requirements.txt"] = b"sympy==1.14.0\nnumpy==2.3.5\n"
    payload["ARCHIVE_MANIFEST.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    payload["SHA256SUMS"] = "".join(
        f"{sha(data)}  {path}\n" for path, data in sorted(payload.items())).encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="theoretical-bundle-", dir=output.parent) as temporary:
        temporary = Path(temporary)
        archive = temporary / output.name
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9) as bundle:
            for path, data in sorted(payload.items()):
                entry = zipfile.ZipInfo(PREFIX + "/" + path, date_time=(2026, 10, 16, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                entry.create_system = 3
                bundle.writestr(entry, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        extracted = temporary / "extracted"
        with zipfile.ZipFile(archive) as bundle:
            need(bundle.testzip() is None, "ZIP CRC verification failed")
            bundle.extractall(extracted)
        isolated = extracted / PREFIX
        result = subprocess.run([sys.executable, str(isolated / VERIFIER)],
                                cwd=isolated, text=True, capture_output=True)
        need(result.returncode == 0,
             "Standalone archive replay failed:\n" + result.stdout + result.stderr)
        report = json.loads(result.stdout)
        need(report.get("status") == "PASS"
             and report.get("new_general_exclusions") == count,
             "Standalone verifier returned an inconsistent receipt")
        # Refuse to publish a mixed snapshot if sources changed during the replay.
        for path, meta in manifest["files"].items():
            need(sha((root / path).read_bytes()) == meta["sha256"],
                 "Input changed while packaging: " + path)
        archive_digest = sha(archive.read_bytes())
        archive_bytes = archive.stat().st_size
        os.replace(archive, output)
    print(json.dumps({"status": "PASS", "archive": str(output),
                      "sha256": archive_digest, "bytes": archive_bytes,
                      "files": len(payload), "new_general_exclusions": count,
                      "remaining": manifest["remaining"],
                      "standalone_replay": report}, indent=2))


if __name__ == "__main__":
    main()
