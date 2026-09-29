import sys,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT/'software'),str(ROOT/'research/round3/quartic')]
from galois_probe import *
from fractions import Fraction
import numpy as np
rid=sys.argv[1] if len(sys.argv)>1 else 'R6_4_91'
R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==rid);m.R=R;data=data_for(R,3);tab=table_for(R,data);cols=data['lows'][1];C=data['C'];out=[]
for lab in tab.assignments(cols):
 wi=json.load(open(ROOT/f'research/round3/quartic/{rid}_witness_{lab[-1]}.json'));counts=Counter()
 for j,val in zip(wi['keep'],map(Fraction,wi['variables'])):
  if j<len(wi['labels']) and val:counts[(0,)+tuple(wi['labels'][j][0])]+=int(val)
 counts.update(cols);sp=Spectrum(tab,cols,[(v[1:],None) for v in counts if v[0]==0]);tt=dict(zip(sp.vectors,sp.types));pairs=list(itertools.combinations_with_replacement(range(1,6),2));ccon=lambda x:evaluate(x.to_list(),C.unit**(data['F']-1),C)
 lowstar=[lab.index(tab.rows.index(tuple(ccon(x) for x in tab.rows[lab[a]]))) for a in range(6)]
 triples=list(itertools.combinations_with_replacement(range(1,6),3));nt={abc:Fraction(wi['variables'][wi['keep'].index(wi['base']+k)]) for k,abc in enumerate(triples)}
 nlow=[[int(a==lowstar[b])]+[nt[tuple(sorted((a,b,lowstar[c])))] for c in range(1,6)] for a,b in pairs]
 pp={v:[tt[v][lab[a]]*tt[v][lab[b]] for a,b in pairs] for v in counts};ww={v:C(counts[v])*tab.dims[v]**2/tab.D**2 for v in counts};G=[]
 for i in range(len(pairs)):
  row=[]
  for j in range(len(pairs)):
   z=sum((ww[v]*pp[v][i]*ccon(pp[v][j]) for v in counts),C.zero)-C(sum(a*b for a,b in zip(nlow[i],nlow[j])))
   require(len(z.to_list())<=1,'nonrational fourth product');row.append(str(z.to_list()[0] if z else 0))
  G.append(row)
 eig=np.linalg.eigvalsh(np.array(G,dtype=float));print(rid,lab,'eigen',eig,'minentry',min(Fraction(x) for row in G for x in row),flush=True)
 rec=dict(id=rid,lab=lab,pairs=pairs,high_gram=G,low_coefficients=[[str(x) for x in row] for row in nlow],eigenvalues_float=list(map(float,eig)),minimum_entry=str(min(Fraction(x) for row in G for x in row)));out.append(rec);Path(__file__).with_name(rid+'_product_gram_probe.json').write_text(json.dumps(out,indent=2)+'\n')
