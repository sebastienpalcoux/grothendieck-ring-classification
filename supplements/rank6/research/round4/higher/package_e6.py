import sys,json
from pathlib import Path
D=Path(__file__).parent;r=json.loads((D/'R6_6_1035_half_e6_cached.json').read_text())
if r.get('outcome')!='pseudo_unitary_excluded':raise RuntimeError('incomplete source exclusion')
r.pop('id');r.pop('seconds');r.update(kind='half_e6_projection',version=1,complex_conjugation_reduction=True)
c={'kind':'general_half_e6_projection','version':1,'scope':'general','reduction':json.loads((D/'R6_6_1035_reduction.json').read_text()),'pseudo':r}
(D/'R6_6_1035_general.json').write_text(json.dumps(c,separators=(',',':'))+'\n')
