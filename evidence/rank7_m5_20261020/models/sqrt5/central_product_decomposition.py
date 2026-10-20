"""Integer decomposability of known low central products in a fixed witness."""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import time
import central_fusion_extension as e


def run(path,seconds):
    import numpy as np
    from scipy.optimize import milp,Bounds,LinearConstraint
    from scipy.sparse import csc_matrix
    data=e.load(path);rows=data['rows'];source=data['source'];low=data['lowcoeff']
    high=sorted(set(rows[7:]));results=[]
    for a,b in itertools.combinations_with_replacement(range(1,7),2):
        target=[sum(rows[a][i]*rows[b][j]*source[i][j][k] for i in range(7) for j in range(7))-sum(low[a][b][z]*rows[z][k] for z in range(7)) for k in range(7)]
        upper=[min([target[k]//v[k] for k in range(7) if v[k]] or [0]) for v in high]
        start=time.monotonic()
        if any(x<0 for x in target):
            result={'pair':[a,b],'status':'negative_residual','target':target}
        else:
            res=milp(np.ones(len(high)),integrality=np.ones(len(high)),bounds=Bounds(np.zeros(len(high)),upper),constraints=LinearConstraint(csc_matrix(np.array(high).T),target,target),options={'time_limit':seconds})
            result={'pair':[a,b],'status':int(res.status),'target':target,'seconds':time.monotonic()-start}
            if res.x is not None:
                coeff=[int(round(x)) for x in res.x]
                e.q.require(all(sum(c*v[k] for c,v in zip(coeff,high))==target[k] for k in range(7)),'exact nonnegative integral residual decomposition')
                result['coefficients']=coeff;result['exact_feasible']=True
        results.append(result)
        print(json.dumps(result),flush=True)
    output={'id':data['id'],'source_sha256':data['source_sha256'],'witness_sha256':data['witness_sha256'],'center_rank':len(rows),'high_distinct_rows':high,'results':results,'scope':'Necessary low tensor-product decompositions for this fixed restriction witness only.'}
    (e.HERE/(Path(path).stem+'_product_decomposition.json')).write_text(json.dumps(output,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('witness');p.add_argument('--seconds',type=float,default=5);a=p.parse_args();run(a.witness,a.seconds)
