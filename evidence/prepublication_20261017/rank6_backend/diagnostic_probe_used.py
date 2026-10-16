import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[name]='1'
from pathlib import Path
import sys,json,gzip,time,argparse,hashlib,traceback
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'software'))
import higher_traces as H
from sympy.external.gmpy import GROUND_TYPES
import flint
parser=argparse.ArgumentParser();parser.add_argument('case');parser.add_argument('--capture-call',type=int);parser.add_argument('--tag',required=True);args=parser.parse_args()
case=json.loads((P/'cases.json').read_text())[args.case]
original=H.check_farkas;calls=0;start=time.monotonic()
def diagnostic(A,b,y,raise_error=True):
 global calls
 calls+=1
 passed=original(A,b,y,False)
 if not passed or args.capture_call==calls:
  vals=[sum(A[i][j]*y[i] for i in range(len(b))) for j in range(len(A[0]))]
  result={'case':args.case,'call':calls,'passed':passed,'rows':len(A),'columns':len(A[0]),'bTy':str(sum(t*v for t,v in zip(b,y))),'negative_columns':[(j,str(v)) for j,v in enumerate(vals) if v<0],'ground_types':GROUND_TYPES,'flint':flint.__version__,'flint_file':flint.__file__,'seconds':time.monotonic()-start}
  with gzip.open(P/(args.tag+'.system.json.gz'),'wt') as out:json.dump({'result':result,'A':A,'b':b,'y':y},out,default=str)
  (P/(args.tag+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
  if args.capture_call==calls:raise SystemExit(0 if passed else 1)
 return original(A,b,y,raise_error)
H.check_farkas=diagnostic
import stabilizer_rotation_higher as S
try:
 S.verify_general(case['tensor'],case['certificate'])
 print(json.dumps({'case':args.case,'passed':True,'complete':True,'calls':calls,'seconds':time.monotonic()-start,'ground_types':GROUND_TYPES,'flint':flint.__version__}),flush=True)
except Exception:
 traceback.print_exc();raise SystemExit(1)
