import sys,time,sympy as s,json
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'supplements/rank6/software'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4982_module import all_modules
from full_morita_gram import full_gram,image_candidates
M=all_modules()[0];G=full_gram(M);V=s.Matrix.hstack(*G.columnspace());print('rank',V.cols,'diag',sorted(set(G[i,i] for i in range(169))),flush=True)
for a,b in [(0,0),(0,1),(4,4),(4,5),(4,7),(4,10)]:
 c=[int(i==a) for i in range(13)];r=[int(i==b) for i in range(13)];t=time.monotonic()
 try:cs=image_candidates(G,V,c,r,10000000);print(a,b,'n',len(cs),'seconds',time.monotonic()-t,flush=True)
 except Exception as e:print(a,b,str(e),flush=True)
