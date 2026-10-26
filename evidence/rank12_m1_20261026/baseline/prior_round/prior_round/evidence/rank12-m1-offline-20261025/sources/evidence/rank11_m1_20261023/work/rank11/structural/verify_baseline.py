#!/usr/bin/env python3
"""Independent exact replay of baseline and zero/one-spectrum certificates.

Only Python, SymPy, this directory, and the original source gzip are needed.
Set RANK11_SOURCE to relocate the source data. No discovery implementation or
lower-rank positive catalogue is imported. All checks survive Python -O.
"""
import collections
import itertools
import json
import time
from fractions import Fraction
import sympy as s
from support import OUT, load, require, sha

t = s.Symbol('t')

def dual(R):
    out=[]
    for i in range(len(R)):
        hits=[j for j in range(len(R)) if R[i][j][0]]
        require(len(hits)==1 and R[i][hits[0]][0]==1, 'unique dual')
        out.append(hits[0])
    return out

def casimir(R):
    return sum((s.Matrix(A)*s.Matrix(A).T for A in R),s.zeros(len(R)))

def embedded(R,J):
    n=len(R);du=dual(R)
    require(J and J[0]==0 and J==sorted(set(J)) and all(0<=i<n for i in J), 'based subset')
    require(all(du[i] in J for i in J), 'dual closure')
    require(all(not R[i][j][k] for i in J for j in J for k in range(n) if k not in J), 'product closure')
    return [[[R[i][j][k] for k in J]for j in J]for i in J]

def factor(R,co):
    q=s.Poly.from_list(co,t);p=casimir(R).charpoly(t).as_poly()
    require(q.LC()==1 and q.is_irreducible and p.rem(q).is_zero,'irreducible Casimir factor')
    return q

def check(R,c):
    kind=c['kind'];n=len(R)
    if kind=='excluded_lower_subring':
        J=c['subset'];S=embedded(R,J)
        require(len(J)==c['subrank'] and sha(S)==c['subtensor_sha256'],'embedded tensor identity')
        require('direct_subring_certificate' in c,'an explicit exclusion is required')
        check(S,c['direct_subring_certificate'])
    elif kind=='casimir_dnumber':
        q=factor(R,c['factor']);co=list(map(int,q.all_coeffs()));d=q.degree();j=c['index'];norm=abs(co[-1])
        require(1<=j<=d and norm>0,'d-number index and norm')
        rem=pow(co[j],d,norm**j)
        require(rem!=0 and rem==c['nonzero_remainder'],'d-number divisibility failure')
    elif kind=='integral_drinfeld':
        require(all(R[i][j]==R[j][i] for i in range(n) for j in range(n)),'commutative scope')
        dims=c['dims'];require(len(dims)==n and dims[0]==1 and all(type(d)is int and d>0 for d in dims),'positive integer dimension vector')
        require(all(sum(R[i][j][k]*dims[k] for k in range(n))==dims[i]*dims[j] for i,j in itertools.product(range(n),repeat=2)),'dimension homomorphism')
        D=sum(d*d for d in dims);require(D==c['global_dimension'],'global dimension')
        q=factor(R,c['failed_factor'])
        if q.degree()==1:
            f=-int(q.TC());require(f>0 and D%f!=0,'central induction dimension not integral')
        else:
            require(q.degree()>1,'nonrational formal codegree')
    elif kind=='two_dimension_induction':
        # The accepted rank-eleven witness is the C10+1 near-group ring.
        # Check the dimension relation and induction contradiction directly.
        require(all(R[i][j]==R[j][i] for i in range(n) for j in range(n)),'commutative scope')
        du=dual(R);G=[i for i in range(n) if sum(R[i][du[i]])==1];X=[i for i in range(n) if i not in G]
        require(G==c['invertibles'] and X==c['noninvertibles'] and len(X)==1,'near-group partition')
        x=X[0];require(x==c['object'] and du[x]==x,'near-group object')
        require(all(R[g][x][x]==R[x][g][x]==1 for g in G),'transitive action')
        r=R[x][x][x];h=len(G)
        require(all(R[x][x][g]==1 for g in G),'near-group square')
        require((h,r)==(10,1) and c['r']==r and c['s']==h and c['stabilizer']==G,'accepted dimensions')
        require(c['discriminant']==41 and c['D']==[20,1],'quadratic global dimension')
        q=factor(R,c['failed_factor']);require(q.all_coeffs()==[1,-10],'formal codegree ten')
        require(c['reason']=='not_nonnegative_integral_dimension_sum','witness type')
        require(list(map(Fraction,c['codegree_coordinates']))==[10,0],'codegree coordinates')
        require(list(map(Fraction,c['restriction_dimension_coordinates']))==[2,Fraction(1,10)],'restriction coordinates')
        # D/f = 2+d/10 is not in Z+Z*d; d=(1+sqrt(41))/2 is irrational.
        require(Fraction(1,10).denominator!=1,'dimension lattice failure')
    elif kind in ('zero_spectrum','one_spectrum'):
        spectrum(R,c)
    else:
        raise ValueError('unsupported accepted certificate '+kind)

