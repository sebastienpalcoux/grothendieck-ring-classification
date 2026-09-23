"""Exact, tensor-based rank-seven categorification pass on the pinned census.

Usage: python analyze.py --max-m 1 [--dnumber]
       python analyze.py --max-m 4 [--dnumber]
The source enumerates fusion rings; undecided entries remain undecided.
"""
import argparse
import ast
import collections
import concurrent.futures
import gzip
import hashlib
import itertools
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'data/rank7_tables.txt.gz'
SOURCE_SHA='6ddea4c66de7fbe077e9552e71e8cf95ec3fec5bbd30a615e68e2d8fcb9ae9c9'
KNOWN={1:43,2:319,3:1059,4:2780}
LOW=ROOT/'software'
sys.path.insert(0,str(LOW))
from prepare import key, flatten, dual
from subring_descent import certificate as lower_certificate
from check import verify as check_certificate

def read_source(max_m):
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA:
        raise ValueError('the pinned source census changed')
    rows=[];counts=collections.Counter();seen=set()
    with gzip.open(SOURCE,'rt') as f:
        for line_number,line in enumerate(f,1):
            if not line.strip():continue
            R=json.loads(line.replace('{','[').replace('}',']'))
            assert len(R)==7 and all(len(M)==7 and all(len(row)==7 for row in M) for M in R)
            m=max(flatten(R));counts[m]+=1
            if m>max_m:continue
            if line in seen:raise ValueError(f'duplicate source line {line_number}')
            seen.add(line)
            rows.append({'id':f'R7_{m}_{counts[m]}','rank':7,'multiplicity':m,'source_line':line_number,
                         'source_repository_commit':'b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726','tensor':R})
    if counts!=KNOWN:raise ValueError(f'count mismatch: {counts} != {KNOWN}')
    return rows

def su2(level,labels):
    return [[[int(c in range(abs(a-b), min(a+b,2*level-a-b)+1,2)) for c in labels]
             for b in labels] for a in labels]

def pointed_c7():
    return [[[int((i+j)%7==k) for k in range(7)] for j in range(7)] for i in range(7)]

def ty_c6():
    R=[[[0]*7 for _ in range(7)] for _ in range(7)]
    for i,j in itertools.product(range(6),repeat=2):R[i][j][(i+j)%6]=1
    for i in range(6):R[i][6][6]=R[6][i][6]=R[6][6][i]=1
    return R

def frobenius_prime(p,q,action):
    """Rep(Cp ⋊ Cq) via exact induction from the normal Cp."""
    if q+(p-1)//q!=7 or pow(action,q,p)!=1:
        raise ValueError('unsupported seven-class Frobenius group')
    seen=set();orbits=[]
    for a in range(1,p):
        if a not in seen:
            o=tuple(sorted({(a*pow(action,j,p))%p for j in range(q)}))
            seen.update(o);orbits.append(o)
    if len(orbits)!=(p-1)//q or any(len(o)!=q for o in orbits):
        raise ValueError('wrong normal subgroup character orbit count')
    lookup={v:i for i,o in enumerate(orbits) for v in o}
    R=[[[0]*7 for _ in range(7)] for _ in range(7)]
    for a,b in itertools.product(range(q),repeat=2):R[a][b][(a+b)%q]=1
    for g in range(q):
        for x in range(q,7):R[g][x][x]=R[x][g][x]=1
    for a,b in itertools.product(range(len(orbits)),repeat=2):
        coefficients=[0]*len(orbits);zeros=0
        for x,y in itertools.product(orbits[a],orbits[b]):
            z=(x+y)%p
            if z:coefficients[lookup[z]]+=1
            else:zeros+=1
        if zeros%q or any(v%q for v in coefficients):
            raise ValueError('normal subgroup orbit induction integrality failed')
        for g in range(q):R[q+a][q+b][g]=zeros//q
        for j,v in enumerate(coefficients):R[q+a][q+b][q+j]=v//q
    return R

