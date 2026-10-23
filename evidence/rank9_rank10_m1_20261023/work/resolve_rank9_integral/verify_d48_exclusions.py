"""Exact finite data for the D48 exclusion theorem; no floating arithmetic."""
from pathlib import Path
import itertools,json,math
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DATA=json.loads((ROOT/'work/input_audit/tensors.json').read_text())
AUDIT=json.loads((ROOT/'work/input_audit/audit.json').read_text())
RECS={r['id']:r for n in ['9','10']for r in AUDIT[n]['rings']}
TARGETS=[f'R9_1_{i}'for i in [12,62,87,108]]
def dims(rid):
 sq=RECS[rid]['squared_fp_dimensions_exact'];d=[math.isqrt(v)for v in sq]
 assert all(a*a==b for a,b in zip(d,sq))
 T=DATA[rid];n=len(T)
 assert d[0]==1 and all(sum(T[i][j][k]*d[k]for k in range(n))==d[i]*d[j]for i,j in itertools.product(range(n),repeat=2))
 return d

def orbits(p):
 seen=set();out=[]
 for i in range(len(p)):
  if i in seen:continue
  o=[];j=i
  while j not in o:o.append(j);seen.add(j);j=p[j]
  out.append(sorted(o))
 return out

def dual(T):return[next(j for j in range(len(T))if T[i][j][0])for i in range(len(T))]
def adjoint(T):
 n=len(T);star=dual(T);a={0}|{k for i in range(n)for k in range(n)if T[i][star[i]][k]}
 while True:
  b=a|{k for i,j in itertools.product(a,repeat=2)for k in range(n)if T[i][j][k]}
  if a==b:return sorted(a)
  a=b

profiles={}
for rid in TARGETS:
 T=DATA[rid];d=dims(rid);n=len(T);inv=[i for i in range(n)if d[i]==1]
 assert len(inv)==4 and all(T[g][g][0]==1 for g in inv)
 assert adjoint(T)==list(range(n))
 rows=[]
 for g in inv[1:]:
  p=[T[g][i].index(1)for i in range(n)];oo=orbits(p);dd=[]
  for o in oo:
   if len(o)==2:dd.append(d[o[0]])
   else:assert d[o[0]]%2==0;dd.extend([d[o[0]]//2]*2)
  rows.append({'sign':g,'source_orbits':oo,'quotient_profile':sorted(dd)})
 assert sorted(tuple(r['quotient_profile'])for r in rows)==sorted([(1,)*8+(4,),(1,)*4+(2,4),(1,)*4+(2,)*5])
 profiles[rid]=rows

# Independently replay every directly enumerated quotient; exhaustiveness is
# proved by direct_quotient.py's binary search, not by a quotient catalog.
DIRECT=json.loads((ROOT/'work/resolve_rank9_neargroup/direct_quotient.json').read_text())
COUNTS={}
for rec in DIRECT['sources']:
 rid=rec['source'];C=DATA[rid];F=rec['restriction'];Ddim=DIRECT['quotient_dimensions'];alpha=DIRECT['involution'];count=0
 assert rec['sign']==next(x['sign']for x in profiles[rid]if x['quotient_profile']==[1]*4+[2]*5)
 for branch in rec['dual_branches']:
  star=branch['dual']
  for sol in branch['solutions']:
   T=sol['tensor'];p=sol['quotient_to_R117'];R=DATA['R9_1_117'];count+=1
   assert all(T[i][j][k]in [0,1]for i,j,k in itertools.product(range(9),repeat=3))
   assert all(T[0][i][j]==T[i][0][j]==int(i==j)and T[i][j][0]==int(star[i]==j)for i,j in itertools.product(range(9),repeat=2))
   assert all(T[i][j][k]==T[alpha[i]][alpha[j]][alpha[k]]==R[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(9),repeat=3))
   assert all(sum(T[i][j][k]*Ddim[k]for k in range(9))==Ddim[i]*Ddim[j]for i,j in itertools.product(range(9),repeat=2))
   assert all(sum(C[i][j][h]*F[h][k]for h in range(9))==sum(F[i][a]*F[j][b]*T[a][b][k]for a,b in itertools.product(range(9),repeat=2))for i,j,k in itertools.product(range(9),repeat=3))
   assert all(sum(T[i][j][h]*T[h][k][l]for h in range(9))==sum(T[j][k][h]*T[i][h][l]for h in range(9))for i,j,k,l in itertools.product(range(9),repeat=4))
 assert count==4
 COUNTS[rid]=count
assert set(COUNTS)==set(TARGETS)

# C4 neutral group: all quadratic automorphisms of C4+C4*.
O4=[]
for a,b,c,d in itertools.product(range(4),repeat=4):
 if (a*d-b*c)%2!=1:continue
 if all(((a*x+b*y)*(c*x+d*y)-x*y)%4==0 for x,y in itertools.product(range(4),repeat=2)):O4.append((a,b,c,d))
assert set(O4)=={(1,0,0,1),(3,0,0,3),(0,1,1,0),(0,3,3,0)}

def app(M,x):return sum(((M[i]&x).bit_count()%2)<<i for i in range(4))
def mul(M,N):return tuple(sum((sum(((M[i]>>k)&1)*((N[k]>>j)&1)for k in range(4))%2)<<j for j in range(4))for i in range(4))
def q(x):return ((x&3)&(x>>2)).bit_count()%2
I=(1,2,4,8)
O=[M for M in itertools.product(range(16),repeat=4)if len({app(M,x)for x in range(16)})==16 and all(q(app(M,x))==q(x)for x in range(16))]
assert len(O)==72
C3=[]
for M in O:
 beta=(M[0]>>2,M[1]>>2)
 if M==I or mul(mul(M,M),M)!=I or not all(beta)or beta[0]==beta[1]:continue
 fixed=[x for x in range(16)if app(M,x)==x]
 assert all(q(x)==1 for x in fixed if x)
 C3.append({'matrix_rows':M,'fixed_vectors':fixed,'nonzero_fixed_quadratic_values':[q(x)for x in fixed if x]})
assert len(C3)==6
RECEIPT={'targets':TARGETS,'excluded':['R9_1_62','R9_1_87'],'source_profiles':profiles,'direct_quotient_receipt':'work/resolve_rank9_neargroup/direct_quotient.json','direct_quotient_completion_counts':COUNTS,'C4_quadratic_automorphisms':O4,'V4_orthogonal_group_order':len(O),'all_C3_rank_one_matrices':C3,'claim':'Exact finite checks supporting D48_EXCLUSIONS.tex; categorical implications are proved there.'}
(HERE/'d48_exclusions_receipt.json').write_text(json.dumps(RECEIPT,indent=2)+'\n')
print('PASS: four source trichotomies; all sixteen direct quotient completions independently verified as R117; C4 obstruction; six V4 matrices with no nonzero isotropic fixed vector.')
print('Direct quotient completions:',COUNTS)