def spectrum(R,c):
    n=len(R);inds=c['indices'];d=dual(R)
    require(all(type(i)is int and 0<=i<n for i in inds),'spectrum index bounds')
    dot=lambda i,j,k,l:sum(R[i][j][h]*R[k][l][h] for h in range(n))
    if c['kind']=='zero_spectrum':
        require(len(inds)==9,'nine indices');a,b,c0,u,v,w,x,y,z=inds
        require(all([R[u][a][w],R[v][u][b],R[v][w][c0],R[x][z][a],R[b][x][y],R[y][z][c0]]),'six nonzero boundary spaces')
        require(sum(R[u][x][k]*R[d[v]][y][k]*R[w][d[z]][k] for k in range(n))==0,'empty spectrum')
        require(R[b][a][c0]==1,'distinguished multiplicity one')
        require(1 in [dot(v,u,c0,d[a]),dot(b,d[u],c0,d[w]),dot(d[v],b,w,d[a])],'left forced invertible')
        require(1 in [dot(b,x,c0,d[z]),dot(y,d[x],c0,d[a]),dot(d[b],y,a,d[z])],'right forced invertible')
    else:
        require(len(inds)==10,'ten indices');q,a,b,c0,u,v,w,x,y,z=inds
        require(all([R[u][a][w],R[v][u][b],R[v][w][c0],R[x][z][a],R[b][x][y],R[y][z][c0]]),'six nonzero boundary spaces')
        require(sum(R[u][x][k]*R[d[v]][y][k]*R[w][d[z]][k] for k in range(n))==1,'equation6.13')
        require(R[u][x][q]==R[d[v]][y][q]==R[w][d[z]][q]==1,'equation6.14')
        require(R[b][a][c0]==0,'equation6.15')
        require(1 in [dot(v,u,y,d[x]),dot(v,q,b,x),dot(b,d[u],y,d[q])],'equation6.16')
        require(1 in [dot(v,q,c0,d[z]),dot(v,w,y,z),dot(y,d[q],c0,d[w])],'equation6.17')
        require(1 in [dot(u,x,w,d[z]),dot(u,a,q,z),dot(q,d[x],w,d[a])],'equation6.18')

def verify_inventory(rows,base):
    classes=base['subring_classes'];total=0
    require(len(classes)==33,'complete subring isomorphism inventory')
    for C in classes:
        require(sha(C['tensor'])==C['tensor_sha256'],'class tensor identity')
        if C['certificate']:check(C['tensor'],C['certificate'])
    for source,record in zip(rows,base['records']):
        R=source['tensor'];n=len(R);du=dual(R);actual=[]
        for mask in range(1,(1<<(n-1))-1):
            J=[0]+[i for i in range(1,n) if mask>>(i-1)&1]
            if any(du[i] not in J for i in J):continue
            if any(R[i][j][k] for i in J for j in J for k in range(n) if k not in J):continue
            actual.append(J)
        require(actual==[x['subset'] for x in record['proper_subrings']],'exhaustive proper based-subring inventory')
        for rec in record['proper_subrings']:
            J=rec['subset'];A=embedded(R,J);p=rec['source_to_class_basis_map'];B=classes[rec['class_index']]['tensor'];m=len(J)
            require(m==rec['subrank'] and sha(A)==rec['subtensor_sha256'],'subring inventory binding')
            require(p[0]==0 and sorted(p)==list(range(m)) and len(B)==m,'class basis bijection')
            require(all(A[i][j][k]==B[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(m),repeat=3)),'all embedded tensor coefficients')
        total+=len(actual)
    return total

def main():
    start=time.monotonic();rows=load();counts={};union=set();hist=collections.Counter()
    for name in ('baseline','zero_spectrum','one_spectrum'):
        data=json.loads((OUT/(name+'.json')).read_text());records=data['records'];require(len(records)==182,'full certificate inventory')
        accepted=[]
        for source,record in zip(rows,records):
            require((source['id'],source['tensor_sha256'])==(record['id'],record['tensor_sha256']),'physical source identity')
            cs=record.get('certificates', [record['certificate']] if record.get('certificate') else [])
            for c in cs:check(source['tensor'],c);hist[c['kind']]+=1
            if cs:accepted.append(record['id']);union.add(record['id'])
        require(accepted==data['excluded_ids'],'excluded IDs derive from certificates')
        counts[name]=len(accepted)
        if name=='baseline':subrings=verify_inventory(rows,data)
        print('PASS',name,len(accepted),flush=True)
    report=dict(status='PASS',input_count=182,counts=counts,distinct_excluded=len(union),certificate_counts=dict(hist),proper_subrings=subrings,subring_classes=33,elapsed_seconds=time.monotonic()-start)
    (OUT/'baseline_replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
