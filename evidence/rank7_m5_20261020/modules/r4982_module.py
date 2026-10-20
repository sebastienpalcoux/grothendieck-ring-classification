"""Reconstruct all exact C3 right-module fusion matrices for R7_5_4982."""
if not __debug__:
 raise RuntimeError("This exact certificate requires Python assertions; disable optimization.")
import json,itertools,sys,sympy as s
from pathlib import Path
P=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(P/'evidence/rank7_m5_20261019/theory'))
from cyclic3_spectral import matmul,choices,conjugate,trace,norm
R=next(r['tensor'] for r in json.load(open(P/'supplements/rank7/output/m5/census.json')) if r['id']=='R7_5_4982')

def reconstruct(big):
 T=[]
 for i in range(7):
  A=[[(0,0)]*4 for k in range(4)]
  A[0][0]=(1 if i<3 else -1 if i==3 else 0,0)
  for a in range(3):
   for b in range(3):A[a+1][b+1]=tuple(map(int,big[i][a][b]))
  T.append(A)
 Ms=[]
 for i in range(7):
  M=s.zeros(13);M[0,0]=int(i<3)
  for a in range(4):
   for t in range(3):M[0,1+3*a+t]=M[1+3*a+t,0]=int(i==a+3)
  for a in range(4):
   for b in range(4):
    u,v=T[i][a][b];N=R[i][a+3][b+3];assert (N-u-v)%3==0
    c=(N-u-v)//3;ns=[u+c,v+c,c];assert min(ns)>=0
    for t in range(3):
     for z in range(3):M[1+3*a+t,1+3*b+z]=ns[(z-t)%3]
  Ms.append(M)
 assert Ms[0]==s.eye(13) and Ms[1]==Ms[2]==s.eye(13)
 for i in range(7):
  for j in range(7):assert Ms[i]*Ms[j]==sum((R[i][j][k]*Ms[k] for k in range(7)),s.zeros(13))
 return Ms

def all_modules():
 raw=json.load(open(Path(__file__).with_name('r4982_fourier_certificate.json')))['full_representations']
 return [reconstruct(t) for t in raw]

if __name__=='__main__':
 import networkx as nx
 from networkx.algorithms.isomorphism import GraphMatcher,categorical_edge_match,categorical_node_match
 def graph(Ms):
  G=nx.Graph()
  for a in range(13):G.add_node(a,label=(int(a>=4),tuple(int(M[a,a]) for M in Ms)))
  for a in range(13):
   for b in range(a+1,13):G.add_edge(a,b,label=tuple(int(M[a,b]) for M in Ms))
  return G
 representatives=[];out=[]; first=all_modules()[0]
 for i,Ms in enumerate(all_modules()):
  G=graph(Ms);em=categorical_edge_match('label',None);nm=categorical_node_match('label',None)
  matches=[j for j,H in enumerate(representatives) if GraphMatcher(G,H,node_match=nm,edge_match=em).is_isomorphic()]
  if not matches:
   representatives.append(G);auts=list(GraphMatcher(G,G,node_match=nm,edge_match=em).isomorphisms_iter())
   print('new graph',i,'automorphisms',len(auts),'images of0',sorted(set(p[0] for p in auts)),flush=True)
  else:print('same graph',i,'as',matches[0],flush=True)
  witness=next(GraphMatcher(G,representatives[0],node_match=nm,edge_match=em).isomorphisms_iter())
  p=[witness[a] for a in range(13)]; assert p[0]==0
  assert all(Ms[k][a,b]==first[k][p[a],p[b]] for k in range(7) for a in range(13) for b in range(13))
  out.append({'index':i,'isomorphism_to_first':p,'matrices':[[list(map(int,row)) for row in M.tolist()] for M in Ms]})
 Path(__file__).with_name('r4982_module_matrices.json').write_text(json.dumps(out)+'\n')
