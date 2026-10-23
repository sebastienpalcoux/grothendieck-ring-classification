"""Build the review ledger solely from accepted evidence; discovery files are ignored."""
import csv,json,hashlib,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'deliverable';OUT.mkdir(exist_ok=True)
def load(p):return json.load(open(ROOT/p))
def key(k):return tuple(map(int,k.replace('R','').split('_')))
T=load('work/input_audit/tensors.json');E=collections.defaultdict(list);M=collections.defaultdict(list)
def exc(ids,label,proof,certificate,verifier):
 for rid in ids:E[rid].append(dict(criterion=label,scope='no fusion category over C',proof=proof,certificate=certificate,verifier=verifier))
def model(ids,label,proof,certificate,verifier):
 for rid in ids:M[rid].append(dict(model=label,scope='unitary realization exists',proof=proof,certificate=certificate,verifier=verifier))
for r in load('work/root_audit/baseline_verified.json')['records']:
 exc([r['id']],r['certificate']['kind'],'deliverable/report.pdf',r['source'],'python work/root_audit/verify_baseline.py')
exc(['R9_1_41'],'signed sphericalization and formal-codegree integrality','work/rank9_bridge/proof.tex','work/rank9_bridge/signed_bridge_certificate.json','python work/audit_signed/replay.py')
exc(load('work/integral_induction/dim60_exclusion_certificate.json')['case_ids'],'central-induction twist moment bound','deliverable/report.pdf','work/integral_induction/dim60_exclusion_certificate.json','python work/integral_induction/verify_dim60.py')
for rid,r in load('work/literature/gty_exact_obstructions.json').items():
 if r.get('all_complex_solutions_excluded'):exc([rid],'Liptrap equations: exact complex obstruction','work/literature/gty_proof.md','work/literature/gty_exact_obstructions.json','python work/literature/gty_verify_obstructions.py')
for kind in ['cubic_lattice','quadratic']:
 file='work/resolve_rank9_irrational/'+kind+'_certificates.json'
 exc([r['id']for r in load(file)],'central restriction: '+kind,'work/resolve_rank9_irrational/proofs.tex',file,'python work/resolve_rank9_irrational/'+('cubic_lattice.py'if kind=='cubic_lattice'else'quadratic_exact.py'))
exc([r['id']for r in load('work/resolve_metaplectic/certificates.json')],'Morita pointedization and nonabelian GTY stabilizer','work/resolve_metaplectic/THEORY.md','work/resolve_metaplectic/certificates.json','python work/resolve_metaplectic/verify.py')
exc(['R10_1_83','R10_1_177'],'forced dihedral equivariantization has commutative fusion','work/audit_new_models/INT160_AUDIT.md','work/audit_new_models/int160_audit.json','python work/audit_new_models/verify_int160_audit.py')
exc([r['id']for r in load('work/audit_new_models/rank10_reciprocity_audit.json')],'central-character reciprocity and induction Gram bound','work/resolve_rank10_quadratic/reciprocity.tex','work/resolve_rank10_quadratic/exclusion_receipts.json','python work/audit_new_models/verify_rank10_reciprocity.py')
for r in load('work/audit_models/selected_models.json'):
 model([r['id']],r['model']['model'],'work/audit_models/THEORY.md','work/audit_models/selected_models.json','python work/audit_models/verify_models.py')
model(['R10_1_132'],'Haagerup-Izumi category for C5','work/literature/hi_c5_model.py','work/literature/hi_c5_certificate.json','python work/literature/hi_c5_model.py')
for rid,r in load('work/literature/gty_liptrap_certificates.json').items():
 if r.get('found'):model([rid],'unitary Liptrap generalized Tambara-Yamagami data','work/literature/gty_proof.md','work/literature/gty_liptrap_certificates.json','python work/literature/gty_verify.py')
for r in load('work/resolve_small_models/records.json'):
 model([r['id']],r['model'],r['proof_file'],r['certificate_file'],r['verifier_command'])
for r in load('work/resolve_integral/verified_models160.json'):
 model([r['id']],r['model'],'work/resolve_integral/THEORY160.md','work/resolve_integral/verified_models160.json','python work/resolve_integral/replay160.py')
# Further results enter only through this deliberately explicit, reviewed manifest.
extra=ROOT/'work/consolidation/additional_accepted.json'
if extra.exists():
 for r in json.load(open(extra)):
  (exc if r['status']=='excluded' else model)([r['id']],r['label'],r['proof'],r['certificate'],r['verifier'])
assert not(set(E)&set(M)),('contradictory classifications',set(E)&set(M))
assert (set(E)|set(M))<=set(T),'unknown input identifier'
audit={r['id']:r for p in load('work/input_audit/audit.json').values()for r in p['rings']}
rows=[]
for rid in sorted(T,key=key):
 R=T[rid];a=audit[rid];status='excluded'if rid in E else'unitarily_realized'if rid in M else'unresolved'
 rows.append(dict(id=rid,rank=len(R),input_line=a['line'],status=status,
  tensor_sha256_compact_json=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),
  tensor_sha256_uint8_flattened=hashlib.sha256(bytes(v for A in R for B in A for v in B)).hexdigest(),
  commutative=a['commutative'],dual=a['dual'],fp_dimensions_approx=a['fp_dimensions_approx'],
  fp_dimension_approx=a['fp_dimension_approx'],exclusions=E.get(rid,[]),models=M.get(rid,[])))
counts={str(n):dict(collections.Counter(r['status']for r in rows if r['rank']==n))for n in(9,10)}
result=dict(input_count=len(rows),counts=counts,meaning={'excluded':'No fusion category over C; pivotal hypotheses are removed where required by an audited bridge.','unitarily_realized':'At least one unitary fusion category with this based fusion ring. This is not a classification of all associators.','unresolved':'No accepted existence or nonexistence proof in this package.'},records=rows)
(OUT/'ledger.json').write_text(json.dumps(result,indent=2)+'\n')
with open(OUT/'ledger.csv','w',newline='')as f:
 w=csv.writer(f);w.writerow(['id','rank','input_line','status','evidence','proof','certificate','verifier','tensor_sha256_compact_json'])
 for r in rows:
  evidence=(r['exclusions']or r['models']or[{}])[0]
  w.writerow([r['id'],r['rank'],r['input_line'],r['status'],evidence.get('criterion',evidence.get('model','')),evidence.get('proof',''),evidence.get('certificate',''),evidence.get('verifier',''),r['tensor_sha256_compact_json']])
print(json.dumps(counts,indent=2));print('Unresolved:',','.join(r['id']for r in rows if r['status']=='unresolved'))
