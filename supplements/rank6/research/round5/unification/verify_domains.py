"""Independent small-domain exhaustive controls for unified Gram enumeration."""
from pathlib import Path
import hashlib
import itertools
import json
import math
import random
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'software'))
from sympy import Matrix
from round5_unified import enumerate_gram_ellipsoid, enumerate_fixed_gram_block


def require(condition,message):
    if not condition:
        raise ValueError(message)


def exhaustive(H,prefix=()):
    _,p=H.rref()
    P=list(p)
    inverse=H[P,P].inv() if P else None
    out=[]
    for suffix in itertools.product(*(range(math.isqrt(int(H[i,i]))+1)
                                      for i in range(len(prefix),H.rows))):
        z=Matrix(list(prefix)+list(suffix))
        if H.row_join(z).rank()!=H.rank():
            continue
        if P and (z[P,:].T*inverse*z[P,:])[0]>1:
            continue
        if all(z[i]*z[j]<=H[i,j] for i in range(H.rows) for j in range(H.rows)):
            out.append(list(suffix))
    return sorted(out)


def main():
    random.seed(7)
    grams=[Matrix(x) for x in [[[2,1],[1,1]],[[2,2],[2,2]],
           [[0,0],[0,3]],[[4,2,0],[2,2,1],[0,1,2]],[[0,0],[0,0]]]]
    for _ in range(15):
        B=Matrix([[random.randrange(3) for _ in range(3)] for _ in range(3)])
        grams.append(B*B.T)
    ordinary=[]
    for G in grams:
        expected=exhaustive(G)
        actual=enumerate_gram_ellipsoid(G.tolist(),time_limit=15)
        require(actual['complete'],'unfinished small control')
        require(actual['candidates']==expected,'ellipsoid differs from exhaustive box')
        ordinary.append(dict(gram=G.tolist(),rank=int(G.rank()),candidates=len(expected)))
    random.seed(11)
    joint=[]
    for test in range(20):
        V=Matrix([[random.randrange(3) for _ in range(4)] for _ in range(2)])
        X=Matrix([[random.randrange(3) for _ in range(4)] for _ in range(3)])
        Q,B,G=V*V.T,X*V.T,X*X.T
        H=Q.row_join(B.T).col_join(B.row_join(G))
        v=list(V[:,test%4])
        expected=exhaustive(H,v)
        actual=enumerate_fixed_gram_block(Q.tolist(),B.tolist(),G.tolist(),v,time_limit=15)
        require(actual['complete'],'unfinished fixed-column control')
        require(actual['candidates']==expected,'Schur domain differs from exhaustive joint box')
        joint.append(dict(restriction_gram=Q.tolist(),mixed=B.tolist(),word_gram=G.tolist(),
                          fixed=v,free_rank=actual['rank'],candidates=len(expected)))
    require(not enumerate_gram_ellipsoid([[100,0],[0,100]],node_limit=1)['complete'],
            'budget stop presented as complete')
    payload=dict(passed=True,optimizer_used=False,ordinary_cases=ordinary,joint_cases=joint,
                 budget_stop_checked=True,source_sha256=hashlib.sha256(
                    (ROOT/'software/round5_unified.py').read_bytes()).hexdigest())
    text=json.dumps(payload,indent=2,default=int)+'\n'
    if len(sys.argv)>1:
        Path(sys.argv[1]).write_text(text)
    print(json.dumps(dict(passed=True,ordinary_cases=len(ordinary),joint_cases=len(joint),
                          budget_stop_checked=True,source_sha256=payload['source_sha256'])))


if __name__=='__main__':
    main()
