"""Exact irreducible T spectra of SL(2,Z/m); no numerical character recovery."""
import argparse, collections, hashlib, itertools, json, math, signal, sys, time
from pathlib import Path
import sympy as s
from sympy.polys.matrices import DomainMatrix
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'software'))
from exact import require,evaluate
HERE=Path(__file__).parent

def mul(g,h,m):
 a,b,c,d=g;e,f,u,v=h
 return ((a*e+b*u)%m,(a*f+b*v)%m,(c*e+d*u)%m,(c*f+d*v)%m)
def inv(g,m):a,b,c,d=g;return(d,-b%m,-c%m,a)
def finite_group(m):
 G=[g for g in itertools.product(range(m),repeat=4) if (g[0]*g[3]-g[1]*g[2])%m==1]
 one=(1,0,0,1);todo=set(G);classes=[]
 while todo:
  g=one if one in todo else min(todo)
  cl={mul(mul(h,g,m),inv(h,m),m) for h in G};require(cl<=todo,'overlapping classes');classes.append(sorted(cl));todo-=cl
 classes.sort(key=lambda c:(c!=[one],len(c),c));ix={g:i for i,c in enumerate(classes) for g in c};n=len(classes);N=[]
 for i,cl in enumerate(classes):
  counts=[[0]*n for _ in range(n)];x=cl[0]
  for j,cj in enumerate(classes):
   for y in cj:counts[j][ix[mul(x,y,m)]]+=1
  for j in range(n):
   for k in range(n):
    q,r=divmod(counts[j][k]*len(cl),len(classes[k]));require(not r,'nonintegral class product');counts[j][k]=q
  N.append(counts)
 require(all(N[i][j]==N[j][i] for i in range(n) for j in range(n)),'noncommutative class algebra')
 T=(1,1,0,1);powers=[one]
 for _ in range(1,m):powers.append(mul(powers[-1],T,m))
 require(mul(powers[-1],T,m)==one,'incorrect T order')
 orders=[]
 for c in classes:
  h=one
  for r in range(1,len(G)+1):
   h=mul(h,c[0],m)
   if h==one:orders.append(r);break
  else:raise ValueError('group exponent enumeration failed')
 print('group',m,'order',len(G),'classes',n,'exponent',math.lcm(*orders),flush=True)
 return dict(modulus=m,order=len(G),classes=classes,sizes=list(map(len,classes)),class_algebra=N,power_classes=[ix[g] for g in powers],central_class=ix[((-1)%m,0,0,(-1)%m)],exponent=math.lcm(*orders))

def coefficient_field():return s.QQ.alg_field_from_poly(s.Poly(s.cyclotomic_poly(48,s.Symbol('x')),s.Symbol('x')),alias='z')

