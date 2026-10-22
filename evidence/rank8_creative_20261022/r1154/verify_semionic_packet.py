#!/usr/bin/env python3
"""Exact four-object semionic packet reconstruction for R8_3_1154.

This is a necessary center-data theorem, not a categorification or exclusion.
"""
from pathlib import Path
from fractions import Fraction
import hashlib,inspect,json,sys
ROOT=Path(__file__).resolve().parents[3]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'evidence/rank8_next_20261021/r1154'))
import low_action_bounds as l
s=l.s

def need(ok,message):
 if not ok:raise ValueError(message)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def matrix(M):return [[str(s.simplify(x))for x in row]for row in M.tolist()]

# The upstream reconstruction is reused without changing its frozen source.
source=inspect.getsource(l.build).replace('def build(ix):','def build_at(ix,pno):').replace("['pair11_histogram_solutions_by_high_type'][0]","['pair11_histogram_solutions_by_high_type'][pno]")
env=dict(vars(l));exec(source,env);build_at=env['build_at']

def packet_options():
 I=s.I;u=s.Matrix([1,1,1,1])/2;v=s.Matrix([1,1,-1,-1])/2
 E=s.Matrix([[1,0],[-1,0],[0,1],[0,-1]])/s.sqrt(2)
 Ts=s.diag(I,-I)
 options=[('diagonal',s.diag(I,-I)),('mixed_plus',I*s.Matrix([[-1,s.sqrt(3)],[s.sqrt(3),1]])/2),('mixed_minus',I*s.Matrix([[-1,-s.sqrt(3)],[-s.sqrt(3),1]])/2)]
 out=[]
 for name,A in options:
  need(s.simplify(A.T-A)==s.zeros(2),'symmetric residual S block')
  need(s.simplify(A*s.conjugate(A.T))==s.eye(2),'unitary residual S block')
  need(A*A==-s.eye(2),'dual pairs necessarily exchanged')
  need(s.simplify(A*Ts*A-Ts.inv()*A*Ts.inv())==s.zeros(2),'exact residual STS relation')
  B=s.simplify(-v*v.T+E*A*E.T)
  C=s.Matrix([[s.Rational(sign,4)]*4 for sign in [1,1,-1,-1]]).col_join(B)
  need(s.simplify(s.conjugate(C.T)*C)==s.eye(4),'four full S columns are orthonormal')
  delta=s.simplify(C*s.diag(*(4*(B[0,j]-B[1,j])for j in range(4)))*s.conjugate(C.T))
  obstruction=s.simplify(delta[6,7])
  if name=='diagonal':need(obstruction==0,'diagonal packet passes this entry')
  else:need(obstruction in [s.sqrt(3),-s.sqrt(3)],'mixed packet violates Verlinde integrality')
  out.append({'name':name,'residual_S':matrix(A),'packet_S':matrix(B),'fusion_difference_entry':str(obstruction),'status':'retained'if name=='diagonal'else'excluded_nonintegral_fusion_difference'})
 return out,u,v,E

def check_branch(ix,pno,u,v,E):
 b=build_at(ix,pno);labels=b['labels'];n=len(labels);at=[i for i,q in enumerate(labels)if q.get('type')==10]
 need(len(at)==4,'exact four-object packet')
 M=s.Matrix([l.cols[q['low']]if 'low'in q else (0,)+tuple(l.domain['high_columns'][q['type']])for q in labels]).T
 need(list(M[3,:])==[int(i in at)for i in range(n)],'I(g) is exactly the four packet objects')
 delta=l.a['D']/l.K(4)
 for i in at:
  d=sum((l.K(int(M[j,i]))*l.a['ds'][j]for j in range(8)),l.K.zero)
  need(d==delta,'packet dimensions D/4')
 N2=s.Matrix(b['N2']);In=s.eye(n)
 P=N2*(N2-3*In)*(N2+5*In)*(N2*N2-270*N2+225*In)/s.Integer(7936)
 w=s.zeros(n,1)
 for i,z in enumerate([1,1,-1,-1]):w[i]=s.Rational(z,2)
 Jz=s.zeros(n);uz=s.zeros(n,1)
 for i in at:Jz[i,i]=1;uz[i]=s.Rational(1,2)
 need(P==w*w.T+Jz-uz*uz.T,'forced A2 minus-one projector decomposition')
 need(P*P==P and s.trace(P)==4,'projector rank four')
 B=s.simplify(-v*v.T+E*s.diag(s.I,-s.I)*E.T);C=s.zeros(n,4)
 for j in range(4):
  C[:,j]=w/2
  for k,i in enumerate(at):C[i,j]=B[k,j]
 need(s.simplify(s.conjugate(C.T)*C)==s.eye(4),'orthonormal packet S columns')
 Ng=s.Matrix(8,8,lambda k,j:l.R[3][j][k]);J=M.T*Ng*M
 Dp=s.simplify(C*s.diag(*(4*(B[0,j]-B[1,j])for j in range(4)))*s.conjugate(C.T))
 Dm=s.simplify(C*s.diag(*(4*(B[2,j]-B[3,j])for j in range(4)))*s.conjugate(C.T))
 H=s.simplify(C*s.diag(-4,-4,4,4)*s.conjugate(C.T))
 # Row-input convention for N_Z; its column at the vacuum is e_(Z*).
 Ns=[(J+H+2*Dp)/4,(J+H-2*Dp)/4,(J-H+2*Dm)/4,(J-H-2*Dm)/4]
 dual=[1,0,3,2]
 for a,N in enumerate(Ns):
  need(all(x.is_Integer and x>=0 for x in N),'nonnegative integral packet fusion matrix')
  need(list(N[0,:])==[int(i==at[a])for i in range(n)],'fusion unit row')
  need(N.T==Ns[dual[a]],'fusion duality transpose')
  need(all(N*Q==Q*N for Q in Ns),'packet matrices commute')
  need(N*N2==N2*N,'packet matrices commute with forced A2')
 need(sum(Ns,s.zeros(n))==J,'induced object fusion action')
 return {'pattern':ix,'pair_histogram':pno,'center_rank':n,'packet_indices':at,'status':'PASS','packet_fusion_matrices':[[list(map(int,row))for row in N.tolist()]for N in Ns]}

def main():
 options,u,v,E=packet_options();path=ROOT/'evidence/rank8_research_20261022/r1154_r1795/galois_fixed_review.json';old=json.loads(path.read_text())
 rows=[check_branch(r['index'],r['histogram_solution'],u,v,E)for r in old['results']if r.get('witness')]
 need(len(rows)==25 and {r['pattern']for r in rows}=={6971,8766,8772},'complete current pair domain')
 sources=[path,Path(l.__file__),ROOT/'evidence/rank8_next_20261021/models/NEW_CONSTRUCTION_ATTEMPTS.md',ROOT/'evidence/rank8_next_20261021/models/rank5_dual_exclusions.json',ROOT/'evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json']
 result={'schema':'r1154-semionic-packet-reconstruction/v1','status':'PASS','scope':'Necessary center packet structure. All three center patterns and all 25 pair histograms remain; no categorification or source-ring exclusion.','packet_twists':['i','i','-i','-i'],'packet_duality':[1,0,3,2],'classification':options,'complete_pair_domain':25,'remaining_patterns':[6971,8766,8772],'results':rows,'source_sha256':{p.relative_to(ROOT).as_posix():sha(p)for p in sources},'verifier_sha256':sha(Path(__file__))}
 Path(__file__).with_name('semionic_packet.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k not in('results','classification')},indent=2))
if __name__=='__main__':main()
