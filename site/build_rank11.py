#!/usr/bin/env python3
"""Publish the source-bound rank-eleven extension after the older builders."""
import argparse,ast,hashlib,json,re,shutil
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp
from build_realized import tensor_checks
from build_rank9_10 import CONVENTION,REPO_URL,sha,write_json

HERE=Path(__file__).resolve().parent
RELEASE='evidence/rank11_m1_20261023'
MODEL_NAMES={
 1:'Rep(D32)',10:'TY(C12) equivariantized by C2, positive parity',
 24:'SU(2)6 equivariantized by the spin-current C2 action, odd coherence',
 26:'SU(2)10',28:'PSU(2)20',30:'SO(8)2',37:'SO(15)2',45:'Rep(D38)',46:'PSU(2)21',
 48:'Twisted Vec(C16) equivariantized by inversion',57:'V4 zest of SO(8)2, parameters (0,0,0,2)',
 64:'TY(C3 × C2²) equivariantized by C2, positive parity',
 68:'SU(2)6 equivariantized by the spin-current C2 action, trivial coherence',
 72:'TY(C12) equivariantized by C2, negative parity',75:'TY(C15) equivariantized by C2, negative parity',
 103:'C2 zest of SU(2)10',104:'Group-theoretical category C(G32, ω, V4, 1)',
 105:'V4 zest of SO(8)2, parameters (0,0,0,1)',112:'Vec(C16) equivariantized by multiplication by 7',
 113:'TY(C3 × C2²) equivariantized by C2, negative parity',
 146:'Twisted Vec(C16) equivariantized by multiplication by 7',
 150:'V4 zest of SO(8)2, parameters (2,0,0,3)',157:'TY(C3²) equivariantized by C2, positive parity',
 171:'TY(C10)',176:'TY(C3²) equivariantized by C2, negative parity',
 179:'Izumi Q8 near-group category equivariantized by triality C3',182:'Vec(C11)'}

