"""Independent source tensors and a central-boson construction.

Existence inputs are mathematical constructions cited in the manuscript.
Neither source tensors nor quotient formulas depend on a census identifier.
"""
import itertools, json
from pathlib import Path
from functools import lru_cache
from exact import require
from oriented_signed import validate_general
from rings import permute
from positive_models import ng2, su2, product
from literature_models import free_involution_quotient
from existence import all_values
ROOT=Path(__file__).resolve().parents[1]

@lru_cache(None)
def extended_haagerup():
    """Burciu--Palcoux, arXiv:2210.13936v3, Section 5.1 (p.10).

    The unitary category is the dual even half, EH1, in the GMPPS convention.
    It is an even part of the subfactor constructed by BMPS; EH2 is the
    principal even half in that convention.
    Grossman--Morrison--Penneys--Peters--Snyder, Ann. Sci. ENS (4) 56
    (2023), no. 2, 589--664, Section 2.1, p.597, gives the EH1 fusion rules;
    doi:10.24033/asens.2541; arXiv:1810.06076.
    Coefficients are transcribed from the published six fusion matrices.
    """
    matrices=[
        '100000 010000 001000 000100 000010 000001',
        '010000 111000 011010 000011 001111 000112',
        '001000 011010 111111 001112 011123 001233',
        '000100 000011 001112 101122 011233 012234',
        '000010 001111 011123 011233 112345 013356',
        '000001 000112 001233 012234 013356 123467',
    ]
    R=[[list(map(int,row)) for row in m.split()] for m in matrices]
    validate_general(R)
    return R

def cyclic_near_group(n,m):
    """Near-group based ring, not an unconditional categorification constructor."""
    require(type(n) is int and n>0 and type(m) is int and m>=0,'invalid near-group parameters')
    R=[[[0]*(n+1) for _ in range(n+1)] for _ in range(n+1)]
    for i,j in itertools.product(range(n),repeat=2):R[i][j][(i+j)%n]=1
    for i in range(n):
        R[i][n][n]=R[n][i][n]=1
        R[n][n][i]=1
    R[n][n][n]=m
    validate_general(R)
    return R

@lru_cache(None)
def half_e6_psu2_6():
    """Half-E6 x PSU(2)_6, over the diagonal categorical central fermions.

    Half-E6 uses the central fermion explicitly supplied by Aasen--Lake--Walker.
    V6 in the standard unitary SU(2)_6 category is a fermion; its restriction
    supplies the required half-braiding in the even subcategory. Their product
    is a central boson. The V6-action is free, so no fixed-point resolution is
    assumed by the quotient formula.
    """
    parent=product(ng2(2),su2(6,True))
    return free_involution_quotient(parent,7)

def examples():
    yield ('Extended Haagerup EH1',extended_haagerup(),
           'Bigelow--Morrison--Peters--Snyder, Acta Math. 209 (2012), 29--82, '
           'arXiv:0909.4099; Grossman--Morrison--Penneys--Peters--Snyder, '
           'The Extended Haagerup fusion categories, Ann. Sci. Ec. Norm. Super. (4) '
           '56 (2023), no. 2, 589--664, Section 2.1, p.597, '
           'doi:10.24033/asens.2541, arXiv:1810.06076; '
           'fusion matrices: Burciu--Palcoux, arXiv:2210.13936v3, '
           'Section 5.1, p.10',all_values('yes'))
    yield ('Izumi C5+5 near-group category',cyclic_near_group(5,5),
           'Izumi, arXiv:1512.04288v2, Example 13.8 and Theorem 9.1; '
           'unitary near-group input already used for its inversion equivariantization',
           all_values('yes'))
    yield ('Diagonal-fermion quotient of half-E6 x PSU(2)_6',half_e6_psu2_6()[0],
           'Central-boson quotient proposition of the manuscript; half-E6 central '
           'fermion from Aasen--Lake--Walker, arXiv:1709.01941; standard unitary SU(2)_6',
           all_values('yes'))

def build_records():
    from prepare import key
    rows=json.loads((ROOT/'data/census.json').read_text())
    index={key(r['N']):r for r in rows};out=[]
    for name,R,ref,e in examples():
        target=index.get(key(R));require(target is not None,'model absent from census: '+name)
        ps=[(0,)+p for p in itertools.permutations(range(1,6)) if permute(R,(0,)+p)==target['N']]
        require(ps,'no full-tensor identification')
        rec=dict(id=target['id'],name=name,N=R,reference=ref,existence=e,census_permutation=list(min(ps)))
        out.append(rec)
        print(name,target['id'],min(ps),flush=True)
    (ROOT/'data/residual_positive_models.json').write_text(json.dumps(out,indent=2)+'\n')
    (ROOT/'data/half_e6_psu2_quotient.json').write_text(json.dumps(half_e6_psu2_6()[1],indent=2)+'\n')
    from relative_fibonacci_models import relative_tt3
    (ROOT/'data/relative_tt3.json').write_text(json.dumps(relative_tt3()[1],indent=2)+'\n')
    return out

