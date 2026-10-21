"""Independent central-idempotent accounting for the quartic NC scope gates."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'noncommutative'))
import central_support as c

def audit(R):
    s=c.s;a=c.w.ScalarCharacters(R);n=len(R)
    f,K,ds,D,pD,embedding=a.fp()
    c.require(all(N.T==a.N[a.du[i]] for i,N in enumerate(a.N)),'regular algebra is star closed and semisimple')
    roots=c.w.discover_roots(a.p,K)
    c.require(roots is not None and len(roots)==4,'all four scalar characters split in selected field')
    c.w.check_roots(a.p,K,roots)
    characters=[]
    for root in roots:
        character=[sum((K(co)*root**j for j,co in enumerate(polynomial)),K.zero) for polynomial in a.coeff]
        c.require(all(character[i]*character[j]==sum((K(R[i][j][k])*character[k] for k in range(n)),K.zero) for i in range(n) for j in range(n)),'all scalar multiplication identities')
        characters.append(character)
    matrix_character=[(K(int(s.trace(N)))-sum((ch[i] for ch in characters),K.zero))/K(2) for i,N in enumerate(a.N)]
    characters.append(matrix_character);multiplicities=[1,1,1,1,2]
    codegrees=[sum((ch[i]*ch[a.du[i]] for i in range(n)),K.zero)/K(m) for ch,m in zip(characters,multiplicities)]
    def product(x,y):
        return [sum((x[i]*y[j]*K(R[i][j][k]) for i in range(n) for j in range(n)),K.zero) for k in range(n)]
    idempotents=[[ch[a.du[i]]/fc for i in range(n)] for ch,fc in zip(characters,codegrees)]
    zero=[K.zero]*n;unit=[K.one]+[K.zero]*(n-1)
    for E,e in enumerate(idempotents):
        for F,ee in enumerate(idempotents):
            c.require(product(e,ee)==(e if E==F else zero),'primitive central projectors are orthogonal idempotents')
        for i in range(n):
            basis=[K.zero]*n;basis[i]=K.one
            c.require(product(e,basis)==product(basis,e),'central projector')
        trace=sum((co*K(int(s.trace(N))) for co,N in zip(e,a.N)),K.zero)
        c.require(trace==K(multiplicities[E]**2),'regular projector rank')
    c.require([sum((e[i] for e in idempotents),K.zero) for i in range(n)]==unit,'complete regular decomposition')
    center=s.Matrix([[R[i][j][k]-R[j][i][k] for i in range(n)] for j in range(n) for k in range(n)]).nullspace()
    c.require(len(center)==5,'five-dimensional center makes all five projectors primitive over C')
    c.require(a.scalar_rank==4 and a.matrix_codegree==4,'scalar and matrix accounting agrees')
    for E,ch in enumerate(characters):
        for F,other in enumerate(characters):
            inner=sum((ch[i]*other[a.du[i]] for i in range(n)),K.zero)
            c.require(inner==(codegrees[E]*K(multiplicities[E]) if E==F else K.zero),'full trace-character orthogonality')
    return {'center_dimension':5,'regular_projector_ranks':[1,1,1,1,4],
            'irreducible_dimensions':multiplicities,'scalar_polynomial':list(map(str,a.p.all_coeffs())),
            'scalar_polynomial_squarefree':True,'all_scalar_maps_enumerated':True,
            'matrix_formal_codegree':'4',
            'scalar_character_values':[[c.ec(x) for x in ch] for ch in characters[:4]],
            'matrix_trace_character':[c.ec(x) for x in matrix_character],
            'formal_codegrees':[c.ec(x) for x in codegrees],
            'central_idempotents':[[c.ec(x) for x in e] for e in idempotents]}

def audit_signed(R):
    """Rational scalar/matrix projectors; no positivity or Galois assumption."""
    s=c.s;a=c.w.ScalarCharacters(R);n=len(R)
    c.require(all(N.T==a.N[a.du[i]] for i,N in enumerate(a.N)),'signed regular algebra is star closed and semisimple')
    commutators=s.Matrix.vstack(*(Ni*Nj-Nj*Ni for Ni in a.N for Nj in a.N))
    basis=commutators.nullspace();c.require(len(basis)==4,'complete scalar submodule')
    W=s.Matrix.hstack(*basis);P=W*(W.T*W).inv()*W.T;Q=s.eye(n)-P
    c.require(P*P==P and Q*Q==Q and P*Q==s.zeros(n),'orthogonal regular projectors')
    c.require(all(P*N==N*P and Q*N==N*Q for N in a.N),'both regular summands invariant')
    c.require(P.rank()==Q.rank()==4,'regular block ranks')
    c.require(len(a.components)==1 and a.p.degree()==4 and s.gcd(a.p,a.p.diff()).degree()==0,'single separable quartic scalar field')
    scalar_blocks=[P*N for N in a.N];matrix_blocks=[Q*N for N in a.N]
    scalar_span=s.Matrix.hstack(*(s.Matrix(list(N)) for N in scalar_blocks))
    matrix_span=s.Matrix.hstack(*(s.Matrix(list(N)) for N in matrix_blocks))
    c.require(scalar_span.rank()==matrix_span.rank()==4,'both block algebras have dimension four')
    c.require(all(N*M==M*N for N in scalar_blocks for M in scalar_blocks),'scalar block commutative')
    pivots=matrix_span.rref()[1];B=[matrix_blocks[i] for i in pivots]
    center_equations=s.Matrix.vstack(*(s.Matrix.hstack(*(s.Matrix(list(N*M-M*N)) for N in B)) for M in B))
    c.require(len(B)-center_equations.rank()==1,'complementary block center one-dimensional')
    c.require(Q*a.C==8*Q and a.matrix_codegree==4,'matrix Casimir eigenvalue 8 gives formal codegree 4')
    f=a.components[0][0];K,ds,D,pD=a.component(f)
    c.require(all(ds[i]*ds[j]==sum((K(R[i][j][k])*ds[k] for k in range(n)),K.zero) for i in range(n) for j in range(n)),'all scalar maps verified over their irreducible field')
    return {'scalar_regular_rank':4,'matrix_regular_rank':4,'scalar_algebra_dimension':4,
            'matrix_algebra_dimension':4,'matrix_center_dimension':1,
            'scalar_polynomial':list(map(str,a.p.all_coeffs())),
            'scalar_polynomial_irreducible_and_separable':True,
            'all_scalar_maps_enumerated':True,'matrix_casimir_eigenvalue':8,
            'matrix_formal_codegree':4,'signed_dimension_polynomial':list(map(str,pD.all_coeffs())),
            'scalar_projector':[[str(x) for x in row] for row in P.tolist()],
            'matrix_projector':[[str(x) for x in row] for row in Q.tolist()]}
