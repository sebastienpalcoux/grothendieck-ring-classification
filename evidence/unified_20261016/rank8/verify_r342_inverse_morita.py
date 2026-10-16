#!/usr/bin/env python3
"""Complete exact finite inputs to the R342 inverse-Morita obstruction.
Pure standard library; no optimization package, floating point, or assertions.
"""
import argparse,gzip,hashlib,itertools,json,math
from fractions import Fraction as Q
from pathlib import Path

def need(x,msg):
    if not x: raise ValueError(msg)
def flat(A):return tuple(x for row in A for x in row)
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def zero(n,m=None):return [[0]*(m or n) for _ in range(n)]
def tr(A):return [list(x) for x in zip(*A)]
def mm(A,B):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def linear(c,Ms):return [[sum(a*M[i][j] for a,M in zip(c,Ms)) for j in range(len(Ms[0][0]))] for i in range(len(Ms[0]))]
def rref(A,columns=None):
    A=[list(map(Q,row)) for row in A];n=len(A[0]) if columns is None else columns;piv=[];r=0
    for j in range(n):
        p=next((i for i in range(r,len(A)) if A[i][j]),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r];v=A[r][j];A[r]=[x/v for x in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][j]:
                v=A[i][j];A[i]=[x-v*y for x,y in zip(A[i],A[r])]
        piv.append(j);r+=1
        if r==len(A):break
    return A,piv

def rank(A):return len(rref(A)[1])
def inverse(A):
    n=len(A);R,p=rref([row+u for row,u in zip(A,eye(n))],n);need(p==list(range(n)),'invertible basis');return [row[n:] for row in R]
def affine_solutions(equations,n,bounds):
    R,piv=rref(equations,n);need(all(any(row[:n]) or not row[n] for row in R),'consistent affine space')
    free=[j for j in range(n) if j not in piv];out=[]
    for vals in itertools.product(*(range(bounds[j]+1) for j in free)):
        x=[Q(0)]*n
        for j,v in zip(free,vals):x[j]=Q(v)
        for i,j in enumerate(piv):x[j]=R[i][n]-sum(R[i][k]*x[k] for k in free)
        if all(v.denominator==1 and 0<=v<=bounds[j] for j,v in enumerate(x)):out.append(tuple(int(v) for v in x))
    return out,free

def polynomial(M,coeff):
    n=len(M);A=zero(n)
    for c in coeff:A=linear([1,c],[mm(A,M),eye(n)])
    return A

def anti_representations(R):
    f=[3,7];du=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    polynomials=[[1,-1],[1,-6,6,-4,8,16,0],[1,-6,6,-4,8,16,0],[1,-4,-8,16,16,0],[1,-6,0,6,-1],[1,0,-1],[1,-6,0,6,-1],[1,-6,-8,16,0]]
    sets=[]
    for i in range(8):
        need(polynomial(R[i],polynomials[i])==zero(8),'certified annihilator')
        pos=[(a,b) for a in range(2) for b in range(2) if i!=du[i] or a<=b];options=[]
        for vals in itertools.product(*(range(-R[i][f[a]][f[b]],R[i][f[a]][f[b]]+1,2) for a,b in pos)):
            M=zero(2)
            for (a,b),v in zip(pos,vals):
                M[a][b]=v
                if i==du[i]:M[b][a]=v
            if mm(M,tr(M))!=mm(tr(M),M):continue
            if polynomial(M,polynomials[i])!=zero(2):continue
            options.append(M)
        sets.append(options)
    seeds=[1,4,6];vectors=[eye(8)[0]];words=[()];a=0
    while len(vectors)<8 and a<len(vectors):
        for j in seeds:
            v=mm([vectors[a]],R[j])[0]
            if rank(vectors+[v])>len(vectors):vectors.append(v);words.append(words[a]+(j,))
            if len(vectors)==8:break
        a+=1
    need(len(vectors)==8,'three generators span source');I=inverse(vectors);reps=set();tuples=0
    for vals in itertools.product(*(sets[j] for j in seeds)):
        tuples+=1;given=dict(zip(seeds,vals))
        if any(mm(given[i],given[j])!=mm(given[j],given[i]) for i in seeds for j in seeds):continue
        images=[]
        for word in words:
            A=eye(2)
            for j in word:A=mm(A,given[j])
            images.append(A)
        T=[linear(row,images) for row in I]
        if any(T[i] not in sets[i] for i in range(8)):continue
        if any(tr(T[i])!=T[du[i]] for i in range(8)):continue
        if any(mm(T[i],T[j])!=linear(R[i][j],T) for i,j in itertools.product(range(8),repeat=2)):continue
        gauges=[tuple(tuple(int(signs[a]*signs[b]*M[a][b]) for a in range(2) for b in range(2)) for M in T) for signs in itertools.product([-1,1],repeat=2)]
        reps.add(min(gauges))
    need(tuples==8 and len(reps)==1,'complete signed module classification')
    return [[[v[2*a+b] for b in range(2)] for a in range(2)] for v in next(iter(reps))]

