#!/usr/bin/env python3
"""Small exact finite proof of the actual R721 bimodule fusion completion.

No native solver, SAT, MILP, float or census is used to enumerate solutions.
Only mandatory categorical induction data and the verified coefficient bound.
"""
from pathlib import Path
import os,ast,hashlib,itertools,json,math,sys,time
import sympy as s
A=Path(__file__).resolve().parent;REPO=Path(os.environ.get('FUSION_CLASSIFICATION_REPO',Path(__file__).resolve().parents[2])).resolve()
MODELS=REPO/'evidence/rank8_next_20261021/models'
def need(b,m):
 if not b:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(N):
 n=len(N);du=[]
 for i in range(n):
  hits=[j for j in range(n)if N[i][j][0]];need(len(hits)==1 and N[i][hits[0]][0]==1,'duality');du.append(hits[0])
 for i,j,k in itertools.product(range(n),repeat=3):
  need(type(N[i][j][k])is int and N[i][j][k]>=0,'positive integral coefficient')
  need(N[0][j][k]==int(j==k) and N[i][0][k]==int(i==k),'unit')
  need(N[i][j][k]==N[du[i]][k][j]==N[k][du[j]][i]==N[du[j]][du[i]][du[k]],'Frobenius')
 for i,j,k,l in itertools.product(range(n),repeat=4):
  need(sum(N[i][j][r]*N[r][k][l]for r in range(n))==sum(N[j][k][r]*N[i][r][l]for r in range(n)),'associativity')
 return du
# Avoid construction_reductions' unrelated census load at module import.
tree=ast.parse((MODELS/'r721_dual_fusion.py').read_text())
pure=[z for z in tree.body if isinstance(z,ast.FunctionDef)and z.name in('source','mul','prepare')or isinstance(z,ast.Assign)and any(isinstance(t,ast.Name)and t.id in('B','dims')for t in z.targets)]
need(len(pure)==5,'pure input definition coverage')
env=dict(s=s,itertools=itertools,validate=validate)
exec(compile(ast.Module(body=pure,type_ignores=[]),'r721_dual_fusion.py:exact pure definitions','exec'),env)
prepare,source,B,dims,mul=[env[x]for x in('prepare','source','B','dims','mul')]

def check_categorical_linear_input():
 C=source();rank_path=MODELS.parent/'semion_fermion/construction/r721_bimodule_rank.json'
 rank=json.loads(rank_path.read_text());factors=[x for x in rank['factors']if x['rank']==8]
 need(len(factors)==1,'unique recorded rank8 Gram factor')
 need(sorted(map(tuple,factors[0]['forgetful_rows']))==sorted(tuple(B[:,i])for i in range(8)),'actual rank8 factor to mandatory B')
 need(list(B[:,0])==[1,0,0,0,1,0,0,0],'tensor unit forgets to the actual algebra1+rho')
 K=s.Matrix(8,8,lambda i,j:sum(C[p][j][t]*C[t][q][i]for p in(0,4)for q in(0,4)for t in range(8)))
 need(B*B.T==K,'all64 actual free-induction Gram coordinates')
 delta=4+s.sqrt(17);alpha=(3+s.sqrt(17))/2
 for i in range(8):
  actual=(sum(B[j,i]for j in range(4))+delta*sum(B[j,i]for j in range(4,8)))/(1+delta)
  need(s.simplify(actual-dims[i][0]-dims[i][1]*alpha)==0,'actual bimodule FP dimensions')
 return dict(rank_factor_sha256=sha(rank_path),all64_Gram_coordinates_match=True,all8_dimensions_match=True,unit_algebra_column_match=True,
             scope='Rank selection and actual Q-system existence use the separately audited categorical proof; this freshly ties its unique factor to every linear completion input.')

