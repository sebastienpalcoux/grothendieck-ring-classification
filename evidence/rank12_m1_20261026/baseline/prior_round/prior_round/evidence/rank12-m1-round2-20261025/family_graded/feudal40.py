from pathlib import Path
import sys,itertools,json,collections,time
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE));import feudal
common=feudal.require

def rings():
 # S=C5 rt C4(F20) or C5 rt V4(D10xC2), quotientQorder4.
 for name in ['F20','D10xC2']:
  Q=[[(a+b)%4 if name=='F20'else a^b for b in range(4)]for a in range(4)]
  invQ=[next(b for b in range(4)if Q[a][b]==0)for a in range(4)]
  act=[pow(2,a,5)for a in range(4)]if name=='F20'else[(-1 if a&1 else 1)for a in range(4)]
  G=[[5*Q[a//5][b//5]+(a%5+act[a//5]*(b%5))%5 for b in range(20)]for a in range(20)]
  sigmas=[p for p in itertools.permutations(range(4))if p[0]==0 and all(p[p[a]]==a for a in range(4))and all(p[Q[a][b]]==Q[p[a]][p[b]]for a,b in itertools.product(range(4),repeat=2))]
  for sigma in sigmas:
   for p in range(4):
    if sigma[p]!=p:continue
    R=[[[0]*24 for _ in range(24)]for _ in range(24)]
    for a,b in itertools.product(range(20),repeat=2):R[a][b][G[a][b]]=1
    for a,m in itertools.product(range(20),range(4)):R[a][20+m][20+Q[a//5][m]]=1;R[20+m][a][20+Q[m][sigma[a//5]]]=1
    for m,l in itertools.product(range(4),repeat=2):
     c=Q[Q[m][sigma[l]]][p]
     for h in range(5):R[20+m][20+l][5*c+h]=1
    yield dict(group=name,sigma=list(sigma),p=p),R

def solve_python(R,seconds=8):
 start=time.monotonic();z=feudal.setup(R,False);keys=z['keys'];ki={tuple(k):i for i,k in enumerate(keys)};M=z['M'];H=z['H'];h=len(H);form=z['forms'][0];piv={};constraints=[];equations=z['equations'];descs=z['descriptions']
 for row,desc in zip(equations,descs):
  if time.monotonic()-start>seconds:return None,dict(status='short_budget',seconds=seconds)
  a={i:v%5 for i,v in row.items()if v%5};b=[0]*len(M)
  if desc[0]=='bicharacter':_,x,y,m=desc;b[M.index(m)]=form[H.index(x)][H.index(y)]
  while a:
   k=min(a)
   if k not in piv:
    u=pow(a[k],-1,5);a={j:v*u%5 for j,v in a.items()};b=[v*u%5 for v in b];piv[k]=(a,b);break
   old,bb=piv[k];c=a[k]
   for j,v in old.items():
    nv=(a.get(j,0)-c*v)%5
    if nv:a[j]=nv
    elif j in a:del a[j]
   b=[(v-c*w)%5 for v,w in zip(b,bb)]
  if not a and any(b):constraints.append(b)
 good=next((t for t in itertools.product(range(1,5),repeat=len(M))if all(sum(v*w for v,w in zip(row,t))%5==0 for row in constraints)),None)
 if good is None:return None,dict(status='no_F5_phase_witness',constraints=constraints,seconds=time.monotonic()-start)
 x=[0]*len(keys)
 for k,(row,b)in sorted(piv.items(),reverse=True):x[k]=(sum(v*w for v,w in zip(b,good))-sum(v*x[j]for j,v in row.items()if j!=k))%5
 for row,desc in zip(equations,descs):
  rhs=0
  if desc[0]=='bicharacter':_,a,b,m=desc;rhs=form[H.index(a)][H.index(b)]*good[M.index(m)]
  common((sum(v*x[i]for i,v in row.items())-rhs)%5==0,'all positivephaseequations')
 forms=[[[v*t%5 for v in row]for row in form]for t in good]
 assignment=[z['forms'].index(tuple(tuple(v for v in row)for row in F))for F in forms]
 rec=dict(kind='liptrap_unitary_model',modulus=5,serfs=z['S'],lords=M,stabilizer=H,tau_times_tau_dual='1/5',tau='positive_inverse_square_root',bicharacter_assignment=assignment,phase_values=[list(k)+[x[i]]for i,k in enumerate(keys)],reference='Liptrap 1002.3166v2 Definition4.3/Theorem4/Lemma5.4')
 return rec,dict(status='positive',seconds=time.monotonic()-start)

def solve(R,seconds=8,variable_tau=False):
 import subprocess
 start=time.monotonic();z=feudal.setup(R,variable_tau);keys=z['keys'];M=z['M'];H=z['H'];form=z['forms'][0];lines=[f"{len(z['equations'])} {len(keys)}"]
 for row,desc in zip(z['equations'],z['descriptions']):
  b=[0]*4
  if desc[0]=='bicharacter':_,a,c,m=desc;b[M.index(m)]=form[H.index(a)][H.index(c)]
  entries=sorted((i,v%5)for i,v in row.items()if v%5)
  lines.append(' '.join(map(str,[len(entries)]+[a for iv in entries for a in iv]+b)))
 result=subprocess.run([str(OUT/'sparse5')],input='\n'.join(lines)+'\n',capture_output=True,text=True,timeout=seconds)
 common(result.returncode==0,'short sparse phase discovery process');ls=result.stdout.splitlines();status=ls[0]
 if status!='positive':return None,dict(status=status+'_F5_phase_attempt_only',seconds=time.monotonic()-start)
 good=list(map(int,ls[1].split()));x=list(map(int,ls[2].split()));common(len(x)==len(keys),'complete phasevalues')
 for row,desc in zip(z['equations'],z['descriptions']):
  rhs=0
  if desc[0]=='bicharacter':_,a,b,m=desc;rhs=form[H.index(a)][H.index(b)]*good[M.index(m)]
  common((sum(v*x[i]for i,v in row.items())-rhs)%5==0,'all positive phase equations')
 forms=[tuple(tuple(v*t%5 for v in row)for row in form)for t in good];assignment=[z['forms'].index(F)for F in forms]
 rec=dict(kind='liptrap_unitary_model',modulus=5,serfs=z['S'],lords=M,stabilizer=H,tau_times_tau_dual='1/5',tau='phase_times_inverse_square_root'if variable_tau else'positive_inverse_square_root',bicharacter_assignment=assignment,phase_values=[list(k)+[x[i]]for i,k in enumerate(keys)],reference='Liptrap 1002.3166v2 Definition4.3/Theorem4/Lemma5.4')
 return rec,dict(status='positive',seconds=time.monotonic()-start)

def main():
 rows=[]
 for par,R in rings():
  selected=(par['group']=='F20'and par['sigma']==[0,3,2,1]and par['p']==0)or(par['group']=='D10xC2'and par['sigma']in[[0,1,2,3],[0,3,2,1]]and par['p']in[0,2])
  if not selected:continue
  common(__import__('numpy').array(R).shape==(24,24,24),'shape');rec,info=solve(R);print(par,info,flush=True)
  rows.append(dict(parameters=par,tensor=R,certificate=rec,attempt=info));(OUT/'feudal40_models_sparse.json').write_text(json.dumps(rows,separators=(',',':'))+'\n')
if __name__=='__main__':main()
