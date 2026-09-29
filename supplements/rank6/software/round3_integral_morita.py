"""Exact integer multiplicity refinement of the full Morita Gram equations.

Integral separation certificates use exact modular row combinations.
No optimizer is called by the verifier. The domain is reconstructed from
the full fusion tensor, with no ring identifiers or dimension lookup.
"""
from exact import require
from higher_traces import check_farkas,farkas

def reduced(A,b):
 rows=sorted(set(tuple(row)+(v,) for row,v in zip(A,b) if any(row) or v))
 return [list(row[:-1]) for row in rows],[row[-1]for row in rows]

def modular_ray(A,b,p=2):
 """Propose y with y A=0 but y b nonzero over F_p."""
 if not A:return None
 m=len(A);n=len(A[0]);basis={}
 for i in range(m):
  row=[x%p for x in A[i]]+[b[i]%p];y=[0]*m;y[i]=1
  while True:
   j=next((j for j,v in enumerate(row[:-1])if v),None)
   if j is None:
    if row[-1]:return {'method':'modular','modulus':p,'y':y}
    break
   if j not in basis:
    inv=pow(row[j],-1,p);row=[z*inv%p for z in row];y=[z*inv%p for z in y];basis[j]=(row,y);break
   rr,yy=basis[j];f=row[j];row=[(v-f*z)%p for v,z in zip(row,rr)];y=[(v-f*z)%p for v,z in zip(y,yy)]
 return None

def verify_system(A,b,c):
 A,b=reduced(A,b)
 require(bool(A),'empty equality system has no modular contradiction')
 require(c.get('method')=='modular','unknown integral Morita method')
 p=c['modulus'];y=c['y']
 require(type(p)is int and p>1 and len(y)==len(A)and all(type(v)is int for v in y),'bad modular ray')
 require(all(sum(y[i]*A[i][j]for i in range(len(A)))%p==0 for j in range(len(A[0]))),'nonzero modular column pairing')
 require(sum(x*z for x,z in zip(y,b))%p!=0,'zero modular right pairing')
 return True


def certificate(R,height=6,progress=None):
 """Combine integral Morita Gram branches with forced Clifford indicators."""
 import stabilizer_rotation_higher as H
 n=len(R)
 if any(R[i][j]!=R[j][i]for i in range(n)for j in range(n)):raise H.Ineligible('commutative input required')
 eligible=False
 for g in H.invs(R):
  info=H.anti_representations(R,g)
  if info is None:continue
  eligible=True;fixed,seed,nodes,reps=info;branches=[];conditionals=[];cache={};failed=False
  for T in reps:
   ab,meta=H.C.morita_system(R,g,fixed,T);branch={'T':list(map(list,T)),'meta':meta}
   if ab is None:branch['method']='morita_rank'
   else:
    A,b=reduced(*ab);congruence=modular_ray(A,b,2)
    if congruence is not None:
     verify_system(*ab,congruence);branch.update(method='morita_integral',integral=congruence)
    else:
     ray=H.C.zero_column_ray(*ab)
     if ray is not None:H.check_farkas(*ab,ray);branch.update(method='morita_gram',y=ray)
     else:
      objects=H.objects_for(R,g,fixed,T)
      if any(H.cubic(R,y)%2 for y in objects):branch.update(method='odd_cubic',objects=objects)
      elif objects:
       key=tuple(objects)
       if key not in cache:
        try:cc=H.discover_conditional(R,objects,height,progress)
        except H.Survives:cc=None
        if cc is None:cache[key]=None
        else:cache[key]=len(conditionals);conditionals.append(cc)
       if cache[key] is None:failed=True;break
       branch.update(method='higher_stabilizer',objects=objects,conditional=cache[key])
      else:failed=True;break
   branches.append(branch)
  if not failed:return {'kind':'integral_morita_rotation','version':1,'scope':'pseudo_unitary','involution':g,'fixed':fixed,'generators':list(seed),'generator_tuples':nodes,'branches':branches,'conditionals':conditionals}
 if not eligible:raise H.Ineligible('no eligible forced involution module')
 raise H.Survives('a necessary integral module/center branch survives')

def verify(R,c):
 import stabilizer_rotation_higher as H
 require(c.get('kind')=='integral_morita_rotation' and c.get('version')==1 and c.get('scope')=='pseudo_unitary','bad integral Morita rotation certificate')
 g=c['involution'];require(g in H.invs(R),'invalid involution');fixed,seed,nodes,reps=H.anti_representations(R,g)
 require(c['fixed']==fixed and c['generators']==list(seed)and c['generator_tuples']==nodes,'incorrect module domain')
 require([b['T']for b in c['branches']]==[list(map(list,T))for T in reps],'missing module branch')
 for cc in c['conditionals']:H.verify_conditional(R,cc)
 used=set()
 for T,b in zip(reps,c['branches']):
  ab,meta=H.C.morita_system(R,g,fixed,T);require(b['meta']==meta,'wrong Morita system')
  if ab is None:require(b['method']=='morita_rank','wrong rank rejection');continue
  method=b['method']
  if method=='morita_gram':H.check_farkas(*ab,b['y'])
  elif method=='morita_integral':verify_system(*ab,b['integral'])
  elif method=='odd_cubic':
   objs=H.objects_for(R,g,fixed,T);require(objs==b['objects']and any(H.cubic(R,y)%2 for y in objs),'wrong odd cubic condition')
  else:
   require(method=='higher_stabilizer','unknown module branch method');objs=H.objects_for(R,g,fixed,T);ix=b['conditional']
   require(type(ix)is int and 0<=ix<len(c['conditionals'])and objs and objs==b['objects']==c['conditionals'][ix]['objects'],'wrong forced indicator objects');used.add(ix)
 require(used==set(range(len(c['conditionals']))),'unused conditional records');return True

def verify_general(R,c):
 import galois_pseudo_reduction as G
 require(c.get('kind')=='general_integral_morita_rotation'and c.get('version')==1 and c.get('scope')=='general','bad general integral Morita rotation certificate')
 G.verify(R,c['reduction']);verify(R,c['pseudo']);return True
