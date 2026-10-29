#!/usr/bin/env python3
"""Exact arithmetic for the new conditional theorem, not an existence test."""
from pathlib import Path
from itertools import product
from fractions import Fraction
import runpy,json,hashlib

HERE=Path(__file__).resolve().parent
PRIOR=HERE.parents[1]/'prior'

def need(ok,msg):
    if not ok:
        raise ValueError(msg)

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def closure(N,S):
    S=set(S)|{0}
    while True:
        T=S|{k for i in S for j in S for k,n in enumerate(N[i][j]) if n}
        if T==S:return sorted(S)
        S=T

def multiply(a,b,m):
    return ((a[0]*b[0]+a[1]*b[2])%m,
            (a[0]*b[1]+a[1]*b[3])%m,
            (a[2]*b[0]+a[3]*b[2])%m,
            (a[2]*b[1]+a[3]*b[3])%m)

source=PRIOR/'data/current_remaining_cases.py'
Ns=runpy.run_path(str(source))['TENSORS']
N=Ns['R6_8_1660']
tensor_sha=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
need(tensor_sha=='697ec27fe203356199bfcf674587be9c71455dbb681f2e086a076f726b03d267','source1660')
subrings=[]
for bits in product((0,1),repeat=5):
    S=[0]+[i+1 for i,x in enumerate(bits) if x]
    if closure(N,S)==S:subrings.append(S)
need(sorted(subrings,key=len)==[[0],[0,1],[0,1,4],list(range(6))],'subcategory lattice')
need(all(closure(N,[i])==list(range(6)) for i in (2,3,5)),'large simple generation')
H=[[sum(N[i][a][t]*N[i][t][b] for i in range(6) for t in range(6)) for b in range(6)] for a in range(6)]
spin=[0,0,2,2,1,3]
need(H[4]==[8*x for x in spin],'eight inherited spin columns exhaust entire sigma row')
need(N[2][2]==[1,0,3,3,0,4],'canonical augmentation object equals X² at ring level')

ind_path=PRIOR/'evidence/unresolved10_20261027/r6_1660/all_indicators_source.json'
ind=json.loads(ind_path.read_text())
retained=[x for x in ind['cases'] if x['cyclic_dimension_three_compatible']]
need(len(retained)==2,'two third-rotation branches')
need(sorted(x['third_rotation_multiplicities'] for x in retained)==[[2,0,1],[2,1,0]],'two cyclic multiplication directions')
need(N[2][2][2]==3,'three trivalent channels before cyclic cut')

# Signed permutation diagnostic: it yields no obstruction because congruence
# already makes T commute with its conjugate by S T^24 S^-1.
T=(1,1,0,1);S=(0,47,1,0);Si=(0,1,47,0);T24=(1,24,0,1)
g=multiply(multiply(S,T24,48),Si,48)
need(multiply(g,g,48)==(1,0,0,1),'involution')
gTg=multiply(multiply(g,T,48),g,48)
need(multiply(T,gTg,48)==multiply(gTg,T,48),'automatic commuting condition')

# Exact coefficient verification of W=(3-sqrt(3))*D in Q(sqrt2,sqrt3).
D=(144,96,80,56)
W=(3*D[0]-3*D[2],3*D[1]-3*D[3],3*D[2]-D[0],3*D[3]-D[1])
need(W==(192,120,96,72),'SU2 level22 dimension ratio')

r941path=PRIOR/'evidence/rank8_frontier_20261021/quartic_integer_center/source.json'
r941=next(x for x in json.loads(r941path.read_text())['records'] if x['id']=='R8_3_941')
ds=[[Fraction(x) for x in d] for d in r941['full_characters'][0]]
nonpointed=[ds[i] for i in range(8) if i not in (0,3)]
need(all(d[0]>=2 and all(x>0 for x in d[1:]) for d in nonpointed),'all R941 nonpointed source dimensions exceed2')
N941=r941['tensor']
du941=[next(j for j in range(8) if N941[i][j][0]) for i in range(8)]
cubic941=[N941[i][i][du941[i]] for i in range(8)]
need(du941==[0,2,1,3,4,5,6,7],'R941 dual pair at dimensionb')
need(cubic941==[1,1,1,0,1,1,3,3],'R941 cubic dimensions')
need([ds[4][j]+ds[1][j] for j in range(4)]==[4,3,2,2],'sqrt2*d=a+b')
# Columns 1,a,b,d have determinant -1 (unimodular coefficient comparison).
from itertools import permutations
mat=[[1,2,2,3],[0,1,2,2],[0,1,1,2],[0,1,1,1]]
det=0
for p in permutations(range(4)):
    sign=(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
    term=sign
    for i in range(4):term*=mat[i][p[i]]
    det+=term
need(abs(det)==1,'dimension basis independent')
d_spectra=[(3-j,j,0) for j in range(3)]
splits=[(a,b) for a in d_spectra for b in d_spectra if tuple(a[k]+b[k] for k in range(3))==(4,2,0)]
need(len(splits)==3,'three ordered/two unordered cubic assignments')

deps=[source,ind_path,r941path,
PRIOR/'evidence/unresolved7_20261027/r6_1660/SPIN_CONSTRAINTS.md',
PRIOR/'evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/rank6_pair/INTEGRAL_CENTER_CHECK.md']
receipt={
    'status':'PASS',
    'date':'2026-10-29',
    'classifications':{'R6_8_1660':'UNRESOLVED','R8_3_941':'UNRESOLVED'},
    'source1660_tensor_sha256':tensor_sha,
    'source1660_fusion_subrings':sorted(subrings,key=len),
    'source1660_sigma_Gram_row':H[4],
    'inherited_eight_spin_restrictions':spin,
    'cyclic_fixed_subspace_dimensions':[x['third_rotation_multiplicities'][0] for x in retained],
    'conditional_Morita_R941_cubic_dimensions':cubic941,
    'conditional_Morita_R941_d_pair_spectra':splits,
    'automatic_mod48_commutator':{'g':g,'gTg':gTg},
    'SU2_level22_full_condensation_required_algebra_dimension':'3-sqrt(3), strictly between1 and2',
    'inherited_proof_dependencies_sha256':{str(p.relative_to(PRIOR)):digest(p) for p in deps},
    'scope':'Checks source tensor, subring lattice, spin Gram exhaustion, exact third-rotation multiplicities and the automatic commutator only. The categorical theorem is in REPORT.md and inherits the previously proved center restrictions. Neither ring is resolved.'
}
(HERE/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: new theorem arithmetic, two cyclic multiplication directions; both rings UNRESOLVED')
