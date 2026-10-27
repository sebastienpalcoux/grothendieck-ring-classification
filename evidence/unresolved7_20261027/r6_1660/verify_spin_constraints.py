from pathlib import Path
import importlib.util,json,hashlib,runpy
from fractions import Fraction as Q
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('v',ROOT/'evidence/unified_20261016/rank6/verlinde_obstruction/verify_r1660_witness_verlinde.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
C=v.C;mul=v.mul
z=C([0,1]);q2=z**6+z**42;q3=z**4+z**44;d=3+2*q2+2*q3+q2*q3;D=4*(1+d*d)
def aut(a,k):return sum(co*z**((i*k)%48)for i,co in enumerate(a.a))
def inv(a):
 rest=aut(a,5)*aut(a,7)*aut(a,11);norm=a*rest
 v.need(not any(norm.a[1:]) and bool(norm.a[0]),'norm');return rest/norm.a[0]
tables={m:json.loads((ROOT/f'evidence/theoretical_20261016/rank6/r1660_modular_witness/inputs/sl2_{m}.json').read_text()) for m in(16,3)}
def transitions(pair,target):
 local={}
 for m,ir,targ in [(16,pair[0],(target*11)%16),(3,pair[1],target%3)]:
  tab=tables[m];rec=tab['irreps'][ir];index={tuple(g):i for i,cl in enumerate(tab['group']['classes'])for g in cl};chars=[C(list(reversed(a)))for a in rec['characters']]
  Sm=(0,m-1,1,0);Si=(0,1,m-1,0)
  vals=[[chars[index[mul(mul(mul((1,j,0,1),Sm,m),(1,k,0,1),m),Si,m)]]for k in range(m)]for j in range(m)]
  local[m]={a:sum(vals[j][k]*z**((-48//m*(targ*j+a*k))%48)for j in range(m)for k in range(m))/(m*m) for a,rank in enumerate(rec['T_multiplicities']) if rank}
  v.need(sum(local[m].values())==1,'norm transitions')
 return {(3*a+16*b)%48:pa*pb for a,pa in local[16].items()for b,pb in local[3].items()}

need=v.need
source=ROOT/'data/current_remaining_cases.py'
N=runpy.run_path(str(source))['TENSORS']['R6_8_1660']
sha=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
need(sha=='697ec27fe203356199bfcf674587be9c71455dbb681f2e086a076f726b03d267','source tensor')
H=[[sum(N[i][a][t]*N[i][t][b] for i in range(6) for t in range(6)) for b in range(6)] for a in range(6)]
need(H[2][2]==142 and H[3][3]==142 and H[2][3]==138,'induction Gram')
need(H[2][2]+H[3][3]-2*H[2][3]==8,'total asymmetry')
low0=[[1,0,0,0,0,0],[1,0,3,3,0,4],[1,0,1,1,0,2],[1,0,2,2,0,2],[1,1,2,4,0,4],[1,1,4,2,0,4]]
low1=low0[:4]+[[1,1,3,3,0,4]]*2
need([8-sum((w[2]-w[3])**2 for w in low) for low in (low0,low1)]==[0,8],'high budgets')
beta5=D*inv(aut(D,5)); beta7=D*inv(aut(D,7))
need(beta5==1+(4+2*q2)*d and beta7==d*d,'Galois-unit dimensions')
spin=4*d+q2+3*q2*d
need(beta5*aut(spin,5)*inv(spin)==-1,'spin ratio5')
need(beta7*aut(spin,7)*inv(spin)==1,'spin ratio7')
need(beta7*aut(d,7)*inv(d)==-1 and aut(q2,7)==q2,'all nonspin high ratio7')
for q,a,target in [(1,1,1),(2,1,-1)]:
 x=d*(q+a*q2);need(beta5*aut(x,5)*inv(x)==target,'homogeneous ratio')
pp=transitions((44,2),9)
need(pp=={9:C(0),12:C(Q(1,4)),15:C(Q(1,4)),33:C(0),36:C(Q(1,4)),39:C(Q(1,4))},'W44 transitions')
conditional=sum(prob*(1 if phase==12 else -1) for phase,prob in pp.items())
need(conditional==C(Q(-1,2)),'symmetric phase36 contradiction')
surviving=sum(prob*(1 if phase in (12,36) else -1) for phase,prob in pp.items())
need(surviving==0,'even packet surviving expectation')
for pair,target,hom in [((16,2),15,30),((20,2),9,42)]:
 pr=transitions(pair,target)
 need(sum(prob*(1 if phase==hom else -1) for phase,prob in pr.items())==0,'alternative branch passes')
paths=[source,ROOT/'evidence/unified_20261016/rank6/verlinde_obstruction/verify_r1660_witness_verlinde.py']+[ROOT/f'evidence/theoretical_20261016/rank6/r1660_modular_witness/inputs/sl2_{m}.json' for m in(16,3)]
receipt={'status':'PASS','ring':'R6_8_1660','classification':'UNRESOLVED','source_tensor_sha256':sha,'input_sha256':{str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths},'high_asymmetry_budgets':[0,8],'W44_phase9_transition':{str(k):x.encode() for k,x in pp.items()},'W44_symmetric_phase36_diagonal':conditional.encode(),'W44_even_packet_diagonal':surviving.encode(),'A7_nonspin_high_ratio':-1,'A7_spin_ratio':1,'A7_signed_permutation_theorem_arithmetic':'PASS','whole_spin_branch_excluded':False,'ring_excluded':False,'categorification_constructed':False}
Path(__file__).with_name('spin_constraints_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
