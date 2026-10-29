"""Independent all-column exact replay of nine +TY Verlinde bounds.

No optimizer is imported. The inherited positive-TY cubic reduction is an
explicit mathematical premise; the four test-only quartic equalities are
removed from the archived input before any certificate is checked.
"""
from fractions import Fraction as F
from pathlib import Path
from math import lcm
import hashlib,json

P=Path(__file__).resolve().parents[1]/'r137'
source=P/'prior/forced_export.json'
x=json.loads(source.read_text());A=x['A'][:-4];b=x['b'][:-4];nc=len(A[0])
assert len(A)==260
meta=json.loads((P/'complement_metadata.json').read_text())
certfile=P/'exact_bounds.json';saved=json.loads(certfile.read_text())
allowed=[j for j in range(nc) if j not in set(meta['removed'])]
assert allowed==saved['allowed_columns'] and len(allowed)==5996
charfile=json.loads((P/'verlinde_witness.json').read_text())
def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):return a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]+8*a[1]*b[1]
def scale(c,a):return c*a[0],c*a[1]
def inv(a):
    norm=a[0]*a[0]+8*a[0]*a[1]-2*a[1]*a[1]
    return (a[0]+8*a[1])/norm,-a[1]/norm
def from_sqrt(z):return F(z[0])-F(4,3)*F(z[1]),F(z[1])/3
def to_sqrt(z):return z[0]+4*z[1],3*z[1]
chars=[[from_sqrt(z) for z in chi] for chi in charfile['chars']]
ff=[from_sqrt(z) for z in charfile['codegrees']]
mapping={j:tuple(v) for j,v,*_ in x['physical_mapping']}
values={};ZERO=(F(0),F(0));D=(F(16),F(32))
for v in set(mapping.values()):
    aa=F(v[0]+v[1]+v[2]+v[7]+2*v[8]);bb=F(sum(v[3:7]));delta=(aa,bb);eta=(aa,4*aa-bb)
    fac=mul(mul(eta,eta),inv(mul(D,delta)));out=[]
    for chi,f in zip(chars,ff):
        cv=ZERO
        for k in range(9):cv=add(cv,scale(v[k],chi[k]))
        out.extend(to_sqrt(mul(fac,mul(cv,inv(f)))))
    values[v]=out
FD=lcm(*(z.denominator for val in values.values() for z in val))
assert FD==2304==int(saved['Fden'])
intvalues={v:[int(FD*z) for z in val] for v,val in values.items()}
base_spec=[['old',i] for i in range(260)]+[['fusion',2*i+1] for i in range(9)]+[['pair',i] for i in range(len(meta['equalities']))]
base_rhs=list(map(F,b))+[F(0)]*(9+len(meta['equalities']))
expect=[(7,1,F(31,18),[]),(7,-1,F(-1,2),[]),(3,1,F(17,30),[(7,1)]),(6,1,F(17,30),[(7,1)]),(0,1,F(1),[(7,1),(3,0),(6,0)]),(1,1,F(3,4),[(7,1),(3,0),(6,0)]),(2,1,F(3,4),[(7,1),(3,0),(6,0)]),(4,1,F(3,4),[(7,1),(3,0),(6,0)]),(5,1,F(3,4),[(7,1),(3,0),(6,0)])]
assert len(saved['certificates'])==len(expect)
results=[]
for cert,(e,sign,target,extras) in zip(saved['certificates'],expect):
    spec=base_spec+[['fusion',2*j] for j,_ in extras]
    rhs=base_rhs+[F(v) for _,v in extras]
    assert cert['spec']==spec and list(map(F,cert['rhs']))==rhs
    assert cert['objective_label']==e and cert['sign']==sign and F(cert['bound'])==target
    lam={int(j):F(z) for j,z in cert['lambda']};mu={int(j):F(z) for j,z in cert['mu']}
    assert len(lam)==len(cert['lambda']) and len(mu)==len(cert['mu'])
    assert all(z>=0 for z in mu.values())
    assert all(0<=j<len(spec) for j in lam) and all(0<=j<9 for j in mu)
    den=FD*lcm(*(z.denominator for z in list(lam.values())+list(mu.values())))
    residual=[0]*nc
    for ri,w in lam.items():
        kind,k=spec[ri]
        if kind=='old':
            h=int(w*den)
            for j in allowed:residual[j]+=h*A[k][j]
        elif kind=='pair':
            h=int(w*den)
            for j in meta['equalities'][k][0]:residual[j]+=h
            for j in meta['equalities'][k][1]:residual[j]-=h
        else:
            h=int(w*den/FD)
            for j in allowed:
                if j in mapping:residual[j]+=h*intvalues[mapping[j]][k]
    for ee,w in mu.items():
        h=int(w*den/FD)
        for j in allowed:
            if j in mapping:residual[j]-=h*intvalues[mapping[j]][2*ee]
    for j in allowed:
        if j in mapping:residual[j]-=sign*(den//FD)*intvalues[mapping[j]][2*e]
    assert min(residual[j] for j in allowed)>=0
    assert sum(w*rhs[i] for i,w in lam.items())==target
    results.append({'label':e,'sign':sign,'bound':str(target),'allowed_columns_verified':len(allowed),'minimum_scaled_slack':str(min(residual[j] for j in allowed)),'added_integer_consequences':extras})
out={'status':'PASS','original_test_only_quartic_equalities_removed':4,'inherited_positive_TY_cubic_branch':'nu3=1/2 retained as separately established necessity, not proved by this script','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'certificate_sha256':hashlib.sha256(certfile.read_bytes()).hexdigest(),'certificates':results,'consequence':'Positive TY branch impossible: NBB-to-B=1, six other nonunit distinguished coefficients vanish, last coefficient <=1, contradicting their forced total4.','scope':'Does not exclude the negative TY branch or R137 globally.'}
(Path(__file__).parent/'audit_r137_positive_certificates.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','certificates':len(results),'columns_each':len(allowed),'scope':out['scope']},indent=2))
