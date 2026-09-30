"""Construct and verify the three neutral conformal-embedding models.

The arithmetic reconstructs full tensors from source fusion graphs or affine
branching data. The accompanying mathematical proofs establish the existence
of the unitary module categories and select the categorical completions.
Run ``python -O software/conformal_models.py --verify`` for fresh exact checks.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys, time
import sympy as sp
from exact import require

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'research/structural_models'
REGISTRY = ROOT/'data/conformal_positive_models.json'
SCRIPTS = ('quartic/reconstruct_b2_7.py', 'r629/complete_from_generator.py',
           'r629/check_center_dimensions.py', 'c3_model/exact_certificate.py',
           'c3_model/complete_tensor.py')


def load(relative):
    return json.loads((BASE/relative).read_text())


def examples():
    a = load('quartic/b2_7_tensor_certificate.json')
    require(a['all_tensor_entries_match'] and a['associativity_checked'],
            'Incomplete B2 level-seven reconstruction')
    yield 'R6_4_22', 'Neutral modules for (B2)_7 ⊂ (D7)_1', a['tensor'], \
          'Coquereaux–Rais–Tahri, arXiv:1001.5416, §3.5; manuscript conformal-model theorem'
    b = load('c3_model/completion_certificate.json')
    require(len(b)==2, 'Incomplete C3 duality alternatives')
    candidates=[s['fusion_tensor'] for r in b if r['star']==[0,2,1,3,4,5]
                for s in r['solutions']]
    require(len(candidates)==1, 'C3 non-self-dual completion is not unique')
    yield 'R6_4_91', 'Neutral modules for (C3)_4 ⊂ (B10)_1', candidates[0], \
          'Cellini–Kac–Möseneder Frajria–Papi, arXiv:math-ph/0506043; manuscript conformal-model theorem'
    c = load('r629/fusion_completion.json')
    rows=[r for r in c if r['star']==list(range(6))]
    require(len(rows)==1 and len(rows[0]['free'])==1, 'B2 level-twelve completion domain')
    r=rows[0]; variable=sp.Symbol(r['free'][0])
    tensor=[[[int(sp.sympify(v).subs(variable,2)) for v in row] for row in m]
            for m in r['matrices']]
    center=load('r629/center_dimension_certificate.json')
    require(center['formal_codegree3_impossible'] and center['formal_codegree15_impossible'],
            'The other B2 level-twelve completions have not been eliminated')
    yield 'R6_4_629', 'Neutral modules for (B2)_12 ⊂ (E8)_1', tensor, \
          'Coquereaux–Rais–Tahri, arXiv:1001.5416, §3.6; manuscript conformal-model theorem'


def build_registry():
    from oriented_signed import validate_general
    census={r['id']:r for r in json.loads((ROOT/'data/census.json').read_text())}
    result=[]
    for rid,name,tensor,reference in examples():
        validate_general(tensor)
        require(tensor==census[rid]['N'], 'Full conformal-model tensor mismatch: '+rid)
        result.append(dict(id=rid,name=name,N=tensor,reference=reference,
            proof='papers/conformal_models.tex',
            verification='python -O software/conformal_models.py --verify',
            existence={s:'yes' for s in ('general','pivotal','spherical','pseudo_unitary','unitary')},
            schema='rank6-conformal-model/v1'))
    REGISTRY.write_text(json.dumps(result,indent=2)+'\n')
    return result


def verify(fresh=False):
    reports=[]
    if fresh:
        for script in SCRIPTS:
            start=time.monotonic()
            proc=subprocess.run([sys.executable,'-O',str(BASE/script)],cwd=BASE,
                                capture_output=True,text=True,timeout=900)
            require(proc.returncode==0,script+' failed:\n'+proc.stdout[-3000:]+proc.stderr[-3000:])
            reports.append(dict(script=script,seconds=round(time.monotonic()-start,3),passed=True))
            print('Verified',script,flush=True)
    saved=json.loads(REGISTRY.read_text()) if REGISTRY.exists() else None
    constructed=build_registry()
    require(saved is None or saved==constructed,'Conformal constructor registry changed')
    result=dict(passed=True,fresh_arithmetic_replay=fresh,models=3,full_tensor_coefficients=648,
                ids=[r['id'] for r in constructed],scripts=reports,
                categorical_input='Actual unitary conformal-embedding module categories; see papers/conformal_models.tex.',
                source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted(BASE.rglob('*')) if p.is_file() and p.suffix in ('.py','.json','.md')})
    out=ROOT/'verification/current/conformal_models.json';out.parent.mkdir(parents=True,exist_ok=True)
    if fresh or not out.exists():out.write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true',help='Fresh exact source and tensor reconstruction')
    args=parser.parse_args()
    print(json.dumps(verify(fresh=args.verify),indent=2))
