#!/usr/bin/env python3
"""Independent consistency checks, not exclusions, of two forced center blocks."""
import hashlib,json,sys
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=Path('/workspace/scratch/90f37cc83103/online_revision/grothendieck-ring-classification')
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'evidence/rank8_creative_20261022/r1154'))
import verify_semionic_packet as p
sys.path.insert(0,str(ROOT/'evidence/rank8_creative_20261022/unified'))
import verify_r1768_weil as w

def need(ok,why):
    if not ok:raise ValueError(why)

def check_1154():
    l=p.l;path=ROOT/'evidence/rank8_creative_20261022/r1154/semionic_packet.json'
    rows=json.loads(path.read_text())['results'];out=[]
    for r in rows:
        b=p.build_at(r['pattern'],r['pair_histogram']);labels=b['labels'];n=len(labels)
        M=s.Matrix([l.cols[q['low']]if 'low'in q else (0,)+tuple(l.domain['high_columns'][q['type']])for q in labels]).T
        Ng=s.Matrix(8,8,lambda k,j:l.R[3][j][k]);J=M.T*Ng*M
        ds=s.Matrix([l.K.to_sympy(sum((l.K(int(M[j,i]))*l.a['ds'][j]for j in range(8)),l.K.zero))for i in range(n)])
        known=set(range(4))|set(r['packet_indices']);tw=s.ones(n,1)
        for i in r['packet_indices']:tw[i]=-1
        v=ds.multiply_elementwise(tw);D=l.K.to_sympy(l.a['D'])
        for Ndata in r['packet_fusion_matrices']:
            K=4*s.Matrix(Ndata)-J
            need(all(K[i,j]==0 for i in range(n)for j in range(n)if i not in known or j not in known),'correction supported only on known twist squares')
            need(s.simplify((v.T*K*v)[0])==0,'zero packet correction in second-indicator formula')
        out.append({'pattern':r['pattern'],'pair_histogram':r['pair_histogram'],'packet_checks':4})
    a,b,c,d=s.symbols('a b c d');nu=s.Matrix([1,0,0,-1,a,b,c,d])
    need(s.expand((nu.T*Ng*nu)[0])==2*a*b-2,'source second-indicator quadratic form')
    need(len(rows)==25,'all current histograms')
    return {'status':'PASS','histograms':25,'packet_checks':100,
            'identity':'nu2(Z_j)=(nu2(X4)*nu2(X5)-1)/2=0',
            'implication':'nu2(X4)=nu2(X5); this repeats an already forced sign, with no new reduction',
            'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checks':out}

def check_1768():
    P=37;root=s.sqrt(P);u=6+root;a=u*u;d=12*u;D=12*root*u;q=root*u
    tau=[w.chi(i)for i in range(P)]
    need(w.equal(w.mul(tau,tau),w.mon(0,P)),'quadratic Gauss square')
    labels=[2*b*b%P for b in range(1,19)]
    B=[[w.add(w.mon(4*b*c,-1),w.mon(-4*b*c,-1))for c in range(1,19)]for b in range(1,19)]
    for j,m in enumerate(labels):
        actual=w.add(*(w.mul(w.mon(2*k),B[i][j])for i,k in enumerate(labels)))
        expect=w.add(w.mon(0),w.scale(w.mul(tau,w.mon(-m*pow(2,-1,P))),-1))
        need(w.equal(actual,expect),'completed quadratic Gauss sum for v2 projection')
        need(w.equal(w.add(*B[j]),w.mon(0)),'Weil B row sum1')
    sector=s.simplify((D*6*u-(1+a*a)-d*d*(-1+root)/2)/(q*q))
    need(sector==-2,'rational-sector twist-square moment')
    need(s.simplify((1+a*a-2*q*q+d*d*(-1+root)/2)/D-6*u)==0,'vacuum projection6u')
    need(s.simplify((2*a-2*q*q-d*d*(-1+root)/2)/D+6*u)==0,'alpha projection-6u')
    nuZ=s.simplify((36*u*u*d*(1-1/a)+144*u*u)/(D*D))
    nuA=s.simplify(1+(36*u*u*(a+1/a-2)-2*18*144*u*u)/(D*D))
    need(nuZ==1 and nuA==1,'positive second indicators of all forced selfdual simples')
    return {'status':'PASS','scope':'eighteen-object branch only',
            'exact_cyclotomic_projection_checks':18,'rational_sector_twist_square_sum':-2,
            'nu2_each_primitive_Z':1,'nu2_alpha':1,'exclusion':False}

if __name__=='__main__':
    result={'status':'PASS','scope':'Independent consistency checks; neither ring is excluded or categorified.',
            'R8_3_1154':check_1154(),'R8_3_1768':check_1768()}
    (HERE/'indicator_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS:100 semionic packet indicator identities and18 exact Weil Gauss projections; both cases remain unresolved.')
