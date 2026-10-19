"""General cyclic-stabilizer bimodule divisibility, exact integer witnesses.

Categorical input: manuscripts/rank7/papers/cyclic_module_divisibility.tex,
Proposition 'A cyclic-stabilizer divisibility obstruction'.
"""
import argparse,json,time
from pathlib import Path
import sympy as s

t=s.Symbol('t')
HERE=Path(__file__).resolve().parent

def require(value,why):
    if not value:raise ValueError(why)

def order(R,g):
    n=len(R);a=0
    for k in range(1,n+1):
        v=R[a][g]
        if sum(v)!=1:return None
        a=v.index(1)
        if a==0:return k
    return None

def perron_factor(R,z):
    P=s.Matrix(R[z]).charpoly(t).as_poly()
    fs=P.factor_list()[1]; candidates=[]
    for f,m in fs:
        intervals=f.intervals(eps=s.Rational(1,10**12))
        if intervals:candidates.append((f,intervals[-1][0]))
    require(candidates,'Perron root missing')
    f,(lo,hi)=max(candidates,key=lambda a:a[1][0])
    require(lo>0,'nonpositive Perron root')
    require(all(other==f or bound[1]<lo for other,bound in candidates),'Perron factor not separated')
    return f

def certificate(R):
    n=len(R)
    for g in range(1,n):
        p=order(R,g)
        if p is None or not s.isprime(p):continue
        left=[i for i in range(n) if R[g][i]==[int(j==i) for j in range(n)]]
        right=[i for i in range(n) if R[i][g]==[int(j==i) for j in range(n)]]
        for z in sorted(set(left)&set(right)):
            hit=next(((x,y) for x in left for y in right if R[x][y][z]%p),None)
            if hit is None:continue
            f=perron_factor(R,z)
            q=s.Poly(f.as_expr().subs(t,p*t)/p**f.degree(),t)
            if all(c.q==1 for c in q.all_coeffs()):continue
            return {'kind':'cyclic_stabilizer_divisibility','g':g,'prime':int(p),
                    'X':hit[0],'Y':hit[1],'Z':z,'multiplicity':R[hit[0]][hit[1]][z],
                    'dimension_polynomial':list(map(str,f.all_coeffs())),
                    'quotient_polynomial':list(map(str,q.all_coeffs()))}
    return None

def verify(R,c):
    n=len(R);g=c['g'];p=c['prime'];x,y,z=(c[k] for k in ('X','Y','Z'))
    require(c['kind']=='cyclic_stabilizer_divisibility','kind')
    require(all(type(a) is int and 0<=a<n for a in (g,x,y,z)),'indices')
    require(type(p) is int and s.isprime(p) and order(R,g)==p,'prime subgroup')
    for a,left in ((x,True),(y,False),(z,True),(z,False)):
        require((R[g][a] if left else R[a][g])==[int(j==a) for j in range(n)],'fixed object')
    require(R[x][y][z]==c['multiplicity'] and R[x][y][z]%p!=0,'violated divisibility')
    f=perron_factor(R,z);q=s.Poly(f.as_expr().subs(t,p*t)/p**f.degree(),t)
    require(list(map(str,f.all_coeffs()))==c['dimension_polynomial'],'dimension minpoly')
    require(list(map(str,q.all_coeffs()))==c['quotient_polynomial'],'scaled minpoly')
    require(any(a.q!=1 for a in q.all_coeffs()),'algebraically integral quotient')
    return True

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('--output',default=str(HERE/'cyclic_divisibility_results.json'));args=ap.parse_args()
    rows=json.load(open(args.source));out=[];start=time.monotonic()
    for r in rows:
        c=certificate(r['tensor'])
        if c:
            verify(r['tensor'],c);out.append({'id':r['id'],'certificate':c,'scope':'general_complex'})
    result={'tested':len(rows),'excluded':len(out),'seconds':time.monotonic()-start,'certificates':out}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='certificates'},indent=2));print([r['id'] for r in out])

if __name__=='__main__':main()
