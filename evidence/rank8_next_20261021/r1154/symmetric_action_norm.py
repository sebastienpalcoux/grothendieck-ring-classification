"""Exact Frobenius rounding bound for symmetric bounded N1 extensions."""
import sys,json,math,itertools,time
from pathlib import Path
from fractions import Fraction as F
UP=Path(__file__).resolve().with_name('joint_triple_after_a2.py');exec(compile(UP.read_text().split('def main():')[0],str(UP),'exec'))
BOUNDS=HERE/'low_action_bounds.json';bounds=json.load(open(BOUNDS));byix={r['index']:r for r in bounds['results']}
need(bounds['verifier_sha256']==digest(HERE/'low_action_bounds.py'),'bounds binding')
L=s.Matrix(8,8,lambda k,j:sum(cols[1][i]*R[i][j][k]for i in range(8)));need(L.T==L,'symmetric source action')
out=[];start=time.monotonic()
for pr in fibers['results']:
 ix=pr['index']
 if ix not in byix:continue
 b=byix[ix];counts=domain['completions'][ix];ns=[1]+counts;sig=tuple(sum(n*v[1]for n,v in zip(ns,co))//den for co,den in moment_coefficients.values());inds,C,aa,hh,mom=augmented(sig)
 fullnorm=sum((K(n)*v[1]**2 for n,v in zip([1]*5+counts,values)),K.zero);fulltrace=sum((K(n)*v[1]for n,v in zip([1]*5+counts,values)),K.zero);fullnorm=F(c.ec(fullnorm)[0]);fulltrace=F(c.ec(fulltrace)[0])
 for number,hist in enumerate(pr['pair11_histogram_solutions_by_high_type']):
  labels=[];Mcols=[];Acols=[];mapold=[]
  for j in range(5):
   labels.append({'low':j});Mcols.append(cols[j]);Acols.append([int(j==1)]+[mom[tuple(sorted((1,k,j)))]if j else int(k==1)for k in range(1,5)]);mapold.append(j)
  for typ,his in enumerate(hist):
   for x,n in his:
    if not n:continue
    row,bs,q,vs=row_data(pr['group'],typ,x,sig);pp=[0]+[int(row[5+pairs.index((1,k))])for k in range(1,5)]
    old=next(i for i,z in enumerate(b['labels'])if z.get('type')==typ)
    for _ in range(n):labels.append({'type':typ,'pair11':x});Mcols.append((0,)+tuple(domain['high_columns'][typ]));Acols.append(pp);mapold.append(old)
  M=s.Matrix(Mcols).T;n=M.cols;W=s.eye(n)[:,:5].row_join(M.T);Y=s.Matrix(Acols).row_join(M.T*L);pivs=list(W.rref()[1]);need(len(pivs)==8,'known source/low domain rank eight');W=W[:,pivs];Y=Y[:,pivs];G=W.T*W;Gi=G.inv();P=W*Gi*W.T;Z=Y*Gi*W.T;F0=Z+Z.T-P*Z;need(F0.T==F0 and F0*W==Y,'minimum norm symmetric action extension')
  beta=fullnorm-F(s.trace(F0*F0));need(beta>=0,'symmetric extension norm residual');minimum=F(0);why=None
  for i in range(n):
   for j in range(i,n):
    k3=F(b['K3'][mapold[i]][mapold[j]]);k4=F(b['K4'][mapold[i]][mapold[j]])
    if i!=j and mapold[i]==mapold[j]:
     # Copies have identical spectral rows, but identity/projector diagonal
     # terms must be removed when converting a stored diagonal to off-diagonal.
     k3+=2 if labels[i].get('type')==10 else -1
     k4+=-1 if labels[i].get('type')==10 else 1
    lo=max(0,math.ceil(-k3));hi=math.floor(k4)
    if i<5:lo=hi=int(Acols[j][i])
    f=F(F0[i,j]);nearest=max(lo,min(hi,f.numerator//f.denominator));cost=min((F(k)-f)**2 for k in set([nearest,max(lo,min(hi,nearest+1))]));minimum+=(1 if i==j else 2)*cost
  if minimum>beta:why='integer_rounding_norm'
  out.append({'index':ix,'pair_histogram':number,'minimum_norm_extension_trace':str(s.trace(F0)),'required_residual_trace':str(fulltrace-F(s.trace(F0))),'residual_squared_norm':str(beta),'minimum_integer_squared_norm':str(minimum),'status':'excluded'if why else 'passes','reason':why})
  print(json.dumps({'index':ix,'pair_histogram':number,'minimum':str(minimum),'beta':str(beta),'status':out[-1]['status'],'seconds':round(time.monotonic()-start,2)}),file=sys.stderr,flush=True)
print(json.dumps({'schema':'r1154-symmetric-action-norm/v1','scope':'Necessary full symmetric bounded N1 rounding inequality; no model assertion','results':out,'source_sha256':{p.relative_to(ROOT).as_posix():digest(p)for p in [UP,BOUNDS,fiberpath]},'verifier_sha256':digest(Path(__file__))},indent=2))
