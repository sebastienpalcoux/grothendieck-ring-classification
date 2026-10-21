"""R928 correlated semion-pair trace strengthening, exact read-only default."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
import verify as base
need=base.need;HERE=Path(__file__).resolve().parent;FRONTIER=HERE.parent


def setup():
    data=base.setup();prior=json.loads((HERE/'results.json').read_text())
    need([r['metadata']['pattern_index']for r in prior['cases']]==data[6],'complete original fifteen-pattern campaign')
    need(all(r['decision']['status']in('exact_infeasible_relaxation','exact_feasible_relaxation')for r in prior['cases']),'every original branch exactly certified')
    types,_=base.rotation.bq.trace_types(6)
    receipt=json.loads((FRONTIER/'review/semion_pair_traces.json').read_text())
    pairtypes=[tuple(tuple(map(F,row))for row in typ)for typ in receipt['pair_trace_types']]
    need(len(pairtypes)==30 and receipt['root_order_box']==288,'complete correlated pair domain')
    matches=[]
    for typ in pairtypes:
        found=[(i,j)for i,u in enumerate(types)for j,v in enumerate(types)if i<=j and tuple(tuple(x+y for x,y in zip(a,b))for a,b in zip(u,v))==typ]
        need(bool(found),'each correlated pair is an exact sum of linked old traces');matches.append(found[0])
    return data,prior,pairtypes,matches


def build(loaded,index):
    data,prior,pairtypes,matches=loaded
    A,b,old=base.build(data,index);nt=38
    raw_to_canonical={raw:canonical for canonical,raw in enumerate(data[4]['original_high_order'])}
    groups=[]
    for raw in range(65):
        if raw_to_canonical[raw]<40:groups.extend((raw*nt+i,raw*nt+j)for i,j in matches)
        else:groups.extend((raw*nt+i,)for i in range(nt))
    groups.extend((i,)for i in range(65*nt,len(A[0])))
    newA=[[sum(row[j]for j in group)for group in groups]for row in A]
    meta={'pattern_index':index,'fixed_canonical_high_multiplicities':old['fixed_canonical_high_multiplicities'],
          'height':6,'pair_trace_types':30,'ordinary_trace_types':38,'order_bound':288,
          'paired_canonical_columns':list(range(40)),'pair_type_old_trace_summands':[list(v)for v in matches],
          'rows':len(newA),'variables':len(groups),'old_variables':len(A[0]),
          'matrix_sha256':hashlib.sha256(json.dumps(newA,separators=(',',':')).encode()).hexdigest(),
          'rhs_sha256':hashlib.sha256(json.dumps(b,separators=(',',':')).encode()).hexdigest()}
    need(len(groups)==2227,'pair columns and unchanged auxiliary block counted once')
    return newA,b,meta


def run(write):
    loaded=setup();data,prior,types,matches=loaded;path=HERE/'pair_rotation.json'
    saved=None if write else json.loads(path.read_text());cases=[];pool=[];matrix=None
    for previous in prior['cases']:
        index=previous['metadata']['pattern_index']
        if previous['decision']['status']=='exact_infeasible_relaxation':continue
        A,b,meta=build(loaded,index)
        need(matrix is None or meta['matrix_sha256']==matrix,'one common pair matrix');matrix=meta['matrix_sha256']
        if write:
            decision=None
            for old in pool:
                # A^T y was checked exactly upon insertion; only the RHS changes.
                if sum(x*y for x,y in zip(b,old['ray']))<0:decision=old;break
            if decision is None:
                decision=base.lp.decide(A,b)
                if decision['status']=='exact_infeasible_relaxation':pool.append(decision)
        else:
            need(meta==saved['cases'][len(cases)]['metadata'],'complete exact pair system binding')
            decision=saved['cases'][len(cases)]['decision']
        base.lp.verify(A,b,decision)
        need(decision['status']in('exact_infeasible_relaxation','exact_feasible_relaxation'),'exact certificate required for completed pair branch')
        cases.append({'metadata':meta,'decision':decision});print('R928 correlated pairs',index,decision['status'],flush=True)
    receipt={'id':'R8_3_928','prior_semion_pattern_count':15,
        'prior_exact_infeasible_indices':[x['metadata']['pattern_index']for x in prior['cases']if x['decision']['status']=='exact_infeasible_relaxation'],
        'complete_remaining_indices':[x['metadata']['pattern_index']for x in prior['cases']if x['decision']['status']=='exact_feasible_relaxation'],
        'dependencies_sha256':{str(p.relative_to(FRONTIER)):hashlib.sha256(p.read_bytes()).hexdigest()for p in[
            HERE/'verify.py',HERE/'results.json',FRONTIER/'review/semion_pair_traces.py',FRONTIER/'review/semion_pair_traces.json',
            FRONTIER/'review/verify_quartic_central_orbits.py',FRONTIER/'review/quartic_central_orbits.json']},
        'cases':cases,'all_patterns_excluded':all(x['decision']['status']=='exact_infeasible_relaxation'for x in cases),
        'scope':'general-complex necessary test after verified Galois-pseudo-unitary and central-semion gates; complete correlated-pair height-six domain, not a construction'}
    if write:path.write_text(json.dumps(receipt,indent=2)+'\n')
    else:need(receipt==saved,'complete pair campaign replay')
    print('PASS R928 correlated semion-pair campaign; all excluded=',receipt['all_patterns_excluded'],flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');run(p.parse_args().write)
