"""Joint center Gram / induction-codegree / quadratic Galois / rotation system.
All finite columns enumerated without choosing low frames. Exact Farkas replay.
"""
import sys,json,math,itertools,time,subprocess,collections
from pathlib import Path
from fractions import Fraction as Q
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'sources'),str(ROOT/'phase2/integral_theory')]
from rings import Characters,codegree_poly
from exact import ec
from induction import discover_roots,check_roots
from higher_traces import trace_types,mul,integer_pair
from tensor_rotation import rotation_types
from center_lp import exact_separator,verify_ray

def div(x,y,q):
 norm=y[0]*y[0]-q*y[1]*y[1]
 return ((x[0]*y[0]-q*x[1]*y[1])/norm,(x[1]*y[0]-x[0]*y[1])/norm)
def sign(x,q):
 a,b=x
 if a==0:return 1 if b>0 else -1 if b<0 else 0
 if b==0:return 1 if a>0 else -1
 if a>0 and b>0:return 1
 if a<0 and b<0:return -1
 return (1 if a*a>q*b*b else -1)if a>0 else (1 if q*b*b>a*a else -1)
def scale(x,c):return (x[0]*c,x[1]*c)
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def inputs(rid):return json.load(open(ROOT/'work/verification_corpus.json'))['tensors'][rid]
def modular_columns(cols,ch,D,q):
 import flint
 n=ch.n;inv=ch.C.inv();den=int(s.ilcm(*[x.q for x in inv]));J=inv*den;ops=[list(map(int,J*N))for N in ch.N];keep=[]
 for v,z in cols:
  num=[sum(v[i]*ops[i][j]for i in range(n))for j in range(n*n)]
  M=flint.fmpq_mat(n,n,[flint.fmpq(x,den)for x in num]);coeff=list(M.charpoly());ratio=div(D,z,q);power=(Q(1),Q(0));ok=True
  for j in range(1,n+1):
   power=mul(power,ratio,q);c=Q(str(coeff[n-j]));val=scale(power,c)
   if not integer_pair(val,q):ok=False;break
  if ok:keep.append((v,z))
 return keep

