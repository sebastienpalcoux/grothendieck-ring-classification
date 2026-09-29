"""Verify all frontier Morita branches exactly, without an optimizer."""
import json,sys,itertools
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import sympy as s
from full_morita_gram import *
from rings import permute

def faithful_frames(M,g):
 r=M[0].rows;G=full_gram(M);cols=first_columns(M,g)
 require(G.rank()==len(cols),'not faithful case')
 counts=Counter(cols);unique=sorted(counts);V=s.Matrix.hstack(*G.columnspace())
 I=tuple(int(i==j) for i in range(r) for j in range(r));counts[tuple(int(i==0) for i in range(r))]-=1
 ij=list(itertools.combinations_with_replacement(range(r*r),2));target=tuple(int(G[i,j])-I[i]*I[j] for i,j in ij);groups=[]
 for c in unique:
  cs=set()
  for row in unique:cs.update(image_candidates(G,V,c,row))
  cs=[x for x in sorted(cs) if all(s.Matrix(r,r,x)*m==m*s.Matrix(r,r,x) for m in M)]
  options=[]
  # rank(G)=number of actual simples, so no two action matrices coincide.
  for selected in itertools.combinations(cs,counts[c]):
   vv=tuple(sum(x[i]*x[j] for x in selected) for i,j in ij)
   if all(x<=y for x,y in zip(vv,target)):options.append((vv,list(selected)))
  groups.append(options)
 groups.sort(key=len);out=[]
 def rec(at,res,chosen):
  if at==len(groups):
   if not any(res):out.append([I]+chosen)
   return
  for vv,cc in groups[at]:
   nxt=tuple(x-y for x,y in zip(res,vv))
   if all(x>=0 for x in nxt):rec(at+1,nxt,chosen+cc)
 rec(0,target,[])
 return out

def main():
 frozen=json.load(open(Path(__file__).with_name('frontier_full_morita.json')))
 R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==frozen['id'])
 fixed,seed,nodes,reps=anti_representations(R,1)
 require(len(reps)==len(frozen['branches'])==16,'incomplete module branches')
 bad=good=0
 for ti,(T,record) in enumerate(zip(reps,frozen['branches'])):
  require(record['branch']==ti and record['T']==[list(v) for v in T],'wrong module branch')
  ab,meta=system(R,1,fixed,T);require(meta==record['meta'],'wrong reconstructed metadata')
  if ab is None:
   require(record['outcome']=='exact_rank_obstruction','rank obstruction mislabelled');bad+=1
  elif record['outcome']=='exact_farkas_obstruction':check_farkas(*ab,record['y']);bad+=1
  else:
   require(record['outcome']=='exact_full_based_bimodule_witness','unverified branch')
   labels,L=module_matrices(R,1,fixed,T);M=[s.Matrix(m) for m in record['right_actions']]
   V=s.Matrix.hstack(*[m.reshape(36,1) for m in M]);require(V*V.T==full_gram(L),'wrong full Gram witness')
   require(M[0]==s.eye(6) and V.rank()==6,'wrong unit or dependent actions')
   require(all(m*l==l*m for m in M for l in L),'actions do not commute')
   require(all(m.T in M for m in M),'missing dual right action')
   N=record['dual_N'];require(all(M[a]*M[b]==sum((N[a][b][k]*M[k] for k in range(6)),s.zeros(6)) for a in range(6) for b in range(6)),'wrong dual multiplication')
   require(permute(N,tuple(record['census_permutation']))==R,'wrong based-ring identification')
   frames=faithful_frames(L,1);require(len(frames)==1,'nonunique full action frame')
   require(set(map(tuple,frames[0]))==set(tuple(m) for m in M),'unique frame differs from frozen witness')
   good+=1
 require((bad,good)==(14,2),'unexpected verified outcomes')
 print(json.dumps({'id':frozen['id'],'exact_rejected_module_branches':bad,'unique_based_bimodule_completions':good,'dual_ring':'R6_3_215','categorification_asserted':False}))
if __name__=='__main__':main()
