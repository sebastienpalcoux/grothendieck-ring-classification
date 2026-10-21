"""Complete fixed-integer-pattern Q(sqrt3,sqrt13) rotation and STS test."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,itertools,json,math
import verify as base
import certified_lp as lp
from exact import vector,discover_roots
HERE=Path(__file__).resolve().parent;s=base.s;need=base.need


def disc(q):return q if q%4==1 else 4*q


def trace_types(height,qs=(3,13),primes=(2,3,13),orders=None,powers=None):
    powers=list(range(1,height+1))if powers is None else powers
    radicands=(qs[0],qs[1],qs[0]*qs[1]);conductors=tuple(map(disc,radicands))
    if orders is None:
        bound=1
        for p in primes:
            conductor=max(int(s.factorint(d).get(p,0))for d in conductors);power=0
            while p**(power+1)<=height:power+=1
            bound*=p**(conductor+power)
        orders=s.divisors(bound);out={tuple((F(0),)*4 for k in powers)}
    else:bound=None;out=set()
    for order in orders:
        order=int(order)
        for sign0,sign1 in itertools.product((-1,1),repeat=2):
            values=[]
            for k in powers:
                g=math.gcd(order,k);n=order//g;phi=int(s.totient(n));a=[F(int(s.mobius(n)),phi)]
                for q,D,sign in zip(radicands,conductors,(sign0,sign1,sign0*sign1)):
                    z=n//D;value=F(0)
                    if n%D==0 and math.gcd(z,D)==1:
                        value=F(sign*int(s.mobius(z))*int(s.kronecker_symbol(D,z))*int(s.kronecker_symbol(D,k//g))*math.isqrt(D//q),phi)
                    a.append(value)
                values.append(tuple(a))
            out.add(tuple(values))
    return sorted(out),bound


def mul(a,b,qs=(3,13)):
    out=[F(0)]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i^j]+=x*y*(qs[0]if i&j&1 else 1)*(qs[1]if i&j&2 else 1)
    return tuple(out)


def controls():
    old,bound=base.rotation.bq.trace_types(6)
    new,newbound=trace_types(6,(2,3),(2,3))
    need(old==new and bound==newbound,'complete old biquadratic trace-domain crosscheck')
    # Direct cyclotomic relative traces, independent of the closed formula.
    x=s.Symbol('x');checked=0
    for order in(12,13,24,26,52,156):
        f=s.Poly(s.cyclotomic_poly(order,x),x,domain=s.QQ)
        units=[u for u in range(order)if math.gcd(u,order)==1]
        rad=(3,13,39);conductors=list(map(disc,rad))
        present=[(q,D)for q,D in zip(rad,conductors)if order%D==0]
        H=[u for u in units if all(s.kronecker_symbol(D,u)==1 for q,D in present)]
        basis=[s.Poly(1,x,domain=s.QQ)]
        for q,D in zip(rad,conductors):
            if order%D:basis.append(s.Poly(0,x,domain=s.QQ));continue
            gauss=sum(int(s.kronecker_symbol(D,v))*x**((order//D*v)%order)for v in range(D))
            basis.append(s.Poly(gauss/s.Integer(math.isqrt(D//q)),x,domain=s.QQ).rem(f))
        predicted,_=trace_types(6,orders=[order]);seen=set()
        for u in units:
            direct=[]
            for k in range(1,7):
                p=s.Poly(sum(x**((u*h*k)%order)for h in H)/s.Integer(len(H)),x,domain=s.QQ).rem(f)
                direct.append(p)
            matches=[]
            for at,typ in enumerate(predicted):
                polys=[sum((s.Rational(z.numerator,z.denominator)*v for z,v in zip(row,basis)),s.Poly(0,x,domain=s.QQ)).rem(f)for row in typ]
                if polys==direct:matches.append(at)
            need(bool(matches),'direct cyclotomic relative trace control');seen.update(matches);checked+=1
        need(seen==set(range(len(predicted))),'all closed-form cyclotomic trace types realized')
    # Actual center Z(Vec(C2)): labels (flux, character), twists +/-1.
    labels=list(itertools.product(range(2),repeat=2))
    S=s.Matrix([[(-1)**(g*ep+h*e)for h,ep in labels]for g,e in labels])
    T=s.diag(*[(-1)**(g*e)for g,e in labels])
    need(S*T*S==2*T.inv()*S*T.inv(),'actual pointed-center STS control')
    allowed,_=trace_types(6)
    for theta in(1,-1):
        need(tuple((F(theta**k),F(0),F(0),F(0))for k in range(1,7))in allowed,'actual pointed-center twist types')
    for n in range(2,7):
        dimension=int(n%2==0)
        for r in s.divisors(n):
            if r==n:continue
            power=n//int(r)
            central=sum((-1)**(g*e*power)for g,e in labels if g==int(r)%2)
            need(central==2*dimension,'actual pointed-center joint tensor rotation control')
    return {'old_biquadratic_height':6,'old_biquadratic_order_bound':bound,'old_biquadratic_trace_types':len(old),
            'direct_cyclotomic_orders':[12,13,24,26,52,156],'direct_root_orbits_checked':checked,
            'actual_known_center_control':'Z(Vec(C2)): full STS and all joint tensor rotations through height6'}


def setup():
    R,a,chars,cols,Q,H,meta=base.source();K=a['K'];roots=[]
    for q in(3,13):
        rr=discover_roots(s.Poly(base.c.w.t**2-q,base.c.w.t),K)
        need(rr is not None and len(rr)==2,'required quadratic subfield')
        roots.append(next(z for z in rr if a['embedding'].sign(z)>0))
    basis=[K.one,roots[0],roots[1],roots[0]*roots[1]];V=s.Matrix.hstack(*(vector(z,4)for z in basis));need(V.det()!=0,'full biquadratic basis')
    inverse=V.inv();coords=lambda z:tuple(F(str(v))for v in inverse*vector(z,4))
    ds=list(map(coords,a['ds']));D=coords(a['D']);need(D==(F(39),F(0),F(9),F(0)),'global dimension in positive radical basis')
    norm=base.multiplication_matrix(a['D'],K,a['factor']).det();need(norm==468**2,'global dimension norm in quartic field')
    need(set(s.factorint(int(norm)))=={2,3,13},'complete twist prime support')
    high=[(v,coords(sum((K(x)*d for x,d in zip((0,)+v,a['ds'])),K.zero)))for v,z in H]
    return R,a,chars,cols,Q,high,basis,coords,ds,D


def build(data,counts,ep,height=6):
    R,a,chars,cols,Q,high,basis,coords,ds,D=data;K=a['K'];types,bound=trace_types(height)
    labels=[(v,z,ti)for v,z in high for ti in range(len(types))];nvars=len(labels);L=s.Matrix.hstack(*map(s.Matrix,cols));LL=L*L.T
    low=[tuple(sum((F(int(LL[i,j]))*ds[j][k]for j in range(8)),F(0))for k in range(4))for i in range(8)]
    need(low[0]==D,'induced-unit dimension identity');rows=[];rhs=[]
    for i,j in itertools.combinations_with_replacement(range(7),2):
        rows.append({k:F(v[i]*v[j])for k,(v,z,ti)in enumerate(labels)if v[i]*v[j]});rhs.append(F(int(Q[i+1,j+1])))
    moments=[[mul(z,tr)for tr in types[ti]]for v,z,ti in labels]
    for power in(1,2):
        for i in range(7):
            for k in range(4):
                rows.append({j:v[i]*moments[j][power-1][k]for j,(v,z,ti)in enumerate(labels)if v[i]*moments[j][power-1][k]})
                rhs.append(-low[i+1][k]+(ep[i]*D[k]if power==2 else 0))
    for obj in range(1,8):
        powers=[[1]+[0]*7]
        for order in range(1,height+1):powers.append([sum(powers[-1][i]*R[i][obj][j]for i in range(8))for j in range(8)])
        for order in range(3,height+1):
            divisors=[int(d)for d in s.divisors(order)if d<order]
            rot,_=trace_types(height,orders=s.divisors(order),powers=divisors);start=nvars;nvars+=len(rot)
            rows.append({start+j:F(1)for j in range(len(rot))});rhs.append(F(powers[order][0]))
            for at,r in enumerate(divisors):
                power=order//r
                for k in range(4):
                    row={};constant=sum((F(powers[r][i])*low[i][k]for i in range(8)),F(0))
                    for j,(v,z,ti)in enumerate(labels):
                        coeff=sum(powers[r][i]*v[i-1]for i in range(1,8));entry=-coeff*moments[j][power-1][k]
                        if entry:row[j]=entry
                    for j,tr in enumerate(rot):
                        entry=mul(D,tr[at])[k]
                        if entry:row[start+j]=entry
                    rows.append(row);rhs.append(constant)
    # Full STS is valid over this real splitting field.
    assignments=base.modular.assignments(a,chars,cols)
    need(assignments==[(0,1,2,3,4),(0,1,3,2,4)],'complete S assignments')
    need(cols[2]==cols[3],'equal-column assignments give identical STS equations')
    traces=[sum((K(s.Rational(x.numerator,x.denominator))*v for x,v in zip(typ[0],basis)),K.zero)for typ in types]
    lowvalues=[[base.modular.value(ch,v,K)for ch in chars]for v in cols]
    highvalues=[[base.modular.value(ch,(0,)+v,K)for ch in chars]for v,z in high]
    for E,F_ in itertools.combinations_with_replacement(range(5),2):
        target=a['codegrees'][F_]*K(a['multiplicities'][F_])*base.modular.value(chars[E],cols[F_],K)-sum((v[E]*v[F_]for v in lowvalues),K.zero)
        coeff=[coords(v[E]*v[F_]*tr)for v in highvalues for tr in traces];target=coords(target)
        for k in range(4):rows.append({j:v[k]for j,v in enumerate(coeff)if v[k]});rhs.append(target[k])
    for i,m in enumerate(counts):rows.append({i*len(types)+j:F(1)for j in range(len(types))});rhs.append(F(m))
    A=[];b=[]
    for row,const in zip(rows,rhs):
        den=math.lcm(const.denominator,*(x.denominator for x in row.values()));dense=[0]*nvars
        for j,x in row.items():dense[j]=int(x*den)
        const=int(const*den);g=math.gcd(const,*dense)or 1;A.append([x//g for x in dense]);b.append(const//g)
    return A,b,{'height':height,'order_bound':int(bound),'trace_types':len(types),'variables':nvars,'rows':len(A),
        'both_symmetric_character_assignments_identical':True,'fixed_high_multiplicities':list(counts),
        'indicators':list(ep),'matrix_sha256':hashlib.sha256(json.dumps(A,separators=(',',':')).encode()).hexdigest(),
        'rhs_sha256':hashlib.sha256(json.dumps(b,separators=(',',':')).encode()).hexdigest()}


def run(write):
    control=controls();data=setup();prior=json.loads((HERE/'results.json').read_text());patterns=prior['all_tests_survivors'];eps=base.rotation.h.indicator_choices(data[0]);need(len(patterns)==12 and len(eps)==4,'complete fixed-pattern/indicator domain')
    path=HERE/'joint_rotation.json';saved=None if write else json.loads(path.read_text());cases=[];dual_pool=[];matrix=None
    for index in patterns:
        counts=prior['patterns'][index]['multiplicities']
        for ep in eps:
            A,b,meta=build(data,counts,ep)
            if matrix is None:matrix=meta['matrix_sha256']
            need(meta['matrix_sha256']==matrix,'common fixed-pattern matrix')
            if write:
                decision=None
                for old in dual_pool:
                    try:lp.verify(A,b,old);decision=old;break
                    except Exception:pass
                if decision is None:decision=lp.decide(A,b)
                if decision['status']=='exact_infeasible_relaxation'and decision not in dual_pool:dual_pool.append(decision)
            else:
                need(saved['cases'][len(cases)]['metadata']==meta,'exact fixed-pattern system');decision=saved['cases'][len(cases)]['decision']
            lp.verify(A,b,decision);cases.append({'pattern_index':index,'metadata':meta,'decision':decision})
            print('R455',index,ep,decision['status'],flush=True)
    result={'id':'R8_3_455','controls':control,'source_integer_receipt_sha256':hashlib.sha256((HERE/'results.json').read_bytes()).hexdigest(),
        'field_radical_basis':[1,3,13,39],'cases':cases,
        'all_patterns_excluded':all(c['decision']['status']=='exact_infeasible_relaxation'for c in cases),
        'scope':'complete height-six necessary relaxation on all12 integer/cubic/spectrum/parity patterns and4indicator branches; no categorical construction'}
    if write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==saved,'complete fixed-pattern joint-rotation replay')
    print('PASS R455 fixed-pattern joint rotation; all excluded=',result['all_patterns_excluded'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args();run(args.write)
