from pathlib import Path
import argparse,json,sys,time,hashlib,inspect
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--id',required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--capture-y-from',type=Path);p.add_argument('--stop-after-capture',action='store_true');a=p.parse_args()
r=a.repo/'supplements/rank6';sys.path.insert(0,str(r/'software'))
import scipy.optimize
scipy.optimize.linprog=lambda *a,**kw: (_ for _ in ()).throw(RuntimeError('optimizer forbidden'))
scipy.optimize.milp=scipy.optimize.linprog
import higher_traces
original=higher_traces.check_farkas
class CaptureReached(Exception):pass
calls=[]
capture_y=json.loads(a.capture_y_from.read_text())['y'] if a.capture_y_from else None
def diagnosed(A,b,y,raise_error=True):
    if capture_y is not None and y==capture_y:
        a.out.with_suffix('.captured_system.json').write_text(json.dumps({'A':A,'b':b,'y':y}))
        if a.stop_after_capture:
            original(A,b,y)
            raise CaptureReached('Selected exact matrix and unchanged ray captured and verified; complete certificate not replayed by this invocation')
    ok=original(A,b,y,False)
    sup=[(i,v) for i,v in enumerate(y) if v]
    if not ok:
        vals=[sum(A[i][j]*v for i,v in sup) for j in range(len(A[0]))]
        details={'rows':len(A),'cols':len(A[0]),'len_y':len(y),'bTy':sum(b[i]*v for i,v in sup),'min_ATy':min(vals),'negative_columns':[[j,v] for j,v in enumerate(vals) if v<0][:50],'support':sup,'caller':[]}
        for f in inspect.stack()[1:5]:
            lo=f.frame.f_locals
            details['caller'].append({'function':f.function,'file':Path(f.filename).name,'line':f.lineno,'positions':{k:lo[k] for k in ['ix','g','x','height','lab','ep','objects','cols'] if k in lo and isinstance(lo[k],(list,tuple,int,bool,type(None)))}})
        a.out.with_suffix('.failure_system.json').write_text(json.dumps({'A':A,'b':b,'y':y,'details':details},default=str))
        calls.append(details)
    return original(A,b,y,raise_error)
higher_traces.check_farkas=diagnosed
rows=json.loads((r/'data/census.json').read_text());ledger=json.loads((r/'data/decisions.json').read_text())
R=next(x['N'] for x in rows if x['id']==a.id);c=next(x['certificate'] for x in ledger if x['id']==a.id)
from check import verify
start=time.monotonic()
try:verify(R,c);ans={'id':a.id,'status':'PASS'}
except CaptureReached as e:ans={'id':a.id,'status':'CAPTURED_SELECTED_MATRIX','scope':str(e)}
except Exception as e:ans={'id':a.id,'status':'FAIL','error':str(e),'details':calls}
ans['seconds']=time.monotonic()-start
ans['source_files_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [r/'software/higher_traces.py',r/'software/stabilizer_rotation_higher.py',r/'software/round3_integral_morita.py',r/'software/round4_higher_e6.py']}
import sympy,os
ans['environment']={'sympy':sympy.__version__,'ground_types':os.environ.get('SYMPY_GROUND_TYPES'),'pythonpath':os.environ.get('PYTHONPATH')}
try:
 import flint
 ans['environment']['flint']=flint.__version__
except ImportError:pass
a.out.write_text(json.dumps(ans,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in ans.items() if k!='details'},indent=2,default=str))
