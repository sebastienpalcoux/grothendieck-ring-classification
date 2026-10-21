"""Fast exact verification of every exclusion witness, closure, and positive control.
Surviving row systems are conservatively retained; they are not needed to prove
an exclusion. Every rejected row system is re-enumerated completely.
"""
import json,sys
import sympy as s
from gram_discovery import HERE,REPO,require
from integral_gram import bounded_solutions
from module_rows import FLOORS
from verify_sources import verify
from morita_closure import run as morita_run
from profile_closure import run as profile_run
from trace_closure import run as trace_run
from action_classes import run as actions_run
from verify_final import verify_final

def run():
 verify()
 src={x['id']:x for x in json.loads((REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())};gs={(x['id'],x['candidate_index']):x for x in json.loads((HERE/'integral_gram.json').read_text())};rs=json.loads((HERE/'module_rows.json').read_text());require(len(rs)==len(gs),'row stage coverage');checked=0
 for rec in rs:
  rid=rec['id'];g=gs[(rid,rec['candidate_index'])];R=src[rid]['tensor'];a=g['algebra_object'];V=g['vectors'];require(rec['algebra_object']==a,'row object source');checks=rec['factor_checks'];require(len(checks)==len(g['all_multiplicities'])and [x['factor_index']for x in checks]==list(range(len(checks))),'all factor checks')
  require(rec['surviving_factor_indices']==[x['factor_index']for x in checks if x['obstruction']is None],'survivor set')
  for c in checks:
   bad=c['obstruction']
   if bad is None:continue
   checked+=1;ns=g['all_multiplicities'][c['factor_index']];active=[j for j,n in enumerate(ns)if n];W=[V[j]for j in active];mult=[ns[j]for j in active];uindex=bad['row_type_index'];require(uindex in active,'obstructed row exists');u=V[uindex];i=bad['simple'];require(1<=i<8,'valid simple');b=[sum(u[k]*R[i][j][k]for k in range(8))-u[i]*a[j]for j in range(8)];require(b==bad['rhs'],'obstruction RHS')
   if bad['kind']=='negative_rhs':require(any(x<0 for x in b),'negative RHS witness')
   elif bad['kind']=='integer_row_obstruction':
    require(all(x>=0 for x in b),'nonnegative RHS');bounds=[min([n*FLOORS[rid][i]]+[b[k]//v[k]for k in range(8)if v[k]])for v,n in zip(W,mult)];require(bounds==bad['bounds'],'complete entry bounds');sol,_=bounded_solutions(s.Matrix(W).T,b,bounds);require(not sol,'exact row impossibility')
   else:raise ValueError('unknown obstruction')
 print('All',checked,'rejected induction-factor row witnesses verified exactly.')
 morita_run();profile_run();trace_run();actions_run();final=verify_final(replay=False)
 final['all_exclusion_certificates_reverified']=True;final['optimization_level']=sys.flags.optimize;final['row_exclusion_witnesses_verified']=checked
 (HERE/'verification.json').write_text(json.dumps(final,separators=(',',':'))+'\n')
 print('PASS exact certificate verification; Python optimization level',sys.flags.optimize)
if __name__=='__main__':run()