def module(R,T):
    labels=[(0,0),(1,0),(3,1),(3,-1),(4,0),(7,1),(7,-1)];F={3:0,7:1};out=[]
    for i in range(8):
        A=zero(7)
        for a,(x,sx) in enumerate(labels):
            for b,(y,sy) in enumerate(labels):
                if sx and sy:
                    n=R[i][x][y]+sx*sy*T[i][F[x]][F[y]];need(n>=0 and n%2==0,'split multiplicity');n//=2
                elif not sx and not sy:
                    xg=next(j for j,v in enumerate(R[x][5]) if v);n=R[i][x][y]+R[i][xg][y]
                else:n=R[i][x][y]
                A[a][b]=n
        out.append(A)
    need(out[0]==eye(7) and out[5]==eye(7),'module unit and involution action')
    for i,j in itertools.product(range(8),repeat=2):need(mm(out[i],out[j])==linear(R[i][j],out),'left module equations')
    return out

def dual_matrices(left):
    n=7;equations=[]
    for A in left:
        for i,j in itertools.product(range(n),repeat=2):
            row=[0]*49
            for k in range(n):row[k*n+j]+=A[i][k];row[i*n+k]-=A[k][j]
            if any(row):equations.append(row)
    RR,piv=rref(equations);equations=[row for row in RR if any(row)];need(len(piv)==38,'commutant dimension eleven')
    grams=[linear([A[a][a] for A in left],left) for a in range(n)]
    bounds=[math.isqrt(grams[j][i][i]) for i,j in itertools.product(range(n),repeat=2)];candidates=[]
    for j in range(n):
        eq=[row+[0] for row in equations]
        for i in range(n):eq.append([int(k==i*n) for k in range(49)]+[int(i==j)])
        vals,free=affine_solutions(eq,49,bounds);need(len(free)==4,'four free physical entries')
        candidates.append([[list(v[i*n:(i+1)*n]) for i in range(n)] for v in vals])
    need(list(map(len,candidates))==[2,4,2,2,2,2,2],'complete bounded commuting domains')
    units=[M for M in candidates[0] if M!=eye(n) and mm(M,M)==eye(n)];need(len(units)==1,'unique nontrivial invertible action');P=units[0]
    pairs=[]
    for j,cs in enumerate(candidates):
        seen=set();opts=[]
        for M in cs:
            Qm=mm(M,P);need(Qm in cs and Qm!=M,'free twin action')
            if flat(M) in seen:continue
            seen.update([flat(M),flat(Qm)]);opts.append((M,Qm))
        pairs.append(opts if j else [(eye(n),P)])
    need(list(map(len,pairs))==[1,2,1,1,1,1,1],'two joint candidate tuples')
    good=[]
    for choices in itertools.product(*pairs):
        mats=[M for pair in choices for M in pair]
        if all([[sum(M[b][a]*M[c][a] for M in mats) for c in range(n)] for b in range(n)]==grams[a] for a in range(n)):good.append(mats)
    need(len(good)==1,'unique simultaneous linking Gram solution')
    return good[0]

