#!/usr/bin/env python3
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
def independent(R,tau,height=6):
    data=sy.base(R);n=len(R);q=data['q'];D=data['D'];ch=data['ch']
    need(q==2 and D==(144,96),'quadratic dimension control')
    Y=8
    cols=[(v,z) for v,z in data['cols'] if z[1]!=0 or tuple(v)==(1,0,0,0,0,0,0,0,0)]
    need(all(not v[Y] for v,z in cols if v[0]),'all low columns have zero Y')
    types,bound=qc.trace_types(q,data['primes'],height)
    zero=(F(0),F(0));one=(F(1),F(0));rowtags=[];rhs=[]
    def new(tag,value):rowtags.append(tag);rhs.append(F(value));return len(rhs)-1
    gram={(i,j):new(('gram',i,j),int(ch.C[i,j])) for i,j in itertools.combinations_with_replacement(range(n),2)}
    low={z:new(('low',z),num) for z,num in sorted(data['counts'].items())}
    gal=[(a,b,new(('gal',a,b),0)) for a,b in data['galois_pairs']]
    first={(i,c):new(('first',i,c),0) for i in range(1,n) for c in range(2)}
    second={};unknown=[]
    for i in range(1,n):
        eps=0 if ch.du[i]!=i else 1 if any(R[j][ch.du[j]][i]%2 for j in range(n)) else None
        if eps is None:
            rr=[new(('second',i,c),-D[c]) for c in range(2)]
            br=new(('indicator_bound',i),1);unknown.append((i,rr,br))
        else:rr=[new(('second',i,c),eps*D[c]) for c in range(2)]
        second[i]=rr
    powers={}
    for i in range(1,n):
        pp=[[1]+[0]*(n-1)]
        for k in range(1,height+1):pp.append([sum(pp[-1][a]*R[a][i][b] for a in range(n)) for b in range(n)])
        powers[i]=pp
    blocks=[]
    for i in range(1,n):
        for order in range(3,height+1):
            divisors=[r for r in range(1,order) if order%r==0]
            traces=qc.rotation_types(q,order,divisors)
            mass=new(('rotation_mass',i,order),powers[i][order][0])
            eq=[(at,r,[new(('rotation',i,order,r,c),0) for c in range(2)]) for at,r in enumerate(divisors)]
            blocks.append((i,order,traces,mass,eq))
    variables=[];rawkeys=[]
    for v,z in cols:
        phases=[(-1,(one,)*height)] if v[0] else list(enumerate(types))
        for ti,tt in phases:
            col={row:F(v[i]*v[j]) for (i,j),row in gram.items() if v[i]*v[j]}
            if v[0]:col[low[z]]=F(1)
            for a,b,row in gal:
                if z==a:col[row]=F(1)
                elif z==b:col[row]=F(-1)
            for i in range(1,n):
                for power,rows in [(0,[first[i,c] for c in range(2)]),(1,second[i])]:
                    value=qc.scale(qc.mul(z,tt[power],q),v[i])
                    for c in range(2):
                        if value[c]:col[rows[c]]=value[c]
            for i,order,traces,mass,eq in blocks:
                for at,r,rows in eq:
                    mult=sum(powers[i][r][a]*v[a] for a in range(n))
                    value=qc.scale(qc.mul(z,tt[order//r-1],q),-mult)
                    for c in range(2):
                        if value[c]:col[rows[c]]=value[c]
            variables.append(col);rawkeys.append(('high' if not v[0] else 'low',v,ti))
    sourcevarcount=len(variables)
    for i,rows,br in unknown:
        col={rows[c]:-2*D[c] for c in range(2) if D[c]};col[br]=F(1)
        variables.extend([col,{br:F(1)}])
    for i,order,traces,mass,eq in blocks:
        for trace in traces:
            col={mass:F(1)}
            for at,r,rows in eq:
                value=qc.mul(D,trace[at],q)
                for c in range(2):
                    if value[c]:col[rows[c]]=value[c]
            variables.append(col)
    A=[];b=[]
    for row,value in enumerate(rhs):
        rr,bb=normalize([v.get(row,F(0)) for v in variables],value)
        A.append(rr);b.append(bb)
    ringchars=sy.chars(R)
    chars=sy.characters(ringchars,q,D)
    for c in chars:c['degree']=1
    val=[(F(ringchars.N[i].trace()-ringchars.A[i].trace(),4),F(0)) for i in range(n)]
    need(val[0]==(1,0),'normalized degree-two character')
    chars.append({'values':val,'dimension':qc.div(D,(F(4),F(0)),q),'degree':2})
    dims=dict(cols);select=[];keys=[];labels=[]
    for j,(kind,v,ti) in enumerate(rawkeys):
        z=dims[v]
        if kind=='high':select.append(j);keys.append((kind,v,ti));labels.append((None,None));continue
        for h,c in enumerate(chars):
            if c['dimension']==z and v[0]==c['degree']:select.append(j);keys.append(('label',v,h));labels.append((h,v))
        if z==(F(9),F(6)):select.append(j);keys.append(('anonymous',v,0));labels.append((None,None))
    for j in range(sourcevarcount,len(variables)):
        select.append(j);keys.append(('extra',(),j));labels.append((None,None))
    A=[[row[j] for j in select] for row in A]
    for h in range(len(chars)):
        A.append([int(label==h) for label,v in labels]);b.append(1)
    for h in range(len(chars)):
        for k in range(h):
            parts=[[F(0)]*len(keys) for _ in range(2)]
            for j,(label,v) in enumerate(labels):
                if label not in (h,k):continue
                other=k if label==h else h
                ev=tuple(sum(v[i]*chars[other]['values'][i][c] for i in range(n)) for c in range(2))
                val=qc.mul(chars[other]['dimension'],ev,q)
                if label==h:val=qc.scale(val,-1)
                for c in range(2):parts[c][j]=val[c]
            for row in parts:
                rr,bb=normalize(row,F(0))
                if any(rr):A.append(rr);b.append(bb)
    # S-symmetry equations summed over the two omitted conjugate scalar characters.
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
    return A,b,{'restriction_columns':len(cols),'labelled_characters':len(chars),'zero_Y_in_low_columns':True,'trace_representative_bound':bound}

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
    (HERE/f'audit_R9_2_1975_TY_h{height}_tau{tau}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)
if __name__=='__main__':
    for tau in [1,-1]:audit(tau)
