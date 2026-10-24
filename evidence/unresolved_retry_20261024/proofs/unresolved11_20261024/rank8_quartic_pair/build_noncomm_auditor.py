from pathlib import Path
P=Path(__file__).resolve().parent
src=(P/'audit_ty_systems.py').read_text()
start=src.index('def independent(');end=src.index('\ndef audit(',start)
f=src[start:end]
f=f.replace('def independent(R,rid,tau):','def independent(R,tau,height=6):')
f=f.replace("data=qc.base(R);n=len(R);q=data['q'];D=data['D'];ch=data['ch']","data=sy.base(R);n=len(R);q=data['q'];D=data['D'];ch=data['ch']")
a=f.index("    g={'R9_2_137'");b=f.index("    zero=",a)
f=f[:a]+'''    Y=8
    cols=[(v,z) for v,z in data['cols'] if z[1]!=0 or tuple(v)==(1,0,0,0,0,0,0,0,0)]
    need(all(not v[Y] for v,z in cols if v[0]),'all low columns have zero Y')
    types,bound=qc.trace_types(q,data['primes'],height)
'''+f[b:]
f=f.replace('range(1,5)','range(1,height+1)').replace('for order in (3,4):','for order in range(3,height+1):').replace('(one,)*4','(one,)*height')
f=f.replace("chars=qs.characters(ch,q,D);known=Counter(c['dimension'] for c in chars)",'''ringchars=sy.chars(R)
    chars=sy.characters(ringchars,q,D)
    for c in chars:c['degree']=1
    val=[(F(ringchars.N[i].trace()-ringchars.A[i].trace(),4),F(0)) for i in range(n)]
    need(val[0]==(1,0),'normalized degree-two character')
    chars.append({'values':val,'dimension':qc.div(D,(F(4),F(0)),q),'degree':2})''')
f=f.replace("if c['dimension']==z:","if c['dimension']==z and v[0]==c['degree']:")
f=f.replace("if data['counts'][z]>known[z]:", "if z==(F(9),F(6)):")
a=f.index('    fermion=');b=f.index('    return A,b,',a)
f=f[:a]+'''    # S-symmetry equations summed over the two omitted conjugate scalar characters.
    realpart=[1,0,0,0,0,1,1,1,-2];cdim=(F(9),F(6))
    for h,c in enumerate(chars):
        parts=[[F(0)]*len(keys) for _ in range(2)]
        for j,(kind,v,ti) in enumerate(keys):
            value=zero
            if kind=='anonymous':
                ev=tuple(sum(v[i]*c['values'][i][component] for i in range(n)) for component in range(2))
                value=qc.mul(c['dimension'],ev,q)
            elif kind=='label' and ti==h:
                value=qc.scale(cdim,-2*sum(v[i]*realpart[i] for i in range(n)))
            for component in range(2):parts[component][j]=value[component]
        for row in parts:
            rr,bb=normalize(row,F(0))
            if any(rr):A.append(rr);b.append(bb)
    cosine=[one,(F(0),F(1,2)),zero,(F(0),F(-1,2)),(-1,0),(F(0),F(-1,2)),zero,(F(0),F(1,2))]
    allowed=[tuple(cosine[j*k%8] for k in range(1,height+1)) for j in (1,3)]
    allowed+=([tuple((F(a**k),F(0)) for k in range(1,height+1)) for a in (1,-1)] if tau==1 else [tuple((F(0) if k%2 else F((-1)**(k//2)),F(0)) for k in range(1,height+1))])
    keep=[j for j,(kind,v,ti) in enumerate(keys) if kind!='high' or not v[Y] or tuple(types[ti]) in allowed]
    A=[[row[j] for j in keep] for row in A];keys=[keys[j] for j in keep]
    for k,nu in [(k,nu) for k,nu in [(2,tau),(4,0),(6,tau)] if k<=height]:
        vals=[qc.scale(qc.mul(dims[v],types[ti][k-1],q),v[Y]) if kind=='high' and v[Y] else zero for kind,v,ti in keys]
        value=qc.scale(D,nu)
        for component in range(2):
            rr,bb=normalize([v[component] for v in vals],value[component],gcd=False);A.append(rr);b.append(bb)
'''+f[b:]
header='''#!/usr/bin/env python3
"""Independent semantic reconstruction of R1975 TY branch systems.

No call to symmetry.build or quadratic_center.system occurs. Restriction-column
and complete relative-trace domain helpers remain inherited explicit dependencies.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,itertools,json,math,sys,gzip
HERE=Path(__file__).resolve().parent
WORK=HERE.parents[1]
sys.path.insert(0,str(WORK/'rank9_m2_research/phase3/noncomm1975'))
import symmetry as sy
qc=sy.qc
from audit_ty_systems import need,normalize,digest
'''
footer='''
def audit(tau,height=6):
    R=json.loads((HERE.parent/'inputs/R9_2_1975.json').read_text())['fusion_tensor']
    A,b,meta=independent(R,tau,height)
    folder=HERE.parent/'rank9_noncommutative';name=f'ty_spectrum_h{height}_tau{tau}'
    receipt=json.loads((folder/(name+'.json')).read_text())
    with gzip.open(folder/(name+'_system.json.gz'),'rt') as stream:discovery=json.load(stream)
    need(A==discovery['A'] and b==discovery['b'],'all independently reconstructed matrix entries equal saved system')
    need(digest([A,b])==receipt['system_sha256'],'recorded system hash')
    need(len(A)==receipt['rows'] and len(A[0])==receipt['variables'],'recorded system dimensions')
    out={'status':'PASS','id':'R9_2_1975','tau_sign':tau,'height':height,'rows':len(A),'columns':len(A[0]),'system_sha256':digest([A,b]),'source_tensor_sha256':digest(R),'metadata':meta}
    if tau==1:
        ray=receipt['ray'];need(len(ray)==len(A),'ray length')
        bt=sum(x*y for x,y in zip(b,ray));aty=[sum(row[j]*y for row,y in zip(A,ray)) for j in range(len(A[0]))]
        need(bt<0 and min(aty)>=0,'independently reconstructed Farkas contradiction')
        need(bt==receipt['bTy'] and min(aty)==receipt['min_ATy'],'recorded pairings')
        out.update(bTy=bt,minimum_ATy=min(aty),scope='Positive-TY-sign branch excluded; no whole-ring exclusion.')
    else:
        for key in ['rational_witness','integer_witness']:
            witness=[F(0)]*len(A[0])
            for j,v in receipt[key]:witness[j]=F(v)
            need(min(witness)>=0 and all(sum(a*x for a,x in zip(row,witness))==z for row,z in zip(A,b)),'exact feasible '+key)
            out[key+'_support']=sum(bool(x) for x in witness)
        out['scope']='Necessary-condition witnesses only, not category models.'
    (HERE/f'audit_R9_2_1975_TY_h{height}_tau{tau}.json').write_text(json.dumps(out,indent=2)+'\\n')
    print(json.dumps(out),flush=True)
if __name__=='__main__':
    for tau in [1,-1]:audit(tau)
'''
(P/'audit_noncomm_ty_systems.py').write_text(header+f+footer)
