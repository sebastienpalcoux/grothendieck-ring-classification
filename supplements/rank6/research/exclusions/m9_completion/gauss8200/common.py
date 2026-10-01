"""Small exact arithmetic core; all checks remain active under python -O."""
import itertools,hashlib,json,math
from fractions import Fraction
import sympy as s

def require(test,message):
    if not test:
        raise ValueError(message)

def pc(p):
    return list(map(str,p.all_coeffs()))

def flat(R): return tuple(v for M in R for row in M for v in row)

def dual(R):
    n=len(R)
    d=[]
    for i in range(n):
        hits=[j for j in range(n) if R[i][j][0]]
        require(len(hits)==1,'duality is not unique')
        d.append(hits[0])
    return d

def matrices(R): return list(map(s.Matrix,R))

def permute(R,p): return [[[R[i][j][k] for k in p] for j in p] for i in p]

def fingerprint(R): return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()

def casimir(R):
    N=matrices(R)
    return sum((a*a.T for a in N),s.zeros(len(R)))

def validate(R,nonnegative=True):
    n=len(R);I=range(n)
    require(all(len(M)==n and all(len(row)==n for row in M) for M in R),'tensor shape')
    require(all(type(v) is int and (v>=0 or not nonnegative) for v in flat(R)),'coefficient')
    du=dual(R)
    require(all(du[du[i]]==i for i in I),'duality involution')
    for i,j in itertools.product(I,repeat=2):
        require(R[0][i][j]==R[i][0][j]==int(i==j),'unit')
        require(R[i][j][0]==int(du[i]==j),'unit coefficient')
    for i,j,k in itertools.product(I,repeat=3):
        require(R[i][j][k]==R[j][i][k]==R[du[i]][k][j]==R[k][du[j]][i],'commutativity/reciprocity')
    N=matrices(R)
    for i,j in itertools.product(I,repeat=2):
        require(N[i]*N[j]==sum((R[i][j][k]*N[k] for k in I),s.zeros(n)),'associativity')

def mod_two_factors(R):
    n=len(R);vectors=list(itertools.product((0,1),repeat=n));zero=(0,)*n
    def mul(a,b):
        return tuple(sum(a[i]*b[j]*R[i][j][k] for i in range(n) for j in range(n))%2
                     for k in range(n))
    idems=[v for v in vectors if v!=zero and mul(v,v)==v]
    primitive=[v for v in idems if not any(w!=v and mul(v,w)==w for w in idems)]
    require(tuple(sum(v[i] for v in primitive)%2 for i in range(n))==(1,)+(0,)*(n-1),
            'primitive idempotents do not sum to the unit')
    require(all(mul(v,w)==zero for v,w in itertools.combinations(primitive,2)),
            'primitive idempotents are not orthogonal')
    factors=[]
    for e in primitive:
        space=[v for v in vectors if mul(e,v)==v]
        rank=(len(space)).bit_length()-1
        require(len(space)==2**rank,'mod-two factor does not have power-of-two order')
        nonzero=[v for v in space if v!=zero]
        field=all(any(mul(v,w)==e for w in nonzero) for v in nonzero)
        nil=[v for v in nonzero if mul(v,v)==zero]
        kind='unramified_field' if field else 'dual_numbers' if rank==2 and len(nil)==1 else 'other'
        factors.append({'unit':list(e),'rank':rank,'kind':kind,
                        'elements':[list(v) for v in space],
                        'square_zero_nonzero':[list(v) for v in nil]})
    require(sum(f['rank'] for f in factors)==n,'incomplete mod-two decomposition')
    return factors

