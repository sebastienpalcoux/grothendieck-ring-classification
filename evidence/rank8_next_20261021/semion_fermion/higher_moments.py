"""Exact nonnegative integral unit coefficients of distinguished words.

Enumerates all monomials in A1,...,A4 of total degree at most --degree,
both with and without the central involution.  This is a finite screen,
not a claimed bound on all possible categorical obstructions.
"""
from charged_quartic_pair import *
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--degree',type=int,default=10);args=ap.parse_args()
 source=read(P/'source.json');domain=read(P/'gram_cubic.json');charged=read(HERE/'charged_quartic_pair.json')
 fermion=read(P/'r941_charges.json')['solutions'];lc=[1,1,1,1,-1];tr=[40,41,42,43,57];results=[]
 for rec,previous in zip(source['records'],charged['records']):
  semion=rec['id'].endswith('928');mg=-1 if semion else 1
  chars=[[tuple(map(F,x)) for x in ch] for ch in rec['full_characters']];D=tuple(map(F,rec['formal_codegrees'][0]))
  cols=rec['low_columns']+[(0,)+tuple(v) for v in rec['canonical_high_vectors']]
  beta=[scale(div(D,tuple(map(F,f))),F(1,n)) for f,n in zip(rec['formal_codegrees'],rec['irreducible_dimensions'])]
  dims=[fp(v,chars[0]) for v in cols]
  lambdas=[[div(mul(b,fp(v,ch)),d) for b,ch in zip(beta,chars)] for v,d in zip(cols,dims)]
  base=[div(mul(d,d),mul(D,D)) for d in dims]
  cases=[]
  for c in previous['cases']:
   if not c.get('survives') or not c['prior_final_survivor']:continue
   a=c['allocation'];ix=c['pattern'];counts=domain['patterns'][ix]
   signed=[0]*65 if semion else [2*p-q for p,q in zip(fermion[a]['plus_pairs'],fermion[a]['minus_individuals'])]+[0]*25
   for e,k in enumerate(tr):signed[k]=mg*lc[e]
   cases.append({'allocation':a,'pattern':ix,'weights':[[1]*5+counts,lc+signed],'tested':0})
  forms={(0,0,0,0):base};degree_counts=[]
  for degree in range(args.degree+1):
   words=[e for e in product(range(degree+1),repeat=4) if sum(e)==degree]
   for e in words:
    if degree:
     j=next(j for j,z in enumerate(e) if z);parent=list(e);parent[j]-=1
     forms[e]=[mul(v,l[j+1]) for v,l in zip(forms[tuple(parent)],lambdas)]
    co=forms[e];den=math.lcm(*(x.denominator for z in co for x in z));ints=[[int(x*den) for x in z] for z in co]
    for case in cases:
     if 'failure' in case:continue
     for insertion,ws in enumerate(case['weights']):
      val=[sum(w*z[j] for w,z in zip(ws,ints)) for j in range(4)];case['tested']+=1
      if any(val[1:]) or val[0]%den or val[0]<0:
       case['failure']={'word':list(e),'G':insertion,'coefficient':[str(F(x,den)) for x in val]};break
   degree_counts.append({'degree':degree,'words':len(words),'survivors':sum('failure' not in c for c in cases)})
   # Only the current degree is needed for the next recurrence.
   forms={e:z for e,z in forms.items() if sum(e)==degree}
  for c in cases:del c['weights']
  results.append({'id':rec['id'],'maximum_degree':args.degree,'degrees':degree_counts,'cases':cases,'surviving_allocations':[c['allocation'] for c in cases if 'failure' not in c]})
 files=[P/'source.json',P/'gram_cubic.json',P/'r941_charges.json',HERE/'charged_quartic_pair.json']
 print(json.dumps({'kind':'distinguished_word_unit_moments','records':results,'source_sha256':{str(p.relative_to(ROOT)):digest(p) for p in files},'verifier_sha256':digest(Path(__file__)),'scope':'Finite necessary screen only. No survivor is asserted to exist.'},indent=2))
if __name__=='__main__':main()
