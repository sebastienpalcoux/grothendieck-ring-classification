"""Exact scalar-character sieve, including all oriented sphericalizations.

Reconstructed after workspace cleanup. Every certificate is regenerated from
the source tensor; historical counts are not used as proof inputs.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,sys,time,traceback
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'supplements/rank8/experimental_signed'))
from exact import require,field,t,pc,ec,embeddings
from rings import matrices,dual,casimir,flat
import proofs
from oriented_signed import enumerate_all,from_values,validate_general

class ScalarCharacters:
    def __init__(self,R,k=None):
        self.R=R;self.n=n=len(R);self.N=N=matrices(R);self.du=dual(R)
        basis=s.Matrix.vstack(*(N[i]*N[j]-N[j]*N[i] for i in range(n) for j in range(i))).nullspace()
        self.scalar_rank=m=len(basis)
        require(m>0,'no scalar characters')
        W=s.Matrix.hstack(*basis);piv=list(W.T.rref()[1]);J=W.extract(piv,range(m)).inv()
        A=[J*(a*W).extract(piv,range(m)) for a in N]
        require(all(a*W==W*b for a,b in zip(N,A)),'scalar space not invariant')
        require(all(a*b==b*a for a in A for b in A),'scalar quotient not commutative')
        for u in ([k] if k is not None else range(1,m*(m-1)*(n-2)//2+2)):
            H=A[0]+sum((u**(i-1)*A[i] for i in range(1,n)),s.zeros(m))
            p=H.charpoly(t).as_poly()
            if s.gcd(p,p.diff()).degree()==0:break
        else:raise ValueError('scalar separation failed')
        require(s.gcd(p,p.diff()).degree()==0,'nonseparating scalar element')
        V=s.Matrix.hstack(*(s.Matrix(list(H**j)) for j in range(m)))
        coeff=[list(V.gauss_jordan_solve(s.Matrix(list(a)))[0]) for a in A]
        require(all(sum((c[j]*H**j for j in range(m)),s.zeros(m))==a for c,a in zip(coeff,A)),'scalar polynomial coordinates')
        C=casimir(R);SC=sum((A[i]*A[self.du[i]] for i in range(n)),s.zeros(m));q=SC.charpoly(t).as_poly()
        cf=list(q.factor_list()[1]);fe=None
        if m!=n:
            require(n==8 and m==4,'only rank-eight C^4 plus M2 supported')
            quotient,rem=s.div(C.charpoly(t).as_poly(),q)
            require(rem.is_zero,'scalar Casimir does not divide full Casimir')
            ff=quotient.factor_list()[1]
            require(len(ff)==1 and ff[0][0].degree()==1 and ff[0][1]==4,'unique M2 block not verified')
            z=ff[0][0];fe=-s.Rational(z.TC(),2*z.LC())
            require(fe.q==1 and fe>0,'matrix-block formal codegree not positive integral')
            cf.append((s.Poly(t-fe,t,domain=s.QQ),1))
        self.W=W;self.A=A;self.H=H;self.k=u;self.p=p;self.components=p.factor_list()[1]
        self.coeff=coeff;self.C=C;self.scalar_codegree_poly=q;self.matrix_codegree=fe;self.cf=cf

    def component(self,f):
        K=field(f)
        ds=[K(s.Poly.from_list(list(reversed(c)),t,domain=s.QQ).rem(f).all_coeffs()) for c in self.coeff]
        require(all(ds[i]*ds[j]==sum((K(self.R[i][j][h])*ds[h] for h in range(self.n)),K.zero) for i in range(self.n) for j in range(self.n)),'scalar character multiplication')
        D=sum((ds[i]*ds[self.du[i]] for i in range(self.n)),K.zero)
        pD=proofs.multiplication_matrix(D,K,f).charpoly(t).as_poly().sqf_part()
        return K,ds,D,pD

    def fp(self):
        choices=[]
        for f,m in self.components:
            K,ds,D,pD=self.component(f)
            for emb in embeddings(f):
                if all(emb.sign(d)>0 for d in ds):choices.append((f,K,ds,D,pD,emb))
        require(len(choices)==1,'unique positive character not verified')
        return choices[0]

def character_obstructions(R,required):
    a=ScalarCharacters(R);out=[]
    for f,m in a.components:
        K,ds,D,pD=a.component(f)
        zero=next((i for i,d in enumerate(ds) if not d),None)
        unequal=next((i for i,d in enumerate(ds) if d!=ds[a.du[i]]),None)
        if zero is not None:why={'kind':'zero','object':zero}
        elif unequal is not None:why={'kind':'duality','object':unequal}
        else:why=proofs.norm_failure(pD,required) or proofs.field_failure(f,required)
        out.append({'factor':pc(f),'obstruction':why})
    return out

def discover(R,timeout=120):
    a=ScalarCharacters(R);sphere=character_obstructions(R,a.cf)
    report={'scalar_rank':a.scalar_rank,'original_components':len(sphere)}
    if any(b['obstruction'] is None for b in sphere):return None,report
    vals,p,stats=enumerate_all(R,timeout);branches=[]
    for v in vals:
        T=from_values(R,p,v);validate_general(T);b={'values':list(v)}
        why=proofs.signed_adjoint_parity(R,T);gauge=proofs.gauge_original(T,R)
        if why:b['obstruction']=why
        elif gauge is not None:b['obstruction']={'kind':'gauge_original','signs':gauge}
        else:
            aa=ScalarCharacters(T);cc=character_obstructions(T,a.cf+aa.cf)
            if any(c['obstruction'] is None for c in cc):return None,dict(report,signed_count=len(vals),surviving_signed_values=list(v))
            b['characters']=cc
        branches.append(b)
    return {'kind':'rank8_scalar_oriented','sphere':sphere,'branches':branches},dict(report,signed_count=len(vals))

def signed_component_certificate(R,T):
    original=ScalarCharacters(R);signed=ScalarCharacters(T)
    branches=character_obstructions(T,original.cf+signed.cf)
    if any(b['obstruction'] is None for b in branches):return None
    return {'kind':'noncommutative_signed','characters':branches}

def verify(R,c):
    require(c.get('kind')=='rank8_scalar_oriented','wrong scalar proof kind')
    expected,_=discover(R,timeout=1200)
    require(expected is not None and expected==c,'scalar proof did not replay completely')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--ring');a=ap.parse_args()
    path=HERE/'results.json';source=HERE.parent/'pipeline/survivors_m3.json'
    rows=json.loads(source.read_text());rows=list(rows.values()) if isinstance(rows,dict) else rows
    census={r['id']:r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text())}
    if not a.write:
        for row in json.loads(path.read_text()):
            if row.get('certificate'):verify(census[row['id']]['tensor'],row['certificate'])
        print('PASS: exact scalar certificates');return
    out=[]
    for row in rows:
        rid=row['id'];row=census[rid];R=row['tensor']
        if a.ring and rid!=a.ring:continue
        if all(R[i][j]==R[j][i] for i in range(8) for j in range(8)):continue
        start=time.monotonic();record={'id':rid,'tensor_sha256':row['tensor_sha256'],'scope':'general_complex_fusion_category'}
        try:
            cert,report=discover(R);record.update(outcome='excluded' if cert else 'no_conclusion',certificate=cert,report=report)
        except Exception as e:record.update(outcome='error',error=type(e).__name__+': '+str(e))
        record['seconds']=round(time.monotonic()-start,6);out.append(record)
        path.write_text(json.dumps(out,indent=2)+'\n');print(rid,record['outcome'],flush=True)
if __name__=='__main__':main()
