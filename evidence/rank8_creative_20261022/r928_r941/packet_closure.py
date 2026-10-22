#!/usr/bin/env python3
"""Exact fusion algebra closure and packet products for R941 necessary centers."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement as cwr
from functools import lru_cache
import json,sys,argparse,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];NEXT=ROOT/'evidence/rank8_next_20261021/semion_fermion';FR=ROOT/'evidence/rank8_frontier_20261021';P=FR/'quartic_integer_center'
sys.path.insert(0,str(NEXT))
from quartic_pair import mul,div,scale,fp,add,ONE,Z,need,s

def word(indices=(),g=0):return (g,)+tuple(indices.count(i)for i in range(1,5))
def plus(a,b):return ((a[0]+b[0])%2,)+tuple(x+y for x,y in zip(a[1:],b[1:]))
def scalar(x):return (F(x),F(0),F(0),F(0))
def rational(z):need(not any(z[1:]),'nonrational fusion moment');return s.Rational(z[0].numerator,z[0].denominator)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--allocation',type=int);args=ap.parse_args()
 rec=json.loads((P/'source.json').read_text())['records'][1];patterns=json.loads((P/'gram_cubic.json').read_text())['patterns'];charges=json.loads((P/'r941_charges.json').read_text())['solutions'];charged=json.loads((NEXT/'charged_quartic_pair.json').read_text())['records'][1]['cases'];witnesses=json.loads((NEXT/'integer_pair_completion.json').read_text())['records'][1]['cases'];indices=json.loads((FR/'review/r941_fusion_traces.json').read_text())['paired_surviving_allocations']
 if args.allocation is not None:indices=[args.allocation]
 chars=[[tuple(map(F,x))for x in ch]for ch in rec['full_characters']];D=tuple(map(F,rec['formal_codegrees'][0]));d2=mul(D,D);beta=[scale(div(D,tuple(map(F,f))),F(1,n))for f,n in zip(rec['formal_codegrees'],rec['irreducible_dimensions'])]
 cols=rec['low_columns']+[[0]+v for v in rec['canonical_high_vectors']];dims=[fp(v,chars[0])for v in cols];eigen=[[div(mul(b,fp(v,ch)),d)for b,ch in zip(beta,chars)][1:]for v,d in zip(cols,dims)]
 pairs=list(cwr(range(1,5),2));triples=list(cwr(range(1,5),3));translated=[40,41,42,43,57];lowcharge=[1,1,1,1,-1]
 words=[word(),word(g=1)]+[word((i,),g)for g in (0,1)for i in range(1,5)]+[word(pair,g)for g in (0,1)for pair in pairs]
 # physical known-simple order must match the 10 coordinate unit words.
 knownorder=[0,5]+list(range(1,5))+list(range(6,10))
 out=[]
 for ai in indices:
  charge=charges[ai];pat=patterns[charge['pattern_index']];case=next(x for x in charged if x['allocation']==ai);wit=next(x for x in witnesses if x['allocation']==ai)
  cub=[]
  for t in rec['low_cubic_equations']:
   z=tuple(F(t['constant'][k])+sum(n*F(v[k])for n,v in zip(pat,t['coefficients']))for k in range(4));cub.append(rational(z))
  cub=dict(zip(triples,cub));pairrows=[]
  for e in range(5):pairrows.append([int(i==j)if e==0 else cub[tuple(sorted((i,j,e)))]for i,j in pairs])
  pairrows += [[s.Rational(v)for v in row]for row in case['translated_low_fusion']]
  physical=[];multiplicities=[];labels=[]
  for e in knownorder:
   row=[int(e==f)for f in knownorder]+pairrows[e]+pairrows[(e+5)%10]
   physical.append(row);multiplicities.append(1);labels.append(['known',e])
  positive=case['sectors'][0];negative=case['sectors'][1]
  need(positive['charge']==1 and negative['charge']==-1,'sector order')
  for w in wit['witness']:
   pr=[0]*10
   for j,v in zip(positive['pairs'],w['pair_fusion_coefficients']):pr[j]=v
   physical.append([0]*10+pr+pr);multiplicities.append(2*w['multiplicity']);labels.append(['positive',w['type'],w['pair_fusion_coefficients']])
  for k,n in enumerate(charge['minus_individuals']):
   if not n:continue
   pr=[0]*10
   for j,v in zip(negative['pairs'],negative['Xtypes'][k]):pr[j]=s.Rational(v)
   need(all(v>=0 and s.Rational(v).q==1 for v in pr),'forced negative physical coefficients')
   physical.append([0]*10+pr+pr);multiplicities.append(n);labels.append(['negative',k])
  # Spectral measure, including all low translates and the charge allocation.
  spectral=[]
  for e in range(5):spectral.append((e,lowcharge[e],1));spectral.append((5+translated[e],lowcharge[e],1))
  for k,(pp,qq)in enumerate(zip(charge['plus_pairs'],charge['minus_individuals'])):
   if pp:spectral.append((5+k,1,2*pp))
   if qq:spectral.append((5+k,-1,qq))
  weights=[scale(div(mul(dims[k],dims[k]),d2),n)for k,q,n in spectral]
  @lru_cache(None)
  def ev(w):
   result=[]
   for k,q,n in spectral:
    z=scalar(q**w[0])
    for lam,power in zip(eigen[k],w[1:]):
     for _ in range(power):z=mul(z,lam)
    result.append(z)
   return result
  @lru_cache(None)
  def moment(w):
   return rational(tuple(sum(mul(weight,z)[c]for weight,z in zip(weights,ev(w)))for c in range(4)))
  M=s.Matrix(physical);W=s.diag(*multiplicities);gram=M.T*W*M
  need(all(gram[i,j]==moment(plus(w,v))for i,w in enumerate(words)for j,v in enumerate(words)),'physical versus spectral degree-two Gram')
  piv=list(M.rref()[1]);B=M[:,piv];ws=[words[j]for j in piv];G=B.T*W*B;Gi=G.inv();generators=[word((i,))for i in range(1,5)]+[word(g=1)];residuals=[];failed=[]
  for gi,g in enumerate(generators):
   for bi,w in enumerate(ws):
    gw=plus(g,w);v=s.Matrix([moment(plus(gw,u))for u in ws]);coeff=Gi*v;norm=moment(plus(gw,gw))-(coeff.T*G*coeff)[0]
    residuals.append(norm)
    if norm==0:
     forced=B*coeff
     for k,value in enumerate(forced):
      if value<0 or value.q!=1:failed.append({'generator':gi,'basis_word':bi,'physical_row':k,'value':str(value)})
    need(norm>=0,'negative word residual norm')
  report={'allocation':ai,'center_rank':sum(multiplicities),'distinct_physical_rows':len(set(tuple(row)for row in physical)),'degree_two_span_rank':len(piv),'generator_products_tested':len(residuals),'zero_residual_count':sum(v==0 for v in residuals),'forced_fusion_failures':failed}
  closed=all(v==0 for v in residuals);report['closed_generated_algebra']=closed
  if closed:
   unique={};newrows=[];counts=[]
   for row,n in zip(physical,multiplicities):
    key=tuple(row)
    if key not in unique:unique[key]=len(newrows);newrows.append(row);counts.append(0)
    counts[unique[key]]+=n
   if len(newrows)==len(piv):
    basis=s.Matrix(newrows)[:,piv];C=basis.inv();packet_eigen=[]
    for j in range(C.cols):
     packet_eigen.append([tuple(sum(F(C[k,j])*ev(ws[k])[z][c]for k in range(len(ws)))for c in range(4))for z in range(len(spectral))])
    bad=[];constants=[]
    for i,j,k in cwr(range(len(newrows)),3):
     val=rational(tuple(sum(mul(weight,mul(mul(packet_eigen[i][z],packet_eigen[j][z]),packet_eigen[k][z]))[c]for z,weight in enumerate(weights))for c in range(4)))
     values=[val/n for n in (counts[i],counts[j],counts[k])]
     if any(v<0 or v.q!=1 for v in values):bad.append({'triple':[i,j,k],'weighted_cubic':str(val),'packet_sizes':[counts[i],counts[j],counts[k]],'coefficients':list(map(str,values))})
     constants.append(str(val))
    report.update(packet_basis_spans=True,packet_sizes=counts,packet_triples_tested=len(constants),packet_fusion_failures=bad,packet_cubics_sha256=hashlib.sha256(json.dumps(constants).encode()).hexdigest())
   else:report['packet_basis_spans']=False
  out.append(report);print(json.dumps(report),flush=True)
 result={'id':'R8_3_941','method':'degree-two fusion-algebra closure and packet multiplication','records':out,'scope':'Necessary fusion-rule closure tests using the uniquely forced pair-product rows; surviving data are not categories.'}
 path=HERE/('R941_packet_closure.json'if args.allocation is None else f'R941_packet_closure_{args.allocation}.json')
 if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
 else:need(result==json.loads(path.read_text()),'packet closure deterministic replay')
if __name__=='__main__':main()
