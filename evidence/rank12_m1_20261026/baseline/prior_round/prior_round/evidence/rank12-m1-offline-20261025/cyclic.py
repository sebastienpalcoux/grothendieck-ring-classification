"""Established cyclic-isotypic integrality, all eligible invertibles/triples."""
from pathlib import Path
import json,math,sys,time
import sympy as s
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/work/rank11'))
from common import require,sha
t=s.Symbol('t')

def perron_factor(R,z):
    ps=s.Matrix(R[z]).charpoly(t).as_poly()
    fs=ps.factor_list()[1]
    roots=ps.intervals(eps=s.Rational(1,10**12));require(bool(roots),'positive root exists')
    lo,hi=roots[-1][0]
    for f,e in fs:
        if (lo==hi and f.eval(lo)==0)or(lo<hi and f.count_roots(lo,hi)==1):return f
    raise ValueError('missing Perron factor')

def scan(R):
    n=len(R);unit=lambda a:[int(i==a)for i in range(n)]
    du=[next(j for j in range(n)if R[i][j][0])for i in range(n)]
    G=[i for i in range(1,n)if sum(R[i][du[i]])==1];cache={};tested=0
    for g in G:
        order=1;h=g
        while h:
            h=R[h][g].index(1);order+=1
        L=[x for x in range(n)if R[g][x]==unit(x)]
        Q=[y for y in range(n)if R[y][g]==unit(y)]
        for z in set(L)&set(Q):
            pair=next(((x,y)for x in L for y in Q if R[x][y][z]),None)
            if pair is None:continue
            tested+=1
            if z not in cache:cache[z]=perron_factor(R,z)
            f=cache[z];q=order//math.gcd(order,R[pair[0]][pair[1]][z])
            h=s.Poly(f.as_expr().subs(t,q*t)/q**f.degree(),t)
            if any(a.q!=1 for a in h.all_coeffs()):
                return dict(kind='cyclic_isotypic_integrality',g=g,order=order,X=pair[0],Y=pair[1],Z=z,multiplicity=R[pair[0]][pair[1]][z],dimension_polynomial=list(map(str,f.all_coeffs())),normalized_dimension_polynomial=list(map(str,h.all_coeffs())),scope='general_complex_fusion_category'),tested
    return None,tested

def main():
    start=time.monotonic();rows=[]
    for rid,R in json.loads((ROOT/'tensors.json').read_text()).items():
        c,k=scan(R);rows.append(dict(id=rid,tensor_sha256=sha(R),certificate=c,eligible_tests_before_first_witness=k))
    (ROOT/'cyclic.json').write_text(json.dumps(dict(records=rows,elapsed_seconds=time.monotonic()-start),indent=2)+'\n')
    print('Cyclic exact exclusions',sum(r['certificate']is not None for r in rows),'seconds',time.monotonic()-start)

if __name__=='__main__':main()
