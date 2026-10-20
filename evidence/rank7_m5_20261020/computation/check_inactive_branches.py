"""Replay inactive-lattice tests against the exported finite active branches."""
import collections,hashlib,json,time
from pathlib import Path
from inactive_lattice import verify_prepared,check_counts,require
HERE=Path(__file__).resolve().parent;INPUT=HERE.parent/'integral_gram'


def main():
    start=time.monotonic();results=[];sources={}
    for frame in (6,8):
        branch_path=INPUT/f'R7_5_3895_active_{frame}.json';branches=json.loads(branch_path.read_text())
        sources[str(branch_path.relative_to(HERE.parents[2]))]=hashlib.sha256(branch_path.read_bytes()).hexdigest()
        for case in (0,2,4,6):
            path=HERE/f'R7_5_3895_inactive_lattice_{frame}_{case}.json';record=json.loads(path.read_text())
            system_path=INPUT/f'R7_5_3895_system_{frame}_{case}.json';raw=system_path.read_bytes();system=json.loads(raw)
            require(hashlib.sha256(raw).hexdigest()==record['source_sha256'],'system binding')
            if case==0:require(record['source_sha256']==branches['system_sha256'],'active enumeration binding')
            active=system['active_variables'];active_set=set(active)
            inactive=[col for i,col in enumerate(system['columns']) if i not in active_set]
            cols=[system['columns'][i] for i in active]
            prepared=verify_prepared(record['prepared'],inactive,system['rhs'],cols)
            failures=collections.Counter();remaining=[];witnesses=[]
            for ix,branch in enumerate(branches['branches']):
                counts=dict(branch)
                require(len(counts)==len(branch) and all(i in active_set and type(c)is int and c>0 for i,c in counts.items()),'active count domain')
                require(sum(int(system['active_weights'][str(i)])*c for i,c in counts.items())==system['active_budget'],'active budget')
                okay,why=check_counts(prepared,[counts.get(i,0) for i in active],return_failure=True)
                if okay:remaining.append(ix)
                else:failures[why['test']]+=1;witnesses.append({'branch':ix,**why})
            results.append({'low_index':frame,'case':case,'input_branches':len(branches['branches']),
                            'remaining_branch_indices':remaining,'rejected_by_test':dict(failures),'witnesses':witnesses})
            for source in (path,system_path):sources[str(source.relative_to(HERE.parents[2]))]=hashlib.sha256(source.read_bytes()).hexdigest()
            print(json.dumps({k:v for k,v in results[-1].items() if k!='witnesses'}),flush=True)
    output={'status':'PASS','scope':'Exact lattice exclusion of recorded active branches only; completeness and system derivation are separately checked.',
            'optimized_python':not __debug__,'source_hashes':sources,'results':results,'seconds':time.monotonic()-start}
    target=HERE/('inactive_branch_replay_optimized.json' if not __debug__ else 'inactive_branch_replay_normal.json')
    target.write_text(json.dumps(output,indent=2)+'\n')


if __name__=='__main__':main()
