"""Exact rational conformal weights and complete finite-character plethysm."""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
def need(x,msg):
    if not x:raise ValueError(msg)
A=[[Q(3,4),Q(1,2),Q(1,4)],
   [Q(1,2),Q(1),Q(1,2)],
   [Q(1,4),Q(1,2),Q(3,4)]]
def h(w):
    return sum(w[i]*A[i][j]*(w[j]+2)
               for i in range(3) for j in range(3))/20
weights=[(0,0,0),(1,0,1),(0,2,0),(0,1,0),(1,1,1),(2,0,0),(0,0,2),(0,3,0)]
expected=[Q(0),Q(2,5),Q(3,5),Q(1,4),Q(3,4),Q(9,20),Q(9,20),Q(21,20)]
need([h(w) for w in weights]==expected,'conformal weights')
large=[Q(j*(10-j),20) for j in range(10)]
poss={w:[j for j,H in enumerate(large) if h(w)>=H and (h(w)-H).denominator==1] for w in weights}
need(poss==dict(zip(weights,[[0],[],[],[],[],[1,9],[1,9],[3,7]])), 'all nonnegative energy possibilities')

def schur_character(shape):
    cells=[(r,c) for r,n in enumerate(shape) for c in range(n)]
    out=Counter();table={};weight=[0]*4
    def rec(at):
        if at==len(cells):out[tuple(weight)]+=1;return
        r,c=cells[at]
        low=max(table.get((r,c-1),0),table.get((r-1,c),-1)+1)
        for v in range(low,4):
            table[r,c]=v;weight[v]+=1;rec(at+1);weight[v]-=1
        table.pop((r,c),None)
    rec(0)
    return out
sym2=[]
for i,j in combinations_with_replacement(range(4),2):
    v=[0]*4;v[i]+=1;v[j]+=1;sym2.append(v)
exterior=Counter(tuple(sum(sym2[a][i] for a in triple) for i in range(4))
                 for triple in combinations(range(10),3))
left=schur_character((4,1,1));right=schur_character((3,3))
need(sum(left.values())==70 and sum(right.values())==50, 'Schur dimensions')
need(exterior==left+right,'complete plethysm character equality')
receipt={'status':'PASS',
 'conformal_weights':{''.join(map(str,w)):str(h(w)) for w in weights},
 'SU10_level1_ground_weights':list(map(str,large)),
 'possible_branch_indices':{''.join(map(str,w)):v for w,v in poss.items()},
 'plethysm':'exterior^3(Sym^2 C4)=Schur_(4,1,1)(C4)+Schur_(3,3)(C4)',
 'Schur_dimensions':[70,50], 'exterior_cube_dimension':120,
 'complete_weight_characters_equal':True,
 'scope':'Exact finite inputs for the conformal-embedding model proof; existence supplied by the actual conformal embedding.'}
(HERE/'minimal_branching_certificate.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
