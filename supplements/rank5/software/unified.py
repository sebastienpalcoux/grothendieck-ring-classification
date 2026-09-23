"""Tensor-based decision engine. Census indices never enter a criterion."""
import json, itertools, hashlib
from pathlib import Path
from extension import *
import cyclic_four, quadratic_parity
P=Path(__file__).resolve().parents[1]

def basic_certificate(R):
    c=dnumber(R)
    if c:return c
    for i in range(1,len(R)):
        if R[i][i][0]==1 and R[i][i][i]>=2 and sum(R[i][i])==1+R[i][i][i]:
            return {'kind':'rank_two','object':i,'multiplicity':R[i][i][i]}
    c=cyclotomic_failure([M.charpoly(t).as_poly() for M in matrices(R)])
    if c:return c
    return subring_certificate(R)

def certificate(R,height=6,timeout=45):
    c=basic_certificate(R)
    if c:return c
    c=cyclic_four.certificate(R,height)
    if c:return c
    q=quadratic_parity.certificate(R)
    if q:
        c=extended_pseudo(R,height)
        if c:return {'kind':'quadratic_parity_pseudo','descent':q,'pseudo':c}
        c=sphere_certificate(R,lambda R:extended_pseudo(R,height))
        if c:return {'kind':'quadratic_parity_spherical','descent':q,'sphere':c}
    return general_certificate(R,height=height,timeout=timeout,positive_indicators=True)

def verify(R,c):
    k=c['kind']
    if k=='dnumber':check_dnumber(R,c)
    elif k=='rank_two':
        i=c['object'];require(0<i<len(R),'rank-two index')
        require(R[i][i][0]==1 and R[i][i][i]==c['multiplicity']>=2 and sum(R[i][i])==1+c['multiplicity'],'rank-two subring')
    elif k=='cyclotomic':check_cyclotomic([M.charpoly(t).as_poly() for M in matrices(R)],c)
    elif k=='subring':check_subring(R,c)
    elif k=='cyclic_four_central':cyclic_four.verify(R,c)
    elif k=='quadratic_parity_pseudo':
        quadratic_parity.verify(R,c['descent']);check_extended_pseudo(R,c['pseudo'])
    elif k=='quadratic_parity_spherical':
        quadratic_parity.verify(R,c['descent']);check_sphere(R,c['sphere'],check_extended_pseudo)
    else:verify_general(R,c)

def build_model_registry():
    from models import multiplicity_one_models,group_characters
    from models_extension import frobenius20,izumi_equivariantization,ty
    spec=multiplicity_one_models()
    phi=(1+s.sqrt(5))/2;phib=(1-s.sqrt(5))/2
    spec['Rep(A5)']=group_characters([[1,1,1,1,1],[3,-1,0,phi,phib],[3,-1,0,phib,phi],[4,0,1,-1,-1],[5,1,-1,0,0]],[1,15,20,12,12],60)
    w=(-1+s.sqrt(-3))/2;a=(-1+s.sqrt(-7))/2;ab=s.conjugate(a)
    spec['Rep(C7 semidirect C3)']=group_characters([[1,1,1,1,1],[1,1,1,w,w*w],[1,1,1,w*w,w],[3,a,ab,0,0],[3,ab,a,0,0]],[1,3,3,7,7],21)
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
