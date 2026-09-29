"""Half-E6 projection in the multiquadratic field Q(sqrt3,sqrt5,i)."""
from round4_higher_real import *
from round4_higher_fast import SmallFieldSpectrum
from exact import field

def data_for(R):
 ar=__import__('round4_higher_mass').data_for(R);a=ambient.data_for(R,3,60);C=a['C'];ce=C.mod.degree();t=s.Symbol('t');K=field(s.Poly(s.minpoly(s.sqrt(3)+s.sqrt(5)+s.I,t),t));e=K.mod.degree()
 # sqrt3=2cos(pi/6), sqrt5=1+2(zeta5+zeta5^-1).
 hc=C.unit**15+C.unit**5+C.unit**55+C.one+2*(C.unit**12+C.unit**48)
 require(not evaluate(K.mod.to_list(),hc,C),'wrong multiquadratic embedding')
 B=s.Matrix.hstack(*(vector(hc**j,ce)for j in range(e)));rows=B.T.rref()[1];inv=B.extract(rows,range(e)).inv();powers=[K.unit**j for j in range(e)]
 autos=[C.unit**j for j in range(60)if math.gcd(j,60)==1];fix=[z for z in autos if evaluate(hc.to_list(),z,C)==hc]
 require(len(fix)*e==ce,'wrong relative Galois subgroup')
 def pull(v):
  vv=vector(v,ce);co=inv*vv.extract(rows,[0]);require(B*co==vv,'trace pullback failed');return sum((K(co[j])*powers[j]for j in range(e)),K.zero)
 images=[pull(sum((z**j for z in fix),C.zero)/C(len(fix)))for j in range(ce)]
 def down(v):return sum((K(co)*images[j]for j,co in enumerate(reversed(v.to_list()))),K.zero)
 phases=sorted({tuple(down(v)for v in ph)for ph in a['phases']},key=lambda ph:tuple(key(v)for v in ph));source=[tuple(down(C.unit**(5*ex*k%60))for k in range(1,4))for ex in[-3,5,2,-4,6,0]]
 tab=a['tab'];tab.K=K;tab.rows=[tuple(down(x)for x in row)for row in tab.rows];tab.codegrees=[down(x)for x in tab.codegrees];tab.ds=[down(x)for x in a['dims']];tab.D=down(a['DD']);tab.dims={};tab.values={};tab.allowed={};tab.compatibility={};tab._automorphisms=list(dict.fromkeys(down(evaluate(hc.to_list(),z,C))for z in autos))
 for z in tab._automorphisms:require(evaluate(z.to_list(),z,K)==K.unit,'trace-field Galois group is not exponent two')
 d=dict(ar);d.update(K=K,ds=tab.ds,D=tab.D,tab=tab,phases=phases,source_phases=source,arith=ar,C=K,DD=tab.D,trace_metadata={'ambient_conductor':60,'ambient_types':len(a['phases']),'complex_types':len(phases),'relative_degree':len(fix),'trace_field':[str(z)for z in K.mod.to_list()]})
 return d

def system(R,data,cols,ep,lab):
 K=data['K'];ds=data['ds'];D=data['D'];n=len(R);tab=data['tab'];types=data['phases'];source=data['source_phases'];g,x=half_e6_subrings(R)[0];objects,module=forced(R,g)
 cache=data.setdefault('_cache',{});ck=tuple(map(tuple,cols))
 if ck not in cache:
  G,vs=high_vectors(data['arith'],cols);sp=Spectrum(tab,cols,[(v,None)for v in vs]);bad=set(map(tuple,sp.forbidden));vs=[v for v in vs if v not in bad];cache[ck]=(G,vs,sp)
 G,vs,sp=cache[ck]
 if sp.missing_low:return None,None,{'spectrum':sp.metadata(),'module':module}
 labels=[(v,ti)for v in vs for ti,ph in enumerate(types)if(not v[g-1]and not v[x-1])or(not v[g-1]and v[x-1]and ph in source[:4])or(v[g-1]and v[g-1]>=v[x-1]and ph==source[4])]
 nv=len(labels);z={v:sum((K(v[i])*ds[i+1]for i in range(n-1)),K.zero)for v in vs};low=[sum((K(sum(c[i]*c[j]for c in cols))*ds[j]for j in range(n)),K.zero)for i in range(n)];A=[];b=[]
 def add(co,rhs):
  for row,val in rational_rows(co,rhs,K):A.append(row);b.append(val)
 for i in range(n-1):
  for j in range(i,n-1):A.append([v[i]*v[j]for v,ti in labels]);b.append(int(G[i,j]))
 for i in range(1,n):
  for power,target in[(1,0),(2,ep[i-1])]:add([K(v[i-1])*z[v]*types[ti][power-1]for v,ti in labels],K(target)*D-low[i])
 DE=K(2)+ds[x]**2;masses=[ds[x],2*ds[x],ds[x],ds[x],ds[x]+K.one,2*ds[x]+K(3)]
 for j,target in enumerate(masses):add([K(v[x-1])*z[v]if types[ti]==source[j]else K.zero for v,ti in labels],D/DE*target-(low[x]if j==5 else K.zero))
 rt=[K.one,source[2][0]**2,source[2][0]**4]
 for i in range(1,n):
  dim=sum(R[i][i][k]*R[k][i][0]for k in range(n));prev=len(A[0]);forced_obj=i in objects;require(not forced_obj or dim%2==0,'odd Clifford rotation dimension')
  for row in A:row.extend([0]*3)
  signs=[-tt for tt in rt]if forced_obj else rt
  add([K(v[i-1])*z[v]*types[ti][2]for v,ti in labels]+[K.zero]*(prev-nv)+[-D*tt for tt in signs],-low[i]);A.append([0]*prev+[1]*3);b.append(dim//2 if forced_obj else dim)
 one=types.index((K.one,)*3);rows,rhs=sp.balance(labels,len(A[0]),one);A+=rows;b+=rhs
 tuples=dict(zip(sp.vectors,sp.types))
 for aa,bb in itertools.combinations_with_replacement(range(1,n),2):
  ha,hb=lab[aa],lab[bb];weights={v:tuples[v][ha]*tuples[v][hb]*tab.dims[v]**2 for v in set(sp.vectors)};rhs=D*tab.dims[tuple(cols[aa])]*tab.values[ha,tuple(cols[bb])]-sum((weights[v]for v in sp.low),K.zero);add([weights[(0,)+v]*types[ti][0]for v,ti in labels]+[K.zero]*(len(A[0])-nv),rhs)
 return A,b,{'spectrum':sp.metadata(),'module':module,'labels':[[list(v),ti]for v,ti in labels],'variables':len(A[0]),'rows':len(A)}
