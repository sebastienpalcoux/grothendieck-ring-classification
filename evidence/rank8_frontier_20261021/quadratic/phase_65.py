"""Exact CM-real-STS/rotation compatibility of the saved R65 integer pattern."""
from pathlib import Path
import argparse,hashlib,itertools,json,sys
HERE=Path(__file__).resolve().parent;STAGE=HERE.parent
sys.path.insert(0,str(STAGE/'commutative_integer'))
from phase_mass import MassCone,discover,verify,st,require
from atomic_cm_real_sts import AtomicCMRealSTS


def domain():
    source=st.load_ring('R8_3_65');C=AtomicCMRealSTS(source['tensor'],4)
    frozen=json.loads((STAGE/'global_induction/complete_results/R8_3_65_cm_real_sts_h4.json').read_text())
    require(C.meta==frozen['metadata']and frozen['tensor_sha256']==source['tensor_sha256'],'complete CM-STS source differs')
    path=HERE/'joint_atomic_integer_65_results.json';receipt=json.loads(path.read_text())
    require(receipt['outcome']=='exact_nonnegative_integer_witness'and receipt['tensor_sha256']==source['tensor_sha256'],'integer source outcome differs')
    supports=receipt['support_filter'];individual=supports['individual'];joint=supports['joint']
    low=[individual['retained_low_indices'][j]for j in joint['retained_low_indices']]
    high=[individual['retained_high_orbit_indices'][j]for j in joint['retained_high_orbit_indices']]
    labels=[('low',C.meta['low_character_labels'][C.low[j][0]],tuple(C.low[j][1]))for j in low]
    labels += [('high_orbit',tuple(C.orbits[j]),tuple((0,)+tuple(C.a['high'][k][0])for k in C.orbits[j]))for j in high]
    Es=[E for E in range(8)if E!=C.meta['FP_character']]
    labels += [('fusion_coefficient',E,F,G)for E,F in itertools.combinations_with_replacement(Es,2)for G in Es]
    require(st.digest(labels)==receipt['system_metadata']['column_labels_sha256'],'integer restriction-label alignment differs')
    values=receipt['original_integer_witness'];require(len(values)==len(labels),'integer source vector length differs')
    require(all(isinstance(x,int)and x>=0 for x in values),'integer source values invalid')
    selected=[j for k,j in enumerate(low)if values[k]]
    require(len(selected)==7 and all(x in[0,1]for x in values[:len(low)]),'invalid selected distinguished lows')
    masses=[(j,values[len(low)+k])for k,j in enumerate(high)if values[len(low)+k]]
    D=MassCone(C,selected,masses)
    binding={'id':source['id'],'tensor_sha256':source['tensor_sha256'],
             'integer_witness_source':path.name,'integer_receipt_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
             'integer_column_labels_sha256':st.digest(labels),
             'source_sha256':{str(p.relative_to(STAGE)):hashlib.sha256(p.read_bytes()).hexdigest()for p in
                              [HERE/'atomic_cm_real_sts.py',STAGE/'commutative_integer/phase_mass.py']}}
    return D,binding


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');a=p.parse_args()
    D,binding=domain();path=HERE/'phase_65_results.json'
    if a.write:
        def save(result):path.write_text(json.dumps({'binding':binding,'phase':result},separators=(',',':'))+'\n')
        result=discover(D,save=save,seconds=120)
    else:
        out=json.loads(path.read_text());require(out['binding']==binding,'phase source binding differs');result=out['phase']
    verify(D,result)
    print('PASS R65 selected integer pattern',result['status'],D.nrows,D.nvars,flush=True)


if __name__=='__main__':main()
