"""Independent algebra/module/full-Hom check of all92 conditional GT cases."""
from itertools import product
import json,time
import numpy as np
from audit_liptrap import HERE,FIRST,need
from generic_group_hom import audit

def main():
    start=time.monotonic();source=json.loads((HERE/'d48_gt_frozen.json').read_text());groups=source['groups'];cocycles=source['cocycles'];targets=json.loads((FIRST/'tensors.json').read_text());out=[]
    for key,W0 in cocycles.items():
        G=np.array(groups[key.split(':')[0]],dtype=int);W=np.array(W0,dtype=int);n=len(G)
        need(not np.any(W[0]) and not np.any(W[:,0]) and not np.any(W[:,:,0]),'normalized3cocycle')
        b=np.arange(n)[:,None,None];c=np.arange(n)[None,:,None];d=np.arange(n)[None,None,:]
        for a in range(n):need(not np.any((W[b,c,d]-W[G[a,b],c,d]+W[a,G[b,c],d]-W[a,b,G[c,d]]+W[a,b,c])%8),'all source3cocycle equations')
    for case in source['cases']:
        G=groups[case['group_key']];W=cocycles[case['omega_key']];H=case['subgroup'];psi=case['psi'];hi={a:i for i,a in enumerate(H)};q=case['modulus'];w=lambda a,b,c:W[a][b][c]
        need(q==8,'actual phase field');need(all(psi[0][a]==psi[a][0]==0 for a in range(len(H))),'normalized subgroup cochain')
        need(all((psi[hi[b]][hi[c]]-psi[hi[G[a][b]]][hi[c]]+psi[hi[a]][hi[G[b][c]]]-psi[hi[a]][hi[b]]+w(a,b,c))%q==0 for a,b,c in product(H,repeat=3)),'actual algebra delta_psi+omega=0')
        row=dict(group_table=G,subgroup=H,info=dict(objects=case['objects']),model_tensor=case['model_tensor'],matched_source=targets.get(case['matched_source']),source_to_model=case['source_to_model'])
        positive=case['model_tensor'] is not None;coefficient=case['coefficient_witness']
        ans=audit(row,w,q,psi,coefficient,positive)
        dims=sorted(len(o['support'])*o['fiber_dimension']//len(H) for o in case['objects']);need(dims==case['dimensions'],'recorded dimensions')
        if positive:
            need(case['matched_source'] in targets,'actual physical input binding');ans['matched_id']=case['matched_source']
        elif coefficient:ans['nonmultiplicityfree_witness']=coefficient
        else:need(len(case['objects'])!=12,'wrong-rank category');ans['wrong_rank']=len(case['objects'])
        ans['case']=case['case'];out.append(ans)
    counts=dict(positive=sum('matched_id'in r for r in out),nonmultiplicityfree=sum('nonmultiplicityfree_witness'in r for r in out),wrong_rank=sum('wrong_rank'in r for r in out))
    need(counts==dict(positive=40,nonmultiplicityfree=16,wrong_rank=36),'complete92case accounting')
    result=dict(status='PASS',scope='Conditional group-theoretical list only; no universal GT premise inferred',source_cocycles=len(cocycles),cases=len(out),counts=counts,records=out,seconds=time.monotonic()-start)
    (HERE/'d48_catalog_independent.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='records'})

if __name__=='__main__':main()
