#!/usr/bin/env python3
"""Independently replay accepted module exclusions without sign-gauge reduction.

The complete finite generator domains are enumerated with exact rational
reconstruction. This is a verifier of the fixed accepted receipt; it does not
select records from exploratory searches or rewrite the certificate file.
"""
import json, time
from support import OUT, load, require
import legacy_noncomm_module as legacy

def main():
    start=time.monotonic();inputs={r['id']:r for r in load()}
    data=json.loads((OUT/'noncomm_exclusions_verified.json').read_text())
    require(data['status']=='PASS' and len(data['records'])==21, 'accepted receipt inventory')
    seen=set();records=[]
    for row in data['records']:
        require(row['id'] not in seen,'duplicate ID');seen.add(row['id'])
        source=inputs[row['id']];require(source['tensor_sha256']==row['tensor_sha256'],'source tensor identity')
        c=row['certificate'];g=c['involution']
        require(c['kind']=='noncommutative_involution_module', 'accepted criterion kind')
        require(all(source['tensor'][i][j]==source['tensor'][j][i] for i in range(11) for j in range(11)) is False, 'commutativity scope')
        require(g in legacy.invs(source['tensor']),'invertible involution')
        z=legacy.solve(source['tensor'],g)
        require(z is not None and not z['feasible'],'independent search did not exclude')
        for key,value in z.items():require(c[key]==value,'stored search mismatch: '+key)
        records.append(dict(id=row['id'],status='PASS',nodes=z['nodes']))
        print(row['id'],'PASS',z['nodes'],flush=True)
    result=dict(status='PASS',exact_exclusion_count=len(records),elapsed_seconds=time.monotonic()-start,records=records)
    (OUT/'noncomm_independent_replay.json').write_text(json.dumps(result,indent=2)+'\n')
    print('COMPLETE',len(records),result['elapsed_seconds'],flush=True)

if __name__=='__main__':main()
