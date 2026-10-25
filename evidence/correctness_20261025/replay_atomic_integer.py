"""Final source-bound bounded integer Gram/S/cubic/Galois screens.

Default replay reconstructs both complete source domains. Numerical search
is used only to propose an integer witness, never to certify exclusion.
"""
from pathlib import Path
import argparse,gzip,hashlib,json,pickle,sys,time
ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'evidence/rank8_frontier_20261021/quadratic';STAGE=HERE.parent
sys.path.insert(0,str(STAGE/'commutative_integer'))
sys.path.insert(0,str(STAGE/'global_induction'))
import streaming as st
from atomic_spectrum import AtomicSpectrum,table_for
from features import build,check_integer
from lattice import modular,verify_result,hermite,verify_hermite
import bounds as box
import equations
from atomic_galois_balance import append_galois_balance
from galois_support_filter import filter_support
from joint_galois_balance import filter_support as joint_filter,append_joint_balance
from fp_fusion_bounds import tighten_fusion_bounds
from rank_two_and_models import need


def source_pins():
    files=[Path(__file__).resolve(),HERE/'atomic_galois_balance.py',
           HERE/'galois_support_filter.py',HERE/'joint_galois_balance.py',HERE/'fp_fusion_bounds.py',
           HERE/'quartic_complex_character_table.py',HERE/'sextic_character_table.py',
           STAGE/'commutative_integer/features.py',STAGE/'commutative_integer/bounds.py',
           STAGE/'commutative_integer/equations.py',STAGE/'commutative_integer/lattice.py',
           STAGE/'global_induction/atomic_spectrum.py']
    return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()for f in files}


def construct(index):
    start=time.monotonic();source=st.load_ring(f'R8_3_{index}')
    C=AtomicSpectrum(source['tensor'],4)
    old=json.loads((STAGE/'global_induction/atomic_spectrum_results'/f'R8_3_{index}_h4.json').read_text())
    need(st.digest(C.R)==source['tensor_sha256']==old['tensor_sha256'],'source binding differs')
    need(C.meta==old['metadata'],'previous complete atomic domain differs')
    T=table_for(C.R,C.a);D,support=filter_support(C,T)
    print(index,'support',support['outcome'],len(D.low),len(D.orbits),round(time.monotonic()-start,3),flush=True)
    need(support['outcome']=='necessary_support_survives','support obstruction needs separate general lift')
    D,joint=joint_filter(D,T)
    print(index,'joint support',joint['outcome'],len(D.low),len(D.orbits),flush=True)
    need(joint['outcome']=='joint_support_survives','joint support obstruction needs separate general lift')
    support={'individual':support,'joint':joint}
    S=build(D,T);print(index,'cubic',len(S.rhs),len(S.columns),round(time.monotonic()-start,3),flush=True)
    S=append_galois_balance(S,D,T)
    S=append_joint_balance(S,D,T)
    S=tighten_fusion_bounds(S,D,T)
    print(index,'Galois+FP',len(S.rhs),len(S.columns),round(time.monotonic()-start,3),flush=True)
    return source,support,S



def verify_terminal(S,out):
    """Derive a completed scoped outcome from verified exact components."""
    tests=out.get('modular_tests',[])
    need([r.get('prime') for r in tests]==[2,3],'incomplete modular coverage')
    for r in tests:verify_result(S,r)
    box.verify(S,out['box'])
    scopes=['complete_source_domain','missing_conjugate_support_closure',
            'joint_Galois_support_and_balance','modulo_2_and_3','finite_box_propagation']
    need(out['box']['outcome'] in ('integer_box_consistent','integer_box_obstruction'),'unfinished box result')
    if out['box']['outcome']=='integer_box_consistent':
        need('Hermite' in out and 'compact_metadata' in out,'incomplete signed-lattice scope')
        compressed=equations.compact(box.reduced(S,out['box']))
        need(st.encode(compressed.metadata)==out['compact_metadata'],'compressed integer system differs')
        verify_hermite(compressed,out['Hermite'])
        scopes.append('signed_integer_lattice_membership')
    if 'original_integer_witness' in out:check_integer(S,out['original_integer_witness'])
    obstruction=(any(r['outcome']=='modular_obstruction' for r in tests)
                 or out['box']['outcome']=='integer_box_obstruction'
                 or out.get('Hermite',{}).get('outcome')=='integer_lattice_obstruction')
    expected=('pseudo_unitary_integer_obstruction' if obstruction else
              'exact_nonnegative_integer_witness' if 'original_integer_witness' in out else
              'exact_signed_lattice_consistency_only')
    need(out.get('outcome')==expected,'terminal outcome does not follow from exact evidence')
    need(out.get('completed_exact_scopes')==scopes,'claimed completed scopes differ')
    return expected