def build(repo,ref='main'):
    source=repo/RELEASE;dist=repo/'site/dist';base=source/'work/rank11'
    ledger_path=base/'ledger.json';ledger=json.loads(ledger_path.read_text())
    tensors=json.loads((base/'tensors.json').read_text())
    rows=ledger['records'];expected={f'R11_1_{i}' for i in range(1,183)}
    if len(rows)!=182 or {r['id'] for r in rows}!=expected or set(tensors)!=expected:
        raise ValueError('Incomplete rank-eleven input inventory')
    counts=dict(Counter(r['status'] for r in rows))
    if counts!={'unitarily_realized':27,'excluded':155} or ledger['counts']!=counts:
        raise ValueError('Classification partition mismatch')
    preserved={str(p.relative_to(repo)):sha(p) for p in (dist/'data').glob('*.json')
               if not p.name.startswith('rank11_') and p.name not in ('current_document_revision.json','current_publication_revision.json')}
    # All proof references are retained under their original portable paths.
    index={}
    def evidence(relative):
        p=(source/relative).resolve()
        if not p.is_relative_to(source.resolve()) or not p.is_file():
            raise ValueError('Missing or unsafe evidence: '+relative)
        if relative not in index:
            path=RELEASE+'/'+relative
            index[relative]={'label':relative,'path':path,'url':f'{REPO_URL}/blob/{ref}/{path}','sha256':sha(p)}
        return index[relative]
    def path_for(value):
        value=value.split(':',1)[0]
        if (source/value).is_file():return value
        if (base/value).is_file():return 'work/rank11/'+value
        raise ValueError('Missing ledger proof: '+value)
    profiles=[];folder=dist/'downloads/fusion-tensors';folder.mkdir(parents=True,exist_ok=True)
    for row in rows:
        rid=row['id'];tensor=tensors[rid]
        digest=hashlib.sha256(json.dumps(tensor,separators=(',',':')).encode()).hexdigest()
        if digest!=row['tensor_sha256_compact_json']:raise ValueError('Tensor identity: '+rid)
        a,dual=tensor_checks(tensor)
        if len(a)!=11 or int(a.max())!=1 or dual!=row['dual']:raise ValueError('Tensor axioms: '+rid)
        if bool(np.array_equal(a,a.transpose(1,0,2)))!=row['commutative']:raise ValueError('Commutativity: '+rid)
        text=json.dumps(tensor,indent=2)+'\n'
        if ast.literal_eval(text)!=tensor:raise ValueError('Tensor literal round-trip')
        (folder/(rid+'.txt')).write_text(text)
        model=row['status']=='unitarily_realized'
        if bool(row['models'])!=model or bool(row['exclusions'])==model:raise ValueError('Proof/model scope: '+rid)
        chosen=row['models'][0] if model else row['exclusions'][0]
        paths={'README.md','RESULTS.json','VERIFICATION.md','SHA256SUMS','work/rank11/ledger.json',
               'work/rank11/tensors.json','work/rank11/replay_all.py','work/rank11/criteria_audit/CRITERIA_AUDIT.md'}
        for receipt in row['models']+row['exclusions']:
            for key in ('proof','certificate','categorical_review'):
                if isinstance(receipt.get(key),str):paths.add(path_for(receipt[key]))
            for p in re.findall(r'(?:work|inputs|repositories)/[\w./+-]+\.py',receipt.get('verifier','')):
                if (source/p).is_file():paths.add(p)
        evidence_rows=[evidence(p) for p in sorted(paths)]
        ledger_source=evidence('work/rank11/ledger.json')
        name=MODEL_NAMES.get(row['input_line'],rid)
        if model:
            summary=f'A unitary realization exists: {name}. The construction and full tensor identification are verified; this does not classify all associators.'
        else:
            criterion=chosen.get('criterion',chosen.get('reason',chosen.get('method','the linked necessary-condition proof')))
            summary='Excluded from fusion categorification over ℂ by '+str(criterion).replace('_',' ')+'. The proof covers general complex fusion categories.'
        omega=sum((sp.Matrix(a[i].tolist())*sp.Matrix(a[dual[i]].tolist()) for i in range(11)),sp.zeros(11))
        poly=str(sp.factor(omega.charpoly(sp.Symbol('t')).as_expr()))
        inv={'dual_indices':dual,'invertible_indices':[i for i in range(11) if int(sum(a[i,dual[i]]))==1],
             'commutative':row['commutative'],'frobenius_perron_dimensions_approx':row['fp_dimensions_approx'],
             'global_fp_dimension_approx':row['fp_dimension_approx'],'central_casimir_polynomial':poly,
             'dimensions_method':'Numerical Frobenius–Perron dimensions from the original tensor; displayed values are approximate.',
            'character_method':'Exact character calculations and certificates are included in the linked verification package.'}
        if row['commutative']:inv['formal_codegree_polynomial']=poly
        sources=[{'label':'Accepted case proof and certificate record','path':ledger_source['path'],
                  'url':ledger_source['url'],'sha256':ledger_source['sha256']}]
        scope={'general_status':'realized' if model else 'excluded',
               'level_status':{k:('realized' if model else 'excluded') for k in ('general','pivotal','spherical','pseudo_unitary','unitary')},
               'strongest_excluded':None if model else 'general','same_category_implications':[],
               'existence_implications':[],'notes':[summary],'audit_sources':sources}
        if not model:scope['braided']={'status':'excluded','explanation':'General nonexistence also excludes a braided categorification.','sources':sources}
        profiles.append({'id':rid,'rank':11,'multiplicity':1,'status':row['status'],'summary':summary,
            'name':name,'existence':'unitary' if model else 'excluded','model_reference':chosen.get('scope',''),
            'model_reference_url':ledger_source['url'],'source_file':ledger_source['path'],'source_url':ledger_source['url'],
            'source_location':rid,'report_url':'./papers/rank11.pdf','report_label':'Rank-eleven classification manuscript',
            'case_url':f'./case.html?id={rid}','fusion_tensor':tensor,'tensor_sha256':digest,
            'basis':[f'X{i}' for i in range(11)],'unit_index':0,'tensor_convention':CONVENTION,
            'hash_convention':'SHA-256 of UTF-8 compact JSON, without a trailing newline.','invariants':inv,
            'research':[{'title':'Current accepted case decision','source':ledger_source['path'],'url':ledger_source['url'],
                         'source_sha256':ledger_source['sha256'],'data':row}],
            'evidence':evidence_rows,'categorification_scope':scope,'download_url':f'./downloads/fusion-tensors/{rid}.txt',
            'investigation_deferred':False})
    summary={'date':'2026-10-23','release':RELEASE,'input_count':182,'counts':{'11':counts},'totals':counts,
        'ledger_sha256':sha(ledger_path),'ledger_url':f'{REPO_URL}/blob/{ref}/{RELEASE}/work/rank11/ledger.json',
        'source_url':f'{REPO_URL}/tree/{ref}/{RELEASE}','report_url':'./papers/rank11.pdf','remaining_ids':[],
        'census_url':'https://github.com/sebastienpalcoux/fusion-ring-census/tree/main/verification/rank11',
        'enumeration_qualification':'Producer-reported complete enumeration; independent tensor and uniqueness checks; full enumeration not independently rerun.',
        'current_documents':{'path':'data/current_publication_revision.json','sha256':sha(repo/'data/current_publication_revision.json'),'date':'2026-10-23'}}
    archive=dist/'downloads/Rank11_Multiplicity1_2026-10-23.zip'
    if archive.is_file():summary['archive']={'url':'./downloads/'+archive.name,'sha256':sha(archive),'bytes':archive.stat().st_size}
    write_json(dist/'data/rank11_m1.json',{'schema':'ring-atlas/rank11-m1/v1','summary':summary,'cases':profiles})
    for p,digest in preserved.items():
        if sha(repo/p)!=digest:raise ValueError('Prior classification data changed: '+p)
    write_json(dist/'data/rank11_m1_build.json',{'records':182,'counts':counts,'ledger_sha256':sha(ledger_path),
        'legacy_sha256':preserved,'tensor_downloads':182})
    shutil.copy2(repo/'publications/rank11/paper/rank11.pdf',dist/'papers/rank11.pdf')
    shutil.copy2(repo/'data/current_publication_revision.json',dist/'data/current_publication_revision.json')
    shutil.copy2(repo/'data/current_manuscript_page_counts.json',dist/'downloads/current_manuscript_page_counts.json')
    for html in dist.glob('*.html'):
        text=html.read_text()
        for asset in ('app.js','cases.js','catalogue.js','redirect.js','styles.css','cases.css'):
            digest=sha(dist/asset)[:12]
            text=re.sub(r'(\b(?:src|href)="\./'+re.escape(asset)+r')(?:\?v=[^\"]*)?(\")',
                        lambda m:m[1]+'?v='+digest+m[2],text)
        if text!=html.read_text():html.write_text(text)
    print('Rank-eleven extension built: 182 profiles, 182 tensors, 155 exclusions, 27 unitary models; older ledgers preserved.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--classification',type=Path,default=HERE.parent);p.add_argument('--ref',default='main')
    a=p.parse_args();build(a.classification.resolve(),a.ref)
