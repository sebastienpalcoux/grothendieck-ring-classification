"""Finite odd-multiplicity C4/V4 free-orbit dual-ring reduction for R65.
The categorical subgroup-dual argument is proved in POINTED_COCYCLE.md.
This script verifies finite tensors, formal codegrees, subrings and matches;
it binds, and does not replay or replace, the accepted R1453 exclusion.
"""
from pathlib import Path
import json,itertools,hashlib
from fractions import Fraction as F
import sympy as s
from gram_discovery import HERE,REPO,require

def tensor(N,kind):
 op=(lambda a,b:(a+b)%4)if kind=='C4'else(lambda a,b:a^b)
 R=[[[0]*8 for _ in range(8)]for _ in range(8)]
 for i,j in itertools.product(range(8),repeat=2):
  g=op(i%4,j%4)
  if i<4 and j<4:R[i][j][g]=1
  elif i<4 or j<4:R[i][j][4+g]=1
  else:
   R[i][j][g]=1
   for k,n in enumerate(N):R[i][j][4+op(g,k)]=n
 return R

def check(R):
 for i,j,k in itertools.product(range(8),repeat=3):
  for l in range(8):require(sum(R[i][j][a]*R[a][k][l]for a in range(8))==sum(R[j][k][a]*R[i][a][l]for a in range(8)),'associativity')
 dual=[next(j for j in range(8)if R[i][j][0])for i in range(8)]
 require(all(R[i][j][k]==R[dual[i]][k][j]for i,j,k in itertools.product(range(8),repeat=3)),'Frobenius reciprocity')
 require(all(R[0][i][j]==int(i==j)for i,j in itertools.product(range(8),repeat=2)),'unit')
 return dual

def find_map(R,T,kind):
 inv=[i for i in range(8)if all(sum(T[i][j])==1 for j in range(8))];non=[i for i in range(8)if i not in inv]
 for perm in itertools.permutations([i for i in inv if i]):
  gm=[0,*perm]
  for rho in non:
   p=gm+[T[g][rho].index(1)for g in gm]
   if len(set(p))==8 and all(R[i][j][k]==T[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(8),repeat=3)):return p
 raise ValueError('no based isomorphism')

def run():
 require(250**2-5*110**2==2000,'global dimension norm')
 require(125>45 and 21**2>12**2*3,'strict rank4 bound comparison')
 censuspath=REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json';src={x['id']:x for x in json.loads(censuspath.read_text())};x=s.Symbol('x');results={}
 for kind in ('C4','V4'):
  domain=[(a,b,c,b)for b in range(6)for a in range(12-2*b)for c in [11-2*b-a]if a<=c]if kind=='C4'else[n for n in itertools.combinations_with_replacement(range(12),4)if sum(n)==11]
  require(len(domain)==(21 if kind=='C4' else 27),'complete coefficient domain');rows=[]
  for N in domain:
   R=tensor(N,kind);dual=check(R)
   a,b,c,d=N;ms=[11,a-b+c-d,a-c,a-c]if kind=='C4'else[11,a+b-c-d,a-b+c-d,a-b-c+d]
   NN=list(map(s.Matrix,R));C=sum((NN[i]*NN[dual[i]]for i in range(8)),s.zeros(8));expected=s.prod(x*x-4*(m*m+4)*x+16*(m*m+4)for m in ms)
   require(s.expand(C.charpoly(x).as_expr()-expected)==0,'exact formal codegrees')
   bad=next((m for m in ms if F(125,m*m+4).denominator!=1),None)
   rec={'coefficients':N,'group_character_parameters':ms,'formal_codegree_norm_ratios':[str(F(125,m*m+4))for m in ms]}
   if bad is not None:rec.update(outcome='formal_codegree_norm_obstruction',witness_parameter=bad)
   elif sorted(N)==[0,0,0,11]:
    rho=next(i for i in range(4,8)if R[i][i][0]==1 and R[i][i][i]==11);require(sum(R[rho][rho])==12,'rank2 closure');rec.update(outcome='forbidden_rank_two_subring',subring=[0,rho],rank_two_parameter=11)
   elif sorted(N)==[0,0,5,6]:
    sub=next(S for S in itertools.combinations(range(8),4)if 0 in S and sum(i<4 for i in S)==2 and all(not R[i][j][k]for i in S for j in S for k in range(8)if k not in S));rec.update(outcome='repository_rank_four_bound_obstruction',subring=sub,FPdim=['125','55'])
   else:
    rid='R8_3_65'if kind=='C4'else'R8_3_1453';p=find_map(R,src[rid]['tensor'],kind);rec.update(outcome='source_tensor_match',id=rid,permutation=p,tensor_sha256=src[rid]['tensor_sha256'])
   rows.append(rec)
  require(sum(r['outcome']!='formal_codegree_norm_obstruction'for r in rows)==3,'exactly three norm survivors')
  results[kind]={'complete_domain':len(rows),'records':rows,'norm_survivors':[r['coefficients']for r in rows if r['outcome']!='formal_codegree_norm_obstruction']}
 paths=[censuspath,REPO/'evidence/rank8_frontier_20261021/global_induction/results/R8_3_1453_h4.json',REPO/'evidence/rank8_m3_20261021/criteria/rank8_signed_bridge.py',REPO/'evidence/rank8_m3_20261021/criteria/quadratic_compression.py',REPO/'manuscripts/rank4/papers/companion_sections/14_finite_certification.tex',REPO/'evidence/rank8_frontier_20261021/structural_models/R65_MODULES.md']
 prior=json.loads(paths[1].read_text());require(prior['status']=='excluded'and prior['tensor_sha256']==src['R8_3_1453']['tensor_sha256'],'accepted R1453 tensor exclusion binding')
 profiles=json.loads((HERE/'profile_closure.json').read_text())['R8_3_65']['surviving_factors'];removed=sorted({f['candidate_index']for f in profiles if len(f['B'])==2});require(removed==[18,21,26,29],'complete rank-two algebra removals');require(all(len(f['B'])==2 for f in profiles if f['candidate_index']in removed),'removed objects have no other factors');paths.append(HERE/'profile_closure.json')
 closure=json.loads((HERE/'profile_closure.json').read_text());actions=json.loads((HERE/'action_classes.json').read_text());paths.append(HERE/'action_classes.json');summary={}
 for rid,r in closure.items():
  fs=[f for f in r['surviving_factors']if rid!='R8_3_65'or f['candidate_index']not in removed];acs=[c for c in actions[rid]['complete_action_classes']if rid!='R8_3_65'or c['module_rank']!=2]
  summary[rid]={'remaining_algebra_objects':len({f['candidate_index']for f in fs}),'remaining_induction_factors':len(fs),'remaining_complete_action_classes':len(acs),'remaining_full_action_ranks':sorted(c['module_rank']for c in acs)}
 require(sum(r['remaining_algebra_objects']for r in summary.values())==144 and sum(r['remaining_induction_factors']for r in summary.values())==178 and sum(r['remaining_complete_action_classes']for r in summary.values())==30,'combined final counts')
 out={'scope':'Finite algebraic dual-ring reduction. POINTED_COCYCLE.md supplies categorical hypotheses; accepted rank4 theorem and R1453 exclusion are explicit dependencies. No exclusion of R65 itself.','results':results,'combined_summary':summary,'source_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths},'r65_removed_rank_two_algebra_candidates':removed,'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'r65_pointed_trivial_associator_branch':'excluded_via_C2_dual_V4'}
 (HERE/'pointed_dual.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print('PASS C4 complete21, V4 complete27; each has3 norm survivors; source maps and forbidden subrings exact.');return out
if __name__=='__main__':run()
