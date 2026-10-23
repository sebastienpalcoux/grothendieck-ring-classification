#!/usr/bin/env python3
"""Describe a reviewed repository diff for GitHub Git-data publication.

This performs no network writes and changes no Git references. Output must be
outside the checkout. UTF-8 files are grouped into create_tree request batches;
binary files have individual base64 create_blob requests, deduplicated by SHA.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess

REPOSITORY = "sebastienpalcoux/grothendieck-ring-classification"
BASE = "7f4aea6fb5e5a98aa9e5e5dc78a58bd46c1c92e1"


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")


def prepare(repo, output, base, batch_bytes):
    if output.is_relative_to(repo):
        raise ValueError("Publication manifests must be outside the checkout")
    output.mkdir(parents=True, exist_ok=True)
    tracked = git(repo, "diff", "--name-only", "-z", base).decode().split("\0")
    untracked = git(repo, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")
    paths = sorted(set(tracked + untracked) - {""})
    groups = {"text": [], "binary": [], "deleted": []}
    batches = []; current = []; size = 0; binary_requests = {}
    for relative in paths:
        path = repo / relative
        if path.is_symlink():
            raise ValueError("Unexpected symbolic link: " + relative)
        if not path.exists():
            groups["deleted"].append({"path": relative, "sha": None})
            continue
        raw = path.read_bytes()
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        mode = "100755" if path.stat().st_mode & 0o111 else "100644"
        record = {"path": relative, "mode": mode, "type": "blob", "sha": sha,
                  "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        try:
            text = raw.decode("utf-8")
            if "\0" in text: raise UnicodeError("NUL in file")
        except UnicodeError:
            groups["binary"].append(record)
            filename = "blob-" + sha + ".json"
            if sha not in binary_requests:
                write(output / filename, {"repository_full_name": REPOSITORY, "encoding": "base64", "content": base64.b64encode(raw).decode()})
                binary_requests[sha] = filename
        else:
            groups["text"].append(record)
            entry = {"path": relative, "mode": mode, "type": "blob", "content": text}
            encoded_size = len(json.dumps(entry, ensure_ascii=False).encode())
            if current and size + encoded_size > batch_bytes:
                batches.append(current); current = []; size = 0
            current.append(entry); size += encoded_size
    if current: batches.append(current)
    text_files = []
    for index, entries in enumerate(batches, 1):
        filename = f"text-tree-{index:03}.json"
        write(output / filename, {"repository_full_name": REPOSITORY, "tree_elements": entries})
        text_files.append(filename)
    base_tree = git(repo, "rev-parse", base + "^{tree}").decode().strip()
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    manifest = {"repository": REPOSITORY, "base_commit": base, "base_tree": base_tree, "local_head": head,
                "branch": git(repo, "branch", "--show-current").decode().strip(), "groups": groups,
                "counts": {key: len(value) for key, value in groups.items()},
                "total_bytes": sum(r["bytes"] for key in ("text", "binary") for r in groups[key]),
                "text_tree_requests": text_files, "binary_blob_requests": binary_requests,
                "instructions": ["Recheck every file hash before publication.",
                    "Create each binary blob once and require the returned SHA to equal its recorded SHA.",
                    "For each text-tree request, supply the previous tree SHA as base_tree_sha, starting with base_tree.",
                    "Create a final tree adding binary path/mode/type/sha entries and any explicit deletions.",
                    "Create a commit with base_commit as parent. This changes no branch.",
                    "Update only the designated publication branch, then let the coordinator update main using expected_sha."]}
    write(output / "manifest.json", manifest)
    print(json.dumps({"manifest": str(output / "manifest.json"), "counts": manifest["counts"], "total_bytes": manifest["total_bytes"], "text_batches": len(text_files), "unique_binary_blobs": len(binary_requests)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base", default=BASE)
    parser.add_argument("--batch-bytes", type=int, default=80000)
    args = parser.parse_args()
    prepare(args.repository.resolve(), args.output.resolve(), args.base, args.batch_bytes)
