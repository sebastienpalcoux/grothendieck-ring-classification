#!/usr/bin/env python3
"""Independent two-functional audit of the R928 pattern-40 obstruction.

Character-table validity is checked separately by verify_level24_inputs.py.
No character reconstruction, optimization, or spectrum search is used here.
"""
from collections import Counter
from itertools import product, permutations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'r155' / 'level24'

def need(value, message):
    if not value:
        raise ValueError(message)

tables = [json.loads((SOURCE / f'sl2_{q}.json').read_text()) for q in (8, 3)]
# Actual twists, in exponents modulo 96. Removing both invariant blocks
# happens before dividing by gamma=zeta24 (exponent 4 modulo96).
full = Counter({0:4, 24:1, 64:2, 16:2, 48:1, 52:4,
                84:2, 40:2, 72:1, 9:1, 33:1, 57:1, 81:1})
block6 = Counter([0,84,9,33,57,81])
block2 = Counter([0,24])
need(sum(full.values()) == 23, 'full branch rank')
remainder = full.copy()
for block in (block6, block2):
    for k, v in block.items():
        remainder[k] -= v
        need(remainder[k] >= 0, 'invariant-block spectrum is contained')
target = Counter()
for k, v in remainder.items():
    if v:
        exponent = (k-4) % 96
        need(exponent % 4 == 0, 'complementary normalized T has order dividing24')
        target[exponent // 4] += v
need(target == Counter({3:2,9:2,11:1,12:4,15:2,17:1,20:1,23:2}),
     'independently reconstructed target')
need(full[52] == 4 and sum(v for k,v in full.items() if (k-4)%96==48)==4,
     'full T=-1 eigenspace is exactly four coordinates')

# Reconstruct all CRT T spectra directly, with neither central-sign filter
# nor a selection of only self-dual representations.
eligible = {}
all_degree_squares = 0
for i,a in enumerate(tables[0]['irreps']):
    for j,b in enumerate(tables[1]['irreps']):
        spectrum = Counter()
        for ka,ma in enumerate(a['T_multiplicities']):
            for kb,mb in enumerate(b['T_multiplicities']):
                if ma*mb:
                    spectrum[(3*ka+8*kb)%24] += ma*mb
        degree = a['degree']*b['degree']
        need(sum(spectrum.values()) == degree, 'CRT degree')
        all_degree_squares += degree**2
        if all(n <= target[e] for e,n in spectrum.items()):
            eligible[i,j] = spectrum
need(all_degree_squares == 9216, 'all210 irreducible degree squares')
need(len(eligible) == 12, 'complete compatible spectrum list')

# Two elementary nonnegative certificates replace enumeration of decompositions.
def L1(v):
    return 2*v[20]-v[23]-v[11]+v[17]
def L2(v):
    return 2*v[12]-v[3]-v[15]+v[9]
for label,v in eligible.items():
    need(L1(v) == 2*int(label in ((1,1),(1,5))), 'first linear certificate')
    need(L2(v) == 2*int(label in ((1,2),(1,5))), 'second linear certificate')
need(L1(target)==0 and L2(target)==6, 'target functional values')
need(eligible[1,2] == Counter({12:1}), 'one-dimensional sign T')
# In a one-dimensional SL2 representation, (ST)^3=S^2 with T=-1
# implies S=-1. Hence the sign Galois word below acts by +1.

# Independent concrete kernel check: no SL2(Z32) character table is needed.
def mul(x,y,n):
    a,b,c,d=x; e,f,g,h=y
    return ((a*e+b*g)%n,(a*f+b*h)%n,(c*e+d*g)%n,(c*f+d*h)%n)
def inv(x,n):
    a,b,c,d=x
    return (d%n,-b%n,-c%n,a%n)
def power(x,k,n):
    y=(1,0,0,1)
    for _ in range(k):
        y=mul(y,x,n)
    return y
u=power((1,24,0,1),3,32)
need(u==(1,8,0,1), 'cube of T24')
conjugates=[mul(mul(g,u,32),inv(g,32),32)
            for g in ((1,0,0,1),(0,31,1,0),(1,0,1,1))]
span=set()
for exponents in product(range(4),repeat=3):
    x=(1,0,0,1)
    for g,k in zip(conjugates,exponents):
        x=mul(x,power(g,k,32),32)
    span.add(x)
kernel={(1+8*a,8*b,8*c,(1-8*a)%32) for a,b,c in product(range(4),repeat=3)}
need(len(span)==64 and span==kernel, 'normal conjugates generate reduction kernel')
need(all((a*d-b*c)%32==1 for a,b,c,d in kernel), 'kernel determinants')

# G5 = t5 S t77 S t5 S^-1, on S=t=-1.
need(5*77 % 96 == 1, 'inverse exponent')
need((-1)**(5+1+77+1+5-1)==1, 'G5 acts trivially on sign copies')
# On four coordinates, the fixed dimension of -P is the number of even cycles.
maximum=0
for p in permutations(range(4)):
    unused=set(range(4)); even=0
    while unused:
        start=min(unused); x=start; length=0
        while x in unused:
            unused.remove(x); length+=1; x=p[x]
        even += (length%2==0)
    maximum=max(maximum,even)
need(maximum==2, 'negative-permutation fixed-space bound')
receipt={
    'status':'PASS',
    'scope':'R928 pattern40 only; full ring and pattern186 remain unresolved',
    'independent_target_rank':15,
    'compatible_irreps_both_central_signs':12,
    'linear_certificates':2,
    'forced_sign_copies':3,
    'kernel_order_and_normal_span':64,
    'negative_permutation_fixed_space_maximum':maximum,
    'table_hashes':{f'sl2_{q}.json':hashlib.sha256((SOURCE/f'sl2_{q}.json').read_bytes()).hexdigest()
                    for q in (8,3)},
    'optimizer_used':False,
    'representation_decomposition_search_used':False,
}
(HERE/'audit_r928_pattern40.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
