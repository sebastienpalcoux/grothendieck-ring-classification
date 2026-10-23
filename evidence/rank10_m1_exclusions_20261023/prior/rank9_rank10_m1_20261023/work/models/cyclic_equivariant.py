from extra_models import *
def cyclic_equivariant(R,sigma,m,parity=None):
 n=len(R);parity=parity or [0]*n;seen=set();labs=[]
 for a in range(n):
  if a in seen:continue
  O=[];b=a
  while b not in O:O.append(b);b=sigma[b]
  assert b==a and m%len(O)==0;seen.update(O)
  for j in range(m//len(O)):labs.append((O,j))
 powers=[list(range(n))]
 for t in range(1,m):powers.append([sigma[powers[-1][a]]for a in range(n)])
 import sympy as s
 z=s.exp(2*s.pi*s.I/(2*m))
 rank=len(labs);T=[[[0]*rank for _ in range(rank)]for _ in range(rank)]
 for i,(A,ja) in enumerate(labs):
  for j,(B,jb) in enumerate(labs):
   for k,(C,jc) in enumerate(labs):
    c=C[0];val=0;lc=len(C)
    for h in range(0,m,lc):
     tr=sum(R[a][b][c]for a in A for b in B if powers[h][a]==a and powers[h][b]==b)
     val+=tr*z**(((2*(ja+jb-jc)+parity[A[0]]+parity[B[0]]-parity[C[0]])*h)%(2*m))
    val=s.simplify(val/(m//lc));assert val.is_Integer and val>=0
    T[i][j][k]=int(val)
 return T,labs

def run():
 known=json.load(open(OUT/'known_models_central.json'));lookup={x['id']:x for x in known};new=[]
 R=ty((3,));sigma=[0,2,1,3];T,labs=cyclic_equivariant(R,sigma,4)
 for i,S in enumerate(read(10),1):
  bm=based_iso(S,T)
  if bm is None:continue
  rid=f'R10_1_{i}'
  if rid not in lookup:lookup[rid]={'id':rid,'tensor_sha256':tensor_hash(S),'status':'unitarily_realized','models':[]};new.append(rid)
  lookup[rid]['models'].append({'model':'TY(C3)^C4, generator acts by inversion','constructor':'ty_cyclic_equivariant','parameters':{'orders':[3],'group_order':4,'automorphism':sigma,'base_tensor':R,'labels':labs},'reference':'Canonical inversion action preserves the nondegenerate symmetric bicharacter onC3 and standardTY associator; inflate actionC2 toC4, then unitary equivariantization','basis_map_source_to_model':bm,'model_tensor':T});print(rid)
 known=sorted(lookup.values(),key=lambda x:tuple(map(int,x['id'].replace('R','').split('_'))))
 (OUT/'known_models_cyclic.json').write_text(json.dumps(known,indent=2)+'\n');print('NEW',new)
if __name__=='__main__':run()
