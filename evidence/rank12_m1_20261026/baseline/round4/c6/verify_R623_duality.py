#!/usr/bin/env python3
import json
from pathlib import Path
P=Path(__file__).resolve().parent
J=json.loads((P/'audit/frozen_inputs.json').read_text());R=J['tensors']['R12_1_623'];low=J['controls']['R623']['low'];G=low['G']
def need(x,m):
 if not x:raise ValueError(m)
du=[next(j for j in range(12)if R[i][j][0])for i in range(12)]
rows=[r for r in low['branches']if r['psd']];out=[];valid=[]
for bi,r in enumerate(rows):
 cs=r['columns'];ds=[(sum(c[i]for i in G),sum(c[i]for i in range(12)if i not in G))for c in cs]
 need(ds==[(1,0),(1,6),(1,3),(1,3),(2,6),(2,6)],'formal-codegree dimensions')
 zz=[i for i,d in enumerate(ds)if d==(1,6)];need(len(zz)==1,'not unique Z')
 v=cs[zz[0]];fixed=all(v[i]==v[du[i]]for i in range(12))
 out.append({'old_psd_branch':bi,'Z_restriction_selfdual':fixed})
 if fixed:valid.append(cs)
need([r['old_psd_branch']for r in out if r['Z_restriction_selfdual']]==[1,2],'unexpected surviving indices')
need(sorted(valid[0])==sorted(valid[1]),'remaining columns not isomorphic by relabeling')
report={'status':'PASS','ring':'R12_1_623','restriction_only':True,'new_exclusion':False,'old_psd_branches':4,'new_psd_branches':2,'branches_up_to_permuting_equal_dimension_summands':1,'details':out,'optimizer_used':False}
(P/'R623_duality_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