def dihedral16():
    # Irr(D_16) has four linear characters and rho_1,rho_2,rho_3 of degree two.
    # Linear characters: (rotation sign, reflection sign); the latter fixes rho.
    R=[[[0]*7 for _ in range(7)] for _ in range(7)]
    for i,j in itertools.product(range(4),repeat=2):R[i][j][i^j]=1
    for lin in range(4):
        for t in range(1,4):
            u=4+(4-t if lin&1 else t)-1
            R[lin][3+t][u]=R[3+t][lin][u]=1
    for s,t in itertools.product(range(1,4),repeat=2):
        for z in (abs(s-t),s+t):
            if z==0:
                R[3+s][3+t][0]+=1;R[3+s][3+t][2]+=1
            elif z==4:
                R[3+s][3+t][1]+=1;R[3+s][3+t][3]+=1
            else:
                R[3+s][3+t][3+min(z,8-z)]+=1
    return R

def dihedral22():
    # Irr(D_22): 1, sign, and five two-dimensional representations of C_11.
    R=[[[0]*7 for _ in range(7)] for _ in range(7)]
    for i,j in itertools.product(range(2),repeat=2):R[i][j][i^j]=1
    for i in range(2):
        for a in range(2,7):R[i][a][a]=R[a][i][a]=1
    for a,b in itertools.product(range(1,6),repeat=2):
        for t in (a+b,abs(a-b)):
            t=min(t,11-t) if t else 0
            if t==0:R[a+1][b+1][0]+=1;R[a+1][b+1][1]+=1
            else:R[a+1][b+1][t+1]+=1
    return R

def semidihedral16():
    # Irr(C8 \rtimes_3 C2): four linears and three induced degree-two objects.
    R=[[[0]*7 for _ in range(7)] for _ in range(7)]
    for i,j in itertools.product(range(4),repeat=2):R[i][j][i^j]=1
    reps=[1,2,5]
    orbit={j%8:i+4 for i,v in enumerate(reps) for j in (v,3*v)}
    assert len(orbit)==6
    for i in range(4):
        for j,v in enumerate(reps):
            k=orbit[(v+4*(i&1))%8]
            R[i][j+4][k]=R[j+4][i][k]=1
    for i,a in enumerate(reps):
        for j,b in enumerate(reps):
            for t in ((a+b)%8,(a+3*b)%8):
                if t==0:R[i+4][j+4][0]+=1;R[i+4][j+4][2]+=1
                elif t==4:R[i+4][j+4][1]+=1;R[i+4][j+4][3]+=1
                else:R[i+4][j+4][orbit[t]]+=1
    return R

def metaplectic7():
    # Odd metaplectic SO(7)_2 category: 1,g,Y1,Y2,Y3,X+,X-.
    R=[[[0]*7 for _ in range(7)] for _ in range(7)]
    for i,j in itertools.product(range(2),repeat=2):R[i][j][i^j]=1
    for i in range(2):
        for j in range(2,5):R[i][j][j]=R[j][i][j]=1
    R[0][5][5]=R[5][0][5]=R[0][6][6]=R[6][0][6]=1
    R[1][5][6]=R[5][1][6]=R[1][6][5]=R[6][1][5]=1
    for a,b in itertools.product(range(1,4),repeat=2):
        for t in (a+b,abs(a-b)):
            t=min(t,7-t) if t else 0
            if t==0:R[a+1][b+1][0]+=1;R[a+1][b+1][1]+=1
            else:R[a+1][b+1][t+1]+=1
    for i in range(2,5):
        for j in (5,6):R[i][j][5]=R[i][j][6]=R[j][i][5]=R[j][i][6]=1
    for i in (5,6):
        for j in (5,6):
            R[i][j][0 if i==j else 1]=1
            for k in range(2,5):R[i][j][k]=1
    return R

def zest_su2_6():
    R=su2(6,list(range(7)))
    # A Z2-graded zest: odd × odd carries the invertible object of label 6.
    for a,b in itertools.product(range(7),repeat=2):
        if a%2 and b%2:R[a][b]=list(reversed(R[a][b]))
    return R

def partitions(n,largest=None):
    if not n:
        yield ();return
    for a in range(min(n,largest or n),0,-1):
        for tail in partitions(n-a,a):yield (a,)+tail

