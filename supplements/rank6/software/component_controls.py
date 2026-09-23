"""Regression tests for the established multiplicity-1--7 source prefix.

Classification may improve when a new proved criterion or model is added.
These tests preserve the census prefix and exact checker mutation controls,
without treating an older research ledger as an immutable result.
"""
from pathlib import Path
import json,copy,time,collections
from fractions import Fraction
from exact import require,VerificationError,poly
from rings import Characters
from existence import verify_ledger,structure_only_records
from unittest.mock import patch
from import_repository import verify_source
import dimension_order,signed_spherical_traces,through7_models
P=Path(__file__).resolve().parents[1]
(P/'verification/current').mkdir(parents=True,exist_ok=True)

def reject(fn):
 try:fn()
 except (VerificationError,ValueError,KeyError,IndexError):return
 raise RuntimeError('a deliberately corrupted certificate was accepted')
def run():
 start=time.monotonic();rows=json.load(open(P/'data/census.json'));idx={r['id']:r for r in rows};ledger=json.load(open(P/'data/decisions.json'));by={r['id']:r for r in ledger}
 prefix=[r for r in rows if r['m']<=7]
 require(len(prefix)==9613 and [sum(r['m']==m for r in prefix) for m in range(1,8)]==[39,154,384,872,1582,2768,3814],'established source count prefix')
 source=verify_source(rows)
 verify_ledger(ledger)
 require(all(x['id'] in idx and x['structure']=='pseudo_unitary' for x in structure_only_records()),'structure-only scope')
 record=next(json.loads(l) for l in open(P/'certificates/dimension_order_general.jsonl') if json.loads(l)['id']=='R6_4_375')
 sphere=record['certificate']['sphere'];a=Characters(idx[record['id']]['N'],sphere['generator'])
 cases=[x for x in sphere['characters'] if x['obstruction']['kind']=='dimension_order']
 for x in cases:
  f=poly(x['factor']);c=x['obstruction'];dimension_order.verify(a,f,c)
  for field in ['value','functional','root','hermite_basis']:
   bad=copy.deepcopy(c)
   if field=='value':bad[field]='0'
   elif field=='functional':bad[field][0]=str(Fraction(bad[field][0])+1)
   elif field=='root':bad[field]=['0']
   else:bad[field][0][0]=str(int(bad[field][0][0])+1)
   reject(lambda bad=bad:dimension_order.verify(a,f,bad))
 sr=json.load(open(P/'certificates/signed_spherical_general.json'))[0];sp=sr['certificate']['sphere'];aa=Characters(idx[sr['id']]['N'],sp['generator'])
 comp=next(x for x in sp['characters'] if x['obstruction']['kind']=='signed_spherical_traces');c=comp['obstruction']['certificate'];f=poly(comp['factor'])
 # Full 128-case proofs run in verify.py; these mutation controls fail at input validation.
 meta=copy.deepcopy(c['table']);meta['characters'][0][0]=['2']
 reject(lambda:signed_spherical_traces.data_and_table(idx[sr['id']]['N'],aa,f,meta))
 models=through7_models.verify();original=list(through7_models.examples());bad=copy.deepcopy(original);bad[0][1][1][1][1]+=1
 with patch('through7_models.examples',return_value=iter(bad)):reject(through7_models.verify)
 targets=sorted({r['id'] for r in [json.loads(l) for l in open(P/'certificates/dimension_order_general.jsonl')]}|{r['id'] for r in json.load(open(P/'data/model_catalog.json'))})
 require(set(targets)<=set(idx),'component eligibility references absent tensor')
 coverage=[{'id':rid,'commutative':idx[rid]['commutative'],'scope':'eligible for commutative component screening' if idx[rid]['commutative'] else 'outside commutative signed-trace scope'} for rid in targets]
 (P/'verification/component_eligibility.json').write_text(json.dumps(coverage,indent=2)+'\n')
 return dict(passed=True,optimized_python=not __debug__,seconds=time.monotonic()-start,source_prefix_tensors=len(prefix),source=source,dimension_order_components=len(cases),order_mutations_rejected=4*len(cases),signed_character_mutation_rejected=True,model_mutation_rejected=True,models=models,counts=dict(collections.Counter(d['status'] for d in ledger)),source_hashes_verified=True,eligibility_records=len(coverage),noncommutative_outside_scope=sum(not idx[x]['commutative'] for x in targets))

if __name__=='__main__':
 result=run();name='component_controls_optimized.json' if not __debug__ else 'component_controls_normal.json';(P/'verification/current'/name).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
