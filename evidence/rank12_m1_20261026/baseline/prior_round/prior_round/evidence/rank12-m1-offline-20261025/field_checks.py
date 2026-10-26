"""Established FP-index and (with explicit PU gate) central dimension order."""
from pathlib import Path
import collections,json,math,signal,sys,time
import sympy as s
from sympy.matrices.normalforms import hermite_normal_form
from fp import fp_character,polynomial_of,exact,require
from state import current
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/work/rank11/arithmetic/legacy'))
import arithmetic as ar

def pu_gate(R,profile):
    if profile['squared_dimensions']is not None:return 'weak_integrality'
    G=profile['invertibles'];X=set(range(len(R)))-set(G)
    if X and {next(k for k in range(len(R))if R[g][min(X)][k])for g in G}==X:return 'two_FP_values_Galois_PU'
    return None

def central_order(R,f,K,u,d,D,emb,gate):
    deg=f.degree();v=[exact.vector(a,deg)for a in d]
    denom=s.ilcm(*[a.q for x in v for a in x]);A=s.Matrix.hstack(*v)*denom
    require(all(a.q==1 for a in A),'integer order matrix')
    H=hermite_normal_form(A.applyfunc(int));require(H.shape==(deg,deg),'full dimension-field order rank')
    inverse=H.inv();factors=ar.casimir(R).charpoly(exact.t).as_poly().factor_list()[1]
    comm=ar.comm(R)
    for q,m in factors:
        if deg%q.degree():return dict(kind='central_dimension_field',gate=gate,field_polynomial=exact.pc(f),casimir_factor=exact.pc(q),reason='field_degree',scope='general_complex_fusion_category')
        roots=exact.discover_roots(q,K)
        if roots is None:return dict(kind='central_dimension_field',gate=gate,field_polynomial=exact.pc(f),casimir_factor=exact.pc(q),reason='not_split_in_dimension_field',scope='general_complex_fusion_category')
        for lam in set(roots):
            allowed=[];details=[]
            for e in range(1,math.isqrt(m)+1):
                if comm and e!=1:continue
                beta=K(e)*D/lam
                coords=inverse*(exact.vector(beta,deg)*denom)
                integral=all(a.q==1 for a in coords)
                positive=emb.sign(beta-K(e))>=0
                if integral and positive:allowed.append(e)
                details.append(dict(irrep_degree=e,central_dimension=exact.ec(beta),order_coordinates=list(map(str,coords)),integral=integral,dimension_at_least_unit_multiplicity=positive))
            reached={0}
            for j in range(1,m+1):
                if any(j-e*e in reached for e in allowed):reached.add(j)
            if m not in reached:
                return dict(kind='central_dimension_order',gate=gate,field_polynomial=exact.pc(f),casimir_factor=exact.pc(q),casimir_root=exact.ec(lam),regular_multiplicity=m,allowed_irrep_degrees=allowed,degree_tests=details,reachable_multiplicities=sorted(reached),scope='general_complex_fusion_category')
    return None

def main():
    start=time.monotonic();data=json.loads((ROOT/'tensors.json').read_text());profiles=json.loads((ROOT/'profile.json').read_text())['records'];ex,mo=current();out=[]
    for profile in profiles:
        rid=profile['id']
        if rid in ex or rid in mo:continue
        R=data[rid];f,K,u,d,D,emb=fp_character(R);cs=[];gate=pu_gate(R,profile)
        rec=dict(id=rid,tensor_sha256=ar.sha(R),field_polynomial=exact.pc(f),dimensions_in_field=[exact.ec(a)for a in d],positive_root_interval=[str(emb.lo),str(emb.hi)],PU_gate=gate)
        c=exact.cyclotomic_failure([f])
        if c:cs.append(dict(c,kind='FP_sum_cyclotomic',scope='general_complex_fusion_category'))
        for J in profile['subrings']:
            if len(J)in(1,len(R)):continue
            S=sum((d[j]**2 for j in J),K.zero);p=polynomial_of(D/S,f,K,u)
            if any(a.q!=1 for a in p.all_coeffs()):
                cs.append(dict(kind='FP_subcategory_index',subset=J,quotient_polynomial=exact.pc(p),scope='general_complex_fusion_category'));break
        if not cs and gate:
            c=central_order(R,f,K,u,d,D,emb,gate)
            if c:cs.append(c)
        rec['certificates']=cs;out.append(rec)
        if len(out)%20==0:
            print('processed',len(out),'excluded',sum(bool(r['certificates'])for r in out),'seconds',round(time.monotonic()-start,2),flush=True)
            (ROOT/'field_checks.json').write_text(json.dumps(dict(records=out),indent=2)+'\n')
    (ROOT/'field_checks.json').write_text(json.dumps(dict(records=out,elapsed_seconds=time.monotonic()-start),indent=2)+'\n')
    print('DONE',len(out),'excluded',sum(bool(r['certificates'])for r in out),'seconds',time.monotonic()-start)

if __name__=='__main__':main()
