"""The E4(G2) module category from G2,4 inside Spin(14),1.

The conformal embedding and the published annular/branching data are the
categorical inputs.  Weyl-character fusion, annular compatibility, the cyclic
local subgroup, and all 216 output coefficients are reconstructed exactly.
No census tensor is an input to this constructor.
"""
import json
from pathlib import Path
from functools import lru_cache
import sympy as s
from exact import require
from quantum_rank2 import principal
from oriented_signed import validate_general

REFERENCE='Coquereaux--Rais--Tahri, Exceptional quantum subgroups for B2 and G2, arXiv:1001.5416v1, Section 4.5, pp. 29--32; G2,4 conformally embedded in Spin(14),1.'
# Source ordering (unit,X,Y,h,g,g^{-1}); the four local simples form C4.
F01=[[0,1,0,0,0,0],[1,2,2,1,0,0],[0,2,2,0,1,1],
     [0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,1,0,0,0]]
E0=[[1,0,0,0,0,0],[0,1,0,0,0,0],[0,1,1,0,0,0],
    [0,0,1,1,0,0],[1,1,1,0,0,0],[0,1,1,0,1,1],
    [0,1,0,1,0,0],[0,1,1,0,0,0],[0,0,1,0,0,0]]
# The paper puts the long fundamental weight first.
SOURCE_WEIGHTS=[(0,0),(0,1),(0,2),(1,0),(0,3),(1,1),(0,4),(1,2),(2,0)]

@lru_cache(None)
def construct():
    n=6;X=s.Matrix(F01);image=[4,2,1,5,3,0]
    g=s.Matrix([[int(k==image[j]) for k in range(n)] for j in range(n)])
    require(g**4==s.eye(n) and g**2!=s.eye(n),'local group is not cyclic of order four')
    require(g*X==X*g,'central free-module generator fails to commute')
    matrices=[s.eye(n),X,g*X,g**2,g,g**3]
    R=[[[int(x) for x in row] for row in M.tolist()] for M in matrices]
    validate_general(R)
    require([next(j for j in range(n) if R[i][j][0]) for i in range(n)]==[0,1,2,3,5,4],'incorrect source duality')
    N,weights,conductor=principal('G2',4)
    permutation=[weights.index((b,a)) for a,b in SOURCE_WEIGHTS]
    E=s.Matrix(E0)
    NN=[s.Matrix([[N[i][j][k] for k in permutation] for j in permutation]) for i in permutation]
    annular=[sum((E[i,j]*matrices[j] for j in range(n)),s.zeros(n)) for i in range(9)]
    require(annular[1]==X,'basic annular matrix differs from source')
    for i in range(9):require(NN[i]*E==E*annular[i],'Weyl fusion and published branching are incompatible')
    # Free-module adjunction: Gram matrix determined by A=1+(0,3).
    require(E*E.T==s.eye(9)+NN[4],'branching Gram matrix does not reconstruct the vacuum algebra')
    # Local branch rows: unit, vector, spinor, conjugate spinor.
    local=[list(E[:,j]) for j in (0,3,4,5)]
    require(local[0]==[1,0,0,0,1,0,0,0,0] and local[1]==[0,0,0,1,0,0,1,0,0],'wrong vacuum or vector branching')
    require(local[2]==local[3]==[0,0,0,0,0,1,0,0,0],'wrong spinor branching')
    return R,{'conductor':conductor,'source_weights':[list(w) for w in SOURCE_WEIGHTS],
              'annular_generator':F01,'branching':E0,'local_generator_permutation':image,
              'module_duality':[0,1,2,3,5,4],'structure_constants':216,
              'weyl_intertwiner_equations':9*9*6}

def examples():
    R,aux=construct()
    yield ('E4(G2): modules for G2 level 4 in Spin(14) level 1',R,REFERENCE,{k:'yes' for k in ('general','pivotal','spherical','pseudo_unitary','unitary')})

if __name__=='__main__':
    import time
    from prepare import key
    P=Path(__file__).resolve().parents[1];st=time.monotonic();R,aux=construct()
    rows=json.load(open(P/'data/census.json'));hits=[r['id'] for r in rows if key(r['N'])==key(R)]
    print('G2 E4 exact matches',hits,'seconds',time.monotonic()-st,flush=True)
    print(json.dumps(aux),flush=True)
