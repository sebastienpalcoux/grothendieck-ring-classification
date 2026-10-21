"""Exact split-module polynomial obstruction for any fixed-point involution.

The categorical derivation is the general version of ../models/psl2_11/r280.
Integer matrices are tested modulo a prime: absence even modulo that prime
is sufficient for exclusion. No floating-point eigenvalue calculation is used.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,math,sys,time
import numpy as np
import sympy as s
HERE=Path(__file__).resolve().parent
PRIME=1009
def require(v,m):
    if not v:raise ValueError(m)

def setup(R,g,x):
    n=len(R);require(n==8,'rank eight required')
    require(all(R[i][j]==R[j][i] for i in range(n) for j in range(n)),'commutative ring required')
    require(g!=0 and R[g][g]==[1]+[0]*(n-1),'involutive invertible required')
    require(R[x][x][0]==1,'self-dual generator required')
    fixed=[i for i in range(n) if R[g][i][i]==1];require(fixed,'no fixed simple')
    A=[[R[x][i][j] for j in fixed] for i in fixed]
    require(A==list(map(list,zip(*A))),'nonsymmetric fixed block')
    f=len(fixed);parent=list(range(f));entries=[]
    def root(i):
        while parent[i]!=i:i=parent[i]
        return i
    for i in range(f):
        for j in range(i,f):
            a=A[i][j];allowed=list(range(-a,a+1,2));gauge=False
            if i!=j and a%2 and root(i)!=root(j):
                parent[root(i)]=root(j);allowed=[v for v in allowed if v>0];gauge=True
            entries.append([i,j,allowed,gauge])
    N=s.Matrix(R[x]);p=N.charpoly().as_poly().sqf_part()
    coefficients=[int(c) for c in p.all_coeffs()]
    require(all(c.q==1 for c in p.all_coeffs()),'nonintegral polynomial')
    check=s.zeros(n)
    for c in coefficients:check=check*N+c*s.eye(n)
    require(check==s.zeros(n),'source polynomial identity failed')
    return dict(fixed=fixed,bounds=A,entries=entries,polynomial=coefficients,cases=math.prod(len(a) for i,j,a,gauge in entries),prime=PRIME)

def search(R,g,x,budget=2000000):
    return search_setup(setup(R,g,x),budget)

def search_setup(a,budget=2000000):
    f=len(a['fixed'])
    if a['cases']>budget:return dict(a,outcome='enumeration_budget',budget=budget)
    eye=np.eye(f,dtype=np.int64);tested=0;modular_zeros=0
    choices=itertools.product(*(e[2] for e in a['entries']))
    while True:
        chunk=list(itertools.islice(choices,4096))
        if not chunk:break
        B=np.zeros((len(chunk),f,f),dtype=np.int64)
        for k,(i,j,allowed,gauge) in enumerate(a['entries']):B[:,i,j]=B[:,j,i]=[row[k] for row in chunk]
        B%=PRIME;V=np.zeros_like(B)
        for c in a['polynomial']:V=(V@B+(c%PRIME)*eye)%PRIME
        good=np.flatnonzero(np.all(V==0,axis=(1,2)));tested+=len(chunk)
        modular_zeros+=len(good)
        if len(good):
            # Only a modular survivor is needed for a no-conclusion outcome.
            i=int(good[0]);witness=[[int(v) for v in row] for row in B[i]]
            return dict(a,outcome='no_conclusion',tested=tested,modular_survivor=witness)
    require(tested==a['cases'],'incomplete finite search')
    require(modular_zeros==0,'unhandled modular survivor')
    return dict(a,outcome='excluded',tested=tested)

def verify(R,c):
    require(c['kind']=='rank8_split_module_polynomial','wrong certificate kind')
    actual=search(R,c['involution'],c['generator'],budget=c['search']['cases'])
    require(actual['outcome']=='excluded' and actual==c['search'],'split-module proof does not replay')

def discover():
    base=HERE.parent;rows=json.loads((base/'pipeline/census_m3.json').read_text())
    sys.path.insert(0,str(HERE.parents[2]/'supplements/rank8/software'))
    import finalize_m3
    try:
        _,summary=finalize_m3.reconcile();pending=set(summary['unresolved_ids'])
    except ValueError as error:
        # During concurrent recovery a source-bound manifest may be stale.
        # Testing every baseline residual is a safe superset of the frontier.
        pending={r['id'] for r in json.loads((base/'pipeline/survivors_m3.json').read_text())}
        print('Using all baseline residuals while manifest refresh is pending:',str(error),flush=True)
    pending.update(f'R8_3_{i}' for i in (76,735,738,1019,1051,1057,1067,1197,1805,2392,2415,2836))
    pending.update(['R8_3_1051','R8_3_2415','R8_3_331','R8_3_471','R8_3_1456',
                    'R8_3_3314','R8_3_342','R8_3_724','R8_3_3278','R8_3_448',
                    'R8_3_334','R8_3_274','R8_3_715','R8_3_475','R8_3_458','R8_3_3342'])
    output=[]
    for row in rows:
        if row['id'] not in pending or not row['commutative']:continue
        R=row['tensor'];start=time.monotonic();records=[];cert=None
        dual=[]
        for i in range(8):
            hits=[j for j in range(8) if R[i][j][0]];require(len(hits)==1,'unique dual required');dual.append(hits[0])
        invertibles=[i for i in range(8) if R[i][dual[i]]==[1]+[0]*7]
        for g in invertibles:
            if g==0 or R[g][g][0]!=1 or not any(R[g][i][i] for i in range(8)):continue
            for x in range(1,8):
                if dual[x]!=x:continue
                report=search(R,g,x);records.append({'involution':g,'generator':x,'search':report})
                if report['outcome']=='excluded':
                    cert=dict(kind='rank8_split_module_polynomial',involution=g,generator=x,search=report)
                    verify(R,cert);break
            if cert:break
        item={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'scope':'general_complex_fusion_category','outcome':'excluded' if cert else ('no_conclusion' if records else 'inapplicable_no_fixed_involution'),'certificate':cert,'attempts':records,'seconds':round(time.monotonic()-start,3)}
        output.append(item);target=HERE/'split_module_polynomial_results.json';temporary=target.with_suffix('.json.tmp');temporary.write_text(json.dumps(output,separators=(',',':'))+'\n');temporary.replace(target)
        print(row['id'],item['outcome'],item['seconds'],flush=True)
def replay():
    rows={r['id']:r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text())}
    count=0
    for item in json.loads((HERE/'split_module_polynomial_results.json').read_text()):
        row=rows[item['id']]
        digest=hashlib.sha256(json.dumps(row['tensor'],separators=(',',':')).encode()).hexdigest()
        require(digest==item['tensor_sha256']==row['tensor_sha256'],'source tensor mismatch')
        if item['outcome']=='excluded':verify(row['tensor'],item['certificate']);count+=1
    print('PASS:',count,'exact split-module exclusions',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='explicitly regenerate the discovery report')
    if parser.parse_args().write:discover()
    else:replay()