# Explicit exact certificate verification independent of LP discovery.
def check_bound(rec,proof):
 need((rec['dual_a'],rec['dual_b'])==(proof['dual_a'],proof['dual_b']),'bound duality')
 need(proof['rref_sha256']==hashlib.sha256(json.dumps(rec['rref'],separators=(',',':')).encode()).hexdigest(),'bound exact system')
 R=s.Matrix(rec['rref']);E=R[:,:-1];b=R[:,-1];n=E.cols
 need([x['variable']for x in proof['certificates']]==list(range(n)),'bound covers every orbit')
 for p in proof['certificates']:
  y=s.zeros(1,E.rows)
  for i,t in p['covector']:y[0,i]=s.Rational(t)
  row=y*E;rhs=(y*b)[0]
  need(all(row[j]>=int(j==p['variable'])for j in range(n)),'exact coefficient dominance')
  need(rhs==s.Rational(p['upper_bound']) and rhs<=3,'exact bound at most3')

def affine(rec):
 R=s.Matrix(rec['rref']);free=rec['free_indices'];q=len(free);F=s.zeros(rec['variables'],q+1)
 for k,j in enumerate(free):F[j,k]=1
 for i,j in enumerate(rec['pivots']):
  F[j,-1]=R[i,-1]
  for k,l in enumerate(free):F[j,k]=-R[i,l]
 D=int(s.ilcm(*[s.denom(x)for x in F]));M=[[int(v*D)for v in row]for row in F.tolist()]
 need(all(M[j][k]==D for k,j in enumerate(free)),'free variables are actual coefficient coordinates')
 return D,M

