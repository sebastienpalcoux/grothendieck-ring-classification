"""Independent exact check of saved span, Farkas and automorphism certificates.
No numerical optimization, no matrix pickle and no phase-LP implementation import.
"""

if not __debug__:
    raise RuntimeError('Proof verification requires assertions enabled; run without -O.')
from pathlib import Path
from fractions import Fraction as F
import json,sys,itertools,math,hashlib,time
import sympy as s
PACKAGE=Path(__file__).resolve().parents[1];ROOT=PACKAGE.parents[1];BASE=PACKAGE;OUT=PACKAGE/'domain';sys.path.insert(0,str(ROOT/'evidence/rank8_frontier_20261021/quadratic'))
from sextic_character_table import SexticTable,simple_data
paths=[]
def read(p):paths.append(p);return json.loads(p.read_text())
R=read(ROOT/'site/dist/downloads/fusion-tensors/R8_3_3472.txt');T=SexticTable(R,simple_data(3472));H=T.characters;N=list(map(s.Matrix,R));B=sum((x*x.T for x in N),s.zeros(8))
D=read(OUT/'low_beta_assignments.json');V=[tuple(v)for v in D['vectors']];highrows=read(OUT/'final_highs_discovery.json');hs=[tuple(v)for col,v,dim,bound in highrows if dim!=[490,350]];assert len(hs)==171
frames=read(PACKAGE/'frames/span_certificates.json')['frames'];assert len(frames)==len(D['psd_solutions'])==372
pairs=[(i,j)for i in range(1,8)for j in range(i,8)];u=(1,0,0,0,0,0,0,0);pi=(1,2,2,2,2,2,2,2)
co=[[[F(x)for x in T.coordinates(z)]for z in row]for row in H];dc=math.lcm(*(q.denominator for row in co for z in row for q in z));cc=[[[int(q*dc)for q in z]for z in row]for row in co]
def target(low,den):
 gram=[int(B[i,j])-sum(v[i]*v[j]for v in low)for i,j in pairs];moment=[]
 for i,j in pairs:
  for k in range(6):
   a=sum(low[e][i]*cc[e][j][k]for e in range(8))*den//dc
   b=sum(low[e][j]*cc[e][i][k]for e in range(8))*den//dc
   assert a==b,'distinguished S symmetry'
   if k==0:a-=den*sum(v[i]*v[j]for v in low)
   moment.append(a)
 return gram+moment
spanexcluded=[];surv=[];lowcache={};allowedcache={}
for idx,frame in enumerate(frames):
 assert frame['frame']==idx and frame['ids']==D['psd_solutions'][idx]
 low=[u]+[V[j]for j in frame['ids']]+[pi];lowcache[idx]=low;L=s.Matrix(low);G=B-L.T*L;kernel=G.nullspace();allowed=[v for v in hs if all(sum(x*y for x,y in zip(z,v))==0 for z in kernel)]
 assert set(allowed)==set(map(tuple,frame['allowed_highs']));allowedcache[idx]=allowed
 if not frame['span_consistent']:
  cert=frame['certificate'];a=list(map(F,cert['annihilator']));assert len(a)==28
  assert all(sum(z*v[i]*v[j]for z,(i,j)in zip(a,pairs))==0 for v in allowed)
  rhs=target(low,dc)[28:];z=[sum(a[i]*rhs[6*i+k]for i in range(28))/dc for k in range(6)]
  assert z==list(map(F,cert['residual_coordinates']))and any(z);spanexcluded.append(idx)
 else:surv.append(idx)
 if idx%100==0:print('span',idx,flush=True)
assert len(spanexcluded)==276 and len(surv)==96
# Reconstruct all source automorphisms allowed by distinct FP dimensions.
vi={v:i for i,v in enumerate(V)};fi={tuple(f['ids']):f['frame']for f in frames};autos=[]
for ap in itertools.permutations([1,2,4]):
 for cp in itertools.permutations([5,6,7]):
  p=[0,ap[0],ap[1],3,ap[2],*cp]
  if not all(R[p[i]][p[j]][p[k]]==R[i][j][k]for i in range(8)for j in range(8)for k in range(8)):continue
  charmap=[H.index(tuple(row[p[i]]for i in range(8)))for row in H];charinv=[charmap.index(i)for i in range(8)];vmap=[]
  for v in V:
   w=[0]*8
   for i in range(8):w[p[i]]=v[i]
   vmap.append(vi[tuple(w)])
  autos.append((p,charinv,vmap))
assert len(autos)==9
seen=set();orbits=[]
for idx in surv:
 if idx in seen:continue
 orb=set()
 for p,charinv,vmap in autos:
  new=[None]*6
  for E,v in zip(D['characters'],frames[idx]['ids']):new[charinv[E]-1]=vmap[v]
  to=fi[tuple(new)];assert to in surv;orb.add(to)
 seen|=orb;orbits.append(sorted(orb))
old=read(PACKAGE/'frames/automorphism_orbits.json');assert orbits==old['orbits']and len(seen)==96
# Independently build every integer phase column and right-hand side.
atoms=read(PACKAGE/'frames/first_trace_atoms.json');phase=[list(map(F,z['coordinates']))for z in atoms['atoms']];assert len(phase)==33
den=2*math.lcm(dc,*(q.denominator for a in phase for q in a));ph=[[int(q*den)for q in a]for a in phase];gramcols=[[v[i]*v[j]for i,j in pairs]for v in hs]
certpaths=[PACKAGE/'frames/farkas_5_22_23.json',PACKAGE/'frames/exact_phase_farkas_25_27.json',PACKAGE/'frames/farkas_29_30_31.json',PACKAGE/'frames/farkas_39_40.json'];certs=sum((read(z)for z in certpaths),[]);certified=[]
for cert in certs:
 idx=cert['frame'];y=[0]*196
 if 'covector'in cert:
  for j,z in cert['covector']:y[j]=int(z)
 else:y=list(map(int,cert['row_coefficients']))
 keep=cert.get('supported_global_columns',cert.get('columns'));expected=[33*j+k for j,v in enumerate(hs)if v in set(allowedcache[idx])for k in range(33)];assert keep==expected and len(y)==196
 dots=[]
 for col in keep:
  hi,k=divmod(col,33);g=gramcols[hi];z=sum(y[i]*g[i]for i in range(28))+sum(y[28+6*i+d]*g[i]*ph[k][d]for i in range(28)for d in range(6));dots.append(z)
 rhs=target(lowcache[idx],den);pair=sum(z*b for z,b in zip(y,rhs));assert min(dots)>=0 and pair<0;assert min(dots)==int(cert['minimum_column_pairing'])and pair==int(cert['rhs_pairing']);certified.append(idx);print('farkas',idx,'PASS',flush=True)
assert sorted(certified)==[5,22,23,25,26,27,29,30,31,39,40]
remaining=[orb for orb in orbits if orb[0]not in certified];assert remaining==[[42,117,304]]
out={'status':'PASS_complete_372_frame_reduction','source_character_reconstruction':True,'span_certificates':len(spanexcluded),'source_automorphisms':len(autos),'surviving_orbits_before_Farkas':len(orbits),'exact_Farkas_representatives':sorted(certified),'remaining_frames':remaining[0],'phase_scale':den,'sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths},'scope':'Independent exact arithmetic on canonical tensor, source character construction, audited high support and phase atoms. No numerical solver invoked.'}
print(json.dumps({k:v for k,v in out.items()if k!='sha256'},indent=2))
