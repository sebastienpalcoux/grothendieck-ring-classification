from itertools import product
import json
from independent_audit import BASE,HERE,dual,require

if __name__=='__main__':
    data=json.loads((BASE/'tensors.json').read_text());profiles={r['id']:r for r in json.loads((BASE/'profile.json').read_text())['records']};out=[]
    for i in(156,263,309,383,449,467,470,501,514):
        rid=f'R12_1_{i}';R=data[rid];du=dual(R);sq=profiles[rid]['squared_dimensions'];require(sorted(sq)==[1]*4+[4]*4+[5]*4,'exact dimension pattern')
        ds=[(1,0)if q==1 else(2,0)if q==4 else(0,1)for q in sq]
        for a,b in product(range(12),repeat=2):
            x,y=ds[a];z,w=ds[b];require(tuple(sum(R[a][b][k]*ds[k][c]for k in range(12))for c in range(2))==(x*z+5*y*w,x*w+y*z),'exact positive Qsqrt5 character')
        G=[a for a in range(12)if sq[a]==1];T=[a for a in range(12)if sq[a]==4];M=[a for a in range(12)if sq[a]==5];I=G+T
        require(all(du[a]in I for a in I)and all(not R[a][b][k]for a,b in product(I,repeat=2)for k in M),'actual integral subcategory')
        unit=lambda a:[int(a==b)for b in range(12)]
        gs=[g for g in G if g and R[g][g][0]and all(R[g][a]==R[a][g]==unit(a)for a in T)];require(len(gs)==1,'unique common order-two stabilizer');g=gs[0]
        require(all(R[g][a]==R[a][g]for a in range(12)),'central based action')
        require(all(R[g][a]!=unit(a)for a in M),'free sqrt5 action')
        require(all([h for h in G if R[h][a]==unit(a)]==[0,g]for a in T),'every integral noninvertible has exact common stabilizer')
        comm=all(R[a][b]==R[b][a]for a,b in product(I,repeat=2));require(comm==(i==449),'all eight noncommutative cases have noncommutative integral subring')
        out.append(dict(id=rid,integral_subset=I,central_involution=g,integral_subring_commutative=comm,precursor_pointedness_hypotheses=True))
    result=dict(status='PASS',records=out)
    (HERE/'d40_sources_independent.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS nineD40sourcehypotheses')
