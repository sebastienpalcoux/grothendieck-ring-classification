#!/usr/bin/env python3
"""Verify the sole new decision, current public records and portable exact proofs."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess,sys
from unresolved_retry_20261024 import validate,EVIDENCE,NEW,FINDINGS
from current_frontier import identifiers

ROOT=Path(__file__).resolve().parents[1]
def need(x,message):
    if not x:raise ValueError(message)
def read(p):return json.loads(Path(p).read_text())

def run_exact(repo=ROOT):
    script=Path(repo)/NEW/'verify_retry.py'
    command=[sys.executable]+(['-O']if sys.flags.optimize else [])+[str(script)]
    result=subprocess.run(command,cwd=repo,text=True,capture_output=True)
    need(result.returncode==0,'Portable exact retry replay failed:\n'+result.stdout+result.stderr)
    receipt=read(Path(repo)/NEW/'verification_receipt.json')
    need(receipt['status']=='PASS' and len(receipt['checks'])==13,'Complete portable replay inventory')
    return {'status':'PASS','exact_verifiers':13,'assertions_disabled_in_children':True}

def main(metadata_only=False):
    result=validate(ROOT);ids=identifiers(ROOT)
    expected=['R6_4_155','R6_8_1660','R8_3_928','R8_3_941','R8_3_1154','R8_3_1768','R9_2_137','R9_2_1607','R9_2_1975','R9_2_1976']
    need(ids==expected,'Exact ten-case current frontier')
    records={}
    for name in ('unresolved_cases.json','resolved_cases.json','rank9_rank10_m1.json','rank9_m2.json'):
        data=read(ROOT/'site/dist/data'/name)
        records.update({r['id']:r for r in data['cases']})
    for rid in FINDINGS:
        row=records[rid]
        need(row['research'][0]['title'] in ('Current theoretical continuation','Current accepted case decision'),'Current findings presented first: '+rid)
        need(any(r.get('title')=='Current theoretical continuation'for r in row['research']),'Missing theoretical progress: '+rid)
        for item in row['evidence']:
            if not item['path'].startswith(EVIDENCE+'/'):continue
            p=ROOT/item['path'];need(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],'Bound research source: '+item['path'])
    model=records['R10_1_189']
    need(model['status']=='unitarily_realized' and model['existence']=='unitary','Unitary model is publicly classified')
    need(all(v=='realized'for v in model['categorification_scope']['level_status'].values()),'Positive categorical existence levels')
    need(model['categorification_scope']['braided']['status']=='excluded','Retain the independent braided obstruction')
    need(all(records[r]['status']=='unresolved'for r in expected),'No further categorical decision was inferred')
    payload=read(ROOT/'site/dist/data/rank9_rank10_m1.json')
    need(payload['summary']['counts']['10']=={'excluded':136,'unitarily_realized':58},'Current complete rank-ten partition')
    revision=read(ROOT/'data/current_publication_revision.json')
    need(revision['remaining_ids']==expected and revision['current_unresolved_total']==10,'Current publication frontier')
    need(revision['rank9_rank10_m1']['unitarily_realized']==98 and revision['rank9_rank10_m1']['unresolved']==0,'Combined multiplicity-one count')
    assignment=(ROOT/'publications/rank9-rank10/paper/assignment.tex').read_text().replace('\\_','_')
    table=dict(re.findall(r'\\texttt\{(R(?:9|10)_1_\d+)\}: \\textbf\{([EU?])\}',assignment))
    ledger=read(ROOT/EVIDENCE/'rank9_rank10_m1_ledger.json')['records']
    need(len(table)==336 and all(table[r['id']]==('U'if r['status']=='unitarily_realized'else'E')for r in ledger),'All 336 printed assignment symbols match the current ledger')
    need('**10 open cases.**'in(ROOT/'README.md').read_text(),'README frontier')
    need('| 10 | Multiplicity 1 | **Complete at multiplicity 1** | 136 excluded, 58 realized, 0 unresolved. |'in(ROOT/'README.md').read_text(),'README complete rank-ten band')
    if not metadata_only:result['portable_replay']=run_exact()
    result['scope']='One actual unitary categorification; ten open source rings; proof checks do not constitute independent human verification.'
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--metadata-only',action='store_true');args=parser.parse_args();main(args.metadata_only)
