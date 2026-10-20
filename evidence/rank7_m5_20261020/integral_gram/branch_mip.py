"""Discovery of the remaining small active branches."""
import argparse
import json
import time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import csc_matrix
from explore import HERE


def run(low):
    info=json.loads((HERE/('R7_5_3895_branch_farkas_'+str(low)+'.json')).read_text())
    allocations=json.loads((HERE/('R7_5_3895_active_'+str(low)+'.json')).read_text())['branches']
    results=[]
    for rec in info['unresolved']:
        if rec['case']!=0:continue
        sys=json.loads((HERE/('R7_5_3895_system_'+str(low)+'_'+str(rec['case'])+'.json')).read_text())
        cols=sys['columns'];rhs=[v-sum(n*cols[j][i] for j,n in allocations[rec['branch']]) for i,v in enumerate(sys['rhs'])]
        active=set(sys['active_variables'])
        keep=[j for j,c in enumerate(cols) if j not in active and all(c[i]<=rhs[i] for i in range(21))]
        cs=[cols[j] for j in keep]
        ub=[min([rhs[i]//c[i] for i in range(21) if c[i]>0] or [np.inf]) for c in cs]
        st=time.monotonic()
        result=milp(np.ones(len(cs)),integrality=np.ones(len(cs)),bounds=Bounds(np.zeros(len(cs)),ub),constraints=LinearConstraint(csc_matrix(np.array(cs,dtype=float).T),rhs,rhs),options={'time_limit':60})
        out={**rec,'status':int(result.status),'seconds':time.monotonic()-st}
        if result.x is not None:
            x=[round(float(v)) for v in result.x]
            out['exact_feasible']=all(sum(c[i]*v for c,v in zip(cs,x))==b for i,b in enumerate(rhs))
            out['support']=[(keep[i],v) for i,v in enumerate(x) if v]
        print(json.dumps(out),flush=True);results.append(out)
        (HERE/('R7_5_3895_branch_mip_'+str(low)+'.json')).write_text(json.dumps(results,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('low',type=int,choices=[6,8]);a=p.parse_args();run(a.low)
