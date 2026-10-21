"""Reduce all remaining distinguished actions to a single bounded matrix N1."""
import sys,json,math,itertools
from pathlib import Path
from fractions import Fraction as F
UP=Path(__file__).resolve().with_name('a2_action_probe.py')
exec(compile(UP.read_text().split('start=time.monotonic();')[0],str(UP),'exec'))
PATTERNS=[6971,8766,8772]
def build(ix):
 row=next(z for z in fibers['results']if z['index']==ix);hist=row['pair11_histogram_solutions_by_high_type'][0];counts=domain['completions'][ix];ns=[1]+counts;sig=tuple(sum(n*v[1]for n,v in zip(ns,co))//den for co,den in moment_coefficients.values());inds,H,tr,tr2,cp,moments=action(sig)
 vecs=[];labels=[];types=[]
 for j in range(5):
  v=[int(j==k)for k in range(5)]+[moments[tuple(sorted(pair+(j,)))]if j else int(pair[0]==pair[1])for pair in pairs]+list(cols[j]);vecs.append([F(v[i])for i in inds]);labels.append({'low':j});types.append(j)
 for typ,his in enumerate(hist):
  for x,n in his:
   if n:
    rr,*_=row_data(row['group'],typ,x,sig)
    for k in range(n):vecs.append([rr[i]for i in inds]);labels.append({'type':typ,'pair11':x});types.append(5+typ)
 V=s.Matrix(vecs);N2=V*s.Matrix(H)*V.T;at=[i for i,lab in enumerate(labels)if lab.get('type')==10]
 for i in at:
  for j in at:N2[i,j]+=s.Rational(1,4)-int(i==j)
 need(all(x.q==1 and x>=0 for x in N2),'known A2 nonnegative integer action')
 u=[[dims[typ]*values[typ][E]/a['D']for typ in types]for E in range(5)]
 need(all(sum((x*y for x,y in zip(ui,uj)),K.zero)==K(int(i==j))for i,ui in enumerate(u)for j,uj in enumerate(u)),'five exact low spectral projectors')
 for typ,n in enumerate(counts):
  if n:
   vs=values[typ+5];need(vs[3]-vs[1]-K.one==K(-3 if typ==10 else 0),'high A3 relation');need(vs[4]+vs[1]+K.one==K(2 if typ==10 else 0),'high A4 relation')
 C3=[values[E][3]-values[E][1]-K.one-K(3)*values[E][2]for E in range(5)]
 C4=[values[E][4]+values[E][1]+K.one+K(2)*values[E][2]for E in range(5)]
 Ks=[]
 for cs,sgn,coef in [(C3,1,3),(C4,-1,-2)]:
  rows=[]
  for i in range(len(labels)):
   rr=[]
   for j in range(len(labels)):
    val=K(sgn*int(i==j)+coef*int(N2[i,j]))+sum((cc*uu[i]*uu[j]for cc,uu in zip(cs,u)),K.zero);raw=c.ec(val);need(len(raw)<=1,'rational action shift');rr.append(F(raw[0])if raw else F(0))
   rows.append(rr)
  Ks.append(rows)
 K3,K4=Ks;lo=[[max(0,math.ceil(-x))for x in rr]for rr in K3];hi=[[math.floor(x)for x in rr]for rr in K4]
 need(all((K3[i][j]+K4[i][j]).denominator==1 for i in range(len(labels))for j in range(len(labels))),'integer sum action')
 tr1=sum((values[typ][1]for typ in types),K.zero);raw=c.ec(tr1);need(len(raw)<=1,'rational A1 trace');tr1=F(raw[0])if raw else F(0)
 return {'index':ix,'center_rank':len(labels),'labels':labels,'N2':[[int(x)for x in rr]for rr in N2.tolist()],'K3':[[str(x)for x in rr]for rr in K3],'K4':[[str(x)for x in rr]for rr in K4],'lower':lo,'upper':hi,'trace_A1':str(tr1),'diagonal_lower_sum':sum(lo[i][i]for i in range(len(labels))),'diagonal_upper_sum':sum(hi[i][i]for i in range(len(labels))),'empty_entry_domains':[[i,j]for i in range(len(labels))for j in range(len(labels))if lo[i][j]>hi[i][j]],'group':row['group'],'moments':{''.join(map(str,k)):v for k,v in moments.items()}}
if __name__=='__main__':
 rows=[build(ix)for ix in PATTERNS];print(json.dumps({'schema':'r1154-low-action-bounds/v1','results':rows,'source_sha256':{p.relative_to(ROOT).as_posix():digest(p)for p in [UP,HERE/'a2_action_probe.json',fiberpath]},'verifier_sha256':digest(Path(__file__))},indent=2))
