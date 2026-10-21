"""Exact premises of the Rep(A5) module-rank obstruction for R8_3_307.

The categorical argument is in r307_module_review.md. This checks its finite
source, linear-algebra and double-coset premises, also under Python -O.
"""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from finite_group_exact import *
RID='R8_3_307'
SHA='8c1cad1664a341585edcd1b998161fb8b47264e8ba90d6db78cf94159b8bd0cc'
KIND='rep_a5_module_rank'

def certificate(R):
    require(digest(R)==SHA,'source tensor hash')
    d=[(1,0),(0,1),(0,1),(0,2),(5,0),(3,0),(3,0),(4,0)]
    require(quadratic_dimensions(R,d,10)==120,'total dimension')
    neutral=[0,4,5,6,7];odd=[1,2,3];grading(R,neutral,odd)
    require(sum(d[i][0]**2 for i in neutral)==60,'neutral dimension')
    subrings=closed_subsets(R,neutral);require(subrings==[[0],neutral],'neutral categorical simplicity')
    v=[1,1,2];equations=[]
    for i in neutral:
        for a,j in enumerate(odd):
            row=[R[i][j][k]-d[i][0]*int(a==b) for b,k in enumerate(odd)]
            require(sum(x*y for x,y in zip(row,v))==0,'module dimension eigenvector')
            equations.append(row)
    rank=matrix_rank(equations);require(rank==2,'unique positive module dimension ratio')
    scales=[a for a in range(1,4) if 60%(6*a*a)==0];require(scales==[1],'projective degree normalization')
    G=alternating();require(len(G)==60,'A5 order')
    H=generated([(1,2,0,3,4),(1,0,2,4,3)])
    require(H<=G and len(H)==6 and len(classes(H))==3,'S3 subgroup')
    allH={frozenset(conjugate(g,h) for h in H) for g in G};require(len(allH)==10,'S3 conjugacy orbit')
    # Every subgroup of order six has an order-three Sylow subgroup and lies
    # in its order-six normalizer. Enumerate all such normalizers exactly.
    C3={frozenset(generated([g])) for g in G if len(generated([g]))==3}
    normalizers={frozenset(g for g in G if {conjugate(g,h) for h in A}==set(A)) for A in C3}
    require(normalizers==allH,'all possible subgroup embeddings covered')
    todo=set(G);double=[]
    while todo:
        g=min(todo);D={compose(compose(a,g),b) for a in H for b in H}
        require(D<=todo,'double-coset partition');todo-=D
        J=H & {conjugate(g,h) for h in H}
        double.append({'size':len(D),'stabilizer_order':len(J),'irreducibles':len(classes(J))})
    double=sorted(double,key=lambda x:x['size'])
    require(double==[{'size':6,'stabilizer_order':6,'irreducibles':3},{'size':18,'stabilizer_order':2,'irreducibles':2},{'size':36,'stabilizer_order':1,'irreducibles':1}],'dual rank calculation')
    require(sum(x['irreducibles'] for x in double)==6!=len(neutral),'module dual rank contradiction')
    return {'kind':KIND,'id':RID,'tensor_sha256':SHA,'neutral_basis':neutral,'odd_basis':odd,
            'neutral_dimension':60,'neutral_closed_subrings':subrings,'module_dimension_ratio':v,
            'eigenvector_equation_rank':rank,'possible_integer_scales':scales,'double_cosets':double,
            'dual_rank':6,'required_dual_rank':5}

def verify(R,c):
    require(c==certificate(R),'module-rank certificate replay differs');return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
    R=source(RID,SHA);c=certificate(R)
    record={'id':RID,'tensor_sha256':SHA,'scope':'general_complex_fusion_category','status':'excluded','certificate':c}
    path=Path(__file__).with_suffix('.json')
    if a.write:path.write_text(json.dumps(record,indent=2)+'\n')
    else:verify(R,json.loads(path.read_text())['certificate'])
    print(json.dumps({'status':'PASS','id':RID,'scope':record['scope'],'certificate':c},indent=2))
if __name__=='__main__':main()
