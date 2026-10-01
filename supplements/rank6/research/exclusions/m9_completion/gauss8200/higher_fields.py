#!/usr/bin/env python3
"""Exclude dimension-field degrees four and six for the 7018/8785 profiles.
All conductor bounds follow from local different trace divisibility, not
from a trial cutoff. See higher_fields_proof.tex for the categorical bridge.
"""
import hashlib,itertools,json,math,sys
from pathlib import Path
from fractions import Fraction as F
import sympy as s
from common import (validate,dual,casimir,integral,positive,
                    conjugate_polynomial,inverse_trace,squarefree,mod_two_factors)

def need(test,msg):
 if not test:raise ValueError(msg)

def hypotheses(R):
 validate(R);need(dual(R)==list(range(6)),'not rank-six self-dual')
 need(all(R[i][j]==R[j][i] for i,j in itertools.product(range(6),repeat=2)),'not commutative')
 G=casimir(R);T=int(s.trace(G));x=s.Symbol('x');cp=G.charpoly(x).as_poly()
 blocks=mod_two_factors(R)
 need(sorted((a['rank'],a['kind']) for a in blocks)==[(2,'unramified_field')]*3,'not F4 cubed')
 profiles=[];scales=[]
 for f,m in cp.factor_list()[1]:
  co=list(map(int,f.all_coeffs()));need(f.degree()==2 and co[0]==1,'not quadratic profile')
  A=-co[1];B=math.isqrt((A*A-4*co[2])//5)
  need(5*B*B==A*A-4*co[2] and B>0,'field is not sqrt5')
  a=math.isqrt(co[2]//5);need(5*a*a==co[2] and a>0,'not scalar times sqrt5 unit')
  u,v=F(B,a),F(A,5*a)
  need(u.denominator==v.denominator==1 and (u-v)%2==0 and u*u-5*v*v==-4,'unit quotient nonintegral')
  scales.append(a);profiles.append({'polynomial':co,'multiplicity':int(m),'ideal_scale':a,'unit_twice_coordinates':[int(u),int(v)]})
 c=math.lcm(*scales)
 need((c,T) in [(195,4405),(65,4325)],'outside the two proved profiles')
 mod2=[int(v)%2 for v in cp.all_coeffs()]
 need(mod2==[int(v)%2 for v in s.Poly((x*x+x+1)*(x+1)**4,x).all_coeffs()],'wrong Casimir parity')
 return {'tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),
         'Casimir_trace':T,'codegree_ideal_scale':c,'quadratic_radicand':5,
         'original_codegree_profiles':profiles,'Casimir_polynomial_mod2':mod2,'mod_two_factors':blocks}

def conductor_reduction(c,T):
 B=T//(5*c)
 # For K=E5 Fq biquadratic, q is odd squarefree, 5-free, q=1 mod4.
 # Each ramified p not dividing c divides Tr_F(b), whose upper bound is B.
 primes=sorted(set([int(p) for p in s.factorint(c) if p!=5]+[int(p) for p in s.primerange(3,B+1) if p!=5]))
 quartic=[]
 for bits in itertools.product((0,1),repeat=len(primes)):
  q=math.prod(p for p,b in zip(primes,bits) if b)
  if q>1 and q%4==1 and q//math.gcd(q,c)<=B:quartic.append(q)
 need(quartic==[13],'unexpected biquadratic field')
 # A primitive order-three Dirichlet character has conductor 9^e prod p,
 # e in {0,1}, p=1 mod3 distinct. At ramified p the cubic different
 # exponent is 2 (tame), or 4 at 3. Subtract the valuation of c.
 primes3=sorted(set([int(p) for p in s.factorint(c) if p%3==1]+[int(p) for p in s.primerange(3,B+1) if p%3==1]))
 blocks=[9]+primes3
 cubic=[]
 for bits in itertools.product((0,1),repeat=len(blocks)):
  selected=[p for p,b in zip(blocks,bits) if b]
  if not selected:continue
  conductor=math.prod(selected);trace_factor=norm_bound=1;local=[]
  for block in selected:
   p=3 if block==9 else block;diff=4 if p==3 else 2
   vc=0;rem=c
   while rem%p==0:vc+=1;rem//=p
   k=max(0,diff-3*vc)
   trace_exp=(k+diff)//3
   trace_factor*=p**trace_exp;norm_bound*=p**k
   local.append({'prime':p,'different_exponent':diff,'scalar_valuation':vc,
                 'required_b_valuation':k,'trace_valuation':trace_exp})
  if trace_factor>B:continue
  # Single conductors 7,9,13 are inert at two. Composite conductors are
  # conservatively retained, whether or not every associated field splits.
  if len(selected)==1:
   if conductor==9:need(2 not in (1,8),'two not excluded at conductor nine')
   else:need(pow(2,(conductor-1)//3,conductor)!=1,'unproved single-conductor rejection')
   cubic.append({'conductor':conductor,'rejection':'two inert','local':local})
   continue
  traces=list(range(trace_factor,B+1,trace_factor))
  need(all(27*norm_bound>t**3 for t in traces),'sextic AMGM survivor')
  cubic.append({'conductor':conductor,'local':local,'trace_factor':trace_factor,
                'possible_positive_traces':traces,'norm_lower_bound':norm_bound,
                'rejection':'AMGM','exact_comparisons':[[27*norm_bound,t**3] for t in traces]})
 return {'positive_relative_trace_bound':B,'biquadratic_candidate_primes':primes,
         'biquadratic_radicands':quartic,'cyclic_quartic_rejection':'Frobenius order-two projection contradiction',
         'cubic_candidate_blocks':blocks,'cyclic_cubic_fields':cubic,'all_sextic_fields_excluded':True}

def complementary_pairs(delta,T,original_mod2):
 r=1-inverse_trace(*delta,5,13)
 if r<=0:return []
 A,B=r.numerator,r.denominator;out=[]
 for k in range(1,(T-delta[0])//A+1):
  S,N=A*k,B*k;disc=S*S-4*N
  if disc<0 or S<=2 or N<=S-1:continue
  rr=math.isqrt(disc)
  if rr*rr==disc:
   if (S-rr)%2 or (S-rr)//2<=1:continue
  elif S*S%N or squarefree(disc)[1] not in (5,13,65):continue
  p=conjugate_polynomial(delta,5,13);x=p.gen
  total=p*s.Poly(x*x-S*x+N,x)
  parity=[int(v)%2 for v in total.all_coeffs()]
  out.append({'sum':S,'product':N,'total_polynomial_mod2':parity,'parity_compatible':parity==original_mod2})
 return out

def quartic_spectrum(c,T,original_mod2):
 stats=[];candidates=[]
 for y in range(1,T//(5*c)+1):
  positive_count=dnumber_count=0
  # theta=(x+y sqrt5+z sqrt13+w sqrt65)/4 and Delta=c sqrt5 theta.
  # Positivity of every Delta conjugate proves all three strict bounds.
  bx=math.isqrt(5*y*y-1);bz=math.isqrt((5*y*y-1)//13);bw=math.isqrt((y*y-1)//13)
  for w,z,x in itertools.product(range(-bw,bw+1),range(-bz,bz+1),range(-bx,bx+1)):
   if not integral(x,y,z,w,5,13):continue
   delta=(5*c*y,c*x,5*c*w,c*z)
   if not positive(*delta,5,13):continue
   positive_count+=1
   co=list(map(int,conjugate_polynomial(delta,5,13).all_coeffs()));N=co[-1]
   need(N>0 and co[1]==-5*c*y,'bad positive dimension polynomial')
   if any(co[j]**4%N**j for j in range(1,5)):continue
   dnumber_count+=1;ps=complementary_pairs(delta,T,original_mod2)
   need(not any(v['parity_compatible'] for v in ps),'quartic spectrum survives')
   candidates.append({'theta_numerator':[x,y,z,w],'theta_denominator':4,
                      'dimension_polynomial':co,'complementary_pairs':ps})
  stats.append({'y':y,'positive_candidates':positive_count,'dnumber_candidates':dnumber_count})
 need(sum(a['dnumber_candidates'] for a in stats)==(7 if c==195 else 35),'incomplete quartic candidate count')
 return {'field_radicands':[5,13],'integral_basis':'1,(1+sqrt5)/2,(1+sqrt13)/2,(1+sqrt5)(1+sqrt13)/4',
         'counts':stats,'dnumber_candidates':candidates,'all_quartic_fields_excluded':True}

def certificate(R):
 h=hypotheses(R);c=h['codegree_ideal_scale'];T=h['Casimir_trace']
 return {'kind':'inert_quadratic_higher_dimension_field_exclusion','scope':'general_complex_fusion_categories',
         'hypotheses':h,'conductor_reduction':conductor_reduction(c,T),
         'quartic_spectrum':quartic_spectrum(c,T,h['Casimir_polynomial_mod2']),
         'conclusion':'The signed dimension-character field is Q(sqrt5).'}

def verify(R,c):
 need(certificate(R)==c,'higher-field certificate differs from full exact replay');return True