def fusion_from_matrices(M):
    n=14;du=[next(j for j,N in enumerate(M) if tr(A)==N) for A in M];base=[[M[j][a][b] for j in range(n)] for a,b in itertools.product(range(7),repeat=2)]
    base += [[int(i==j) for i in range(n)] for j in [0,1]]
    # Independent physical equations suffice; all solutions are checked against every equation.
    _,rowids=rref(tr(base));selected=[base[i] for i in rowids];need(len(rowids)==12,'rank twelve after unit reciprocity')
    choices={}
    for i,j in itertools.product(range(n),repeat=2):
        P=mm(M[i],M[j]);rhs=list(flat(P))+[int(j==du[i]),int(mm(M[j],M[1])==M[du[i]])]
        bounds=[P[k//2][0] for k in range(n)]
        eq=[base[a]+[rhs[a]] for a in rowids];sol,free=affine_solutions(eq,n,bounds)
        sol=[v for v in sol if all(sum(a*b for a,b in zip(row,v))==x for row,x in zip(base,rhs))]
        need(sol,'nonempty product domain');choices[i,j]=sol
    forced=[i for i in range(n) if all(len(choices[i,j])==1 for j in range(n))]
    need(forced==[0,1,4,5,6,7,10,11,12,13],'ten forced fusion matrices')
    N={i:[list(choices[i,j][0]) for j in range(n)] for i in forced};vectors=[eye(n)[0]];words=[()];at=0
    while len(vectors)<n and at<len(vectors):
        for i in forced:
            row=mm([vectors[at]],N[i])[0]
            if rank(vectors+[row])>len(vectors):vectors.append(row);words.append(words[at]+(i,))
            if len(vectors)==n:break
        at+=1
    need(len(vectors)==n,'forced products generate all fourteen classes');inv=inverse(vectors);images=[]
    for word in words:
        P=eye(n)
        for i in word:P=mm(P,N[i])
        images.append(P)
    R=[linear(row,images) for row in inv]
    need(all(tuple(R[i][j]) in choices[i,j] for i,j in itertools.product(range(n),repeat=2)),'reconstructed products in complete domains')
    R=[[[int(x) for x in row] for row in mat] for mat in R]
    for i,j in itertools.product(range(n),repeat=2):need(mm(R[i],R[j])==linear(R[j][i],R),'all dual associativity equations')
    return R,du,words

def neutral_checks(R,M):
    ids=[0,2,5,6,9,10,13];outside=[i for i in range(14) if i not in ids]
    need(all(R[i][j][k]==0 for i in ids for j in ids for k in outside),'rank seven neutral closure')
    need(all(R[i][j][k]==0 for i in ids for j in outside for k in ids),'odd bimodule closure')
    need(all(R[i][j][k]==0 for i in outside for j in outside for k in outside),'faithful C2 grading')
    need(all(sum(R[i][1])==1 and next(j for j,x in enumerate(R[i][1]) if x) in outside for i in ids),'odd invertible generates complement')
    need(all([M[i][a][0] for a in range(7)]==eye(7)[j] for j,i in enumerate(ids)),'module restricts to regular neutral module')
    conj=[]
    for i in ids:
        iu=next(j for j,x in enumerate(R[i][1]) if x);uiu=next(j for j,x in enumerate(R[1][iu]) if x);conj.append(ids.index(uiu))
    need(conj==[0,1,3,2,4,6,5],'odd conjugation is charge conjugation')
    Y=tr([[0,0,0,1,0,0,0],[0,1,1,1,1,1,0],[1,1,0,0,1,0,0],[0,1,1,0,0,0,1],[0,1,0,1,1,0,1],[0,0,1,0,1,0,0],[0,1,0,0,0,1,0]])
    f=[0,4,5,6,1,3,2];B=[[[R[i][j][k] for k in ids] for j in ids] for i in ids]
    need(all(Y[i][j]==B[f[2]][f[i]][f[j]] for i,j in itertools.product(range(7),repeat=2)),'BRW PSU3_5 fusion generator')
    powers=[];v=eye(7)[0]
    for _ in range(7):powers.append(v);v=mm([v],Y)[0]
    need(rank(powers)==7,'single PSU3_5 generator determines full tensor')
    # U(B)=1: every simple occurs in an adjoint product, checked by closure.
    dual=[next(j for j in range(7) if B[i][j][0]) for i in range(7)];seen={0}
    for i in range(7):seen.update(j for j,v in enumerate(B[i][dual[i]]) if v)
    while True:
        new=seen|{k for i in seen for j in seen for k,v in enumerate(B[i][j]) if v}
        if new==seen:break
        seen=new
    need(len(seen)==7,'trivial universal grading')
    autos=[]
    for tail in itertools.permutations(range(1,7)):
        p=(0,)+tail
        if all(B[i][j][k]==B[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(7),repeat=3)):autos.append(p)
    need(autos==[tuple(range(7)),tuple(conj)],'based automorphism group C2')
    return ids,f

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path);args=ap.parse_args()
    rows=[json.loads(line.replace('{','[').replace('}',']')) for line in gzip.open(args.repo/'supplements/rank8/data/rank8_tables.txt.gz','rt')]
    flatten=lambda R:tuple(x for A in R for row in A for x in row)
    rows=sorted((R for R in rows if max(flatten(R))==2),key=flatten);R=rows[341]
    digest=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    need(digest=='6d9246ba099d4676e98ae3cc60bba5a176db651fa740b5f8c4c5906ff652ae5d','source hash')
    T=anti_representations(R);left=module(R,T);M=dual_matrices(left);dual,du,words=fusion_from_matrices(M);ids,f=neutral_checks(dual,M)
    out={'status':'PASS','case':'R8_2_342','source_sha256':digest,'anti_representations_up_to_gauge':1,'joint_right_action_solutions':1,'dual_rank':14,'neutral_rank':7,'neutral_labels':ids,'BRW_to_neutral_map':f,'forced_generator_words':words,'all_dual_associativity_checks':14**4,'neutral_based_aut_group':'C2','neutral_universal_grading':'trivial','dual_tensor':dual,'right_matrices':M,'left_matrices':left}
    if args.output:args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['dual_tensor','right_matrices','left_matrices']},indent=2))
if __name__=='__main__':main()
