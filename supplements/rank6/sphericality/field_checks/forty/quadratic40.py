"""Three square congruences over the dyadic orders at conductor forty. Python 3.8+."""
from itertools import product
from functools import lru_cache

radix = range(2)
binary = tuple(product(radix, repeat=6))
field_one = (1, 0, 0, 0)
epsilon = (0, 0, 1, 0)

def quadratic(a,b,c,d):
    return a*c+b*d, a*d+b*c+b*d  # phi^2 = 1+phi

def mul4(u,v):
    a,b,c,d=u
    x,y,z,w=v
    e,f=quadratic(a,b,x,y)
    g,h=quadratic(c,d,z,w)
    i,j=quadratic(a,b,z,w)
    k,l=quadratic(c,d,x,y)
    return e+2*g,f+2*h,i+k,j+l

def multiply(x,y,kind):
    u,v=x[4:]; a,b=y[4:]
    return mul4(x[:4],y[:4])+((u*a,v*b) if kind=="R" else quadratic(u,v,a,b))

def red(x,m): return tuple(t%m for t in x)

def powers(y):
    line=[field_one]
    while True:
        t=red(mul4(line[-1],y),16)
        if t==field_one:return line
        line.append(t)
        assert len(line)<=48

def conjugate(v,j,l):
    a,b,c,d=v
    if j: a,b,c,d=a+b,-b,c+d,-d
    if l: c,d=-c,-d
    return a,b,c,d

def normfield(a,b,c,d):
    return (2*c+d,c+3*d,2*a+b,a+3*b)

@lru_cache(None)
def parameters(kind):
    xi=powers((1,0,1,0)); ph=powers((0,1,0,0)); th=powers((3,0,-1,2))
    assert [len(xi),len(ph),len(th)]==[16,24,16]
    items=set()
    for i,j,l in product(range(len(xi)),range(0,len(ph),3),range(len(th))):
        if (i+l)%2!=1: continue
        for d in range(2):
            if (j+l+d)%2: continue
            base=(-1,2,0,0) if d else field_one
            v=mul4(mul4(xi[i],ph[j]),mul4(th[l],base))
            vinv=tuple((13**d)*x for x in mul4(mul4(xi[-i],ph[-j]),mul4(th[-l],base)))
            assert red(mul4(v,vinv),16)==field_one
            wk=[red(tuple((-1)**L*x for x in mul4(conjugate(v,J,L),vinv)),16) for J,L in ((1,0),(0,1),(1,1))]
            for h in range(1,16,2):
                invh=pow(h,-1,16)
                av=red(tuple(2*invh*x for x in mul4(epsilon,vinv)),16)
                kl=tuple(h*n for n in normfield(*v))
                if kind=="R":
                    for cn,m in product((1,9),(0,2)):
                        w=red(kl+(1,cn),16)
                        if (w[0]+1+cn)%16==4:
                            items.add((w,(av+(m,(-cn*m)%16),*(x+(1,1) for x in wk))))
                else:
                    for J,k in product(range(3,24,6),range(1,16,2)):
                        f=mul4(ph[J],(-1,2,0,0))
                        fi=tuple(13*t for t in mul4(ph[-J],(-1,2,0,0)))
                        v1=red(mul4(conjugate(f,1,0),fi),16)[:2]
                        a,b=f[:2]
                        w=red(kl+(k*(2*a+b),k*(a+3*b)),16)
                        if (w[0]+w[4])%16==4:
                            items.add((w,(av+(0,0),wk[0]+v1,wk[1]+(1,0),wk[2]+v1)))
    return items

def make_order(kind,width,hi,hj):
    one=(1,0,0,0,1,int(kind=='R'))
    def ell(v):return (v[1]+v[3]+v[5]+(v[4] if kind=='R' else 0))%2
    V=[v for v in binary if not ell(v) and (not width or not v[1])]
    a=(0,2*hi,1,2*hj,0,0)
    H={red(tuple(k*b+j*c+2*d for b,c,d in zip(one,a,v)),4)
       for k,j,v in product(range(2),range(1+width),V)}
    assert len(H)==64
    def inside(x):return red(x,4) in H
    def twice(x):return all(v%2==0 for v in x) and inside(tuple(v//2 for v in x))
    def fourtimes(x):return all(v%4==0 for v in x) and inside(tuple(v//4 for v in x))
    gens=[one]+([a] if width else [])+[tuple(2*x for x in v) for v in V]
    gens += [tuple(4*int(i==j) for j in range(6)) for i in range(6)]
    reps=[(0,)*6]
    for g in gens:
        if any(twice(tuple(x-y for x,y in zip(g,z))) for z in reps):continue
        reps+=[red(tuple(x+y for x,y in zip(g,z)),8) for z in reps]
    assert len(reps)==64 and all(inside(z) for z in reps)
    return one,H,inside,fourtimes,reps

def census(kind,width,hi,hj):
    one,H,inside,fourtimes,reps=make_order(kind,width,hi,hj)
    sq=[red(multiply(x,x,kind),16) for x in reps]
    keep=set()
    tested=set()
    for weight,markers in parameters(kind):
        if markers in tested:continue
        if not all(sum(t*x for t,x in zip(v,weight))%4==0 for v in H): continue
        if not all(inside(marker) for marker in markers): continue
        tested.add(markers)
        A,J,L,M=markers
        c1=tuple(2*a-j-l-m for a,j,l,m in zip(A,J,L,M))
        c2=tuple(2*b-l for b,l in zip(one,L))
        c3=tuple(2*a for a,l,m in zip(A,L,M))
        def count(values,rhs):
            return sum(fourtimes(tuple(x-y for x,y in zip(v,rhs))) for v in values)
        keep.add((count(sq,c1),count(sq,c2),count([multiply(v,A,kind) for v in sq],c3)))
    return keep

if __name__=="__main__":
    results={}
    for kind in ("R","T"):
        found=set()
        for w,i,j in [(0,0,0),*((1,i,j) for i,j in product(range(2),repeat=2))]:
            found.update(census(kind,w,i,j))
        print(kind,len(parameters(kind)),sorted(found))
        results[kind]=found
    assert results['R']=={(0,0,16),(0,2,0),(2,0,0),(2,2,0)}
    assert results['T']=={(0,0,0),(0,2,16)}
    assert not(results['R'] & results['T'])
