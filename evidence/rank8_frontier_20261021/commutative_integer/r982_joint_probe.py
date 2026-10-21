"""Exact joint-Galois check of already verified R982 integer center witnesses.

This additive check depends on the canonical r982.py reconstruction/replay
of the source-bound Gram/S/cubic systems and their integer witnesses.
"""
from pathlib import Path
from types import SimpleNamespace
import argparse,itertools,json,sys
import sympy as s
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'global_induction'))
sys.path.insert(0,str(HERE.parent/'quadratic'))
import streaming as st
from exact import require,evaluate
from joint_galois_balance import rows_for_labels

def run():
    source=st.load_ring('R8_3_982');R=source['tensor'];du=[next(j for j in range(8)if R[i][j][0])for i in range(8)]
    reference_path=HERE.parent/'global_induction/complete_results/R8_3_982_sts_frame_h4.json';reference=json.loads(reference_path.read_text());table=reference['metadata']['character_table']
    require(reference['tensor_sha256']==source['tensor_sha256'],'character source tensor differs')
    x=s.Symbol('x');poly=s.Poly.from_list(list(map(s.Rational,table['cyclotomic_polynomial'])),x);require(poly==s.Poly(s.cyclotomic_poly(24,x),x),'unexpected character field')
    K=s.QQ.alg_field_from_poly(poly,alias='zeta');z=K([1,0]);characters=[tuple(K(list(map(s.Rational,v)))for v in row)for row in table['characters']]
    require(len(set(characters))==8,'incomplete source character table')
    for row in characters:
        require(all(row[i]*row[j]==sum((K(R[i][j][k])*row[k]for k in range(8)),K.zero)for i in range(8)for j in range(8)),'character multiplication fails')
        require(all(row[du[i]]==evaluate(row[i].to_list(),z**-1,K)for i in range(8)),'character duality fails')
    codegrees=[sum((row[i]*row[du[i]]for i in range(8)),K.zero)for row in characters]
    require(codegrees==[K(list(map(s.Rational,v)))for v in table['codegrees']],'formal codegrees differ')
    require(all(sum((a[k]*b[du[k]]for k in range(8)),K.zero)==(codegrees[i]if i==j else K.zero)for i,a in enumerate(characters)for j,b in enumerate(characters)),'character orthogonality fails')
    profile_path=HERE/'R8_3_982_profile.json';profile=json.loads(profile_path.read_text());require(profile['tensor_sha256']==source['tensor_sha256'],'fixed domain source differs')
    records=[]
    for fi in(2,3):
        old_path=HERE/f'R8_3_982_frame{fi}.json';old=json.loads(old_path.read_text());require(old['tensor_sha256']==source['tensor_sha256'],'integer source differs')
        witness=old['original_integer_witness'];meta=old['metadata'];fp=meta['FP_character'];ds=characters[fp];D=sum((v*v for v in ds),K.zero)
        T=SimpleNamespace(K=K,degree=8,characters=characters,ds=ds,D=D,beta=[D/f for f in codegrees])
        p=profile['records'][fi];vectors={v['index']:(0,)+tuple(v['vector'])for v in p['high_vectors']}
        labels=[('high_orbit',tuple(o['indices']),tuple(vectors[j]for j in o['indices']))for o in p['duality_orbits']]
        Es=[E for E in range(8)if E!=fp];labels += [('fusion_coefficient',E,F,G)for E,F in itertools.combinations_with_replacement(Es,2)for G in Es]
        require(st.digest(labels)==meta['column_labels_sha256']and len(witness)==len(labels),'integer witness label binding differs')
        rows,rhs,row_labels,report=rows_for_labels(T,labels,p['low_columns'])
        failures=[i for i,(row,b)in enumerate(zip(rows,rhs))if sum(a*v for a,v in zip(row,witness))!=b]
        records.append({'frame_index':fi,'old_certificate_sha256':st.digest(old),'integer_witness_sha256':st.digest(witness),'joint_report':report,
                        'outcome':'exact_integer_witness_satisfies_joint_Galois'if not failures else'existing_witness_fails_joint_Galois','failed_rows':failures})
    return {'id':source['id'],'tensor_sha256':source['tensor_sha256'],'kind':'joint_Galois_check_of_exact_integer_witnesses','scope':'pseudo_unitary_necessary_system_survival_only',
            'character_reference_sha256':st.digest(reference),'profile_sha256':st.digest(profile),'records':records}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');a=ap.parse_args();out=run();p=HERE/'R8_3_982_joint_probe.json'
    if a.write:p.write_text(json.dumps(out,separators=(',',':'))+'\n')
    else:require(json.loads(p.read_text())==out,'joint witness check differs')
    print('PASS R982 joint witness check',[(r['frame_index'],r['outcome'],len(r['failed_rows']))for r in out['records']],flush=True)
if __name__=='__main__':main()
