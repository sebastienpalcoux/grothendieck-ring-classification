"""Exact small-generator enumeration for the real cyclic quartic fields 15,20."""

if not __debug__:
    raise RuntimeError("Run this verifier with Python assertions enabled")

from fractions import Fraction
from math import isqrt
from collections import Counter

SCALE = 10**12
ONE = (1, 0, 0, 0)
FIELDS = {15: (1, 4, -4, -1), 20: (5, 0, -5, 0)}
# Three non-Perron conjugates are allowed absolute value at most sqrt(10).
SMALL_ROOT = 317* SCALE //100


def roots(poly):
    def sign(a):
        return (((a + poly[3]*SCALE)*a + poly[2]*SCALE**2)*a +
                poly[1]*SCALE**3)*a + poly[0]*SCALE**4
    points = list(range(-2*SCALE, 2*SCALE+1, SCALE//10))
    result = []
    for l, r in zip(points, points[1:]):
        if sign(l)*sign(r) >= 0:
            continue
        while r-l > 1:
            m = (l+r)//2
            if sign(l)*sign(m) < 0:
                r = m
            else:
                l = m
        result.append(l)
    assert len(result) == 4
    return result


def mul(x,y,p):
    v = [0]*7
    for i in range(4):
        for j in range(4): v[i+j] += x[i]*y[j]
    for i in (6,5,4):
        for j in range(4): v[i-4+j] -= v[i]*p[j]
    return tuple(v[:4])


def formal_trace(p):
    t=-p[3]
    t2 = t*t-2*p[2]
    return (4,t,t2,t*t2-p[2]*t-3*p[1])


def trace(x,T):
    return sum(a*b for a,b in zip(x,T))


def characteristics(x,field,T):
    if x==ONE:return (1,-4,6,-4)
    y=mul(x,x,field)
    a=trace(x,T); b=(a*a-trace(y,T))//2
    z=mul(x,y,field)
    c=(trace(z,T)-a*(a*a-2*b)+a*b)//3
    quart=trace(mul(y,y,field),T)
    e=(a*trace(z,T)-b*(a*a-2*b)+c*a-quart)//4
    return (e,-c,b,-a)


def add(*terms):
    return tuple(sum(k*v[j] for k,v in terms) for j in range(4))


def power_vectors(a,p):
    a2=mul(a,a,p)
    return (ONE,a,a2,mul(a,a2,p))


def embedding_boxes(poly,M):
    R=roots(poly)
    r1,r2,r3,r0=R
    # E=sum y_i/P'(r_i) by interpolation. The checked inequalities
    # |P'(r_i)|>1 and P'(r0)>1 give a deliberately enlarged range.
    for u in R:
        derivative = 4*u**3+3*poly[3]*u*u*SCALE+2*poly[2]*u*SCALE**2+poly[1]*SCALE**3
        assert abs(derivative)>SCALE**3+10**4*SCALE**2
    assert derivative>SCALE**3+10**4*SCALE**2
    # The sum of the three absolute divided-difference coefficients
    # controls C+(r1+r2+r3)E. Compute a rational outward bound,
    # using |root_i-root_j| >= (|R_i-R_j|-1)/SCALE.
    cd=Fraction(SMALL_ROOT,SCALE)*sum(Fraction(SCALE**2,
         (abs(u-v)-1)*(abs(u-w)-1)) for u,v,w in
        ((r1,r2,r3),(r2,r1,r3),(r3,r1,r2)))
    # B+(r1+r3)C+(r1^2+r1*r3+r3^2)E is their first divided difference.
    bd=Fraction(2*SMALL_ROOT,r3-r1-1)
    rp=[tuple(u**i//SCALE**(i-1) if i else SCALE for i in range(4)) for u in R]
    def neighbors(center,delta):
        return range((center-delta)//SCALE,(center+delta)//SCALE+2)
    def V(vec,pw):
        return sum(q*w for q,w in zip(vec,pw))
    for E in range(-10, M+11):
        for C in neighbors((r0+poly[3]*SCALE)*E,int(cd*SCALE)+SCALE//100):
            c2=(r1*r1+r1*r3+r3*r3)//SCALE
            for B in neighbors(-(r1+r3)*C-c2*E,int(bd*SCALE)+SCALE//100):
                for A in neighbors(-B*rp[1][1]-C*rp[1][2]-E*rp[1][3], SMALL_ROOT+SCALE//100):
                    x=(A,B,C,E)
                    assert max(abs(v) for v in x)<10**6
                    # |SCALE*root^i-rp| <15, so every approximate
                    # embedding error is less than 60*10^6/SCALE <.001.
                    if any(abs(V(x,pw))>SMALL_ROOT+SCALE//1000 for pw in rp[:3]): continue
                    d0=V(x,rp[3])
                    if not 2*SCALE-SCALE//1000<d0<M*SCALE+SCALE//1000:continue
                    # Each scaled power is enclosed within 15 units.  Include
                    # that error before rounding the Perron value upwards;
                    # rounding the approximation alone need not be an upper bound.
                    upper_error = 15*sum(abs(v) for v in x)
                    yield x,(d0+upper_error)//SCALE+1


def sqrt_exact(z):
    if z<0:return -1
    h=isqrt(z)
    return h if h*h==z else -1


def inv_num(x,poly,T):
    # Return integral numerator times norm for the inverse.
    h=characteristics(x,poly,T)
    v=power_vectors(x,poly)
    return add((-1,v[3]),(-h[3],v[2]),(-h[2],v[1]),(-h[1],v[0])),h[0]


def real_value(vec,r):
    return ((vec[3]*r+vec[2]*SCALE)*r+vec[1]*SCALE**2)*r+vec[0]*SCALE**3


def above_cutoff(vec,den,r,threshold):
    if den < 0:vec,den=tuple(-k for k in vec),-den
    # With an isolating interval [r/SCALE,(r+1)/SCALE] and |root|<2.
    err=(abs(vec[1])+4*abs(vec[2])+12*abs(vec[3]))*SCALE**2
    return real_value(vec,r)+err >= threshold*den*SCALE**3


def faithful_fourier(D,den,F,K,T):
    # sigma sends 2cos(2pi/F) to its Chebyshev transform for k=2 or 3.
    gen=(-2,0,1,0) if F==15 else (0,-3,0,1)
    powers=power_vectors(gen,K)
    v,m=inv_num(D,K,T)
    ys=[]
    for i in range(4):
        ys.append(v)
        v=add(*zip(v,powers))
    assert v==ys[0]
    a=add((1,ys[0]),(-1,ys[2])); b=add((1,ys[1]),(-1,ys[3]))
    square=add((1,mul(a,a,K)),(1,mul(b,b,K)))
    assert square[1:]==(0,0,0)
    return Fraction(square[0]*den*den,m*m)


def run(F,f,M):
    K=FIELDS[F]; T=formal_trace(K); R=roots(K)
    df=5*F**2; counts=Counter(); survivors=[]
    for d,dhi in embedding_boxes(K,M):
        pp=characteristics(d,K,T)
        dv=power_vectors(d,K)
        deriv=add((4,dv[3]),(3*pp[3],dv[2]),(2*pp[2],d),(pp[1],ONE))
        disc=characteristics(deriv,K,T)[0]
        if disc==0:continue # nonprimitive case handled in the text.
        assert disc>0 and disc%df==0
        ji2=disc//df
        counts['dimensions']+=1
        # D>=4 d^2 when d is the least nonunit dimension. Hence
        # n<=d/4 + sqrt(10)*sum_{g!=1}p_g*g(d)^2+1/f < d/4+4.
        nmax=dhi//4+4
        for rho in ((-1,0,1) if f==4 else (-1,1)):
            qq=add((f-1,dv[3]),((f-1)*pp[3]-rho,dv[2]),
                  ((f-1)*pp[2]-rho*pp[3]+f-rho*rho,d),
                  ((f-1)*pp[1]-rho*pp[2]+(f-rho*rho)*pp[3]-rho**3,ONE))
            # Norm(fn+qq) is charpoly(-qq) at fn.
            h=characteristics(tuple(-v for v in qq),K,T)
            jfull=f**3*ji2; f3=f**3
            for n in range(nmax+1):
                v=f*n
                norm=(((v+h[3])*v+h[2])*v+h[1])*v+h[0]
                if norm<f3 or norm%f3 or jfull%norm:continue
                if sqrt_exact(norm//f3)<0:continue
                counts['norm']+=1
                ell=add((1,qq),(v,ONE))
                inv,k=inv_num(ell,K,T)
                assert k==norm
                D=mul(deriv,inv,K); den=k//f # k divisible by f
                Dpol=characteristics(D,K,T)
                if any(Dpol[4-i]%den**i for i in range(1,5)):continue
                Dpol=tuple(v//den**(4-i) for i,v in enumerate(Dpol))
                if Dpol[3]**4%Dpol[0] or Dpol[2]**4%Dpol[0]**2:continue
                # Each of the four nonunit simples has dimension at least d.
                dimension_gap=add((1,D),(-4*den,dv[2]),(-den,ONE))
                if not above_cutoff(dimension_gap,den,R[3],0):continue
                if not all(above_cutoff(D,den,r,1) and
                  above_cutoff(tuple(-z for z in D),den,r,-11) for r in R[:3]):continue
                counts['before Fourier']+=1
                fsq=faithful_fourier(D,den,F,K,T)
                if F*fsq>1:
                    counts['faithful, '+str(fsq)]+=1
                    continue
                counts['after faithful']+=1
                # Parseval on Gal(K/Q) and the quadratic conductor five.
                # p=den/D, so Tr(p^2) follows from the reciprocal polynomial.
                E,negC,B,negA=Dpol
                tr_p2=Fraction(negC**2-2*B*E,E**2)
                if 4*tr_p2-Fraction((f-1)**2,f*f)>Fraction(1,5)+Fraction(2,F):continue
                survivors.append((d,rho,n,Dpol))
    return counts,survivors

if __name__=='__main__':
    import sys
    from quartic_generator_bound import generator_cap
    for F,f,M in ([(c,f,generator_cap(c,f)) for c,f in ((15,4),(15,5),(20,5))] if len(sys.argv)==1 else [tuple(map(int,sys.argv[1:]))]):
        cnt,z=run(F,f,M)
        print(F,f,M,dict(cnt),len(z),z[:12],flush=True)
        assert not z, "a small-simple dimension survived"