def arithmetic(R):
    n=len(R)
    if n!=6 or dual(R)!=list(range(n)) or any(R[i][j]!=R[j][i] for i in range(n) for j in range(n)):
        return None
    validate(R)
    C=casimir(R);T=int(s.trace(C));data=[]
    for f,m in C.charpoly().as_poly().factor_list()[1]:
        if f.degree()==1:
            value=-s.Rational(f.TC(),f.LC())
            require(value.q==1 and value>0,'invalid rational formal codegree')
            data.append({'polynomial':pc(f),'multiplicity':int(m),'field_degree':1,
                         'trace_generators':[int(value)],'trace_ideal_generator':int(value)})
        elif f.degree()==2:
            A=-int(f.all_coeffs()[1]);B=int(f.TC());disc=A*A-4*B
            require(disc>0,'formal codegree field not real')
            q=math.prod(int(p) for p,e in s.factorint(disc).items() if e%2)
            b=math.isqrt(disc//q)
            require(q>1 and b*b*q==disc,'invalid quadratic discriminant')
            if q%4==1:
                require((A+b*q)%2==0,'nonintegral trace from quadratic integral basis')
                traces=[A,(A+b*q)//2];basis=['1','(1+sqrt(q))/2']
            else:
                traces=[A,b*q];basis=['1','sqrt(q)']
            step=math.gcd(*traces)
            require(step>0,'zero trace ideal')
            data.append({'polynomial':pc(f),'multiplicity':int(m),'field_degree':2,
                         'quadratic_radicand':q,'root_numerator':[A,b],'root_denominator':2,
                         'integral_basis':basis,'trace_generators':traces,'trace_ideal_generator':step})
        # Higher-degree factors are deliberately unused. Omitting necessary
        # divisibilities only weakens this criterion.
    if not data:return None
    L=math.lcm(*(v['trace_ideal_generator'] for v in data))
    deficits=[]
    for i in range(1,n):
        for j in range(i,n):
            for k in range(j,n):
                v=R[i][j][k]
                if v>=2:
                    w=len(set(itertools.permutations((i,j,k))))
                    deficits.append(w*(v*v-(v-2)**2))
    return {'rank':n,'original_Casimir_trace':T,'codegree_trace_ideals':data,
            'dimension_trace_multiple':L,'deficit_budget':T-L,
            'minimum_positive_magnitude_deficit':min(deficits) if deficits else None}

def squarefree(n):
    k = 1
    q = 1
    for p, e in s.factorint(n).items():
        k *= int(p) ** (e // 2)
        q *= int(p) ** (e % 2)
    return k, q

def integral(x,y,z,w,p,q):
    e,h = (1,2) if q % 4 == 1 else (0,1)
    return (h*w % 2 == 0 and h*(z-w) % 4 == 0
            and (y-e*w) % 2 == 0 and (x-y-e*z+e*w) % 4 == 0)

def positive(a,b,c,d,p,q):
    if a <= 0 or a*a <= p*b*b:
        return False
    L = a*a+p*b*b-q*(c*c+p*d*d)
    H = 2*a*b-2*q*c*d
    return L > 0 and L*L > p*H*H

def norm_numerator(x,y,z,w,p,q):
    L = x*x+p*y*y-q*(z*z+p*w*w)
    H = 2*x*y-2*q*z*w
    return L*L-p*H*H

def inverse_trace(a,b,c,d,p,q):
    # For Delta=(a+b*sqrt(p)+c*sqrt(q)+d*sqrt(pq))/4,
    # the constant coefficient of the cubic conjugate product is
    # a^3-a*p*b^2-a*q*c^2-a*p*q*d^2+2*p*q*b*c*d.
    num = a*a*a-a*p*b*b-a*q*c*c-a*p*q*d*d+2*p*q*b*c*d
    return Fraction(16*num, norm_numerator(a,b,c,d,p,q))

def conjugate_polynomial(delta,p,q):
    t=s.Symbol('t')
    a,b,c,d=[s.Rational(v,4) for v in delta]
    L=(t-a)**2+p*b*b-q*c*c-p*q*d*d
    H=-2*b*(t-a)-2*q*c*d
    P=s.Poly(L*L-p*H*H,t)
    require(all(v.q==1 for v in P.all_coeffs()),'nonintegral conjugate polynomial')
    return P
