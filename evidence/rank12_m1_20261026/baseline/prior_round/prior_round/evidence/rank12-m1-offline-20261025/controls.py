"""Corrupted-witness rejection and categorical-scope controls."""
from pathlib import Path
from copy import deepcopy
import json
import verify as V
ROOT=Path(__file__).resolve().parent
def main():
    checks=[]
    def rejects(name,fn):
        try:fn()
        except(ValueError,AssertionError):checks.append(name);return
        raise ValueError('invalid witness accepted: '+name)
    a=next(r for r in json.loads((ROOT/'arithmetic.json').read_text())if any(c['kind']=='casimir_dnumber'for c in r['certificates']))
    c=deepcopy(next(c for c in a['certificates']if c['kind']=='casimir_dnumber'));c['nonzero_remainder']=0
    rejects('zero d-number remainder rejected',lambda:V.arithmetic(V.data[a['id']],c))
    a=next(r for r in json.loads((ROOT/'cyclic.json').read_text())['records']if r['certificate']);c=deepcopy(a['certificate']);c['order']+=1
    rejects('forged cyclic order rejected',lambda:V.cyclic(V.data[a['id']],c))
    a=next(r for r in json.loads((ROOT/'feudal.json').read_text())['records']if r['certificate']);c=deepcopy(a['certificate']);c['contradictions'][0]['row_combination']=[]
    rejects('empty Liptrap contradiction rejected',lambda:V.liptrap_negative(V.data[a['id']],c))
    a=next(r for r in json.loads((ROOT/'feudal.json').read_text())['records']if r['model']);c=deepcopy(a['model'])
    for row in c['phase_values']:
        if row[0]=='chi':row[-1]=0
    rejects('degenerate Liptrap bicharacter rejected',lambda:V.liptrap_positive(V.data[a['id']],c))
    eligible={r['id']for r in json.loads((ROOT/'primary.json').read_text())['records']}
    V.need('R12_1_25'not in eligible and len(V.s.factorint(120))==3,'three-prime dimension is not the solvability gate');checks.append('dimension120 not promoted by the p^a q^b unitarity gate')
    attempts=json.loads((ROOT/'induction.json').read_text())['records']
    V.need(all(not r['certificate']for r in attempts if 'budget'in r['attempt']['result']),'budgets are no conclusion');checks.append('limited induction attempts are not exclusions')
    out=dict(status='PASS',checks=checks)
    (ROOT/'controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
