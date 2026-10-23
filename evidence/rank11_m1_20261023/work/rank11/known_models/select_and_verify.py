"""Select and fully replay one categorical model for each of these25 inputs."""
from standard import *
from su2_spin_action import solve_action,equiv as spin_equiv
from twisted_cyclic import action as cyclic_action,equiv as twisted_equiv
from v4_zest import construct as v4_construct

def require(c,msg):
 if not c:raise ValueError(msg)

def reconstruct(kind,p):
 if kind=='pointed':return group(tuple(p['orders']))
 if kind=='ty':return ty(tuple(p['orders']))
 if kind=='su2':return su2(p['level'],p['even'])
 if kind=='rep_dihedral':return rep_dihedral(p['m'],p.get('dicyclic',False))
 if kind=='odd_metaplectic':return metaplectic(p['N'])
 if kind=='even_metaplectic':require(p['N']==8,'SO8');return so8_level2()
 if kind=='half_even_metaplectic':return half_even_metaplectic(p['N'])[0]
 if kind=='pointed_equivariant':
  G=p['group_table'];s=p['automorphism'];n=len(G)
  require(all(G[0][i]==G[i][0]==i and 0 in G[i] for i in range(n)),'groupidentity/inverses')
  require(all(G[G[a][b]][c]==G[a][G[b][c]]for a,b,c in itertools.product(range(n),repeat=3)),'groupassociativity')
  require(sorted(s)==list(range(n))and all(s[s[a]]==a for a in range(n)),'involutivebijection')
  require(all(s[G[a][b]]==G[s[a]][s[b]]for a,b in itertools.product(range(n),repeat=2)),'groupautomorphism')
  return pointed_equivariant(G,s)
 if kind=='ty_cyclic_equivariant':
  oo=tuple(p['orders']);G=abelian_table(oo);n=len(G);s=p['automorphism'];m=p['group_order']
  mod=p.get('bicharacter_modulus',n);C=p.get('bicharacter_exponents',[[a*b%n for b in range(n)]for a in range(n)])
  require(len(C)==n and len({tuple(r)for r in C})==n,'bicharacternondegeneracy')
  require(all(C[a][b]==C[b][a] for a,b in itertools.product(range(n),repeat=2)),'symmetricbicharacter')
  require(all((C[G[a][b]][c]-C[a][c]-C[b][c])%mod==0 for a,b,c in itertools.product(range(n),repeat=3)),'bicharacterlaw')
  require(sorted(s)==list(range(n+1))and s[n]==n,'TYautpermutation')
  require(all(s[G[a][b]]==G[s[a]][s[b]]and C[s[a]][s[b]]==C[a][b]for a,b in itertools.product(range(n),repeat=2)),'orthogonalautomorphism')
  require(all(p.get('parity',[0]*(n+1))[a]==0 for a in range(n)),'paritycharacter')
  return cyclic_equivariant(ty(oo),s,m,p.get('parity'))[0]
 if kind=='associative_C2_zest':
  T=reconstruct(p['base_constructor'],p['base_parameters']);require(T==p['base_tensor'],'zestbase');g=p['grading'];h=p['central_invertible']
  require(p['base_constructor']in['su2','even_metaplectic','half_even_metaplectic','odd_metaplectic','rep_dihedral','pointed_equivariant'],'braidedbase')
  require(g in list(gradings(T)),'grading');require(g[h]==0 and T[h][h][0]==1 and sum(T[h][h])==1,'neutralinvolution')
  return zest(T,g,h)
 if kind=='v4_so8_zest':
  T,lam,g=v4_construct(p['bilinear_parameters']);require(lam==p['cocycle']and g==p['grading']and p['base_tensor']==so8_level2(),'V4zestparameters')
  require(all(lam[a][b]^lam[a^b][c]^lam[b][c]^lam[a][b^c]==0 for a,b,c in itertools.product(range(4),repeat=3)),'V4cocycle')
  return T
 if kind=='su2_spin_equivariant':
  J,mus,stats=SPIN
  require(p['tensorator_exponents_mod2']==[[*k,v]for k,v in J.items()],'spintensorator');require(p['coherence_exponents_mod4']in mus,'spincoherence');require(p['q6j_validation']==stats,'spinexactreceipt')
  return spin_equiv(J,p['coherence_exponents_mod4'])[0]
 if kind=='twisted_cyclic_equivariant':
  s,J,mu=cyclic_action(p['cyclic_order'],p['cocycle_class'],p['automorphism_multiplier']);require(s==p['automorphism']and J==p['tensorator_mod16']and mu==p['coherence_mod32'],'cycliccochains')
  return twisted_equiv(p['cyclic_order'],s,J,mu)[0]
 raise ValueError('unsupportedconstructor '+kind)

def priority(m):
 k=m['constructor']
 order=['pointed','ty','su2','rep_dihedral','odd_metaplectic','even_metaplectic','ty_cyclic_equivariant','pointed_equivariant','v4_so8_zest','associative_C2_zest','half_even_metaplectic','su2_spin_equivariant','twisted_cyclic_equivariant']
 return order.index(k)

def main():
 global SPIN
 SPIN=solve_action();data=targets();rows=collections.defaultdict(list)
 for fn in['standard_models.json','v4_zest_models.json','su2_spin_models.json','twisted_cyclic_models.json']:
  for r in json.load(open(HERE/fn)):
   require(r['tensor_sha256']==tensor_hash(data[r['id']]),'sourcehash');rows[r['id']].extend(r['models'])
 selected=[];constructors=collections.Counter()
 for rid,ms in sorted(rows.items(),key=lambda kv:int(kv[0].split('_')[-1])):
  # Prefer directTYequivariantizations over equivalent half-metaplectic zests.
  m=min(ms,key=priority)
  T=reconstruct(m['constructor'],m['parameters']);require(T==m['model_tensor'],'constructedtensor')
  q=m['basis_map_source_to_model'];R=data[rid]
  require(q[0]==0 and sorted(q)==list(range(11)),'unitalbasisbijection')
  require(all(R[a][b][c]==T[q[a]][q[b]][q[c]]for a,b,c in itertools.product(range(11),repeat=3)),'fullfusiontable')
  validate(T);constructors[m['constructor']]+=1
  selected.append({'id':rid,'tensor_sha256':tensor_hash(R),'status':'unitarily_realized','model':m})
 require(len(selected)==25,'acceptedmodelcount')
 (HERE/'selected_models.json').write_text(json.dumps(selected,indent=2)+'\n')
 report={'status':'PASS','inputs':25,'fusion_coefficients_per_input':1331,'constructors':dict(constructors),'ids':[r['id']for r in selected],'note':'Exactrecipe andallcoefficients; categoricalexistencetheorems inTHEORY.md'}
 (HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
