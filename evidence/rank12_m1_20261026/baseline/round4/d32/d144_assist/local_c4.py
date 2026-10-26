"""Exact neutral trivialization and local BrPic C4 uniqueness checks."""
from pathlib import Path
import itertools,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from liptrap_certificate import check,reconstruct
from ring_checks import require,validate

def mat(x):return [[x&1,(x>>1)&1],[(x>>2)&1,(x>>3)&1]]
def enc(A):return sum(A[i][j]<<(2*i+j) for i in range(2) for j in range(2))
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(2))%2 for j in range(2)]for i in range(2)]
def tr(A):return list(map(list,zip(*A)))
def det(A):return(A[0][0]*A[1][1]+A[0][1]*A[1][0])%2
def comp(a,b):return tuple(a[b[x]]for x in range(16))
def inv(a):return tuple(a.index(x)for x in range(16))
def order(a):
 b=a;n=1
 while b!=tuple(range(16)):b=comp(b,a);n+=1
 return n

def main():
 G2=[mat(x)for x in range(16)if det(mat(x))];G=set()
 for A,B,e in itertools.product(G2,G2,range(2)):
  G.add(tuple(enc(mm(mm(A,tr(mat(x))if e else mat(x)),tr(B)))for x in range(16)))
 require(len(G)==72,'orthogonal group size')
 L={0,1,2,3};P={g for g in G if {g[x]for x in L}==L}
 require(len(P)==12,'pointed parabolic size')
 Q={g for g in G if order(g)==4 and comp(g,g)in P and g not in P}
 require(len(Q)==6,'eligible order4 maps')
 g=min(Q);orbit={comp(comp(p,g),inv(p))for p in P};require(orbit==Q,'unique parabolic conjugacy class')
 fixed=[x for x in range(16)if g[x]==x];require(len(fixed)==2,'Jordan4: fixedspace dimension1')
 # The norm and (g-1) maps have ranks 1 and 3 respectively.
 norm={x^g[x]^comp(g,g)[x]^comp(comp(g,g),g)[x]for x in range(16)}
 diff={x^g[x]for x in range(16)}
 require(norm==set(fixed) and len(diff)==8,'C4 regular module and vanishing positive cohomology')
 p=HERE/'inputs';R=json.loads((p/'sylow_a10.json').read_text());cert=json.loads((p/'sylow_a10_test.json').read_text())['certificate'];validate(R);source=check(R,cert);F,mul,du=reconstruct(R,cert)
 for a,b,c in itertools.product(range(8),repeat=3):F(a,b,c,mul[mul[a,b],c])
 grades=[0,2,0,2,2,0,2,0,1,3,1,3]
 require(all((grades[a]+grades[b]-grades[c])%4==0 for a,b,c in itertools.product(range(12),repeat=3)if R[a][b][c]),'actual C4 grading')
 neutral=[0,2,5,7]
 def f(a,b):return 8 if (a,b)==(5,5) else 0
 for a,b,c in itertools.product(neutral,repeat=3):
  require((F(a,b,c,mul[mul[a,b],c])-f(b,c)-f(a,mul[b,c])+f(mul[a,b],c)+f(a,b))%16==0,'neutral VecV4 exact coboundary')
 # Degree2 represented by r=1 swaps two nontrivial neutral objects.
 conj=[mul[mul[1,x],du[1]]for x in neutral]
 require(conj==[0,2,7,5],'nontrivial square Brauer action')
 require(all(mul[mul[4,x],4]==x for x in range(8,12)),'local simultaneous s stabilizer fixes both objects')
 orbits=[{8,11},{9,10}]
 require(all({mul[4,x]for x in o}==o for o in orbits),'local H2 support orbits')
 require({du[x]for x in orbits[0]}==orbits[1],'local duality exchanges support orbits')
 out={'orthogonal_order':72,'parabolic_order':12,'eligible_C4_generators':6,'single_parabolic_conjugacy_class':True,'fixedspace_dimension':1,'norm_rank':1,'difference_rank':3,'H2_C4_natural_module':0,'source_hypotheses':source,'neutral':[0,2,5,7],'neutral_coboundary_modulus':16,'only_nonzero_cochain_entry':[5,5,8],'neutral_equations':64,'square_conjugation':conj,'C4_grading':grades,'local_H2_orbits':[sorted(o)for o in orbits],'local_duality':[du[x]for x in range(8,12)]}
 (HERE/'local_c4.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
