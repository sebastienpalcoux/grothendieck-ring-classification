if not __debug__:
 raise RuntimeError("This exact certificate requires Python assertions; disable optimization.")
import sys,sympy as s,math,json
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'supplements/rank6/software'));sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4982_module import all_modules
from full_morita_gram import full_gram
M=all_modules()[0];G=full_gram(M);V=s.Matrix.hstack(*G.columnspace());out=[]
for anchor in [4,7,10]:
 inds=list(range(0,169,13))+list(range(1,13))+[i*13+j for i in range(1,4) for j in range(1,4)];vals=[int(i==anchor) for i in range(13)]+[int(i==anchor) for i in range(1,13)]+[0]*9
 sol,pars=V.extract(inds,range(V.cols)).gauss_jordan_solve(s.Matrix(vals));ans=V*sol;v=ans.subs({p:0 for p in pars});W=ans.jacobian(pars);piv=list(W.T.rref()[1]);H=W*W.extract(piv,range(W.cols)).inv();b=v-H*v.extract(piv,[0]);den=int(s.ilcm(*(z.q for z in list(H)+list(b))));HH=H*den;bb=b*den;bounds=[math.isqrt(int(G[i,i])) for i in piv]
 A=[[int(z)%den for z in row]+[-int(bb[i])%den] for i,row in enumerate(HH.tolist())];rank=0;cols=[]
 for col in range(W.cols):
  ix=next((j for j in range(rank,len(A)) if A[j][col]),None)
  if ix is None:continue
  A[rank],A[ix]=A[ix],A[rank];f=pow(int(A[rank][col]),-1,int(den));A[rank]=[(x*f)%den for x in A[rank]]
  for j in range(len(A)):
   if j!=rank and A[j][col]:f=A[j][col];A[j]=[(x-f*y)%den for x,y in zip(A[j],A[rank])]
  cols.append(col);rank+=1
 free=[i for i in range(W.cols) if i not in cols];assert all(not any(row[:-1]) and row[-1]==0 for row in A[rank:]);print(anchor,'params',W.cols,'modrank',rank,'box',math.prod(bounds[i]+1 for i in free),flush=True)
 out.append({'anchor':anchor,'den':den,'variables':W.cols,'piv':piv,'H':[[int(z) for z in row] for row in HH.tolist()],'b':[int(z) for z in bb],'bounds':bounds,'solved':cols,'free':free,'mod_equations':A[:rank],'G':[[int(z) for z in row] for row in G.tolist()]})
base=Path(__file__).parent
(base/'rightaction_parameters.json').write_text(json.dumps(out)+'\n')
for d in out:
 with (base/f'rightaction_{d["anchor"]}.in').open('w') as f:
  f.write(f'169 {d["variables"]} {d["den"]} {len(d["solved"])}\n')
  for z in [d['bounds'],d['solved'],d['free'],d['b']]+d['mod_equations']+d['H']+d['G']:f.write(' '.join(map(str,z))+'\n')
