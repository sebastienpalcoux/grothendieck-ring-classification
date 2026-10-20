"""Discovery of finite central fusion-matrix extensions of necessary data.

This is a stronger necessary-data check, never a categorical construction.
Matrix convention: L_A[Y,Z]=[A tensor Y:Z]. Thus L_A M=M L_F(A),
L_A[1,Z]=delta(A,Z), and L_A[Y,1]=delta(A*,Y).
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
EVIDENCE=HERE.parents[1]
sys.path.insert(0,str(EVIDENCE/'criteria'))
import q5_center_trace as q
from exact_quadratic_characters import ExactQuadraticCharacterTable


def load(path):
    raw=json.loads(Path(path).read_text()); rid=raw['id']
    source=next(x['tensor'] for x in json.loads((ROOT/'supplements/rank7/output/m5/census.json').read_text()) if x['id']==rid)
    q.require(q.tensor_hash(source)==raw['source_sha256'],'pinned tensor')
    result=next(r for r in raw['results'] if r.get('exact_feasible'))
    low=[(1,0,0,0,0,0,0)]+[tuple(v) for v in raw['low']]
    rows=list(low); provenance=[{'low':i} for i in range(7)]
    for rec in result['support']:
        for row,_,_ in raw['orbits'][rec['orbit']]:
            for copy in range(rec['multiplicity_unit']*rec['count']):
                rows.append((0,)+tuple(row)); provenance.append({**rec,'copy':copy})
    dimensions,D,B,zs,T,signs=q.source_data(source,rid)
    q.require([[sum(v[i]*v[j] for v in rows) for j in range(7)] for i in range(7)]==B,'restriction Gram')
    table=ExactQuadraticCharacterTable(source,dimensions,5)
    dom=next(r for r in json.loads((EVIDENCE/'integral_gram'/(rid+'_domains.json')).read_text()) if r['low_index']==result['index'])
    label=dom['cases'][result['case']]['label'];K=table.K
    dual_chars=[next(j for j,row in enumerate(table.rows) if row==tuple(ch[table.du[i]] for i in range(7))) for ch in table.rows]
    lowdual=[label.index(dual_chars[ch]) for ch in label]
    triples=list(itertools.combinations_with_replacement([i for i in range(7) if i!=table.fp],3))
    coeff=dict(zip(triples,result['verlinde_coefficients']))
    def triple(a,b,c):
        if table.fp in (a,b,c):
            x=[a,b,c];x.remove(table.fp)
            return int(x[0]==dual_chars[x[1]])
        return coeff[tuple(sorted((a,b,c)))]
    lows=[[[triple(label[a],label[y],dual_chars[label[z]]) for z in range(7)] for y in range(7)] for a in range(7)]
    # Recompute every recorded coefficient, without trusting the discovery cache.
    vals=[];dims=[]
    for row in rows:
        dims.append(sum((K(v)*d for v,d in zip(row,table.ds)),K.zero))
        vals.append([sum((K(v)*c for v,c in zip(row,ch)),K.zero) for ch in table.rows])
    for abc,c in coeff.items():
        a,b,c0=abc
        value=table.D/(table.codegrees[a]*table.codegrees[b]*table.codegrees[c0])
        value*=sum((v[a]*v[b]*v[c0]/d for v,d in zip(vals,dims)),K.zero)
        q.require(value==K(c),'exact low Verlinde coefficient')
    traces=[];squares=[]
    for a in range(7):
        ch=label[a]
        eigenvalues=[table.D*v[ch]/(table.codegrees[ch]*d) for v,d in zip(vals,dims)]
        trace=sum(eigenvalues,K.zero)
        trace=K.to_sympy(trace)
        q.require(trace.is_Integer and trace>=0,'integral nonnegative fusion trace')
        traces.append(int(trace))
        square=K.to_sympy(sum((x*x for x in eigenvalues),K.zero))
        q.require(square.is_Integer and square>=0,'integral nonnegative spectral square trace')
        squares.append(int(square))
    return dict(id=rid,source=source,rows=rows,provenance=provenance,phase_records=raw['phase_records'],lowdual=lowdual,lowcoeff=lows,traces=traces,squares=squares,label=label,dimension_pairs=dimensions,table=table,
                witness_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),source_sha256=q.tensor_hash(source))


def exact_check(data,a,mat):
    rows=data['rows'];n=len(rows);source=data['source'];low=data['lowcoeff'][a]
    q.require(len(mat)==n and all(len(r)==n for r in mat),'matrix shape')
    q.require(all(type(v) is int and v>=0 for row in mat for v in row),'nonnegative integral entries')
    q.require(all(mat[y][z]==low[y][z] for y in range(7) for z in range(7)),'low fusion block')
    if data['lowdual'][a]==a:q.require(all(mat[y][z]==mat[z][y] for y in range(n) for z in range(n)),'selfadjoint fusion matrix')
    else:q.require(all(mat[y][z]==data['lowcoeff'][data['lowdual'][a]][z][y] for y in range(7) for z in range(7)),'adjoint low block')
    target=[[sum(rows[y][i]*rows[a][j]*source[j][i][k] for i in range(7) for j in range(7)) for k in range(7)] for y in range(n)]
    q.require(all(sum(mat[y][z]*rows[z][k] for z in range(n))==target[y][k] for y in range(n) for k in range(7)),'complete fusion restriction intertwiner')
    q.require(all(mat[0][z]==int(z==a) for z in range(n)),'unit row')
    q.require(all(mat[y][0]==int(y==data['lowdual'][a]) for y in range(n)),'unit column')
    q.require(sum(mat[i][i] for i in range(n))==data['traces'][a],'known spectral trace')
    return True


def discover(data,a,seconds):
    import numpy as np
    from scipy.optimize import milp,Bounds,LinearConstraint
    from scipy.sparse import coo_matrix
    rows=data['rows'];n=len(rows);source=data['source'];low=data['lowcoeff'][a]
    symmetric=data['lowdual'][a]==a
    target=[[sum(rows[y][i]*rows[a][j]*source[j][i][k] for i in range(7) for j in range(7)) for k in range(7)] for y in range(n)]
    cells=[];index={};lower=[];upper=[]
    for y in range(n):
        for z in range(y if symmetric else 0,n):
            ub=min([target[y][k]//rows[z][k] for k in range(7) if rows[z][k]] or [0])
            if symmetric:ub=min(ub,min([target[z][k]//rows[y][k] for k in range(7) if rows[y][k]] or [0]))
            lb=0
            if y<7 and z<7:lb=ub=low[y][z]
            if y==0:lb=ub=int(z==a)
            if z==0:lb=ub=int(y==data['lowdual'][a])
            index[y,z]=len(cells)
            if symmetric:index[z,y]=len(cells)
            cells.append((y,z));lower.append(lb);upper.append(ub)
    rr=[];cc=[];vv=[];rhs=[]
    for y in range(n):
        for k in range(7):
            r=len(rhs);rhs.append(target[y][k])
            for z in range(n):
                if rows[z][k]:rr.append(r);cc.append(index[y,z]);vv.append(rows[z][k])
    r=len(rhs);rhs.append(data['traces'][a])
    for y in range(n):rr.append(r);cc.append(index[y,y]);vv.append(1)
    matrix=coo_matrix((vv,(rr,cc)),shape=(len(rhs),len(cells))).tocsc()
    start=time.monotonic()
    res=milp(np.zeros(len(cells)),integrality=np.ones(len(cells)),bounds=Bounds(lower,upper),constraints=LinearConstraint(matrix,rhs,rhs),options={'time_limit':seconds})
    out={'low_object':a,'selfdual':symmetric,'status':int(res.status),'message':res.message,'seconds':time.monotonic()-start,'variables':len(cells),'equations':len(rhs)}
    if res.x is not None:
        sol=[int(round(x)) for x in res.x]
        mat=[[sol[index[y,z]] for z in range(n)] for y in range(n)]
        exact_check(data,a,mat);out['exact_feasible']=True;out['matrix']=mat
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('witness');p.add_argument('--seconds',type=float,default=20);p.add_argument('--objects',default='1,2,3,4,5,6');args=p.parse_args()
    data=load(args.witness)
    result={'id':data['id'],'center_rank':len(data['rows']),'rows':data['rows'],'label':data['label'],'lowdual':data['lowdual'],'source_sha256':data['source_sha256'],'witness_sha256':data['witness_sha256'],'scope':'Necessary individual fusion-matrix extensions, without mutual commutativity, full associativity, or categorical existence.','results':[]}
    target=HERE/(Path(args.witness).stem+'_central_extension.json')
    for a in map(int,args.objects.split(',')):
        out=discover(data,a,args.seconds);result['results'].append(out)
        target.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in out.items() if k!='matrix'}),flush=True)


if __name__=='__main__':main()
