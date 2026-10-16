#!/usr/bin/env python3
"""Independent exact finite and scalar regression checks.

This supplements, and does not replace, supplementary/classification/verify_compact.py.
It does not formalize the categorical proofs.
"""


def _require(condition, message):
    if not condition:
        raise RuntimeError(message)

from pathlib import Path
import ast,gzip,json,subprocess,sys,tempfile,time
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
SOFT=ROOT/'supplementary/classification/software'
sys.path.insert(0,str(SOFT))
from rings import sd_tensor,sd_tuple,permute,PERMS,SD_MASKS,SD_PERM_MAPS,validate,codegree_poly,dnumber
from rapid import casimir_polynomial,dnumber as fast_dnumber,BACKEND
started=time.monotonic()
report={'scope':'Independent exact regression checks; not categorical proof formalization.'}

# Recompute every displayed dimension identity, rather than accepting old flags.
models=json.loads((ROOT/'supplementary/classification/data/models.json').read_text())
old=json.loads((ROOT/'supplementary/classification/verification/exact_model_dimensions_audit.json').read_text())
expressions={row['model']:row for row in old}
model_results=[]
for model in models:
    name=model['name'] if 'name' in model else model['model']
    R=model['matrices'];validate(R)
    row=expressions[name]
    ds=[s.sympify(x,locals={'t':s.Symbol('t')}) for x in row['fp_dimensions_in_model_basis']]
    _require(all(d.is_positive is True for d in ds), (name,'positivity'))
    extensions=[d for d in ds if not d.is_Rational]
    K=s.QQ.algebraic_field(*extensions) if extensions else s.QQ
    dd=[K.from_sympy(d) for d in ds]
    for i in range(4):
        for j in range(4):
            _require(dd[i]*dd[j]==sum((R[i][j][k]*dd[k] for k in range(4)),K.zero), (name,i,j))
    D=s.sympify(row['global_fp_dimension'],locals={'t':s.Symbol('t')})
    _require(sum((d*d for d in dd),K.zero)==K.from_sympy(D), (name,'global dimension'))
    model_results.append({'model':name,'character_products_checked':16,
                          'positive_dimensions_proved':True,'global_dimension_checked':True})
report['exact_models']=model_results
print('PASS all fifteen model character and global dimension identities.',flush=True)

# All 48 signed permutations, independently checked against tensor transforms.
def canon(q):
    return min(tuple(q[mapping[k]]*(-1 if (mask&SD_MASKS[k]).bit_count()%2 else 1)
                     for k in range(10)) for mapping in SD_PERM_MAPS for mask in range(8))
q=tuple(range(-5,5));R=sd_tensor(q)
for pp,mapping in zip(PERMS,SD_PERM_MAPS):
    _require(sd_tuple(permute(R,pp))==tuple(q[k] for k in mapping), 'audit/check_regressions.py exact check failed at source line 48')
    for mask in range(8):
        eps=[1]+[-1 if mask&(1<<j) else 1 for j in range(3)]
        A=permute(R,pp)
        B=[[[eps[i]*eps[j]*eps[k]*A[i][j][k] for k in range(4)] for j in range(4)] for i in range(4)]
        _require(sd_tuple(B)==tuple(q[mapping[k]]*(-1 if (mask&SD_MASKS[k]).bit_count()%2 else 1) for k in range(10)), 'audit/check_regressions.py exact check failed at source line 53')

# Compare the optimized Diophantine enumeration with literal ten-variable search.
def tuples(text):
    return [tuple(map(int,line.split()[1:])) for line in text.splitlines() if line.startswith('S ')]
independent=[];small=[]
with tempfile.TemporaryDirectory(prefix='rank4-independent-') as td:
    td=Path(td)
    for source,target in [('enumerate_global_signed.cpp','fast'),('enumerate_global_signed_reference.cpp','reference')]:
        subprocess.run(['g++','-O3','-std=c++17','-fopenmp',str(SOFT/source),'-o',str(td/target)],check=True)
    for bound in (1,2):
        fast=tuples(subprocess.check_output([str(td/'fast'),str(bound),'2'],text=True,stderr=subprocess.DEVNULL))
        ref=tuples(subprocess.check_output([str(td/'reference'),str(bound)],text=True))
        F={canon(q) for q in fast};G={canon(q) for q in ref}
        _require(len(fast)==len(F) and F==G, (bound,'enumeration mismatch'))
        independent.append({'bound':bound,'signed_orbits':len(F),'raw_reference_tables':len(ref),'exact_set_equality':True})
        small.extend(sorted(F))
report['independent_enumerations']=independent
print('PASS optimized/reference signed orbit sets at bounds one and two.',flush=True)

# The fallback's Newton identities and divisibilities against independent SymPy matrices.
with gzip.open(ROOT/'supplementary/classification/data/signed_universal.jsonl.gz','rt') as f:
    retained=[tuple(json.loads(line)['tuple']) for line in f]
all_checks=list(dict.fromkeys(retained+small))
for index,q in enumerate(all_checks,1):
    R=sd_tensor(q)
    _require(tuple(reversed(tuple(map(int,codegree_poly(R).all_coeffs()))))==tuple(map(int,casimir_polynomial(R))), 'audit/check_regressions.py exact check failed at source line 79')
    _require((dnumber(R) is None)==(fast_dnumber(R) is None), 'audit/check_regressions.py exact check failed at source line 80')
    if index%500==0:print('Independent arithmetic comparisons',index,flush=True)
report['universal_arithmetic_comparisons']={'backend':BACKEND,'tables':len(all_checks),
    'characteristic_polynomials_match':True,'dnumber_decisions_match':True,
    'flint_backend_executed':BACKEND=='python-flint'}
subprocess.run([sys.executable,str(ROOT/'audit/check_shortcut_algebra.py')],check=True)
report['shortcut_scalar_algebra']=True
for path in ROOT.rglob('*.py'):
    if 'history' not in path.parts:ast.parse(path.read_text(),filename=str(path))
report['python_syntax']=True
report['passed']=True
report['elapsed_seconds']=round(time.monotonic()-started,3)
(ROOT/'audit/exact_regression_results.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS exact regression checks.',flush=True)
