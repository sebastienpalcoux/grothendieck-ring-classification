if not __debug__:
 raise RuntimeError("This exact certificate requires Python assertions; disable optimization.")
import sys,time,json,itertools,collections,numpy as np,sympy as s,networkx as nx
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'supplements/rank6/software'));sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4982_module import all_modules
from full_morita_gram import full_gram
from networkx.algorithms.isomorphism import GraphMatcher,categorical_edge_match,categorical_node_match
M=all_modules()[0];G=full_gram(M);r=13;graph=nx.Graph()
for a in range(r):graph.add_node(a,label=(int(a>=4),tuple(int(X[a,a]) for X in M)))
for a in range(r):
 for b in range(a+1,r):graph.add_edge(a,b,label=tuple(int(X[a,b]) for X in M))
auts=list(GraphMatcher(graph,graph,node_match=categorical_node_match('label',None),edge_match=categorical_edge_match('label',None)).isomorphisms_iter());ps=[]
for p in auts:
 A=np.zeros((r,r),dtype=int)
 for a in range(r):A[p[a],a]=1
 assert all(s.Matrix(A)*X==X*s.Matrix(A) for X in M)
 ps.append(A)
stab=[A for A in ps if A[0,0]];noninv=set()
for a in [4,7,10]:
 B=np.array([list(map(int,z.split())) for z in (Path(__file__).parent/f'rightaction_{a}.out').read_text().splitlines()]);assert B.shape==(1,169);B=B.reshape(13,13)
 assert all(s.Matrix(B)*X==X*s.Matrix(B) for X in M)
 for Q in stab:
  for S in stab:noninv.add(tuple((Q@B@S).flat))
print('noninv',len(noninv),'perm',len(ps),flush=True)
H=np.array(G,dtype=int)
for z in noninv:H-=np.outer(z,z)
print('Hmin',H.min(),'diag',sorted(set(H.diagonal())),'rank',s.Matrix(H).rank(),flush=True)
allowed=[]
for Q in ps:
 v=np.array(tuple(Q.flat));outer=np.outer(v,v)
 if np.all(outer<=H):allowed.append(tuple(v))
print('allowed perms',len(allowed),flush=True)
print('sumall matches',np.array_equal(sum((np.outer(z,z) for z in allowed),np.zeros((169,169),dtype=int)),H),flush=True)
report={'noninvertible_actions':[list(z) for z in sorted(noninv)],'invertible_actions':[list(z) for z in sorted(allowed)],'invertible_candidates':len(allowed),'gram_remainder_minimum':int(H.min())}
if len(allowed)==12 and np.array_equal(sum((np.outer(z,z) for z in allowed),np.zeros((169,169),dtype=int)),H):
 matrices=[np.array(z,dtype=int).reshape(13,13) for z in allowed+sorted(noninv)];ids={tuple(A.flat):i for i,A in enumerate(matrices)}
 print('closed group',all(tuple((A@B).flat) in ids for A in matrices[:12] for B in matrices[:12]),flush=True)
 # The representation is not faithful on the Grothendieck ring:39simples butmatrixspan37.
 print('matrixrank',s.Matrix.hstack(*(s.Matrix(list(A.flat)) for A in matrices)).rank(),flush=True)
report=json.loads(json.dumps(report,default=int));(Path(__file__).parent/'r4982_fullgram_actions.json').write_text(json.dumps(report)+'\n')
