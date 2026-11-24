"""The seventeen realized based rings and exact basis identifications."""
import itertools
from rings import *

def build_model_registry():
    from models import multiplicity_one_models,group_characters
    from models_extension import frobenius20,izumi_equivariantization,ty
    spec=multiplicity_one_models()
    phi=(1+s.sqrt(5))/2;phib=(1-s.sqrt(5))/2
    spec['Rep(A5)']=group_characters([[1,1,1,1,1],[3,-1,0,phi,phib],[3,-1,0,phib,phi],[4,0,1,-1,-1],[5,1,-1,0,0]],[1,15,20,12,12],60)
    w=(-1+s.sqrt(-3))/2;a=(-1+s.sqrt(-7))/2;ab=s.conjugate(a)
    spec['Rep(C7 semidirect C3)']=group_characters([[1,1,1,1,1],[1,1,1,w,w*w],[1,1,1,w*w,w],[3,a,ab,0,0],[3,ab,a,0,0]],[1,3,3,7,7],21)
    # Independent SU(3)_4 Pieri construction of this tensor, up to basis permutation:
    # on weights (a,b)>=0 with a+b<=4, F sends (a,b) to (a+1,b),
    # (a-1,b+1), (a,b-1), omitting weights outside the alcove; put G=F.T.
    # The matrices for (1,1),(3,0),(0,3),(2,2) are respectively
    # A=F*G-I, B=F**3-2*F*G+I, C=G**3-2*F*G+I,
    # E=A**2-B-C-2*A-I. Restrict I,B,C,E,A to the neutral weights
    # (0,0),(3,0),(0,3),(2,2),(1,1). Exact comparison gives the tensor below.
    U1=[[0,1,0,0,0],[1,2,1,1,1],[0,1,1,1,1],[0,1,1,1,0],[0,1,1,0,1]]
    U2=[[0,0,1,0,0],[0,1,1,1,1],[1,1,1,0,0],[0,1,0,0,1],[0,1,0,1,0]]
    U3=[[0,0,0,0,1],[0,1,1,0,1],[0,1,0,1,0],[1,1,0,0,0],[0,0,1,1,0]]
    U=[s.eye(5).tolist(),U1,U2,U3,s.Matrix(U3).T.tolist()]
    spec['PSU(3)_4']=[s.Matrix(A).T.tolist() for A in U]
    spec['Rep(AGL(1,5))']=frobenius20()
    spec['Izumi C3+6 equivariantization']=izumi_equivariantization()
    for cyc in [False,True]:
        R=ty(cyc);R[4][4][4]=4;spec['Izumi '+('C4' if cyc else 'V4')+'+4']=R
    out=[]
    for name,R in spec.items():
        R=[[[int(x) for x in r] for r in M] for M in R];validate(R)
        out.append({'name':name,'tensor':R})
    require(len(out)==17,'positive registry size')
    require(len({canonical(r['tensor']) for r in out})==17,'duplicate positive model')
    return out

def match_model(R,registry):
    for i,rec in enumerate(registry):
        if max(flat(R))!=max(flat(rec['tensor'])):continue
        for p in itertools.permutations(range(1,len(R))):
            p=(0,)+p
            if permute(rec['tensor'],p)==R:return {'model':i,'name':rec['name'],'permutation':list(p)}
    return None
