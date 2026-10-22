from pathlib import Path
import sys,itertools,functools,json
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'evidence/rank8_next_20261021/r1154'))
import low_action_bounds as l
s=l.s;K=l.K
@functools.lru_cache(None)
def setup(ix):
 counts=l.domain['completions'][ix];ns=[1]*5+counts
 @functools.lru_cache(None)
 def moment(word):
  v=K.zero
  for n,vs,wt in zip(ns,l.values,l.weights):
   if not n:continue
   z=K(n)*wt
   for a in word:z*=vs[a]
   v+=z
  raw=l.c.ec(v);assert len(raw)<=1
  f=F(raw[0])if raw else F(0);assert f.denominator==1
  return int(f)
 def mom(word):return moment(tuple(sorted(word)))
 W=[()]+[(i,)for i in range(1,5)]+l.pairs+l.triples
 G=s.Matrix(len(W),len(W),lambda i,j:mom(W[i]+W[j]));inds=list(G.rref()[1]);B=[W[i]for i in inds];Gi=G.extract(inds,inds).inv()
 Q=list(itertools.combinations_with_replacement(range(1,5),4));V=s.Matrix(len(B),len(Q),lambda i,j:mom(B[i]+Q[j]));C=Gi*V
 H=s.Matrix(len(Q),len(Q),lambda i,j:mom(Q[i]+Q[j]))-V.T*C
 piv=list(H.rref()[1]);Hb=H.extract(piv,piv);Hi=Hb.inv()if piv else s.zeros(0)
 print('PATTERN',ix,'rank3',len(B),'rank_residual4',len(piv),'basis',B,'pivs',[Q[i]for i in piv],flush=True)
 return {'B':B,'Q':Q,'C':C,'H':H,'piv':piv,'Hi':Hi,'mom':mom}
if __name__=='__main__':
 for ix in [6971,8766,8772]:setup(ix)

