"""Complete finite parameters AFTER the categorical Morita/ENO reduction.
No failed finite associator search enters this enumeration.
"""
from pathlib import Path
import itertools,json
import ring_checks as common,bimodule,liptrap_certificate as lip
from finite_bicharacter_lemmas import group,forms,auts
HERE=Path(__file__).resolve().parent
E=list(itertools.product(range(8),range(2)));ei={g:i for i,g in enumerate(E)};SD=json.loads((HERE/'cocycle_SD16_mod16.json').read_text());D=json.loads((HERE/'original_tensors.json').read_text());accepted=['R12_1_'+str(n)for n in[28,183,240,405,408,419,522,530]]
def match(R):
 hits=[]
 for rid in accepted:
  if common.coarse(D[rid])!=common.coarse(R):continue
  p=common.based_iso(D[rid],R)
  if p is not None:hits.append(dict(id=rid,basis_map_source_to_model=p))
 common.require(len(hits)==1,'exactly one allowed census tensor');return hits[0]
def group_omega(u,g,h,k):
 if u==3:return SD[ei[g]][ei[h]][ei[k]]
 a,b=g;c,d=h;e,f=k;t=c+(-1)**d*e;return 2*a*(-1)**b*((t-t%8)//8)%16

def split(u):
 labs=[(a,g)for a in range(3)for g in E if int(a==2)==g[0]%2];degree=[g for a,g in labs];um=lambda g,h:((g[0]+u**g[1]*h[0])%8,g[1]^h[1])
 def ising(a,b,c):return int(c==a^b)if a<2 and b<2 else int(c==2)if(a==2)!=(b==2)else int(c<2)
 R=[[[ising(a,b,c)*int(um(g,h)==k)for c,k in labs]for b,h in labs]for a,g in labs]
 def F(a,b,c,k):
  aa,bb,cc,kk=[labs[x][0]for x in(a,b,c,k)]
  if aa==cc==2 and bb<2:return 8*bb*kk
  if aa<2 and bb==2 and cc<2:return 8*aa*cc
  common.require(not(aa==bb==cc==2),'three-Ising Fourier not needed')
  return 0
 return R,degree,F,[labs.index((a,(0,1)))for a in[0,1]]

def equiv(N,sigma,parity):
 labs=[];seen=set();n=len(N)
 for a in range(n):
  if a in seen:continue
  orb=sorted({a,sigma[a]});seen.update(orb)
  for bit in range(2 if len(orb)==1 else 1):labs.append((orb,bit))
 R=[]
 for A,aa in labs:
  row=[]
  for B,bb in labs:
   vals=[]
   for C,cc in labs:
    c=C[0];dim=sum(N[a][b][c]for a in A for b in B)
    if len(C)==2:vals.append(dim);continue
    tr=0
    for a in A:
     for b in B:
      if sigma[a]!=a or sigma[b]!=b or not N[a][b][c]:continue
      exp=(parity[a]+parity[b]-parity[c]+2*(aa+bb-cc))%4;common.require(exp in(0,2),'Hom involution');tr+=1 if exp==0 else-1
    common.require((dim+tr)%2==0 and dim+tr>=0,'equivariant multiplicity');vals.append((dim+tr)//2)
   row.append(vals)
  R.append(row)
 return R

def main():
 out=[];groupchecks=[];ref={r['u']:r for r in json.loads((HERE/'models.json').read_text())}
 for u in[7,3]:
  um=lambda g,h:((g[0]+u**g[1]*h[0])%8,g[1]^h[1])
  for g,h,k,l in itertools.product(E,repeat=4):common.require((group_omega(u,h,k,l)-group_omega(u,um(g,h),k,l)+group_omega(u,g,um(h,k),l)-group_omega(u,g,h,um(k,l))+group_omega(u,g,h,k))%16==0,'generator cocycle')
  r=(1,0);s=(0,1);res=sum(group_omega(u,r,(j,0),r)for j in range(8))%16;common.require(res%4==2,'restriction generates cyclic H3');common.require(group_omega(u,s,s,s)==0,'rotation cocycle restriction to inverse subgroup');groupchecks.append(dict(u=u,cocycle_equations=65536,cyclic_restriction_exponent_mod16=res))
  for nonsplit in[0,1]:
   if nonsplit:
    row=ref[u];R=row['source_tensor'];degree=[tuple(g)for g in row['source_degrees']];F0,_,_=lip.reconstruct(R,row['liptrap_certificate']);cs=[row['source_labels'].index(['g',0,1,a])for a in[0,1]];lip.check(R,row['liptrap_certificate'])
   else:R,degree,F0,cs=split(u)
   common.validate(R)
   for rot,mixed,sign in itertools.product(range(8),range(2)if u==7 else[0],range(2)):
    c=cs[sign];fix=F0(c,c,c,c);common.require(fix in[0,8],'order2 subgroup associator class')
    def F(a,b,d,k):
     g,h,j=[degree[x]for x in(a,b,d)];return(F0(a,b,d,k)+fix*g[1]*h[1]*j[1]+rot*group_omega(u,g,h,j)+8*mixed*(g[0]%2)*h[1]*j[1])%16
    M,info=bimodule.construct(R,F,c,q=16);hit=match(M);out.append(dict(branch='generalized_Ising',u=u,nonsplit=nonsplit,rotation=rot,mixed=mixed,inverse_lift_sign=sign,subgroup_correction=fix,**hit))
   print('generalized-Ising source',u,nonsplit,'complete',flush=True)
 tycases=[]
 for orders in[(8,),(4,2),(2,2,2)]:
  els,G=group(orders);Bs=[B for B in forms(orders,els)if B==list(map(list,zip(*B)))];N=[[[0]*9 for _ in range(9)]for _ in range(9)]
  for a,b in itertools.product(range(8),repeat=2):N[a][b][G[a][b]]=1
  for a in range(8):N[a][8][8]=N[8][a][8]=N[8][8][a]=1
  count=0
  for P in auts(orders,els):
   if sum(P[i]==i for i in range(8))!=4 or not all(P[P[i]]==i for i in range(8)):continue
   witnesses=[B for B in Bs if all(B[P[i]][P[j]]==B[i][j]for i,j in itertools.product(range(8),repeat=2))]
   if not witnesses:continue
   for parity in[0,1]:
    M=equiv(N,P+[8],[0]*8+[parity]);common.validate(M);hit=match(M);out.append(dict(branch='TY_equivariant',orders=orders,automorphism=P,parity=parity,invariant_bicharacter=witnesses[0],**hit));count+=1
  tycases.append(dict(orders=orders,symmetric_nondegenerate_bicharacters=len(Bs),action_square_parameters=count))
 (HERE/'exhaustive_catalog.json').write_text(json.dumps(dict(status='pass',constructions=len(out),group_cocycle_checks=groupchecks,ty_parameters=tycases,allowed_ids=sorted({r['id']for r in out}),records=out),indent=2)+'\n');print('COMPLETE',len(out),sorted({r['id']for r in out}))
if __name__=='__main__':main()
