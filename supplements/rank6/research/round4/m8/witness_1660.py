import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round4_m8_ising_verlinde as M
from frontier_feasibility import rational_feasible
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_8_1660')
st=time.monotonic()
def stop(*a):raise TimeoutError('explicit 800 second witness budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(800)
try:
 d=M.data_for(R,3,24);col=d['lows'][0];lab=[0,5,4,1,3,2];ep=[1,1,1,-1,1];A,b,meta=M.system(R,d,col,ep,lab);x=rational_feasible(A,b)
 o={'id':'R6_8_1660','outcome':'exact_necessary_relaxation_witness' if x else 'no_exact_witness_found','scope':'pseudo_unitary_necessary_single_branch','height':3,'conductor':24,'columns':list(map(list,col)),'labelling':lab,'indicators':ep,'system':meta,'primal':x}
 if x:
  from fractions import Fraction
  xx={j:Fraction(p,q) for j,p,q in x};M.require(all(sum(Fraction(row[j])*v for j,v in xx.items())==rhs for row,rhs in zip(A,b)),'bad rational witness');o['exact_reconstruction_passed']=True
except TimeoutError as e:o={'outcome':'budget_incomplete','reason':str(e)}
finally:signal.alarm(0)
o['seconds']=time.monotonic()-st;(P/'research/round4/m8/1660_necessary_witness.json').write_text(json.dumps(o,separators=(',',':'))+'\n');print({k:v for k,v in o.items() if k not in ('primal','system')},flush=True)
