"""Fusion tables of the ten published multiplicity-one unitary models."""
import itertools
from rings import *

def su2(level,labels):
    return [[[int(c in range(abs(a-b),min(a+b,2*level-a-b)+1,2)) for c in labels] for b in labels] for a in labels]

def ty(cyclic):
    R=[[[0]*5 for _ in range(5)] for _ in range(5)]
    for i,j in itertools.product(range(4),repeat=2):R[i][j][(i+j)%4 if cyclic else i^j]=1
    for i in range(4):R[i][4][4]=R[4][i][4]=R[4][4][i]=1
    return R

def group_characters(T,sizes,order):
    require(sum(sizes)==order,'character-table conjugacy class sizes')
    out=[]
    for i in range(len(T)):
        mat=[]
        for j in range(len(T)):
            row=[]
            for k in range(len(T)):
                x=s.simplify(sum(w*T[i][c]*T[j][c]*s.conjugate(T[k][c]) for c,w in enumerate(sizes))/order)
                require(x.is_Integer and x>=0,'nonintegral or negative character product')
                row.append(int(x))
            mat.append(row)
        out.append(mat)
    return out

def dihedral14():
    R=[[[0]*5 for _ in range(5)] for _ in range(5)]
    for i in range(5):R[0][i][i]=R[i][0][i]=1
    R[1][1][0]=1
    for i in range(2,5):R[1][i][i]=R[i][1][i]=1
    for a,b in itertools.product(range(1,4),repeat=2):
        for c in (a+b,a-b):
            c%=7;c=min(c,7-c)
            if c==0:R[a+1][b+1][0]+=1;R[a+1][b+1][1]+=1
            else:R[a+1][b+1][c+1]+=1
    return R

def multiplicity_one_models():
    # The two non-self-dual tables below are transcribed from [LPR],
    # Section 3.5, entries 7 and 11; their unitary solutions are in 4.2/4.4.
    z12=[[[int(i==j) for j in range(5)] for i in range(5)],
      [[0,1,0,0,0],[1,0,0,0,0],[0,0,0,1,0],[0,0,1,0,0],[0,0,0,0,1]],
      [[0,0,1,0,0],[0,0,0,1,0],[0,1,0,0,1],[1,0,0,0,1],[0,0,1,1,0]],
      [[0,0,0,1,0],[0,0,1,0,0],[1,0,0,0,1],[0,1,0,0,1],[0,0,1,1,0]],
      [[0,0,0,0,1],[0,0,0,0,1],[0,0,1,1,0],[0,0,1,1,0],[1,1,0,0,1]]]
    z24=[[[int(i==j) for j in range(5)] for i in range(5)],
      [[0,1,0,0,0],[1,0,0,0,0],[0,0,1,0,0],[0,0,0,0,1],[0,0,0,1,0]],
      [[0,0,1,0,0],[0,0,1,0,0],[1,1,1,0,0],[0,0,0,1,1],[0,0,0,1,1]],
      [[0,0,0,1,0],[0,0,0,0,1],[0,0,0,1,1],[0,1,1,1,1],[1,0,1,1,1]],
      [[0,0,0,0,1],[0,0,0,1,0],[0,0,0,1,1],[1,0,1,1,1],[0,1,1,1,1]]]
    S4=group_characters([[1,1,1,1,1],[1,-1,1,1,-1],[2,0,2,-1,0],[3,1,-1,0,-1],[3,-1,-1,0,1]],[1,6,3,8,6],24)
    return {'Vec(C5)':[[[int((i+j)%5==k) for k in range(5)] for j in range(5)] for i in range(5)],
       'TY(C4)':ty(True),'TY(C2xC2)':ty(False),'SU(2)_4':su2(4,list(range(5))),
       'Rep(D14)':dihedral14(),'Rep(S4)':S4,'PSU(2)_8':su2(8,[0,2,4,6,8]),
       'PSU(2)_9':su2(9,[0,2,4,6,8]),'LPR-12':z12,'LPR-24':z24}

def match_models(rows):
    out=[]
    for name,R in multiplicity_one_models().items():
        validate(R)
        found=[]
        for row in rows:
            if row['m']!=1:continue
            for pp in itertools.permutations(range(1,5)):
                p=(0,)+pp
                if permute(R,p)==row['N']:found.append((row,p));break
        require(len(found)==1,'model match not unique: '+name)
        row,p=found[0];out.append({'m':1,'j':row['j'],'name':name,'basis':p,'model_tensor':R})
    require(len({a['j'] for a in out})==10,'duplicate models')
    return sorted(out,key=lambda a:a['j'])
