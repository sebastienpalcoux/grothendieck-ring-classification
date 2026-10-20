"""Optimizer-free replay of a quartic fusion-integrality witness obstruction."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import sympy as s

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(HERE.parents[1]/'criteria'))
import q5_center_trace as q
from exact_quadratic_characters import ExactQuadraticCharacterTable
SOURCE_HASH='8606c63a2f02ea028185db755a4b055382073b94736d5040ee92f3eec07f450c'
WITNESS_HASH='8d9681693d7de504c389919f8968d4a4bac01a01312fcd9aa5bb81b4ffc9eda3'


def conjugate(t):
    """max_{k>=0 integral} (t*k-k*k), with exact rational arithmetic."""
    k=max(0,int(s.floor(t/2)))
    return max(t*k-k*k,t*(k+1)-(k+1)**2)


def verify(record):
    N=next(r['tensor'] for r in json.loads((ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==record['id'])
    q.require(q.tensor_hash(N)==record['source_sha256']==SOURCE_HASH,'pinned source tensor')
    q.require(record['witness_sha256']==WITNESS_HASH,'pinned discovery witness identity')
    low=record['low'];high=record['high_rows'];rows=low+high
    q.require(len(low)==7 and len(high)==48,'pinned center rank55')
    q.require(all(len(v)==7 and all(type(x) is int and x>=0 for x in v) for v in rows),'nonnegative integral restriction rows')
    ds,D,B,zs,T,signs=q.source_data(N,record['id']);table=ExactQuadraticCharacterTable(N,ds,5);K=table.K
    q.require((s.Matrix(rows).T*s.Matrix(rows)).tolist()==B,'complete restriction Gram')
    labels=record['low_labels'];q.require(labels==[2,0,3,4,5,6,1] and labels[0]==table.fp,'pinned low labels')
    values=[[sum((K(v[i])*ch[i] for i in range(7)),K.zero) for ch in table.rows] for v in rows]
    dims=[sum((K(v[i])*table.ds[i] for i in range(7)),K.zero) for v in rows]
    for i,E in enumerate(labels):
        q.require(dims[i]==table.D/table.codegrees[E],'low dimension/formal-codegree matching')
        for j,F in enumerate(labels):q.require(values[j][E]/table.codegrees[E]==values[i][F]/table.codegrees[F],'low S symmetry')
    dual=[next(j for j,ch in enumerate(table.rows) if ch==tuple(row[table.du[i]] for i in range(7))) for row in table.rows]
    def moment(indices):
        value=K.zero
        for val,d in zip(values,dims):
            term=K.one/d**(len(indices)-2)
            for E in indices:term*=val[E]/table.codegrees[E]
            value+=term
        return K.to_sympy(table.D**(len(indices)-2)*value)
    E,F=record['characters'];a,b=record['low_objects']
    q.require((a,b)==(1,6) and (E,F)==(0,1) and labels[a]==E and labels[b]==F,'pinned product')
    n=[moment((E,F,dual[G])) for G in labels]
    q.require(n==record['low_coefficients_at_witness'],'exact low product coefficients')
    quartic=moment((E,F,dual[E],dual[F]));q.require(quartic==1621,'exact quartic norm')
    product=s.Matrix([[sum(low[a][i]*low[b][j]*N[i][j][k] for i in range(7) for j in range(7)) for k in range(7)]])
    q.require(list(product)==record['source_product'],'forgetful product')
    residual=product-s.Matrix([n])*s.Matrix(low);V=s.Matrix(high)
    columns=(V.T*V).rref()[1];W=V[:,columns]
    projection=residual[:,columns]*(W.T*W).inv()*W.T
    q.require(projection*V==residual,'projection satisfies every restriction equation')
    high_norm=quartic-sum(t*t for t in n)
    q.require(high_norm==(projection*projection.T)[0]==1326,'quartic projection saturation')
    q.require(any(not t.is_Integer for t in projection),'forced nonintegral fusion coefficient')
    x=s.Matrix([[s.Rational(t) for t in record['x']]])
    q.require(x==s.Matrix([[0,s.Rational(1,2),s.Rational(1,2),1,1,1,1]]),'pinned exact cut vector')
    weights=[2*n0+1-(x*s.Matrix(v))[0] for n0,v in zip(n,low)]
    constant=(x*product.T)[0]-sum(t*(t+1) for t in n)
    rhs=constant+sum(w*t for w,t in zip(weights,n))-sum(conjugate((x*s.Matrix(v))[0]) for v in high)
    q.require(weights==[1,3,1,1,1,1,1] and constant==2894,'global linear-cut coefficients')
    q.require(rhs==1625 and rhs-quartic==record['violation']==4,'strict exact integer-norm cut violation')
    return {'status':'PASS','scope':'Rejects this rank55 necessary-data witness only; the linear cut is necessary for every categorification with this labelled low frame.',
            'center_rank':55,'quartic':str(quartic),'high_norm':str(high_norm),'linear_lower_bound':str(rhs),'strict_gap':str(rhs-quartic),
            'forced_fractional_values':sorted(set(str(t) for t in projection if not t.is_Integer)),
            'numerical_optimizers_used':False}


if __name__=='__main__':
    path=HERE/'R5039_c2_fp5_integral_norm_cut.json';record=json.loads(path.read_text());result=verify(record)
    bad=copy.deepcopy(record);bad['high_rows'][0][1]+=1
    try:verify(bad)
    except (ValueError,RuntimeError):result['altered_row_control_rejected']=True
    else:raise ValueError('altered row accepted')
    result.update(optimized_python=not __debug__,source_sha256=SOURCE_HASH,certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    out=HERE/('integral_norm_cut_optimized.json' if not __debug__ else 'integral_norm_cut_normal.json')
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
