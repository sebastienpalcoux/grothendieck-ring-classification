from pathlib import Path
import sys,json,itertools
repo=Path(__file__).resolve().parents[3];P=repo/'evidence/rank8_frontier_20261021/noncommutative';sys.path.insert(0,str(P));import central_support as c;import character_modular as md;import rotation_search as base
base.install(); rows=json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text());R=next(r['tensor']for r in rows if r['id']=='R8_3_721');a=c.w.data(R);K=a['K'];cols=a['lows'][10];chs=md.characters(R,a);high=md.full.base.grams.high_columns(a,c.s.Matrix.hstack(*map(c.s.Matrix,cols)))[1];allcols=list(cols)+[(0,)+tuple(v)for v,z in high];vals=[[md.value(ch,v,K)for ch in chs]for v in allcols]
cases=json.loads((P/'verlinde_low_721.json').read_text())['cases']
for case in cases:
 active=[i for i,n in enumerate(case['multiplicities'])if n];perm=case['permutation'];A=[]
 for E,F in itertools.combinations_with_replacement(range(5),2):
  target=a['codegrees'][F]*K(a['multiplicities'][F])*md.value(chs[E],cols[perm[F]],K)-sum((v[E]*v[F]for v in vals[:5]),K.zero)
  A.append([vals[t+5][E]*vals[t+5][F]for t in active]+[target])
 piv=[];rr=0
 for k in range(len(active)):
  j=next((i for i in range(rr,len(A))if A[i][k]!=K.zero),None)
  if j is None:continue
  A[rr],A[j]=A[j],A[rr];v=A[rr][k];A[rr]=[x/v for x in A[rr]]
  for j in range(len(A)):
   if j!=rr:
    v=A[j][k];A[j]=[x-v*y for x,y in zip(A[j],A[rr])]
  piv.append(k);rr+=1
 print('COUNTS',case['multiplicities'],'active',active,'rank',rr,'piv',piv)
 for r in A[:rr]:print([c.ec(x)for x in r])