def symmetric_five():
    """Compute the seven irreducible character rows via border-strip removal."""
    from functools import lru_cache
    from math import factorial
    labels=list(partitions(5));classes=labels
    def ribbon(lam,nu):
        cells={(row,col) for row,count in enumerate(lam) for col in range(count)
               if col >= (nu[row] if row<len(nu) else 0)}
        if any({(i,j),(i+1,j),(i,j+1),(i+1,j+1)}<=cells for i,j in cells):return False
        seen={next(iter(cells))};q=list(seen)
        while q:
            i,j=q.pop()
            for pos in ((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
                if pos in cells and pos not in seen:seen.add(pos);q.append(pos)
        return len(seen)==len(cells)
    @lru_cache(None)
    def chi(lam,mu):
        if not mu:return int(not lam)
        out=0
        for nu in partitions(sum(lam)-mu[0]):
            if len(nu)>len(lam) or any(nu[i]>lam[i] for i in range(len(nu))):continue
            if not ribbon(lam,nu):continue
            rows=sum((lam[i] if i<len(lam) else 0)>(nu[i] if i<len(nu) else 0)
                     for i in range(len(lam)))
            out+=(-1)**(rows-1)*chi(nu,mu[1:])
        return out
    chars=[[chi(a,b) for b in classes] for a in labels]
    sizes=[factorial(5)//__import__('math').prod(
       t**b.count(t)*factorial(b.count(t)) for t in set(b)) for b in classes]
    assert sum(sizes)==120 and all(sum(sizes[c]*chars[i][c]*chars[j][c]
        for c in range(7))==120*(i==j) for i in range(7) for j in range(7))
    trivial=labels.index((5,));order=[trivial]+[i for i in range(7) if i!=trivial]
    out=[]
    for i in order:
        out.append([])
        for j in order:
            out[-1].append([sum(sizes[c]*chars[i][c]*chars[j][c]*chars[k][c]
                                    for c in range(7))//120 for k in order])
    return out

def binary_tetrahedral():
    """Character orthogonality for SL_2(F_3), order 24."""
    import sympy as s
    z=s.exp(2*s.pi*s.I/3).expand(complex=True)
    # 1, -1, six quaternion units, and two size-four conjugacy classes
    # each of elements of orders three and six.
    sizes=[1,1,6,4,4,4,4]
    chars=[]
    for i in range(3):chars.append([1,1,1,z**i,z**(2*i),z**i,z**(2*i)])
    for i in range(3):
        t=[2,-2,0,-1,-1,1,1]
        chars.append([s.simplify(t[j]*chars[i][j]) for j in range(7)])
    chars.append([3,3,-1,0,0,0,0])
    for i,j in itertools.product(range(7),repeat=2):
        assert s.simplify(sum(sizes[c]*chars[i][c]*s.conjugate(chars[j][c])
                              for c in range(7))/24)==int(i==j)
    R=[]
    for i,j in itertools.product(range(7),repeat=2):
        row=[]
        for k in range(7):
            v=s.simplify(sum(sizes[c]*chars[i][c]*chars[j][c]*s.conjugate(chars[k][c])
                         for c in range(7))/24)
            assert v.is_Integer and v>=0
            row.append(int(v))
        if j==0:R.append([])
        R[-1].append(row)
    return R

def integral_noncommutative_models():
    # Published, full integral fusion data paired with Theorem 1.6 and
    # Section 6.2 of Alekseyev--Bruns--Dong--Palcoux (accepted in LiMP).
    # Repository blob 7bd5803c733d893dbd5978a9856ad8962b86ffb6;
    # the order-42 ring has multiplicity five and is not included here.
    f=ROOT/'data/integral_rank7_noncomm_published.txt'
    sha='559cc9c0f978a5926a8a36c92645825ed82927188d51b6a397da3ae4e7d92eb3'
    if hashlib.sha256(f.read_bytes()).hexdigest()!=sha:
        raise ValueError('the published noncommutative model tensors changed')
    found={}
    for line in f.read_text().splitlines():
        if line.startswith('['):
            D,types,d,codegrees,R=ast.literal_eval(line)
            if D in found:raise ValueError('duplicate published global dimension')
            if D!=sum(x*x for x in types):raise ValueError('invalid published dimensions')
            found[D]=R
    if set(found)!={24,42,60}:raise ValueError('published integral registry incomplete')
    return found

def model_registry():
    integral=integral_noncommutative_models()
    return {
        'Vec(C7)':('pointed fusion category on the cyclic group of order seven',pointed_c7()),
        'TY(C6)':('Tambara--Yamagami category on C6 with a nondegenerate bicharacter',ty_c6()),
        'Rep(D16)':('representations of the dihedral group of order sixteen',dihedral16()),
        'Rep(D22)':('representations of the dihedral group of order twenty-two',dihedral22()),
        'Rep(SD16)':('representations of C8 semidirect C2 with action a to a cubed',semidihedral16()),
        'Rep(S5)':('ordinary complex representation category of the symmetric group on five letters',symmetric_five()),
        'Rep(SL2(F3))':('ordinary complex representation category of the binary tetrahedral group',binary_tetrahedral()),
        'Rep(C13rtimesC3)':('ordinary complex representations of C13 semidirect C3 with action a to a cubed, by induction of C13 characters',frobenius_prime(13,3,3)),
        'Rep(C11rtimesC5)':('ordinary complex representations of C11 semidirect C5 with action a to a cubed, by induction of C11 characters',frobenius_prime(11,5,3)),
        'Rep(H24)':('representation category of the dimension-24 Kac algebra identified in Alekseyev--Bruns--Dong--Palcoux, Theorem 1.6',integral[24]),
        'C(A5,1,A4,1)':('group-theoretical fusion category of A4-bimodules in Vec(A5) with trivial cocycles, constructed in Alekseyev--Bruns--Dong--Palcoux, Section 6.2',integral[60]),
        'SO(7)_2':('unitary odd metaplectic SO(7) category at level two',metaplectic7()),
        'Zest(SU(2)_6)':('Z2-graded zesting of unitary SU(2) at level six',zest_su2_6()),
        'SU(2)_6':('unitary SU(2) fusion category at level six',su2(6,list(range(7)))),
        'PSU(2)_12':('even part of unitary SU(2) at level twelve',su2(12,list(range(0,13,2)))),
        'PSU(2)_13':('even part of unitary SU(2) at level thirteen',su2(13,list(range(0,13,2)))),
    }

def oriented_validate(R):
    from oriented_signed import validate_general
    validate_general(R)

def invariants(R):
    d=dual(R)
    return (max(flatten(R)),sum(d[i]!=i for i in range(7)),
            tuple(sorted(sum(v for row in R[i] for v in row) for i in range(1,7))),
            tuple(sorted(sum(R[i][d[i]]) for i in range(1,7))))

def model_matches(rows):
    # Only full-tensor matches, never a guess from dimensions or a partial graph.
    buckets=collections.defaultdict(list)
    for row in rows:buckets[invariants(row['tensor'])].append(row)
    result={};catalog=[]
    for name,(ref,R) in model_registry().items():
        oriented_validate(R)
        hits=[]
        for row in buckets[invariants(R)]:
            for tail in itertools.permutations(range(1,7)):
                p=(0,)+tail
                if all(R[i][j][k]==row['tensor'][p[i]][p[j]][p[k]]
                       for i,j,k in itertools.product(range(7),repeat=3)):
                    hits.append((row,p));break
        if len(hits)!=1:raise ValueError(f'model {name} matches {len(hits)} source tensors')
        row,p=hits[0]
        result.setdefault(row['id'],[]).append(name)
        catalog.append({'id':row['id'],'rank':7,'multiplicity':row['multiplicity'],
                        'name':name,'source_construction':ref,'source_reference':{
          'Vec(C7)':'EGNO, Tensor Categories, pointed categories',
          'TY(C6)':'Tambara and Yamagami, Tensor categories with fusion rules of self-duality for finite abelian groups (1998)',
          'Rep(D16)':'ordinary complex representation category of the explicitly presented dihedral group of order sixteen',
          'Rep(D22)':'ordinary complex representation category of the explicitly presented dihedral group of order twenty-two',
          'Rep(SD16)':'ordinary complex representation category of the explicitly presented semidihedral group of order sixteen',
          'Rep(S5)':'ordinary representation category of S5; exact character products reconstructed by Murnaghan--Nakayama',
          'Rep(SL2(F3))':'ordinary representation category of SL2(F3); character rows are reconstructed and orthogonality checked exactly',
          'Rep(C13rtimesC3)':'Alekseyev--Bruns--Dong--Palcoux, Classifying integral Grothendieck rings up to rank 5 and beyond, Theorem 1.7; exact induced-character products of C13 semidirect C3 in the bundled code',
          'Rep(C11rtimesC5)':'Alekseyev--Bruns--Dong--Palcoux, Classifying integral Grothendieck rings up to rank 5 and beyond, Theorem 1.7; exact induced-character products of C11 semidirect C5 in the bundled code',
          'Rep(H24)':'Alekseyev--Bruns--Dong--Palcoux, Classifying integral Grothendieck rings up to rank 5 and beyond, Theorem 1.6; published full rank-7 noncommutative tensor appendix, FPdim 24',
          'C(A5,1,A4,1)':'Alekseyev--Bruns--Dong--Palcoux, Classifying integral Grothendieck rings up to rank 5 and beyond, Theorem 1.6 and Section 6.2; published full rank-7 noncommutative tensor appendix, FPdim 60',
          'SO(7)_2':'unitary odd metaplectic SO(7) at level two; see Vercleyen, On Low-Rank Multiplicity-Free Fusion Categories (2024), Appendix',
          'Zest(SU(2)_6)':'Vercleyen, On Low-Rank Multiplicity-Free Fusion Categories (2024), Appendix, exact symbolic zesting data',
          'SU(2)_6':'Kirillov and Ostrik, On a q-analogue of the McKay correspondence (2002)',
          'PSU(2)_12':'Kirillov and Ostrik, On a q-analogue of the McKay correspondence (2002)',
          'PSU(2)_13':'Kirillov and Ostrik, On a q-analogue of the McKay correspondence (2002)'}[name],
                        'source_url':{
          'Vec(C7)':'https://www.ams.org/books/surv/205/',
          'TY(C6)':'https://www.sciencedirect.com/science/article/pii/S0021869398975585',
          'Rep(D16)':'https://www.ams.org/books/surv/205/',
          'Rep(D22)':'https://www.ams.org/books/surv/205/',
          'Rep(SD16)':'https://www.ams.org/books/surv/205/',
          'Rep(S5)':'https://www.ams.org/books/surv/205/',
          'Rep(SL2(F3))':'https://www.ams.org/books/surv/205/',
          'Rep(C13rtimesC3)':'https://arxiv.org/abs/2507.07023',
          'Rep(C11rtimesC5)':'https://arxiv.org/abs/2507.07023',
          'Rep(H24)':'https://github.com/sebastienpalcoux/Fusion-Categories/blob/main/IntegralPaper/Data/Noncommutative/InvestNCRank7DataOnly.txt',
          'C(A5,1,A4,1)':'https://github.com/sebastienpalcoux/Fusion-Categories/blob/main/IntegralPaper/Data/Noncommutative/InvestNCRank7DataOnly.txt',
          'SO(7)_2':'https://arxiv.org/abs/2405.20075',
          'Zest(SU(2)_6)':'https://arxiv.org/abs/2405.20075',
          'SU(2)_6':'https://arxiv.org/abs/math/0101219',
          'PSU(2)_12':'https://arxiv.org/abs/math/0101219',
          'PSU(2)_13':'https://arxiv.org/abs/math/0101219'}[name],
                        'basis_permutation_model_to_census':list(p),'tensor':row['tensor'],
                        'existence':{x:'yes' for x in ('general','pivotal','spherical','pseudo_unitary','unitary')}})
    return result,catalog

def spectrum_batch(rows):
    binary=ROOT/'zero_spectrum7'
    if not binary.exists():
        subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'zero_spectrum7.cpp'),'-o',str(binary)],check=True)
    payload=[str(len(rows))]
    for r in rows:
        payload.append('7');payload.extend(map(str,flatten(r['tensor'])))
    result=subprocess.run([str(binary)],input=' '.join(payload),capture_output=True,text=True,check=True,timeout=900)
    answers=[]
    from zero_spectrum import verify as check_spectrum
    for j,line in enumerate(result.stdout.splitlines()):
        parts=list(map(int,line.split()))
        assert parts[0]==j and len(parts)==(11 if parts[1] else 2)
        cert={'kind':'zero_spectrum','indices':parts[2:]} if parts[1] else None
        if cert:check_spectrum(rows[j]['tensor'],cert)
        answers.append(cert)
    assert len(answers)==len(rows)
    return answers

