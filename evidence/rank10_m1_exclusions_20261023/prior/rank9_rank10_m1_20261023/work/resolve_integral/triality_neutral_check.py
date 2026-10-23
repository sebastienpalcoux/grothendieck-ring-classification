"""Exact input structure and TY bicharacter elimination for R9_1_117."""
import json,itertools
from pathlib import Path
P=Path(__file__).parent;ROOT=P.parents[1]
N=json.load(open(ROOT/'work/input_audit/tensors.json'))['R9_1_117'];n=len(N)
dual=[next(j for j in range(n)if N[i][j][0])for i in range(n)]
I=[i for i in range(n)if sum(N[i][dual[i]])==1]
d=[1 if i in I else 2 for i in range(n)]
assert all(sum(N[i][j][k]*d[k]for k in range(n))==d[i]*d[j]for i,j in itertools.product(range(n),repeat=2))
assert len(I)==4 and all(dual[i]==i for i in I)
A={0}|{k for i in range(n)for k in range(n)if N[i][dual[i]][k]}
while True:
 B=A|{k for i in A for j in A for k in range(n)if N[i][j][k]}
 if B==A:break
 A=B
assert len(A)==5 and set(I)<A
m=next(iter(A-set(I)));outside=sorted(set(range(n))-A)
assert all(N[m][m][k]==int(k in I)for k in range(n))
witness=[]
for x in outside:
 l=[g for g in I if N[g][x][x]];rr=[g for g in I if N[x][g][x]]
 assert len(l)==len(rr)==2 and l!=rr
 hl=next(g for g in l if g);hr=next(g for g in rr if g)
 assert N[x][dual[x]]==[int(k in[0,hl,m])for k in range(n)]
 assert N[dual[x]][x]==[int(k in[0,hr,m])for k in range(n)]
 witness.append({'x':x,'h_left':hl,'h_right':hr})
# Adjoint grading components are equivalence classes under left A action.
parts=[];seen=set()
for x in range(n):
 if x in seen:continue
 C={k for a in A for k in range(n)if N[a][x][k]};parts.append(sorted(C));seen|=C
assert sorted(map(len,parts))==[2,2,5]
forms=[]
for a,b,c in itertools.product(range(2),repeat=3):
 if (a*c-b*b)%2!=1:continue
 iso=[v for v in[1,2,3]if (a*(v&1)+c*((v>>1)&1))%2==0]
 forms.append({'matrix':[[a,b],[b,c]],'nonzero_isotropic':iso,'alternating':a==c==0})
assert len(forms)==4 and all(len(f['nonzero_isotropic'])==(3 if f['alternating']else 1)for f in forms)
report={'status':'PASS','id':'R9_1_117','dimensions':d,'invertibles':I,'adjoint_basis':sorted(A),'TY_object':m,'universal_grading_components':parts,'internal_end_witnesses':witness,'symmetric_nondegenerate_forms':forms,'only_alternating_form_has_two_distinct_isotropic_nonzero_vectors':True}
P.joinpath('triality_neutral_check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS neutral TY(V4), universal C3, distinct left/right stabilizers, alternating chi forced')
