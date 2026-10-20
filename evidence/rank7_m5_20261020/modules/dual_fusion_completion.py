"""Enumerate all nonnegative fusion products compatible with the full Morita action."""
if not __debug__:
 raise RuntimeError("This exact certificate requires Python assertions; disable optimization.")
import json,itertools,collections,numpy as np,sys,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];base=Path(__file__).parent
ar=json.load(open(base/'r4982_fullgram_actions.json'));gr=json.load(open(base/'r4982_invertible_group_result.json'));allinv=[tuple(z) for z in ar['invertible_actions']];noninv=[tuple(z) for z in ar['noninvertible_actions']]

def compositions(n,k):
 if k==1:yield(n,);return
 for a in range(n+1):
  for z in compositions(n-a,k-1):yield(a,)+z
reports=[]
for H in gr['passing_subgroups']:
 HH=[gr['identity']]+[g for g in H if g!=gr['identity']];flat=[allinv[g] for g in HH]+noninv;idx={v:i for i,v in enumerate(flat)};M=[np.array(z).reshape(13,13) for z in flat];n=len(M);dual=[idx[tuple(A.T.flat)] for A in M];table={};act={};bad=[]
 for g in range(12):
  for x in range(n):
   v=tuple((M[g]@M[x]).flat);w=tuple((M[x]@M[g]).flat)
   assert v in idx and w in idx;act[g,x]=idx[v];act[x,g]=idx[w]
   table[g,x]=[int(i==idx[v]) for i in range(n)];table[x,g]=[int(i==idx[w]) for i in range(n)]
 bycol={a:[j for j in range(12,n) if M[j][a,0]] for a in range(4,13)};assert all(len(z)==3 for z in bycol.values())
 possibilities={};stats=collections.Counter()
 for x in range(12,n):
  for y in range(12,n):
   prod=M[x]@M[y];ivec=[int(act[dual[x],g]==y) for g in range(12)];rem=prod-sum((c*M[g] for g,c in enumerate(ivec)),np.zeros((13,13),dtype=int));weights=[int(rem[a,0]) for a in range(4,13)];assert all(w>=0 for w in weights);assert sum(weights)<=4
   choices=[list(compositions(w,3)) for w in weights];opts=[]
   for zz in itertools.product(*choices):
    ns=[0]*27
    for a,cs in zip(range(4,13),zz):
     for j,c in zip(bycol[a],cs):ns[j-12]=c
    if np.array_equal(sum((c*M[j+12] for j,c in enumerate(ns) if c),np.zeros((13,13),dtype=int)),rem):opts.append(ivec+ns)
   stats[len(opts)]+=1
   if not opts:bad.append([x,y])
   elif len(opts)==1:table[x,y]=opts[0]
   else:possibilities[f'{x},{y}']=opts
 print('group',HH,'stats',dict(stats),'bad',bad[:10],flush=True)
 rep={'invertible_indices':HH,'product_option_counts':dict(stats),'incompatible_products':bad,'ambiguous_products':possibilities,'duality':dual,'unique_products':{f'{i},{j}':v for (i,j),v in table.items()},'action_matrices':[list(z) for z in flat]};reports.append(rep)
 if not bad and not possibilities:
  N=np.array([[table[i,j] for j in range(n)] for i in range(n)]);fail=[]
  for i in range(n):
   for j in range(n):
    if not np.array_equal(N[i]@N[j],sum((int(N[j,i,k])*N[k] for k in range(n)),np.zeros((n,n),dtype=int))):fail.append([i,j])
  print('associativity failures',len(fail),fail[:10],flush=True);rep['associativity_failures']=fail
 (base/'r4982_dual_fusion_options.json').write_text(json.dumps(reports)+'\n')
