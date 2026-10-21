"""Source-bound ledger of the final complete commutative center domains.

Publication acceptance is owned by ../accepted.json. This ledger records
the actual mathematical certificate and preserves superseded attempts;
it never treats a numerical proposal or unfinished search as a conclusion.
"""
import argparse,hashlib,json
import coverage as inventory
import streaming as st
from exact import require

TARGETS=(
 ('R8_3_65','complete_results/R8_3_65_cm_real_sts_h4.json','cm_generation.py'),
 ('R8_3_903','complete_results/R8_3_903_sts_frame_h4.json','complete_phase_one.py'),
 ('R8_3_982','complete_results/R8_3_982_sts_frame_h4.json','complete_phase_one.py'),
 ('R8_3_1615','complete_results/R8_3_1615_sts_frame_h4.json','complete_phase_one.py'),
 ('R8_3_1617','complete_results/R8_3_1617_sts_frame_h4.json','complete_phase_one.py'),
 ('R8_3_1660','complete_results/R8_3_1660_sts_frame_h4.json','complete_phase_one.py'),
 ('R8_3_1661','complete_results/R8_3_1661_sts_frame_h4.json','complete_phase_one.py'),
 ('R8_3_1768','complete_results/R8_3_1768_atomic_real_sts_h4.json','complete_phase_one.py'),
 ('R8_3_1795','complete_results/R8_3_1795_atomic_real_sts_h4.json','complete_phase_one.py'),
 ('R8_3_3472','atomic_spectrum_results/R8_3_3472_h4.json','atomic_spectrum_generation.py'),
)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def build():
    histories={r['id']:r for r in inventory.build()['records']};records=[]
    for rid,relative,script in TARGETS:
        source=st.load_ring(rid);path=st.HERE/relative;row=json.loads(path.read_text())
        require(row['id']==rid and row['tensor_sha256']==source['tensor_sha256'],'final target source binding differs')
        require(row['status'] in ('excluded','exact_feasible_relaxation') and 'certificate' in row,'final target has no complete exact certificate')
        if row['status']=='excluded':require(row['scope']=='general_complex_fusion_category','final exclusion lacks general scope')
        record={'id':rid,'tensor_sha256':source['tensor_sha256'],
                'result_path':'global_induction/'+relative,'result_sha256':sha(path),
                'certificate_sha256':st.digest(row['certificate']),
                'producer_outcome':row['status'],'scope':row['scope'],
                'method':row.get('method'),'height':row.get('height'),
                'metadata':row.get('metadata',{}),'seconds':row.get('seconds'),
                'exact_replay':['global_induction/'+script,'--verify','global_induction/'+relative],
                'historical_incomplete_attempts':histories[rid]['incomplete_or_inapplicable_attempts'],
                'arithmetic_scope_limits':histories[rid]['arithmetic_scope_limits']}
        if row['status']=='exact_feasible_relaxation' and 'low_frames' in row.get('metadata',{}):
            c=row['certificate'];record['feasible_complete_low_frame_weights']=[{'index':i,'weight':w}for i,w in zip(c['indices'],c['weights'])if i<row['metadata']['low_frames']]
        records.append(record)
    external=st.HERE.parent/'quadratic/octic_low_s_general_results.json';row=json.loads(external.read_text());source=st.load_ring('R8_3_901')
    require(row['id']==source['id'] and row['tensor_sha256']==source['tensor_sha256'] and row['status']=='excluded' and row['scope']=='general_complex_fusion_category','octic low-S result incomplete')
    return {'schema':'frontier-final-center-campaign/v1',
            'scope':'complete necessary systems; feasible systems are not category models or proofs that all stronger tests survive',
            'publication_acceptance_source':'accepted.json',
            'records':records,
            'additional_complete_low_S_exclusion':{'id':row['id'],'tensor_sha256':row['tensor_sha256'],'result_path':'quadratic/octic_low_s_general_results.json','result_sha256':sha(external),'certificate_sha256':st.digest(row['certificate']),'exact_replay':['quadratic/octic_low_s_general.py']}}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();out=build();dest=st.HERE/'final_campaign.json'
    if args.write:dest.write_text(json.dumps(out,separators=(',',':'))+'\n')
    else:require(json.loads(dest.read_text())==out,'final campaign ledger differs from source-bound evidence')
    print('PASS final center campaign ledger',len(out['records']),'complete cone domains and one complete low-S obstruction',flush=True)

if __name__=='__main__':main()
