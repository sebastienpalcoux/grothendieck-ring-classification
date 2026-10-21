#!/usr/bin/env python3
"""Reconstruct Rep(PSL(2,11)) from all 660 matrices and its class algebra.

Recovery reconstruction after the workspace reset: no prior certificate is
assumed. The proposed character values are certified against the actual
class algebra and character orthogonality using exact rational arithmetic.
Default replays certificate.json; --write explicitly generates it.
"""
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
TARGET='R8_3_724'
SOURCE_SHA='d0424cf6cfd9e8e99dfdddeabc3a84aa014262259721e3ddc6b466b2772b0ee5'

def require(condition,message):
    if not condition:
        raise ValueError(message)

def fingerprint(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()

def canonical(g):
    g=tuple(x%11 for x in g)
    return min(g,tuple(-x%11 for x in g))

def multiply(a,b):
    x,y,z,w=a
    p,q,r,s=b
    return canonical((x*p+y*r,x*q+y*s,z*p+w*r,z*q+w*s))

def inverse(g):
    a,b,c,d=g
    return canonical((d,-b,-c,a))

# Q(sqrt(5),sqrt(-11)), basis 1,sqrt(5),sqrt(-11),sqrt(-55).
def q(a=0,b=0,c=0,d=0):
    return tuple(map(F,(a,b,c,d)))
ZERO=q()
ONE=q(1)
def add(a,b):
    return tuple(x+y for x,y in zip(a,b))
def scale(a,k):
    return tuple(x*k for x in a)
def product(a,b):
    out=[F(0)]*4
    for i,j in itertools.product(range(4),repeat=2):
        common=i&j
        coefficient=(5 if common&1 else 1)*(-11 if common&2 else 1)
        out[i^j]+=a[i]*b[j]*coefficient
    return tuple(out)
def conjugate(a):
    return (a[0],a[1],-a[2],-a[3])
def total(items):
    result=ZERO
    for item in items:
        result=add(result,item)
    return result
def encoded(a):
    return [str(x) for x in a]

def construct():
    elements=sorted({canonical(g) for g in itertools.product(range(11),repeat=4)
                     if (g[0]*g[3]-g[1]*g[2])%11==1})
    require(len(elements)==660,'wrong PSL2(11) order')
    identity=(1,0,0,1)
    require(all(multiply(g,inverse(g))==identity for g in elements),'inverse check failed')
    def order(g):
        z=identity
        for n in range(1,661):
            z=multiply(z,g)
            if z==identity:
                return n
        raise ValueError('group element order missing')
    remaining=set(elements)
    classes=[]
    while remaining:
        x=min(remaining)
        orbit={multiply(multiply(g,x),inverse(g)) for g in elements}
        require(orbit<=remaining,'conjugacy classes overlap')
        classes.append(sorted(orbit))
        remaining-=orbit
    classes.sort(key=lambda C:(order(C[0]),len(C),C[0]))
    require(len(classes)==8,'wrong class count')
    sizes=list(map(len,classes))
    orders=[order(C[0]) for C in classes]
    require(orders==[1,2,3,5,5,6,11,11],'unexpected conjugacy class orders')
    require(sizes==[1,55,110,132,132,110,60,60],'unexpected conjugacy class sizes')
    location={g:i for i,C in enumerate(classes) for g in C}
    algebra=[[[0]*8 for _ in range(8)] for _ in range(8)]
    for i,j in itertools.product(range(8),repeat=2):
        counts=[0]*8
        for a in classes[i]:
            for b in classes[j]:
                counts[location[multiply(a,b)]]+=1
        require(all(counts[k]%sizes[k]==0 for k in range(8)),'nonintegral class product')
        algebra[i][j]=[counts[k]//sizes[k] for k in range(8)]
    aa=q(F(-1,2),0,F(1,2))
    ab=conjugate(aa)
    ca=q(F(-1,2),F(1,2))
    cb=q(F(-1,2),F(-1,2))
    chars=[list(map(q,[1,1,1,1,1,1,1,1])),
           list(map(q,[5,1,-1,0,0,1]))+[aa,ab],
           list(map(q,[5,1,-1,0,0,1]))+[ab,aa],
           list(map(q,[10,-2,1,0,0,1,-1,-1])),
           list(map(q,[10,2,1,0,0,-1,-1,-1])),
           list(map(q,[11,-1,-1,1,1,-1,0,0])),
           [q(12),ZERO,ZERO,ca,cb,ZERO,ONE,ONE],
           [q(12),ZERO,ZERO,cb,ca,ZERO,ONE,ONE]]
    degrees=[int(row[0][0]) for row in chars]
    # A class-algebra character must send each K_i to |C_i| chi(C_i)/chi(1).
    # Its multiplicative identities certify the candidate rows against this
    # independently enumerated group. Orthogonality fixes the positive degrees.
    for row,d in zip(chars,degrees):
        central=[scale(row[i],F(sizes[i],d)) for i in range(8)]
        require(central[0]==ONE,'central character is not unital')
        for i,j in itertools.product(range(8),repeat=2):
            require(product(central[i],central[j])==
                    total(scale(central[k],algebra[i][j][k]) for k in range(8)),
                    f'candidate degree {d} is not a central character at ({i},{j}): {row}')
    for i,j in itertools.product(range(8),repeat=2):
        inner=total(scale(product(chars[i][c],conjugate(chars[j][c])),F(sizes[c],660))
                    for c in range(8))
        require(inner==q(int(i==j)),'exact character orthogonality failed')
    require(sum(d*d for d in degrees)==660,'sum of character degree squares failed')
    tensor=[[[0]*8 for _ in range(8)] for _ in range(8)]
    for i,j,k in itertools.product(range(8),repeat=3):
        inner=total(scale(product(product(chars[i][c],chars[j][c]),conjugate(chars[k][c])),
                          F(sizes[c],660)) for c in range(8))
        require(inner[1:]==(0,0,0) and inner[0].denominator==1 and inner[0]>=0,
                'character product is not a nonnegative integer')
        tensor[i][j][k]=int(inner[0])
    require(max(x for plane in tensor for row in plane for x in row)==3,'wrong maximum multiplicity')
    require(all(sum(tensor[i][j][k]*degrees[k] for k in range(8))==degrees[i]*degrees[j]
                for i,j in itertools.product(range(8),repeat=2)),'dimension character failed')
    data={'group':'SL(2,F11)/{+I,-I}','group_order':660,
          'group_elements_sha256':fingerprint(elements),'conjugacy_class_orders':orders,
          'conjugacy_class_sizes':sizes,'conjugacy_class_representatives':[C[0] for C in classes],
          'class_algebra_tensor':algebra,'character_degrees':degrees,
          'character_field_basis':['1','sqrt(5)','sqrt(-11)','sqrt(-55)'],
          'character_table':[[encoded(a) for a in row] for row in chars],
          'verified_central_character_identities':512,'verified_character_inner_products':64,
          'tensor':tensor,'tensor_sha256':fingerprint(tensor)}
    return tensor,data

def reconstructed_model():
    tensor,data=construct()
    return {'model':'Rep(PSL(2,11))',
            'reference':'explicit matrix-group class algebra and exact character certification',
            'tensor':tensor,'construction':data}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    tensor,data=construct()
    census=json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())
    source=next(r for r in census if r['id']==TARGET)
    require(fingerprint(source['tensor'])==source['tensor_sha256']==SOURCE_SHA,'source hash mismatch')
    mapping=None
    for p in itertools.permutations(range(1,8)):
        candidate=(0,)+p
        if all(tensor[i][j][k]==source['tensor'][candidate[i]][candidate[j]][candidate[k]]
               for i,j,k in itertools.product(range(8),repeat=3)):
            mapping=list(candidate)
            break
    require(mapping is not None,'no exact based tensor isomorphism')
    data.update({'id':TARGET,'model':'Rep(PSL(2,11))',
                 'reference':'explicit matrix-group class algebra and exact character certification',
                 'scope':'unitary representation category of a finite group',
                 'source_tensor_sha256':SOURCE_SHA,'source_line':source['source_line'],
                 'model_to_source_basis_map':mapping,
                 'source_to_model_basis_map':[mapping.index(i) for i in range(8)],
                 'verified_fusion_coefficients':512,
                 'recovery_note':'fresh exact reconstruction; no previous certificate assumed'})
    path=HERE/'certificate.json'
    if args.write:
        path.write_text(json.dumps(data,indent=2)+'\n')
    else:
        require(json.loads(path.read_text())==json.loads(json.dumps(data)),'saved certificate does not replay')
    print(json.dumps({'id':TARGET,'group_order':660,'coefficients_verified':512,
                      'model_to_source_basis_map':mapping,'mode':'write' if args.write else 'compare'}))

if __name__=='__main__':
    main()
