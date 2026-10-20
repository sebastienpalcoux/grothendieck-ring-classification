"""Exact full low-product Gram and integer norm-decomposition discovery."""
import argparse
from collections import Counter
import itertools
import json
import math
from pathlib import Path
import time
import sympy as s
import central_fusion_extension as e


def gram_data(data,path):
    four=json.loads((e.EVIDENCE/'computation/low_four_point_full_field.json').read_text())
    rec=next((r for r in four['results'] if r['file']==Path(path).name),None)
    if rec is None:
        other=json.loads((e.EVIDENCE/'computation'/('low_four_point_'+data['id']+'_fp5.json')).read_text())
        if isinstance(other,dict):other=other['results']
        rec=next(r for r in other if r['file']==Path(path).name)
    e.q.require(not rec['violations'],'integral quartic coefficients required')
    coefficients=rec['coefficients'];label=data['label'];du=data['lowdual'];low=data['lowcoeff']
    pairs=list(itertools.combinations_with_replacement(range(1,7),2));rows=data['rows'];source=data['source']
    G=[];R=[]
    for a,b in pairs:
        grow=[]
        for c,d in pairs:
            key=','.join(map(str,sorted((label[a],label[b],label[du[c]],label[du[d]]))))
            value=s.Rational(coefficients[key])-sum(low[a][b][z]*low[c][d][z] for z in range(7))
            e.q.require(value.is_Integer,'integral high-product Gram entry');grow.append(int(value))
        G.append(grow)
        R.append([sum(rows[a][i]*rows[b][j]*source[i][j][k] for i in range(7) for j in range(7))-sum(low[a][b][z]*rows[z][k] for z in range(7)) for k in range(7)])
    V=s.Matrix(rows[7:]);G=s.Matrix(G);R=s.Matrix(R);J=V.T*V
    # The seven-column restriction rows have zero unit column. Choose a full basis.
    basis=J.rref()[1];VV=V[:,basis];RR=R[:,basis];J=VV.T*VV
    projection=RR*J.inv()*VV.T
    slack=G-projection*projection.T
    e.q.require(slack==slack.T,'symmetric orthogonal Gram slack')
    forced=[]
    for i,pair in enumerate(pairs):
        if slack[i,i]==0:
            forced.append({'pair':pair,'coefficients':[str(x) for x in projection[i,:]],'nonintegral':any(not x.is_Integer or x<0 for x in projection[i,:])})
    return {'pairs':pairs,'G':G,'R':R,'V':V,'slack':slack,'projection':projection,'forced':forced}


