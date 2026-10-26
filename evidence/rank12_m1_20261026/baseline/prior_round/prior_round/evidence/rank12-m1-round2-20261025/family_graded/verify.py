"""Exact D40 classification and model replay. No discovery solver or network.
The classification of categorical extensions is the theoretical premise in
 d40_classification.md; all finite exhaustions below are complete.
"""
from pathlib import Path
import collections,itertools,json,sys,time
import sympy as s
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parents[1]/'rank12-m1-offline-20261025'
sys.path[:0]=[str(BASE),str(BASE/'sources/work/rank11'),str(BASE/'sources/work/models')]
from group_models import common
from match_models import ty,rep_dihedral
from twisted_c2_models import construct as pointed_dual
from feudal_dual import construct as feudal_dual
from grading_cocycles import representatives
need=common.require
DATA=json.loads((BASE/'tensors.json').read_text())
TARGETS=[f'R12_1_{i}'for i in [156,263,309,383,449,467,470,501,514]]
POS=[f'R12_1_{i}'for i in [156,263,449]]
NEG=[f'R12_1_{i}'for i in [309,383,467,470,501,514]]

def iso(A,B):
 p=common.based_iso(A,B);return p

def dimension_character(R):
 # Determine exact dimension1/2/sqrt5 from the baseline exact family ledger.
 rows={r['id']:r for r in json.loads((BASE/'unresolved_families.json').read_text())['records']}
 rid=next(rid for rid in TARGETS if DATA[rid]==R);v=rows[rid]['dimensions_in_field'];ds=[(int(x[0]),0)if len(x)==1 else(int(x[1]),int(x[0]))for x in v]
 def add(a,b):return(a[0]+b[0],a[1]+b[1])
 def mul(a,b):return(a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
 need(ds[0]==(1,0)and collections.Counter(ds)=={(1,0):4,(2,0):4,(0,1):4},'exact dimension multiset')
 for a,b in itertools.product(range(12),repeat=2):
  total=(0,0)
  for k in range(12):total=add(total,(R[a][b][k]*ds[k][0],R[a][b][k]*ds[k][1]))
  need(total==mul(ds[a],ds[b]),'exact positive dimension character')
 return ds

def source_conditions(R):
 ds=dimension_character(R);du=common.dual(R);G=[i for i,d in enumerate(ds)if d==(1,0)];Y=[i for i,d in enumerate(ds)if d==(2,0)];X=[i for i,d in enumerate(ds)if d==(0,1)];B={0}
 for a in range(12):B|={k for k,v in enumerate(R[a][du[a]])if v}
 while True:
  C=B|{k for a,b in itertools.product(B,repeat=2)for k,v in enumerate(R[a][b])if v}
  if C==B:break
  B=C
 B=sorted(B);BT=[[[R[a][b][c]for c in B]for b in B]for a in B];need(len(B)==4 and iso(BT,rep_dihedral(5))is not None,'adjoint odd-dihedral rank4 subring')
 g=next(a for a in B if a and a in G);need(R[g][g][0]==1 and sum(R[g][g])==1,'involution')
 need(all(R[g][a]==R[a][g]for a in range(12)),'centrality in the entire ring')
 need(all(R[g][a][a]==1 for a in Y),'fixed dimension-two objects')
 need(all([h for h in G if R[h][a][a]]==[0,g]for a in Y),'common stabilizer exactly C2')
 need(all(R[g][a][a]==0 for a in X),'free irrational-object action')
 need(len({tuple(sorted({a,R[g][a].index(1)}))for a in X})==2,'two free double orbits')
 E=sorted(G+Y);h=next(a for a in G if a not in B)
 need(set(E)==set(B)|{R[h][a].index(1)for a in B},'integral crossed extension by an actual invertible')
 need(R[R[h][g].index(1)][du[h]][g]==1,'h normalizes g')
 ET=[[[R[a][b][c]for c in E]for b in E]for a in E]
 rid=next(rid for rid in TARGETS if DATA[rid]==R)
 iscomm=all(ET[a][b]==ET[b][a]for a,b in itertools.product(range(8),repeat=2))
 need(iscomm==(rid=='R12_1_449'),'dihedral alternative commutativity premise')
 return dict(adjoint_subring=B,integral_subring=E,involution=g,extension_invertible=h,integral_tensor=ET)

def c4_equivariant():
 A=ty((5,));sigma=[0,4,3,2,1,5];parity=[0]*5+[1]
 need(all((sigma[a]*sigma[b]-a*b)%5==0 for a,b in itertools.product(range(5),repeat=2)),'orthogonal TY inversion')
 need(all((int(a==5)+int(b==5)-int(c==5))%2==0 for a,b,c in itertools.product(range(6),repeat=3)if A[a][b][c]),'monoidal parity natural automorphism')
 for a,b,c in itertools.product(range(4),repeat=3):need(((a+b)//4+((a+b)%4+c)//4-(b+c)//4-(a+(b+c)%4)//4)%2==0,'C4 action coherence')
 labs=[];seen=set()
 for a in range(6):
  if a in seen:continue
  O=[a]if sigma[a]==a else[a,sigma[a]];seen.update(O)
  for j in range(4//len(O)):labs.append((O,j))
 K=s.QQ.cyclotomic_field(8);z=K.unit;T=[[[0]*12 for _ in range(12)]for _ in range(12)]
 powers=[list(range(6))]
 for _ in range(1,4):powers.append([sigma[powers[-1][a]]for a in range(6)])
 for i,(U,j)in enumerate(labs):
  for k,(V,l)in enumerate(labs):
   for m,(W,t)in enumerate(labs):
    v=K.zero
    for a in range(0,4,len(W)):
     tr=sum(A[x][y][W[0]]for x in U for y in V if powers[a][x]==x and powers[a][y]==y)
     v+=tr*z**(((2*(j+l-t)+parity[U[0]]+parity[V[0]]-parity[W[0]])*a)%8)
    v/=K(4//len(W));co=v.to_list();need(len(co)<=1 and(not co or co[0].denominator==1 and co[0]>=0),'exact C4 projective Fourier projection');T[i][k][m]=int(co[0])if co else 0
 common.validate(T);bm=iso(DATA['R12_1_449'],T);need(bm is not None,'all1728 C4 model coefficients')
 return T,bm,labs

def main():
 start=time.monotonic();conditions={rid:source_conditions(DATA[rid])for rid in TARGETS};counter=collections.Counter()
 # Recompute all six possible integral parts from actual group-theoretical categories.
 group_models=[]
 for source in json.loads((ROOT/'feudal40_models_sparse.json').read_text()):
  name=source['parameters']['group']
  if any(z['group']==name for z in group_models):continue
  R=source['tensor'];G=[[R[a][b].index(1)for b in range(20)]for a in range(20)];Q=[[(a+b)%4 if name=='F20'else a^b for b in range(4)]for a in range(4)];c=10 if name=='F20'else 5
  pars=([dict(cyclic_class=k)for k in[0,2]]if name=='F20'else[dict(trilinear_coefficients=[0,b,c])for b,c in itertools.product(range(2),repeat=2)])
  for par in pars:
   if name=='F20':wq=lambda a,b,c:par['cyclic_class']*a*((b+c)//4)%4
   else:
    terms=[(0,0,0),(1,1,1),(0,1,1)];bits=par['trilinear_coefficients'];coords=lambda a:(a&1,a>>1);wq=lambda a,b,c:2*(sum(v*coords(a)[i]*coords(b)[j]*coords(c)[k]for v,(i,j,k)in zip(bits,terms))%2)
   need(all((wq(b,c,d)+wq(a,Q[b][c],d)+wq(a,b,c)-wq(Q[a][b],c,d)-wq(a,b,Q[c][d]))%4==0 for a,b,c,d in itertools.product(range(4),repeat=4)),'integral part quotient cocycle')
   need(all(G[a][b]//5==Q[a//5][b//5]for a,b in itertools.product(range(20),repeat=2)),'quotient homomorphism')
   T,info=pointed_dual(G,c,lambda a,b,c:wq(a//5,b//5,c//5),expected_rank=8);need(T is not None,'complete rank8 group-theoretical integral model')
   hits=[rid for rid,z in conditions.items()if iso(z['integral_tensor'],T)is not None];group_models.append(dict(group=name,parameters=par,matches=hits))
 need(len(group_models)==6,'all six integral models')
 for rid in TARGETS:
  possibilities=[z for z in group_models if rid in z['matches']];need(bool(possibilities),'at least one possible pointed group')
  need({z['group']for z in possibilities}==({'D10xC2'}if rid=='R12_1_449'else{'F20'}),'forced pointed precursor group')
 counter['source_structural_checks']=9;counter['integral_cocycle_models']=6
 source=next(r for r in json.loads((ROOT/'feudal40_models_sparse.json').read_text())if r['parameters']['group']=='F20');R=source['tensor'];cert=source['certificate'];need(source['parameters']==dict(group='F20',sigma=[0,3,2,1],p=0),'correct universalD8 precursor')
 # Independent exact accepted-Liptrap identity and Fourier unitarity replay.
 import verify as baseline_verify
 baseline_verify.liptrap_positive(R,cert);counter['Liptrap_positive']=1
 package=json.loads((ROOT/'d8_cocycles.json').read_text());U=package['group_table'];reps,cohom=representatives(U,2);need(reps==package['representatives']and cohom['representative_count']==16,'complete relative mu4 cohomology list')
 degree=[a//5 for a in range(20)]+list(range(4,8));need(all(degree[k]==U[degree[a]][degree[b]]for a,b,k in itertools.product(range(24),repeat=3)if R[a][b][k]),'full faithful D8 grading')
 coverage=[]
 for i,omega in enumerate(reps):
  twist=dict(grading_group_table=U,grading=degree,cocycle=omega,modulus=4);N,info=feudal_dual(R,cert,10,twist=twist);need(N is not None,'rank12 Morita dual for each relative twist');hits=[]
  for rid in TARGETS:
   bm=iso(DATA[rid],N)
   if bm is not None:hits.append(rid)
  need(len(hits)==1 and hits[0]in POS[:2],'every possible inverse-Morita ring identified positively')
  coverage.append(dict(cocycle_index=i,result=hits[0],model_tensor_sha256=common.sha(N)))
 counter['relative_grading_cocycles']=16;counter['complete_Morita_tensors']=16
 T,bm,labs=c4_equivariant();counter['C4_TY_model']=1
 out=dict(status='PASS',modeled=POS,excluded=NEG,checks=dict(counter),relative_twist_coverage=coverage,optimized_python=not __debug__,elapsed_seconds=time.monotonic()-start,theoretical_scope='arbitrary complex categorification; categorical exhaustion proof in d40_classification.md')
 (ROOT/('verification_optimized.json'if not __debug__ else'verification.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
