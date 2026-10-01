# Locate the enclosing frozen release or the explicitly supplied base.
import os as _task_os
from pathlib import Path as _TaskPath
def _find_release():
    if _task_os.environ.get("RANK6_PACKAGE"):
        return _TaskPath(_task_os.environ["RANK6_PACKAGE"]).resolve()
    for _p in _TaskPath(__file__).resolve().parents:
        for _c in (_p, _p / "Rank6_Categorification_M9"):
            if (_c / "software/round3_m4.py").is_file() and (_c / "data/census.json").is_file():
                return _c
    raise FileNotFoundError("Set RANK6_PACKAGE to the extracted multiplicity-nine package")
_TASK_PACKAGE = _find_release()

from pathlib import Path
import json,itertools,time,signal
HERE=Path(__file__).parent;st=time.time();signal.signal(signal.SIGALRM,lambda *_:(_ for _ in()).throw(TimeoutError('60-second exact enumeration budget')));signal.alarm(60)
import sys,hashlib,runpy,contextlib,io
P=_TASK_PACKAGE
source8=HERE/'sl2_8.json'
source3=P/'research/round5/m8_modrep/sl2_3.json'
locals_=[json.load(open(p))for p in [source8,source3]]
sys.path.insert(0,str(P/'research/round5/m8_modrep'));import finite_spectra48 as F
for m,loc in zip([8,3],locals_):
 group=F.finite_group(m)
 if json.loads(json.dumps(group))!=loc['group']:raise ValueError('group enumeration differs')
 F.verify(group,loc['irreps'],F.coefficient_field())
U=[1,5,7,11,13,17,19,23]
chars=[p for p in itertools.product((1,-1),repeat=8)if p[0]==1 and all(p[U.index(a*b%24)]==p[i]*p[j]for i,a in enumerate(U)for j,b in enumerate(U))]
triv=chars.index((1,)*8);chi2=chars.index(tuple(1 if a%8 in (1,7)else -1 for a in U));chii=chars.index(tuple(1 if a%4==1 else -1 for a in U))
exps=[12,0,0,12,21,0,12,21,4,16,8,20,5,5,13,13,6,6,18,18,9,9,12,0,18,0]
tar=[sum((e+1)%24==k for e in exps)for k in range(24)]
def central(local,index,a):
 m=local['group']['modulus'];j=next(j for j,c in enumerate(local['group']['classes'])if [a%m,0,0,a%m]in c)
 v=local['irreps'][index]['characters'][j];degree=local['irreps'][index]['degree']
 if len(v)!=1 or int(v[0]) not in [degree,-degree]:raise ValueError('non-scalar central character')
 return int(v[0])//degree
reps=[]
for i,A in enumerate(locals_[0]['irreps']):
 for j,B in enumerate(locals_[1]['irreps']):
  T=[0]*24
  for k,x in enumerate(A['T_multiplicities']):
   for l,y in enumerate(B['T_multiplicities']):T[(3*k+8*l)%24]+=x*y
  if all(x<=y for x,y in zip(T,tar)):
   gal=chars.index(tuple(central(locals_[0],i,a)*central(locals_[1],j,a)for a in U))
   reps.append(dict(indices=[i,j],degree=A['degree']*B['degree'],central_sign=A['central_sign']*B['central_sign'],T=T,gal=gal))
U=[1,5,7,11,13,17,19,23]
def prod(i,j):return chars.index(tuple(a*b for a,b in zip(chars[i],chars[j])))
base=[[0]*24 for _ in range(8)]
for e in [1,13]:base[triv][e]+=1;base[chi2][e]+=1
for e in [1,19]:base[chi2][e]+=1
for e in [5,17,9,21]:base[triv][e]+=1
groups=[('even_d',[1,13],triv,True),('odd_d',[22],triv,True),('odd_3d',[10],triv,True),('M',[7,19],chi2,True),('odd_2d_w',[6],triv,False),('odd_2d_w2',[14],triv,False)]
for name,es,sgn,neg in groups:
 for e in es:base[sgn][e]+=1
# Reorder by rarity of their supporting exponents to prune; enumerate multiplicities once per irrep.
support=[sum(bool(r['T'][k])for r in reps)for k in range(24)]
order=sorted(range(len(reps)),key=lambda i:(min(support[k]for k,v in enumerate(reps[i]['T'])if v),-reps[i]['degree']))
reps=[reps[i]for i in order];n=len(reps);suffix=[set()for _ in range(n+1)]
for k in reversed(range(n)):suffix[k]=suffix[k+1]|{e for e,v in enumerate(reps[k]['T'])if v}
sol=[];total=0;nodes=0;mult=[0]*n

