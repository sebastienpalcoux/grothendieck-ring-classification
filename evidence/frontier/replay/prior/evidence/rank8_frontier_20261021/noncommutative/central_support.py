"""Exact central-image refinement of noncommutative induction columns.

All accepted arithmetic is rational/algebraic. Pseudo-unitary scope only.
"""
from pathlib import Path
import argparse, itertools, json, math, sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=ROOT/'evidence/rank8_m3_20261021/noncommutative'
sys.path.insert(0,str(OLD))
import weighted_rank8 as w
from exact import vector,ec,require
from weighted_data_fast import low_frames
s=w.s

def restriction(ds,beta,r,K,B):
    n=len(ds); degree=K.mod.degree(); tail=n-1
    A=s.Matrix.hstack(*(vector(d,degree) for d in ds[1:])); b=vector(beta-K(r),degree)
    for u in B.nullspace():
        A=A.col_join(u[1:,:].T); b=b.col_join(s.Matrix([-r*u[0]]))
    rr,piv=A.row_join(b).rref()
    if tail in piv:return []
    free=[j for j in range(tail) if j not in piv]
    bounds=[min(int(B[0,i])//r,math.isqrt(int(B[i,i]))) for i in range(1,n)]
    out=[]
    for chosen in itertools.product(*(range(bounds[j]+1) for j in free)):
        v=[s.S.Zero]*tail
        for j,z in zip(free,chosen):v[j]=s.Integer(z)
        for row,j in enumerate(piv):v[j]=rr[row,tail]-sum(rr[row,k]*v[k] for k in free)
        if all(z.q==1 and 0<=z<=bounds[j] for j,z in enumerate(v)):
            c=(r,)+tuple(map(int,v)); require(all((u.T*s.Matrix(c))[0]==0 for u in B.nullspace()),'central support')
            out.append(c)
    return sorted(out)

def data(R):
    a=w.spectral(R)
    a['columns']=[restriction(a['ds'],a['D']/fc,r,a['K'],a['Gram']) for fc,r in zip(a['codegrees'][1:],a['multiplicities'][1:])]
    a['lows']=low_frames(a['columns'],a['multiplicities'][1:],a['Gram'])
    return a

def scan(R):
    a=data(R); B=a['Gram']; branches=[]
    for cols in a['lows']:
        why=w.core.low_failure(cols,B,a['ds'],a['D'],a['K'],a['embedding'],a['du'])
        L=s.Matrix.hstack(*map(s.Matrix,cols)); Q=B-L*L.T
        branches.append({'columns':list(map(list,cols)),'obstruction':why,'residual_rank':Q.rank(),'residual_gram':list(map(list,Q.tolist()))})
    return {'scope':'pseudo_unitary_only','gram_rank':B.rank(),'kernel':[list(map(int,u)) for u in B.nullspace()],
            'column_counts':list(map(len,a['columns'])),'columns':a['columns'],'low_count':len(a['lows']),
            'passing_low_count':sum(x['obstruction'] is None for x in branches),'branches':branches}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--write',action='store_true');args=ap.parse_args()
    census=json.loads((OLD.parent/'pipeline/census_m3.json').read_text()); targets={721,928,941,1154};out=[]
    for r in census:
        if int(r['id'].split('_')[-1]) not in targets:continue
        rec={'id':r['id'],'tensor_sha256':r['tensor_sha256'],**scan(r['tensor'])};out.append(rec)
        print(r['id'],rec['column_counts'],rec['low_count'],rec['passing_low_count'],flush=True)
    # Convert SymPy integers, preserving exact values.
    out=json.loads(json.dumps(out,default=int))
    path=HERE/'central_support_results.json'
    if args.write:path.write_text(json.dumps(out,indent=2)+'\n')
    else:require(json.loads(path.read_text())==out,'central support replay differs')

if __name__=='__main__':main()
