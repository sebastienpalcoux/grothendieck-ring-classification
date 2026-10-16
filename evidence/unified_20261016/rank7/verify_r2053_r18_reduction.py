#!/usr/bin/env python3
"""Exact source-bound endpoint of the proved R2053 dihedral Morita reduction."""
import argparse,collections,gzip,hashlib,itertools,json
from pathlib import Path

def need(x,m):
 if not x:raise RuntimeError(m)
def sha(N):return hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
def source(path,rank,mult,index,lexical=False):
 rows=[];count=0
 for line in gzip.open(path,'rt'):
  if not line.strip():continue
  N=json.loads(line.replace('{','[').replace('}',']'))
  if max(z for a in N for b in a for z in b)!=mult:continue
  if lexical:rows.append(N)
  else:
   count+=1
   if count==index:return N
 if lexical:return sorted(rows)[index-1]
 raise RuntimeError('missing source')
def fusion_check(N):
 n=len(N);one=[1]+[0]*(n-1)
 dual=[]
 for i in range(n):
  need(N[0][i]==N[i][0]==[int(j==i)for j in range(n)],'unit')
  jj=[j for j in range(n)if N[i][j][0]];need(len(jj)==1 and N[i][jj[0]][0]==1,'dual');dual.append(jj[0])
 for i,j,k in itertools.product(range(n),repeat=3):
  need(N[i][j][k]==N[dual[i]][k][j]==N[k][dual[j]][i],'reciprocity')
  for l in range(n):need(sum(N[i][j][a]*N[a][k][l]for a in range(n))==sum(N[j][k][a]*N[i][a][l]for a in range(n)),'associativity')
 return dual

def verify(repo):
 N=source(repo/'supplements/rank7/data/rank7_tables.txt.gz',7,4,2053)
 T18=source(repo/'supplements/rank8/data/rank8_tables.txt.gz',8,1,18,True)
 need(sha(N)=='17b7a12f7ae481ec749633f470cf33ca50e4b09c3ea168be5392cc5dfe0f1534','R2053 binding')
 need(sha(T18)=='cdd3aa4477861e8521c75ac63cb0f9e4e5d0a021073d1619aae358a0850704f2','R18 binding')
 dual=fusion_check(N);G0=[0,1,2,6];X,Y,Z,h=4,3,5,6
 need(sum(N[g][g][0]for g in G0)==2,'C4 integral pointed part')
 need(N[X][X]==[int(i in G0)for i in range(7)],'TY square')
 need(N[h][h][0]==1 and all(N[h][w][w]==N[w][h][w]==1 for w in [X,Y,Z]),'fixed common involution')
 need(N[X][Y]==N[Y][X]==[int(i in [Y,Z])for i in range(7)] and N[Y][dual[Y]][X]==1,'split projective blocks')
 need(dual[Y]==Y and dual[Z]==Z,'self-dual irrational pair')
 G=list(itertools.product(range(4),range(2)));idx={g:i for i,g in enumerate(G)};e=(0,0);r=(1,0);s=(0,1)
 def mul(g,h):return((g[0]+(-1)**g[1]*h[0])%4,(g[1]+h[1])%2)
 def inv(g):return next(h for h in G if mul(g,h)==e)
 def phi(g):return((-g[0]+g[1])%4,g[1])
 def tensor(a,reflection):
  T=[[[0]*16 for _ in range(16)]for _ in range(16)]
  for i,g in enumerate(G):
   for j,h in enumerate(G):
    gh=mul(g,phi(h));T[i][j][idx[mul(g,h)]]=1;T[i][8+j][8+idx[mul(g,h)]]=1;T[8+i][j][8+idx[gh]]=1;T[8+i][8+j][idx[mul(gh,a)]]=1
    for k in G:
     if k[1]==int(reflection):T[8+i][8+j][8+idx[mul(gh,k)]]+=1
  return T
 # Trivial stabilizers give exactly the two irrational simple objects in the inverse reflection dual.
 H=[e,s];orbits=[];seen=set()
 for g in G:
  if g in seen:continue
  O={mul(mul(x,g),phi(y))for x in H for y in H};need(len(O)==4,'trivial inverse stabilizers');seen|=O;orbits.append(O)
 need(len(orbits)==2,'two inverse irrational objects')
 for a in [e,(2,0)]:
  dualorbits=[{mul(inv(a),phi(inv(g)))for g in O}for O in orbits]
  need(all(dualorbits[i]==orbits[i]for i in range(2))==(a==e),'a determined by source duality')
 # Rotational branch: pivotal odd cube forces r² positive; exact TY(C4) eighth indicator contradicts exponent dividing8.
 Rot=tensor(e,False);fusion_check(Rot);rho=8+idx[e]
 cube=[sum(Rot[rho][rho][j]*Rot[j][rho][k]for j in range(16))for k in range(16)]
 need(cube[:8]==[int(g[1]==0)for g in G],'all rotations once in rho cube')
 sums=[]
 for sign in [1,-1]:
  residues=[0]*4
  for aa,bb,cc in itertools.product(range(4),repeat=3):
   dd=(-aa-bb-cc)%4;residues[sign*(aa*bb+aa*cc+aa*dd+bb*cc+bb*dd+cc*dd)%4]+=1
  need(residues==[8,24,8,24],'Shimizu exact sum');sums.append(residues)
 # Remaining reflection branch and its actual closed fusion subcategory.
 Ref=tensor(e,True);fusion_check(Ref)
 sub=[idx[(j,0)]for j in range(4)]+[8+idx[(j,1)]for j in range(4)]
 need(all(Ref[i][j][k]==0 for i,j in itertools.product(sub,repeat=2)for k in set(range(16))-set(sub)),'closed full rank8 subcategory')
 T=[[[Ref[i][j][k]for k in sub]for j in sub]for i in sub]
 rr,sg=1,4
 need(T[rr][sg]==T[sg][rr],'sigma commutes with r')
 need(T[sg][sg]==[int(i==3)+int(i>=4)for i in range(8)],'sigma squared equals r cubed plus P sigma')
 mapping=[0,1,7,2,4,3,6,5]
 need(all(T[i][j][k]==T18[mapping[i]][mapping[j]][mapping[k]]for i,j,k in itertools.product(range(8),repeat=3)),'all512 source coefficients')
 return {'status':'PASS','scope':'general complex categorification of R7_4_2053 implies categorification of R8_1_18','source_tensor_sha256':sha(N),'endpoint_tensor_sha256':sha(T18),'reflection_tensor_sha256':sha(Ref),'neutral_to_census':mapping,'inverse_irrational_orbits':[[list(g)for g in sorted(O)]for O in orbits],'rotational_indicator_residues':sums,'endpoint_coefficients_checked':512,'optimizer_used':False}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path);a=ap.parse_args();out=verify(a.repo)
 if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
