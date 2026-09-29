import sys,json,copy
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
p=Path(__file__).with_name('R6_6_49_c3_cached.json');r=json.loads(p.read_text());r.pop('id');r.pop('seconds');r.update(kind='cyclic_three_projection',version=1)
for br in r['branches']:
 for c in br.get('cases',[]):c['associator_class']=c.pop('conjugate')
c={'kind':'general_cyclic_three_projection','version':1,'scope':'general','reduction':{'kind':'two_FP_values'},'pseudo':r}
Path(__file__).with_name('R6_6_49_general.json').write_text(json.dumps(c,separators=(',',':'))+'\n')