def check():
 global total
 total+=1
 joint=[[0]*24 for _ in range(8)]
 for m,r in zip(mult,reps):
  for e,z in enumerate(r['T']):joint[r['gal']][e]+=m*z
 residual=[[a-b for a,b in zip(x,y)]for x,y in zip(joint,base)]
 if any(v<0 for r in residual for v in r):return
 opts=[]
 for name,es,sgn,neg in groups:
  poss=[]
  for h in range(8):
   if neg and chars[h][-1]!=-1:continue
   if name=='M' and h!=prod(chi2,chii):continue
   j=prod(sgn,h)
   if all(residual[j][e]>=1 for e in es):poss.append(h)
  if len(poss)!=1:return
  h=poss[0];opts.append(h)
  for e in es:residual[prod(sgn,h)][e]-=1
 if any(v for r in residual for v in r):return
 sol.append(dict(multiplicities=[dict(multiplicity=m,indices=r['indices'],degree=r['degree'],gal=r['gal'])for m,r in zip(mult,reps)if m],pair_characters=opts))

def rec(k,rem):
 global nodes
 nodes+=1
 if not any(rem):
  for j in range(k,n):mult[j]=0
  check();return
 if k==n or any(v and e not in suffix[k]for e,v in enumerate(rem)):return
 r=reps[k]['T'];bd=min(rem[e]//v for e,v in enumerate(r)if v)
 for m in range(bd+1):
  mult[k]=m;rec(k+1,[v-m*w for v,w in zip(rem,r)])
rec(0,tar)
# Independent exact known-low-row trace on the chi_sqrt2 six-space.
sys.argv=[str(P/'research/frontier/R6_4_155/verify_forced_twists.py'),'--package',str(P)]
with contextlib.redirect_stdout(io.StringIO()):ns=runpy.run_path(sys.argv[0])
C,dd,W,tab,lab,dat,roots,eps=[ns[k]for k in ['C','d','W','tab','lab','dat','roots','eps']]
known={}
for a,j in enumerate([1,23,25,24,18,19]):
 dl=sum((C(t)*dim for t,dim in zip(dat['lows'][6][a],dat['dims'])),C.zero)
 known[j]=[dl*tab.values[lab[a],v]/(12*dd)for v in W]
for j,k in [(1,0),(23,22),(18,16),(19,17)]:known[k]=[C(e)*x for e,x in zip(eps,known[j])]
vectors=[{1:1,23:1},{0:1,22:1},{16:1,17:1},{18:1,19:1},{24:1},{25:1}]
trace=C.zero
for v in vectors:
 z=sum((C(c*q)*known[i][j]for i,c in v.items()for j,q in v.items()),C.zero)/sum(c*c for c in v.values())
 trace+=z*roots[(exps[next(iter(v))]+1)%24]
if trace!=C.zero:raise ValueError('known chi2 trace should vanish')
K=F.coefficient_field()
def value_at_st(local,index):
 m=local['group']['modulus'];j=next(j for j,c in enumerate(local['group']['classes'])if [0,m-1,1,1]in c)
 return K([F.s.Rational(v)for v in local['irreps'][index]['characters'][j]])
st8=[value_at_st(locals_[0],r)for r in [4,8,23]];st3=value_at_st(locals_[1],0)
if (st8[0]+2*st8[1])*st3==K.zero or (st8[2]+st8[1])*st3!=K.zero:raise ValueError('low trace irrep distinction failed')
before_low_trace=len(sol)
sol=[r for r in sol if any(v['indices']==[23,0]for v in r['multiplicities'])]
if len(sol)!=4:raise ValueError('expected four representation types')
# det(s) = det(t)^(-3), det(C)=det(t)^(-6).
det_t_exponent=(sum(exps)+26)%24
det_s_exponent=(-3*det_t_exponent)%24
det_c_exponent=(-6*det_t_exponent)%24
if (det_t_exponent,det_s_exponent,det_c_exponent)!=(20,12,0):raise ValueError('determinant computation failed')
out=dict(passed=True,scope='exact finite character and Galois necessary conditions, not modular data',optimizer_used=False,T_decompositions=total,Galois_retained=before_low_trace,retained=len(sol),det_t_exponent_mod24=det_t_exponent,det_s_exponent_mod24=det_s_exponent,det_charge_conjugation=1,source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [source8,source3,P/'research/frontier/R6_4_155/verify_forced_twists.py']},nodes=nodes,seconds=time.time()-st,solutions=sol)
(HERE/'exact_enumeration.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items()if k!='solutions'});print('characters',sorted(set(tuple(s['pair_characters'])for s in sol)));print('solutions',sol)
