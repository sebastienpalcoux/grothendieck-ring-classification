"""Exact rank-eight weighted induction using C^4 + M2 character data."""
from pathlib import Path
from fractions import Fraction as Q
from types import SimpleNamespace
import argparse,importlib.util,itertools,json,math,sys,time
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'supplements/rank8/experimental_signed'))
from exact import require,t,ec,discover_roots,check_roots
from scalar_sieve import ScalarCharacters
from weighted_data_fast import low_frames
spec=importlib.util.spec_from_file_location('rank6_weighted_core',ROOT/'supplements/rank6/software/weighted_induction.py')
core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)

def spectral(R):
    a=ScalarCharacters(R);n=len(R);require(n==8,'rank eight required')
    f,K,ds,D,pD,emb=a.fp();roots=discover_roots(a.scalar_codegree_poly,K)
    require(roots is not None,'scalar formal codegrees do not split in FP field')
    check_roots(a.scalar_codegree_poly,K,roots);require(D in roots,'FP codegree absent');roots.remove(D)
    codegrees=[D]+roots;multiplicities=[1]*len(codegrees)
    if a.matrix_codegree is not None:codegrees.append(K(a.matrix_codegree));multiplicities.append(2)
    require(sum(r*r for r in multiplicities)==n,'Wedderburn dimensions incomplete')
    B=s.zeros(n)
    for j,i in itertools.product(range(n),repeat=2):
        B[j,i]=sum(R[u][j][v]*R[v][a.du[u]][i] for u,v in itertools.product(range(n),repeat=2))
    require(B==B.T,'induction Gram not symmetric')
    return dict(n=n,N=a.N,du=a.du,generator=a.k,factor=f,K=K,ds=ds,D=D,embedding=emb,
                Casimir=a.C,Gram=B,codegrees=codegrees,multiplicities=multiplicities)

def data(R):
    a=spectral(R);n=a['n'];K=a['K'];f=a['factor'];D=a['D'];ds=a['ds'];B=a['Gram']
    require(f.degree() in (1,2),'rational/quadratic FP field required')
    cs=[core.restriction(ds,D/fc,r,K,B) for fc,r in zip(a['codegrees'][1:],a['multiplicities'][1:])]
    lows=low_frames(cs,a['multiplicities'][1:],B)
    if f.degree()==1:
        q=1;conductor=1
        def coords(x):return (Q(str(ec(x)[0])) if x else Q(0),Q(0))
    else:
        co=list(map(int,f.all_coeffs()));disc=co[1]**2-4*co[2]
        q=math.prod(int(p) for p,e in s.factorint(disc).items() if e%2);h=math.isqrt(disc//q);conductor=q if q%4==1 else 4*q
        def coords(x):
            z=list(map(lambda v:Q(str(v)),ec(x)));z=[Q(0)]*(2-len(z))+z
            return z[1]-Q(co[1],2)*z[0],Q(h,2)*z[0]
    dims=list(map(coords,ds));dd=coords(D);norm=dd[0]**2-q*dd[1]**2
    require(norm.denominator==1,'nonintegral dimension norm')
    primes=sorted(map(int,s.factorint(abs(norm.numerator))))
    return dict(a,ch=SimpleNamespace(n=n,C=B,du=a['du']),q=q,conductor=conductor,
                dimensions=dims,global_dimension=dd,primes=primes,columns=cs,lows=lows)
core.spectral=spectral;core.data=data
def discover(R,height=6):return core.certificate(R,height)
def verify(R,c):return core.verify(R,c)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--ring');args=ap.parse_args()
    census={r['id']:r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text())};path=HERE/'weighted_results.json'
    if not args.write:
        for row in json.loads(path.read_text()):
            if row.get('certificate'):verify(census[row['id']]['tensor'],row['certificate'])
        print('PASS: weighted induction certificates');return
    survivors=json.loads((HERE.parent/'pipeline/survivors_m3.json').read_text());out=[]
    for rec in survivors:
        row=census[rec['id']];R=row['tensor'];rid=row['id']
        if args.ring and rid!=args.ring:continue
        if all(R[i][j]==R[j][i] for i in range(8) for j in range(8)):continue
        result={'id':rid,'tensor_sha256':row['tensor_sha256'],'scope':'general_complex_fusion_category'};start=time.monotonic()
        try:
            a=spectral(R)
            if core.gate(a) is None:result.update(outcome='ineligible',reason='no general-to-pseudo-unitary gate')
            else:
                cert=discover(R);result.update(outcome='excluded' if cert else 'no_conclusion',certificate=cert)
                if cert:verify(R,cert)
        except Exception as e:result.update(outcome='error',error=type(e).__name__+': '+str(e))
        result['seconds']=round(time.monotonic()-start,6);out.append(result);path.write_text(json.dumps(out,indent=2)+'\n');print(rid,result['outcome'],flush=True)
if __name__=='__main__':main()