def propagate(dom,M,D):
 changed=True;deductions=0
 while changed:
  changed=False
  for ri,row in enumerate(M):
   for j,a in enumerate(row[:-1]):
    if not a:continue
    L=H=row[-1]
    for k,b in enumerate(row[:-1]):
     if k==j:continue
     vals=[b*v for v in dom[k]];L+=min(vals);H+=max(vals)
    keep=tuple(v for v in dom[j]if H+a*v>=0 and L+a*v<=3*D)
    if not keep:return None,dict(kind='affine_interval',row=ri,variable=j,other_interval=[L,H],coefficient=a)
    if keep!=dom[j]:dom[j]=keep;changed=True;deductions+=1
 mins=[];maxs=[]
 for ri,row in enumerate(M):
  L=H=base=row[-1];g=D
  for a,values in zip(row[:-1],dom):
   terms=[a*v for v in values];L+=min(terms);H+=max(terms);base+=a*values[0]
   for v in values:g=math.gcd(g,a*(v-values[0]))
  if base%g:return None,dict(kind='integrality_congruence',row=ri,base=base,gcd=g)
  low=max(0,-((-L)//D));high=min(3,H//D)
  if low>high:return None,dict(kind='integral_interval',row=ri,interval=[L,H],denominator=D)
  mins.append(low);maxs.append(high)
 return (mins,maxs,deductions),None

def complete(rec):
 D,M=affine(rec);q=len(rec['free_indices']);locdict={tuple(t):i for i,o in enumerate(rec['orbits'])for t in o};loc=[locdict[t]for t in itertools.product(range(8),repeat=3)]
 tree=[];solutions=[]
 def dfs(dom,parent=None,choice=None):
  nid=len(tree);record=dict(node=nid,parent=parent,choice=choice);tree.append(record)
  got,reason=propagate(dom,M,D)
  if reason:record['reject']=reason;return
  mins,maxs,deductions=got;record['domains_after_affine_propagation']=[list(d)for d in dom];record['affine_deductions']=deductions
  openvars=[j for j in range(q)if len(dom[j])>1]
  if not openvars:
   need(mins==maxs,'fixed variables give integral tensor');T=[[[mins[locdict[i,j,k]]for k in range(8)]for j in range(8)]for i in range(8)]
   du=validate(T);expected=list(range(8))
   if rec['dual_a']:expected[1],expected[2]=2,1
   if rec['dual_b']:expected[3],expected[4]=4,3
   need(du==expected,'actual duality branch');solutions.append(T);record['solution']=len(solutions)-1;return
  j=min(openvars,key=lambda j:(len(dom[j]),-sum(row[j]!=0 for row in M),j));record['branch_variable']=j;record['coefficient_orbit']=rec['orbits'][rec['free_indices'][j]]
  for v in dom[j]:
   child=dom.copy();child[j]=(v,);dfs(child,nid,[j,v])
 dfs([(0,1,2,3)]*q)
 # A separate direct check of every source induction coordinate and dimension.
 C=source()
 for T in solutions:
  for i,j in itertools.product(range(8),repeat=2):need(tuple(sum(T[i][j][k]*dims[k][h]for k in range(8))for h in(0,1))==mul(dims[i],dims[j]),'direct dimensions')
  for i,j,z in itertools.product(range(8),repeat=3):
   lhs=sum(B[i,x]*B[j,y]*T[x][y][z]for x in range(8)for y in range(8))
   rhs=sum(C[i][a][u]*C[u][j][t]*B[t,z]for a in(0,4)for u in range(8)for t in range(8))
   need(lhs==rhs,'direct full induction identity')
 return dict(dual_a=rec['dual_a'],dual_b=rec['dual_b'],complete=True,variables=rec['variables'],free_variables=q,nodes=len(tree),labelled_solutions=len(solutions),tree=tree,tensors=solutions)

def canonical(T):
 vals=[]
 for a,b in itertools.product(range(2),repeat=2):
  p=list(range(8))
  if a:p[1],p[2]=p[2],p[1]
  if b:p[3],p[4]=p[4],p[3]
  vals.append(tuple(T[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(8),repeat=3)))
 return min(vals)

def main():
 start=time.monotonic();categorical_input=check_categorical_linear_input();proof=json.loads((MODELS/'r721_dual_multiplicity_bound.json').read_text());need(len(proof)==4,'all coefficient bound cases')
 records=[]
 for ix,(da,db)in enumerate(itertools.product(range(2),repeat=2)):
  rec=prepare(da,db);need(rec['linear_consistent'],'linear consistency');check_bound(rec,proof[ix]);row=complete(rec);records.append(row)
  print(json.dumps({k:row[k]for k in('dual_a','dual_b','complete','nodes','labelled_solutions')}),flush=True)
 classes={canonical(t)for r in records for t in r['tensors']};need(len(classes)==1,'unique based-ring completion')
 # All exhaustive completion work is finished before this naming comparison.
 rows=json.loads((REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text());R=next(r['tensor']for r in rows if r['id']=='R8_3_721');p=[0,1,2,4,6,3,5,7]
 T=[[[R[p[i]][p[j]][p[k]]for k in range(8)]for j in range(8)]for i in range(8)];need(canonical(T)in classes,'full512 coefficient identification')
 out=dict(status='PASS',optimized_python=not __debug__,solver='Exact affine integer interval/congruence DFS; no associativity pruning, SAT, MILP, or native solver',all_four_dualities_complete=True,branches=records,
  canonical_classes=1,target='R8_3_721',target_all512_coefficients_match=True,actual_category_exists_before_completion=True,
  depends_on_upstream_census_completeness=False,census_read_only_after_exhaustion=True,
  categorical_linear_input=categorical_input,bound_covectors_freshly_checked=True,linear_constraints_alone_force_the_two_labelled_tensors=True,associativity_only_checked_on_complete_tensors=True,normal_or_optimized_checks_active=True,seconds=time.monotonic()-start,
  source_sha256={p.name:sha(p)for p in[Path(__file__),MODELS/'r721_dual_fusion.py',MODELS/'r721_dual_multiplicity_bound.json']})
 name='r721-exact-completion-optimized.json'if not __debug__ else 'r721-exact-completion.json';(A/name).write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items()if k!='branches'},indent=2))
if __name__=='__main__':main()
