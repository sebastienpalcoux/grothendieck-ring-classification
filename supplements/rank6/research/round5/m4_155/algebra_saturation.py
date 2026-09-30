"""Exact unit-column saturation of the six forced centralizer low algebras.

No categorification assertion is inferred from passing these necessary tests.
"""
import argparse,json,sys,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import sympy as s
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp
from exact import require

def check_pair(A,B,unit,extra=()):
    generators=[A,B]+list(extra);n=A.rows
    require(all(M==M.T for M in generators) and all(M*N==N*M for M in generators for N in generators),'low matrices not commuting self-dual fusion actions')
    powers=None
    for q in range(1,20):
        G=sum((q**j*M for j,M in enumerate(generators)),s.zeros(n));cp=G.charpoly().as_poly();minimal=cp.sqf_part();k=minimal.degree();powers=[s.eye(n)]
        for _ in range(k):powers.append(powers[-1]*G)
        require(sum((c*M for c,M in zip(reversed(minimal.all_coeffs()),powers)),s.zeros(n))==s.zeros(n),'minimal polynomial failed')
        U=s.Matrix.hstack(*(M[:,unit] for M in powers[:-1]));rank=U.rank()
        if rank<k:
            c=U.nullspace()[0];N=sum((z*M for z,M in zip(c,powers)),s.zeros(n));require(any(N),'matrix algebra relation unexpectedly zero')
            return dict(passed=False,reason='noninjective_unit_column',generator_parameter=q,algebra_dimension=k,unit_cyclic_rank=rank,polynomial=list(map(str,c)),matrix=list(map(list,N.tolist())))
        pivot_rows=U.T.rref()[1];minor=U[list(pivot_rows),:];inverse=minor.inv()
        if all(U*(inverse*M[list(pivot_rows),unit])==M[:,unit] and sum((z*X for z,X in zip(inverse*M[list(pivot_rows),unit],powers)),s.zeros(n))==M for M in generators):break
    else:raise RuntimeError('no separating small generic low combination found')
    D,L,T=smith_normal_decomp(DomainMatrix.from_Matrix(U));D=D.to_Matrix();L=L.to_Matrix();T=T.to_Matrix()
    require(L*U*T==D and abs(L.det())==1 and abs(T.det())==1,'invalid Smith decomposition')
    record=dict(generator_parameter=q,algebra_dimension=k,centralizer_rank=n,joint_spectrum_factors=[dict(polynomial=str(f.as_expr()),multiplicity=m,degree=f.degree()) for f,m in cp.factor_list()[1]],smith_invariants=[int(D[i,i]) for i in range(k)],saturated_basis=[])
    for j in range(k):
        denominator=D[j,j];v=U*T[:,j]/denominator;N=sum((z*M for z,M in zip(T[:,j],powers)),s.zeros(n))/denominator
        require(all(z.q==1 for z in v) and N[:,unit]==v,'saturated unit vector reconstruction failed')
        bad=[(i,h,N[i,h]) for i in range(n) for h in range(n) if N[i,h].q!=1]
        if bad:
            record.update(passed=False,reason='nonintegral_saturated_action',saturated_vector=list(map(int,v)),polynomial=[str(z/denominator)for z in T[:,j]],first_failure=[bad[0][0],bad[0][1],str(bad[0][2])]);return record
        record['saturated_basis'].append(dict(vector=list(map(int,v)),matrix=[list(map(int,row))for row in N.tolist()]))
    record.update(passed=True,reason='unit_saturation_survives')
    V=s.Matrix.hstack(*(s.Matrix(z['vector']) for z in record['saturated_basis']));rr,piv=V.T.rref();cone=rr.T
    if all(z>=0 for z in cone):
        inv=V[list(piv),:].inv();operators=[s.Matrix(z['matrix']) for z in record['saturated_basis']]
        actions=[sum((a*M for a,M in zip(inv*cone[list(piv),j],operators)),s.zeros(n)) for j in range(k)]
        record['positive_cone']=[dict(vector=list(map(str,cone[:,j])),matrix=[[str(z)for z in row]for row in N.tolist()])for j,N in enumerate(actions)]
        bad=[(j,i,h,N[i,h]) for j,N in enumerate(actions) for i in range(n) for h in range(n) if N[i,h]<0]
        if bad:record.update(passed=False,reason='negative_positive_cone_action',first_failure=[*bad[0][:3],str(bad[0][3])])
        else:record['positive_cone_passed']=True
    return record

def calculate():
    source=json.loads((Path(__file__).parent/'packet_frontier.json').read_text());out=[]
    for split in source['splittings']:
        for survivor in split['survivors']:
            packet=next(c for c in source['cases'] if c['profile']==split['profile'])['survivors'][split['orientation']];W=packet['W'];unit=W.index([1,0,0,0,0,0]);r=check_pair(s.Matrix(survivor['Na']),s.Matrix(survivor['Nb']),unit)
            rec=dict(profile=split['profile'],orientation=split['orientation'],quadratic_sign=split['quadratic_sign'],unit=unit,**r);out.append(rec);print({k:v for k,v in rec.items() if k not in ('saturated_basis','positive_cone')},flush=True)
    require(len(out)==source['low_matrix_pairs']==6,'incomplete pair coverage');return dict(id='R6_4_155',scope='six_forced_semion_centralizer_low_matrix_pairs',optimizer_used=False,cases=out)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--verify',action='store_true');args=ap.parse_args();p=Path(__file__).with_suffix('.json');result=calculate()
    if args.verify:require(result==json.loads(p.read_text()),'unit saturation certificate differs')
    else:p.write_text(json.dumps(result,indent=2)+'\n')
