#!/usr/bin/env python3
"""Restore the exact archived rank-four certificate from public binary parts.

Uses Python's standard library only. Every part and the concatenated stream
are checked before the destination is installed. Existing mismatching files
are never overwritten. No network requests or decompression are performed.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile


EXPECTED_BYTES = 75_825_461
EXPECTED_SHA256 = "969a2a5a84b794a3da1d9cd3978f92324d631760f503f5d208011923a723920f"


def digest(path):
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
            size += len(block)
    return size, h.hexdigest()


def restore(manifest_path, output, verify_only=False):
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (manifest.get("schema"), manifest.get("bytes"), manifest.get("sha256")) != (
        1, EXPECTED_BYTES, EXPECTED_SHA256
    ):
        raise ValueError("Manifest does not describe the pinned rank-four certificate")
    parts = manifest.get("parts")
    if not isinstance(parts, list) or len(parts) != 13:
        raise ValueError("Expected all 13 ordered certificate parts")
    base = manifest_path.resolve().parent
    combined = hashlib.sha256()
    total = 0
    temp_path = None
    stream = None
    try:
        if not verify_only:
            output.parent.mkdir(parents=True, exist_ok=True)
            if output.exists():
                if digest(output) != (EXPECTED_BYTES, EXPECTED_SHA256):
                    raise FileExistsError("Existing destination differs; select a new --output path")
                # Still check every public part instead of trusting the destination.
            else:
                stream = tempfile.NamedTemporaryFile(
                    mode="wb", prefix=".rank4-certificate-", suffix=".tmp",
                    dir=output.parent, delete=False,
                )
                temp_path = Path(stream.name)
        for index, entry in enumerate(parts, 1):
            name = f"parts/part-{index:03d}.bin"
            if entry.get("path") != name:
                raise ValueError(f"Unexpected part path or order at part {index}")
            path = (base / name).resolve()
            if not path.is_relative_to(base):
                raise ValueError("Part resolves outside the certificate directory")
            part_hash = hashlib.sha256()
            part_size = 0
            with path.open("rb") as part:
                for block in iter(lambda: part.read(1024 * 1024), b""):
                    part_hash.update(block)
                    combined.update(block)
                    part_size += len(block)
                    total += len(block)
                    if stream is not None:
                        stream.write(block)
            if (part_size, part_hash.hexdigest()) != (entry["bytes"], entry["sha256"]):
                raise ValueError(f"Part size or SHA-256 mismatch: {name}")
        if (total, combined.hexdigest()) != (EXPECTED_BYTES, EXPECTED_SHA256):
            raise ValueError("Concatenated certificate size or SHA-256 mismatch")
        if stream is not None:
            stream.flush()
            os.fsync(stream.fileno())
            stream.close()
            stream = None
            # Refuse to overwrite a destination created while parts were checked.
            if output.exists():
                raise FileExistsError("Destination appeared during restoration")
            os.replace(temp_path, output)
            temp_path = None
        print(f"PASS: 13 parts, {total:,} bytes, SHA-256 {combined.hexdigest()}")
        print("Verified without writing." if verify_only else f"Restored or already verified: {output}")
    finally:
        if stream is not None:
            stream.close()
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=here / "certificates/manifest.json")
    parser.add_argument("--output", type=Path, default=here / "certificates/classification.jsonl.gz")
    parser.add_argument("--verify-only", action="store_true", help="verify all parts without writing a file")
    args = parser.parse_args()
    try:
        restore(args.manifest, args.output, args.verify_only)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Restoration failed: {error}\n")


if __name__ == "__main__":
    main()
