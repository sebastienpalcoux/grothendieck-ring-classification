"""Cyclic isotypic-summand integrality: general complex obstruction.

For a cyclic stabilizer of order n fixing X on the left, Y on the right,
and Z on both sides, gcd(n,N_XY^Z)*FPdim(Z)/n must be algebraically integral.
See CYCLIC_ISOTYPIC_PROOF.md. No pivotal or positivity assumption is used.
"""
import argparse,json,math,time
from pathlib import Path
import sympy as s
from cyclic_divisibility import order,perron_factor,require,t
HERE=Path(__file__).resolve().parent

def scaled_polynomial(f,n,m):
    denominator=n//math.gcd(n,m)
    return s.Poly(f.as_expr().subs(t,denominator*t)/denominator**f.degree(),t)

def certificate(R):
    rank=len(R)
    for g in range(1,rank):
        n=order(R,g)
        if n is None:continue
        left=[i for i in range(rank) if R[g][i]==[int(j==i) for j in range(rank)]]
        right=[i for i in range(rank) if R[i][g]==[int(j==i) for j in range(rank)]]
        for z in sorted(set(left)&set(right)):
            f=None
            for x in left:
                for y in right:
                    m=R[x][y][z]
                    if m%n==0:continue
                    if f is None:f=perron_factor(R,z)
                    q=scaled_polynomial(f,n,m)
                    if all(c.q==1 for c in q.all_coeffs()):continue
                    return {'kind':'cyclic_isotypic_integrality','g':g,'order':n,
                            'X':x,'Y':y,'Z':z,'multiplicity':m,'gcd':math.gcd(n,m),
                            'dimension_polynomial':list(map(str,f.all_coeffs())),
                            'normalized_dimension_polynomial':list(map(str,q.all_coeffs()))}
    return None

def verify(R,c):
    rank=len(R);g=c['g'];n=c['order'];x,y,z=(c[k] for k in ('X','Y','Z'));m=c['multiplicity']
    require(c['kind']=='cyclic_isotypic_integrality','kind')
    require(all(type(a) is int and 0<=a<rank for a in (g,x,y,z)),'indices')
    require(type(n) is int and n>1 and order(R,g)==n,'cyclic subgroup')
    for a,left in ((x,True),(y,False),(z,True),(z,False)):
        require((R[g][a] if left else R[a][g])==[int(j==a) for j in range(rank)],'fixed object')
    require(type(m) is int and R[x][y][z]==m and m>0,'fusion multiplicity')
    require(c['gcd']==math.gcd(n,m),'greatest common divisor')
    f=perron_factor(R,z);q=scaled_polynomial(f,n,m)
    require(list(map(str,f.all_coeffs()))==c['dimension_polynomial'],'dimension minpoly')
    require(list(map(str,q.all_coeffs()))==c['normalized_dimension_polynomial'],'normalized minpoly')
    require(any(a.q!=1 for a in q.all_coeffs()),'normalized dimension is algebraically integral')
    return True

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('--output',default=str(HERE/'cyclic_isotypic_results.json'));args=ap.parse_args()
    rows=json.load(open(args.source));out=[];start=time.monotonic()
    for row in rows:
        c=certificate(row['tensor'])
        if c:
            verify(row['tensor'],c);out.append({'id':row['id'],'certificate':c,'scope':'general_complex'})
    report={'tested':len(rows),'excluded':len(out),'seconds':time.monotonic()-start,'certificates':out}
    Path(args.output).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='certificates'},indent=2))

if __name__=='__main__':main()
