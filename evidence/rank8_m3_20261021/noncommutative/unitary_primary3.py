"""Exact negative primary-3 quadratic forms; scope is UNITARY only.

Floating eigensolvers propose integer vectors. Acceptance recomputes the
integer tensor quadratic forms and their sign in the exact FP number field.
No unsuccessful numerical search is a positivity or categorification proof.
"""
from pathlib import Path
import argparse,hashlib,json,sys,time,traceback
import numpy as np
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'supplements/rank8/experimental_signed'))
from exact import require,pc,ec
from scalar_sieve import ScalarCharacters

def exact_form(R,v):
    n=len(R);require(len(v)==n**3 and all(type(x) is int for x in v),'invalid integer witness')
    a=ScalarCharacters(R);f,K,ds,D,pD,emb=a.fp()
    largest=max(map(abs,v),default=0);bound=n**6*max(abs(x) for M in R for row in M for x in row)**3*largest**2
    require(bound<2**62,'int64 quadratic-form range not established')
    vector=np.array(v,dtype=np.int64);coeff=[]
    for M in R:
        A=np.array(M,dtype=np.int64);T=np.kron(np.kron(A,A),A)
        coeff.append(int(vector@(T@vector)))
    value=sum((K(c)/d for c,d in zip(coeff,ds)),K.zero)
    return f,emb,coeff,value

def verify(R,c):
    require(c.get('kind')=='unitary_primary_three_negative' and c.get('scope')=='unitary_only','wrong positivity scope')
    f,emb,coeff,value=exact_form(R,c['integer_vector'])
    require(pc(f)==c['fp_factor'] and coeff==c['quadratic_coefficients'] and ec(value)==c['exact_value'],'primary-3 source arithmetic differs')
    require(emb.sign(value)<0,'primary-3 quadratic form is not negative')

def discover(R):
    from scipy.linalg import eigh
    a=ScalarCharacters(R);f,K,ds,D,pD,emb=a.fp();root=float((emb.lo+emb.hi)/2)
    dims=[float(np.polyval([float(s.Rational(v)) for v in ec(d)],root)) for d in ds]
    require(all(d>0 for d in dims),'numerical FP approximation failed')
    P=np.zeros((len(R)**3,len(R)**3))
    for M,d in zip(R,dims):
        A=np.array(M,dtype=np.float64);P+=np.kron(np.kron(A,A),A)/d
    require(np.max(abs(P-P.T))<1e-8,'primary-3 floating matrix not symmetric')
    ev,vec=eigh(P,subset_by_index=[0,0]);report={'lowest_numerical_eigenvalue':float(ev[0]),'scope':'numerical discovery only'}
    if ev[0]>=-1e-8:return None,report
    for scale in (100,1000,10000):
        v=np.rint(vec[:,0]*scale).astype(np.int64).tolist();f,emb,coeff,value=exact_form(R,v)
        if emb.sign(value)<0:
            cert={'kind':'unitary_primary_three_negative','scope':'unitary_only','integer_vector':v,
                  'fp_factor':pc(f),'quadratic_coefficients':coeff,'exact_value':ec(value)}
            verify(R,cert);return cert,report
    return None,report

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--ring');args=ap.parse_args()
    path=HERE/'unitary_primary3_results.json';census={r['id']:r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text())}
    if not args.write:
        rows=json.loads(path.read_text());count=0
        for row in rows:
            if row.get('certificate'):verify(census[row['id']]['tensor'],row['certificate']);count+=1
        print('PASS',count,'exact unitary-only exclusions');return
    rows=json.loads((HERE.parent/'pipeline/survivors_m3.json').read_text());out=[]
    for source in rows:
        rid=source['id'];row=census[rid]
        if args.ring and rid!=args.ring:continue
        start=time.monotonic();record={'id':rid,'tensor_sha256':row['tensor_sha256']}
        try:
            cert,report=discover(row['tensor']);record.update(outcome='unitary_excluded' if cert else 'no_conclusion',certificate=cert,report=report)
        except Exception as exc:record.update(outcome='error',error=type(exc).__name__+': '+str(exc))
        record['seconds']=round(time.monotonic()-start,6);out.append(record);path.write_text(json.dumps(out,indent=2)+'\n');print(rid,record['outcome'],flush=True)
if __name__=='__main__':main()