def near_group_certificate(R):
    d=dual(R)
    invertibles=[i for i in range(7) if R[i][d[i]]==[1,0,0,0,0,0,0]]
    if len(invertibles)!=6:return None
    x=next(i for i in range(7) if i not in invertibles)
    if not all(R[g][x][x]==R[x][g][x]==1 and sum(R[g][x])==sum(R[x][g])==1 for g in invertibles):return None
    if not all(R[x][x][g]==1 for g in invertibles):return None
    l=R[x][x][x]
    abelian=all(R[g][h]==R[h][g] for g in invertibles for h in invertibles)
    if l==0 and not abelian:
        return {'kind':'near_group','branch':'nonabelian_TY','noninvertible':x,'level':l,'invertibles':invertibles}
    if 0<l<5 and abelian and all(R[i][j]==R[j][i] for i in range(7) for j in range(7)):
        # Schopieray (2023), Proposition 3.2: d^2=l*d+6, |H|=6.
        return {'kind':'near_group','branch':'Schopieray_3_2','noninvertible':x,'level':l,'invertibles':invertibles}
    return None

def dimension15_certificate(R):
    for x in range(1,7):
        d=[1]*7;d[x]=3
        if all(sum(R[i][j][k]*d[k] for k in range(7))==d[i]*d[j]
               for i in range(7) for j in range(7)):
            # Positive dimension character identifies FPdim; total is 6+9=15.
            return {'kind':'dimension_15','dimensions':d,'global_dimension':15,
                    'theorem':'Etingof--Gelaki--Ostrik 2004, Theorems 3.1 and 5.1'}
    return None

