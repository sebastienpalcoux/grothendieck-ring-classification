"""Accepted unitary rank-ten model and theoretical progress, without rewriting old ledgers."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import hashlib,json,re

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE='evidence/unresolved_retry_20261024'
LEDGER=EVIDENCE+'/rank9_rank10_m1_ledger.json'
NEW=EVIDENCE+'/proofs/unresolved11_retry_20261024'
OLD=EVIDENCE+'/proofs/unresolved11_20261024'
URL='https://github.com/sebastienpalcoux/grothendieck-ring-classification'
TITLE='Current theoretical continuation'
MODEL='Charge-zero conformal-embedding model SU(4)_6 inside SU(10)_1'

def active(repo=ROOT):return (Path(repo)/EVIDENCE/'accepted.json').is_file()
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def need(x,message):
    if not x:raise ValueError(message)
def write(p,data):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')

def validate(repo=ROOT):
    repo=Path(repo);a=read(repo/EVIDENCE/'accepted.json')
    manifest=read(repo/EVIDENCE/'source_manifest.json')
    need(manifest['accepted_sha256']==sha(repo/EVIDENCE/'accepted.json'),'Accepted research identity')
    for path,digest in manifest['files'].items():
        need(sha(repo/path)==digest,'Research proof source changed: '+path)
    baseline=a['baseline_rank9_rank10_ledger'];need(sha(repo/baseline['path'])==baseline['sha256'],'Retry predecessor ledger identity')
    before=read(repo/baseline['path']);after=read(repo/LEDGER)
    need(len(before['records'])==len(after['records'])==336,'Rank-nine/ten coverage')
    changes=[]
    for x,y in zip(before['records'],after['records']):
        need(x['id']==y['id'] and x['tensor_sha256_compact_json']==y['tensor_sha256_compact_json'],'Retry tensor identity')
        if x!=y:
            need(x['id']=='R10_1_189' and x['status']=='unresolved' and y['status']=='unitarily_realized','Only the proved model changes status')
            need(y['models'] and not y['exclusions'],'Actual positive model record')
            changes.append(x['id'])
    need(changes==['R10_1_189'],'Retry transition coverage')
    actual=Counter(r['status']for r in after['records']if r['rank']==10)
    need(actual==Counter(excluded=136,unitarily_realized=58),'Complete rank-ten partition')
    archive=a['proof_archive'];need(sha(repo/archive['path'])==archive['sha256'],'Retry archive identity')
    receipt=read(repo/NEW/'rank10/conformal_model_certificate.json')
    need(receipt['source_tensor_sha256']==a['changes'][0]['tensor_sha256'] and receipt['structure_constants_checked']==1000 and receipt['status']=='PASS','Exact unitary-model certificate')
    return {'status':'PASS','current_open_cases':10,'rank10':{'excluded':136,'unitarily_realized':58,'unresolved':0},'ledger':LEDGER,'ledger_sha256':sha(repo/LEDGER),'evidence':EVIDENCE}

FINDINGS={
'R6_4_155':[
 'Every tensor autoequivalence fixes all four pointed simple classes, because their uniquely lifted central twists are distinct. The resulting extension obstruction rules out the specified rank-nine Morita branch.',
 'The new even cyclic Clifford criterion passes 1,144 exact blocks through order 24. The incomplete numerical laptop campaign supplies no model or exclusion.'],
'R6_8_1660':[
 'The surviving rank-eight Morita alternative is exactly R8_3_941; all 512 coefficients agree under the recorded basis map. Existence of the required nonpointed algebra is not forced.',
 'The regular Ising-bimodule route was already covered by the manuscript; it is an audited existing deduction, not a new categorification.'],
'R8_3_928':[
 'Every indecomposable semisimple module category in a hypothetical categorification is categorically regular, without a module-rank cutoff. All categorical Morita partners are therefore equivalent to that category.',
 'The proof uses the complete internal-end domain, a paired Gram determinant argument, and a module object with unit internal end. Four necessary center patterns remain; the source category is not constructed.'],
'R8_3_941':[
 'The rank-eight alternative in the R6_8_1660 Morita list is exactly this source tensor. The connection remains conditional on the corresponding nonpointed algebra.',
 'Fourteen necessary center allocations remain. The SU(4)_8 exceptional module-category route is ruled out by the proper-subcategory index bound; no general exclusion follows.'],
'R8_3_1154':[
 'The three center patterns and 25 pair histograms remain necessary data. Exact indicator checks recover an existing sign restriction and give no model.',
 'Five entire construction families, each with arbitrary pointed factors followed by connected étale condensation, are excluded: SU(4)_6, SU(5)_5, SU(6)_4, SU(3)_7 times Fibonacci, and the realized rank-fourteen factor from the rank-ten construction. These are route exclusions only.'],
'R8_3_1768':[
 'An actual complex twisted GH(C6,2) category is constructed from the split C12 times C12 near-group input of Radchenko–Wheeler. Its pointed associator is class 3, exactly the class required by the completed rank-eight based-module route.',
 'The remaining categorical gap is a connected separable algebra 1+sigma. The canonical near-group algebra descends to End(sigma), so it does not fill that gap. The two-variable associativity equations are explicit; cubic rotation is the identity on the two-dimensional trivalent space.',
 'The two completed based module actions and their commuting matrices are necessary data, not a Morita equivalence. The final indicator/Gram branch remains open.'],
'R9_2_137':[
 'No central boson or nontrivial Tannakian subcategory exists; every integral central simple is invertible. The pointed center is Vec or sVec.',
 'A general module-functor sign theorem forces each large simple third indicator into {-1,-zeta_3,-zeta_3^2}. In the positive TY-sign branch every projected third indicator is 1/2, so 9 divides the FS exponent. Both TY signs retain exact feasible necessary-system witnesses.'],
'R9_2_1607':[
 'No central boson or nontrivial Tannakian subcategory exists; every integral central simple is invertible. The positive TY-sign branch is excluded by an exact separating certificate.',
 'The new source-local Clifford theorem forces each large simple third indicator into {-1,-zeta_3,-zeta_3^2}. The negative-sign branch still has an exact rational witness to the strengthened necessary system.'],
'R9_2_1975':[
 'The extreme D8 Morita branch is ruled out by the R155 tensor-autoequivalence obstruction. The integral center is Vec and the positive TY sign is excluded.',
 'The all-cochain D8 bimodule theorem forces the mixed stabilizer pairing to be -1. Morita invariance restricts the sum of the four projected third indicators to {-4,-5/2,-1,1/2,2}. The negative-sign necessary system remains feasible; the source-local common-stabilizer theorem does not apply to this noncommutative case.'],
'R9_2_1976':[
 'No central boson or nontrivial Tannakian subcategory exists; integral central simples are invertible. Only the negative TY-sign branch survives.',
 'The new source-local Clifford theorem and exact separating certificates force each projected large-object third indicator to be 1/2 in that branch, so 9 divides the FS exponent. An exact rational witness remains for the strengthened necessary system.'],
'R10_1_189':[
 'An actual unitary model is the charge-zero component of the category of modules over B=000+060+202+222 supplied by the known conformal embedding SU(4)_6 inside SU(10)_1.',
 'With beta=F(010), g=tau_2 and x=tau_5 beta, the ten simples satisfy g^5=1, gx=xg, x*=x and x^2=1+(g+g^2+g^3+g^4)x. All 1,000 census coefficients match exactly.',
 'The accompanying rank-fourteen modular category and the actual algebra 1+U are constructed within the same known WZW category. No existence inference from candidate modular data is required.',
 'This recognizes a classical construction; it is not a claim of a new tensor category. The unitary model is unbraided, consistently with the retained braided obstruction.']}

PROOFS={
'R6_4_155':[(OLD+'/rank6_pair/POINTED_AUTOMORPHISM_OBSTRUCTION.md','Pointed automorphism obstruction'),(NEW+'/rank6/EVEN_CLIFFORD.md','Even cyclic Clifford theorem')],
'R6_8_1660':[(OLD+'/rank6_pair/RANK6_REPORT.md','Conditional R1660–R941 identification'),(NEW+'/rank6/R1660_REGULAR_BIMODULE.md','Ising-bimodule audit')],
'R8_3_928':[(OLD+'/rank8_quartic_pair/R928_MORITA_RIGIDITY.md','All-rank categorical Morita rigidity'),(NEW+'/quartic/THEORETICAL_RETRY.md','Further route obstructions')],
'R8_3_941':[(OLD+'/rank6_pair/RANK6_REPORT.md','Exact cross-rank Morita identification'),(NEW+'/quartic/THEORETICAL_RETRY.md','Quartic construction scope')],
'R8_3_1154':[(NEW+'/quadratic8/R1154_POINTED_EXTENSION_OBSTRUCTIONS.md','Uniform pointed-extension route obstructions')],
'R8_3_1768':[(NEW+'/quadratic8/TWISTED_GH6_CONSTRUCTION.md','Actual twisted GH precursor'),(NEW+'/global/R1768_TWISTED_PRECURSOR_AUDIT.md','Independent categorical audit and remaining algebra')],
'R9_2_137':[(OLD+'/rank9_commutative/NO_CENTRAL_BOSON.md','Unified center obstruction'),(NEW+'/rank9/SOURCE_LOCAL_CLIFFORD.md','Source-local Clifford theorem'),(NEW+'/quartic/AUDIT_DISCRETE_CLIFFORD.md','Exact discrete spectrum audit')],
'R9_2_1607':[(OLD+'/rank9_commutative/TY_SPECTRUM.md','TY-sign exclusion'),(NEW+'/rank9/SOURCE_LOCAL_CLIFFORD.md','Source-local Clifford theorem')],
'R9_2_1975':[(OLD+'/rank9_noncommutative/NEW_RESTRICTIONS.md','Noncommutative center and Morita restrictions'),(NEW+'/rank9/POINTED_BIMODULE.md','All-cochain pointed bimodule theorem')],
'R9_2_1976':[(OLD+'/rank9_commutative/TY_SPECTRUM.md','TY-sign exclusion'),(NEW+'/rank9/SOURCE_LOCAL_CLIFFORD.md','Source-local Clifford theorem'),(NEW+'/quartic/AUDIT_DISCRETE_CLIFFORD.md','Exact discrete spectrum audit')],
'R10_1_189':[(NEW+'/rank10/CONFORMAL_MODEL.md','Actual unitary construction'),(NEW+'/rank10/rank10_conformal_model.pdf','Categorical proof PDF'),(NEW+'/rank10/conformal_model_certificate.json','Exact 1,000-coefficient certificate')]}

def apply_profiles(repo=ROOT,ref='main'):
    repo=Path(repo)
    if not active(repo):return
    validate(repo)
    def evidence(path,label):
        need((repo/path).is_file(),'Missing retry proof '+path)
        return {'label':label,'path':path,'url':URL+'/blob/'+ref+'/'+path,'sha256':sha(repo/path)}
    current=evidence(LEDGER,'Current accepted rank-nine/ten decisions')
    row=next(r for r in read(repo/LEDGER)['records']if r['id']=='R10_1_189')
    for name,key in [('unresolved_cases.json','cases'),('resolved_cases.json','cases'),('rank9_rank10_m1.json','cases'),('rank9_m2.json','cases')]:
        path=repo/'site/dist/data'/name
        if not path.is_file():continue
        data=read(path);changed=False
        for r in data[key]:
            rid=r['id']
            if rid not in FINDINGS:continue
            changed=True;proofs=[evidence(p,label)for p,label in PROOFS[rid]]
            research={'title':TITLE,'source':proofs[0]['path'],'url':proofs[0]['url'],'source_sha256':proofs[0]['sha256'],'data':{'findings':FINDINGS[rid],'status_changed':rid=='R10_1_189','remaining_gap':None if rid=='R10_1_189' else 'An actual categorification or a general categorical contradiction is still missing.'}}
            r['research']=[research]+[v for v in r.get('research',[])if v.get('title')!=TITLE]
            r['evidence']=proofs+[v for v in r.get('evidence',[])if v['path']not in {p['path']for p in proofs}]
            r['summary']=' '.join(FINDINGS[rid][:2])
            if rid=='R10_1_189':
                r.update(status='unitarily_realized',existence='unitary',name=MODEL,model_reference='Known conformal embedding SU(4)_6 subset SU(10)_1; charge-zero module subcategory',model_reference_url=proofs[0]['url'],source_file=LEDGER,source_url=current['url'],investigation_deferred=False)
                r['research']=[{'title':'Current accepted case decision','source':LEDGER,'url':current['url'],'source_sha256':current['sha256'],'data':row}]+[v for v in r['research']if v.get('title')!='Current accepted case decision']
                r['evidence']=[current]+[v for v in r['evidence']if v['path']!=LEDGER]
                scope=r['categorification_scope'];scope.update(general_status='realized',level_status={k:'realized'for k in ('general','pivotal','spherical','pseudo_unitary','unitary')},strongest_excluded=None,same_category_implications=[],existence_implications=[],notes=FINDINGS[rid],audit_sources=proofs)
            elif rid.startswith('R9_2_'):
                r['categorification_scope']['notes']=[v for v in r['categorification_scope'].get('notes',[])if 'two common'not in v and not v.startswith('The necessary D8 Morita rings have three types')]
                r['categorification_scope']['notes'].append('The necessary D8 Morita rings have three types in their union: zero or reflection shift for commutative sources; reflection or rotation for R1975. Only the reflection type overlaps. None is a model without compatible associators.')
        if not changed:continue
        if name=='rank9_rank10_m1.json':
            s=data['summary'];s.update(ledger_path=LEDGER,ledger_sha256=current['sha256'],ledger_url=current['url'],theoretical_retry=EVIDENCE,source_url=URL+'/tree/'+ref+'/'+EVIDENCE)
            s['counts']={str(rank):dict(Counter(r['status']for r in data[key]if r['rank']==rank))for rank in (9,10)}
            s['totals']=dict(Counter(r['status']for r in data[key]));s['remaining_ids']=[]
            s['archive']={'url':'./downloads/theoretical-continuation-2026-10-24.zip','sha256':sha(repo/EVIDENCE/'replay.zip'),'bytes':(repo/EVIDENCE/'replay.zip').stat().st_size}
        write(path,data)
    p=repo/'site/dist/data/rank9_rank10_m1_build.json'
    if p.is_file():
        data=read(p);data.update(ledger_sha256=current['sha256'],counts=read(repo/'site/dist/data/rank9_rank10_m1.json')['summary']['counts'],theoretical_retry=EVIDENCE);write(p,data)

def revise_document(name,text,repo=ROOT):
    if not active(repo):return text
    if name=='site/README.md':return (Path(repo)/'tools/templates/atlas_readme.md').read_text()
    text=text.replace('11 open cases','10 open cases').replace('11 unresolved rings','10 unresolved rings').replace('11 current open tensors','10 current open tensors').replace('11 open tensors','10 open tensors').replace('11 present questions','10 present questions')
    text=text.replace('across ranks six, eight, nine and ten','across ranks six, eight and nine')
    text=text.replace('136 exclusions, 57 unitary models and 1 unresolved','136 exclusions, 58 unitary models and no unresolved')
    text=text.replace('238 exclusions, 97 unitary models and 1 unresolved','238 exclusions, 98 unitary models and no unresolved')
    text=re.sub(r'\| 10 \| Multiplicity 1 \|.*?\|[^\n]*\n','| 10 | Multiplicity 1 | **Complete at multiplicity 1** | 136 excluded, 58 realized, 0 unresolved. |\n',text)
    text=text.replace('| ≥57 | 27 |','| 58 | 27 |').replace('evidence/rank10_m1_exclusions_20261023/accepted_ledger.csv',LEDGER.replace('.json','.csv'))
    text=re.sub(r'<!-- current-research-continuation -->.*?<!-- /current-research-continuation -->\n*','',text,flags=re.S)
    text=re.sub(r'<!-- current-theoretical-retry -->.*?<!-- /current-theoretical-retry -->\n*','',text,flags=re.S)
    if name.startswith('docs/') or name in ('manuscripts/README.md','site/README.md'):
        notice='''<!-- current-theoretical-retry -->
**Current results · 24 October 2026.** Rank ten at multiplicity one is complete:
136 general exclusions and 58 unitary models. R10_1_189 is recognized inside
the classical SU(4)_6 conformal-embedding module category. Ten cases remain
open at ranks six, eight and nine. Their new theoretical restrictions and
the actual twisted precursor for R8_3_1768 do not claim further decisions.
[Proofs and precise scope](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/unresolved_retry_20261024/README.md).
<!-- /current-theoretical-retry -->'''
        at=text.find('\n\n');text=text[:at]+'\n\n'+notice+text[at:]
    return text
