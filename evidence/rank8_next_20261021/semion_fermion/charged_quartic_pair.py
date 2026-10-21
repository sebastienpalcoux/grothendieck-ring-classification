"""Coupled fourth moments, monodromy sectors and translated low objects.

Every calculation is rational or in Q(sqrt(2),sqrt(3)).  Frozen evidence is
read-only.  Run from any directory; JSON goes to stdout.
"""
from quartic_pair import *

def matrix(v): return s.Matrix([[s.Rational(x) for x in row] for row in v])

def main():
 source=read(P/'source.json'); domain=read(P/'gram_cubic.json')
 uncharged=read(HERE/'quartic_pair.json'); charges=read(P/'r941_charges.json')
 final941=read(OLD/'review/r941_fusion_traces.json')['paired_surviving_allocations']
 final928=[40,44,49,58,186,191,196,243,245,248]
 parity928=[2,6,40,44,49,58,61,64,186,191,196,199,243,245,248]
 pairs=list(cwr(range(1,5),2)); lowcharges=[1,1,1,1,-1]
 translated=[40,41,42,43,57]; results=[]
 for rec, prior in zip(source['records'], uncharged['records']):
  need(rec['id']==prior['id'],'record order')
  semion=rec['id'].endswith('928'); mg=-1 if semion else 1
  chars=[[tuple(map(F,x)) for x in ch] for ch in rec['full_characters']]
  D=tuple(map(F,rec['formal_codegrees'][0])); ds=chars[0]
  lows=rec['low_columns']; highs=[(0,)+tuple(v) for v in rec['canonical_high_vectors']]; cols=lows+highs
  beta=[scale(div(D,tuple(map(F,f))),F(1,n)) for f,n in zip(rec['formal_codegrees'],rec['irreducible_dimensions'])]
  vals=[[mul(b,fp(v,ch)) for b,ch in zip(beta,chars)] for v in cols]
  dims=[fp(v,ds) for v in cols]
  # N_{Ai,Aj}^{G Ae} from the third Verlinde moment weighted by monodromy.
  equations=[]
  for i,j in pairs:
   row=[]
   for e in range(5):
    co=[div(mul(mul(v[i],v[j]),v[e]),mul(d,mul(D,D))) for v,d in zip(vals,dims)]
    den=math.lcm(*(x.denominator for z in co for x in z))
    row.append(([[int(x*den) for x in z] for z in co],den))
   equations.append(row)
  groupby={ix:g for g in prior['groups'] for ix in g['indices']}
  allocations=[]
  if semion:
   for ix in parity928:
    counts=domain['patterns'][ix]
    need(all(counts[k]%2==0 for k in range(40)),'semion parity')
    allocations.append((ix,ix,[counts[k]//2 for k in range(40)],[counts[k]//2 for k in range(40)]))
  else:
   for a,sol in enumerate(charges['solutions']):
    allocations.append((a,sol['pattern_index'],[2*p for p in sol['plus_pairs']],sol['minus_individuals']))
  cases=[]
  for a,ix,plus,minus in allocations:
   counts=domain['patterns'][ix]; g=groupby[ix]; G=matrix(g['G']);T=matrix(g['T'])
   signed=[plus[k]-minus[k] for k in range(40)]+[0]*25
   for e,k in enumerate(translated): signed[k]=mg*lowcharges[e]
   need(all(plus[k]+minus[k]==counts[k] for k in range(40)),'charge multiplicity')
   coeff=s.zeros(5,10); failure=None
   for p,(i,j) in enumerate(pairs):
    for e,(co,den) in enumerate(equations[p]):
     v=[sum(n*z[k] for n,z in zip(lowcharges+signed,co)) for k in range(4)]
     if any(v[1:]) or v[0]%den or v[0]<0:
      failure={'reason':'translated_cubic_nonintegral_or_negative','pair':pairs[p],'e':e,'value':[str(F(x,den)) for x in v]};break
     coeff[e,p]=v[0]//den
     need(not coeff[e,p] or lowcharges[i]*lowcharges[j]==mg*lowcharges[e],'charge support')
    if failure: break
   case={'allocation':a,'pattern':ix,'prior_final_survivor':a in (final928 if semion else final941)}
   if failure: case['failure']=failure;cases.append(case);continue
   # Remove the five known translates from the unknown Gram and restrictions.
   W=s.Matrix.hstack(*(s.Matrix(highs[k]) for k in translated))
   G=G-coeff.T*coeff;T=T-W*coeff
   case['translated_low_fusion']=mj(coeff)
   V=s.Matrix.hstack(*(s.Matrix(v) for v in highs[:40])); sectors=[]
   for charge,ns in [(1,plus),(-1,minus)]:
    pp=[p for p,(i,j) in enumerate(pairs) if lowcharges[i]*lowcharges[j]==charge]
    Q=V*s.diag(*ns)*V.T; ind=list(Q.rref()[1]); Qb=Q.extract(ind,ind)
    Tg=T[:,pp]; Gg=G.extract(pp,pp); C=Qb.inv()*Tg[ind,:]
    sector={'charge':charge,'pairs':pp,'simple_count':sum(ns),'restriction_rank':len(ind)}
    if Q[:,ind]*C!=Tg: sector['failure']='restriction_range'
    else:
     H=Gg-C.T*Qb*C; X=V[ind,:].T*C
     sector.update(G=mj(Gg),H=mj(H),T=mj(Tg),Xtypes=mj(X),Grank=Gg.rank(),Hrank=H.rank(),H_psd=bool(H.is_positive_semidefinite))
     if not sector['H_psd']: sector['failure']='nonpositive_residual_Gram'
     elif sum(ns)-len(ind)<sector['Hrank']:sector['failure']='insufficient_kernel_dimension'
    sectors.append(sector)
   case['sectors']=sectors;case['survives']=all('failure' not in t for t in sectors)
   cases.append(case)
  results.append({'id':rec['id'],'cases':cases,'surviving_allocations':[x['allocation'] for x in cases if x.get('survives')],
    'surviving_prior_final_allocations':[x['allocation'] for x in cases if x.get('survives') and x['prior_final_survivor']]})
 files=[P/'source.json',P/'gram_cubic.json',P/'r941_charges.json',HERE/'quartic_pair.json',OLD/'review/r941_fusion_traces.json']
 print(json.dumps({'kind':'monodromy_sector_translated_low_fourth_Gram','records':results,'source_sha256':{str(p.relative_to(ROOT)):digest(p) for p in files},'verifier_sha256':digest(Path(__file__)),'scope':'Necessary fusion multiplicity constraints only; no survivor is asserted to exist.'},indent=2))

if __name__=='__main__': main()