def norm_decompose(data,gd,index,seconds,packets=False,balancing=False):
    import numpy as np
    from scipy.optimize import milp,Bounds,LinearConstraint
    from scipy.sparse import coo_matrix
    count=Counter(data['rows'][7:]);rows=sorted(count);weights=[[1] for v in rows]
    if packets or balancing:
        count=Counter((v,p['phase']) for v,p in zip(data['rows'][7:],data['provenance'][7:]))
        groups=sorted(count);rows=[v for v,phase in groups]
        records=data['phase_records'];weights=[]
        for v,phase in groups:
            rec=records[phase]
            weights.append((rec.get('zero_semigroup') or [rec['fixed_row_multiple']]) if packets else [1])
        multiplicities=[count[g] for g in groups]
    else:multiplicities=[count[v] for v in rows]
    target=list(map(int,gd['R'][index,:]));norm=int(gd['G'][index,index])
    choices=[];upper=[]
    for gi,v in enumerate(rows):
        bound=min([target[k]//v[k] for k in range(7) if v[k]]+[math.isqrt(norm)])
        for k in range(bound+1):
            for w in weights[gi]:choices.append((gi,k,w));upper.append(multiplicities[gi]//w)
    rr=[];cc=[];vv=[];rhs=target+[norm]+multiplicities
    phase_columns=[]
    if balancing:
        table=data['table'];K=table.K;a,b=gd['pairs'][index];E=data['label'][data['lowdual'][a]]
        val=sum((K(t)*v for t,v in zip(data['rows'][b],table.rows[E])),K.zero)
        target_value=table.D*val/table.codegrees[E]
        known=sum((K(data['lowcoeff'][a][b][j])*sum((K(t)*d for t,d in zip(data['rows'][j],table.ds)),K.zero) for j in range(7)),K.zero)
        sym=s.expand(K.to_sympy(target_value-known));beta=sym.coeff(s.sqrt(5));alpha=s.simplify(sym-beta*s.sqrt(5))
        e.q.require(alpha.is_Rational and beta.is_Rational,'real quadratic balancing target')
        balance_rhs=[8*alpha,8*beta]+[0]*6
        for v,phase in groups:
            aa=sum(v[i]*data['dimension_pairs'][i][0] for i in range(7));bb=sum(v[i]*data['dimension_pairs'][i][1] for i in range(7))
            rec=records[phase];phase_vector=rec['scaled8'][:8]
            out=[]
            for i in range(0,8,2):out.extend([aa*phase_vector[i]+5*bb*phase_vector[i+1],bb*phase_vector[i]+aa*phase_vector[i+1]])
            phase_columns.append(out)
        balance_offset=len(rhs);rhs+=balance_rhs
    for j,(gi,k,w) in enumerate(choices):
        for d in range(7):
            if rows[gi][d]*k:rr.append(d);cc.append(j);vv.append(w*rows[gi][d]*k)
        if k:rr.append(7);cc.append(j);vv.append(w*k*k)
        rr.append(8+gi);cc.append(j);vv.append(w)
        if balancing:
            for d,value in enumerate(phase_columns[gi]):
                if value*k:rr.append(balance_offset+d);cc.append(j);vv.append(w*k*value)
    A=coo_matrix((vv,(rr,cc)),shape=(len(rhs),len(choices))).tocsc();start=time.monotonic()
    res=milp(np.zeros(len(choices)),integrality=np.ones(len(choices)),bounds=Bounds(np.zeros(len(choices)),upper),constraints=LinearConstraint(A,rhs,rhs),options={'time_limit':seconds})
    rec={'pair':gd['pairs'][index],'norm':norm,'status':int(res.status),'seconds':time.monotonic()-start,'variables':len(choices),'galois_packets':packets,'balancing':balancing}
    if res.x is not None:
        sol=[int(round(x)) for x in res.x];hist=[[] for _ in rows]
        packet_support=[]
        for (gi,k,w),n in zip(choices,sol):
            hist[gi].extend([k]*(w*n))
            if n:packet_support.append([gi,k,w,n])
        e.q.require(all(len(h)==m for h,m in zip(hist,multiplicities)),'all high copies accounted for')
        e.q.require(sum(k*k for h in hist for k in h)==norm,'exact prescribed squared fusion norm')
        e.q.require(all(sum(sum(h)*v[d] for h,v in zip(hist,rows))==target[d] for d in range(7)),'exact fusion residual restriction')
        if balancing:e.q.require(all(sum(sum(h)*v[d] for h,v in zip(hist,phase_columns))==balance_rhs[d] for d in range(8)),'exact relative-trace balancing')
        rec.update(exact_feasible=True,rows=rows,coefficient_multisets=hist,packet_support=packet_support)
    return rec


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('witness');p.add_argument('--seconds',type=float,default=10);p.add_argument('--pairs',default='0,1,2,3,4,5');p.add_argument('--packets',action='store_true');p.add_argument('--balancing',action='store_true');a=p.parse_args()
    data=e.load(a.witness);gd=gram_data(data,a.witness)
    result={'id':data['id'],'witness_sha256':data['witness_sha256'],'source_sha256':data['source_sha256'],'pairs':gd['pairs'],'gram':gd['G'].tolist(),'residual':gd['R'].tolist(),'gram_rank':gd['G'].rank(),'orthogonal_slack_rank':gd['slack'].rank(),'orthogonal_slack_diagonal':[str(gd['slack'][i,i]) for i in range(len(gd['pairs']))],'forced':gd['forced'],'results':[]}
    print(json.dumps({k:v for k,v in result.items() if k not in ('gram','residual')}),flush=True)
    path=e.HERE/(Path(a.witness).stem+('_balanced' if a.balancing else '')+('_packet_product_gram.json' if a.packets else '_product_gram.json'))
    for i in map(int,a.pairs.split(',')):
        rec=norm_decompose(data,gd,i,a.seconds,a.packets,a.balancing);result['results'].append(rec)
        path.write_text(json.dumps(result,indent=2,default=int)+'\n');print(json.dumps({k:v for k,v in rec.items() if k not in ('rows','coefficient_multisets','packet_support')}),flush=True)


if __name__=='__main__':main()
