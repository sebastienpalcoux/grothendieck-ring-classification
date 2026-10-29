"""Independent finite indicator audit for all 48 pattern-186 phase allocations.

The larger phase-exhaustion theorem is audited separately. This script performs
no search: it checks the saved list using Q(zeta_288), with SymPy supplying
the minimal polynomial rather than the researcher's zeta_1728 helper.
"""
from pathlib import Path
from collections import defaultdict,Counter
import json,math
import sympy as s

P=Path(__file__).resolve().parents[1]/'r928'
data=json.loads((P/'vafa_probe.json').read_text())['survivors']
p=next(p for p in json.loads((P/'prior/spectral_reduction.json').read_text())['patterns'] if p['pattern']==186)
N=288;x=s.symbols('x');phi=s.Poly(s.cyclotomic_poly(N,x),x);degree=phi.degree()
assert degree==96
roots=[]
for k in range(N):
    q=s.rem(s.Poly(x**k,x),phi)
    roots.append({i:int(c) for (i,),c in q.terms()})
def add(*terms):
    z=defaultdict(int)
    for t in terms:
        for k,c in t.items():z[k]+=c
    return {k:c for k,c in z.items() if c}
def scale(c,z):return {k:c*a for k,a in z.items() if c*a}
def mul(a,b):
    z=defaultdict(int)
    for i,ci in a.items():
        for j,cj in b.items():
            for k,ck in roots[(i+j)%N].items():z[k]+=ci*cj*ck
    return {k:c for k,c in z.items() if c}
def gal(a,z):return add(*(scale(c,roots[(a*k)%N]) for k,c in z.items()))
sqrt2=add(roots[N//8],roots[-N//8]);sqrt3=add(roots[N//12],roots[-N//12]);sqrt6=mul(sqrt2,sqrt3)
basis=[roots[0],sqrt2,sqrt3,sqrt6]
ds=[add(*(scale(int(c),z) for c,z in zip(v,basis))) for v in p['dimensions']]
D=add(*(scale(c,z) for c,z in zip([144,96,80,56],basis)));D2=mul(D,D)
W=p['N_W'];terms=[(i,j,scale(2*W[i][j],mul(ds[i],ds[j]))) for i in range(20) for j in range(20) if W[i][j]]
def numerator(phase,m):return add(*(mul(z,roots[(m*(phase[i]-phase[j]))%N]) for i,j,z in terms))
results=[];counts=Counter()
for record in data:
    t,k,A,B,H=record
    original=[0]*4+[432,12*t]+A+[12*b for b in B]+H+[k,12*t]
    assert len(original)==20 and all(q%6==0 for q in original)
    phase=[q//6 for q in original]
    z2=numerator(phase,2)
    status='plus1' if z2==D2 else ('minus1' if z2==scale(-1,D2) else 'zero' if not z2 else 'other')
    counts[status]+=1
    if status!='plus1':continue
    z4=numerator(phase,4)
    # Any a=1 mod4 fixes i; non-invariance of z4/D2 disproves Q(i)-membership.
    witness=None
    for a in range(1,N,4):
        if math.gcd(a,N)>1:continue
        difference=add(mul(gal(a,z4),D2),scale(-1,mul(z4,gal(a,D2))))
        if difference:
            witness={'automorphism_exponent':a,'nonzero_difference_coefficient':list(sorted(difference.items()))[0]}
            break
    results.append({'phase_allocation':record,'nu2':'1','nu4_outside_Q_i':witness is not None,'galois_witness':witness})
assert len(data)==48
assert counts['plus1']==12
result={'field':'Q(zeta_288), Phi generated independently by SymPy','saved_phase_allocations':len(data),'nu2_counts':dict(counts),'nu4_checks':results,'all_twelve_nu4_fail':all(r['nu4_outside_Q_i'] for r in results),'scope':'Exact indicator values checked on all saved 48 allocations; global exclusion additionally needs the separate exhaustive phase-reduction theorem.'}
(Path(__file__).parent/'audit_r928_higher_indicators.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'saved_phase_allocations':len(data),'nu2_counts':dict(counts),'all_twelve_nu4_fail':result['all_twelve_nu4_fail'],'failing_count':sum(r['nu4_outside_Q_i'] for r in results),'automorphisms':[r['galois_witness']['automorphism_exponent'] if r['galois_witness'] else None for r in results]},indent=2))
