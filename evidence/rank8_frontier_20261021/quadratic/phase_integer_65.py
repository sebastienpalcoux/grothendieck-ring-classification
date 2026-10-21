"""Finite exact-cut campaign joining R65 integer and phase constraints."""
from pathlib import Path
from types import SimpleNamespace
from fractions import Fraction as Q
import argparse,gzip,hashlib,json,pickle,sys,time
HERE=Path(__file__).resolve().parent;STAGE=HERE.parent
for directory in('commutative_integer','quadratic_atomic_integer'):
    sys.path.insert(0,str(STAGE/directory))
from features import st,require,check_integer
from exact import VerificationError
import bounds as box
import equations,linear,lattice
from proposal import propose_bounded
from unit_pair_constraints import append_unit_pair_constraints,lift_witness
from joint_atomic_integer import construct
from atomic_cm_real_sts import AtomicCMRealSTS
from atomic_spectrum import table_for
from pure_pointed_bounds import tighten_pure_bounds
from integer_phase_cuts import specialize,make_cut,append_cut
import phase_mass


def initial(checkpoint=False):
    if checkpoint:
        with gzip.open('/tmp/joint_atomic65.pkl.gz','rb')as f:source,support,S=pickle.load(f)
    else:source,support,S=construct(65)
    C=AtomicCMRealSTS(source['tensor'],4);T=table_for(C.R,C.a)
    frozen=json.loads((STAGE/'global_induction/complete_results/R8_3_65_cm_real_sts_h4.json').read_text())
    require(frozen['metadata']==C.meta and frozen['tensor_sha256']==source['tensor_sha256'],'frozen CM domain differs')
    choices=list(map(list,st.old.ht.indicator_choices(C.R)));require(choices,'empty indicator domain')
    saved=json.loads((HERE/'joint_atomic_integer_65_results.json').read_text())
    require(saved['system_metadata']==st.encode(S.metadata),'original integer metadata differs')
    x=saved['original_integer_witness'];check_integer(S,x)
    bounded=tighten_pure_bounds(S,C.R,T);check_integer(bounded,x)
    strong=append_unit_pair_constraints(bounded,C,T);x=lift_witness(bounded,strong,x)
    return source,support,C,strong,x,choices


def uniform_cut(C,S,choices,y):
    rhs_values=[sum(a*b for a,b in zip(y,C.rhs_for(ep)))for ep in choices]
    ep=choices[rhs_values.index(max(rhs_values))]
    co,b,report=make_cut(C,S,ep,y)
    require(b==max(rhs_values),'uniform cut scaling differs')
    report={**report,'covered_indicator_branches':choices,'all_indicator_rhs':rhs_values,
            'uniform_maximum_rhs':b}
    return co,b,report


