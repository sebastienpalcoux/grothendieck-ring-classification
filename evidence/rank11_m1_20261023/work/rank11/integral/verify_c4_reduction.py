from pathlib import Path
import sys,itertools,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import *

def span(vs):
 s={0}
 for v in vs:s|={x^v for x in list(s)}
 return s

def run():
 # Basis w0,w1,w2 and w3=w0+w1+w2.
 cols=[2,4,7]
 def t(a):
  out=0
  for i,c in enumerate(cols):
   if a>>i&1:out^=c
  return out
 N=lambda a:a^t(a)
 N2=lambda a:N(N(a))
 require(all(N(N2(a))==0 for a in range(8)),'nilpotence')
 imN={N(a)for a in range(8)};imN2={N2(a)for a in range(8)}
 kerN={a for a in range(8)if N(a)==0};kerN2={a for a in range(8)if N2(a)==0}
 require(len(imN)==4 and len(imN2)==2 and kerN==imN2 and len(kerN2)==4,'Jordan3 module')
 oddrep=next(a for a in range(8)if a not in imN)
 require(N(oddrep)in kerN2 and N(oddrep)not in imN2,'odd restriction injective')
 records=[]
 for no in[104,153]:
  rid=f'R11_1_{no}';R=read()[rid];d=dual(R);n=len(R)
  inv=[i for i in range(n)if sum(R[i][d[i]])==1]
  dims=[1 if i in inv else 2 for i in range(n)]
  require(all(sum(R[i][j][k]*dims[k]for k in range(n))==dims[i]*dims[j]for i,j in itertools.product(range(n),repeat=2)),'dimension character')
  S={0}|{k for i in range(n)for k in range(n)if R[i][d[i]][k]}
  while True:
   U=S|{k for i in S for j in S for k in range(n)if R[i][j][k]}
   if U==S:break
   S=U
  comps=[];seen=set()
  for i in range(n):
   if i in seen:continue
   C=sorted({k for a in S for k in range(n)if R[a][i][k]});seen|=set(C);comps.append(C)
  dg={i:k for k,C in enumerate(comps)for i in C}
  grading=[[dg[next(k for k in range(n)if R[C[0]][D[0]][k])]for D in comps]for C in comps]
  require(sorted(map(len,comps))==[2,2,2,5],'component ranks')
  require(len(dg)==n and sum(map(len,comps))==n,'component partition')
  require(all(dg[k]==grading[dg[i]][dg[j]] for i,j,k in itertools.product(range(n),repeat=3) if R[i][j][k]),'every homogeneous product')
  require(all(grading[0][i]==grading[i][0]==i for i in range(4)),'grading unit')
  require(all(grading[grading[i][j]][k]==grading[i][grading[j][k]] for i,j,k in itertools.product(range(4),repeat=3)),'grading associativity')
  require(set(inv)<=S and len(inv)==4 and len(S)==5,'neutral TY profile')
  m=next(iter(S-set(inv)))
  require(all(R[g][g][0]==1 and R[g][m][m]==R[m][g][m]==1 for g in inv),'neutral V4 action')
  require(R[m][m]==[int(k in inv) for k in range(n)],'neutral TY square')
  gen=next(a for a in range(1,4)if grading[a][a]!=0)
  degree2=grading[gen][gen]
  require(grading[degree2][degree2]==0 and grading[gen][degree2]not in[0,gen,degree2],'C4 grading')
  x=comps[gen][0];L=[g for g in inv if R[g][x][x]];Rt=[g for g in inv if R[x][g][x]]
  require(len(L)==len(Rt)==2 and L!=Rt,'distinct left/right stabilizers')
  require(R[x][d[x]]==[int(k in set(L)|{m}) for k in range(n)],'left internal end')
  require(R[d[x]][x]==[int(k in set(Rt)|{m}) for k in range(n)],'right internal end')
  records.append({'id':rid,'tensor_sha256':sha(R),'invertibles':inv,'adjoint':sorted(S),'components':comps,'grading_table':grading,'degree1':gen,'degree2':degree2,'left_stabilizer':L,'right_stabilizer':Rt,'degree2_dual':[d[x]for x in comps[degree2]],'degree2_selfdual':all(d[x]==x for x in comps[degree2]),'even_basis':sorted(S|set(comps[degree2])),'even_selfdual_count':sum(d[x]==x for x in S|set(comps[degree2]))})
 out={'status':'structural_reduction_only','cohomology':{'action_columns':cols,'imN':sorted(imN),'imN2':sorted(imN2),'kerN':sorted(kerN),'kerN2':sorted(kerN2),'odd_source_representative':oddrep,'odd_restriction_representative':N(oddrep),'H3_restriction':'isomorphism','H2_restriction':'zero'},'records':records}
 dump(Path(__file__).with_name('c4_reduction.json'),out);print(json.dumps(out,indent=2));return out
if __name__=='__main__':run()
