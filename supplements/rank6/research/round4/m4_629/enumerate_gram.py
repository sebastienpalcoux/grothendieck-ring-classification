import json,sys,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path[:0]=[str(P/'software')]
import round3_m4 as m
from spectral_induction import Spectrum
import sympy as s
R=next(x['N'] for x in json.load(open(P/'data/unresolved_tensors.json')) if x['id']=='R6_4_629');st=time.monotonic();d=m.data_for(R,3,15);cols=d['lows'][3];tab=d['tab'];G,vs=m.high_vectors(d,cols);sp=Spectrum(tab,cols,[(v,None) for v in vs]);vs=[v for v in vs if list(v) not in sp.forbidden]
A=[[v[i]*v[j] for v in vs] for i in range(5) for j in range(i,5)];b=[int(G[i,j]) for i in range(5) for j in range(i,5)];rows,bs=sp.balance([(v,0) for v in vs],len(vs));A+=rows;b+=bs
print('rank',s.Matrix(A).rank(),'cols',len(vs),'rref',flush=True);M,piv=s.Matrix(A).row_join(s.Matrix(b)).rref();free=[j for j in range(len(vs)) if j not in piv];print('free',len(free),free,flush=True)
print('bounds',[min(int(G[i,i])//(vs[j][i]**2) for i in range(5) if vs[j][i]) for j in free],flush=True)
Path(__file__).with_suffix('.json').write_text(json.dumps({'A':A,'b':b,'vs':vs,'free':free,'rref':[[str(z) for z in row] for row in M.tolist()],'pivots':list(piv)}));print('seconds',time.monotonic()-st,flush=True)
