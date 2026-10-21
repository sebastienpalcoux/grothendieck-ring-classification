from pathlib import Path
import json,sys,time
from domain_probe import rows_for,propagate
from hybrid_probe import prune,dual_or_point
HERE=Path(__file__).resolve().parent

def main(fi,dual=False):
 prefix="central_dual" if dual else "central"
 start=time.monotonic();d,rows,rank=rows_for(f'{prefix}_frame{fi}');base=json.loads((HERE/f'frame{fi}_domains.json').read_text())
 domains=[set(v)for v in base['domains']];parity_removed=[]
 for j,residue,original in d['central_action_parities']:
  rem=sorted(x for x in domains[j]if x%2!=residue);domains[j].difference_update(rem)
  parity_removed.append([j,residue,original,rem])
  if not domains[j]:raise AssertionError('parity alone empties a mass domain')
 result=propagate(rows,domains,record_steps=True)
 report={'frame':fi,'scope':'pseudo_unitary_indicator_g_minus_one','parity_deletions':parity_removed,'propagation':result,'rank':rank,'branches':[]}
 (HERE/f'{prefix}_frame{fi}_result.json').write_text(json.dumps(report,separators=(',',':'))+'\n')
 print('central propagation',result['outcome'],'deleted',result['deletions'],'fixed',sum(len(v)==1 for v in result['domains']),'seconds',time.monotonic()-start,flush=True)
 if result['outcome']!='exact_domains_consistent':return
 rr=rows[len(d['rhs']):len(d['rhs'])+rank];phase=json.loads((HERE/f'phasecut_frame{fi}.json').read_text());keep=d['metadata']['source_metadata']['retained_indices'];lower=d['source_lower']
 for bi in(0,4):
  branch=phase['branches'][bi];ineq=[[c[j]for j in keep]+[b-sum(x*y for x,y in zip(c,lower))]for c,b in zip(phase['rounded_coefficients'],branch['rounded_rhs'])]
  pr=prune(rows,ineq,result['domains']);rec={'branch':bi,'indicators':branch['indicators'],'domain_propagation':pr}
  if pr['status']=='consistent':rec['linear']=dual_or_point(rr,ineq,pr['domains']);print('branch',bi,rec['linear']['status'],flush=True)
  else:print('branch',bi,pr['status'],flush=True)
  report['branches'].append(rec);(HERE/f'{prefix}_frame{fi}_result.json').write_text(json.dumps(report,separators=(',',':'))+'\n')
if __name__=='__main__':main(int(sys.argv[1]),'--dual'in sys.argv)
