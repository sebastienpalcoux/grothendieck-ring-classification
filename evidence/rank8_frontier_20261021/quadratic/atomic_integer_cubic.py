"""Source-bound atomic integer Gram/S/cubic/Galois tests for 65 and 3472.

Default replay rebuilds exact systems. Passing the stated modular tests is
not an integer feasibility or categorification claim. --cache writes only
a local discovery checkpoint; canonical replay never reads a checkpoint.
"""
from pathlib import Path
import argparse,gzip,hashlib,json,pickle,sys,time
HERE=Path(__file__).resolve().parent;STAGE=HERE.parent
sys.path.insert(0,str(STAGE/'commutative_integer'))
sys.path.insert(0,str(STAGE/'global_induction'))
import streaming as st
from atomic_spectrum import AtomicSpectrum,table_for
from features import build
from lattice import modular,verify_result
from atomic_galois_balance import append_galois_balance
from rank_two_and_models import need


def build_system(index):
    source=st.load_ring(f'R8_3_{index}');R=source['tensor'];C=AtomicSpectrum(R,4)
    old=json.loads((STAGE/'global_induction/atomic_spectrum_results'/f'R8_3_{index}_h4.json').read_text())
    need(st.digest(R)==source['tensor_sha256']==old['tensor_sha256'],'source binding differs')
    need(C.meta==old['metadata'],'previous complete atomic domain differs')
    T=table_for(R,C.a)
    print(index,'building exact integer cubic system',flush=True)
    base=build(C,T)
    print(index,'base integer system',len(base.rhs),len(base.columns),flush=True)
    system=append_galois_balance(base,C,T)
    print(index,'Galois-augmented integer system',len(system.rhs),len(system.columns),flush=True)
    return source,C.meta,system


def run(index,cache=None):
    source,domain,system=build_system(index)
    if cache:
        with gzip.open(cache,'wb',compresslevel=3)as f:pickle.dump(system,f,protocol=5)
    results=[]
    for p in [2,3]:
        result=modular(system,p);verify_result(system,result);results.append(result)
        print(index,'prime',p,result['outcome'],'rank',result['rank'],flush=True)
    files=[STAGE/'commutative_integer/features.py',HERE/'atomic_galois_balance.py',
           HERE/'quartic_complex_character_table.py',HERE/'sextic_character_table.py',
           STAGE/'global_induction/atomic_spectrum.py']
    return {'kind':'atomic_integer_Gram_S_cubic_Galois_modular_test','id':source['id'],
            'tensor_sha256':source['tensor_sha256'],'atomic_domain':domain,'system':system.metadata,
            'source_sha256':{str(f.relative_to(STAGE)):hashlib.sha256(f.read_bytes()).hexdigest()for f in files},
            'modular_results':results,
            'scope':'necessary pseudo-unitary integer system; modular consistency is not Z-membership or nonnegative integer feasibility',
            'outcome':'pseudo_unitary_modular_obstruction'if any(r['outcome']=='modular_obstruction'for r in results)
                      else'consistent_modulo_2_and_3_only'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ring',type=int,action='append',choices=[65,3472]);p.add_argument('--write',action='store_true');p.add_argument('--cache');args=p.parse_args()
    indices=args.ring or[65,3472];need(not args.cache or len(indices)==1,'one target per discovery checkpoint')
    for index in indices:
        result=run(index,args.cache);path=HERE/f'atomic_integer_{index}_results.json'
        if args.write:path.write_text(json.dumps(st.encode(result),indent=2)+'\n')
        else:need(st.encode(result)==json.loads(path.read_text()),'atomic integer modular replay differs')
        print('PASS',index,result['outcome'],flush=True)


if __name__=='__main__':main()
