"""Exact rational separators for the finite active-row branches."""
import argparse
import hashlib
import json
import time

import explore as e
q=e.q;HERE=e.HERE


def run(low):
    lattice=json.loads((HERE.parent/'computation/inactive_branch_replay_normal.json').read_text())
    allocations=json.loads((HERE/('R7_5_3895_active_'+str(low)+'.json')).read_text())['branches']
    pool=[];results=[];unresolved=[];start=time.monotonic()
    for case in [0,2,4,6]:
        path=HERE/('R7_5_3895_system_'+str(low)+'_'+str(case)+'.json')
        sys=json.loads(path.read_text());active=set(sys['active_variables']);cols=sys['columns'];b=sys['rhs']
        surviving=next(r['remaining_branch_indices'] for r in lattice['results'] if r['low_index']==low and r['case']==case)
        for bi in surviving:
            chosen=allocations[bi]
            rhs=[v-sum(n*cols[j][i] for j,n in chosen) for i,v in enumerate(b)]
            keep=[j for j,c in enumerate(cols) if j not in active and all(c[i]<=rhs[i] for i in range(21))]
            remaining=[cols[j] for j in keep]
            sep=q.separate(remaining,rhs,pool)
            rec={'case':case,'branch':bi,'separator':sep,'kept_columns':len(keep)}
            results.append(rec)
            if sep is None:unresolved.append({'case':case,'branch':bi})
            print(json.dumps({'event':'branch',**rec,'pool':len(pool),'unresolved':len(unresolved),'seconds':time.monotonic()-start}),flush=True)
            out={'id':'R7_5_3895','low_index':low,'results':results,'separators':pool,'unresolved':unresolved}
            (HERE/('R7_5_3895_branch_farkas_'+str(low)+'.json')).write_text(json.dumps(out,indent=2)+'\n')
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('low',type=int,choices=[6,8]);a=p.parse_args();run(a.low)
