import sys,json,math
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));from round5_629 import *
from cyclotomic_stabilizer_trace import integral_charpoly
here=Path(__file__).parent;R,d,cols,lab,src=source_data();C=d['C'];D=d['DD'];dims=d['dims'];low=[sum((C(sum(c[i]*c[j] for c in cols))*dims[j] for j in range(6)),C.zero) for i in range(6)];out=[]
for case in json.load(open(here/'decoded_twists.json')):
 require(all(o['orbit_degree']==1 for o in case['orbits']),'nontrivial orbit')
 checks=[]
 for n in range(1,31):
  for i in range(1,6):
   z=low[i]
   for o in case['orbits']:
    v=o['column'];theta=C.unit**(15//o['root_order']*o['root_power']);dim=sum((C(v[j])*dims[j+1] for j in range(5)),C.zero)
    z+=C(o['copies']*v[i-1])*dim*theta**n
   z/=D;p=integral_charpoly(z,C)
   checks.append({'power':n,'object':i,'integral':p is not None,'value':list(map(str,z.to_list()))})
 bad=[x for x in checks if not x['integral']];print(case['rank'],case['solution'],'bad',bad,flush=True);out.append({'rank':case['rank'],'solution':case['solution'],'failures':bad,'checks':checks})
(here/'indicator_integrality.json').write_text(json.dumps(out))
