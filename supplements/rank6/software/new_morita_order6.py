"""General obstruction from an involution dual of dimension type (1^6,d^6).

Here d=2+sqrt(5). Every admissible dual ring either violates an inherited
exact categorical criterion or has a faithful C3 grading whose neutral
component contains every connected two-dimensional algebra. An original
category with trivial universal grading therefore cannot exist.
"""
import itertools,json
from pathlib import Path
import sympy as s
from exact import require,poly,pc,norm_failure,check_norm,ec
from rings import dnumber,check_dnumber,codegree_factors,dual,permute,Characters
from module_dual_gram import anti_representations,module_matrices,dual_dimensions
from involution_module import invs
from prepare import key
P=Path(__file__).resolve().parents[1]

def compositions(total,n):
    if n==1:
        yield (total,);return
    for k in range(total+1):
        for tail in compositions(total-k,n-1):yield (k,)+tail

def cyclic_tensor(order,u,a):
    n=2*order;R=[[[0]*n for _ in range(n)] for _ in range(n)]
    for i,j in itertools.product(range(n),repeat=2):
        k=(i%order+j%order)%order
        if i<order and j<order:R[i][j][k]=1
        elif i<order or j<order:R[i][j][order+k]=1
        else:
            R[i][j][(k+u)%order]=1
            for h,c in enumerate(a):R[i][j][order+(k+h)%order]=c
    return R

def adjoint_closure(R):
    n=len(R);du=dual(R);J={0}
    for i in range(n):J.update(k for k,v in enumerate(R[i][du[i]]) if v)
    while True:
        nxt=J|{k for i in J for j in J for k,v in enumerate(R[i][j]) if v}
        if nxt==J:return sorted(J)
        J=nxt

def _isomorphism(R,S):
    n=len(R)
    for tail in itertools.permutations(range(1,n)):
        p=(0,)+tail
        if permute(R,p)==S:return list(p)
    return None

def inherited_sources():
    ids={'R6_2_20','R6_2_21'}
    tensors={r['id']:r['N'] for r in json.load(open(P/'data/census.json')) if r['id'] in ids}
    decisions={r['id']:r for r in json.load(open(P/'data/decisions.json')) if r['id'] in ids}
    from check import verify
    for rid in ids:
        require(decisions[rid]['status']=='excluded','inherited obstruction no longer allocated')
        verify(tensors[rid],decisions[rid]['certificate'])
    return tensors

