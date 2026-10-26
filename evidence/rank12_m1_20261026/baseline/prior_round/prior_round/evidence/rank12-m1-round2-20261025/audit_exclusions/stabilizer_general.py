"""Two possibly different stabilizer algebras; squared internal-End argument."""
from pathlib import Path
from itertools import product
from collections import Counter
import json,math,time
import sympy as s
from stabilizer_square import BASE,HERE,perron_factor,require,t

def scan(R):
    n=len(R);du=[next(j for j in range(n)if R[i][j][0])for i in range(n)];G=[i for i in range(n)if sum(R[i][du[i]])==1]
    unit=lambda x:[int(i==x)for i in range(n)]
    left=[sum(1<<i for i,g in enumerate(G)if R[g][x]==unit(x))for x in range(n)]
    right=[sum(1<<i for i,g in enumerate(G)if R[x][g]==unit(x))for x in range(n)]
    cache={}
    for x,y,z in product(range(n),repeat=3):
        m=R[x][y][z]
        if not m:continue
        bits=left[x]&right[y]&left[z]&right[z];h=bits.bit_count()
        if h<2:continue
        q=h//math.gcd(h,m)
        if q==1:continue
        if z not in cache:cache[z]=perron_factor(R,z)
        f=cache[z];p=s.Poly(f.as_expr().subs(t,q*t)/q**f.degree(),t)
        if any(a.q!=1 for a in p.all_coeffs()):
            H=[g for i,g in enumerate(G)if bits>>i&1]
            require(all(R[g][k].index(1)in H for g,k in product(H,repeat=2)),'actual subgroup')
            return dict(kind='general_subgroup_isotypic_integrality',X=x,Y=y,Z=z,multiplicity=m,H=H,stabilizer_order=h,
                        dimension_polynomial=list(map(str,f.all_coeffs())),normalized_dimension_polynomial=list(map(str,p.all_coeffs())),
                        scope='general_complex_fusion_category',argument='two stabilizer algebras; squared internal End; integrality transitivity')
    return None

if __name__=='__main__':
    start=time.monotonic();data=json.loads((BASE/'tensors.json').read_text());status={r['id']:r['status']for r in json.loads((BASE/'ledger.json').read_text())['records']};out=[]
    for rid,R in data.items():
        c=scan(R)
        if c:out.append(dict(id=rid,first_round_status=status[rid],certificate=c))
    result=dict(status='PASS',records=out,counts=dict(Counter(r['first_round_status']for r in out)),elapsed_seconds=time.monotonic()-start)
    require(not any(r['first_round_status']=='unitarily_realized'for r in out),'positive-model control')
    (HERE/'stabilizer_general.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['counts']);print('NEW',[r['id']for r in out if r['first_round_status']=='unresolved']);print('seconds',result['elapsed_seconds'])
