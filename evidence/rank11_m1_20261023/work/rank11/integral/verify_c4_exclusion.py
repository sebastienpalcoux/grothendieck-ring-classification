"""Source-bound finite certificate for the C4 restriction exclusion.

Categorical implications are proved in C4_THEORY.md and independently
reviewed in structural/C4_NEUTRAL_MODULE_AUDIT.md. This verifies their exact
input hypotheses, reference basis map, and the full normalized H2 replay.
The independent reference audit is executed before producing an exclusion
receipt; a claimed fusion tensor is not accepted on its own.
"""
from pathlib import Path
import contextlib,hashlib,importlib.util,io,itertools,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from common import read,sha,require,validate
import verify_c4_reduction

def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
 with contextlib.redirect_stdout(io.StringIO()):red=verify_c4_reduction.run()
 A,B=red['records'];require(A['id']=='R11_1_104' and B['id']=='R11_1_153','case identities')
 require(A['even_selfdual_count']==7 and B['even_selfdual_count']==5,'incompatible even duality')
 cp=HERE.parent/'criteria_audit/verify_c4_torsor.py'
 with contextlib.redirect_stdout(io.StringIO()):load(cp,'independent_c4_torsor').main()
 cr=json.loads(cp.with_name('c4_torsor_independent.json').read_text())
 require(cr['passed'] and cr['H2_C4_order']==2 and cr['restriction_values']==cr['C2_coboundary_values'],'complete H2 restriction')
 require(cr['normalized_Z2_count']==128 and cr['normalized_B2_count']==64 and len(cr['four_cycle_conjugators'])==6,'complete cochains and conjugacy')
 mp=HERE.parent/'known_models/jordan_gt_model.json';m=json.loads(mp.read_text());T=m['model_tensor'];q=m['basis_map_source_to_model'];R=read()['R11_1_104'];validate(T)
 require(sha(R)==m['tensor_sha256']==A['tensor_sha256'],'reference source hash')
 require(sorted(q)==list(range(11)) and q[0]==0,'reference unit-preserving bijection')
 require(all(R[i][j][k]==T[q[i]][q[j]][q[k]] for i,j,k in itertools.product(range(11),repeat=3)),'reference full tensor equality')
 audit_path=HERE.parent/'nonintegral/audit104/verify.py'
 audit=load(audit_path,'independent_jordan_audit').Audit(m).run()
 require(audit['status']=='PASS' and audit['model_tensor']==T and audit['coefficients']==1331,'independent reference categorical tensor audit')
 out={'id':'R11_1_153','tensor_sha256':B['tensor_sha256'],'outcome':'excluded','scope':'all_complex_fusion_categories','criterion':'C4_extension_even_restriction','proof':'C4_THEORY.md','reference_model_id':'R11_1_104','reference_model_tensor_sha256':A['tensor_sha256'],'reference_model_certificate_sha256':hashlib.sha256(mp.read_bytes()).hexdigest(),'reference_model_independent_replay':'PASS','reference_model_independent_verifier':'../nonintegral/audit104/verify.py','reference_model_independent_verifier_sha256':hashlib.sha256(audit_path.read_bytes()).hexdigest(),'source_hypotheses':red['records'],'cohomology':{'A':'F2^4/<1111>','action_columns':cr['action_columns'],'normalized_cocycles':128,'normalized_coboundaries':64,'restriction':'zero','four_cycle_conjugacy_orbit_size':6},'finite_replay':'PASS','categorical_audits':['../structural/C4_NEUTRAL_MODULE_AUDIT.md','../criteria_audit/C4_TORSOR_REVIEW.md']}
 (HERE/'c4_exclusion.json').write_text(json.dumps(out,indent=2)+'\n')
 print('PASS: R153 exact C4 restriction-exclusion hypotheses; reference104 independent balanced-bimodule audit; all128 H2 cocycles; all6 four-cycles')
 return out
if __name__=='__main__':main()
