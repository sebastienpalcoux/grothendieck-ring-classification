"""Exact normalized 2-cocycle and S3-conjugacy replay, standard library only."""
from pathlib import Path
import itertools,json
HERE=Path(__file__).resolve().parent

def need(v,msg):
 if not v:raise ValueError(msg)
def lin(cols,x):
 y=0
 for i,c in enumerate(cols):
  if x>>i&1:y^=c
 return y
T=[2,4,7]
def action(p,x):
 for _ in range(p%4):x=lin(T,x)
 return x
pairs=[(i,j)for i in range(1,4)for j in range(1,4)];index={ij:3*k for k,ij in enumerate(pairs)}
def val(f,i,j):return 0 if not i or not j else (f>>index[i,j])&7
def delta(f,i,j,k):return action(i,val(f,j,k))^val(f,i,(j+k)%4)^val(f,(i+j)%4,k)^val(f,i,j)
def kernel(rows,n):
 piv={}
 for a in rows:
  while a:
   k=a.bit_length()-1
   if k in piv:a^=piv[k]
   else:piv[k]=a;break
 free=[i for i in range(n)if i not in piv];out=[]
 for j in free:
  a=1<<j
  for i in sorted(piv):
   if (a&piv[i]).bit_count()%2:a|=1<<i
  need(all((a&r).bit_count()%2==0 for r in rows),'kernel solve');out.append(a)
 return out
def span(vs):
 out={0}
 for a in vs:out|={b^a for b in out}
 return out
def perm_product(a,b):return tuple(a[b[i]]for i in range(4))
def inverse(a):return tuple(a.index(i)for i in range(4))
def main():
 n=27;rows=[]
 for i,j,k in itertools.product(range(4),repeat=3):
  images=[delta(1<<a,i,j,k)for a in range(n)]
  for c in range(3):rows.append(sum(1<<a for a,x in enumerate(images)if x>>c&1))
 Z=span(kernel(rows,n));cob=[]
 for l in range(9):
  values=[0]+[(1<<(l%3))if i==l//3+1 else 0 for i in range(1,4)]
  f=0
  for i,j in pairs:f|=(action(i,values[j])^values[(i+j)%4]^values[i])<<index[i,j]
  cob.append(f)
 B=span(cob);need(B<=Z,'coboundaries are cocycles');need(len(Z)==128 and len(B)==64,'H2C4 order2')
 Bsub={x^action(2,x)for x in range(8)};restrictions={val(f,2,2)for f in Z}
 need(restrictions<=Bsub,'every C4 2-cocycle restricts to a C2 coboundary')
 # Explicit cochains trivializing the restriction for every normalized cocycle.
 trivializers=[{'cocycle':f,'restriction':val(f,2,2),'one_cochain':next(x for x in range(8)if x^action(2,x)==val(f,2,2))}for f in sorted(Z)]
 ident=tuple(range(4));perms=list(itertools.permutations(range(4)));S3=[p for p in perms if p[0]==0]
 fours=[]
 for p in perms:
  powers=[ident]
  for _ in range(4):powers.append(perm_product(p,powers[-1]))
  if powers[4]==ident and powers[2]!=ident:fours.append(p)
 need(len(fours)==6 and len(S3)==6,'cycle and point-stabilizer counts')
 base=fours[0];orbit={perm_product(perm_product(s,base),inverse(s))for s in S3};need(orbit==set(fours),'S3 transitive on4cycles')
 conjugators=[{'cycle':p,'conjugator':next(s for s in S3 if perm_product(perm_product(s,base),inverse(s))==p)}for p in fours]
 out={'passed':True,'action_columns':T,'normalized_Z2_count':len(Z),'normalized_B2_count':len(B),'H2_C4_order':len(Z)//len(B),'restriction_values':sorted(restrictions),'C2_coboundary_values':sorted(Bsub),'restriction_trivializers':trivializers,'base_four_cycle':base,'four_cycle_conjugators':conjugators}
 (HERE/'c4_torsor_independent.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS: all128 normalized C4 2-cocycles restrict trivially; S3 conjugates all6 four-cycles')
if __name__=='__main__':main()
