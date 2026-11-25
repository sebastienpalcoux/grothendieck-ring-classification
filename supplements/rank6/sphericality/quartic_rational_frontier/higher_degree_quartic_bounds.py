"""Exact cutoffs for quartic dimension fields with rational complementary codegrees.

Verify the finite coefficient ranges and radical inequalities in the field reduction."""
from fractions import Fraction as Q
from math import gcd, isqrt, prod
from pathlib import Path
from itertools import combinations
import json

SCALE=10**25

def factor(n):
    out={}
    p=2
    while p*p<=n:
        while n%p==0:
            out[p]=out.get(p,0)+1
            n//=p
        p+=1
    if n>1:out[n]=1
    return out

def sf(n):return n>0 and all(v==1 for v in factor(n).values())
def conductor(d):return d if d%4==1 else 4*d
def fundamental(a):
    return a>1 and ((a%4==1 and sf(a)) or
                    (a%4==0 and a//4%4 in (2,3) and sf(a//4)))

class Interval:
    def __init__(self,a,b=None):
        self.lo=Q(a);self.hi=Q(a if b is None else b)
        assert self.lo<=self.hi
    def __add__(self,o):
        o=asinterval(o);return Interval(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):return Interval(-self.hi,-self.lo)
    def __sub__(self,o):return self+-asinterval(o)
    def __rsub__(self,o):return asinterval(o)+-self
    def __mul__(self,o):
        o=asinterval(o)
        z=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi]
        return Interval(min(z),max(z))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=asinterval(o);assert o.lo>0
        return self*Interval(1/o.hi,1/o.lo)
    def __rtruediv__(self,o):return asinterval(o)/self
    def square(self):
        if self.lo>=0:return Interval(self.lo**2,self.hi**2)
        if self.hi<=0:return Interval(self.hi**2,self.lo**2)
        return Interval(0,max(self.lo**2,self.hi**2))
    def receipt(self):return [str(self.lo),str(self.hi)]

def asinterval(x):return x if isinstance(x,Interval) else Interval(x)
def root(x):
    x=asinterval(x);assert x.lo>=0
    lo=isqrt(x.lo.numerator*SCALE*SCALE//x.lo.denominator)
    hi=isqrt(x.hi.numerator*SCALE*SCALE//x.hi.denominator)+1
    return Interval(Q(lo,SCALE),Q(hi,SCALE))

def amplitude(c):return root(Q(gcd(c,2),c))
def ceilq(q):return -((-q.numerator)//q.denominator)
def strict_integer_cap(x):
    """A<x is guaranteed by A<an upper endpoint; return its integer cap."""
    return ceilq(asinterval(x).hi)-1

def ordinary_small_mass():
    remaining=[]
    tested=0
    for N in range(1,80):
        for L in range(N//2+1,N):
            tested+=1
            if L*L%N:continue
            delta=L*L-4*N
            if delta<=0 or isqrt(delta)**2==delta:continue
            d=prod(p for p,e in factor(delta).items() if e%2)
            c=conductor(d)
            if delta%c:continue
            b=isqrt(delta//c)
            if c*b*b!=delta or c*c*b*b>N*N:continue
            remaining.append(dict(conductor=c,trace=L,norm=N,
                                  coefficient=b,s=str(1-Q(L,N))))
    assert remaining==[dict(conductor=5,trace=15,norm=25,
                            coefficient=5,s='2/5')]
    # Its reciprocal difference has square 1/5, saturating the mixed bound.
    assert Q(5*5*5,25*25)==Q(1,5)
    # If s=2/5 and t<3/5, a rational signed complement has even
    # codegrees (4,4) or (4,6); neither denominator can produce3/5.
    low_even=[]
    for g in range(4,20,2):
        for h in range(g,30,2):
            if 1-Q(1,g)-Q(1,h)<Q(3,5):low_even.append((g,h))
    assert low_even==[(4,4),(4,6)]
    assert all(Q(b,g)+Q(c,h)!=Q(3,5)
               for g,h in low_even for b in range(1,g)
               for c in range(1,h))
    # A quadratic signed pair has trace(beta)=3g/5, hence 5|g.
    assert all((3*g)%5 for g in range(4,5))
    return dict(norm_range=[1,79],trace_pairs_tested=tested,
                surviving_quadratic_pair=remaining,
                even_signed_pairs_below_mass_three_fifths=low_even)

def mass_endpoints():
    assert Q(559,250)**2<5
    delta=Q(1,120)
    corners=[(Q(1,2),Q(1,2)),(Q(1,3),Q(2,3)),(Q(2,5),Q(3,5))]
    lower=[Q(559,250)*(t-delta)+5*(s-delta)**2 for s,t in corners]
    assert min(lower)==Q(240019,120000)>2
    return dict(corners=[dict(s=str(s),t=str(t)) for s,t in corners],
                square_root_lower_bound='559/250 < sqrt(5)',
                shift=str(delta),shifted_lower_bounds=list(map(str,lower)))

def tangent_pair(a,s,t,B):
    """Lower bound on y=q0+qj from a tangent to the matrix inequality."""
    r=asinterval(s)-B
    assert r.lo>0
    numerator=root(a)*t+a*r.square()-2
    denominator=2*root(a)+4*a*r
    return numerator/denominator

def zero_pair_possible(a,B):
    r=Interval(Q(1,2))-B
    if r.hi<=0:return True
    assert r.lo>=0
    test=root(a)/2+a*r.square()
    assert test.hi<2 or test.lo>2
    return test.hi<2

def exceptional_fields():
    two=[]
    for d in range(3,54,2):
        if not sf(d):continue
        cs=(conductor(d),conductor(2*d))
        B=sum(amplitude(c) for c in cs)
        if zero_pair_possible(8,B):
            two.append(tuple(sorted((2,d,2*d))))
    expected_d=[3,5,7,11,13,15,17,19,21,23,29,33,37,41]
    assert two==[tuple(sorted((2,d,2*d))) for d in expected_d]
    # For d>=55, both residue classes have amplitude <=3/(2sqrt55).
    assert not zero_pair_possible(8,Q(3,2)/root(55))

    three=[]
    for d in range(2,35):
        if d%3==0 or not sf(d):continue
        cs=(conductor(d),conductor(3*d))
        B=sum(amplitude(c) for c in cs)
        if zero_pair_possible(12,B):
            three.append(tuple(sorted((3,d,3*d))))
    expected_d3=[2,5,7,10,11,13]
    assert three==[tuple(sorted((3,d,3*d))) for d in expected_d3]
    # Each amplitude is <=3/(2sqrt d), so this proves the infinite tail.
    assert not zero_pair_possible(12,Q(3,2)/root(35))
    biquadratic=sorted(set(two+three))
    assert len(biquadratic)==19

    cyclic8=[]
    for J in range(16,177,16):
        m=J//16
        if m%2==0 or not sf(m):continue
        if zero_pair_possible(8,2*root(Q(2,J))):cyclic8.append(J)
    assert cyclic8==[16,48,80,112]
    assert not zero_pair_possible(8,2*root(Q(2,176)))
    cyclic=cyclic8+[20]
    assert len(biquadratic)+len(cyclic)==24
    return dict(biquadratic_radicands=biquadratic,
                cyclic_conductors=sorted(cyclic),count=24)

def height_cutoffs():
    # Outside the explicit field list, these are the largest remaining
    # ordinary Fourier-amplitude sums at a character of conductor8 or12.
    B8=amplitude(conductor(31))+amplitude(conductor(62))
    B12=amplitude(conductor(17))+amplitude(conductor(51))
    BC=2*root(Q(2,176))
    # Verify the finite initial intervals; later terms are monotone tails.
    exc=exceptional_fields()
    excluded=set(tuple(x) for x in exc['biquadratic_radicands'])
    for d in range(3,54,2):
        if sf(d) and tuple(sorted((2,d,2*d))) not in excluded:
            B=amplitude(conductor(d))+amplitude(conductor(2*d))
            assert B.hi<=B8.hi
    for d in range(2,35):
        if d%3 and sf(d) and tuple(sorted((3,d,3*d))) not in excluded:
            B=amplitude(conductor(d))+amplitude(conductor(3*d))
            assert B.hi<=B12.hi
    assert (Q(3,2)/root(55)).hi<B8.lo
    assert (Q(3,2)/root(35)).hi<B12.lo
    ell8=tangent_pair(8,Q(1,2),Q(1,2),B8)
    ell12=tangent_pair(12,Q(1,2),Q(1,2),B12)
    ellC=tangent_pair(8,Q(1,2),Q(1,2),BC)
    assert min(ell8.lo,ell12.lo,ellC.lo)>0
    caps={
        'biquadratic_conductor8':strict_integer_cap(1+1/ell8),
        'biquadratic_conductor12':strict_integer_cap(1+1/ell12),
        'cyclic_quadratic_conductor8':strict_integer_cap(1+1/ellC),
        'conductor12_with_s_one_third':strict_integer_cap(1+Q(4,3)/(Q(2,3)-1/root(3))),
        'all_other_pairs':strict_integer_cap(21+8*root(5)),
    }
    assert caps==dict(biquadratic_conductor8=264,
        biquadratic_conductor12=437,cyclic_quadratic_conductor8=206,
        conductor12_with_s_one_third=15,all_other_pairs=38)
    # If the second character conductor is at least1000, the exceptional
    # pair amplitudes are <=2sqrt(2/1000); each tangent then yields A<=38.
    Bfar=2*root(Q(2,1000))
    assert tangent_pair(8,Q(1,2),Q(1,2),Bfar).lo>Q(1,38)
    assert tangent_pair(12,Q(1,2),Q(1,2),Bfar).lo>Q(1,38)
    return dict(trace_caps=caps,uniform_cap_outside_24_fields=437,
        cap_when_second_conductor_at_least_1000=38,
        amplitude_intervals={k:v.receipt() for k,v in
            [('biquadratic8',B8),('biquadratic12',B12),('cyclic8',BC)]},
        pair_margin_intervals={k:v.receipt() for k,v in
            [('biquadratic8',ell8),('biquadratic12',ell12),('cyclic8',ellC)]})

def conductor_cutoffs():
    # At smallest character conductor >=88, the Fourier trace bound is <8.
    assert 88*3**2>28**2
    # But the relative-discriminant lower bound at degree4 forces A>7.
    assert 88>Q(33,4)**2
    rows=[]
    for a in range(5,88):
        if not fundamental(a):continue
        allowed=[]
        for A in range(5,39):
            if a<=16 or A<=5 or a*(A-5)**2<16*(A-1)**2:
                allowed.append(A)
        cap=max(allowed)
        # b^2 <= a*(A^2/4-4)^2.
        upper=isqrt(a*(cap*cap-16)**2//16)
        rows.append(dict(a=a,trace_cap_if_b_at_least_1000=cap,b_upper=upper))
    assert max(r['b_upper'] for r in rows)==1471
    assert [r['a'] for r in rows if r['b_upper']==1471]==[17]
    # The largest possible field conductor after the same bounds.
    products=[]
    for r in rows:
        # For a=8 or12 and b<1000 use b<=999; otherwise the pair trace
        # estimate applies at all b, except fields already explicitly listed.
        bound=max(999,r['b_upper']) if r['a'] in (8,12) else r['b_upper']
        products.append(r['a']*bound)
    assert max(products)==25007
    return dict(smallest_character_conductor_strict_upper_bound=88,
        second_character_conductor_strict_upper_bound=1472,
        field_conductor_upper_bound=25007,relative_discriminant_rows=rows)

def field_inventory():
    exception=exceptional_fields()
    special_bi=set(tuple(x) for x in exception['biquadratic_radicands'])
    special_cy=set(exception['cyclic_conductors'])
    def cap_for(a,b,bad_pair_data):
        cap=38
        if b<1000:
            for pair_conductor,B in bad_pair_data:
                ell=tangent_pair(pair_conductor,Q(1,2),Q(1,2),B)
                assert ell.lo>0
                cap=max(cap,strict_integer_cap(1+1/ell))
        if a>16:
            cap=min(cap,max(A for A in range(5,cap+1)
                            if A<=5 or a*(A-5)**2<16*(A-1)**2))
        return cap
    fs=[a for a in range(5,1472) if fundamental(a)]
    bi=[]
    for a in fs:
        if a>=88:break
        da=a if a%4 else a//4
        for b in fs:
            if b<=a:continue
            db=b if b%4 else b//4
            dc=da*db//gcd(da,db)**2
            c=conductor(dc)
            if c<b:continue
            radicands=tuple(sorted([da,db,dc]))
            field_conductor=a*b//gcd(a,b)
            if field_conductor>25007:continue
            special=radicands in special_bi
            bad=[]
            for pair_conductor in (8,12):
                if pair_conductor in (a,b,c):
                    others=[z for z in (a,b,c) if z!=pair_conductor]
                    bad.append((pair_conductor,sum(amplitude(z) for z in others)))
            cap=None if special else cap_for(a,b,bad)
            if cap is not None and 16*b*c>a*(cap*cap-16)**2:continue
            bi.append(dict(conductors=[a,b,c],radicands=radicands,
                           field_conductor=field_conductor,trace_cap=cap))
    cy=[]
    for J in range(5,1472):
        fac=factor(J);v2=fac.pop(2,0)
        if v2 not in (0,2,3,4) or any(e!=1 for e in fac.values()):continue
        primes=list(fac)
        eligible=[p for p in primes if p%4==1]
        for k in range(len(eligible)+1):
            for chosen in combinations(eligible,k):
                if v2!=4 and not chosen:continue
                a=(8 if v2==4 else 1)*prod(chosen)
                if a>=88:continue
                parity=prod((-1)**((p-1)//(4 if p in chosen else 2))
                            for p in primes)
                if v2==0 and parity!=1:continue
                if v2==2 and parity!=-1:continue
                multiplicity=2**(len(chosen) if v2==4 else len(chosen)-1)
                special=J in special_cy and a==(5 if J==20 else 8)
                bad=[(8,2*amplitude(J))] if a==8 else []
                cap=None if special else cap_for(a,J,bad)
                if cap is not None and 16*J*J>a*(cap*cap-16)**2:continue
                cy.append(dict(quadratic_conductor=a,conductor=J,
                               number_of_fields=multiplicity,trace_cap=cap))
    return dict(biquadratic=bi,cyclic=cy,
        biquadratic_count=len(bi),cyclic_count=sum(x['number_of_fields'] for x in cy),
        note='An outer field inventory after relative-discriminant bounds; no ratio exclusion is asserted.')

if __name__=='__main__':
    result=dict(ordinary_mass=ordinary_small_mass(),mass_endpoints=mass_endpoints(),
        exceptional_fields=exceptional_fields(),height=height_cutoffs(),
        conductors=conductor_cutoffs(),fields=field_inventory())
    path=Path(__file__).with_name('higher_degree_quartic_bounds_certificate.json')
    path.write_text(json.dumps(result,indent=2))
    print('Quartic exact bounds passed: a<88, b<1472, field conductor<=25007.')
    print('Outside24 explicitly listed fields, Tr_K(alpha)<=437; generic bound38.')
    print('Outer inventory:',result['fields']['biquadratic_count'],'biquadratic and',
          result['fields']['cyclic_count'],'cyclic quartic fields.')
    print('The field and height reductions do not assert categorical exclusion.')
