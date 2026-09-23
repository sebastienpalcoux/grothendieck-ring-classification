"""Conservative exploratory port of the rank-seven oriented spherical sieve.

A ring is excluded only when ``advanced_criteria.verify`` completes exactly.
All incomplete search paths, timeouts, and unsupported signed noncommutative
branches remain undecided.  This is not used by the main rank-eight ledger.
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(ROOT / 'software'))
import advanced_criteria
import analyze


def main():
    requested = sys.argv[1]
    mult,index = map(int,requested.split('_')) if '_' in requested else (1,int(requested))
    budget = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    decisions = json.loads((ROOT / 'data/decisions.json').read_text())
    row = next(d for d in decisions if d['id'] == f'R8_{mult}_{index}')
    # The main ledger may advance while a bounded exploratory campaign runs.
    # A witness remains a meaningful independent check for an already
    # excluded source tensor; its stage will be assigned by the main ledger.
    source = [R for R in analyze.read_source() if analyze.mult(R) == mult]
    source.sort(key=lambda R: tuple(x for M in R for l in M for x in l))
    R = source[index - 1]
    assert row['tensor_sha256'] == analyze.fp(R)
    t = time.monotonic()
    print('start', row['id'], 'commutative', row['commutative'], flush=True)
    info = advanced_criteria.eligibility(R)
    print('eligible', info, 'seconds', round(time.monotonic()-t,2), flush=True)
    if not info['eligible']:
        return
    cert = advanced_criteria.general_certificate(R, timeout=budget)
    print('discovery', 'certificate' if cert else 'no_conclusion',
          'seconds', round(time.monotonic()-t,2), flush=True)
    if cert is not None:
        advanced_criteria.verify(R,cert)
        print('exact_verification_complete', 'seconds',
              round(time.monotonic()-t,2),flush=True)
        folder = ROOT / 'experimental_signed/certificates'
        folder.mkdir(exist_ok=True)
        (folder / (row['id']+'.json')).write_text(json.dumps({'id':row['id'],
           'tensor_sha256':row['tensor_sha256'],'certificate':cert},separators=(',',':'))+'\n')


if __name__ == '__main__':
    main()
