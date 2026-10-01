"""Independent optimized-Python replay of all extra-M9 accepted certificates."""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
import argparse,hashlib,importlib,json,signal,subprocess,sys,time,traceback
from pathlib import Path

def sha(x):return hashlib.sha256(json.dumps(x,separators=(',',':'),sort_keys=True).encode()).hexdigest()

def worker(task):
    root,row,rec=task;sys.path.insert(0,str(Path(root)/'software'))
    import scipy.optimize as opt
    def denied(*a,**kw):raise RuntimeError('optimizer forbidden in exact replay')
    opt.linprog=opt.milp=denied
    out=dict(id=row['id'],m=row['m'],tensor_sha256=sha(row['N']),certificate_sha256=sha(rec['certificate']),optimized_python=not __debug__)
    start=time.monotonic()
    try:
        if row['m']!=9 or row['id']!=rec['id'] or out['tensor_sha256']!=rec['tensor_sha256']:raise ValueError('source mismatch')
        allowed={'new_trace_ideal.verify','new_ramified_signed.verify','new_biquadratic_trace.verify','round3_arithmetic.verify','round3_noncommutative.verify','full_morita_gram.verify','round3_smallest.verify','stabilizer_rotation.verify_general','stabilizer_rotation_higher.verify_general','round3_integral_morita.verify_general','round3_verlinde.verify_general','cyclotomic_stabilizer_trace.verify_general','oriented_extension.verify','check.verify'}
        name=rec['verifier']
        if name not in allowed:raise ValueError('unsupported exact verifier')
        mod,fn=name.rsplit('.',1);getattr(importlib.import_module(mod),fn)(row['N'],rec['certificate'])
        out.update(passed=True,optimizer_used=False)
    except Exception as exc:out.update(passed=False,diagnostic=type(exc).__name__+': '+str(exc),traceback=traceback.format_exc())
    out['seconds']=time.monotonic()-start
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--certificates',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--deadline',type=int,default=840);args=ap.parse_args()
    if not 1<=args.deadline<=840:ap.error('deadline 1..840')
    census=args.root/'data/census.json';rows={r['id']:r for r in json.loads(census.read_text())}
    certs=[json.loads(l) for l in args.certificates.read_text().splitlines()];results=[]
    for rec in certs:
        row=rows[rec['id']];start=time.monotonic()
        with subprocess.Popen([sys.executable,'-O',str(Path(__file__).resolve()),'--worker'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True) as p:
            try:
                stdout,stderr=p.communicate(json.dumps((str(args.root.resolve()),row,rec)),timeout=args.deadline)
                if p.returncode:raise RuntimeError('worker exit '+str(p.returncode)+': '+stderr[-3000:])
                z=json.loads(stdout)
            except subprocess.TimeoutExpired:
                os.killpg(p.pid,signal.SIGKILL);p.communicate();z=dict(id=row['id'],m=row['m'],passed=False,diagnostic='hard replay deadline',tensor_sha256=sha(row['N']),certificate_sha256=sha(rec['certificate']))
            except Exception as exc:z=dict(id=row['id'],m=row['m'],passed=False,diagnostic=str(exc),tensor_sha256=sha(row['N']),certificate_sha256=sha(rec['certificate']))
        z['wall_seconds']=time.monotonic()-start;results.append(z);print(row['id'],z['passed'],round(z['wall_seconds'],2),flush=True)
        report=dict(complete=len(results)==len(certs),passed=len(results)==len(certs) and all(z['passed'] for z in results),count=len(certs),optimized_python=True,optimizer_disabled=True,
                    census_sha256=hashlib.sha256(census.read_bytes()).hexdigest(),certificates_sha256=hashlib.sha256(args.certificates.read_bytes()).hexdigest(),results=results)
        args.output.write_text(json.dumps(report,indent=2)+'\n')
    if not certs:
        report=dict(complete=True,passed=True,count=0,optimized_python=True,optimizer_disabled=True,census_sha256=hashlib.sha256(census.read_bytes()).hexdigest(),certificates_sha256=hashlib.sha256(args.certificates.read_bytes()).hexdigest(),results=[])
        args.output.write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':
    if '--worker' in sys.argv:print(json.dumps(worker(json.load(sys.stdin))))
    else:main()