def primitive_codegree_certificate(R):
    from rings import codegree_factors
    import sympy as s
    for p,m in codegree_factors(R):
        n=abs(int(p.TC()));degree=p.degree()
        if degree<7 and all(v<degree for v in s.factorint(n).values()):
            # Schopieray (2021), Theorem 4.4: an indivisible codegree
            # forces rank equal to its algebraic degree, and commutativity.
            return {'kind':'primitive_codegree','polynomial':list(map(int,p.all_coeffs())),
                    'degree':degree,'norm':n,'valuation_factors':list(map(list,s.factorint(n).items()))}
    return None

def verify_own(R,c):
    if c['kind']=='near_group':
        if near_group_certificate(R)!=c:raise ValueError('invalid near-group certificate')
    elif c['kind']=='dimension_15':
        if dimension15_certificate(R)!=c:raise ValueError('invalid dimension-15 certificate')
        if c['global_dimension']!=sum(v*v for v in c['dimensions']) or c['global_dimension']!=15:
            raise ValueError('incorrect integral global dimension')
    elif c['kind']=='primitive_codegree':
        if primitive_codegree_certificate(R)!=c:raise ValueError('invalid primitive codegree')
    elif c['kind']=='oriented_signed':
        from advanced_criteria import verify as verify_oriented
        verify_oriented(R,c)
    else:check_certificate(R,c)

