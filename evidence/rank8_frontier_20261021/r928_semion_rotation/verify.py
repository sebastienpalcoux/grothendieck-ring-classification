"""Fixed integer central patterns with the R928 semion-orbit moments."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,importlib.util,json,math,sys
HERE=Path(__file__).resolve().parent;FRONTIER=HERE.parent
sys.path.insert(0,str(FRONTIER/'noncommutative'))
import rotation_search as rotation,character_modular as modular,certified_lp as lp
c=rotation.c;s=c.s;need=c.require
spec=importlib.util.spec_from_file_location('quartic_pair_source',FRONTIER/'quartic_integer_center/source.py')
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)


def setup():
    rotation.install();record=source.data(928);saved=json.loads((FRONTIER/'quartic_integer_center/source.json').read_text())
    need(record==next(x for x in saved['records']if x['id']=='R8_3_928'),'complete quartic source binding')
    R=record['tensor'];a=rotation.bq.data(R);cols=a['lows'][0]
    chars=modular.characters(R,a);need(chars[0]==a['ds'],'tensor unit explicitly FP character')
    _,Q,high=rotation.bq.high_columns(a,cols)
    order=record['original_high_order']
    need([list(high[j][0])for j in order]==record['canonical_high_vectors'],'canonical/raw high indexing')
    prior=json.loads((FRONTIER/'quartic_integer_center/gram_cubic.json').read_text())
    need(prior['complete_joint_pattern_count']==343 and len(prior['patterns'])==343,'complete integer/cubic domain')
    # Every pattern forces the central g and its five low translates.
    need(record['reduced_high_vectors'][40]==[1,0,0,0],'unique central invertible g column')
    translated=[40,41,42,43,57]
    need(all(all(m[i]==1 for i in translated)for m in prior['patterns']),'complete low-translated simple multiplicities')
    indices=[i for i,m in enumerate(prior['patterns'])if all(m[j]%2==0 for j in range(40))]
    need(indices==[2,6,40,44,49,58,61,64,186,191,196,199,243,245,248],'complete semion parity domain')
    choices=rotation.h.indicator_choices(R);need(choices==[(0,0,0,0,0,0,-1),(0,0,0,0,0,0,1)],'complete raw indicator domain')
    old=json.loads((FRONTIER/'noncommutative/rotation_928_h6.json').read_text())
    positive=[case for case in old['result']['branches'][0]['systems']if case['indicators']==[0,0,0,0,0,0,1]]
    need(len(positive)==1 and positive[0]['ray']is not None,'positive pointed indicator independently excluded')
    A,b,meta=rotation.bq.system(R,a,cols,choices[1],6)
    need(positive[0]['metadata']==meta,'original positive indicator full-system replay')
    rotation.h.check_farkas(A,b,positive[0]['ray'])
    return R,a,cols,high,record,prior,indices,positive[0]


def build(data,index):
    R,a,cols,high,record,prior,indices,positive=data
    ep=(0,0,0,0,0,0,-1);A,b,old=rotation.bq.system(R,a,cols,ep,6)
    A,b,old=modular.append_sts(R,a,cols,(0,1,2,3,4),A,b,old,6)
    types,bound=rotation.bq.trace_types(6);nt=len(types);order=record['original_high_order'];counts=prior['patterns'][index]
    need(old['high_columns']==65 and nt==38,'complete height-six high/trace domain')
    for canonical,raw in enumerate(order):
        row=[0]*len(A[0]);row[raw*nt:(raw+1)*nt]=[1]*nt;A.append(row);b.append(counts[canonical])
    moments=[]
    for canonical in range(40):
        for power in(2,6):moments.append((canonical,power,0))
    for canonical in(40,41,42,43,57):
        for power,target in enumerate((0,-1,0,1,0,-1),1):moments.append((canonical,power,target))
    for canonical,power,target in moments:
        raw=order[canonical]
        for coordinate in range(4):
            coefficients=[typ[power-1][coordinate]for typ in types];constant=F(target*counts[canonical]if coordinate==0 else 0)
            den=math.lcm(constant.denominator,*(x.denominator for x in coefficients));row=[0]*len(A[0])
            for j,x in enumerate(coefficients):row[raw*nt+j]=int(x*den)
            const=int(constant*den);g=math.gcd(const,*row)or 1;A.append([x//g for x in row]);b.append(const//g)
    meta={'pattern_index':index,'fixed_canonical_high_multiplicities':counts,'height':6,'trace_types':nt,'order_bound':int(bound),
        'moment_constraints':len(moments)*4,'rows':len(A),'variables':len(A[0]),
        'matrix_sha256':hashlib.sha256(json.dumps(A,separators=(',',':')).encode()).hexdigest(),
        'rhs_sha256':hashlib.sha256(json.dumps(b,separators=(',',':')).encode()).hexdigest()}
    return A,b,meta


def semion_control():
    # Actual double-semion center Z(Vec(C2)^omega), with omega nontrivial.
    labels=list(__import__('itertools').product(range(2),repeat=2))
    S=s.Matrix([[(-1)**(a*c_+b*d)for c_,d in labels]for a,b in labels])
    twists=[s.I**a*(-s.I)**b for a,b in labels];T=s.diag(*twists)
    need(S*T*S==2*T.inv()*S*T.inv(),'actual double-semion center STS control')
    for g in(1,2):
        need(twists[g]**2==-1,'actual central semion twist')
        average=tuple(s.expand((twists[g]**k+s.conjugate(twists[g])**k)/2)for k in range(1,7))
        need(average==(0,-1,0,1,0,-1),'actual semion translated-low moments')
    return {'actual_category':'Z(Vec(C2)^omega), nontrivial omega',
            'full_STS_verified':True,'translated_low_relative_moments':[0,-1,0,1,0,-1]}


def run(write):
    control=semion_control();data=setup();path=HERE/'results.json';saved=None if write else json.loads(path.read_text());cases=[];dual_pool=[];matrix=None
    for index in data[6]:
        A,b,meta=build(data,index)
        if matrix is None:matrix=meta['matrix_sha256']
        need(matrix==meta['matrix_sha256'],'common semion fixed-pattern matrix')
        if write:
            decision=None
            for old in dual_pool:
                try:lp.verify(A,b,old);decision=old;break
                except Exception:pass
            if decision is None:decision=lp.decide(A,b)
            if decision['status']=='exact_infeasible_relaxation'and decision not in dual_pool:dual_pool.append(decision)
        else:
            need(saved['cases'][len(cases)]['metadata']==meta,'exact semion-pattern system');decision=saved['cases'][len(cases)]['decision']
        lp.verify(A,b,decision);cases.append({'metadata':meta,'decision':decision});print('R928',index,decision['status'],flush=True)
    result={'id':'R8_3_928','source_sha256':hashlib.sha256((FRONTIER/'quartic_integer_center/source.json').read_bytes()).hexdigest(),
        'orbit_prerequisite_sha256':hashlib.sha256((FRONTIER/'review/quartic_central_orbits.json').read_bytes()).hexdigest(),
        'integer_cubic_receipt_sha256':hashlib.sha256((FRONTIER/'quartic_integer_center/gram_cubic.json').read_bytes()).hexdigest(),
        'complete_integer_pattern_count':343,'complete_semion_parity_survivors':data[6],
        'positive_pointed_indicator_original_exact_dual_replayed':True,'actual_known_model_control':control,'cases':cases,
        'all_patterns_excluded':all(c['decision']['status']=='exact_infeasible_relaxation'for c in cases),
        'scope':'general-complex necessary test after the independently verified Galois-pseudo-unitary gate and forced central-semion orbit theorem; finite height-six relaxation, not a construction'}
    if write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==saved,'complete semion fixed-pattern replay')
    print('PASS R928 semion fixed-pattern domain; all excluded=',result['all_patterns_excluded'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args();run(args.write)
