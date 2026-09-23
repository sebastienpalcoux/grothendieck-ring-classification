"""Exact literature identifications and five-status separation controls."""
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[variable] = '1'
import copy
import json
import time
from pathlib import Path
from exact import require
from rings import permute, dual
from oriented_signed import validate_general
from literature_models import examples, schopieray, h8_extension, free_involution_quotient
from positive_models import ng2
from existence import verify_ledger
ROOT=Path(__file__).resolve().parents[1]
(ROOT/'verification/current').mkdir(parents=True,exist_ok=True)


def adjoint_series(R):
    """Fusion-support computation, not an existence test for an abstract ring."""
    validate_general(R)
    n=len(R);star=dual(R);current=set(range(n));series=[]
    while True:
        series.append(sorted(current))
        if current=={0}:return series
        nxt={0}
        for i in current:
            nxt.update(k for k in current if R[i][star[i]][k])
        while True:
            larger=nxt|{star[i] for i in nxt}|{k for i in nxt for j in nxt for k in current if R[i][j][k]}
            if larger==nxt:break
            nxt=larger
        if nxt==current:return series
        require(nxt<current,'adjoint support increased')
        current=nxt


def must_reject(fn,description):
    try:fn()
    except Exception:return
    raise RuntimeError('Mutation accepted: '+description)


def main():
    start=time.monotonic()
    rows={r['id']:r for r in json.loads((ROOT/'data/census.json').read_text())}
    ledger=json.loads((ROOT/'data/decisions.json').read_text());now={r['id']:r for r in ledger}
    saved=json.loads((ROOT/'data/literature_positive_models.json').read_text())
    byname={r['name']:r for r in saved}
    constructed=list(examples());require(len(constructed)==len(byname)==4,'literature model count')
    matched=[]
    for name,R,source,existence in constructed:
        r=byname[name];validate_general(R,nonnegative=True)
        require(R==r['N'] and source==r['reference'] and existence==r['existence'],'literature source differs from constructor')
        require(permute(R,r['basis_permutation'])==rows[r['id']]['N'],'published fusion table mismatch')
        matched.append({'id':r['id'],'basis_permutation':r['basis_permutation'],'coefficients':216,'existence':existence})
        bad=copy.deepcopy(R);bad[1][1][0]+=1
        must_reject(lambda:validate_general(bad,nonnegative=True),'changed source tensor')
    require(permute(schopieray(),[0,5,2,4,1,3])==rows['R6_2_124']['N'],'earlier stated permutation was invalid')
    from prepare import key
    require(key(rows['R6_2_98']['N'])!=key(rows['R6_2_41']['N']),'distinct same-dimension tensors were conflated')
    series=adjoint_series(h8_extension())
    require(series==[[0,1,2,3,4,5],[0,1,2,3,4],[0,1,2,3],[0]],'H8-extension nilpotency certificate mismatch')
    must_reject(lambda:free_involution_quotient(ng2(0),1),'Ising fermion has a fixed point')
    verify_ledger(ledger)
    # Each bad ledger has an otherwise unchanged complete census.
    for changes in [{'status':'unitarily_realized'}, {'existence':{k:'yes' for k in now['R6_2_124']['existence']}},
                    {'status':'excluded','existence':{k:'no' for k in now['R6_2_124']['existence']}},
                    {'status':'unresolved','existence':{k:'unknown' for k in now['R6_2_124']['existence']}}]:
        bad=copy.deepcopy(ledger)
        next(r for r in bad if r['id']=='R6_2_124').update(changes)
        must_reject(lambda:verify_ledger(bad),'Schopieray five-status separation')
    remaining=[r['id'] for r in ledger if r['m']==2 and r['status']=='unresolved']
    require(remaining==[],'multiplicity-two classification is not complete')
    report={'passed':True,'optimized_python':not __debug__,'seconds':time.monotonic()-start,
            'matched_models':matched,'full_tensor_coefficients_checked':864,'h8_adjoint_series':series,
            'mutations_rejected':9,'multiplicity_two_residuals':remaining,
            'scope':'Exact source-table identifications and theorem-hypothesis checks; cited associators and categorical nonexistence theorems remain literature inputs.'}
    dest=ROOT/'verification/current'/('literature_controls_optimized.json' if not __debug__ else 'literature_controls_normal.json')
    dest.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
