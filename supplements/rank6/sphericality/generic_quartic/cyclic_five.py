from itertools import permutations
from math import isqrt
from pathlib import Path
import sys
import json
from verify_quartic_fields import X,SCALE,sp,round_two,rows,solve,gap

def candidates():
    found=set()
    for a in range(5,39):
        for n in sp.divisors(a**4):
            if n*256>a**4: continue
            f=sp.factorint(n)
            sb=int(sp.prod(p**((2*e+3)//4) for p,e in f.items()))
            sc=int(sp.prod(p**((3*e+3)//4) for p,e in f.items()))
            for v in range(a%2,isqrt(a*a//5)+1,2):
                if (a*a-5*v*v)%4: continue
                z=(a*a-5*v*v)//4
                for b in range(sb,3*a*a//8+1,sb):
                    r=b-z
                    if r<=0: continue
                    # Solving the integer resolvent identity in the coefficient C.
                    t=r**3-b*r*r-4*n*r-(a*a-4*b)*n
                    dd=(a*r)**2+4*t
                    if dd<0: continue
                    ss=isqrt(dd)
                    if ss*ss!=dd: continue
                    for rr in set((a*r+ss,a*r-ss)):
                        if rr%2: continue
                        c=rr//2
                        if c<=0 or c%sc or 16*c>a**3 or 9*a*c>4*b*b: continue
                        if min(b-3*a+6,c-2*b+3*a-4,n-c+b-a+1)>0:continue
                        pol=sp.Poly(X**4-a*X**3+b*X**2-c*X+n,X)
                        disc=int(pol.discriminant())
                        if disc<=0 or disc%5 or 5*isqrt(disc//5)**2!=disc: continue
                        if not pol.is_irreducible or pol.count_roots(0,1)==0 or pol.count_roots(0,sp.oo)!=4:continue
                        gal,_=pol.galois_group()
                        if not gal.is_cyclic:continue
                        # Test the two trace ranges without requiring maximal-order computation.
                        if a<=22:found.add((a,b,c,int(n),15))
                        if disc%8000==0 and isqrt(disc//8000)**2==disc//8000:
                            found.add((a,b,c,int(n),40))
    return sorted(found)

if __name__=='__main__':
    pp=candidates()
    from collections import Counter
    assert Counter(t[-1] for t in pp)=={40:62,15:53}
    wfile=Path(__file__).with_name('cyclic_five_duals.json')
    generate='--generate' in sys.argv
    weights=[] if generate else json.loads(wfile.read_text())
    gaps=[]
    for coeff in pp:
        if coeff[:4] in ((7,14,8,1),(8,19,12,1)):
            # The former is treated by c15_lattice.py and the latter generates the excluded field of conductor 20.
            continue
        for mode in ('gold-long','gold-short'):
            for order in ((0,1,2,3),(0,1,3,2),(0,2,1,3)):
                R=rows(coeff[:4],(5,coeff[-1]),order,mode)
                if generate:weights.append(solve(R))
                gaps.append(gap(R,weights[len(gaps)]))
    for order in ((0,1,2,3),(0,1,3,2),(0,2,1,3)):
        R=rows((7,14,8,1),(5,15),order,'gold-short')
        if generate:weights.append(solve(R))
        gaps.append(gap(R,weights[len(gaps)]))
    assert len(gaps)==len(weights)==681 and min(gaps)>0
    if generate:wfile.write_text(json.dumps(weights,separators=(',',':'))+'\n')
    print(len(gaps),'positive cyclic separation certificates. Smallest integral margin',min(gaps))