def run(index,write=False,propose=0,checkpoint=None,resume=False,receipt=None):
    path=Path(receipt) if receipt else HERE/f'joint_atomic_integer_{index}_results.json'
    need(not write or not path.exists(),'refusing to overwrite a published or existing receipt')
    if write:path.parent.mkdir(parents=True,exist_ok=True)
    if resume:
        need(write and checkpoint,'checkpoints are discovery-only')
        with gzip.open(checkpoint,'rb')as f:source,support,S=pickle.load(f)
    else:
        source,support,S=construct(index)
        if checkpoint:
            with gzip.open(checkpoint,'wb',compresslevel=3)as f:pickle.dump((source,support,S),f,protocol=5)
    pins=source_pins()
    if write:
        out={'kind':'joint_atomic_integer_Gram_S_cubic_Galois_screen','id':source['id'],
             'tensor_sha256':source['tensor_sha256'],'source_sha256':pins,
             'support_filter':support,'system_metadata':S.metadata,
             'scope':'necessary pseudo-unitary central integer system; surviving tests do not construct a category'}
        out['modular_tests']=[]
        for p in(2,3):
            r=modular(S,p);verify_result(S,r);out['modular_tests'].append(r)
            print(index,'modular',p,r['outcome'],r['rank'],flush=True)
        out['box']=box.propagate(S);box.verify(S,out['box'])
        print(index,'box',out['box']['outcome'],out['box']['fixed_variables'],out['box']['tightenings'],flush=True)
        path.write_text(json.dumps(st.encode(out),separators=(',',':'))+'\n')
        if out['box']['outcome']=='integer_box_consistent':
            reduced=box.reduced(S,out['box']);compressed=equations.compact(reduced)
            out['compact_metadata']=compressed.metadata
            print(index,'compact',len(compressed.rhs),len(compressed.columns),flush=True)
            out['Hermite']=hermite(compressed,progress=lambda n,r:print(index,'HNF',n,r,flush=True))
            verify_hermite(compressed,out['Hermite'])
            print(index,'Hermite',out['Hermite']['outcome'],out['Hermite']['rank'],flush=True)
            path.write_text(json.dumps(st.encode(out),separators=(',',':'))+'\n')
            if propose and out['Hermite']['outcome']=='integer_lattice_member':
                sys.path.insert(0,str(STAGE/'quadratic_atomic_integer'))
                from proposal import propose as search
                out['integer_proposal']=search(compressed,propose,check_integer)
                if out['integer_proposal']['conclusion']=='exact_integer_feasible_relaxation':
                    witness=box.lift(S,out['box'],out['integer_proposal']['integer_values'])
                    check_integer(S,witness);out['original_integer_witness']=witness
                print(index,'proposal',out['integer_proposal']['conclusion'],flush=True)
        obstruction=any(r['outcome']=='modular_obstruction'for r in out['modular_tests'])or out['box']['outcome']=='integer_box_obstruction'or out.get('Hermite',{}).get('outcome')=='integer_lattice_obstruction'
        out['outcome']='pseudo_unitary_integer_obstruction'if obstruction else'exact_nonnegative_integer_witness'if 'original_integer_witness'in out else'exact_signed_lattice_consistency_only'
        out['completed_exact_scopes']=['complete_source_domain','missing_conjugate_support_closure','joint_Galois_support_and_balance','modulo_2_and_3','finite_box_propagation']
        if 'Hermite' in out:out['completed_exact_scopes'].append('signed_integer_lattice_membership')
        verify_terminal(S,out)
        path.write_text(json.dumps(st.encode(out),separators=(',',':'))+'\n')
    else:
        out=json.loads(path.read_text())
        need(out['source_sha256']==pins and out['tensor_sha256']==source['tensor_sha256'],'source receipt differs')
        need(out['support_filter']==st.encode(support)and out['system_metadata']==st.encode(S.metadata),'complete strengthened domain differs')
        verify_terminal(S,out)
    print('PASS final atomic integer',index,out['outcome'],flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ring',type=int,action='append',choices=[65,3472]);p.add_argument('--write',action='store_true');p.add_argument('--propose',type=int,default=0);p.add_argument('--checkpoint');p.add_argument('--resume',action='store_true');p.add_argument('--receipt',help='new output or explicit source-bound replay receipt');a=p.parse_args()
    indices=a.ring or[65,3472];need(not a.checkpoint or len(indices)==1,'one checkpoint per target');need(not a.receipt or len(indices)==1,'one explicit receipt per target')
    for index in indices:run(index,a.write,a.propose,a.checkpoint,a.resume,a.receipt)


if __name__=='__main__':main()
