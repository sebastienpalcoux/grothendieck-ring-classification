"""Exact finite modular central-projection test on completed quartic centers.

Each column is exhaustively enumerated from twist and forgetful compatibility.
The complete rectangular S intertwining equations are solved over Q; surviving
integral matrices are checked directly. This does not construct a category.
"""
import argparse,hashlib,itertools,json,sys,time
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
from exact import require
from round5_modular_checks import centers
from round5_quartic_pair import digest


def source(rid,R,data,label,W,ds,ee):
 C=data['C'];F=data['F']
 if rid=='R6_4_22':
  g=next(i for i in range(1,6)if R[i][i][0]==1 and sum(R[i][i])==1)
  nu2=sum((d*C(v[g])*C.unit**(2*e)for d,v,e in zip(ds,W,ee)),C.zero)/data['DD'];require(nu2==C.one,'pointed subcategory requires trivial associator sign')
  labels=list(itertools.product(range(2),repeat=2));S=[[C(s.Rational((-1)**(a*l+b*k),2))for b,l in labels]for a,k in labels];theta=[C((-1)**(a*k))for a,k in labels];P=[[int(a==i)for a,k in labels]for i in range(2)]
  return [0,g],labels,S,theta,P,dict(kind='Z(Vec_C2)',second_indicator=1)
 g,ss=4,3;inds=[0,g,ss];q=data['dims'][ss];SI=[[C.one,C.one,q],[C.one,C.one,-q],[q,-q,C.zero]];SI=[[z/C(2)for z in row]for row in SI];eeI=[0,8,label['ising_twist_exponent']];labels=list(itertools.product(range(3),repeat=2));S=[[SI[a][c]*SI[b][d]for c,d in labels]for a,b in labels];theta=[C.unit**((eeI[a]-eeI[b])%F)for a,b in labels];P=[[R[inds[a]][inds[b]][i]for a,b in labels]for i in inds]
 require(all(sum(R[inds[a]][inds[b]][i]for i in range(6)if i not in inds)==0 for a,b in labels),'Ising subring not closed')
 nu2=sum((d*C(v[ss])*C.unit**(2*e)for d,v,e in zip(ds,W,ee)),C.zero)/data['DD'];require(nu2==-C.one,'Ising associator sign')
 return inds,labels,S,theta,P,dict(kind='Ising_times_reverse_Ising',ising_twist_exponent=label['ising_twist_exponent'],second_indicator=-1)


