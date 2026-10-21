"""Fourth moments with the forced central involution inserted."""
from charged_quartic_pair import *

def main():
 source=read(P/'source.json');domain=read(P/'gram_cubic.json')
 charged=read(HERE/'charged_quartic_pair.json');charges=read(P/'r941_charges.json')['solutions']
 pairs=list(cwr(range(1,5),2));quads=list(cwr(range(1,5),4));triples=list(cwr(range(1,5),3))
 lowcharges=[1,1,1,1,-1]; translated=[40,41,42,43,57];results=[]
 for rec,previous in zip(source['records'],charged['records']):
  semion=rec['id'].endswith('928');mg=-1 if semion else 1
  chars=[[tuple(map(F,x)) for x in ch] for ch in rec['full_characters']];D=tuple(map(F,rec['formal_codegrees'][0]))
  lows=rec['low_columns']; highs=[(0,)+tuple(v) for v in rec['canonical_high_vectors']];cols=lows+highs
  beta=[scale(div(D,tuple(map(F,f))),F(1,n)) for f,n in zip(rec['formal_codegrees'],rec['irreducible_dimensions'])]
  vals=[[mul(b,fp(v,ch)) for b,ch in zip(beta,chars)]for v in cols];dims=[fp(v,chars[0])for v in cols]
  equations=[]
  for quad in quads:
   co=[]
   for v,d in zip(vals,dims):
    z=ONE
    for e in quad:z=mul(z,v[e])
    co.append(div(z,mul(mul(d,d),mul(D,D))))
   den=math.lcm(*(x.denominator for z in co for x in z));equations.append(([[int(x*den) for x in z] for z in co],den))
  cases=[]
  for case in previous['cases']:
   if not case.get('survives'):continue
   a=case['allocation'];ix=case['pattern'];counts=domain['patterns'][ix]
   if semion: signed=[0]*65
   else:signed=[2*p-q for p,q in zip(charges[a]['plus_pairs'],charges[a]['minus_individuals'])]+[0]*25
   for e,k in enumerate(translated):signed[k]=mg*lowcharges[e]
   four={}
   for quad,(co,den) in zip(quads,equations):
    v=[sum(n*z[k] for n,z in zip(lowcharges+signed,co)) for k in range(4)]
    need(not any(v[1:]) and v[0]%den==0,'weighted fourth integrality');four[quad]=v[0]//den
   cubic=dict(zip(triples,domain['all_twenty_cubic_values'][ix]))
   L=s.Matrix(5,10,lambda e,p: int(pairs[p][0]==pairs[p][1]) if e==0 else cubic[tuple(sorted(pairs[p]+(e,)))])
   B=matrix(case['translated_low_fusion'])
   J=s.Matrix(10,10,lambda p,q:four[tuple(sorted(pairs[p]+pairs[q]))])-L.T*B-B.T*L
   result={'allocation':a,'pattern':ix,'prior_final_survivor':case['prior_final_survivor'],'weighted_Gram':mj(J),'sectors':[]}
   if not semion:
    for sec in case['sectors']:
     pp=sec['pairs'];G=matrix(sec['G']);H=matrix(sec['H']);Jg=J.extract(pp,pp)
     Hplus=(G+Jg)/2-(G-H);Hminus=(G-Jg)/2
     rr={'charge':sec['charge'],'symmetric_residual':mj(Hplus),'antisymmetric_Gram':mj(Hminus),'symmetric_rank':Hplus.rank(),'antisymmetric_rank':Hminus.rank(),'symmetric_psd':bool(Hplus.is_positive_semidefinite),'antisymmetric_psd':bool(Hminus.is_positive_semidefinite)}
     result['sectors'].append(rr)
    result['survives']=all(z['symmetric_psd'] and z['antisymmetric_psd'] for z in result['sectors'])
   else:
    # G swaps the charge spaces; known negative vectors determine its mixed Gram.
    plus,minus=case['sectors'];Xp=matrix(plus['Xtypes']);Xm=matrix(minus['Xtypes'])
    expected=Xp.T*s.diag(*(n//2 for n in counts[:40]))*Xm
    result['mixed_matches_forced_restriction']=J.extract(plus['pairs'],minus['pairs'])==expected
    result['survives']=result['mixed_matches_forced_restriction']
   cases.append(result)
  results.append({'id':rec['id'],'cases':cases,'surviving_prior_final_allocations':[c['allocation'] for c in cases if c['prior_final_survivor'] and c['survives']]})
 files=[P/'source.json',P/'gram_cubic.json',P/'r941_charges.json',HERE/'charged_quartic_pair.json']
 print(json.dumps({'kind':'involution_weighted_pair_Gram','records':results,'source_sha256':{str(p.relative_to(ROOT)):digest(p) for p in files},'verifier_sha256':digest(Path(__file__)),'scope':'Necessary constraints only.'},indent=2))

if __name__=='__main__':main()