def replay_oriented(item):
    R,c=item
    verify_own(R,c)
    return True

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--max-m',type=int,choices=(1,2,3,4),default=1)
    ap.add_argument('--dnumber',action='store_true',help='perform exact commutative formal-codegree factorization')
    args=ap.parse_args()
    rows=read_source(args.max_m)
    models,catalog=model_matches(rows)
    for r in rows:
        r['commutative']=all(r['tensor'][i][j]==r['tensor'][j][i] for i in range(7) for j in range(i))
    # Keep the allocation table lean: rank-two, primitive-codegree and
    # cyclotomic diagnostics were tested but contribute zero exclusions here.
    stages=['near_group','dimension_15','zero_spectrum','lower_rank_subring']+(
            ['dnumber','subcategory_divisibility','oriented_dimension_order'] if args.dnumber else [])
    stage_counts={s:collections.Counter() for s in stages}
    remaining=list(range(len(rows)))
    records={r['id']:{'id':r['id'],'rank':7,'multiplicity':r['multiplicity'],
                       'source_line':r['source_line'],'commutative':r['commutative'],
                       'status':'unresolved','criterion':None,'certificate':None,
                       'model_names':models.get(r['id'],[]),'tensor':r['tensor']}
             for r in rows}
    # Frozen, independently discovered exhaustive signed trees.  Every tree
    # is replayed against its source tensor below; a stopped search never
    # enters this file and cannot become a negative decision.
    oriented_trees=json.loads((ROOT/'data/oriented_verified_certificates.json').read_text())
    for stage in stages:
        if stage=='zero_spectrum':
            # Skip known positive models to save work; this is not a negative inference.
            active=[i for i in remaining if rows[i]['id'] not in models]
            certificates=spectrum_batch([rows[i] for i in active])
            candidates=zip(active,certificates)
        else:
            candidates=[]
            for i in remaining:
                R=rows[i]['tensor']
                if rows[i]['id'] in models:continue
                if stage=='rank_two':
                    c=next(({'kind':'rank_two','object':j,'multiplicity':R[j][j][j]}
                            for j in range(1,7) if R[j][j][0]==1 and R[j][j][j]>=2
                            and sum(R[j][j])==1+R[j][j][j]),None)
                elif stage=='near_group':c=near_group_certificate(R)
                elif stage=='dimension_15':c=dimension15_certificate(R)
                elif stage=='lower_rank_subring':c=lower_certificate(R)
                elif stage=='dnumber':
                    from rings import dnumber
                    # Noncommutative rank seven has C^3 ⊕ M_2(C). The unique
                    # matrix summand's Casimir eigenvalue is rational and
                    # integral, hence cannot cause a higher-degree d-number
                    # violation; every nonrational factor is a scalar codegree.
                    c=dnumber(R)
                elif stage=='primitive_codegree':
                    c=primitive_codegree_certificate(R) if rows[i]['commutative'] else None
                elif stage=='cyclotomic':
                    from rings import matrices
                    from exact import cyclotomic_failure,t
                    c=cyclotomic_failure([M.charpoly(t).as_poly() for M in matrices(R)]) if rows[i]['commutative'] else None
                elif stage=='subcategory_divisibility':
                    from subring_descent import closed_subrings
                    if rows[i]['commutative'] and next(closed_subrings(R),None) is not None:
                        from proofs import subring_certificate
                        c=subring_certificate(R)
                    else:c=None
                elif stage=='oriented_dimension_order':
                    # All and only complete exact search certificates,
                    # rechecked by verify_own (which enumerates all signed
                    # branches anew).  The verifier repeats this independently.
                    c=oriented_trees.get(rows[i]['id'])
                candidates.append((i,c))
        # Exhaustive signed-table tree replay is independent for each ring.
        # Use processes only here: all cheaper stages keep their simple
        # deterministic sequential ordering and the exact same proof trees.
        if stage=='oriented_dimension_order':
            signed=[(rows[i]['tensor'],c) for i,c in candidates if c is not None]
            with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
                if sum(pool.map(replay_oriented,signed))!=len(signed):
                    raise ValueError('unverified exhaustive signed table')
        excluded=set()
        for i,c in candidates:
            if c is None:continue
            if stage!='oriented_dimension_order':
                verify_own(rows[i]['tensor'],c)
            record=records[rows[i]['id']]
            record['status']='excluded'
            record['criterion']=stage
            record['certificate']=c
            excluded.add(i)
            stage_counts[stage][rows[i]['multiplicity']]+=1
        remaining=[i for i in remaining if i not in excluded]
        print(stage,dict(sorted(stage_counts[stage].items())), 'remaining',len(remaining),flush=True)
    for r in rows:
        rec=records[r['id']]
        if rec['model_names']:
            assert rec['status']=='unresolved', 'positive model contradicted'
            rec['status']='unitarily_realized'
    output=ROOT/'output';output.mkdir(exist_ok=True)
    ledger=sorted(records.values(),key=lambda x:x['source_line'])
    (output/'rank7_ledger.json').write_text(json.dumps(ledger,separators=(',',':'))+'\n')
    (output/'rank7_model_catalog.json').write_text(json.dumps(catalog,separators=(',',':'))+'\n')
    summary={'source_sha256':SOURCE_SHA,'source_commit':'b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726',
             'max_multiplicity':args.max_m,'ring_counts':{m:KNOWN[m] for m in range(1,args.max_m+1)},
             'stage_order':stages,'stage_counts':{s:dict(stage_counts[s]) for s in stages},
             'status_counts':{str(m):dict(collections.Counter(r['status'] for r in ledger if r['multiplicity']==m))
                              for m in range(1,args.max_m+1)},
             'model_count':len({x['id'] for x in catalog}),
             'notes':'Unresolved means no general categorification conclusion; all negative certificates independently reevaluated.'}
    (output/'rank7_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':main()
