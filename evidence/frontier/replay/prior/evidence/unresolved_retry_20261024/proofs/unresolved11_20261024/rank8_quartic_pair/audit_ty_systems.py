#!/usr/bin/env python3
"""Independent semantic reconstruction; no qs.build/qc.system or optimizer."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,itertools,json,math,sys
HERE=Path(__file__).resolve().parent
COMM=HERE.parent/'rank9_commutative';WORK=HERE.parents[1]
sys.path.insert(0,str(WORK/'rank9_m2_research/phase3/quadratic_s_symmetry'))
import quadratic_s_symmetry as qs
qc=qs.qc
def need(x,m):
    if not x:raise ValueError(m)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def normalize(row,rhs,gcd=True):
    den=math.lcm(*(F(t).denominator for t in row+[rhs]))
    row=[int(t*den) for t in row];rhs=int(rhs*den)
    g=(math.gcd(rhs,*row) or 1) if gcd else 1
    return [v//g for v in row],rhs//g

def independent(R,rid,tau):
    data=qc.base(R);n=len(R);q=data['q'];D=data['D'];ch=data['ch']
    need(q==2 and D==(144,96),'quadratic dimension control')
    g={'R9_2_137':1,'R9_2_1607':5,'R9_2_1976':8}[rid]
    Y={'R9_2_137':8,'R9_2_1607':3,'R9_2_1976':5}[rid]
    cols=[(v,z) for v,z in data['cols'] if z[1]!=0 or (z[0]==1 and v[g]==0)]
    need(all(not v[Y] for v,z in cols if v[0]),'all low columns have zero Y')
    fermions={v for v,z in cols if z==(1,0) and not v[0]}
    need(len(fermions)==2,'two possible anisotropic lifts')
    types,bound=qc.trace_types(q,data['primes'],4)
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
        for k in range(1,5):pp.append([sum(pp[-1][a]*R[a][i][b] for a in range(n)) for b in range(n)])
        powers[i]=pp
    blocks=[]
    for i in range(1,n):
        for order in (3,4):
            divisors=[r for r in range(1,order) if order%r==0]
            traces=qc.rotation_types(q,order,divisors)
            mass=new(('rotation_mass',i,order),powers[i][order][0])
            eq=[(at,r,[new(('rotation',i,order,r,c),0) for c in range(2)]) for at,r in enumerate(divisors)]
            blocks.append((i,order,traces,mass,eq))
    variables=[];rawkeys=[]
    for v,z in cols:
        phases=[(-1,(one,)*4)] if v[0] else list(enumerate(types))
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
    chars=qs.characters(ch,q,D);known=Counter(c['dimension'] for c in chars)
    dims=dict(cols);select=[];keys=[];labels=[]
    for j,(kind,v,ti) in enumerate(rawkeys):
        z=dims[v]
        if kind=='high':select.append(j);keys.append((kind,v,ti));labels.append((None,None));continue
        for h,c in enumerate(chars):
            if c['dimension']==z:select.append(j);keys.append(('label',v,h));labels.append((h,v))
        if data['counts'][z]>known[z]:select.append(j);keys.append(('anonymous',v,0));labels.append((None,None))
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
    fermion=tuple((F((-1)**k),F(0)) for k in range(1,5))
    primitive=[((0,F(1,2)),(0,0),(0,F(-1,2)),(-1,0)),((0,F(-1,2)),(0,0),(0,F(1,2)),(-1,0))]
    allowed=primitive+([(one,one,one,one),((-1,0),one,(-1,0),one)] if tau==1 else [((0,0),(-1,0),(0,0),(1,0))])
    keep=[]
    for j,(kind,v,ti) in enumerate(keys):
        if kind=='high':
            if v in fermions and tuple(types[ti])!=fermion:continue
            if v[Y] and tuple(types[ti]) not in allowed:continue
        keep.append(j)
    A=[[row[j] for j in keep]+[0] for row in A];keys=[keys[j] for j in keep]
    A.append([int(kind=='high' and v in fermions) for kind,v,ti in keys]+[1]);b.append(1)
    for k,nu in [(2,tau),(4,0)]:
        vals=[qc.scale(qc.mul(dims[v],types[ti][k-1],q),v[Y]) if kind=='high' and v[Y] else zero for kind,v,ti in keys]+[zero]
        value=qc.scale(D,nu)
        for c in range(2):
            rr,bb=normalize([v[c] for v in vals],value[c],gcd=False);A.append(rr);b.append(bb)
    return A,b,{'restriction_columns':len(cols),'labelled_characters':len(chars),'zero_Y_in_low_columns':True,'trace_representative_bound':bound}

def audit(rid,tau=1):
    R=json.loads((HERE.parent/'inputs'/f'{rid}.json').read_text())['fusion_tensor']
    A,b,meta=independent(R,rid,tau)
    receipt=json.loads((COMM/f'{rid}_integral_center_h4_tau{tau}.json').read_text())
    need(len(A)==receipt['rows'] and len(A[0])==receipt['variables'],'independent dimensions agree')
    ray=receipt['ray'];need(ray is not None,'saved exact ray')
    bt=sum(x*y for x,y in zip(b,ray));aty=[sum(row[j]*y for row,y in zip(A,ray)) for j in range(len(A[0]))]
    need(bt<0 and min(aty)>=0,'independently reconstructed exact Farkas contradiction')
    need(bt==receipt['bTy'] and min(aty)==receipt['minimum_ATy'],'reported pairings agree')
    source=(COMM/'screen_integral_center.py').read_text();prefix=source.split('\nif verify:')[0]
    savedargv=sys.argv;sys.argv=['screen_integral_center.py',rid,'4','1',str(tau)]
    try:
        ns={'__file__':str(COMM/'screen_integral_center.py'),'__name__':'audit_control'};exec(compile(prefix,'discovery_control','exec'),ns)
    finally:sys.argv=savedargv
    need(A==ns['A'] and b==ns['b'],'independent full system equals discovery system exactly')
    out={'status':'PASS','id':rid,'tau_sign':tau,'rows':len(A),'columns':len(A[0]),'bTy':bt,'minimum_ATy':min(aty),'system_sha256':digest({'A':A,'b':b}),'source_tensor_sha256':digest(R),'metadata':meta,'scope':'Independent exact reconstruction confirms only the positive-TY-sign branch contradiction; no whole-ring exclusion.'}
    (HERE/f'audit_{rid}_TY_tau{tau}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)
if __name__=='__main__':
    for rid in sys.argv[1:] or ['R9_2_1607','R9_2_1976']:audit(rid)
