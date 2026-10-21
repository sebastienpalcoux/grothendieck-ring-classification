"""Complete fixed-pattern height-six fermionic moment and STS test for R941."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,math,sys
import source,r941_fermionic
HERE=Path(__file__).resolve().parent;FRONTIER=HERE.parent
sys.path.insert(0,str(FRONTIER/'noncommutative'))
import rotation_search as rotation,character_modular as modular,certified_lp as lp
need=source.need

def setup():
    branch=json.loads(json.dumps(r941_fermionic.run(),default=int))
    need(branch==json.loads((HERE/'r941_fermionic.json').read_text()),'fermionic branch replay')
    row=source.data(941);R=row['tensor'];rotation.install();a=rotation.bq.data(R);cols=a['lows'][0]
    chars=modular.characters(R,a);need(chars[0]==a['ds'],'FP tensor unit character')
    assignments=modular.assignments(a,chars,cols);need(assignments==[(0,1,2,3,4)],'complete S assignment')
    high=rotation.bq.high_columns(a,cols)[2];order=row['original_high_order']
    need([list(high[j][0])for j in order]==row['canonical_high_vectors'],'raw high column binding')
    ep=(0,0,1,1,1,1,1);prior=json.loads((FRONTIER/'noncommutative/modular_941_h6.json').read_text())
    choices=rotation.h.indicator_choices(R)
    # The original complete tensor-rotation receipt excludes every other indicator.
    old=json.loads((FRONTIER/'noncommutative/rotation_941_h6.json').read_text())
    systems=old['result']['branches'][0]['systems']
    need([v['indicators']for v in systems]==list(map(list,choices)),'original complete indicator domain')
    for candidate,case in zip(choices,systems):
        if candidate==ep:continue
        A0,b0,meta0=rotation.bq.system(R,a,cols,candidate,6)
        need(meta0==case['metadata']and case['ray']is not None,'all other indicators excluded')
        rotation.h.check_farkas(A0,b0,case['ray'])
    need(ep in choices,'retained positive pointed indicator')
    A,b,meta=rotation.bq.system(R,a,cols,ep,6)
    A,b,meta=modular.append_sts(R,a,cols,(0,1,2,3,4),A,b,meta,6)
    types,bound=rotation.bq.trace_types(6);nt=len(types);need(nt==38 and len(high)==65,'complete trace/high domain')
    count_start=len(A)
    for canonical,raw in enumerate(order):
        v=[0]*len(A[0]);v[raw*nt:(raw+1)*nt]=[1]*nt;A.append(v);b.append(0)
    for tr in branch['fermionic_branch']['translated_low_twists']:
        raw=order[tr['high_index']]
        for power,target in enumerate(tr['moments_1_through_6'],1):
            for coordinate in range(4):
                coeff=[typ[power-1][coordinate]for typ in types];constant=F(target if coordinate==0 else 0)
                den=math.lcm(constant.denominator,*(x.denominator for x in coeff));v=[0]*len(A[0])
                for j,x in enumerate(coeff):v[raw*nt+j]=int(x*den)
                constant=int(constant*den);g=math.gcd(constant,*v)or 1
                A.append([x//g for x in v]);b.append(constant//g)
    grams=json.loads((HERE/'gram_cubic.json').read_text());need(len(grams['patterns'])==343,'complete integer pattern domain')
    return A,b,count_start,grams,{'height':6,'trace_types':nt,'order_bound':int(bound),'rows':len(A),
        'variables':len(A[0]),'matrix_sha256':hashlib.sha256(json.dumps(A,separators=(',',':')).encode()).hexdigest(),
        'tensor_sha256':row['tensor_sha256'],'indicators':list(ep),'S_assignment':[0,1,2,3,4]},branch

def run(write):
    A,b,start,grams,meta,branch=setup();path=HERE/'r941_rotation.json';saved=None if write else json.loads(path.read_text())
    cases=[];pool=[];verified_rays=set()
    for index,m in enumerate(grams['patterns']):
        rhs=list(b);rhs[start:start+65]=m
        if write:
            decision=None
            for old in pool:
                if sum(v*y for v,y in zip(rhs,old['ray']))<0:decision=old;break
            if decision is None:decision=lp.decide(A,rhs)
            if decision['status']=='exact_infeasible_relaxation'and decision not in pool:pool.append(decision)
        else:
            need(saved['cases'][index]['pattern_index']==index and saved['cases'][index]['multiplicities']==m,'complete fixed pattern coverage')
            decision=saved['cases'][index]['decision']
        need(decision['status']in('exact_feasible_relaxation','exact_infeasible_relaxation'),'incomplete numerical decision')
        if decision['status']=='exact_infeasible_relaxation':
            ray=tuple(decision['ray'])
            if ray not in verified_rays:lp.verify(A,rhs,decision);verified_rays.add(ray)
            else:need(len(ray)==len(rhs)and sum(v*y for v,y in zip(rhs,ray))<0,'cached common-matrix ray exact RHS')
        else:lp.verify(A,rhs,decision)
        cases.append({'pattern_index':index,'multiplicities':m,'decision':decision})
        if write and(index%20==0 or index==342):print('941',index,decision['status'],'dual pool',len(pool),flush=True)
    result={'id':'R8_3_941','kind':'complete_fermionic_fixed_integer_pattern_rotation_STS',
        'source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),
        'gram_sha256':hashlib.sha256((HERE/'gram_cubic.json').read_bytes()).hexdigest(),
        'fermionic_branch_sha256':hashlib.sha256((HERE/'r941_fermionic.json').read_bytes()).hexdigest(),
        'metadata':meta,'complete_pattern_count':343,'cases':cases,
        'exact_excluded_pattern_count':sum(c['decision']['status']=='exact_infeasible_relaxation'for c in cases),
        'exact_feasible_pattern_count':sum(c['decision']['status']=='exact_feasible_relaxation'for c in cases),
        'scope':'complete finite height-six necessary systems after forced central fermion; no superfusion or associator construction'}
    if write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==saved,'complete fermionic rotation replay differs')
    print('PASS941 complete343 patterns:',result['exact_excluded_pattern_count'],'excluded;',result['exact_feasible_pattern_count'],'exact feasible.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args();run(args.write)
