"""Aggregate integer fusion intertwiners and exact Frobenius-norm budgets.

High simples with equal restriction rows are grouped only for necessary tests.
For selfdual A, X_uv is the sum of N_A entries in the corresponding block.
It is symmetric integral and satisfies X M=diag(m) M L_F(A). Its diagonal
block traces have the same parity as X_uu. The fixed spectral square trace
bounds the sum of the least squared entry sums in each block.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import time
import central_fusion_extension as e


def discover(data,a,seconds,norm=True):
    import numpy as np
    from scipy.optimize import milp,Bounds,LinearConstraint
    from scipy.sparse import coo_matrix
    e.q.require(data['lowdual'][a]==a,'selfdual object for symmetric aggregation')
    counts=Counter(data['rows'][7:]);rows=data['rows'][:7]+sorted(counts)
    mult=[1]*7+[counts[v] for v in rows[7:]];n=len(rows);source=data['source']
    target=[[mult[y]*sum(rows[y][i]*rows[a][j]*source[j][i][k] for i in range(7) for j in range(7)) for k in range(7)] for y in range(n)]
    cells=[];index={};lb=[];ub=[];integral=[]
    for y in range(n):
        for z in range(y,n):
            upper=min([target[y][k]//rows[z][k] for k in range(7) if rows[z][k]]+[target[z][k]//rows[y][k] for k in range(7) if rows[y][k]])
            lower=0
            if y<7 and z<7:lower=upper=data['lowcoeff'][a][y][z]
            if y==0:lower=upper=int(z==a)
            index[y,z]=index[z,y]=len(cells);cells.append((y,z));lb.append(lower);ub.append(upper);integral.append(1)
    diagonal=[];offdiagonal=[]
    for y in range(n):
        diagonal.append(len(lb));lb.append(0);ub.append(ub[index[y,y]]);integral.append(1)
        offdiagonal.append(len(lb));lb.append(0);ub.append(ub[index[y,y]]//2);integral.append(1)
    costs=[]
    if norm:
        for y,z in cells:costs.append(len(lb));lb.append(0);ub.append(data['squares'][a]);integral.append(0)
    equations=[];lower=[];upper=[]
    def constraint(row,l,u):equations.append(row);lower.append(l);upper.append(u)
    for y in range(n):
        for k in range(7):constraint({index[y,z]:rows[z][k] for z in range(n) if rows[z][k]},target[y][k],target[y][k])
        constraint({index[y,y]:1,diagonal[y]:-1,offdiagonal[y]:-2},0,0)
        if mult[y]==1:constraint({offdiagonal[y]:1},0,0)
    constraint({j:1 for j in diagonal},data['traces'][a],data['traces'][a])
    if norm:
        for j,(y,z) in enumerate(cells):
            capacity=mult[y]*mult[z]
            for q in range(ub[j]//capacity+1):
                constraint({costs[j]:1,j:-(2*q+1)},-capacity*q*(q+1),np.inf)
        constraint({costs[j]:(1 if y==z else 2) for j,(y,z) in enumerate(cells)},-np.inf,data['squares'][a])
    rr=[];cc=[];vv=[]
    for r,row in enumerate(equations):
        for j,v in row.items():rr.append(r);cc.append(j);vv.append(v)
    A=coo_matrix((vv,(rr,cc)),shape=(len(equations),len(lb))).tocsc()
    start=time.monotonic()
    result=milp(np.zeros(len(lb)),integrality=integral,bounds=Bounds(lb,ub),constraints=LinearConstraint(A,lower,upper),options={'time_limit':seconds})
    out={'object':a,'norm_bound':norm,'status':int(result.status),'message':result.message,'seconds':time.monotonic()-start,'groups':n,'variables':len(lb),'constraints':len(equations),'trace':data['traces'][a],'trace_square':data['squares'][a]}
    if result.x is not None:
        sol=[int(round(x)) if integral[j] else float(x) for j,x in enumerate(result.x)]
        mat=[[sol[index[y,z]] for z in range(n)] for y in range(n)]
        e.q.require(all(sum(mat[y][z]*rows[z][k] for z in range(n))==target[y][k] for y in range(n) for k in range(7)),'exact aggregate intertwiner')
        diag=[sol[j] for j in diagonal]
        e.q.require(sum(diag)==data['traces'][a] and all(0<=diag[y]<=mat[y][y] and (mat[y][y]-diag[y])%2==0 for y in range(n)),'aggregate diagonal trace and parity')
        def least_square(total,capacity):q,r=divmod(total,capacity);return capacity*q*q+r*(2*q+1)
        least=sum((1 if y==z else 2)*least_square(mat[y][z],mult[y]*mult[z]) for y,z in cells)
        e.q.require(not norm or least<=data['squares'][a],'exact least possible block square norm')
        out.update(exact_feasible=True,matrix=mat,diagonal=diag,least_square_norm=least,group_rows=rows,group_multiplicities=mult)
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('witness');p.add_argument('--seconds',type=float,default=20);p.add_argument('--objects',default='1,4,5,6');p.add_argument('--without-norm',action='store_true');a=p.parse_args()
    data=e.load(a.witness);result={'id':data['id'],'witness_sha256':data['witness_sha256'],'source_sha256':data['source_sha256'],'scope':'Necessary aggregate integer fusion matrices of this fixed witness; neither a full fusion ring nor a categorification.','results':[]}
    path=e.HERE/(Path(a.witness).stem+('_aggregate_linear.json' if a.without_norm else '_aggregate_norm.json'))
    for i in map(int,a.objects.split(',')):
        rec=discover(data,i,a.seconds,not a.without_norm);result['results'].append(rec);path.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in rec.items() if k not in ('matrix','group_rows','group_multiplicities','diagonal')}),flush=True)


if __name__=='__main__':main()
