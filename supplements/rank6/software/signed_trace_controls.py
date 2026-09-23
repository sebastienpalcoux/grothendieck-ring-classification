"""Verify cached endpoint reconstruction against independent mixed-sign systems."""
import os,sys
if os.environ.get('SYMPY_GROUND_TYPES') != 'python':
    os.environ['SYMPY_GROUND_TYPES'] = 'python'
    os.execvpe(sys.executable, sys.orig_argv, os.environ)
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from pathlib import Path
import json,time,itertools
from exact import require,poly
from rings import Characters
import signed_spherical_traces as ss
from higher_traces import check_farkas
P=Path(__file__).resolve().parents[1]
(P/'verification/current').mkdir(parents=True,exist_ok=True)
def run():
 st=time.monotonic();rec=json.load(open(P/'certificates/signed_spherical_general.json'))[0];sphere=rec['certificate']['sphere'];R=next(r['N'] for r in json.load(open(P/'data/census.json')) if r['id']==rec['id']);a=Characters(R,sphere['generator']);comp=next(r for r in sphere['characters'] if r['obstruction']['kind']=='signed_spherical_traces');f=poly(comp['factor']);c=comp['obstruction']['certificate'];data,tab=ss.data_and_table(R,a,f,c['table']);systems=cases=0
 for br in c['branches']:
  if not br.get('cases'):continue
  cols=list(map(tuple,br['columns']));L=ss.s.Matrix.hstack(*map(ss.s.Matrix,cols));_,high=ss.high_columns(data,L);sp=ss.Spectrum(tab,cols,high)
  for lab in map(tuple,br['labellings']):
   cache=ss.IndicatorSystems(R,data,tab,cols,6,lab,sp);systems+=1
   # The two independently rebuilt alternating signs cover both values
   # on every second-indicator row. Invariant rows are checked as well.
   for ep in [(-1,1,-1,1,-1),(1,-1,1,-1,1)]:
    A,b=ss.equation_system(R,data,tab,cols,ep,6,lab,sp);AA,bb=cache.system(ep)
    require(A==AA and b==bb,'endpoint reconstruction differs from original equations')
   for case in br['cases']:
    if tuple(case['labelling'])!=lab:continue
    A,b=cache.system(case['indicators']);ss.check_farkas_sparse(A,b,case['y']);cases+=1
   case=next(x for x in br['cases'] if tuple(x['labelling'])==lab);A,b=cache.system(case['indicators']);check_farkas(A,b,case['y'])
   print('verified label',systems,'cases',cases,flush=True)
 require(systems==4 and cases==128,'signed finite inventory')
 return {'passed':True,'optimized_python':not __debug__,'seconds':time.monotonic()-st,'labelled_frames':systems,'full_mixed_sign_reconstructions':2*systems,'exact_sign_cases':cases,'dense_sparse_comparisons':systems,'scope':'Exact equality of reconstructed matrices and right sides, plus every saved Farkas inequality; no numerical optimizer.'}
if __name__=='__main__':
 z=run();name='signed_trace_controls_optimized.json' if not __debug__ else 'signed_trace_controls_normal.json';(P/'verification/current'/name).write_text(json.dumps(z,indent=2)+'\n');print(json.dumps(z,indent=2))
