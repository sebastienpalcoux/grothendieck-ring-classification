"""Exact controls for classification certificates and constructive models."""
import os
for var in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[var]='1'
import json,itertools,math,random,copy,time
from pathlib import Path
import sympy as s
from exact import require
P=Path(__file__).resolve().parents[1]
(P/'verification/current').mkdir(parents=True,exist_ok=True)
def main():
 st=time.monotonic();report={};rows=json.load(open(P/'data/census.json'));by={r['id']:r['N'] for r in rows};ledger=json.load(open(P/'data/decisions.json'))
 from gram_vectors_general import native
 rng=random.Random(19092026);cases=0
 for n in range(1,6):
  for _ in range(5):
   V=s.Matrix(n,2,lambda i,j:rng.randrange(3));Q=V*V.T
   if not Q.rank():continue
   ref=[]
   for v in itertools.product(*(range(math.isqrt(int(Q[i,i]))+1) for i in range(n))):
    if not any(v) or any(v[i]*v[j]>Q[i,j] for i in range(n) for j in range(n)):continue
    S=Q-s.Matrix(v)*s.Matrix(v).T
    if all(S.extract(I,I).det()>=0 for k in range(1,n+1) for I in itertools.combinations(range(n),k)):ref.append(v)
   require(tuple(sorted(ref))==native(Q),'native/reference Gram discrepancy');cases+=1
 report['gram_principal_minor_reference_cases']=cases
 from oriented_signed import problem,enumerate_all,from_values,validate_general
 oriented=0
 for rid in ['R6_1_1','R6_2_38']:
  R=by[rid];p=problem(R);ref=[]
  require(math.prod(map(len,p['domains']))<=2000,'reference signed box unexpectedly large')
  for v in itertools.product(*p['domains']):
   T=from_values(R,p,v)
   try:validate_general(T)
   except Exception:continue
   ref.append(v)
  got,p2,stats=enumerate_all(R,30);require(sorted(ref)==got,'oriented native/reference mismatch');oriented+=1
 report['oriented_signed_reference_cases']=oriented
 from positive_models import check_fermionic_cochain,examples
 require(check_fermionic_cochain(),'zesting cochain failed');report['zesting_scalar_identities']=16
 from frontier_feasibility import verify as primal
 o=json.load(open(P/'data/frontier_feasible.json'));require(o['N']==by[o['id']],'frontier tensor mismatch');primal(o['N'],o['certificate']);report['frontier_primal']={'id':o['id'],'center_rank':o['certificate']['center_rank'],'equations':o['certificate']['equations'],'variables':o['certificate']['variables'],'nonzero_rational_coordinates':len(o['certificate']['primal'])}
 # Mutation checks: false signed exhaustion and an altered exact feasible point.
 from check import verify
 bad=copy.deepcopy(next(d for d in ledger if d['certificate']['kind']=='oriented_signed')) if False else None
 mutations=0
 for kind in ['dnumber','zero_spectrum','oriented_signed','weighted_induction']:
  rec=next(d for d in ledger if d.get('certificate',{}).get('kind')==kind);c=copy.deepcopy(rec['certificate'])
  if kind=='dnumber':
   # Reusing a negative arithmetic witness on the pointed cyclic ring must fail.
   R=next(R for name,R,ref in examples() if name=='VecC2 x VecC3')
  elif kind=='zero_spectrum':c['indices']=[0]*9;R=by[rec['id']]
  elif kind=='oriented_signed':c['branches']=c['branches']+[{}];R=by[rec['id']]
  else:c['low_count']+=1;R=by[rec['id']]
  rejected=False
  try:verify(R,c)
  except Exception:rejected=True
  require(rejected,'corrupt certificate was accepted');mutations+=1
 bad=copy.deepcopy(o['certificate']);bad['primal'][0][1]+=1;rejected=False
 try:primal(o['N'],bad)
 except Exception:rejected=True
 require(rejected,'corrupt exact primal was accepted');mutations+=1
 from higher_traces import check_farkas
 require(check_farkas([[1]],[-1],[1],False) and not check_farkas([[1]],[-1],[-1],False) and not check_farkas([[1]],[-1],[1.0],False),'Farkas sign/integer guard failed');report['mutation_and_ray_checks']=mutations+3
 # Census enumeration and its correctness are supplied by the pinned source.
 # Exercise the import identity and prefix checks, without generating any rings.
 from import_repository import verify_source
 report['trusted_repository_import']=verify_source(rows)
 import_mutations=0
 for field in ('id','m','N'):
  changed=list(rows);record=copy.deepcopy(rows[0]);changed[0]=record
  if field=='id':record['id']=rows[1]['id']
  elif field=='m':record['m']+=1
  else:record['N'][1][1][1]+=1
  rejected=False
  try:verify_source(changed)
  except ValueError:rejected=True
  require(rejected,'corrupted repository import was accepted');import_mutations+=1
 report['source_import_mutations_rejected']=import_mutations
 report.update(passed=True,optimized_python=not __debug__,seconds=time.monotonic()-st);out=P/'verification/current'/('certificate_controls_optimized.json' if not __debug__ else 'certificate_controls_normal.json');out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
