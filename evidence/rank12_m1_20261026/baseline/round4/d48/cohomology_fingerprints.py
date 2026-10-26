from h8_models import *

def cyc(G,W):
 fp=[]
 for a in range(len(G)):
  x=0;v=0
  while True:
   v+=int(W[a,x,a]);x=G[x][a]
   if not x:break
  fp.append(v%8)
 return fp

def alt(W,a,b,c):return int(W[a,b,c]+W[b,c,a]+W[c,a,b]-W[a,c,b]-W[c,b,a]-W[b,a,c])%8

def main():
 ps,S,vs=s4_cocycles();_,_,beta=schur_cover();par=[sum(p[i]>p[j]for i in range(4)for j in range(i+1,4))%2 for p in ps];ix={p:i for i,p in enumerate(ps)};pairs=json.loads((OUT/'h8_pairs.json').read_text());receipt=[]
 for gi in [30,48]:
  row=next(r for r in pairs if r['smallgroup'][1]==gi);G=row['table'];pr=np.array([ix[tuple(v-1 for v in p)]for p in row['projection_permutations']]);q=np.array(row['quotient_character']);B=np.array(beta)[pr[:,None],pr[None,:]];sg=np.array(par)[pr]
  triples=[(a,b,c)for a,b,c in itertools.combinations(range(1,48),3)if G[a][b]==G[b][a]and G[a][c]==G[c][a]and G[b][c]==G[c][b]]
  fps={};allrows=[]
  extra=list(itertools.product(range(2),repeat=3))if gi==48 else [(k,)for k in range(4)]
  for bits,V in vs:
   base=2*V[pr[:,None,None],pr[None,:,None],pr[None,None,:]]
   for ex in extra:
    W=base.copy()
    if gi==48:W+=4*(ex[0]*q[:,None,None]*q[None,:,None]*q[None,None,:]+ex[1]*sg[:,None,None]*q[None,:,None]*q[None,None,:]+ex[2]*q[:,None,None]*B[None,:,:])
    else:W+=2*ex[0]*q[:,None,None]*((q[None,:,None]+q[None,None,:])//4)
    W%=8;fp=cyc(G,W)+[alt(W,*t)for t in triples];fps.setdefault(tuple(fp),[]).append(dict(bits=bits,extra=ex));allrows.append(dict(parameters=dict(bits=bits,extra=ex),fingerprint=fp))
  receipt.append(dict(smallgroup=[48,gi],generated_parameter_choices=len(allrows),provably_distinct_classes=len(fps),cyclic_restrictions=48,commuting_triples=triples,rows=allrows));print(gi,len(allrows),len(fps),flush=True)
 (OUT/'cohomology_fingerprints.json').write_text(json.dumps(receipt,separators=(',',':'))+'\n')
if __name__=='__main__':main()
