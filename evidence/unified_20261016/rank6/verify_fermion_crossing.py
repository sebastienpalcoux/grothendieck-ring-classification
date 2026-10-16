#!/usr/bin/env python3
"""Exact Azumaya linking-Gram check of the published rank-22 R155 witness.

This checks a necessary identity. It does not construct module associators.
No third-party libraries, no writes to the published evidence.
"""
from pathlib import Path
import hashlib
import json
import argparse

def default_repo():
    for parent in [Path.cwd(), *Path(__file__).resolve().parents]:
        for candidate in [parent, parent/'repo']:
            if (candidate/'supplements/rank6/data/decisions.json').is_file():
                return candidate
    raise ValueError('Repository root not found; pass --repo explicitly')

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path)
a = p.parse_args()
root = (a.repo if a.repo is not None else default_repo()).resolve()
e = root/'evidence/theoretical_20261016/rank6'
src = e/'r155_reflection/r155_data.json'
wit = e/'r155_center_module/anti_module_witness.json'
src_bytes = src.read_bytes()
if hashlib.sha256(src_bytes).hexdigest() != '769250938d8bd0c8a251aaacc18832174af8175ed9b44fc487ec3f6d04357353':
    raise ValueError('Published source hash mismatch')
data = json.loads(src_bytes)
wit_bytes = wit.read_bytes()
if hashlib.sha256(wit_bytes).hexdigest() != '3af4757cb0eaffbc37402ec8f26122005fb68c36810eb5b72c6ec8aae203f37f':
    raise ValueError('Published anti-invariant witness hash mismatch')
w = json.loads(wit_bytes)
R, T, fixed = data['fusion'], w['anti_matrices'], w['fixed']
perm = [r.index(1) for r in R[0]]
free = [i for i in range(26) if i < perm[i]]
n, k = len(free)+2*len(fixed), len(free)
if fixed != [4,7,20,21,24,25] or n != 22:
    raise ValueError('Unexpected fermion fixed labels or module rank')
M = [[[0]*n for _ in range(n)] for _ in range(26)]
for x in range(26):
    for a,u in enumerate(free):
        for b,v in enumerate(free):
            M[x][a][b] = R[x][u][v]+R[x][u][perm[v]]
        for b,v in enumerate(fixed):
            for sign in range(2):
                M[x][a][k+2*b+sign] = R[x][u][v]
    for a,u in enumerate(fixed):
        for si in range(2):
            row=k+2*a+si
            for b,v in enumerate(free):
                M[x][row][b] = R[x][u][v]
            for b,v in enumerate(fixed):
                for sj in range(2):
                    z=R[x][u][v]+(-1)**(si+sj)*T[x][a][b]
                    if z < 0 or z % 2:
                        raise ValueError('Invalid integral reconstruction')
                    M[x][row][k+2*b+sj]=z//2
V = [[M[x][a][b] for x in range(26)] for a in range(n) for b in range(n)]
def gram(a,b,c,d):
    return sum(x*y for x,y in zip(V[a*n+b],V[c*n+d]))
count=0
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                if gram(a,b,c,d) != gram(c,a,d,b):
                    raise ValueError(f'Fermion Azumaya crossing fails at {(a,b,c,d)}')
                count += 1
print(json.dumps({
    'status':'PASS',
    'mathematical_verdict':'PASS_NECESSARY',
    'ring':'R6_4_155',
    'source_data_sha256':hashlib.sha256(src_bytes).hexdigest(),
    'source_witness_sha256':hashlib.sha256(wit_bytes).hexdigest(),
    'based_module_rank':n,
    'linking_gram_identities_checked':count,
    'scope':'The published based module passes the additional Azumaya crossing identity. No module category or categorification is constructed; no exclusion follows.'
},indent=2))
