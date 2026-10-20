"""Exact replay of branch-specific Gram exclusions and lattice tests."""
import hashlib,json,time
from pathlib import Path
from inactive_lattice import require,verify_prepared,check_counts
from branch_lattice import matrix
HERE=Path(__file__).resolve().parent;INPUT=HERE.parent/'integral_gram'


def main():
    start=time.monotonic();results=[];hashes={}
    initial=json.loads((HERE/'inactive_branch_replay_normal.json').read_text())['results']
    for frame in (6,8):
        path=HERE/f'R7_5_3895_branch_lattice_{frame}.json';raw=path.read_bytes();record=json.loads(raw)
        require(record['status']=='complete','incomplete branch inventory')
        hashes[path.name]=hashlib.sha256(raw).hexdigest()
        expected=sorted(set(i for r in initial if r['low_index']==frame for i in r['remaining_branch_indices']))
        require([r['index'] for r in record['branches']]==expected,'incomplete initial branch coverage')
        branches_path=INPUT/f'R7_5_3895_active_{frame}.json';branches=json.loads(branches_path.read_text())['branches']
        systems={case:json.loads((INPUT/f'R7_5_3895_system_{frame}_{case}.json').read_text()) for case in (0,2,4,6)}
        for case in systems:
            source=INPUT/f'R7_5_3895_system_{frame}_{case}.json';hashes[source.name]=hashlib.sha256(source.read_bytes()).hexdigest()
        hashes[branches_path.name]=hashlib.sha256(branches_path.read_bytes()).hexdigest()
        source=systems[0];active=set(source['active_variables']);inactive=set(range(len(source['columns'])))-active
        survivors={case:[] for case in systems};pruned=0
        for item in record['branches']:
            ix=item['index'];require(item['active_counts']==branches[ix],'active count binding')
            counts=dict(item['active_counts']);residual=[b-sum(source['columns'][j][i]*c for j,c in counts.items()) for i,b in enumerate(source['rhs'])]
            kept=item['kept_columns'];excluded=item['excluded_columns'];discarded=[r['column'] for r in excluded]
            require(len(set(kept))==len(kept) and len(set(discarded))==len(discarded) and not set(kept)&set(discarded) and set(kept)|set(discarded)==inactive,'inactive partition')
            for witness in excluded:
                col=source['columns'][witness['column']]
                if 'entry' in witness:
                    i=witness['entry'];require(type(i)is int and 0<=i<21 and col[i]>residual[i],'false component bound')
                else:
                    v=witness['negative_vector'];require(len(v)==6 and all(type(x)is int for x in v),'integer quadratic witness')
                    M=matrix([b-c for b,c in zip(residual[:21],col[:21])])
                    require(sum(v[i]*M[i][j]*v[j] for i in range(6) for j in range(6))<0,'false PSD exclusion')
                pruned+=1
            require([r['case'] for r in item['cases']]==[0,2,4,6],'case coverage')
            for check in item['cases']:
                case=check['case'];system=systems[case]
                require([c[:21] for c in system['columns']]==[c[:21] for c in source['columns']],'shared Gram columns')
                rhs=[b-sum(system['columns'][j][i]*c for j,c in counts.items()) for i,b in enumerate(system['rhs'])]
                prepared=verify_prepared(check['prepared'],[system['columns'][j] for j in kept],rhs,[])
                actual,why=check_counts(prepared,[],return_failure=True)
                require(actual==check['lattice_pass'] and why==check['failure'],'lattice outcome')
                if actual:survivors[case].append(ix)
        results.append({'frame':frame,'branches':len(record['branches']),'exact_column_exclusions':pruned,'lattice_survivors':survivors})
    output={'status':'PASS','scope':'Conditional exact Gram/lattice pruning; no complete ring exclusion.',
            'optimized_python':not __debug__,'source_hashes':hashes,'results':results,'seconds':time.monotonic()-start}
    target=HERE/('branch_lattice_replay_optimized.json' if not __debug__ else 'branch_lattice_replay_normal.json')
    target.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))


if __name__=='__main__':main()
