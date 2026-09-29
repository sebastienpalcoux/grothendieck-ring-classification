import sys,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round3_m4 as M
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_4_155');records=[]
base=Path(__file__).parent
for file,F in [('probe_h3.json',8),('probe_h6.json',8),('probe_F24_h3.json',24)]:
 c=json.load(open(base/file));data=M.data_for(R,c['height'],F);z={k:c[k] for k in ['height','low','labelling','indicators','rows','variables','values','center_rank']};z.update({'kind':'complex_center_primal','version':1,'F':F,'low_columns':list(map(list,data['lows'][c['low']])),'quartic':False,'source':file});records.append(z)
p=base/'pointed_probe.json'
if p.exists():
 c=json.load(open(p));data=M.data_for(R,c['height'],c['F'])
 for cc in c['cases']:
  if cc.get('outcome')!='exact_primal':continue
  z={k:cc[k] for k in ['low','labelling','indicators','rows','variables','values','center_rank']};z.update({'height':c['height'],'kind':'complex_center_primal','version':1,'F':c['F'],'low_columns':list(map(list,data['lows'][cc['low']])),'quartic':False,'pointed_subgroup':cc['K'],'source':'pointed_probe.json'});records.append(z)
rec={'id':'R6_4_155','tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),'claim':'Exact integral solutions of necessary systems only; no modular data or fusion category asserted.','certificates':records}
(base/'exact_primal_certificates.json').write_text(json.dumps(rec,separators=(',',':'))+'\n');print(len(records))
