#!/usr/bin/env python3
"""Independent normalized-cochain and ring-hypothesis audit for C4 exclusion.

No assertion or finite-field rank oracle is trusted. GF(2) equations are
represented as integers and every resulting cocycle is directly evaluated.
This checks finite hypotheses; the categorical argument is in the audit note.
"""
import itertools,json
from support import OUT,load,require
from verify_baseline import dual

def rref(rows,n):
    basis={}
    for row in rows:
        while row:
            pivot=row.bit_length()-1
            if pivot in basis:row^=basis[pivot]
            else:basis[pivot]=row;break
    kernels=[]
    for j in sorted(set(range(n))-set(basis)):
        v=1<<j
        for k,row in sorted(basis.items()):
            if (v&row).bit_count()%2:v^=1<<k
        require(all((v&row).bit_count()%2==0 for row in rows),'kernel relation')
        kernels.append(v)
    return len(basis),kernels

def action(a,power=1):
    for _ in range(power%4):
        a=(2 if a&1 else 0)^(4 if a&2 else 0)^(7 if a&4 else 0)
    return a

def cohomology():
    keys=list(itertools.product(range(1,4),repeat=2));index={k:3*i for i,k in enumerate(keys)}
    def value(c,g,h):return (c>>index[g,h])&7 if g and h else 0
    def delta(c,g,h,k):return action(value(c,h,k),g)^value(c,(g+h)%4,k)^value(c,g,(h+k)%4)^value(c,g,h)
    equations=[]
    for g,h,k in itertools.product(range(4),repeat=3):
        vals=[delta(1<<j,g,h,k) for j in range(27)]
        for bit in range(3):equations.append(sum(1<<j for j,v in enumerate(vals) if v>>bit&1))
    rank,Zbasis=rref(equations,27);require(len(Zbasis)==7,'Z2 dimension seven')
    def coboundary(b,g,h):
        f=lambda a:(b>>(3*(a-1)))&7 if a else 0
        return action(f(h),g)^f((g+h)%4)^f(g)
    Bbasis=[sum(coboundary(1<<j,g,h)<<index[g,h] for g,h in keys) for j in range(9)]
    Brank,_=rref(Bbasis,27);require(Brank==6,'B2 dimension six')
    norm2=lambda a:action(a,2)^a
    imnorm={norm2(a)for a in range(8)};restrictions=[]
    require(len(imnorm)==2,'subgroup norm image')
    for mask in range(1<<len(Zbasis)):
        c=0
        for j,v in enumerate(Zbasis):
            if mask>>j&1:c^=v
        require(all(delta(c,g,h,k)==0 for g,h,k in itertools.product(range(4),repeat=3)),'full normalized cocycle equations')
        v=value(c,2,2);require(v in imnorm,'restriction is a coboundary')
        b=next(a for a in range(8) if norm2(a)==v)
        require(all(value(c,g,h)==((action(b,g)^b) if g==h==2 else 0) for g,h in itertools.product((0,2),repeat=2)),'all restricted cochain coefficients')
        if mask and mask&(mask-1)==0:restrictions.append(dict(cocycle=c,restriction_value=v,cobounding_one_cochain=b))
    permutations=list(itertools.permutations(range(4)))
    mul=lambda a,b:tuple(a[b[i]]for i in range(4))
    identity=tuple(range(4));S3=[p for p in permutations if p[0]==0]
    cycles=[p for p in permutations if mul(p,p)!=identity and mul(mul(p,p),mul(p,p))==identity]
    require(len(cycles)==6,'six four-cycles')
    t=cycles[0];orbit={mul(mul(p,t),tuple(p.index(i)for i in range(4)))for p in S3}
    require(orbit==set(cycles),'one four-cycle conjugacy orbit under regular stabilizer')
    return dict(status='PASS',coefficient_action_columns=[2,4,7],normalized_two_cochain_dimension=27,Z2_dimension=7,B2_dimension=6,H2_dimension=1,cocycles_checked=128,restricted_classes='all zero',basis_restriction_witnesses=restrictions,four_cycles=6,regular_stabilizer_conjugacy_orbits=1)

def source_facts(R):
    n=len(R);du=dual(R);G=[i for i in range(n)if sum(R[i][du[i]])==1]
    require(len(G)==4 and all(R[g][g]==[1]+[0]*(n-1) for g in G),'invertible group V4')
    dims=[1 if i in G else 2 for i in range(n)]
    require(all(sum(R[i][j][k]*dims[k]for k in range(n))==dims[i]*dims[j]for i,j in itertools.product(range(n),repeat=2)),'exact positive dimension homomorphism')
    D={0}|{k for i in range(n)for k in range(n)if R[i][du[i]][k]}
    while True:
        E=D|{k for i in D for j in D for k in range(n)if R[i][j][k]}
        if D==E:break
        D=E
    require(len(D)==5 and set(G)<D,'adjoint rank five')
    m=next(iter(D-set(G)))
    require(du[m]==m and R[m][m]==[int(i in G)for i in range(n)],'TY square')
    require(all(R[g][m][m]==R[m][g][m]==1 for g in G),'TY action')
    components=[];seen=set()
    for i in range(n):
        if i in seen:continue
        C=sorted({k for a in D for k in range(n)if R[a][i][k]});seen.update(C);components.append(C)
    require(sorted(map(len,components))==[2,2,2,5] and len(seen)==n,'universal components')
    component_of={i:k for k,C in enumerate(components)for i in C}
    product=[]
    for C in components:
        row=[]
        for E in components:
            degrees={component_of[k] for i in C for j in E for k in range(n)if R[i][j][k]}
            require(len(degrees)==1,'full homogeneous product');row.append(next(iter(degrees)))
        product.append(row)
    generators=[a for a in range(1,4)if product[a][a]!=0]
    require(len(generators)==2,'C4 generators');a=generators[0];b=product[a][a]
    require(product[b][b]==0 and product[a][b]not in(0,a,b),'C4 group')
    x=components[a][0];L=[g for g in G if R[g][x][x]];Rt=[g for g in G if R[x][g][x]]
    require(len(L)==len(Rt)==2 and L!=Rt,'distinct left and right lines')
    require(R[x][du[x]]==[int(i in L)+int(i==m)for i in range(n)],'left internal end')
    require(R[du[x]][x]==[int(i in Rt)+int(i==m)for i in range(n)],'right internal end')
    return dict(invertibles=G,neutral=sorted(D),neutral_noninvertible=m,components=components,grading_product=product,degree1=a,degree2=b,object=x,left_stabilizer=L,right_stabilizer=Rt,degree2_duality=[du[i]for i in components[b]],degree2_selfdual=all(du[i]==i for i in components[b]))

def main():
    inputs={r['id']:r for r in load()};records=[]
    for no in (104,153):
        r=inputs[f'R11_1_{no}'];facts=source_facts(r['tensor']);records.append(dict(id=r['id'],tensor_sha256=r['tensor_sha256'],**facts))
    require(records[0]['degree2_selfdual'] and not records[1]['degree2_selfdual'],'distinct even fusion rings')
    report=dict(status='PASS',cohomology=cohomology(),records=records)
    (OUT/'c4_neutral_cohomology_replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS all128 normalized two-cocycles restrict trivially; exact source104/153 neutral and even-part hypotheses')

if __name__=='__main__':main()
