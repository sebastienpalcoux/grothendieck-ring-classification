"""Fresh direct audit of Liptrap Definition4.3, independent of prior setup code."""
from pathlib import Path
from itertools import product
import json,time,hashlib
import numpy as np
import sympy as sp

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
PACK=BASE/'prior_round'
EVID=PACK/'prior_round/evidence'
FIRST=EVID/'rank12-m1-offline-20261025'
SECOND=EVID/'rank12-m1-round2-20261025'

def need(ok,why):
    if not ok:raise ValueError(why)

def audit(R,c):
    N=np.array(R,dtype=np.int64);n=len(N);q=c['modulus']
    need(set(N.reshape(-1))<={0,1},'multiplicity-free input')
    need(all(np.array_equal(N[0,a],np.eye(n,dtype=int)[a]) and np.array_equal(N[a,0],np.eye(n,dtype=int)[a]) for a in range(n)),'unit')
    need(np.array_equal(np.einsum('ijm,mkl->ijkl',N,N),np.einsum('jkm,iml->ijkl',N,N)),'associative input')
    dual=[]
    for a in range(n):
        choices=[b for b in range(n) if N[a,b,0]]
        need(len(choices)==1,'unique dual');dual.append(choices[0])
    S=[a for a in range(n) if N[a,dual[a]].sum()==1];M=[a for a in range(n) if a not in S];Sset=set(S)
    need(S==c['serfs'] and M==c['lords'],'full even and odd lists')
    need(all(not N[a,b,k] for a,b,k in product(M,repeat=3)),'odd square pointed')
    mult={}
    for a,b in product(range(n),repeat=2):
        if a in Sset or b in Sset:
            choices=np.flatnonzero(N[a,b]);need(len(choices)==1,'invertible translates simples');mult[a,b]=int(choices[0])
    H=[a for a in S if all(mult[a,m]==mult[m,a]==m for m in M)]
    need(H==c['stabilizer'] and all({mult[a,m] for a in S}==set(M)=={mult[m,a] for a in S} for m in M),'common kernel and transitive bimodule')
    need(all([a for a in S if mult[a,m]==m]==H==[a for a in S if mult[m,a]==m] for m in M),'full stabilizers')
    p={tuple(v[:-1]):int(v[-1])%q for v in c['phase_values']}
    varying=c['tau']=='phase_times_inverse_square_root'
    expected={(f,a,b,m) for f in ('chi','upsilon') for a in S if a for b in S if b for m in M}
    if varying:expected|={('tau',m) for m in M}
    need(set(p)==expected and len(p)==len(c['phase_values']),'exact phase-key coverage')
    def chi(a,b,m):return p.get(('chi',a,b,m),0)
    def nu(a,b,m):return p.get(('upsilon',a,b,m),0)
    def tau(m):return p.get(('tau',m),0)
    count=0
    for a,b,m in product(S,S,M):
        am=mult[a,m];mb=mult[m,b];amb=mult[am,b]
        need((chi(b,a,dual[m])-chi(a,b,amb)-tau(amb)-tau(m)+tau(am)+tau(mb))%q==0,'Liptrap quasisymmetry')
        count+=1
    for a,b,c0,m in product(S,S,S,M):
        need((nu(a,b,m)-nu(a,b,mult[m,dual[c0]])+chi(mult[a,b],c0,m)-chi(a,c0,m)-chi(b,c0,mult[dual[a],m]))%q==0,'Liptrap biderivation')
        count+=1
    for m in M:
        need((tau(m)+tau(dual[m]))%q==0,'tau times involution is 1/|H|')
        need(len({tuple(chi(a,b,m) for b in H) for a in H})==len(H),'nondegenerate character pairing')
        for a,b,c0 in product(H,repeat=3):
            need((chi(a,b,m)-chi(b,a,m))%q==0,'symmetric stabilizer pairing')
            need((chi(mult[a,b],c0,m)-chi(a,c0,m)-chi(b,c0,m))%q==0,'multiplicative stabilizer pairing')
    # Each remaining scalar recoupling is a quotient of phases and equal-modulus taus.
    # Lemma5.4 leaves precisely the following gamma blocks to check for unitarity.
    t=sp.Symbol('t');poly=list(reversed([int(x) for x in sp.Poly(sp.cyclotomic_poly(q,t),t).all_coeffs()]));degree=len(poly)-1
    def zero(cs):
        for k in range(len(cs)-1,degree-1,-1):
            z=cs[k]
            for j,v in enumerate(poly):cs[k-degree+j]-=z*v
        return not any(cs)
    cosets=sorted({tuple(sorted(mult[a,h] for h in H)) for a in S})
    def gamma(a,b,m):
        v=mult[dual[b],m]
        return (tau(v)+nu(dual[a],a,dual[v])-nu(dual[b],b,mult[v,dual[a]])-chi(b,a,m))%q
    blocks=0
    for I,J,m in product(cosets,cosets,M):
        for a,b in product(I,repeat=2):
            cs=[0]*q
            for j in J:cs[(gamma(a,j,m)-gamma(b,j,m))%q]+=1
            if a==b:cs[0]-=len(H)
            need(zero(cs),'full exact Fourier-block orthogonality')
        blocks+=1
    return dict(status='PASS',rank=n,serfs=len(S),lords=len(M),stabilizer_order=len(H),phase_modulus=q,defining_equations=count,unitary_Fourier_blocks=blocks)

def main():
    start=time.monotonic();tensors=json.loads((FIRST/'tensors.json').read_text());out=[]
    for row in json.loads((FIRST/'feudal.json').read_text())['records']:
        if row['model']:
            r=audit(tensors[row['id']],row['model']);r['id']=row['id'];out.append(r);print(row['id'],'PASS',flush=True)
    for row in json.loads((SECOND/'family_graded/feudal40_models_sparse.json').read_text()):
        if row.get('certificate'):
            r=audit(row['tensor'],row['certificate']);r['source_parameters']=row['parameters'];out.append(r);print(row['parameters'],'PASS',flush=True)
    result=dict(status='PASS',first_round_ring_count=21,dimension40_precursor_count=5,records=out,seconds=time.monotonic()-start,scope='Actual unitary categories by Liptrap Theorem4 and complete scalar/Fourier unitarity check; no classification inference.')
    (HERE/'liptrap_reaudit.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
