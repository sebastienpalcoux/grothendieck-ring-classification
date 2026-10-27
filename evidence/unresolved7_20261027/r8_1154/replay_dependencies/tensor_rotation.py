"""Cyclic-character compatibility for tensor powers in the center trace system.
Numerical optimization proposes dual rays; verification uses only exact integers.
"""
from balanced_traces import *

def rotation_types(q,n,rs):
    conductor=1 if q==1 else q if q%4==1 else 4*q
    out=set()
    for order in s.divisors(n):
        order=int(order)
        for sign in (-1,1):
            values=[]
            for r in rs:
                g=math.gcd(order,r);v=order//g;phi=int(s.totient(v));a=Q(int(s.mobius(v)),phi);b=Q(0)
                if q>1 and v%conductor==0:
                    z=v//conductor
                    if math.gcd(z,conductor)==1:
                        b=Q(sign*int(s.mobius(z))*int(s.kronecker_symbol(conductor,z))*int(s.kronecker_symbol(conductor,r//g))*math.isqrt(conductor//q),phi)
                values.append((a,b))
            out.add(tuple(values))
    return sorted(out)

def system_rotation(R,data,L,ep,height=6,rotation_height=None):
    if rotation_height is None:rotation_height=height
    require(rotation_height<=height,'rotation moments outside center trace range')
    A,b,meta=system(R,data,L,ep,height);oldvars=len(A[0]);q=data['q'];d=data['dimensions'];D=data['global_dimension'];n=len(R);labs=meta['labels'];types,_=trace_types(q,data['primes'],height);LL=L*L.T
    low=[tuple(sum((Q(int(LL[i,j]))*d[j][a] for j in range(n)),Q(0)) for a in range(2)) for i in range(n)]
    require(low[0]==D,'unit low dimension mismatch')
    dims=[tuple(sum(Q(v[i-1])*d[i][a] for i in range(1,n)) for a in range(2)) for v,ti in labs]
    rows=[];rhs=[];blocks=[];nextvar=oldvars
    for obj in range(1,n):
        powers=[[1]+[0]*(n-1)]
        for r in range(1,rotation_height+1):powers.append([sum(powers[-1][i]*R[i][obj][j] for i in range(n)) for j in range(n)])
        for order in range(3,rotation_height+1):
            rs=[int(r) for r in s.divisors(order) if r<order];rot=rotation_types(q,order,rs);start=nextvar;nextvar+=len(rot);blocks.append({'object':obj,'order':order,'start':start,'count':len(rot)})
            rows.append({start+k:Q(1) for k in range(len(rot))});rhs.append(Q(powers[order][0]))
            for at,r in enumerate(rs):
                k=order//r
                for component in range(2):
                    row={};const=sum(Q(powers[r][i])*low[i][component] for i in range(n))
                    for j,(v,ti) in enumerate(labs):
                        coeff=sum(powers[r][i]*v[i-1] for i in range(1,n))
                        x=coeff*mul(dims[j],types[ti][k-1],q)[component]
                        if x:row[j]=-x
                    for l,tt in enumerate(rot):
                        x=mul(D,tt[at],q)[component]
                        if x:row[start+l]=x
                    rows.append(row);rhs.append(const)
    for row in A:row.extend([0]*(nextvar-oldvars))
    for sparse,c in zip(rows,rhs):
        den=math.lcm(c.denominator,*(x.denominator for x in sparse.values()));rr=[0]*nextvar
        for j,x in sparse.items():rr[j]=int(x*den)
        c=int(c*den);g=math.gcd(c,*rr) or 1;A.append([x//g for x in rr]);b.append(c//g)
    meta.update(rotation_height=rotation_height,rotation_rows=len(rows),rotation_variables=nextvar-oldvars,rotation_blocks=blocks)
    return A,b,meta

def certificate(R,height=6):
    data=quadratic_data(R,gram_prune=True)
    if data is None:return None
    branches=[]
    for ix,cols in enumerate(data['lows']):
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du);branch={'columns':[list(c) for c in cols]}
        if why:branch['ordinary']=why
        else:
            L=s.Matrix.hstack(*map(s.Matrix,cols));cases=[]
            for ep in indicator_choices(R):
                A,b,meta=system_rotation(R,data,L,ep,height);y=farkas(A,b)
                if y is None:return None
                cases.append({'indicators':list(ep),'y':y,'bTy':sum(x*z for x,z in zip(b,y))})
            branch['rotation']=cases
        branches.append(branch)
    return {'kind':'tensor_rotation_traces','height':height,'q':data['q'],'column_counts':list(map(len,data['columns'])),'branches':branches}

def verify(R,c):
    data=quadratic_data(R,gram_prune=True);require(data is not None,'ineligible rotation ring');require(c['kind']=='tensor_rotation_traces' and c['q']==data['q'],'bad rotation certificate');require(c['column_counts']==list(map(len,data['columns'])),'incomplete rotation low columns');require(len(c['branches'])==len(data['lows']),'missing rotation low branches')
    for cols,branch in zip(data['lows'],c['branches']):
        require(branch['columns']==[list(v) for v in cols],'wrong rotation low branch');why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:require(branch.get('ordinary')==why,'bad rotation ordinary obstruction');continue
        eps=indicator_choices(R);require([case['indicators'] for case in branch['rotation']]==list(map(list,eps)),'missing rotation indicators');L=s.Matrix.hstack(*map(s.Matrix,cols))
        for ep,case in zip(eps,branch['rotation']):
            A,b,meta=system_rotation(R,data,L,ep,c['height']);check_farkas(A,b,case['y']);require(case['bTy']==sum(x*z for x,z in zip(b,case['y'])),'wrong separating value')

if __name__=='__main__':
    import argparse,time
    from pathlib import Path
    P=Path(__file__).resolve().parents[1];ap=argparse.ArgumentParser();ap.add_argument('ring');ap.add_argument('--height',type=int,default=6);a=ap.parse_args();r=next(r for r in json.load(open(P/'data/census.json')) if r['id']==a.ring);st=time.monotonic();c=certificate(r['N'],a.height)
    if c:verify(r['N'],c)
    out={'id':r['id'],'scope':'pseudo_unitary','height':a.height,'seconds':time.monotonic()-st,'certificate':c};(P/f'research/rotation_{a.ring}_h{a.height}.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print(r['id'],a.height,'EXCLUDED' if c else 'NOT EXCLUDED',out['seconds'],flush=True)
