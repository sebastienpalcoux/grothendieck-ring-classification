"""Finite exact branching on the remaining central-semion integer domain."""
from pathlib import Path
import json,math,sys,time
from domain_probe import rows_for,propagate
from hybrid_probe import prune,dual_or_point
HERE=Path(__file__).resolve().parent

def main(fi,bi,limit=1000):
 start=time.monotonic();d,rows,rank=rows_for(f'central_frame{fi}');rr=rows[len(d['rhs']):len(d['rhs'])+rank]
 pr=json.loads((HERE/f'central_frame{fi}_result.json').read_text());rootdomains=pr['propagation']['domains']
 phase=json.loads((HERE/f'phasecut_frame{fi}.json').read_text());branch=phase['branches'][bi];keep=d['metadata']['source_metadata']['retained_indices'];lower=d['source_lower']
 ineq=[[c[j]for j in keep]+[b-sum(x*y for x,y in zip(c,lower))]for c,b in zip(phase['rounded_coefficients'],branch['rounded_rhs'])]
 out={'frame':fi,'indicator_branch':bi,'indicators':branch['indicators'],'status':'running','node_limit':limit,'nodes':0,'tree':{}}
 def save(): (HERE/f'central_f{fi}_b{bi}_branch.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
 def visit(node,domains,seed=None,depth=0):
  out['nodes']+=1
  if out['nodes']>limit:node['status']='node_limit';return False
  prop=propagate(rows,domains,seedvars=seed,record_steps=True);node['equality_propagation']=prop
  if prop['outcome']=='exact_domain_obstruction':node['status']='exact_equality_domain_obstruction';return True
  more=prune(rows,ineq,prop['domains']);node['inequality_propagation']=more
  if more['status']!='consistent':node['status']=more['status'];return True
  dom=more['domains'];lp=dual_or_point(rr,ineq,dom)
  if lp['status']!='fractional_proposal':node.update(lp);return lp['status']=='exact_bounded_linear_obstruction'
  x=lp['values'];rounded=[round(v)for v in x]
  valid=all(rounded[j]in dom[j]for j in range(len(dom)))and all(sum(a*v for a,v in zip(row[:-1],rounded))==row[-1]for row in rr)and all(sum(a*v for a,v in zip(row[:-1],rounded))<=row[-1]for row in ineq)
  if valid:node.update(status='exact_integer_survivor',values=rounded);out['integer_survivor']=rounded;return False
  choices=[]
  for j,v in enumerate(x):
   if len(dom[j])<2:continue
   k=math.floor(v);left=[a for a in dom[j]if a<=k];right=[a for a in dom[j]if a>k]
   if not left or not right:continue
   if abs(v-round(v))>1e-7 or round(v)not in dom[j]:choices.append((min(v-left[-1],right[0]-v),-len(dom[j]),j,k,left,right))
  if not choices:node.update(status='numerical_unresolved_no_split');return False
  _,_,j,k,left,right=max(choices)
  node.update(status='split',variable=j,cut=k,children=[{},{}])
  if out['nodes']%10==1:print('node',out['nodes'],'depth',depth,'split',j,k,'seconds',round(time.monotonic()-start,2),flush=True);save()
  a=[list(v)for v in dom];a[j]=left
  if not visit(node['children'][0],a,[j],depth+1):return False
  a=[list(v)for v in dom];a[j]=right
  return visit(node['children'][1],a,[j],depth+1)
 complete=visit(out['tree'],rootdomains)
 out['status']='exact_bounded_integer_obstruction'if complete else'incomplete_or_survivor';out['seconds']=time.monotonic()-start;save();print(out['status'],'nodes',out['nodes'],'seconds',out['seconds'],flush=True)
if __name__=='__main__':main(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])if len(sys.argv)>3 else 1000)
