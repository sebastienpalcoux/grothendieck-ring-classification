"""Final strengthened integer/cubic/joint-spectrum screen for R3472.

Default replay is exact and source-derived. A numerical search that does
not produce a checked witness or separator remains explicitly inconclusive.
No complete Hermite or bounded integer enumeration is claimed here.
"""
from pathlib import Path
from types import SimpleNamespace
import argparse,gzip,hashlib,json,pickle,sys
HERE=Path(__file__).resolve().parent;STAGE=HERE.parent
for name in('commutative_integer','quadratic_atomic_integer'):
    sys.path.insert(0,str(STAGE/name))
from features import st,require,check_integer
from joint_atomic_integer import construct
from sextic_character_table import SexticTable,simple_data
from pure_pointed_bounds import tighten_pure_bounds
from unit_pair_constraints import append_unit_pair_constraints
import bounds as box
import equations,lattice,linear


def sources():
    paths=[HERE/name for name in('strong_integer_3472.py','joint_atomic_integer.py','pure_pointed_bounds.py',
            'atomic_galois_balance.py','joint_galois_balance.py','galois_support_filter.py','fp_fusion_bounds.py','sextic_character_table.py')]
    paths += [STAGE/'commutative_integer'/name for name in('features.py','bounds.py','equations.py','lattice.py','linear.py')]
    paths += [STAGE/'quadratic_atomic_integer'/'unit_pair_constraints.py']
    paths += [STAGE/'global_induction'/'atomic_spectrum.py']
    return {str(p.relative_to(STAGE)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}


def domain(checkpoint=False):
    if checkpoint:
        with gzip.open('/tmp/joint_atomic3472.pkl.gz','rb')as f:source,support,S=pickle.load(f)
    else:source,support,S=construct(3472)
    R=source['tensor'];T=SexticTable(R,simple_data(3472))
    S=tighten_pure_bounds(S,R,T)
    S=append_unit_pair_constraints(S,SimpleNamespace(R=R),T)
    return source,support,S


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');p.add_argument('--checkpoint',action='store_true');a=p.parse_args()
    require(not a.checkpoint or a.write,'checkpoint is discovery-only')
    source,support,S=domain(a.checkpoint);path=HERE/'strong_integer_3472_results.json'
    if a.write:
        discovery=json.loads((HERE/'strong3472_discovery.json').read_text())
        require(discovery['metadata']==st.encode(S.metadata),'strongest discovery matrix differs')
        out={'id':source['id'],'tensor_sha256':source['tensor_sha256'],
             'kind':'complete_strongest_atomic_integer_necessary_screen','source_sha256':sources(),
             'support':support,'metadata':S.metadata,'box':discovery['box'],
             'scope':'necessary pseudo-unitary constraints; no complete integer-lattice or bounded-enumeration claim'}
        box.verify(S,out['box'])
        if out['box']['outcome']=='integer_box_obstruction':out['status']='exact_integer_box_obstruction'
        else:
            reduced=box.reduced(S,out['box']);compressed=equations.compact(reduced)
            require(compressed.metadata==discovery['compressed'],'compressed discovery matrix differs')
            out['compressed_metadata']=compressed.metadata;out['linear_search']=discovery['linear']
            if out['linear_search']['conclusion']=='exact_bounded_linear_obstruction':
                linear.verify(compressed,out['linear_search']['certificate']);out['status']='exact_bounded_linear_obstruction'
            else:
                out['modular_tests']=[]
                for prime in(2,3):
                    test=lattice.modular(compressed,prime);lattice.verify_result(compressed,test);out['modular_tests'].append(test)
                    print('3472 final modular',prime,test['outcome'],test['rank'],flush=True)
                if any(r['outcome']=='modular_obstruction'for r in out['modular_tests']):out['status']='exact_modular_obstruction'
                else:
                    proposal=json.loads((HERE/'strong3472_proposal.json').read_text());out['integer_proposal']=proposal
                    require(proposal['numerical_infeasibility_is_not_a_certificate']is True,'numerical negative cannot certify')
                    if proposal['conclusion']=='exact_integer_feasible_relaxation':
                        check_integer(compressed,proposal['integer_values'])
                        witness=box.lift(S,out['box'],proposal['integer_values']);check_integer(S,witness)
                        out['integer_witness']=witness;out['status']='exact_bounded_integer_feasible_relaxation'
                    else:out['status']='completed_exact_screens_integer_search_inconclusive'
        path.write_text(json.dumps(st.encode(out),separators=(',',':'))+'\n')
    else:
        out=json.loads(path.read_text());require(out['source_sha256']==sources(),'final source inventory differs')
        require(out['tensor_sha256']==source['tensor_sha256']and out['support']==st.encode(support)and out['metadata']==st.encode(S.metadata),'source-bound strongest matrix differs')
        box.verify(S,out['box'])
        if out['box']['outcome']=='integer_box_obstruction':require(out['status']=='exact_integer_box_obstruction','box conclusion differs')
        else:
            reduced=box.reduced(S,out['box']);compressed=equations.compact(reduced)
            require(compressed.metadata==out['compressed_metadata'],'final compression differs')
            if out['linear_search']['conclusion']=='exact_bounded_linear_obstruction':
                linear.verify(compressed,out['linear_search']['certificate']);require(out['status']=='exact_bounded_linear_obstruction','linear outcome differs')
            else:
                require(out['linear_search']['conclusion']=='no_exact_bounded_separator','unsupported linear outcome')
                require([r['prime']for r in out['modular_tests']]==[2,3],'planned modular coverage missing')
                for r in out['modular_tests']:lattice.verify_result(compressed,r)
                if any(r['outcome']=='modular_obstruction'for r in out['modular_tests']):require(out['status']=='exact_modular_obstruction','modular outcome differs')
                elif 'integer_witness'in out:
                    check_integer(compressed,out['integer_proposal']['integer_values'])
                    require(box.lift(S,out['box'],out['integer_proposal']['integer_values'])==out['integer_witness'],'witness lift differs')
                    check_integer(S,out['integer_witness']);require(out['status']=='exact_bounded_integer_feasible_relaxation','positive outcome differs')
                else:
                    require(out['status']=='completed_exact_screens_integer_search_inconclusive'and out['integer_proposal']['conclusion']=='no_exact_integer_witness_found','inconclusive proposal promoted')
                    require(out['integer_proposal']['numerical_infeasibility_is_not_a_certificate']is True,'numerical negative promoted')
    print('PASS strongest R3472 integer screen',out['status'],flush=True)


if __name__=='__main__':main()