def integer_rounding(co,b,report,divisor):
    require(isinstance(divisor,int)and divisor>0,'invalid integer cut divisor')
    rounded=tuple(a//divisor for a in co);target=b//divisor
    report={**report,'integer_rounding_divisor':divisor,
            'rounded_coefficients_sha256':st.digest(rounded),'rounded_rhs':target,
            'rounding_scope':'componentwise floor valid for nonnegative integer variables'}
    return rounded,target,report


def pins():
    paths=[HERE/name for name in('phase_integer_65.py','joint_atomic_integer.py','integer_phase_cuts.py','pure_pointed_bounds.py','atomic_cm_real_sts.py')]
    paths += [STAGE/'commutative_integer'/name for name in('features.py','bounds.py','equations.py','linear.py','lattice.py','phase_mass.py')]
    paths += [STAGE/'quadratic_atomic_integer'/name for name in('unit_pair_constraints.py','proposal.py')]
    paths += [HERE/'joint_atomic_integer_65_results.json']
    return {str(p.relative_to(STAGE)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');p.add_argument('--checkpoint',action='store_true');p.add_argument('--seconds',type=int,default=180);p.add_argument('--wall-seconds',type=int,default=1800);a=p.parse_args()
    require(not a.checkpoint or a.write,'checkpoint is discovery-only')
    require(a.wall_seconds>0,'positive total wall budget required');deadline=time.monotonic()+a.wall_seconds
    source,support,C,S,x,choices=initial(a.checkpoint);path=HERE/'phase_integer_65_results.json'
    if a.write:
        out={'id':source['id'],'tensor_sha256':source['tensor_sha256'],'kind':'bounded_integer_cubic_joint_spectrum_global_phase_cut_campaign',
             'source_sha256':pins(),'initial_metadata':S.metadata,'support_sha256':st.digest(support),
             'indicator_branches':choices,'maximum_global_cuts':10,'total_wall_budget_seconds':a.wall_seconds,'initial_integer_witness':x,'rounds':[],
             'status':'running','scope':'necessary pseudo-unitary system; each cut uses the maximum RHS over every allowed indicator branch'}
        def save():path.write_text(json.dumps(st.encode(out),separators=(',',':'))+'\n')
        save()
        for step in range(11):
            remaining=deadline-time.monotonic()
            if remaining<30:
                out['status']='wall_budget_completed_without_compatible_witness';break
            print('65 phase-cut round',step,'integer variables',len(S.columns),flush=True)
            check_integer(S,x);D=specialize(C,S,x)
            phase=phase_mass.discover(D,seconds=max(1,min(120,int(remaining))))
            round={'integer_witness':x,'phase':phase};out['rounds'].append(round);save()
            if phase['status']=='exact_integer_and_phase_compatible':
                phase_mass.verify(D,phase);out['status']='exact_integer_and_phase_compatible';out['final_integer_witness']=x;break
            if phase['status']!='selected_integer_pattern_phase_incompatible':out['status']='phase_reconstruction_inconclusive';break
            phase_mass.verify(D,phase)
            if step==10:out['status']='ten_global_cuts_completed_no_compatible_integer_witness';break
            require([r['indicators']for r in phase['attempts']]==choices,'incomplete all-indicator phase obstruction')
            found=None;seen=set()
            for attempt in phase['attempts']:
                ray=attempt['certificate']['covector'][:C.nrows]
                if tuple(ray)in seen:continue
                seen.add(tuple(ray))
                co,b,report=uniform_cut(C,S,choices,ray)
                maximum=max(abs(b),*map(abs,co))
                for magnitude in(100,1000,10000,1000000,1000000000,1000000000000,maximum):
                    divisor=max(1,(maximum+magnitude-1)//magnitude)
                    rounded,target,rounded_report=integer_rounding(co,b,report,divisor)
                    violation=sum(v*z for v,z in zip(rounded,x))-target
                    if violation>0:found=(rounded,target,rounded_report,violation);break
                if found:break
            if found is None:out['status']='all_indicator_pattern_rejected_without_uniform_global_cut';break
            co,b,report,violation=found
            round.update(cut=report,originating_pattern_exact_violation=violation)
            S=append_cut(S,co,b,report);round['augmented_metadata']=S.metadata
            round['box']=box.propagate(S);save()
            if round['box']['outcome']=='integer_box_obstruction':out['status']='exact_integer_box_obstruction';break
            reduced=box.reduced(S,round['box']);compact=equations.compact(reduced);round['compressed_metadata']=compact.metadata
            round['linear']=linear.discover(compact);save()
            if round['linear']['conclusion']=='exact_bounded_linear_obstruction':out['status']='exact_bounded_linear_obstruction';break
            remaining=deadline-time.monotonic()
            if remaining<30:out['status']='wall_budget_completed_without_compatible_witness';break
            round['proposal']=propose_bounded(compact,max(1,min(a.seconds,int(remaining)-20)),check_integer);save()
            if round['proposal']['conclusion']!='exact_integer_feasible_relaxation':
                round['modular']=[lattice.modular(compact,p)for p in(2,3)]
                out['status']='exact_modular_obstruction'if any(r['outcome']=='modular_obstruction'for r in round['modular'])else'integer_search_inconclusive_after_exact_global_cuts'
                break
            x=box.lift(S,round['box'],round['proposal']['integer_values']);check_integer(S,x)
        out['final_metadata']=S.metadata;out['global_cut_count']=sum('cut'in r for r in out['rounds']);save()
    else:
        out=json.loads(path.read_text());require(out['source_sha256']==pins(),'global-cut source inventory differs')
        require(out['tensor_sha256']==source['tensor_sha256']and out['initial_metadata']==st.encode(S.metadata)and out['support_sha256']==st.digest(support),'initial strengthened domain differs')
        require(out['initial_integer_witness']==x and out['indicator_branches']==choices,'initial witness or indicators differ')
        for k,round in enumerate(out['rounds']):
            require(round['integer_witness']==x,'integer witness chain differs');check_integer(S,x)
            D=specialize(C,S,x);phase=round['phase']
            if phase['status']in('exact_integer_and_phase_compatible','selected_integer_pattern_phase_incompatible'):phase_mass.verify(D,phase)
            else:require(out['status']=='phase_reconstruction_inconclusive'and k+1==len(out['rounds']),'uncertified phase status promoted')
            if 'cut'not in round:continue
            co,b,report=uniform_cut(C,S,choices,round['cut']['base_covector'])
            co,b,report=integer_rounding(co,b,report,round['cut']['integer_rounding_divisor'])
            require(st.encode(report)==round['cut'],'complete global integer cut differs')
            require(sum(v*z for v,z in zip(co,x))-b==round['originating_pattern_exact_violation']>0,'originating witness not rejected')
            S=append_cut(S,co,b,report);require(S.metadata==round['augmented_metadata'],'global cut matrix differs')
            box.verify(S,round['box'])
            if round['box']['outcome']=='integer_box_obstruction':continue
            compact=equations.compact(box.reduced(S,round['box']));require(compact.metadata==round['compressed_metadata'],'cut compression differs')
            if round['linear']['conclusion']=='exact_bounded_linear_obstruction':linear.verify(compact,round['linear']['certificate'])
            if 'proposal'in round and round['proposal']['conclusion']=='exact_integer_feasible_relaxation':
                check_integer(compact,round['proposal']['integer_values']);x=box.lift(S,round['box'],round['proposal']['integer_values']);check_integer(S,x)
            for r in round.get('modular',[]):lattice.verify_result(compact,r)
        require(out['global_cut_count']==sum('cut'in r for r in out['rounds'])<=10 and out['final_metadata']==S.metadata,'final cut coverage differs')
        require(isinstance(out['total_wall_budget_seconds'],int)and out['total_wall_budget_seconds']>0,'missing finite total wall budget')
        status=out['status'];last=out['rounds'][-1]if out['rounds']else{}
        if status=='exact_integer_and_phase_compatible':
            require(last.get('phase',{}).get('status')=='exact_integer_and_phase_compatible'and out['final_integer_witness']==x,'final compatible witness differs')
        elif status=='exact_integer_box_obstruction':require(last.get('box',{}).get('outcome')=='integer_box_obstruction','missing terminal exact box obstruction')
        elif status=='exact_bounded_linear_obstruction':require(last.get('linear',{}).get('conclusion')=='exact_bounded_linear_obstruction','missing terminal bounded separator')
        elif status=='exact_modular_obstruction':require(any(r['outcome']=='modular_obstruction'for r in last.get('modular',[])),'missing terminal modular obstruction')
        elif status=='integer_search_inconclusive_after_exact_global_cuts':
            require(last.get('proposal',{}).get('conclusion')=='no_exact_integer_witness_found'and last['proposal']['numerical_infeasibility_is_not_a_certificate']is True,'inconclusive integer proposal promoted')
            require(last.get('linear',{}).get('conclusion')=='no_exact_bounded_separator'and len(last.get('modular',[]))==2 and all(r['outcome']=='consistent_mod_prime'for r in last['modular']),'incomplete final necessary screens')
        elif status=='ten_global_cuts_completed_no_compatible_integer_witness':
            require(out['global_cut_count']==10 and len(out['rounds'])==11 and 'cut'not in last and last['phase']['status']=='selected_integer_pattern_phase_incompatible','ten-cut endpoint coverage differs')
        elif status=='all_indicator_pattern_rejected_without_uniform_global_cut':
            require('cut'not in last and last['phase']['status']=='selected_integer_pattern_phase_incompatible','missing all-indicator pattern rejection')
        elif status=='phase_reconstruction_inconclusive':
            require(last.get('phase',{}).get('status')in('numerical_search_incomplete','exact_reconstruction_incomplete')and 'cut'not in last,'inconclusive phase status promoted')
        elif status=='wall_budget_completed_without_compatible_witness':
            require('final_integer_witness'not in out,'wall-budget endpoint claims a compatible witness')
        else:raise VerificationError('unsupported or unfinished terminal cut outcome')
    print('PASS R65 global integer-phase cuts',out['status'],out['global_cut_count'],flush=True)


if __name__=='__main__':main()
