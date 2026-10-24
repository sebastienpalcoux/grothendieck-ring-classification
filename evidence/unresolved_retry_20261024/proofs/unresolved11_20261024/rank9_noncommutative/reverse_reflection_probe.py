from pathlib import Path
import json,itertools,sys,sympy as s
P=Path(__file__).resolve().parent;ROOT=P.parents[1]/'rank9_m2_research'
sys.path[:0]=[str(ROOT/'phase3'),str(ROOT/'work'),str(ROOT/'sources')]
import full_morita_gram as fg
D=json.load(open(ROOT/'phase5/quadratic_noncomm/1975_associator_inputs.json'));out=[]
for c in D['candidates'][1:]:
 N=c['N'];n=len(N)
 for g in [2,4]:
  orbits=[];done=set()
  for a in range(n):
   if a not in done:
    o=sorted({a}|{b for b in range(n)if N[a][g][b]});orbits.append(o);done.update(o)
  assert all(len(o)==2 for o in orbits)
  M=[s.Matrix(len(orbits),len(orbits),lambda j,k:sum(N[i][orbits[j][0]][b]for b in orbits[k]))for i in range(n)]
  assert all(M[j]*M[i]==sum((N[i][j][k]*M[k]for k in range(n)),s.zeros(len(orbits)))for i,j in itertools.product(range(n),repeat=2))
  G=fg.full_gram(M);V=s.Matrix.hstack(*G.columnspace());cols=fg.first_columns(M,g);unique=sorted(set(cols));allcs=[]
  for col in unique:
   cs=set()
   for row in unique:cs.update(fg.image_candidates(G,V,col,row,node_limit=10000000))
   for x in sorted(cs):
    B=s.Matrix(len(orbits),len(orbits),x)
    if all(B*m==m*B for m in M):allcs.append(x)
  print(c['alpha'],g,'orbits',orbits,'G rank',G.rank(),'dual rank',len(cols),'actions',len(allcs),flush=True)
  row={'alpha':c['alpha'],'g':g,'orbits':orbits,'G':G.tolist(),'first_columns':cols,'actions':allcs}
  out.append(row)
 (P/'reverse_reflection_probe.json').write_text(json.dumps(out,indent=2,default=int)+'\n')
