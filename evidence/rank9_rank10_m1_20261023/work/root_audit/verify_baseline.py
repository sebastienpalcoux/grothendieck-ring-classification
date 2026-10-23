#!/usr/bin/env python3
"""Replay every baseline positive obstruction using exact arithmetic.

No absence from a model catalogue is accepted as an obstruction.  In
particular the two rank-six subring references are replaced by direct
central-induction dimension witnesses.
"""
import sys,json,pathlib,collections,time
import sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[2]
W=ROOT/'work';sys.path.insert(0,str(W/'obstructions'))
import arithmetic as a, gng, two_dimension_induction as td
import involution_module as im, noncomm_integral as ni
from exact import require,check_cyclotomic,t
sys.path.insert(0,str(W/'obstructions/spectra'))
import run as spectrum

def check(R,c):
 k=c['kind']
 if k=='casimir_dnumber':
  q=s.Poly.from_list(c['factor'],t);p=a.casimir(R).charpoly(t).as_poly()
  co=list(map(int,q.all_coeffs()));d=q.degree();j=c['index'];N=abs(co[-1])
  require(q.is_irreducible and p.rem(q).is_zero and 1<=j<=d)
  r=pow(co[j],d,N**j);require(r!=0 and r==c['nonzero_remainder'])
 elif k=='cyclotomic':
  require(a.comm(R));check_cyclotomic([s.Matrix(A).charpoly(t).as_poly() for A in R],c)
 elif k=='near_group_small_m':
  got=a.near_group(R);require(got is not None)
  require(all(got.get(x)==v for x,v in c.items() if x!='reference'))
 elif k=='integral_drinfeld':require(a.integral_drinfeld(R)==c)
 elif k=='noncomm_integral_drinfeld':require(ni.test(R)==c)
 elif k in ('generalized_near_group_divisibility','nonabelian_tambara_yamagami'):gng.verify(R,c)
 elif k=='two_dimension_induction':td.verify(R,c)
 elif k=='involution_module':im.verify(R,c)
 elif k in ('zero_spectrum','one_spectrum'):spectrum.verify(R,c)
 elif k=='excluded_lower_subring':
  J=c['subset'];n=len(R);S=[[[R[i][j][k] for k in J]for j in J]for i in J]
  require(J[0]==0 and len(set(J))==len(J) and len(J)==c['subrank'])
  require(all(R[i][j][k]==0 for i in J for j in J for k in range(n) if k not in J))
  require(all(next(j for j in range(n) if R[i][j][0]) in J for i in J))
  require(a.sha(S)==c['subtensor_sha256'])
  sub=c.get('direct_subring_certificate') or td.certificate(S) or gng.certificate(S)
  require(sub is not None,'Catalogue absence is not a certificate')
  check(S,sub)
 else:raise ValueError('unsupported baseline certificate '+k)

def main():
 start=time.time();tensors={r['id']:r for r in a.read()};out=[];hist=collections.Counter()
 files=['arithmetic.json','structural.json','gng.json','noncomm_integral.json',
        'two_dimension_induction.json','module3.json','module_all.json',
        'spectra/zero_spectrum.json','spectra/one_spectrum.json']
 for rel in files:
  rows=json.load(open(W/'obstructions'/rel))
  if isinstance(rows,dict):rows=rows['records']
  num=0
  for r in rows:
   R=tensors[r['id']]['tensor'];require(r['tensor_sha256']==a.sha(R),'Tensor identity')
   for c in r.get('certificates',([r['certificate']]if r.get('certificate')else [])):
    check(R,c);num+=1;hist[c['kind']]+=1
    if c['kind']=='excluded_lower_subring' and not c.get('direct_subring_certificate'):
     J=c['subset'];S=[[[R[i][j][k] for k in J]for j in J]for i in J]
     c=dict(c,direct_subring_certificate=td.certificate(S) or gng.certificate(S))
    out.append({'id':r['id'],'tensor_sha256':a.sha(R),'source':'work/obstructions/'+rel,'certificate':c})
  print('PASS',rel,num,flush=True)
 result={'status':'PASS','certificate_count':len(out),'distinct_excluded':len({r['id']for r in out}),
         'criterion_counts':dict(hist),'seconds':time.time()-start,'records':out}
 (W/'root_audit/baseline_verified.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)
if __name__=='__main__':main()
