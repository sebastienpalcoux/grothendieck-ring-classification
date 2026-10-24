#!/usr/bin/env python3
"""Verify all M2 publication identities, tensor downloads, model maps and scopes."""
import ast,hashlib,json,zipfile
from collections import Counter
from pathlib import Path
from check_cases import check_browser_integers,check_braided_scope,implication_closure
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'site/dist'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def main():
 p=read(DIST/'data/rank9_m2.json');summary=p['summary'];E=ROOT/summary['release'];ledger=read(E/'ledger.json');models={r['id']:r for r in read(E/'models.json')};original=read(E/'tensors.json');rows=p['cases'];expected={f'R9_2_{i}'for i in range(1,2084)}
 need(len(rows)==2083 and{r['id']for r in rows}==expected,'Case coverage')
 need([r['id']for r in rows]==[r['id']for r in ledger],'Source case order')
 need(dict(Counter(r['status']for r in rows))==summary['totals']=={'excluded':2033,'unitarily_realized':32,'unresolved':18},'Partition')
 need(sha(E/'ledger.json')==summary['ledger_sha256'],'Ledger hash')
 check_browser_integers(p,'rank9_m2');byid={r['id']:r for r in ledger};sources={}
 for r in rows:
  rid=r['id'];T=r['fusion_tensor'];literal=ast.literal_eval((DIST/'downloads/fusion-tensors'/(rid+'.txt')).read_text())
  need(T==literal==original[rid],'Tensor download: '+rid)
  need(hashlib.sha256(json.dumps(T,separators=(',',':')).encode()).hexdigest()==r['tensor_sha256']==byid[rid]['tensor_sha256'],'Tensor hash: '+rid)
  need(r['status']==byid[rid]['status']and r['research'][0]['data']==byid[rid],'Decision identity: '+rid)
  scope=r['categorification_scope'];level='realized'if r['status']=='unitarily_realized'else r['status'];need(set(scope['level_status'].values())=={level},'Structure scope')
  if rid in models:
   m=models[rid];q=m['basis_map_source_to_model'];N=m['tensor'];need(all(T[i][j][k]==N[q[i]][q[j]][q[k]]for i in range(9)for j in range(9)for k in range(9)),'Model transport')
  if r['status']=='unresolved':
   together=implication_closure(scope['same_category_implications']+scope['existence_implications']);need(('general','pseudo_unitary')in together,'Existence reduction')
   need(('general','unitary')not in together,'Unproved unitary existence')
   check_braided_scope(r,scope['braided'])
  for x in r['evidence']:sources[x['path']]=x
 for name,x in sources.items():need((ROOT/name).is_file()and sha(ROOT/name)==x['sha256'],'Evidence binding: '+name)
 need(sha(E/'replay.zip')==summary['archive']['sha256'],'Replay archive hash')
 with zipfile.ZipFile(E/'replay.zip')as z:
  root='Rank9_M2_Theoretical_Continuation_20261023/';m=json.loads(z.read(root+'SHA256SUMS.json'));need(all(hashlib.sha256(z.read(root+n)).hexdigest()==h for n,h in m.items()),'Archived source hashes')
 need((DIST/'papers/rank9-m2.pdf').read_bytes()==(ROOT/'publications/rank9-m2/paper/rank9-m2.pdf').read_bytes(),'Canonical manuscript copy')
 revision=read(ROOT/'data/current_publication_revision.json');need(len(revision['remaining_ids'])==revision['current_unresolved_total']==25,'Project frontier')
 need(set(summary['remaining_ids'])=={r['id']for r in rows if r['status']=='unresolved'},'M2 frontier')
 receipt=read(DIST/'data/rank9_m2_build.json')
 for name,h in receipt['legacy_sha256'].items():need(sha(DIST/'data'/name)==h,'Previous publication changed: '+name)
 for name,h in receipt.get('legacy_case_sha256',{}).items():need(hashlib.sha256(json.dumps(read(DIST/'data'/name)['cases'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==h,'Previous case decision changed')
 mod=ast.parse((ROOT/'data/current_remaining_cases.py').read_text());values={node.targets[0].id:ast.literal_eval(node.value)for node in mod.body if isinstance(node,ast.Assign)};need(set(values['TENSORS'])==set(revision['remaining_ids']),'Current open-tensor download')
 pages=read(ROOT/'data/current_manuscript_page_counts.json');need(sum(d['pages']for d in pages['documents']if d['kind']=='mathematical_manuscript')==pages['totals']['mathematical_manuscript'],'Page inventory')
 front=(ROOT/'README.md').read_text();rank9=[line for line in front.splitlines()if line.startswith('| 9 |')]
 need(len(rank9)==1 and 'Through 2' in rank9[0] and '2,135 excluded, 72 realized' in rank9[0],'Single current rank-nine README row')
 need('**25 open cases.**'in front,'Current README frontier')
 review=(DIST/'review.html').read_text();need('Current classification · 25 open questions'in review and 'rank-nine-m2'in review and 'rank-ten-m1'in review and 'rank-eleven-m1'in review,'Current review-page scope')
 need('./data/current_publication_revision.json'in review and './downloads/current_remaining_cases.py'in review,'Current review downloads')
 for name,x in revision['documents'].items():
  if name.startswith('publications/rank9-m2/'):need(sha(ROOT/name)==x['sha256'],'Manuscript source identity')
 print('Rank-nine M2: all2083 case/tensor identities,2033 exclusions,32 model transports,18 scopes,25 project open tensors and every archive hash PASS.')
if __name__=='__main__':main()
