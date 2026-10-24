#!/usr/bin/env python3
"""Exact finite checks for the independent R8_3_436 equivariantization obstruction.
Categorical descent and formal-codegree theorems are proved/stated in REPAIR.md.
No old acceptance file, repository, or website is modified.
"""
from pathlib import Path
import argparse,hashlib,itertools,json
from fractions import Fraction
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent

def require(c,msg):
    if not c: raise ValueError(msg)
def sha(x): return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def source():
    r=json.loads((OUT/'source.json').read_text())
    N=r['tensor']; H=[0,1,2,5]; odd=[3,4,6,7]
    require(sha(N)=='0f6d68de67a7287db7dd32a786237f7af9f35ec7c26b3ada2ba50012ff5455c7','source hash')
    A=[[[0]*4 for _ in range(4)] for _ in range(4)]
    for i,j in itertools.product(range(3),repeat=2):A[i][j][(i+j)%3]=1
    for i in range(3):A[i][3][3]=A[3][i][3]=1
    A[3][3]=[1,1,1,3]
    require([[[N[i][j][k] for k in H] for j in H] for i in H]==A,'near-group subring')
    deg=[int(i in odd) for i in range(8)]
    require(all(not N[i][j][k] or (deg[i]+deg[j])%2==deg[k] for i,j,k in itertools.product(range(8),repeat=3)),'C2 grading')
    def prod(i,j):
        require(sum(N[i][j])==1,'not simple product')
        return N[i][j].index(1)
    require(prod(3,3)==0,'t order two')
    require([prod(prod(3,i),3) for i in H]==[0,2,1,5],'inversion')
    return {'id':r['id'],'tensor_sha256':sha(N),'neutral_basis':H,'odd_basis':odd,'t':3,'conjugation':[0,2,1,5]}

def rank5(a,b,nonselfdual=False):
    # basis 1,e,y,x,z=e*x; e is central.
    N=[[[0]*5 for _ in range(5)] for _ in range(5)]
    def put(i,j,v):N[i][j]=list(v);N[j][i]=list(v)
    for i in range(5):v=[0]*5;v[i]=1;put(0,i,v)
    put(1,1,[1,0,0,0,0]);put(1,2,[0,0,1,0,0]);put(1,3,[0,0,0,0,1]);put(1,4,[0,0,0,1,0]);put(2,2,[1,1,1,0,0]);put(2,3,[0,0,0,1,1]);put(2,4,[0,0,0,1,1])
    v=[0,0,1,a,b];v[int(nonselfdual)]=1
    put(3,3,v);put(4,4,v)
    put(3,4,[v[1],v[0],1,b,a])
    return N

def ringaxioms(N,dual):
    n=len(N)
    return all(sum(N[i][j][u]*N[u][k][v] for u in range(n))==sum(N[j][k][u]*N[i][u][v] for u in range(n)) for i,j,k,v in itertools.product(range(n),repeat=4)) and all(N[i][j][k]==N[dual[j]][dual[i]][dual[k]] for i,j,k in itertools.product(range(n),repeat=3)) and all(N[i][j][0]==int(i==dual[j]) for i,j in itertools.product(range(n),repeat=2))

def main():
    result={'schema':'r436-independent-equivariantization-v1','source':source(),'spherical_dimension_field':'Q(sqrt(21))','categorical_premises_not_proved_by_code':['Thornton near-group sphericality','pointed-cocycle cancellation on a faithful C2 grading','equivariantization of a spherical category under spherical action','Ostrik Theorem 2.13 and Corollary 2.15'],'branches':[]}
    X=s.symbols('X');D=21+3*s.sqrt(21)
    for a in range(4):
        b=3-a;N=rank5(a,b);require(ringaxioms(N,list(range(5))),'self-dual candidate axioms')
        require(not ringaxioms(rank5(a,b,True),[0,1,2,4,3]),'non-selfdual branch should fail')
        h=a-b; m=h*h+4; f=m+h*s.sqrt(m)
        chi=[1,-1,0,(h+s.sqrt(m))/2,-(h+s.sqrt(m))/2]
        require(all(s.simplify(chi[i]*chi[j]-sum(N[i][j][k]*chi[k] for k in range(5)))==0 for i,j in itertools.product(range(5),repeat=2)),'character')
        require(s.simplify(sum(x*x for x in chi)-f)==0,'formal codegree')
        require(s.minpoly(f,X)==X**2-2*m*X+4*m,'formal-codegree polynomial')
        require(s.simplify(D*(21-3*s.sqrt(21)))==252,'global norm')
        ratio_norm=Fraction(252**2,(4*m)**2)
        require(ratio_norm.denominator!=1,'norm should not be integral')
        require(s.sqrt(m) not in [s.sqrt(21),-s.sqrt(21)],'field distinction')
        result['branches'].append({'a':a,'b':b,'s':h,'tensor':N,'tensor_sha256':sha(N),'all_associativity_and_star_identities':True,'nonselfdual_branch_fails_star':True,'formal_codegree_polynomial':[1,-2*m,4*m],'global_dimension_norm':252,'formal_codegree_norm':4*m,'biquadratic_ratio_norm':str(ratio_norm),'outcome':'no_spherical_categorification'})
    result['scope']='general_complex';result['outcome']='excluded_by_independent_replacement_proof'
    parser=argparse.ArgumentParser(); parser.add_argument('--write',action='store_true'); args=parser.parse_args()
    if args.write:
        (OUT/'equivariantization_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    else:
        require(json.loads((OUT/'equivariantization_certificate.json').read_text())==result,'saved certificate differs')
    print('PASS: source grading/inversion; all4 selfdual branches; no nonselfdual branch; exact formal codegrees and nonintegral norms.')
if __name__=='__main__':main()
