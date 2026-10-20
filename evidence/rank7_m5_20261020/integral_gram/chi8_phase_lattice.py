"""Finite active phase packets followed by an exact inactive lattice quotient."""
import argparse
import hashlib
import itertools
import json
import sys
import time
from pathlib import Path

import explore as e
sys.path.insert(0,str(e.HERE.parent/'computation'))
import inactive_lattice as il
from chi8_branch_system import validate_domain


def distributions(indices,labels,count):
    indices=[j for j in indices if labels[j]['multiplicity_unit']<=count]
    answer=[]
    def visit(pos,left,items):
        if pos==len(indices):
            if left==0:answer.append(items[:])
            return
        j=indices[pos];unit=labels[j]['multiplicity_unit']
        for n in range(left//unit+1):
            if n:items.append([j,n])
            visit(pos+1,left-unit*n,items)
            if n:items.pop()
    visit(0,count,[])
    return answer


def run(path,replay=False,basis_from=None):
    start=time.monotonic();raw=path.read_bytes();system=json.loads(raw)
    ipath=e.HERE/f"R7_5_5039_chi8_active_{system['chi8_branch']}.json";iraw=ipath.read_bytes();inventory=json.loads(iraw)
    validate_domain(system,inventory)
    labels=system['phase_labels'];active_set=set(inventory['active_orbits'])
    active=[j for j,lab in enumerate(labels) if lab['orbit'] in active_set]
    inactive=[j for j in range(len(system['columns'])) if j not in active]
    acols=[system['columns'][j] for j in active];icols=[system['columns'][j] for j in inactive]
    positions={j:i for i,j in enumerate(active)}
    opath=e.HERE/(path.stem+'_phase_lattice.json')
    hashes={'system':hashlib.sha256(raw).hexdigest(),'inventory':hashlib.sha256(iraw).hexdigest()}
    if replay:
        output=json.loads(opath.read_text());il.require(output['hashes']==hashes,'input hashes')
        prepared=il.verify_prepared(output['prepared'],icols,system['rhs'],acols)
    else:
        print(json.dumps({'event':'preparing','active':len(active),'inactive':len(inactive)}),flush=True)
        basis=json.loads(basis_from.read_text())['prepared']['basis'] if basis_from else None
        prepared=il.prepare(icols,system['rhs'],acols,basis=basis)
    results=[]
    for bi,allocation in enumerate(inventory['branches']):
        choices=[distributions([j for j in active if labels[j]['orbit']==oi],labels,count) for oi,count in allocation]
        total=0;remaining=[];failures=[]
        for choice in itertools.product(*choices):
            total+=1;support=[item for packet in choice for item in packet];counts=[0]*len(active)
            for j,n in support:counts[positions[j]]=n
            success,why=il.check_counts(prepared,counts,return_failure=True)
            if success:remaining.append(support)
            else:failures.append(why)
        result={'branch':bi,'total':total,'remaining':remaining,'failures':failures};results.append(result)
        print(json.dumps({'branch':bi,'total':total,'remaining':len(remaining)}),flush=True)
    if replay:il.require(output['branches']==results,'complete finite phase enumeration')
    else:
        output={'system':path.name,'hashes':hashes,'active_columns':active,'prepared':prepared,'branches':results}
        opath.write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps({'event':'complete','seconds':time.monotonic()-start,'remaining':sum(len(r['remaining']) for r in results),'optimized_python':not __debug__}),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('file',type=Path);ap.add_argument('--replay',action='store_true');ap.add_argument('--basis-from',type=Path);args=ap.parse_args();run(args.file,args.replay,args.basis_from)
