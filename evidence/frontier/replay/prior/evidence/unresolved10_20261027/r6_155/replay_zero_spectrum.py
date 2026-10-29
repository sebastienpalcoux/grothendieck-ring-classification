"""Bounded exact zero-spectrum scan of the frozen rank-26 candidate.

A timeout is unknown, never an exclusion. No other proof search is run.
"""
import hashlib
import json
import pathlib
import subprocess
import tempfile
import time

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / 'supplements/rank6/research/frontier/new_research/r155_modular/reconstruction.json'
EXPECTED = '756280ec124cfd90bcfe59e29cd39f52d3df6702633d2cf394ee409757ec7cdb'


def main():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED:
        raise ValueError('rank-26 source changed')
    obj = json.loads(raw)
    ring = obj['fusion_rules']
    n = len(ring)
    if n != 26:
        raise ValueError('wrong source rank')
    order = [obj['unit']] + [i for i in range(n) if i != obj['unit']]
    tensor = [[[ring[i][j][k] for k in order] for j in order] for i in order]
    for i in range(n):
        for j in range(n):
            if tensor[0][i][j] != int(i == j):
                raise ValueError('incorrect unit reindexing')
    values = [1, n] + [x for matrix in tensor for row in matrix for x in row]
    with tempfile.TemporaryDirectory(prefix='r155-center-zero-spectrum-') as tmp:
        exe = pathlib.Path(tmp) / 'scan'
        subprocess.run(['g++', '-O3', '-std=c++17', str(HERE / 'zero_spectrum26.cpp'), '-o', str(exe)], check=True)
        start = time.monotonic()
        run = subprocess.run([str(exe)], input=' '.join(map(str, values)), text=True,
                             capture_output=True, check=True, timeout=25)
        if run.stdout.strip() != '0 0':
            raise ValueError('unexpected zero-spectrum result: ' + run.stdout)
        print(json.dumps({'rank': n, 'zero_spectrum_exclusion_found': False,
                          'source_sha256': EXPECTED, 'seconds': time.monotonic() - start,
                          'scope': 'necessary criterion only; no categorification conclusion'}))


if __name__ == '__main__':
    main()
