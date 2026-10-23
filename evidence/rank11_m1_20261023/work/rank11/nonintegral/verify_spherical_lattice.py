"""Independent separating-functional verification of 34 lattice exclusions.

The checker does not call Hermite normal form, factor discovery, or lattice
search. It verifies each saved rational functional is integer on every simple
categorical dimension and noninteger on a mandatory central-object dimension.
The scalar inventory and sign descent have separate independent replay.
"""
from pathlib import Path
import sys,json,time
import sympy as s
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
sys.path[:0]=[str(ROOT/'work/obstructions'),str(ROOT/'work/rank11')]
from exact import poly,field,vector,evaluate
from common import read,sha,require,dual

def verify():
 rows=read();original={r['id']:r for r in json.load(open(P/'original.json'))};signs={r['id']:r for r in json.load(open(P/'signed.json'))};out=[];cert_count=0
 for r in json.load(open(P/'spherical_lattice.json')):
  if not r['all_spherical_dimension_characters_excluded']:continue
  id=r['id'];R=rows[id];rr=original[id];require(sha(R)==r['tensor_sha256']==rr['tensor_sha256']==signs[id]['tensor_sha256'],'source identity')
  require(signs[id]['all_categorical_signed_tables_are_gauge_original'],'spherical descent is certified')
  require(len(r['branches'])==len(rr['branches']),'complete branch list');du=dual(R);branch_checks=[]
  for b,o in zip(r['branches'],rr['branches']):
   require(b['factor']==o['factor'],'ordered dimension branches')
   if o['obstruction']:
    require(b.get('earlier_obstruction')==o['obstruction'],'previous independently checked obstruction');branch_checks.append('previous_scalar_obstruction');continue
   c=b['certificate'];require(c is not None,'all dimension branches excluded');p=poly(b['factor']);K=field(p);m=p.degree();ds=[K(list(map(s.Rational,co)))for co in o['dimensions']];D=sum((ds[i]*ds[du[i]]for i in range(len(ds))),K.zero)
   q=poly(c['codegree_polynomial']);require(any(poly(f['polynomial'])==q for f in rr['formal_codegree_factors']),'actual formal codegree factor')
   f=K(list(map(s.Rational,c['codegree'])));require(f and evaluate(q.all_coeffs(),f,K)==K.zero,'exact root')
   beta=D/f;require(beta==K(list(map(s.Rational,c['required_dimension']))),'central dimension delta/f')
   ell=s.Matrix([list(map(s.Rational,c['separating_functional']))]);require(ell.shape==(1,m),'functional length')
   values=[(ell*vector(x,m))[0]for x in ds];target=(ell*vector(beta,m))[0]
   require(all(x.q==1 for x in values),'integer on the entire simple-dimension lattice')
   require(target.q!=1,'noninteger on required central dimension')
   require(list(map(str,values))==c['simple_functional_values'] and str(target)==c['required_functional_value'],'functional receipt')
   branch_checks.append(dict(codegree_polynomial=c['codegree_polynomial'],required_functional_value=str(target)));cert_count+=1
  out.append(dict(id=id,tensor_sha256=sha(R),scope='general_complex_with_independent_signed_and_scalar_replay',checks=branch_checks))
 require(len(out)==34,'expected 34 exact exclusions')
 return out,cert_count
if __name__=='__main__':
 start=time.monotonic();out,count=verify();receipt=dict(status='PASS',records=len(out),separating_functionals=count,seconds=time.monotonic()-start,results=out)
 (P/'lattice_replay.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items()if k!='results'},indent=2),flush=True)
