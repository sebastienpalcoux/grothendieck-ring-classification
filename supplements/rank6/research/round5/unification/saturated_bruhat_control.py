"""Optimizer-free positive, mutation and finite-model vector-Bruhat controls."""
import hashlib,json,sys,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import scipy.optimize as op
def denied(*a,**k):raise RuntimeError('numerical optimizers disabled')
op.linprog=op.milp=denied
from exact import require,evaluate
from round3_m4 import data_for
from dimension_block_support import saturated_characters
from equality_modrep import identities
from saturated_bruhat import verify_bruhat_model,phase_equations
st=time.monotonic()
R=[[[1,0],[0,1]],[[0,1],[1,1]]];d=data_for(R,2,5);C=d['C'];phi=d['dims'][1];D=d['DD'];pack=saturated_characters(d)
dims=[C.one,phi,phi,phi*phi];H=[[C.one,phi],[phi,-C.one]];S=[[H[i//2][j//2]*H[i%2][j%2]/D for j in range(4)]for i in range(4)];theta=[C.one,C.unit**2,C.unit**3,C.one]
mv=lambda M,v:[sum((a*b for a,b in zip(row,v)),C.zero)for row in M]
ch=next(x for x in pack['characters']if x['conductor']==5);cert=identities(d,ch)
require(all(len(a.to_list())<=1 for a in ch['weights']),'nonrational Fourier weight in quadratic control')
L=[sum((C(a.to_list())*evaluate((dd/D).to_list(),C.unit**b,C)for a,b in zip(ch['weights'],pack['reps'])),C.zero)for dd in dims];w=mv(S,L)
require(w==[C.one,C.zero,C.zero,-C.one],'Fibonacci Fourier-vector normalization failed')
full_checks=0;low_checks=0
for n in range(1,5):
    left=mv(S,[t**n*z for t,z in zip(theta,L)]);right=[C(cert['character'][n])*t**(-pow(n,-1,5))*z for t,z in zip(theta,L)]
    require(left==right,'Fibonacci full vector-Bruhat failed');full_checks+=1
    for a in(0,3):require(left[a]==C(cert['character'][n])*L[a],'Fibonacci low-row Bruhat failed');low_checks+=1
cols=[[1,0],[1,1]];lab=d['tab'].assignments(cols)[0];rows,rhs,forbidden,metadata=phase_equations(d,[[1]],cols,lab,cert)
point=[0]*len(d['phases'])
for t in theta[1:3]:point[d['phases'].index((t,t*t))]+=1
require(all(not point[j]for j in forbidden),'realized Fibonacci root removed')
require(all(sum((a*n for a,n in zip(row,point)),pack['E'].zero)==b for row,b in zip(rows,rhs)),'Fibonacci row-encoder failed')
one=d['phases'].index((C.one,C.one));mutation=sum(2*row[one]!=b for row,b in zip(rows,rhs));require(mutation>0,'trivialized-twist mutation not detected')
census=json.loads((P/'data/census.json').read_text());finite=[]
for ident in('R6_5_1204','R6_8_1660'):
    R0=next(x['N']for x in census if x['id']==ident);data=data_for(R0,3,24)
    for cc in saturated_characters(data)['characters']:finite.append(dict(id=ident,**verify_bruhat_model(identities(data,cc))))
out=dict(passed=True,optimizer_used=False,optimized_python=not __debug__,fibonacci_full_vector_checks=full_checks,fibonacci_low_coordinate_checks=low_checks,row_encoder_checks=len(rows),trivialized_twist_failures=mutation,finite_models=finite,elapsed_seconds=round(time.monotonic()-st,3),files={})
files=[Path(__file__),P/'software/saturated_bruhat.py',P/'research/round5/unification/equality_modrep.py',P/'software/dimension_block_support.py',P/'software/round3_m4.py',P/'software/exact.py',P/'data/census.json']
out['files']={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest()for f in files}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True)
