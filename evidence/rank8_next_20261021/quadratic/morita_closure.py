"""Exact Morita internal-end dimension closure on complete finite algebra targets."""
from fractions import Fraction as F
import json,collections
from gram_discovery import HERE,require
DATA={
 'R8_3_65':(5,[(1,0),(1,0),(1,0),*[(F(11,2),F(5,2))]*4,(1,0)]),
 'R8_3_1768':(37,[(1,0),(1,0),(5,1),(6,1),(7,1),(7,1),(6,1),(5,1)]),
 'R8_3_1795':(5,[(1,0),(1,0),(6,3),(7,3),(7,3),(7,3),(7,3),(6,3)]),
 'R8_3_3472':(2,[(1,0),(6,5),(6,5),(7,5),(6,5),(8,5),(8,5),(8,5)]),
}
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(a,b,n):return (a[0]*b[0]+n*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def div(a,b,n):
 den=b[0]*b[0]-n*b[1]*b[1];require(den!=0,'nonzero denominator')
 c=mul(a,(b[0],-b[1]),n);return(F(c[0])/den,F(c[1])/den)
def dim(v,ds):return tuple(sum(F(x)*d[j]for x,d in zip(v,ds))for j in (0,1))
def enc(x):return [str(v)for v in x]
def run():
 recs=json.loads((HERE/'integral_gram.json').read_text());module=json.loads((HERE/'module_rows.json').read_text())
 require(len(module)==len(recs),'module row screen complete')
 mids={(x['id'],x['candidate_index']):set(x['surviving_factor_indices'])for x in module};out={}
 for rid,(n,ds)in DATA.items():
  rs=[x for x in recs if x['id']==rid];adims={x['candidate_index']:dim(x['algebra_object'],ds)for x in rs}
  vdim={x['candidate_index']:[div(mul(dim(v,ds),dim(v,ds),n),adims[x['candidate_index']],n)for v in x['vectors']]for x in rs}
  factors={x['candidate_index']:sorted(mids[(rid,x['candidate_index'])])for x in rs}
  stages=[]
  while True:
   live={i for i,fs in factors.items()if fs};available={adims[i]for i in live};changes=[];nxt={}
   for x in rs:
    ai=x['candidate_index'];bad=[];keep=[]
    for fi in factors[ai]:
     why=next((j for j,k in enumerate(x['all_multiplicities'][fi])if k and vdim[ai][j]not in available),None)
     if why is None:keep.append(fi)
     else:bad.append({'factor_index':fi,'row_type_index':why,'required_internal_end_dimension':enc(vdim[ai][why])})
    nxt[ai]=keep
    if bad:changes.append({'candidate_index':ai,'removed_factors':bad})
   stages.append({'starting_algebras':len(live),'starting_factors':sum(map(len,factors.values())),'changes':changes})
   if nxt==factors:break
   factors=nxt
  survivors=[{'candidate_index':x['candidate_index'],'algebra_object':x['algebra_object'],'dimension':enc(adims[x['candidate_index']]),'factor_indices':factors[x['candidate_index']]}for x in rs if factors[x['candidate_index']]]
  out[rid]={'radicand':n,'dimension_pairs':[enc(x)for x in ds],'stages':stages,'survivors':survivors,'surviving_algebras':len(survivors),'surviving_factors':sum(len(x['factor_indices'])for x in survivors)}
  print(rid,' -> '.join(f"{q['starting_algebras']}/{q['starting_factors']}"for q in stages),flush=True)
 (HERE/'morita_closure.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
 return out
if __name__=='__main__':run()
