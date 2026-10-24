#!/usr/bin/env python3
"""Exact necessary-data tests for the GH(C6,m=2) / R1768 route.

This certifies based actions, never associators or categorical existence.
"""
import hashlib,itertools,json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=Path('/workspace/scratch/90f37cc83103/online_revision/grothendieck-ring-classification')

def need(ok,why):
    if not ok:raise ValueError(why)
def data(M):return [[int(x)for x in row]for row in M.tolist()]

def run():
    path=HERE.parent/'inputs/R8_3_1768.json'
    source=json.loads(path.read_text());R=source['fusion_tensor']
    digest=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    need(digest=='240509807c67da437c86f2a51efeb831364734feb93ed18a1d2f32087ebc1af0','canonical R1768 tensor')
    Ns=[s.Matrix(8,8,lambda k,j:R[i][j][k])for i in range(8)]
    prior_path=ROOT/'evidence/rank8_next_20261021/quadratic/profile_closure.json'
    prior=json.loads(prior_path.read_text())['R8_3_1768']['surviving_factors']
    f=next(f for f in prior if f['candidate_index']==7)
    B=s.Matrix(f['B'])
    need(B[0,:]==s.Matrix([[1,0,0,1,0,0,0,0]]),'algebra object 1+X3')
    need(B.T*B==Ns[0]+Ns[3],'induction Gram')
    need(B.rank()==5 and len(B.tolist())==8,'rank-eight induction factor of rank five')
    U=s.zeros(8,3)
    for a,(i,j)in enumerate([(1,2),(3,4),(5,6)]):U[i,a]=1;U[j,a]=-1
    need(B.T*U==s.zeros(8,3)and U.T*U==2*s.eye(3),'complete rational kernel')
    Bp=B.pinv();A=[B*N*Bp for N in Ns]
    for i in range(8):
        need(A[i].T==A[i]and A[i]*B==B*Ns[i]and A[i]*U==s.zeros(8,3),'determined image action')
    G=s.Matrix([[0,1,0],[1,0,0],[0,0,-1]])
    gperm=[7,3,4,1,2,6,5,0]
    need(A[1]+U*G*U.T/2==s.eye(8)[:,gperm],'fixed free pointed action')
    chars=[[1,-1,1,-1,0,0,1,-1],[1,-1,0,1,1,-1,-1,0],
           [1,-1,0,1,-2,2,-1,0],[1,1,0,1,-1,-1,1,0],
           [1,1,1,-1,0,0,-1,1],[1,-1,-2,-1,0,0,1,2]]
    irr=[[1,1,5+eps*s.sqrt(37),6+eps*s.sqrt(37),7+eps*s.sqrt(37),7+eps*s.sqrt(37),6+eps*s.sqrt(37),5+eps*s.sqrt(37)]for eps in [-1,1]]
    for c in chars+irr:
        need(all(s.simplify(c[i]*c[j]-sum(R[i][j][k]*c[k]for k in range(8)))==0 for i,j in itertools.product(range(8),repeat=2)),'exact source character')
    need(s.Matrix(chars+irr).det()!=0,'all eight source characters')
    def possible(i):
        bound=max(abs(c[i])for c in chars);vals=[];domains=[]
        for r,t in [(1,1),(1,3),(1,5),(5,5)]:
            lo=max(0,int(s.ceiling(A[i][r,t]-s.Rational(bound,2))))
            hi=int(s.floor(A[i][r,t]+s.Rational(bound,2)))
            domains.append([2*(n-A[i][r,t])for n in range(lo,hi+1)])
        for a,b,c,d in itertools.product(*domains):
            H=s.Matrix([[a,b,c],[b,a,-c],[c,-c,d]])
            T=A[i]+U*H*U.T/2
            if not all(x.is_Integer and x>=0 for x in T):continue
            prod=s.eye(3)
            for q in sorted(set(c[i]for c in chars)):prod=prod*(H-q*s.eye(3))
            if prod!=s.zeros(3):continue
            vals.append(H)
        return vals
    opts={i:possible(i)for i in [2,3,4]}
    need({i:len(v)for i,v in opts.items()}=={2:2,3:4,4:4},'complete bounded kernel matrices')
    completions=[]
    for h2,h3,h4 in itertools.product(*(opts[i]for i in [2,3,4])):
        Hs=[s.eye(3),G,h2,h3,h4,G*h4,G*h3,G*h2]
        if any(Hs[i]*Hs[j]!=Hs[j]*Hs[i]for i in [2,3,4]for j in [2,3,4]):continue
        if any(Hs[i]*Hs[j]!=sum((R[i][j][k]*Hs[k]for k in range(8)),s.zeros(3))for i,j in itertools.product(range(8),repeat=2)):continue
        Ts=[A[i]+U*Hs[i]*U.T/2 for i in range(8)]
        need(all(all(t.is_Integer and t>=0 for t in T)and T.T==T for T in Ts),'nonnegative integral selfdual actions')
        need(all(Ts[i]*Ts[j]==sum((R[i][j][k]*Ts[k]for k in range(8)),s.zeros(8))for i,j in itertools.product(range(8),repeat=2)),'all64 R1768 module products')
        completions.append(Ts)
    need(len(completions)==2,'exactly two action completions with fixed g permutation')
    p=[3,4,7,2,0,6,5,1];P=s.eye(8)[:,p]
    need(P**6==s.eye(8)and P**3==s.eye(8)[:,gperm],'C6 generator cube is source g')
    cycle=[0]
    for k in range(1,6):cycle.append(p[cycle[-1]])
    need(len(set(cycle))==6 and set(cycle)=={0,1,2,3,4,7},'six-object regular orbit')
    need(p[5]==6 and p[6]==5,'two-object parity orbit')
    exhaustive=[]
    small=[0,1,2,3,4,7]
    for index,Ts in enumerate(completions):
        pp=[]
        for images in itertools.permutations(small):
            trial=[None]*8
            for i,j in zip(small,images):trial[i]=j
            trial[5]=6;trial[6]=5
            orbit=[0]
            for k in range(1,6):orbit.append(trial[orbit[-1]])
            if len(set(orbit))!=6 or trial[orbit[-1]]!=0:continue
            Qp=s.eye(8)[:,trial]
            if all(Qp*T==T*Qp for T in Ts):pp.append(trial)
        need(pp==[p,[4,7,3,0,1,6,5,2]],'exhaustive compatible C6 generators, inverse pair')
        exhaustive.append({'completion':index,'all_C6_generators':pp})
    bimodules=[]
    for index,Ts in enumerate(completions):
        for sign in [-1,1]:
            Q=s.zeros(8)
            for k,i in enumerate(cycle):Q[cycle[-k%6],i]=1
            for i in cycle:
                for j in [5,6]:Q[i,j]=Q[j,i]=1
            Q[5,5]=Q[6,6]=(11+sign)//2;Q[5,6]=Q[6,5]=(11-sign)//2
            L=[P**i for i in range(6)]+[P**i*Q for i in range(6)]
            need(Q.T==Q and Q*P==P**5*Q,'GH duality and inversion action')
            need(Q**2==s.eye(8)+2*sum(L[6:],s.zeros(8)),'GH multiplicity-two quadratic relation')
            need(all(M*N==N*M for M in L for N in Ts),'all96 commuting actions')
            bimodules.append({'R1768_completion':index,'rho_kernel_sign':sign,'GH_generator':p,'GH_rho':data(Q)})
    root=s.sqrt(37);u=6+root;D=444+72*root
    need(s.simplify(u*u-12*u-1)==0 and s.simplify(6*(1+u*u)-D)==0,'GH and R1768 global dimensions')
    need(s.simplify((u-1)**2*(u+1)/4-(3+33*u))==0,'two large internal-end dimensions')
    return {'status':'PASS','scope':'Necessary based-module and commuting-action data only; no category, separable algebra, or Morita equivalence is constructed.',
            'id':'R8_3_1768','tensor_sha256':digest,
            'prior_profile_closure_sha256':hashlib.sha256(prior_path.read_bytes()).hexdigest(),
            'candidate_index':7,'factor_index':f['factor_index'],'algebra_object':[1,0,0,1,0,0,0,0],
            'induction_factor':data(B),'module_rank':8,'kernel_rank':3,
            'independent_kernel_candidates':{str(i):len(v)for i,v in opts.items()},
            'complete_actions':[list(map(data,Ts))for Ts in completions],
            'commuting_GH_actions':bimodules,'exhaustive_generators':exhaustive,
            'marked_commuting_action_pairs':8,'pairs_modulo_C6_generator_inversion':4,
            'conditional_pointed_class':'An actual GH(C6,2) -> R1768 Morita realization with these actions requires class3 in H3(C6,C*)=Z/6.',
            'categorification_status':'unresolved'}

if __name__=='__main__':
    result=run();target=HERE/'gh6_route_verified.json';target.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: two rank8 action completions; four commuting GH(C6,2) action pairs; categorical existence unresolved.')