def characters(group,C):
 n=len(group['classes']);N=group['class_algebra'];x=s.Symbol('x');blocks=[DomainMatrix.eye(n,C)];used=[]
 # Use small class sums first, then larger ones until all joint spaces are lines.
 for i in sorted(range(1,n),key=lambda i:(group['sizes'][i],i)):
  if all(B.shape[1]==1 for B in blocks):break
  A=s.Matrix(n,n,lambda k,j:N[i][j][k]);poly=A.charpoly(x).as_poly();factors=poly.factor_list()[1];roots=[]
  for f,mult in factors:
   ff=s.Poly.from_list([C.convert(a) for a in f.all_coeffs()],x,domain=C)
   fs=ff.factor_list()[1]
   require(all(g.degree()==1 for g,e in fs),'character field does not split class spectrum')
   for g,e in fs:
    aa,bb=g.rep.to_list();roots.append(-bb/aa)
  if len(roots)==1:continue
  DM=DomainMatrix.from_Matrix(A).convert_to(C);new=[]
  for B in blocks:
   if B.shape[1]==1:new.append(B);continue
   AB=DM.matmul(B)
   for z in roots:
    K=(AB-B.scalarmul(z)).nullspace().transpose()
    if K.shape[1]:new.append(B.matmul(K))
  require(sum(B.shape[1] for B in new)==n,'joint eigenspaces incomplete');blocks=new;used.append(i)
  print('split',group['modulus'],i,'roots',len(roots),'blocks',[B.shape[1] for B in blocks],flush=True)
 require(len(blocks)==n and all(B.shape[1]==1 for B in blocks),'class generators fail to separate characters')
 rec=[];conj=lambda z:evaluate(z.to_list(),C.unit**47,C)
 for B in blocks:
  v=[r[0] for r in B.to_list()];p=next(j for j,z in enumerate(v) if z)
  lam=[sum((C(N[i][j][p])*v[j] for j in range(n) if N[i][j][p]),C.zero)/v[p] for i in range(n)]
  norm=sum((z*conj(z)/C(a) for z,a in zip(lam,group['sizes'])),C.zero)
  dd=C(group['order'])/norm;coeff=dd.to_list();require(len(coeff)==1,'nonrational character degree square');dd=s.Rational(coeff[0]);degree=math.isqrt(int(dd));require(dd==degree*degree and degree>0,'nonintegral character degree')
  ch=[C(degree)*z/C(a) for z,a in zip(lam,group['sizes'])]
  spectra=[]
  for k in range(group['modulus']):
   z=sum((ch[j]*C.unit**((-48//group['modulus']*k*r)%48) for r,j in enumerate(group['power_classes'])),C.zero)/C(group['modulus'])
   co=z.to_list();q=s.Rational(co[0]) if len(co)==1 else s.S.Zero if not co else None
   require(q is not None and q.q==1 and q>=0,'invalid T multiplicity');spectra.append(int(q))
  sign=ch[group['central_class']]/C(degree);require(sign in (C.one,-C.one),'invalid central sign')
  rec.append({'degree':degree,'T_multiplicities':spectra,'central_sign':1 if sign==C.one else -1,'characters':[list(map(str,z.to_list())) for z in ch]})
 rec.sort(key=lambda r:(r['degree'],r['T_multiplicities'],r['central_sign'],r['characters']))
 return rec,used

def verify(group,rec,C):
 n=len(group['classes']);N=group['class_algebra'];size=group['sizes'];order=group['order'];conj=lambda z:evaluate(z.to_list(),C.unit**47,C)
 require(len(rec)==n,'wrong number of irreducibles')
 for r in rec:
  require(type(r['degree']) is int and r['degree']>0,'nonpositive or nonintegral character degree')
  require(type(r['central_sign']) is int and r['central_sign'] in (-1,1),'invalid recorded central sign')
  require(len(r['characters'])==n,'wrong character row length')
  require(len(r['T_multiplicities'])==group['modulus'] and all(type(z) is int and z>=0 for z in r['T_multiplicities']),'invalid recorded T multiplicities')
  require(sum(r['T_multiplicities'])==r['degree'],'recorded T degree mismatch')
 chars=[[C([s.Rational(t) for t in z]) for z in r['characters']] for r in rec]
 require(sum(r['degree']**2 for r in rec)==order,'degree-square sum')
 for a,row in enumerate(chars):
  d=rec[a]['degree'];require(row[0]==C(d),'identity character degree')
  lam=[C(q)*z/C(d) for q,z in zip(size,row)]
  for i in range(n):
   for j in range(n):require(lam[i]*lam[j]==sum((C(c)*z for c,z in zip(N[i][j],lam) if c),C.zero),'class algebra character failed')
  for b,other in enumerate(chars[:a+1]):require(sum((C(q)*z*conj(w) for q,z,w in zip(size,row,other)),C.zero)==C(order*int(a==b)),'character orthogonality')
  for k in range(group['modulus']):
   z=sum((row[j]*C.unit**((-48//group['modulus']*k*r)%48) for r,j in enumerate(group['power_classes'])),C.zero)/C(group['modulus'])
   require(z==C(rec[a]['T_multiplicities'][k]),'T multiplicity replay')
  require(row[group['central_class']]==C(d*rec[a]['central_sign']),'central sign replay')
 print('exact character checks passed',group['modulus'],n,flush=True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--modulus',type=int,required=True);ap.add_argument('--verify',action='store_true');ap.add_argument('--seconds',type=int,default=840);args=ap.parse_args();signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('bounded exact character job')));signal.alarm(args.seconds);st=time.monotonic()
 g=finite_group(args.modulus);require(48%g['exponent']==0,'field48 not a splitting field by exponent');C=coefficient_field();path=HERE/f'sl2_{args.modulus}.json'
 if args.verify:
  out=json.loads(path.read_text());require(out['group']==json.loads(json.dumps(g)),'group data mismatch');rec=out['irreps']
 else:
  rec,used=characters(g,C);out={'group':g,'irreps':rec,'separating_classes':used};path.write_text(json.dumps(out,separators=(',',':'))+'\n')
 verify(g,rec,C)
 receipt={'passed':True,'optimizer_used':False,'optimized_python':not __debug__,'modulus':args.modulus,'group_order':g['order'],'irreducibles':len(rec),'files_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__).resolve(),path,ROOT/'software/exact.py']}}
 (HERE/f'sl2_{args.modulus}_replay.json').write_text(json.dumps(receipt,indent=2)+'\n');print('finished',args.modulus,time.monotonic()-st,flush=True)
if __name__=='__main__':main()
