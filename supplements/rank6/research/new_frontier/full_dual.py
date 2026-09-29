"""Full Morita-action Gram exploration for a forced C2 algebra."""
import sys,json,itertools,math,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'software'))
import sympy as s
from module_dual_gram import anti_representations,module_matrices

def gram(M):
 r=M[0].rows
 return s.Matrix(r*r,r*r,lambda p,q:sum(m[q//r,p//r]*m[q%r,p%r] for m in M))

def first_columns(M,g):
 r=M[0].rows;done=set();cols=[]
 for a in range(r):
  if a in done:continue
  b=next(b for b in range(r) if M[g][a,b])
  v=[0]*r;v[a]=1
  if a==b:cols += [tuple(v),tuple(v)]
  else:v[b]=1;cols += [tuple(v)]
  done.update((a,b))
 return cols

def candidates(G,col,row=None):
 r=len(col);nn=r*r
 # Entries lie in the image of the full Gram matrix, with fixed column 0.
 A=G.columnspace();V=s.Matrix.hstack(*A)
 inds=list(range(0,nn,r)); vals=list(col)
 if row is not None:
  inds += list(range(1,r)); vals += list(row[1:])
 sol,pars=V.extract(inds,range(V.cols)).gauss_jordan_solve(s.Matrix(vals))
 ans=V*sol
 v=s.Matrix([x.subs({p:0 for p in pars}) for x in ans]);W=ans.jacobian(pars)
 if not W.cols:
  if all(x.is_Integer and x>=0 and x*x<=G[i,i] for i,x in enumerate(v)):
   return [tuple(map(int,v))]
  return []
 # Free parameters are replaced by selected actual entries to give finite boxes.
 piv=list(W.T.rref()[1]);W0=W.extract(piv,range(W.cols));H=W*W0.inv();b=v-H*v.extract(piv,[0])
 bounds=[math.isqrt(G[i,i]) for i in piv]; result=[]
 for z in itertools.product(*(range(t+1) for t in bounds)):
  x=b+H*s.Matrix(z)
  if all(t.is_Integer and t>=0 and t*t<=G[i,i] for i,t in enumerate(x)):
   result.append(tuple(map(int,x)))
 return result

def main():
 ring=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']=='R6_3_215')
 fixed,seed,nodes,reps=anti_representations(ring,1)
 for t,T in enumerate(reps):
  labels,M=module_matrices(ring,1,fixed,T);G=gram(M);r=M[0].rows
  print('BRANCH',t,'rank',G.rank(),'eigen PSD',all(v>=0 for v in G.eigenvals()),flush=True)
  cols=first_columns(M,1);unique=sorted(set(cols)); allcs=[]
  for c in unique:
   out=[]
   for row in unique:
    try:out += candidates(G,c,row)
    except ValueError:pass
   out=sorted(set(out));allcs.append(out)
   print(c,cols.count(c),'candidates',len(out),flush=True)
  path=Path(__file__).with_name('branch_'+str(t)+'.json')
  path.write_text(json.dumps({'T':T,'labels':labels,'module':[[list(map(int,row)) for row in m.tolist()] for m in M], 'gram':G.tolist(),'columns':cols,'unique':unique,'candidates':allcs},default=int))
if __name__=='__main__':main()
