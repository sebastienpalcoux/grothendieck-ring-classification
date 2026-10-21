"""Complete forced split-module representation search for unresolved R8_3_1055.

The four exact representations are necessary data only, not fusion models.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sympy as s

HERE=Path(__file__).resolve().parent


def require(v,m):
    if not v:raise ValueError(m)


def run():
    row=next(r for r in json.loads((HERE.parents[1]/'rank8_m3_20261021/pipeline/census_m3.json').read_text())if r['id']=='R8_3_1055')
    R=row['tensor'];digest=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    require(digest==row['tensor_sha256'],'tensor mismatch')
    require(all(R[i][j]==R[j][i]for i,j in itertools.product(range(8),repeat=2)),'commutativity')
    require(R[3][3]==[1]+[0]*7,'involution')
    fixed=[i for i in range(8)if R[3][i][i]];require(fixed==[1,2],'fixed block')
    dual=[next(j for j in range(8)if R[i][j][0])for i in range(8)]
    require(dual==[0,2,1,3,4,5,6,7],'duality')
    t=s.Symbol('t');p=s.Matrix(R[1]).charpoly().as_poly().sqf_part()
    coeff=[int(v)for v in p.all_coeffs()]
    def evaluate(B):
        V=s.zeros(2)
        for c in coeff:V=V*B+c*s.eye(2)
        return V
    first_domain=[range(-R[1][v][w],R[1][v][w]+1,2)for v,w in itertools.product(fixed,repeat=2)]
    first_count=0;first_survivors=[]
    for entries in itertools.product(*first_domain):
        first_count+=1;B=s.Matrix(2,2,entries)
        if B*B.T==B.T*B and evaluate(B)==s.zeros(2):first_survivors.append(B)
    require(first_count==27 and first_survivors==[s.zeros(2)],'normal first-generator reduction failed')
    # Ring relations g*4=5 and g*6=7 reconstruct the remaining matrices.
    require(R[3][4]==[int(i==5)for i in range(8)]and R[3][6]==[int(i==7)for i in range(8)],'generator relations changed')
    def symmetric_options(x):
        a,b,c=R[x][1][1],R[x][1][2],R[x][2][2]
        return [s.Matrix([[u,v],[v,w]])for u,v,w in itertools.product(range(-a,a+1,2),range(-b,b+1,2),range(-c,c+1,2))]
    cases=0;solutions=[]
    for signs,A,B in itertools.product(itertools.product([-1,1],repeat=2),symmetric_options(4),symmetric_options(6)):
        cases+=1;S=[s.zeros(2)for _ in range(8)];S[0]=s.eye(2);S[3]=s.diag(*signs);S[4]=A;S[5]=S[3]*A;S[6]=B;S[7]=S[3]*B
        if any(S[dual[i]]!=S[i].T for i in range(8)):continue
        if any(abs(S[x][i,j])>R[x][v][w]or(S[x][i,j]-R[x][v][w])%2 for x in range(8)for i,v in enumerate(fixed)for j,w in enumerate(fixed)):continue
        if any(S[i]*S[j]!=sum((R[i][j][k]*S[k]for k in range(8)),s.zeros(2))for i,j in itertools.product(range(8),repeat=2)):continue
        solutions.append([[[int(z)for z in line]for line in M.tolist()]for M in S])
    require(cases==1296 and len(solutions)==4,'complete representation count changed')
    return {'id':row['id'],'tensor_sha256':digest,'scope':'complete necessary fixed-point difference representations over integers',
            'involution':3,'fixed':fixed,'normal_generator':1,'normal_generator_domain':first_count,
            'normal_generator_survivors':[[[0,0],[0,0]]],'reduced_simultaneous_domain':cases,
            'exact_simultaneous_representations':solutions,'representation_count':len(solutions),
            'outcome':'no_exclusion; four exact necessary representations; no associator/model constructed'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');a=p.parse_args();actual=run();path=HERE/'residual_split_1055_results.json'
    if a.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:require(json.loads(path.read_text())==actual,'evidence does not replay')
    print('PASS: complete R8_3_1055 split-module search gives four necessary representations, no exclusion/model')
