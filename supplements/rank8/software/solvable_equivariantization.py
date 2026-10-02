"""Source-bound finite premises for the three solvability exclusions.

The general categorical exhaustion is proved in paper/solvable_proofs.tex. This dispatcher never treats a failed search as a no-go.
"""
from pathlib import Path
from functools import lru_cache
import json,hashlib
from verify_solvable_r29 import verify_record as r29_record
from verify_solvable_d72 import verify_tensor as d72_tensor,action_and_cohomology_checks
ROOT=Path(__file__).resolve().parents[1]
def require(ok,message='solvability certificate mismatch'):
    if not ok:raise ValueError(message)
def fp(N):return hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
@lru_cache(None)
def records():
    r29=json.loads((ROOT/'data/solvable_r29_certificate.json').read_text())
    d72=json.loads((ROOT/'data/solvable_d72_certificates.json').read_text())
    require([r29['id']]+[x['id'] for x in d72]==['R8_1_29','R8_1_45','R8_1_47'])
    return [r29]+d72
@lru_cache(None)
def d72_auxiliary():return action_and_cohomology_checks()
def certificate(N):
    for r in records():
        if fp(N)!=r['tensor_sha256']:continue
        require(N==r['tensor'])
        if r['id']=='R8_1_29':
            r29_record(r)
            case='FPdim24_prime_equivariantization'
            witness='solvable_r29_certificate.json'
        else:
            d72_tensor(r,N);d72_auxiliary()
            case='FPdim72_module_rank_divisibility'
            witness='solvable_d72_certificates.json'
        return dict(kind='solvable_equivariantization',case=case,id=r['id'],
            tensor_sha256=r['tensor_sha256'],witness_file=witness,
            criterion='ENO solvability and prime equivariantization; complete pointed action or module-category exhaustion',
            scope='no fusion category over C')
    return None
def verify_certificate(N,c):require(certificate(N)==c)
