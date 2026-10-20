"""Source-bound exact Gram packet pruning after finite chi8 phase branching."""
import argparse
import hashlib
import json
from pathlib import Path
import explore as e


def build(system,phase_inventory,support):
    N=next(r['tensor'] for r in json.loads((e.q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==system['id'])
    e.q.require(e.q.tensor_hash(N)==system['source_sha256'],'canonical source identity')
    d,D,B,zs,T,signs=e.q.source_data(N,system['id'])
    low=system['low'];pairs=e.q.base.PAIRS
    bound=[B[i+1][j+1]-sum(v[i+1]*v[j+1] for v in low) for i,j in pairs]
    index={tuple(sorted(pair)):j for j,pair in enumerate(pairs)}
    labels=system['phase_labels']
    def gram(j):
        lab=labels[j]
        return [lab['multiplicity_unit']*sum(r[1][i] for r in system['orbits'][lab['orbit']]) for i in range(21)]
    def psd(v):
        return e.q.base.psd([[v[index[tuple(sorted((i,j)))]] for j in range(6)] for i in range(6)])
    residual=[a-sum(n*gram(j)[i] for j,n in support) for i,a in enumerate(bound)]
    e.q.require(min(residual)>=0 and psd(residual),'fixed packets fit source Gram')
    active=set(phase_inventory['active_columns']);kept=[];removed=[]
    for j in range(len(system['columns'])):
        if j in active:continue
        if j<len(labels):
            rest=[a-b for a,b in zip(residual,gram(j))]
            if min(rest)<0 or not psd(rest):removed.append(j);continue
        kept.append(j)
    rhs=[a-sum(n*system['columns'][j][i] for j,n in support) for i,a in enumerate(system['rhs'])]
    return kept,removed,rhs


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('system',type=Path);ap.add_argument('--replay',action='store_true');ap.add_argument('--no-legacy',action='store_true');a=ap.parse_args()
    raw=a.system.read_bytes();system=json.loads(raw)
    path=e.HERE/(a.system.stem+'_phase_lattice.json');praw=path.read_bytes();inventory=json.loads(praw)
    hashes={'system':hashlib.sha256(raw).hexdigest(),'phase_lattice':hashlib.sha256(praw).hexdigest()}
    e.q.require(inventory['hashes']['system']==hashes['system'],'phase inventory source binding')
    results=[]
    for bi,branch in enumerate(inventory['branches']):
        for ix,support in enumerate(branch['remaining']):
            kept,removed,rhs=build(system,inventory,support)
            results.append({'branch':bi,'phase_case':ix,'support':support,'kept':kept,'removed':removed})
    output={'hashes':hashes,'branches':results,'scope':'Exact integer packet pruning only; no whole-ring exclusion.'}
    target=e.HERE/(a.system.stem.replace('_system','')+'_phase_gram_certificate.json')
    if a.replay:e.q.require(json.loads(target.read_text())==output,'exact Gram pruning replay')
    else:
        target.write_text(json.dumps(output,separators=(',',':'))+'\n')
        if not a.no_legacy:
            legacy=e.HERE/(a.system.stem.replace('_system','')+'_phase_gram.json')
            legacy.write_text(json.dumps(results,separators=(',',':'))+'\n')
    print(json.dumps({'status':'PASS' if a.replay else 'COMPLETE','cases':len(results),
                      'kept_columns':[len(r['kept']) for r in results],'optimized_python':not __debug__}),flush=True)


if __name__=='__main__':main()