def verify():
    rows=json.loads((ROOT/'data/census.json').read_text());index={r['id']:r['N'] for r in rows}
    stored=json.loads((ROOT/'data/residual_positive_models.json').read_text())
    built={name:(R,ref,e) for name,R,ref,e in examples()}
    require(len(stored)==len(built)==6 and {r['name'] for r in stored}==set(built),'registry coverage')
    for r in stored:
        R,ref,e=built[r['name']];validate_general(R)
        require(R==r['N'] and ref==r['reference'] and e==r['existence'],'source or structure mismatch')
        require(permute(R,tuple(r['census_permutation']))==index[r['id']],'full-tensor model mismatch')
    require(half_e6_psu2_6()[1]==json.loads((ROOT/'data/half_e6_psu2_quotient.json').read_text()),'quotient orbit data')
    sign_swap_scalar_check()
    from relative_fibonacci_models import verify_controls,relative_tt3
    verify_controls()
    require(relative_tt3()[1]==json.loads((ROOT/'data/relative_tt3.json').read_text()), 'relative center data')
    return dict(passed=True,model_records=6,checked_structure_constants=1296,sign_swap_scalar_cases=6,relative_center_controls=3)


# The constructor below is conditional on a supplied rank-three unitary category
# with central fermion. Only the known Ising (m=0) and half-E6 (m=2) inputs are
# admitted by the positive registry; ring associativity alone is not existence.
def sign_swap_equivariantization(m):
    """Orbit fusion of the sign-twisted swap on the diagonal-fermion quotient."""
    require(type(m) is int and m>=0,'invalid rank-three multiplicity')
    R=[[[0]*6 for _ in range(6)] for _ in range(6)]
    for i,j in itertools.product(range(4),repeat=2):R[i][j][i^j]=1
    for i in range(4):
        for x in (4,5):R[i][x][x]=R[x][i][x]=1
    R[4][4]=[1,1,1,1,m,2]
    R[4][5]=[0,0,0,0,2,2*m];R[5][4]=R[4][5][:]
    R[5][5]=[1,1,1,1,2*m,m*m]
    validate_general(R)
    return R


def sign_swap_scalar_check():
    """Exact Q(i) check of the equivariant invertible's square.

    e0,e1 are the two homogeneous components of (f,1)A. Balancing has
    e1 tensor e0 = - e0 tensor e1 and e1 tensor e1 = - e0 tensor e0.
    The equivariance sends T(e0)->i e1 and T(e1)->-i e0.
    """
    import sympy as s
    I=s.I
    u=[I,-I]
    # T exchanges the two homogeneous degrees, not complex scalars.
    require(all(s.simplify(u[a]*u[1-a])==1 for a in range(2)), 'swap coherence')
    mu={(0,0):(0,1),(0,1):(1,1),(1,0):(1,-1),(1,1):(0,-1)}
    checks=[]
    for a,b in itertools.product(range(2),repeat=2):
        c,v=mu[(1-a,1-b)]
        lhs=s.simplify(u[a]*u[b]*v)
        d,w=mu[(a,b)]
        rhs=w*((-1)**d)  # unit equivariance: 1 -> 1, b -> -b.
        require(c==d and lhs==rhs,'equivariant square is not the tensor unit')
        checks.append(dict(a=a,b=b,component=c,value=str(lhs)))
    return dict(passed=True,coherence_cases=2,tensor_square_cases=4,
                invertible_group='C2 x C2',checks=checks)

_original_examples=examples

def examples():
    yield from _original_examples()
    from relative_fibonacci_models import relative_tt3
    yield ('Relative Fibonacci center of TT3', relative_tt3()[0],
           'Gelaki--Naidu--Nikshych, arXiv:0905.3117, Remark 2.4; '
           'unitary TT3 and its Fibonacci subcategory: Edie-Michell, arXiv:1904.08909, '
           'Definition 2.5; exact relative-center reconstruction theorem of the manuscript',
           all_values('yes'))
    for m,source in [(0,'Ising'),(2,'half-E6')]:
        yield (f'Sign-swap equivariantization from {source}',sign_swap_equivariantization(m),
               'Sign-swap equivariantization theorem of the manuscript; categorical '
               f'input {source} with central fermion; Aasen--Lake--Walker, arXiv:1709.01941',
               all_values('yes'))

if __name__=='__main__':build_records();print(json.dumps(verify(),indent=2))