def base(R):
 n=len(R);ch=Characters(R);f,K,ds,D,pD,emb=ch.fp();assert f.degree()==2
 co=list(map(int,f.all_coeffs()));disc=co[1]**2-4*co[2];q=math.prod(int(p)for p,e in s.factorint(disc).items()if e%2);h=math.isqrt(disc//q)
 def coords(x):
  z=[Q(str(c))for c in ec(x)];z=[Q(0)]*(2-len(z))+z
  return(z[1]-Q(co[1],2)*z[0],Q(h,2)*z[0])
 dims=list(map(coords,ds));DD=coords(D);assert DD[1]>0
 roots=discover_roots(codegree_poly(R),K)
 if roots is None:raise ValueError('formal codegrees do not split in FP field')
 check_roots(codegree_poly(R),K,roots)
 counts=collections.Counter(coords(D/r)for r in roots)
 B=ch.C;inv=B.inv();den=int(s.ilcm(*[a.q for a in inv]));Ai=[int(a*den)for a in inv]
 assert n*n*max(map(abs,Ai))*max(map(int,B.diagonal()))<2**120
 src=Path(__file__).with_name('quadratic_vectors.cpp');exe=src.with_suffix('')
 if not exe.exists()or exe.stat().st_mtime<src.stat().st_mtime:subprocess.run(['g++','-O3','-std=c++17',str(src),'-o',str(exe)],check=True)
 vals=[n,1]+[1]*n+list(map(int,B))+Ai+[den]
 proc=subprocess.run([str(exe)],input=' '.join(map(str,vals)),text=True,capture_output=True,check=True,timeout=120)
 raw=[tuple(map(int,line.split()))[:-1]for line in proc.stdout.splitlines()];cols=[]
 for v in raw:
  z=(sum(v[i]*dims[i][0]for i in range(n)),sum(v[i]*dims[i][1]for i in range(n)))
  if v[0]:
   if z not in counts:continue
  else:
   norm=z[0]*z[0]-q*z[1]*z[1]
   if norm==0 or not integer_pair(div(DD,z,q),q):continue
   if z[1]and((2*z[0])**2/norm).denominator!=1:continue
  cols.append((v,z))
 premod=len(cols);cols=modular_columns(cols,ch,DD,q)
 # Galois dimension closure, finite because vv^t<=B has been exhausted.
 ratio=div(DD,(DD[0],-DD[1]),q)
 def conj(z):
  out=mul(ratio,(z[0],-z[1]),q)
  return out if sign(out,q)>0 else scale(out,-1)
 available={z for v,z in cols};keep={z for z in available if conj(z)in available}
 cols=[(v,z)for v,z in cols if z in keep];pairs=sorted({tuple(sorted((z,conj(z))))for z in keep if z!=conj(z)})
 norm=DD[0]*DD[0]-q*DD[1]*DD[1];assert norm.denominator==1;primes=sorted(map(int,s.factorint(abs(norm.numerator))))
 return {'ch':ch,'q':q,'dims':dims,'D':DD,'counts':counts,'cols':cols,'galois_pairs':pairs,'primes':primes,'raw_columns':len(raw),'pre_modular_columns':premod,'pre_galois_dimensions':len(available),'post_galois_dimensions':len(keep)}

def system(R,height=4):
 data=base(R);n=len(R);q=data['q'];D=data['D'];B=data['ch'].C;counts=data['counts'];cols=data['cols'];types,bound=trace_types(q,data['primes'],height)
 active=data.get('active',list(range(n)));objects=[i for i in active if i]
 # Sparse column-oriented exact rational data.
 rows=[];rhs=[];basevars=[];labels=[]
 def row(label,b):rows.append(label);rhs.append(Q(b));return len(rows)-1
 gram=[(i,j,row(('gram',i,j),int(B[i,j])))for i,j in itertools.combinations_with_replacement(active,2)]
 lows={z:row(('low',list(map(str,z))),num)for z,num in sorted(counts.items())}
 gps=[(a,b,row(('galois',list(map(str,a)),list(map(str,b))),0))for a,b in data['galois_pairs']]
 first={(i,c):row(('moment1',i,c),0)for i in objects for c in range(2)}
 second={};unknown=[]
 for i in objects:
  eps=0 if data['ch'].du[i]!=i else 1 if any(R[j][data['ch'].du[j]][i]%2 for j in range(n))else None
  if eps is None:
   rr=[row(('moment2',i,c),-D[c])for c in range(2)];boundrow=row(('indicator_bound',i),1);unknown.append((i,rr,boundrow));second[i]=rr
  else:second[i]=[row(('moment2',i,c),eps*D[c])for c in range(2)]
 powers={}
 for i in objects:
  ps=[[1]+[0]*(n-1)]
  for k in range(1,height+1):ps.append([sum(ps[-1][a]*R[a][i][b]for a in range(n))for b in range(n)])
  powers[i]=ps
 rotblocks=[]
 for i in objects:
  for order in range(3,height+1):
   rs=[int(r)for r in s.divisors(order)if r<order];rots=rotation_types(q,order,rs)
   mass=row(('rotation_mass',i,order),powers[i][order][0]);equations=[]
   for at,r in enumerate(rs):
    eq=[row(('rotation',i,order,r,c),0)for c in range(2)];equations.append((at,r,eq))
   rotblocks.append((i,order,rs,rots,mass,equations))
 for v,z in cols:
  phases=[(-1,((Q(1),Q(0)),)*height)]if v[0]else list(enumerate(types))
  for ti,tt in phases:
   c={}
   for i,j,rr in gram:
    if v[i]*v[j]:c[rr]=Q(v[i]*v[j])
   if v[0]:c[lows[z]]=Q(1)
   for a,b,rr in gps:
    if z==a:c[rr]=Q(1)
    elif z==b:c[rr]=Q(-1)
   for i in objects:
    if not v[i]:continue
    m1=scale(mul(z,tt[0],q),v[i]);m2=scale(mul(z,tt[1],q),v[i])
    for k in range(2):
     if m1[k]:c[first[i,k]]=m1[k]
     if m2[k]:c[second[i][k]]=m2[k]
   for i,order,rs,rots,mass,equations in rotblocks:
    for at,r,eq in equations:
     multiplicity=sum(powers[i][r][a]*v[a]for a in range(n))
     mm=scale(mul(z,tt[order//r-1],q),multiplicity)
     for k in range(2):
      if mm[k]:c[eq[k]]=-mm[k]
   basevars.append(c);labels.append([list(v),list(map(str,z)),ti])
 for i,rr,br in unknown:
  c={rr[k]:-2*D[k]for k in range(2)if D[k]};c[br]=Q(1);basevars.append(c);labels.append(['indicator',i]);basevars.append({br:Q(1)});labels.append(['indicator_slack',i])
 for i,order,rs,rots,mass,equations in rotblocks:
  for typ in rots:
   c={mass:Q(1)}
   for at,r,eq in equations:
    mm=mul(D,typ[at],q)
    for k in range(2):
     if mm[k]:c[eq[k]]=mm[k]
   basevars.append(c);labels.append(['rotation',i,order,[[str(a),str(b)]for a,b in typ]])
 A=[];b=[]
 for i,value in enumerate(rhs):
  co=[v.get(i,Q(0))for v in basevars];den=math.lcm(value.denominator,*(v.denominator for v in co));line=[int(v*den)for v in co];bb=int(value*den);g=math.gcd(bb,*line)or 1;A.append([x//g for x in line]);b.append(bb//g)
 meta={'modular_integrality':True,'pre_modular_columns':data['pre_modular_columns'],'q':q,'dimensions':[[str(a),str(b)]for a,b in data['dims']],'D':list(map(str,D)),'height':height,'rows':rows,'candidate_columns':len(cols),'variables':len(basevars),'trace_types':len(types),'trace_order_bound':bound,'raw_columns':data['raw_columns'],'pre_galois_dimensions':data['pre_galois_dimensions'],'post_galois_dimensions':data['post_galois_dimensions'],'galois_pairs':[[list(map(str,a)),list(map(str,b))]for a,b in data['galois_pairs']]}
 if 'active'in data:meta['active_neutral_block']=active
 return A,b,meta

def run(rid,height=4):
 start=time.time();R=inputs(rid);A,b,meta=system(R,height);print(rid,'system',len(b),len(A[0]),meta['candidate_columns'],flush=True);y,why=exact_separator(A,b,timeout=90)
 out={'id':rid,'kind':'joint_quadratic_center','outcome':'excluded'if y else 'no_conclusion','metadata':meta,'ray':y,'solver_report':why,'seconds':time.time()-start}
 Path(__file__).with_name(rid+'_qcenter_h'+str(height)+'.json').write_text(json.dumps(out,indent=2)+'\n');print(rid,out['outcome'],out['seconds'],flush=True)
if __name__=='__main__':run(sys.argv[1],int(sys.argv[2])if len(sys.argv)>2 else 4)
