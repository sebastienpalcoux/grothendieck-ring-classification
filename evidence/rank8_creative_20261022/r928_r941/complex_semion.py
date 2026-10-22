#!/usr/bin/env python3
"""Oriented all-order semion trace cones over Q(zeta24), including signed spectra."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,sys,math,hashlib
import numpy as np
import sympy as s
from flint import fmpz_poly
from dimension_mask import load_module,mask,need
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];FR=ROOT/'evidence/rank8_frontier_20261021'
sys.path.insert(0,str(FR/'r928_semion_rotation'))
mod=load_module('complex_pair_base',FR/'r928_semion_rotation/pair_rotation.py')
sys.path.insert(0,str(ROOT/'evidence/rank8_next_20261021/semion_fermion'))
from quartic_pair import mul,add,scale,fp
ZERO=(F(0),)*4

def traces():
 n=288;x=s.Symbol('x');co=list(reversed(list(map(int,s.Poly(s.cyclotomic_poly(n,x),x).all_coeffs()))));degree=len(co)-1
 powers=np.zeros((n,degree),dtype=np.int64);powers[0,0]=1
 for j in range(1,n):powers[j,1:]=powers[j-1,:-1];powers[j]-=int(powers[j-1,-1])*np.array(co[:-1])
 need(max(abs(int(v))for v in powers.flat)*n<2**50,'exact recurrence arithmetic bound')
 def gauss(q,D):return sum((int(s.kronecker_symbol(D,j))*powers[(n//D*j)%n]for j in range(D)),np.zeros(degree,dtype=np.int64))//math.isqrt(D//q)
 base=[powers[0],gauss(2,8),gauss(3,12),gauss(6,24)];poly=fmpz_poly(co)
 for b in list(base):
  z=(fmpz_poly(list(map(int,b)))*fmpz_poly(list(map(int,powers[n//4]))))%poly;base.append(np.array([int(z[j])for j in range(degree)],dtype=np.int64))
 B=s.Matrix(np.stack(base,axis=1).tolist());piv=list(B.T.rref()[1]);need(len(piv)==8,'full complex cyclotomic basis');inverse=B.extract(piv,range(8)).inv();H=[u for u in range(n)if math.gcd(u,n)==1 and u%24==1];out=[]
 for exponent in range(n):
  total=sum((powers[(u*exponent)%n]for u in H),np.zeros(degree,dtype=np.int64));v=inverse*s.Matrix([int(total[i])for i in piv])/len(H);row=tuple(F(int(z.p),int(z.q))for z in v)
  need(B*s.Matrix([s.Rational(z.numerator,z.denominator)for z in row])==s.Matrix(list(map(int,total)))/len(H),'all relative trace coordinates')
  out.append(row)
 # Complete beyond the box: over Q(zeta24), extra p-power depth gives zero at powers1..6.
 typ={tuple(out[(e*k)%n]for k in range(1,7))for e in range(n)};typ.add(tuple((F(0),)*8 for _ in range(6)))
 return out,sorted(typ)

def pair(t):
 out=[]
 for k,v in enumerate(t,1):
  re,im=v[:4],v[4:];q=k%4
  rr,ii=(re,im)if q==0 else(scale(im,-1),re)if q==1 else(scale(re,-1),scale(im,-1))if q==2 else(im,scale(re,-1))
  out.append(tuple(x+y for x,y in zip(re,rr))+tuple(x+y for x,y in zip(im,ii)))
 return tuple(out)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();path=HERE/'R928_complex_semion.json';saved=None if args.write else json.loads(path.read_text())
 data=mod.setup();row,allowed,dims=mask(928);ordinary=mod.base.rotation.bq.trace_types(6)[0];raw_to_canonical={raw:c for c,raw in enumerate(row['original_high_order'])}
 oldlabels=[]
 for raw in range(65):
  c=raw_to_canonical[raw];oldlabels.extend(('pair',c,ti)for ti in range(30))if c<40 else oldlabels.extend(('individual',c,ti)for ti in range(38))
 oldlookup={label:j for j,label in enumerate(oldlabels)};oldtypes=data[2];roottraces,alltypes=traces();chars=[[tuple(map(F,v))for v in ch]for ch in row['full_characters']];D=tuple(map(F,row['formal_codegrees'][0]));lowcharge=[1,1,1,1,-1];translated=[40,41,42,43,57]
 def masks(d):
  a,b,c,e=map(F,d);return {12:3*c-a-b,24:6*e-a-2*b}
 lows=[list(v)for v in row['low_columns']];highs=[[0]+v for v in row['canonical_high_vectors']];lowdims=[fp(v,chars[0])for v in lows]
 fixed=[(v,1,0,q)for v,q in zip(lows,lowcharge)]+[(highs[c],0,q,-q)for c,q in zip(translated,lowcharge)]
 # Fixed tuple: underlying restriction, real twist, imaginary twist, monodromy.
 cp=json.loads((HERE.parent/'unified/composite_verification.json').read_text())['quartic_controls'];spectral={(r['conductor'],k):(F(r['epsilon_minus_weights'][k]),F(r['epsilon_plus_weights'][k]))for r in cp for k in range(r['conductor'])}
 atoms=[]
 for c in range(40):
  L=masks(dims[c]);bound=12 if L[12]else 24 if L[24]else 0
  domain=alltypes if not bound else sorted({tuple(roottraces[(e*k)%288]for k in range(1,7))for e in range(0,288,288//bound)})
  for t in domain:
   pt=pair(t);real=tuple(v[:4]for v in pt);need(real in oldtypes,'oriented trace projects to complete old pair domain')
   if c not in allowed and real==tuple((F(v),F(0),F(0),F(0))for v in (1,0,1,2,1,0)):continue
   actual=[e for e in range(0,288,288//bound)if tuple(roottraces[(e*k)%288]for k in range(1,7))==t]if bound else[]
   need(not bound or actual,'finite root support')
   # First-power trace determines each root in Q(zeta24), so bounded atoms have one exponent.
   need(not bound or len(actual)==1,'unique actual bounded root')
   atoms.append((c,t,pt,oldlookup['pair',c,oldtypes.index(real)],actual[0]if actual else None))
 ordinary_i=tuple((F(0),F(0),F(0),F(0))if k%2 else(F((-1)**(k//2)),F(0),F(0),F(0))for k in range(1,7));it=ordinary.index(ordinary_i)
 indices=json.loads((FR/'r928_semion_rotation/pair_rotation.json').read_text())['complete_remaining_indices'];cases=[]
 for ix in indices:
  A,b,oldmeta=mod.build(data,ix);b=list(b)
  for c in translated:
   j=oldlookup['individual',c,it];b=[v-r[j]for v,r in zip(b,A)]
  auxiliary=list(range(len(oldlabels),len(A[0])));M=[[r[a[3]]for a in atoms]+[r[j]for j in auxiliary]+[0]*4 for r in A];n=len(M[0]);mix={12:n-4,24:n-2};newlabels=[]
  def append(coeff,rhs,label):
   den=math.lcm(F(rhs).denominator,*(F(x).denominator for x in coeff));M.append([int(F(v)*den)for v in coeff]);b.append(int(F(rhs)*den));newlabels.append(label)
  # Imaginary STS equations for all distinguished pairs.
  for E in range(5):
   for H in range(E,5):
    weights=[mul(fp(v,chars[E]),fp(v,chars[H]))for v in highs]
    fixedim=ZERO
    for v,re,im,q in fixed:fixedim=add(fixedim,scale(mul(fp(v,chars[E]),fp(v,chars[H])),im))
    for k in range(4):append([mul(weights[c],pt[0][4:])[k]for c,t,pt,old,e in atoms]+[0]*(len(auxiliary)+4),-fixedim[k],['imag_STS',E,H,k])
  # Complete central-semion S row, normalized after dividing the distinguished-row scale.
  for E in range(5):
   weights=[mul(fp(v,chars[0]),fp(v,chars[E]))for v in highs];fr=ZERO;fi=ZERO
   for v,re,im,q in fixed:
    z=mul(fp(v,chars[0]),fp(v,chars[E]));fr=add(fr,scale(z,re*q));fi=add(fi,scale(z,im*q))
   # S_{G,A_E}=m_E dim(A_E), whereas the distinguished row has
   # beta_E=dim(A_E)/dim(E). Dividing STS by beta_E leaves dim(E),
   # not dim(E)^2. Verify this also against the character at source g.
   dimE=row['irreducible_dimensions'][E]
   need(chars[E][7]==(F(lowcharge[E]*dimE),F(0),F(0),F(0)), 'central character normalization')
   target=scale(mul(D,chars[E][7]),-1)
   for part in (0,1):
    values=[]
    for c,t,pt,old,e in atoms:
     re,im=t[0][:4],t[0][4:];phase=add(re,im)if part==0 else add(im,scale(re,-1));values.append(mul(weights[c],phase))
    for k in range(4):append([v[k]for v in values]+[0]*(len(auxiliary)+4),(-fr[k]if part==0 else target[k]-fi[k]),['semion_STS',E,part,k])
  # Every individual twist fibre, with one convex endpoint mixture per saturated character.
  for (f,k),(wm,wp)in spectral.items():
   coeff=[]
   for c,t,pt,old,e in atoms:
    L=masks(dims[c])[f]
    if not L:coeff.append(F(0));continue
    need(e is not None and (e*f)%288==0,'root in supported conductor')
    es=[(e*f//288)%f,((e+72)*f//288)%f];coeff.append(L*L*es.count(k))
   coeff += [0]*(len(auxiliary)+4);coeff[mix[f]]=-4*f*(wm-wp);rhs=4*f*wp
   for v,re,im,q in fixed:
    phase=0 if re==1 else f//4 if im==1 else 3*f//4
    if phase==k:rhs-=masks(fp(v,chars[0]))[f]**2
   append(coeff,rhs,['spectral_fibre',f,k])
  for f in (12,24):
   co=[0]*n;co[mix[f]]=co[mix[f]+1]=1;append(co,1,['spectral_mixture',f])
  meta={'pattern':ix,'complex_phase_atoms':len(atoms),'rows':len(M),'columns':n,'matrix_sha256':hashlib.sha256(json.dumps(M,separators=(',',':')).encode()).hexdigest(),'rhs_sha256':hashlib.sha256(json.dumps(b,separators=(',',':')).encode()).hexdigest(),'added_rows':newlabels}
  if args.write:decision=mod.base.lp.decide(M,b)
  else:need(saved['cases'][len(cases)]['metadata']==meta,'complex phase matrix binding');decision=saved['cases'][len(cases)]['decision']
  need(decision['status']in ('exact_feasible_relaxation','exact_infeasible_relaxation'),'exact complex cone decision required');mod.base.lp.verify(M,b,decision);cases.append({'metadata':meta,'decision':decision})
  result={'id':'R8_3_928','field':'Q(zeta24)','all_order_box':288,'complete_complex_trace_types':len(alltypes),'known_semion_twist':'i','cases':cases,'scope':'Complete oriented semion phase relaxation with complex STS for the distinguished rows and central invertible row, and all saturated individual spectral fibres. Exact rational feasibility is not categorification.'}
  if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
  print('complex R928',ix,decision['status'],flush=True)
 if not args.write:need(result==saved,'complex phase deterministic replay')
if __name__=='__main__':main()
