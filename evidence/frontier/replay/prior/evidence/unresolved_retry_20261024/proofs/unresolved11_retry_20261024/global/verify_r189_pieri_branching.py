"""Exact independent Pieri/branching verification of the R189 model argument."""
import itertools,json
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent

def require(x,msg):
    if not x: raise ValueError(msg)

def to_partition(w):
    a,b,c=w
    return (a+b+c,b+c,c,0)

def from_partition(p):
    return tuple(p[i]-p[i+1] for i in range(3))

def wedge_two(w):
    p=to_partition(w);out=Counter()
    for rows in itertools.combinations(range(4),2):
        q=tuple(p[i]+int(i in rows) for i in range(4))
        if any(q[i]<q[i+1] for i in range(3)):continue
        out[from_partition(q)]+=1
    return out

v=(0,1,0)
p2=wedge_two(v);p3=Counter()
for w,m in p2.items():
    for z,n in wedge_two(w).items():p3[z]+=m*n
require(p2==Counter({(0,0,0):1,(1,0,1):1,(0,2,0):1}),'v squared')
require(p3==Counter({(0,1,0):3,(1,1,1):2,(0,3,0):1,(2,0,0):1,(0,0,2):1}),'v cubed')
require(all(sum(w)<=6 for w in set(p2)|set(p3)),'inside level-six alcove')
branch_strings=[['000','060','202','222'],['200','212','042'],['012','230','303'],['030','103','321'],['400','121','024'],['600','006','220','022'],['004','121','420'],['030','301','123'],['210','032','303'],['002','212','240']]
branches=[[tuple(map(int,w)) for w in row] for row in branch_strings]
norms=[sum(p2[w] for w in row) for row in branches]
products=[sum(p3[w] for w in row) for row in branches]
require(norms==[1]+[0]*9,'beta simple and distinct C10 translates')
require(products==[0,1,0,1,0,0,0,1,0,1],'beta square large constituents')
out={'status':'PASS','scope':'Arithmetic support for actual conformal-embedding category; categorical existence uses cited sources.',
     'v2':{''.join(map(str,w)):m for w,m in sorted(p2.items())},'v3':{''.join(map(str,w)):m for w,m in sorted(p3.items())},
     'branching':branch_strings,'beta_translate_inner_products':norms,'beta_square_translate_multiplicities':products,
     'g_exponents_in_x_squared':sorted(((j-5)%10)//2 for j in [1,3,7,9])}
require(out['g_exponents_in_x_squared']==[1,2,3,4],'R189 ring relation')
(HERE/'r189_pieri_branching_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: exact Pieri rules, all branching intersections, and R189 relation')
