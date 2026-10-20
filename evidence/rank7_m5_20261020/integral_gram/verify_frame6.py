"""Complete exact exclusion of R3895's distinct-codegree-16 low frame.

This does not exclude the ring: the repeated-codegree-16 frame remains open.
"""
import contextlib
import hashlib
import io
import json
import sys
import time

import explore as e
import negative_indicators
import verify_source_domains

q=e.q;HERE=e.HERE;COMPUTATION=HERE.parent/'computation'
sys.path.insert(0,str(COMPUTATION))
import check_inactive_branches
import verify_branch_lattice
import verify_integer_trees


def run():
    start=time.monotonic()
    with contextlib.redirect_stdout(io.StringIO()):
        source=verify_source_domains.run()
        negative_indicators.run()
        check_inactive_branches.main()
        verify_branch_lattice.main()
        oldargv=sys.argv;sys.argv=['verify_integer_trees.py','--frame','6']
        try:verify_integer_trees.main()
        finally:sys.argv=oldargv
    suffix='normal' if __debug__ else 'optimized'
    lattice=json.loads((COMPUTATION/('inactive_branch_replay_'+suffix+'.json')).read_text())
    trees=json.loads((COMPUTATION/('integer_trees_6_'+suffix+'.json')).read_text())
    fars=json.loads((HERE/'R7_5_3895_branch_farkas_6.json').read_text())
    allocations=json.loads((HERE/'R7_5_3895_active_6.json').read_text())['branches']
    covered=set();unresolved=set();gaps=[]
    for case in [0,2,4,6]:
        system=json.loads((HERE/('R7_5_3895_system_6_'+str(case)+'.json')).read_text())
        cols=system['columns'];active=set(system['active_variables'])
        survivors=next(r['remaining_branch_indices'] for r in lattice['results'] if r['low_index']==6 and r['case']==case)
        for bi in survivors:
            rows=[r for r in fars['results'] if (r['case'],r['branch'])==(case,bi)]
            q.require(len(rows)==1,'exact Farkas branch coverage');record=rows[0]
            rhs=[b-sum(n*cols[j][i] for j,n in allocations[bi]) for i,b in enumerate(system['rhs'])]
            keep=[j for j,c in enumerate(cols) if j not in active and all(c[i]<=rhs[i] for i in range(21))]
            q.require(record['kept_columns']==len(keep),'integer zero-variable column inventory')
            if record['separator'] is None:unresolved.add((case,bi));continue
            y=fars['separators'][record['separator']]
            q.require(len(y)==len(rhs) and all(type(x)is int for x in y),'integer Farkas covector')
            gap=-q.base.dot(rhs,y)
            q.require(gap>0 and all(q.base.dot(cols[j],y)>=0 for j in keep),'strict exact branch separation')
            covered.add((case,bi));gaps.append(gap)
    q.require(unresolved=={(r['case'],r['branch']) for r in fars['unresolved']},'remaining Farkas branch inventory')
    tree_keys={(r['case'],r['branch']) for r in trees['results']}
    q.require(unresolved==tree_keys and len(tree_keys)==16,'all remaining integer branches closed by finite trees')
    q.require(len(covered)==112,'all rationally separated branches')
    sources={}
    for path in [HERE/'R7_5_3895_domains.json',HERE/'R7_5_3895_negative_indicator_certificate.json',HERE/'R7_5_3895_branch_farkas_6.json',HERE/'R7_5_3895_active_6.json']:
        sources[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    result={'status':'PASS','id':'R7_5_3895','scope':'pseudo_unitary_low_frame_exclusion','excluded_low_index':6,
            'remaining_low_index':8,'source_sha256':source['source_sha256'],'optimized_python':not __debug__,
            'optimizer_used':False,'raw_active_allocations':20508,'positive_gram_allocations':126,
            'lattice_survivors_per_labelling':32,'exact_farkas_branches':len(covered),'integer_trees':len(tree_keys),
            'integer_tree_leaves':sum(r['leaves'] for r in trees['results']),'minimum_farkas_gap':min(gaps),
            'source_hashes':sources,'seconds':time.monotonic()-start}
    (HERE/('frame6_replay_'+suffix+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True);return result


if __name__=='__main__':run()