@functools.lru_cache(None)
def context(ix):
 a=setup(ix);pr=next(z for z in l.fibers['results']if z['index']==ix);ns=[1]+l.domain['completions'][ix]
 sig=tuple(sum(n*v[1]for n,v in zip(ns,co))//den for co,den in l.moment_coefficients.values())
 inds,C,alpha,hh,mom=l.augmented(sig)
 return a,pr['group'],sig,inds,C,hh

@functools.lru_cache(None)
def coordinate(ix,typ,x,t):
 a,group,sig,inds,C,hh=context(ix);row,basis,q,vals=l.row_data(group,typ,x,sig);vb=[row[i]for i in inds]
 zs=[sum(y*C[k][j]for k,y in enumerate(vb))for j in range(20)]
 actual=[z+(F(t)-q)*h for z,h in zip(zs,hh)]
 wd={w:row[i]for i,w in enumerate(l.words)};wd.update(dict(zip(l.triples,actual)))
 v=[F(wd[w])for w in a['B']];z=[sum(v[i]*F(a['C'][i,j])for i in range(len(v)))for j in range(len(a['Q']))]
 alpha=F(a['H'][0,0]);h=[F(a['H'][0,j])/alpha for j in range(len(a['Q']))];q=z[0]
 import math
 B=math.isqrt(alpha.numerator//alpha.denominator)+2;mid=q.numerator//q.denominator;opts=[]
 for val in range(max(0,mid-B),mid+B+2):
  d=F(val)-q
  if d*d>alpha:continue
  actual=[zz+d*hh for zz,hh in zip(z,h)]
  if all(v.denominator==1 and v>=0 for v in actual):opts.append((val,d))
 return tuple(v[5:]),q,tuple(opts)

def iter_witnesses(path):
 import gzip
 ix=pno=None;collect=None;number=0
 with gzip.open(path,'rt')as f:
  for line in f:
   if line.startswith('      "index":'):ix=int(line.split(':')[1].strip().rstrip(','))
   elif line.startswith('      "histogram_solution":'):pno=int(line.split(':')[1].strip().rstrip(','));number=0
   elif line=='        [\n':collect=[line]
   elif collect is not None:
    collect.append(line)
    if line in ('        ],\n','        ]\n'):
     raw=''.join(collect).rstrip().rstrip(',');yield ix,pno,number,json.loads(raw);number+=1;collect=None

def joint(ix,witness):
 import math
 from collections import defaultdict
 a,*_=context(ix);alpha=F(a['H'][0,0]);items=[];minnorm=F(0)
 for row in witness:
  typ,x=row['type'],row['pair11']
  for t,n in row['triple133_histogram']:
   if not n:continue
   v,q,opts=coordinate(ix,typ,x,t)
   if not opts:return 'empty_coordinate',None
   minimum=min(d*d for _,d in opts);minnorm+=n*minimum
   items.append((typ,x,t,n,v,q,opts))
 if minnorm>alpha:return 'rounding_norm',None
 den=math.lcm(alpha.denominator,*(q.denominator for _,_,_,_,_,q,_ in items))
 targetnorm=int(alpha*den*den);entries=[]
 for typ,x,t,n,v,q,opts in items:
  assert all(y.denominator==1 for y in v)
  v=tuple(map(int,v));zs=[int(d*den)for _,d in opts]
  base=min(zs,key=lambda x:x*x);costs=[z*z-base*base for z in zs]
  states=[]
  def visit(k,left,sm,cost,hist):
   if k==len(zs)-1:
    states.append((sm+left*(zs[k]-base),cost+left*costs[k],tuple(hist+[left])));return
   for nn in range(left+1):visit(k+1,left-nn,sm+nn*(zs[k]-base),cost+nn*costs[k],hist+[nn])
  visit(0,n,0,0,[])
  # The high10 eigenspace is known to be scalar for every distinguished action.
  # All vacuum fusion words are constant on its four copies.
  if typ==10:states=[z for z in states if max(z[2])==n]
  entries.append((typ,x,t,n,v,base,opts,states))
 basecost=sum(n*base*base for typ,x,t,n,v,base,opts,states in entries);budget=targetnorm-basecost
 target=tuple(-sum(n*base*v[j]for typ,x,t,n,v,base,opts,states in entries)for j in range(5))
 entries.sort(key=lambda r:len(r[-1]));N=len(entries)
 lows=[[0]*6 for _ in range(N+1)];highs=[[0]*6 for _ in range(N+1)]
 for k in range(N-1,-1,-1):
  _,_,_,_,v,_,_,states=entries[k]
  for j in range(6):
   vals=[cost if j==5 else sm*v[j]for sm,cost,h in states]
   lows[k][j]=lows[k+1][j]+min(vals);highs[k][j]=highs[k+1][j]+max(vals)
 @functools.lru_cache(None)
 def search(k,state):
  if any(state[j]<lows[k][j]or state[j]>highs[k][j]for j in range(6)):return None
  if k==N:return ()if not any(state)else None
  _,_,_,_,v,_,_,states=entries[k]
  for sm,cost,h in states:
   new=tuple(state[j]-sm*v[j]for j in range(5))+(state[-1]-cost,)
   z=search(k+1,new)
   if z is not None:return (h,)+z
  return None
 result=search(0,target+(budget,))
 if result is None:return 'empty_joint_fibre',None
 cert=[]
 for e,hs in zip(entries,result):
  typ,x,t,n,v,base,opts,states=e
  cert.append({'type':typ,'pair11':x,'triple133':t,'quartic1111_histogram':[[val,nn]for (val,d),nn in zip(opts,hs)if nn]})
 return 'passes',cert

def run():
 import time,collections,argparse
 p=argparse.ArgumentParser();p.add_argument('--limit',type=int);p.add_argument('--stop-first',action='store_true');args=p.parse_args()
 allowed={(r['index'],r['histogram_solution'])for r in json.loads((ROOT/'evidence/rank8_research_20261022/r1154_r1795/galois_fixed_review.json').read_text())['results']if r.get('witness')}
 out=collections.defaultdict(collections.Counter);passes=collections.defaultdict(list);first={};start=time.monotonic();done=0
 for ix,pno,no,w in iter_witnesses(ROOT/'evidence/rank8_next_20261021/r1154/joint_triple_after_a2.json.gz'):
  if (ix,pno)not in allowed:continue
  status,cert=joint(ix,w);key=str(ix)+':'+str(pno);out[key][status]+=1;done+=1
  if status=='passes':
   passes[key].append(no)
   first.setdefault(key,{'triple_index':no,'quartic_witness':cert})
  if done%1000==0:print(json.dumps({'done':done,'seconds':round(time.monotonic()-start,2),'counts':{k:dict(v)for k,v in out.items()}}),flush=True)
  if args.stop_first and status=='passes':break
  if args.limit and done>=args.limit:break
 result={'schema':'r1154-quartic-extension-exploration/v1','scope':'Exact necessary fourth-product rank-one Gram extension, not a fusion-matrix completion or categorification','complete':not(args.stop_first or args.limit),'processed':done,'counts':{k:dict(v)for k,v in out.items()},'retained_triple_indices':dict(passes),'first_witnesses':first,'seconds':round(time.monotonic()-start,3)}
 Path(__file__).with_name('quartic_extension_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in('retained_triple_indices','first_witnesses')}),flush=True)
if __name__=='__main__':run()