def check(rid,R,data,label,W,ds,S,ee):
 C=data['C'];F=data['F'];r=len(S);inds,labels,SD,TD,P,metadata=source(rid,R,data,label,W,ds,ee);m=len(SD);theta=[C.unit**e for e in ee];options=[]
 require(W[0]==[1,0,0,0,0,0] and ds[0]==C.one,'ambient unit index')
 for j,v in enumerate(W):
  target=[v[i]for i in inds];allowed=[a for a in range(m)if TD[a]==theta[j]];bounds=[min(target[i]//P[i][a]for i in range(len(inds))if P[i][a])for a in allowed];choices=[]
  for values in itertools.product(*(range(b+1)for b in bounds)):
   w=[0]*m
   for a,z in zip(allowed,values):w[a]=z
   if all(sum(P[i][a]*w[a]for a in range(m))==target[i]for i in range(len(inds)))and(j!=0 or w==[1]+[0]*(m-1)):choices.append(w)
  require(choices,'no individual central-projection column');options.append(choices)
 base=[[options[j][0][a]for j in range(r)]for a in range(m)];directions=[];bounds=[]
 for j,opts in enumerate(options):
  if len(opts)==1:continue
  delta=[opts[1][a]-opts[0][a]for a in range(m)];require(opts==[[opts[0][a]+k*delta[a]for a in range(m)]for k in range(len(opts))],'column domain not an integer segment');directions.append((j,delta));bounds.append(len(opts)-1)
 degree=C.mod.degree();equations=set();nv=len(directions)
 def coeff(z):return [s.Rational(0)]*(degree-len(z.to_list()))+[s.Rational(v)for v in z.to_list()]
 for a in range(m):
  for j in range(r):
   rhs=sum((C(base[a][k])*S[k][j]for k in range(r)),C.zero)-sum((SD[a][b]*C(base[b][j])for b in range(m)),C.zero)
   terms=[(sum((SD[a][b]*C(delta[b])for b in range(m)),C.zero)if k==j else C.zero)-C(delta[a])*S[k][j]for k,delta in directions]
   vv=[coeff(z)for z in terms+[rhs]]
   for d in range(degree):
    row=tuple(v[d]for v in vv)
    if any(row):equations.add(row)
 A=s.Matrix(sorted(equations));rr,piv=A.rref();consistent=nv not in piv;solutions=[];free=[j for j in range(nv)if j not in piv]
 if consistent:
  for vals in itertools.product(*(range(bounds[j]+1)for j in free)):
   x=[s.Integer(0)]*nv
   for j,v in zip(free,vals):x[j]=s.Integer(v)
   for i,j in enumerate(piv):x[j]=rr[i,nv]-sum(rr[i,k]*x[k]for k in free)
   if any(v.q!=1 or v<0 or v>bounds[j]for j,v in enumerate(x)):continue
   B=[list(row)for row in base]
   for v,(j,delta)in zip(x,directions):
    for a in range(m):B[a][j]+=int(v)*delta[a]
   require(all(sum((SD[a][b]*C(B[b][j])for b in range(m)),C.zero)==sum((C(B[a][k])*S[k][j]for k in range(r)),C.zero)for a in range(m)for j in range(r)),'full S intertwiner')
   require(all(C(B[a][j])*TD[a]==C(B[a][j])*theta[j]for a in range(m)for j in range(r)),'full T intertwiner')
   require(all(all(sum(P[i][a]*B[a][j]for a in range(m))==W[j][b]for i,b in enumerate(inds))for j in range(r)),'forgetful projection')
   require([row[0]for row in B]==[1]+[0]*(m-1),'projection of unit')
   solutions.append(B)
 return dict(label=label,source=metadata,source_labels=[list(x)for x in labels],column_choice_counts=[len(v)for v in options],variables=nv,variable_bounds=bounds,rational_equations=A.rows,rational_rank=len(piv),rationally_consistent=consistent,free_variables=free,integral_solutions=len(solutions),projection_matrices=solutions,S_equations=m*r,T_equations=m*r,forgetful_equations=len(inds)*r,excluded=not solutions)


def reconstruct():
 results=[]
 for rid in ['R6_4_22','R6_4_91']:
  R=next(x['N']for x in json.load(open(ROOT/'data/census.json'))if x['id']==rid);cert=json.load(open(ROOT/f'research/round5/quartic_pair/{rid}_center_reconstruction.json'))['certificate'];variants=[]
  for data,label,W,ds,S,ee in centers(rid,cert,R):
   out=check(rid,R,data,label,W,ds,S,ee);variants.append(out);print(rid,label,'variables',out['variables'],'rank',out['rational_rank'],'solutions',out['integral_solutions'],flush=True)
  results.append(dict(id=rid,source_sha256=digest(cert),variants=variants,all_variants_excluded=all(x['excluded']for x in variants)))
 return dict(optimizer_used=False,categorification_claimed=False,complete_finite_projection_test=True,results=results)


if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--verify',action='store_true');ap.add_argument('--output',type=Path,default=Path(__file__).with_suffix('.json'));a=ap.parse_args()
 import scipy.optimize
 def denied(*_,**__):raise RuntimeError('numerical optimizer disabled')
 scipy.optimize.linprog=scipy.optimize.milp=denied
 start=time.monotonic();out=reconstruct()
 if a.verify:require(out==json.loads(a.output.read_text()),'central projection record differs')
 else:a.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(dict(passed=True,optimizer_used=False,seconds=time.monotonic()-start)),flush=True)
