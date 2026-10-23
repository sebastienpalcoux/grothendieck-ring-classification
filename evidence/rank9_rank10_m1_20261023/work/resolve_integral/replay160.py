"""Replay categorical witnesses and finite commutativity-obstruction data.
Run from any directory. Dependencies: Python3 and SymPy. The replay uses
only this directory's fixed certificates and exact arithmetic helpers.
"""
from verify160 import *

def require(x,m):
 if not x:raise ValueError(m)

def gf2rank(rows):
 piv={}
 for r in rows:
  while r:
   i=r.bit_length()-1
   if i in piv:r^=piv[i]
   else:piv[i]=r;break
 return len(piv)

if __name__=='__main__':
 models=json.load(open(OUT/'verified_models160.json'));normals=json.load(open(OUT/'normal_forms160.json'));receipts=[]
 for r in models:
  check=verify_action(r);N,labs=fuse_action(r['J'],r['q']);p=r['basis_map_source_to_model'];T=r['input_tensor'];require(tensor_hash(T)==r['tensor_sha256'],'input tensor hash');require(N==r['model_tensor'],'exact reconstructed tensor');require(sorted(p)==list(range(10)),'bijection');require(all(T[i][j][k]==N[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(10),repeat=3)),'1000 coefficient matches');receipts.append({'id':r['id'],'status':'unitarily_realized','coherence':check,'coefficient_matches':1000});print('PASS model',r['id'],flush=True)
 diagonal=[]
 for r in normals:
  check=verify_action(r);require(check['J_symmetric_on_fixed_subspace'],'symmetric normal form');diagonal.append(tuple(check['diagonal_orbit_values']))
 require(set(diagonal)=={(0,0,0),(1,1,0),(1,0,1),(0,1,1)},'all four invariant classes')
 # The standard degree1,2,3 squarefree Boolean functions are independent
 # and span exactly the even-weight functions on the15 nonzero vectors.
 monomials=[(i,)for i in range(4)]+list(itertools.combinations(range(4),2))+list(itertools.combinations(range(4),3));rows=[]
 for m in monomials:
  vals=[int(all((x>>i)&1 for i in m))for x in range(1,16)];require(sum(vals)%2==0,'even weight');rows.append(sum(v<<j for j,v in enumerate(vals)))
 require(gf2rank(rows)==14,'diagonal cohomology basis')
 # Every alternatingF2-bilinear form; onlyfour are a-invariant, all
 # vanish on the involution fixed subspace.
 pairs=list(itertools.combinations(range(4),2));fixed=[x for x in range(16) if act((0,1),x)==x];forms=[]
 for mask in range(64):
  def B(x,y):return sum(((x>>i&1)*(y>>j&1)+(x>>j&1)*(y>>i&1)) for k,(i,j)in enumerate(pairs) if mask>>k&1)%2
  if not all(B(act((1,0),x),act((1,0),y))==B(x,y)for x,y in itertools.product(range(16),repeat=2)):continue
  require(all(B(x,y)==0 for x,y in itertools.product(fixed,repeat=2)),'vanishing invariant commutators');forms.append(mask)
 require(len(forms)==4,'invariant alternating forms dimension2')
 # Structure needed for solvability reduction, directly from full tensors.
 T=json.load(open(OUT/'dimension160_inputs.json'));struct=[]
 for ident in['R10_1_39','R10_1_83','R10_1_138','R10_1_177']:
  N=T[ident];n=10;du=[next(j for j in range(n)if N[i][j][0])for i in range(n)];invs=[i for i in range(n)if sum(N[i][du[i]])==1];require(len(invs)==2,'two invertibles');g=next(i for i in invs if i);require(all(N[g][i]==N[i][g] for i in range(n)),'central invertible');A={0}|{k for i in range(n)for k in range(n)if N[i][du[i]][k]}
  while True:
   B=A|{k for i in A for j in A for k in range(n)if N[i][j][k]}
   if B==A:break
   A=B
  require(len(A)==10,'trivial universal grading');perm=[next(k for k in range(n)if N[g][i][k])for i in range(n)];fixedsmall=[i for i in range(n)if perm[i]==i];require(len(fixedsmall)==2,'two fixed dimension2 objects');require(all(sum(N[i][du[i]])==3 for i in fixedsmall),'2-dimensional low products')
  big=[i for i in range(n)if i not in invs+fixedsmall];d=[1 if i in invs else 2 if i in fixedsmall else 5 for i in range(n)];require(sum(x*x for x in d)==160,'global dimension');require(all(sum(N[i][j][k]*d[k] for k in range(n))==d[i]*d[j] for i,j in itertools.product(range(n),repeat=2)),'positive dimension character');orbits=[];seen=set()
  for i in big:
   if i not in seen:orb={i,perm[i]};require(len(orb)==2,'free g-orbit');orbits.append(sorted(orb));seen|=orb
  require(len(orbits)==3,'three large g-orbits');mp={i:j for j,o in enumerate(orbits)for i in o}
  for i in big:
   require(du[i]in orbits[mp[i]],'large quotient selfduality');v=N[i][du[i]];require(sum(v[k]for k in invs)==1 and all(v[k]==1 for k in fixedsmall),'regularC5 low restriction');require([sum(v[k]for k in o) for o in orbits]==[0 if j==mp[i]else 2 for j in range(3)],'quotient square rules')
  for i,j in itertools.product(big,repeat=2):
   if mp[i]==mp[j]:continue
   v=N[i][j];require(not any(v[k]for k in invs+fixedsmall),'offdiagonal quotient low absence');require([sum(v[k]for k in o)for o in orbits]==[2 if k in[mp[i],mp[j]]else 1 for k in range(3)],'quotient offdiagonal rules')
  witness=next(([i,j,k,N[i][j][k],N[j][i][k]]for i,j,k in itertools.product(range(n),repeat=3)if N[i][j][k]!=N[j][i][k]),None)
  require((witness is not None)==(ident in ['R10_1_83','R10_1_177']),'commutativity status');struct.append({'id':ident,'tensor_sha256':tensor_hash(N),'dimensions':d,'invertibles':invs,'g':g,'fixed_dimension2':fixedsmall,'large_g_orbits':orbits,'adjoint_rank':10,'quotient_rules_verified':True,'noncommutativity_witness':witness})
 report={'models':receipts,'normal_form_diagonals':diagonal,'cohomology_diagonal_rank':14,'invariant_alternating_forms_masks':forms,'fixed_subspace':fixed,'structural_inputs':struct,'finite_audit_status':'PASS','theoretical_exclusion_requires':'THEORY160.md reduction and commutativity argument'}
 (OUT/'replay160_report.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS all finite action,cohomology,and structure checks',flush=True)
