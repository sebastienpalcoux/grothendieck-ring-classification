"""General characteristic-zero exclusion by a closed, dual-stable rank-six subring.

The full nested certificate is replayed against the actual restricted tensor.
The census identifier is provenance only and has no role in the verifier.
"""
import itertools,json,sys
from pathlib import Path
P=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(P/'supplements/rank7/software'))
from exact import require
from rings import dual
from check import verify as verify_nested

def verify(R,c):
 require(c['kind']=='certified_rank6_subring','wrong certificate kind')
 J=c['subset'];n=len(R)
 require(len(J)==6 and J[0]==0 and len(set(J))==6 and all(type(i) is int and 0<=i<n for i in J),'invalid subset')
 du=dual(R)
 require(all(du[i] in J for i in J),'not dual stable')
 require(all(not R[i][j][k] for i in J for j in J for k in range(n) if k not in J),'not closed')
 T=[[[R[i][j][k] for k in J] for j in J] for i in J]
 p=c['permutation'];require(p[0]==0 and sorted(p)==list(range(6)),'invalid permutation')
 S=[[[T[i][j][k] for k in p] for j in p] for i in p]
 verify_nested(S,c['nested_certificate'])
 return True

if __name__=='__main__':
 rows={r['id']:r for r in json.load(open(P/'supplements/rank7/output/m5/survivors.json'))}
 inv=json.load(open(Path(__file__).with_name('structural_invariants.json')))
 out=[]
 for r in inv:
  for m in r['rank6_matches']:
   if m['status']!='excluded':continue
   c={'kind':'certified_rank6_subring','subset':m['subset'],'permutation':m['permutation'],'nested_certificate':m['certificate'],'source_id':m['id']}
   verify(rows[r['id']]['tensor'],c)
   out.append({'id':r['id'],'scope':'all complex fusion categories','certificate':c,'replayed':True})
   print(r['id'],m['id'],'PASS',flush=True)
 Path(__file__).with_name('rank6_subring_certificates.json').write_text(json.dumps(out,indent=2)+'\n')
