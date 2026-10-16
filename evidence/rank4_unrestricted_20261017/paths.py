"""Resolve canonical repository inputs for the independent rank-four checks."""
import argparse
from pathlib import Path


def repository_root():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository-root',type=Path)
    args = parser.parse_args()
    root = args.repository_root.resolve() if args.repository_root else Path(__file__).resolve().parents[2]
    if not (root/'supplements/rank4/unrestricted').is_dir():
        raise RuntimeError('rank-four computational package absent; supply --repository-root')
    return root
