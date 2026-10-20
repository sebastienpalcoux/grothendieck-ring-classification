"""Exact local p=5 projection identities and source FP-weight constants."""
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def require(value, message):
    if not value:raise RuntimeError(message)

def local_check(M):
    p=5
    points=[(x,y) for x in range(M) for y in range(M) if x%p or y%p]
    ix={z:i for i,z in enumerate(points)};n=len(points)
    T=[ix[((x+y)%M,y)] for x,y in points]
    H=[ix[((2*x)%M,(pow(2,-1,M)*y)%M)] for x,y in points]
    require(pow(2,4*M//5,M)==1 and pow(2,2*M//5,M)!=1,
            'The torus generator has the wrong two-primary order.')
    if M>5:require(pow(2,4*M//25,M)!=1,'The torus generator has the wrong five-primary order.')
    seen=set();columns=[]
    for start in range(n):
        if start in seen:continue
        values={start:1};queue=[start];consistent=True
        for i in queue:
            for j,sign in ((T[i],1),(H[i],-1)):
                value=values[i]*sign
                if j not in values:values[j]=value;queue.append(j)
                elif values[j]!=value:consistent=False
        seen.update(values)
        if consistent:
            v=np.zeros(n,dtype=np.int64)
            for i,value in values.items():v[i]=value
            columns.append(v)
    B=np.stack(columns,axis=1)
    require(np.array_equal(B[T,:],B) and np.array_equal(B[H,:],-B),
            'The exact domain basis does not satisfy its invariances.')
    Sperm=[ix[((-y)%M,x)] for x,y in points]
    SB=B[Sperm,:]
    gram=[]
    for step in (1,5):
        perm=[ix[((x+step*y)%M,y)] for x,y in points]
        visited=set();R=np.zeros_like(B)
        for start in range(n):
            if start in visited:continue
            orbit=[];i=start
            while i not in visited:
                visited.add(i);orbit.append(i);i=perm[i]
            require(M%len(orbit)==0,'Unexpected averaging orbit length.')
            R[orbit,:]=SB[orbit,:].sum(axis=0)*(M//len(orbit))
        gram.append(s.Matrix((R.T@R).tolist())/M**2)
    D=s.diag(*(int((B[:,i]**2).sum()) for i in range(B.shape[1])))
    require(gram[1]==p*gram[0],'The exact prime-projection ratio failed.')
    A=D.inv()*gram[0]
    require(A*A==A/p,'The maximal squared singular value is not one fifth.')
    require(s.trace(A)==s.Rational(2,p),'The maximal singular space is not two-dimensional.')
    return {'modulus':M,'primitive_vectors':n,'domain_dimension':B.shape[1],
            'maximal_squared_singular_value':'1/5','maximal_singular_space_dimension':2,
            'exact_squared_norm_ratio':5}

def mul(x,y):return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def inv(x):
    norm=x[0]*x[0]-5*x[1]*x[1]
    return (F(x[0],norm),F(-x[1],norm))

def source_checks():
    census={r['id']:r['tensor'] for r in json.loads((ROOT/'supplements/rank7/output/m5/census.json').read_text())}
    low=json.loads((HERE.parent/'models/sqrt5/low_compression_certificate.json').read_text())['rings']
    out={}
    for rid,a in [('R7_5_3895',[1,5,5,10,8,8,9]),('R7_5_5039',[1,5,5,8,8,10,9])]:
        b=[0,2,2,4,4,4,4];d=list(zip(a,b));N=census[rid]
        digest=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
        require(digest==low[rid]['source_sha256'],'The low rows are not bound to the current tensor.')
        for i in range(7):
            for j in range(7):
                require(mul(d[i],d[j])==tuple(sum(N[i][j][k]*d[k][h] for k in range(7)) for h in range(2)),
                        'The proposed FP dimensions are not a ring character.')
        D=tuple(sum(mul(z,z)[h] for z in d) for h in range(2))
        require(D==(720,320),'Unexpected global dimension.')
        u=[2*a[i]-9*b[i]//2 for i in range(7)]
        for i,z in enumerate(d):
            left=mul(z,inv(D));right=mul((z[0],-z[1]),inv((D[0],-D[1])))
            require(tuple(left[h]-right[h] for h in range(2))==(0,F(-u[i],20)),
                    'The exact FP-character difference coefficient failed.')
        frames=[]
        for frame in low[rid]['frames']:
            rows=[[1,0,0,0,0,0,0]]+frame['low_rows']
            values=[sum(x*y for x,y in zip(u,v)) for v in rows]
            require(sorted(values)==[-2,0,0,0,0,0,2],'The induced-unit contribution is not exactly eight.')
            frames.append({'frame_index':frame['frame_index'],'u_values':values,'squared_weight':sum(x*x for x in values)})
        out[rid]={'source_sha256':digest,'dimensions':d,'global_dimension':D,'u_coefficients':u,
                  'S_difference':'-u/(4*sqrt(5))','total_squared_u_weight':160,
                  'known_induced_unit_weight':8,'five_primary_order_one_weight_bounds':[8,32],
                  'five_primary_order_five_weight':'4*c','frames':frames}
    return out

if __name__=='__main__':
    report={'status':'PASS','local_checks':[local_check(M) for M in (5,25,125)],'sources':source_checks()}
    (HERE/'prime_projection_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