def finite_dual_classification():
    """Reconstruct the entire cyclic parameter domain, no numerical decisions."""
    sources=inherited_sources();pD=poly([1,-120,720]);cyclic=[]
    for u,a in itertools.product(range(6),compositions(4,6)):
        if any(a[k]!=a[(u-k)%6] for k in range(6)):continue
        R=cyclic_tensor(6,u,a);cf=codegree_factors(R)
        why=dnumber(R)
        if why:check_dnumber(R,why)
        else:
            why=norm_failure(pD,cf)
            if why:check_norm(pD,cf,why)
        if why is None:
            r=2*u%3
            deg=[k%3 for k in range(6)]+[(k+r)%3 for k in range(6)]
            if all((deg[i]+deg[j]-deg[k])%3==0 for i in range(12) for j in range(12) for k in range(12) if R[i][j][k]):
                require(set(deg)=={0,1,2} and deg[3]==0,'grading is not faithful with neutral involution')
                why={'kind':'neutral_involution_C3_grading','degrees':deg,'unique_involution':3}
            else:
                for coset in range(2):
                    J=[0,2,4]+[6+coset,8+coset,10+coset]
                    if any(R[i][j][k] for i in J for j in J for k in range(12) if k not in J):continue
                    S=[[[R[i][j][k] for k in J] for j in J] for i in J]
                    p=_isomorphism(S,sources['R6_2_20'])
                    if p is not None:
                        why={'kind':'inherited_closed_subring','subset':J,'source':'R6_2_20','permutation':p};break
        require(why is not None,'unresolved cyclic dual ring')
        cyclic.append({'u':u,'a':list(a),'obstruction':why})
    require(len(cyclic)==60,'incomplete cyclic domain')
    # S3: after an inner gauge rho commutes with G; u is central, hence 1.
    # The three class coefficients satisfy a_e+3*a_t+2*a_c=4.
    nonabelian=[]
    for ae,at,ac in itertools.product(range(5),repeat=3):
        if ae+3*at+2*ac!=4:continue
        if at==0:
            A=(ae,ac,ac);S=cyclic_tensor(3,0,A)
            if A==(4,0,0):
                require(S[3][3]==[1,0,0,4,0,0],'rank two subring absent')
                why={'kind':'rank_two','multiplicity':4}
            else:
                matches=[(rid,_isomorphism(S,T)) for rid,T in sources.items()]
                matches=[(rid,p) for rid,p in matches if p is not None]
                require(len(matches)==1,'S3 C3 subring not identified')
                rid,p=matches[0];why={'kind':'inherited_closed_subring','source':rid,'permutation':p}
        else:
            require((ae,at,ac)==(1,1,0),'unexpected full S3 domain')
            # Sign character: rho eigenvalue lambda solves lambda^2+2lambda-1=0.
            # Its formal codegree is 6(1+lambda^2), polynomial x^2-48x+288.
            q=poly([1,-48,288]);why=norm_failure(pD,[(q,1)])
            require(why is not None,'S3 sign norm obstruction absent');check_norm(pD,[(q,1)],why)
        nonabelian.append({'class_coefficients':[ae,at,ac],'obstruction':why})
    require(len(nonabelian)==4,'incomplete S3 domain')
    return {'cyclic':cyclic,'symmetric_group':nonabelian}

def certificate(R):
    if len(R)!=6 or adjoint_closure(R)!=list(range(6)):return None
    if any(R[i][j]!=R[j][i] for i in range(6) for j in range(6)):return None
    fp=None
    for g in invs(R):
        info=anti_representations(R,g)
        if info is None:continue
        fixed,seeds,nodes,reps=info
        if not reps:continue
        if fp is None:fp=Characters(R).fp()
        f,K,ds,D,pD,em=fp;branches=[]
        for T in reps:
            labels,Ms=module_matrices(R,g,fixed,T)
            dims,counts=dual_dimensions(labels,Ms,g,K,ds)
            counts[tuple(ec(K.one))]+=1
            if len(counts)!=2:break
            one=tuple(ec(K.one));others=[z for z in counts if z!=one]
            if counts.get(one)!=6 or len(others)!=1 or counts[others[0]]!=6:break
            d=K(list(map(s.Rational,others[0])))
            if d*d!=K.one+K(4)*d or em.sign(d-K.one)<=0:break
            branches.append({'T':[list(x) for x in T],'dual_dimensions':[[list(z),c] for z,c in sorted(counts.items())]})
        if len(branches)==len(reps):
            return {'kind':'morita_order6','involution':g,'fixed':fixed,'generators':list(seeds),'generator_tuples':nodes,'branches':branches,'adjoint_closure':list(range(6))}
    return None

def verify(R,c,check_finite=True):
    require(certificate(R)==c,'Morita reduction hypotheses differ')
    if check_finite:finite_dual_classification()
    return True

if __name__=='__main__':
    finite=finite_dual_classification()
    manifest=P/'verification/continuation/campaign_manifest.json'
    rows=(json.load(open(manifest))['inputs'] if manifest.exists()
          else json.load(open(P/'data/unresolved_tensors.json')))
    hits=[]
    for row in rows:
        c=certificate(row['N'])
        if c is not None:
            verify(row['N'],c,False);hits.append({'id':row['id'],'certificate':c})
    out={'finite_dual_classification':finite,'exclusions':hits}
    target=P/'research/model_continuation/morita_order6_certificates.json'
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'exclusions':[r['id'] for r in hits],'cyclic_cases':len(finite['cyclic']),'S3_cases':len(finite['symmetric_group'])}))
