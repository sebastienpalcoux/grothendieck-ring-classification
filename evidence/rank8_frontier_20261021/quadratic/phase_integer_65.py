"""Finite exact-cut campaign joining R65 integer and phase constraints."""
from pathlib import Path
from types import SimpleNamespace
import argparse,gzip,hashlib,json,pickle,sys
HERE=Path(__file__).resolve().parent;STAGE=HERE.parent
for directory in('commutative_integer','quadratic_atomic_integer'):
    sys.path.insert(0,str(STAGE/directory))
from features import st,require,check_integer
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
    choices=list(map(list,st.old.ht.indicator_choices(C.R)));require(len(choices)==1,'branch-specific driver requires exactly one indicator choice')
    saved=json.loads((HERE/'joint_atomic_integer_65_results.json').read_text())
    require(saved['system_metadata']==st.encode(S.metadata),'original integer metadata differs')
    x=saved['original_integer_witness'];check_integer(S,x)
    bounded=tighten_pure_bounds(S,C.R,T);check_integer(bounded,x)
    strong=append_unit_pair_constraints(bounded,C,T);x=lift_witness(bounded,strong,x)
    return source,support,C,strong,x,choices[0]


def pins():
    paths=[HERE/name for name in('phase_integer_65.py','joint_atomic_integer.py','integer_phase_cuts.py','pure_pointed_bounds.py','atomic_cm_real_sts.py')]
    paths += [STAGE/'commutative_integer'/name for name in('features.py','bounds.py','equations.py','linear.py','lattice.py','phase_mass.py')]
    paths += [STAGE/'quadratic_atomic_integer'/name for name in('unit_pair_constraints.py','proposal.py')]
    paths += [HERE/'joint_atomic_integer_65_results.json']
    return {str(p.relative_to(STAGE)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');p.add_argument('--checkpoint',action='store_true');p.add_argument('--seconds',type=int,default=180);a=p.parse_args()
    require(not a.checkpoint or a.write,'checkpoint is discovery-only')
    source,support,C,S,x,ep=initial(a.checkpoint);path=HERE/'phase_integer_65_results.json'
    if a.write:
        out={'id':source['id'],'tensor_sha256':source['tensor_sha256'],'kind':'bounded_integer_cubic_joint_spectrum_global_phase_cut_campaign',
             'source_sha256':pins(),'initial_metadata':S.metadata,'support_sha256':st.digest(support),
             'indicators':ep,'maximum_global_cuts':10,'initial_integer_witness':x,'rounds':[],
             'status':'running','scope':'necessary pseudo-unitary system; each cut is global within the sole indicator branch'}
        def save():path.write_text(json.dumps(st.encode(out),separators=(',',':'))+'\n')
        save()
        for step in range(11):
            print('65 phase-cut round',step,'integer variables',len(S.columns),flush=True)
            check_integer(S,x);D=specialize(C,S,x)
            phase=phase_mass.discover(D,seconds=120)
            round={'integer_witness':x,'phase':phase};out['rounds'].append(round);save()
            if phase['status']=='exact_integer_and_phase_compatible':
                phase_mass.verify(D,phase);out['status']='exact_integer_and_phase_compatible';out['final_integer_witness']=x;break
            if phase['status']!='selected_integer_pattern_phase_incompatible':out['status']='phase_reconstruction_inconclusive';break
            phase_mass.verify(D,phase)
            if step==10:out['status']='ten_global_cuts_completed_no_compatible_integer_witness';break
            require(len(phase['attempts'])==1 and phase['attempts'][0]['indicators']==ep,'incomplete sole-indicator phase obstruction')
            ray=phase['attempts'][0]['certificate']['covector'][:C.nrows]
            co,b,report=make_cut(C,S,ep,ray)
            violation=sum(v*z for v,z in zip(co,x))-b;require(violation>0,'global cut does not reject its originating integer witness')
            round.update(cut=report,originating_pattern_exact_violation=violation)
            S=append_cut(S,co,b,report);round['augmented_metadata']=S.metadata
            round['box']=box.propagate(S);save()
            if round['box']['outcome']=='integer_box_obstruction':out['status']='exact_integer_box_obstruction';break
            reduced=box.reduced(S,round['box']);compact=equations.compact(reduced);round['compressed_metadata']=compact.metadata
            round['linear']=linear.discover(compact);save()
            if round['linear']['conclusion']=='exact_bounded_linear_obstruction':out['status']='exact_bounded_linear_obstruction';break
            round['proposal']=propose_bounded(compact,a.seconds,check_integer);save()
            if round['proposal']['conclusion']!='exact_integer_feasible_relaxation':
                round['modular']=[lattice.modular(compact,p)for p in(2,3)]
                out['status']='exact_modular_obstruction'if any(r['outcome']=='modular_obstruction'for r in round['modular'])else'integer_search_inconclusive_after_exact_global_cuts'
                break
            x=box.lift(S,round['box'],round['proposal']['integer_values']);check_integer(S,x)
        out['final_metadata']=S.metadata;out['global_cut_count']=sum('cut'in r for r in out['rounds']);save()
    else:
        out=json.loads(path.read_text());require(out['source_sha256']==pins(),'global-cut source inventory differs')
        require(out['tensor_sha256']==source['tensor_sha256']and out['initial_metadata']==st.encode(S.metadata)and out['support_sha256']==st.digest(support),'initial strengthened domain differs')
        require(out['initial_integer_witness']==x and out['indicators']==ep,'initial witness or indicators differ')
        for k,round in enumerate(out['rounds']):
            require(round['integer_witness']==x,'integer witness chain differs');check_integer(S,x)
            D=specialize(C,S,x);phase=round['phase']
            if phase['status']in('exact_integer_and_phase_compatible','selected_integer_pattern_phase_incompatible'):phase_mass.verify(D,phase)
            else:require(out['status']=='phase_reconstruction_inconclusive'and k+1==len(out['rounds']),'uncertified phase status promoted')
            if 'cut'not in round:continue
            co,b,report=make_cut(C,S,ep,round['cut']['base_covector']);require(st.encode(report)==round['cut'],'complete global cut differs')
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
        require(out['status']!='running','unfinished cut campaign')
        if out['status']=='exact_integer_and_phase_compatible':require(out['final_integer_witness']==x,'final compatible witness differs')
    print('PASS R65 global integer-phase cuts',out['status'],out['global_cut_count'],flush=True)


if __name__=='__main__':main()
