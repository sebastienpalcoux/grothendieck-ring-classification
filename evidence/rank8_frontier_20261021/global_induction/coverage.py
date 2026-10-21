"""Source-bound inventory of complete/incomplete central-induction domains."""
import argparse,json
import streaming as st
from exact import require
FOLDERS=('results','frame_results','spectral_results','sts_results','generic_results','atomic_results','atomic_spectrum_results','complete_results','fixed_results')
EXTERNAL={'R8_3_901':('quadratic/octic_low_s_general_results.json',)}

def build():
    baseline=json.loads((st.BASE/'criteria/campaign_completion.json').read_text())['unresolved_ids'];accepted=json.loads((st.HERE.parent/'accepted.json').read_text());decisions={x['id']:x for x in accepted['decisions']};rows=[]
    for rid in baseline:
        source=st.load_ring(rid);R=source['tensor'];comm=all(R[i][j]==R[j][i] for i in range(8) for j in range(8));attempts=[]
        for folder in FOLDERS:
            for path in sorted((st.HERE/folder).glob(rid+'_*.json')):
                a=json.loads(path.read_text());require(a['id']==rid and a['tensor_sha256']==source['tensor_sha256'],'attempt source binding differs')
                status=a.get('status','unspecified');complete=status in ('excluded','exact_feasible_relaxation','this_frame_indicator_excluded')
                attempts.append({'path':str(path.relative_to(st.HERE.parent)),'status':status,'complete_exact_certificate':complete and 'certificate' in a,'scope':a.get('scope'),'height':a.get('height',a.get('metadata',{}).get('height')),'method':a.get('method'),'metadata':{k:v for k,v in a.get('metadata',{}).items() if k in ('field','low_domain','low_frames','high_columns','high_duality_orbits','trace_types','order_bound','rows','variables')},'seconds':a.get('seconds')})
        for relative in EXTERNAL.get(rid,()):
            a=json.loads((st.HERE.parent/relative).read_text());require(a['id']==rid and a['tensor_sha256']==source['tensor_sha256'],'external attempt source binding differs')
            require(a['status']=='excluded' and a['scope']=='general_complex_fusion_category' and 'certificate' in a,'external general proof incomplete')
            attempts.append({'path':relative,'status':a['status'],'complete_exact_certificate':True,'scope':a['scope'],'height':None,'method':a['method'],'metadata':{'domain':'all complete raw low frames and full octic character labelings; no high or phase relaxation'},'seconds':a.get('seconds')})
        inapplicable=[]
        if not comm:inapplicable.append({'domain':'commutative low-character frame and atomic cones','reason':'source tensor is noncommutative; separate noncommutative campaign owns the center normalization'})
        if rid=='R8_3_901':inapplicable.append({'domain':'real-FP-field STS adapter','reason':'nontrivial source duality forces some characters to be nonreal; all eight characters cannot split in the totally real Q(sqrt3,sqrt5) FP field','duality':[next(j for j in range(8) if R[i][j][0]) for i in range(8)]})
        if rid in ('R8_3_65','R8_3_1055','R8_3_3413','R8_3_3472'):inapplicable.append({'domain':'original unprojected same-FP-field STS adapter','reason':'the complete character table does not split in the FP field, so that particular adapter is inapplicable; the full splitting-field S-symmetry cone remains valid. For R65 the separate CM-real projection supplies additional STS equations in the FP field without requiring the complete table to split there.','field_coverage':'quadratic/character_field_coverage_results.json'})
        completed=[a for a in attempts if a['complete_exact_certificate']]
        rows.append({'id':rid,'tensor_sha256':source['tensor_sha256'],'commutative':comm,'accepted_status':decisions.get(rid,{}).get('status','unresolved'),'completed_domains':completed,'incomplete_or_inapplicable_attempts':[a for a in attempts if not a['complete_exact_certificate']],'arithmetic_scope_limits':inapplicable})
    return {'schema':'frontier-global-domain-coverage/v1','scope':'operational exact necessary-condition coverage; feasible cones are not models','records':rows}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();out=build();dest=st.HERE/'coverage.json'
    if args.write:dest.write_text(json.dumps(out,separators=(',',':'))+'\n')
    else:require(json.loads(dest.read_text())==out,'coverage inventory differs from current source-bound attempts')
    print('PASS coverage',len(out['records']),'baseline residuals',flush=True)
if __name__=='__main__':main()
