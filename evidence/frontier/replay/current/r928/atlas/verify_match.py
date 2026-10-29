#!/usr/bin/env python3
"""Exact simultaneous S,T and based-ring match with Anyon Atlas B20-02148.

Safe AST parsing of downloaded cyclotomic expressions; no eval or network.
Run with paths to atlas JSON export, project modular JSON, project tensor JSON.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from functools import lru_cache
import ast, hashlib, itertools, json, sys

def need(ok,msg):
    if not ok: raise ValueError(msg)
def root(k):
    k%=288; d={k:Q(1)}
    for i in range(k,95,-1):
        a=d.pop(i,0)
        if a:
            d[i-48]=d.get(i-48,0)+a
            d[i-96]=d.get(i-96,0)-a
    return tuple(sorted((i,c) for i,c in d.items() if c))
R=[root(k) for k in range(288)];ONE=R[0]
def add(*zs):
    d=defaultdict(Q)
    for z in zs:
        for k,c in z:d[k]+=c
    return tuple(sorted((k,c) for k,c in d.items() if c))
def scale(a,z):return tuple((k,a*c) for k,c in z if a*c)
@lru_cache(None)
def mul(a,b):return add(*(scale(c*d,R[(k+l)%288]) for k,c in a for l,d in b))
def scalar(z):
    need(all(k==0 for k,c in z),'division/exponent must be rational')
    return z[0][1] if z else Q(0)
def visit(n):
    if isinstance(n,ast.Constant) and type(n.value) is int:return scale(Q(n.value),ONE)
    if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.USub,ast.UAdd)):
        return scale(-1 if isinstance(n.op,ast.USub) else 1,visit(n.operand))
    if isinstance(n,ast.BinOp):
        a,b=visit(n.left),visit(n.right)
        if isinstance(n.op,ast.Add):return add(a,b)
        if isinstance(n.op,ast.Sub):return add(a,scale(-1,b))
        if isinstance(n.op,ast.Mult):return mul(a,b)
        if isinstance(n.op,ast.Div):return scale(1/scalar(b),a)
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='E' and len(n.args)==1 and not n.keywords:
        q=288*scalar(visit(n.args[0]));need(q.denominator==1,'root outside Q(zeta288)')
        return R[int(q)%288]
    raise ValueError('Unsupported expression node: '+ast.dump(n))
@lru_cache(None)
def parse(s):return visit(ast.parse(s,mode='eval').body)

def main():
    if len(sys.argv)==1:
        here=Path(__file__).resolve().parent
        sys.argv += [str(here/'B20-02148_export.json'),str(here.parent/'rank20_modular_data.json'),str(here.parent/'rank20_fusion_tensor.json')]
    need(len(sys.argv)==4,'usage: verify_atlas_match.py ATLAS_JSON PROJECT_MODULAR_JSON PROJECT_TENSOR_JSON')
    paths=list(map(Path,sys.argv[1:]));atlas,md,tr=[json.loads(p.read_text()) for p in paths]
    records=atlas['records'];need(len(records)==1 and records[0]['id']=='B20-02148','Atlas record identity')
    a=records[0];n=20
    AS=[[parse(x) for x in row] for row in a['modularData']['S']]
    AT=[parse(x) for x in a['modularData']['T']]
    S=[[tuple((int(k),Q(c)) for k,c in z) for z in row] for row in md['S']]
    T=[R[e] for e in md['twist_exponents_mod288']];N=tr['tensor']
    need(AS[0][0]==ONE,'Atlas S normalization')
    r2=add(R[36],R[252]);r3=add(R[24],R[264]);r6=mul(r2,r3)
    D=add(*(scale(Q(c),z) for c,z in zip((144,96,80,56),(ONE,r2,r3,r6))))
    L=scale(Q(1,2),mul(D,r2))
    need(mul(S[0][0],L)==ONE,'project normalization L')
    U=[[mul(z,L) for z in row] for row in S]
    candidates=[[j for j in range(n) if U[0][i]==AS[0][j] and T[i]==AT[j]] for i in range(n)]
    need(all(candidates),'dimension/twist candidates for all simples')
    valid=[]
    for p in itertools.product(*candidates):
        if len(set(p))!=n:continue
        if all(U[i][j]==AS[p[i]][p[j]] for i in range(n) for j in range(n)):valid.append(p)
    need(valid,'simultaneous exact S,T identification')
    p=valid[0]
    f=a['fusionRules'];need(f['encoding']=='sparse' or 'sparse' in str(f['encoding']).lower(),'sparse fusion encoding')
    lifts=f['lifts'];need(len(lifts)==1,'bosonic fusion tensor lift')
    lift=lifts[0]
    entries=lift if isinstance(lift,list) else lift.get('entries',lift.get('coefficients'))
    need(isinstance(entries,list),'fusion entries')
    AN=[[[0]*n for _ in range(n)] for _ in range(n)]
    for i,j,k,c in entries:AN[i][j][k]=AN[j][i][k]=c
    need(all(N[i][j][k]==AN[p[i]][p[j]][p[k]] for i in range(n) for j in range(n) for k in range(n)),'all8000 fusion coefficients')
    receipt={'status':'PASS','atlas_id':a['id'],'atlas_url':'https://anyonatlas.org/data/B20-02148',
      'scope':'Exact simultaneous S,T identification and based-ring isomorphism; no categorical equivalence or categorification claim',
      'field':'Q(zeta288), Phi=x^96-x^48+1','project_to_atlas_zero_based':list(p),
      'normalization':'S_Atlas=L*S_project, L=(144+96sqrt2+80sqrt3+56sqrt6)/sqrt2',
      'matching_permutations':len(valid),'S_entries_checked':400,'T_entries_checked':20,'fusion_coefficients_checked':8000,
      'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
      'atlas_export_generatedAt':atlas.get('generatedAt')}
    out=paths[0].parent/'atlas_match_receipt.json';out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
