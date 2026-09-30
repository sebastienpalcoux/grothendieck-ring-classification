from pathlib import Path
import sympy as s,json,hashlib,itertools
P=Path(__file__).parent;p=json.load(open(P/'b2_7_graph_extraction.json'));order=[i-1 for i in p['matches_to_N4'][0]];B=s.Matrix(p['matrices']['brown']);E=B.extract(order,order);I=s.eye(6)
# Label order 1,x,x*,g,e,f is determined by the graph up to x<->x*.
Gs=[]
for swap in [False,True]:
 perm=[3,2 if swap else 1,1 if swap else 2,0,4,5];G=s.zeros(6)
 for i,j in enumerate(perm):G[i,j]=1
 F=(E*E-I-G)/2
 if all(v.is_Integer and v>=0 for v in F):Gs.append((G,F))
if len(Gs)!=1:raise RuntimeError('pointed action not uniquely recovered')
G,F=Gs[0];Sum=E*F-2*E-2*F
v=s.symbols('x0:36');X=s.Matrix(6,6,v);eq=list(X+G*X-Sum)+list(X.T-G*X)+list(X*E-E*X)+list(X*F-F*X)+list(X*G-G*X)
eq += [X[0,j]-int(j==1) for j in range(6)]
A,b=s.linear_eq_to_matrix(eq,v);sol=s.linsolve((A,b),v)
if len(sol)!=1:raise RuntimeError('ambiguous matrix system')
x=next(iter(sol))
if any(z.free_symbols for z in x):raise RuntimeError('undetermined variables')
X=s.Matrix(6,6,x);N=[I,X,G*X,G,E,F]
if any(not q.is_Integer or q<0 for M in N for q in M):raise RuntimeError('not fusion matrices')
for i,j in itertools.product(range(6),repeat=2):
 if N[i]*N[j]!=sum((N[i][j,k]*N[k] for k in range(6)),s.zeros(6)):raise RuntimeError('associativity')
plain=[[[int(M[j,k])for k in range(6)]for j in range(6)]for M in N]
r=next(r for r in json.load(open(P.parent/'data/model_input_tensors.json'))if r['id']=='R6_4_22')
if plain!=r['N']:raise RuntimeError('tensor mismatch')
receipt=dict(source='Coquereaux--Rais--Tahri, arXiv:1001.5416, Section 3.5, Figure 11(a)',figure_vertex_order=[i+1 for i in order],id='R6_4_22',categorical_duality_input='The odd local spinor z has z^2=g; the odd fundamental free module s is self-dual and central. Thus (zs)^*=g(zs).',pointed_action_candidates=2,integral_candidates=len(Gs),linear_variables=36,linear_rank=A.rank(),equations=A.rows,all_tensor_entries_match=True,associativity_checked=True,tensor=plain)
json.dump(receipt,open(P/'b2_7_tensor_certificate.json','w'),indent=2)
print(json.dumps({k:v for k,v in receipt.items()if k!='tensor'},indent=2))
