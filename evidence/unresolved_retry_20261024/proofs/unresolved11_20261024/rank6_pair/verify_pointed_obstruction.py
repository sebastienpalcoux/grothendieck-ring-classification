from pathlib import Path
import json,itertools,hashlib
P=Path(__file__).resolve().parent
r=json.loads((P.parent/'inputs/R6_4_155.json').read_text());N=r['fusion_tensor'];n=len(N)
need=lambda c,m:None if c else (_ for _ in ()).throw(ValueError(m))
hash_=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest();need(hash_==r['tensor_sha256'],'tensor hash')
inv=r['invariants']['invertible_indices'];non=[i for i in range(n)if i not in inv]
autos=[]
for t in itertools.permutations(range(1,n)):
 p=(0,)+t
 if all(N[i][j][k]==N[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(n),repeat=3)):autos.append(p)
fixed=[p for p in autos if all(p[i]==i for i in inv)]
# X X* contains the unit and both noninvertibles: any scalar tensor
# automorphism of Id must consequently be one on the noninvertibles.
x=non[0];y=r['invariants']['dual_indices'][x]
need(N[x][y][0]==1 and all(N[x][y][i]>0 for i in non),'trivial identity-automorphism premise')
# Each pointed scalar is then one by its action on either noninvertible.
need(all(sum(N[a][x][i] for i in non)==1 for a in inv),'pointed scalar premise')
# D8=(a,b), a mod4,b mod2, with (a,b)(c,d)=(a+(-1)^b c,b+d).
mul=lambda x,y:((x[0]+(-1)**x[1]*y[0])%4,(x[1]+y[1])%2)
G=list(itertools.product(range(4),range(2)));V=[(0,0),(2,0),(0,1),(2,1)];outside=(1,0);inverse=(3,0)
conj=[mul(mul(outside,v),inverse)for v in V]
need(set(conj)==set(V)and conj!=V,'nontrivial D8 conjugation')
out={'status':'PASS','tensor_sha256':hash_,'ring_automorphisms':[list(x)for x in autos],'pointed_fixed_ring_automorphisms':[list(x)for x in fixed],'D8_Klein_four':[list(x)for x in V],'D8_outside_conjugation':[list(x)for x in conj],'scope':'Exact ring and group premises only; categorical central twists use the cited published proof. R6_4_155 remains unresolved.'}
(P/'pointed_obstruction_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
