#!/usr/bin/env python3
"""Complete 2^6 section enumeration for the forced split pointed extension.
The categorical proof excluding the nonsplit extension is in R623_central_semion.md.
"""
import itertools,json
from pathlib import Path
P=Path(__file__).resolve().parent
A=list(itertools.product(range(6),range(2)))
add=lambda a,b:((a[0]+b[0])%6,(a[1]+b[1])%2)
neg=lambda a:(-a[0]%6,a[1]);K=(0,1)
def need(x,m):
 if not x:raise ValueError(m)
frozen=json.loads((P/'audit/frozen_inputs.json').read_text())
R=frozen['tensors']['R12_1_623'];co=frozen['bindings']['R12_1_623']['quadratic_coordinates']['coordinate_to_input']
for i,j in itertools.product(range(12),repeat=2):
 a,u=i%6,i//6;b,v=j%6,j//6;row=[0]*12
 if u+v<2:row[co[(a+((-1)**u)*b)%6+6*(u+v)]]=1
 else:
  row[co[(a-b+3)%6]]=1
  for k in range(6):row[co[6+k]]=1
 need(R[co[i]][co[j]]==row,'source tensor presentation')
rows=[]
for shear in range(2):
 tau=lambda a:(-a[0]%6,(a[1]+shear*a[0])%2)
 for tb in range(2):
  t=(3,tb)
  if tau(t)!=t:
   rows.append({'shear':shear,'pointed_term':t,'excluded_by_tau_t':True});continue
  allsets=[]
  for bits in itertools.product(range(2),repeat=6):
   S={(a,b)for a,b in enumerate(bits)}
   if {tau(a)for a in S}!=S:continue
   if {neg(a)for a in S}!={add(neg(t),a)for a in S}:continue
   if any({add(add(tau(g),neg(g)),a)for a in S}!=S for g in A):continue
   normalized=S if (0,0)in S else{add(K,a)for a in S}
   need((0,0)in normalized and all(add(a,b)in normalized for a in normalized for b in normalized),'survivor not subgroup up to kernel gauge')
   need(t in normalized,'pointed term not in subgroup')
   allsets.append({'bits':bits,'subgroup_after_kernel_gauge':sorted(normalized)})
  need(len(allsets)==2,'unexpected section count')
  rows.append({'shear':shear,'pointed_term':t,'sections_examined':64,'surviving_sections':allsets})
report={'status':'PASS','ring':'R12_1_623','new_exclusion':False,'proved_restriction':'inner C2 equivariantization has only subgroup sections up to kernel gauge; central semion lift follows by separate categorical lemma','cases':rows,'optimizer_used':False,'parent_repository_imports':False}
(P/'R623_C2_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='cases'}))
