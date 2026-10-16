#!/usr/bin/env python3
"""Source-bound R7_4_2603 exclusion by full I(1) reciprocity and two moments.

Standard library only. Every row domain and column is reconstructed from the
original census. The certificate is one 45-entry integer covector.
"""
import argparse
import collections
from fractions import Fraction as F
import gzip
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path

RID = 'R7_4_2603'
D = (80,32)
DIMENSIONS = [(1,0),(4,2),(4,2),(1,0),(1,0),(1,0),(2,0)]
LOW_DIMENSIONS = [(9,4),(10,4),(10,4),(10,4),(20,8),(20,8)]
# First five characters lie in Q(sqrt(-2)), the last two in Q(sqrt(5)).
CHARACTERS = [
    [(1,0),(0,0),(0,0),(1,0),(1,0),(1,0),(-2,0)],
    [(1,0),(0,0),(0,0),(-1,0),(1,0),(-1,0),(0,0)],
    [(1,0),(0,0),(0,0),(-1,0),(-1,0),(1,0),(0,0)],
    [(1,0),(0,1),(0,-1),(1,0),(-1,0),(-1,0),(0,0)],
    [(1,0),(0,-1),(0,1),(1,0),(-1,0),(-1,0),(0,0)],
    [(1,0),(4,-2),(4,-2),(1,0),(1,0),(1,0),(2,0)],
    DIMENSIONS,
]
CODEGREES = [(8,0),(4,0),(4,0),(8,0),(8,0),(80,-32),D]

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def load_helpers(repo):
    path = repo/'evidence/unified_20261016/rank7/verify_quadratic_center_trace.py'
    spec = importlib.util.spec_from_file_location('quadratic_center_helpers',path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def source(repo):
    counts = collections.Counter()
    for line in gzip.open(repo/'supplements/rank7/data/rank7_tables.txt.gz','rt'):
        if not line.strip():
            continue
        N = json.loads(line.replace('{','[').replace('}',']'))
        multiplicity = max(x for row in N for product in row for x in product)
        counts[multiplicity] += 1
        if f'R7_{multiplicity}_{counts[multiplicity]}' == RID:
            return N
    raise RuntimeError('source ID not found')

def evaluate(character, row):
    return tuple(sum(c[k]*v for c,v in zip(character,row)) for k in range(2))

def transport(v):
    a,b = evaluate(DIMENSIONS,v)
    p = 2*a-5*b
    numerators = [4*x+d[1]*p for x,d in zip(v,DIMENSIONS)]
    require(all(x%4==0 for x in numerators),'integral Galois transport')
    return tuple(x//4 for x in numerators)

def verify_characters(N,q):
    dual = [next(j for j in range(7) if N[i][j][0]) for i in range(7)]
    require(dual==[0,2,1,3,4,5,6],'source duality')
    require(all(N[i][j]==N[j][i] for i in range(7) for j in range(7)), 'commutative source')
    require(len({tuple(c) for c in CHARACTERS})==7,'seven distinct characters')
    for ci,character in enumerate(CHARACTERS):
        r = -2 if ci<5 else 5
        for i in range(7):
            for j in range(7):
                require(q.mul(character[i],character[j],r)==evaluate(character,N[i][j]),'full source character identity')
        f = tuple(sum(q.mul(character[i],character[dual[i]],r)[k] for i in range(7)) for k in range(2))
        require(f==CODEGREES[ci],'formal codegree')
        for i in range(7):
            v = tuple(int(j==i) for j in range(7))
            value = evaluate(character,transport(v))
            if ci<5:
                expected = character[i]
            else:
                ratio = (9,-4) if ci==5 else (9,4)
                expected = q.mul(ratio,CHARACTERS[11-ci][i],5)
            require(value==expected,'full character Galois transport')
    for i in range(7):
        v = tuple(int(j==i) for j in range(7))
        require(transport(transport(v))==v,'transport involution')
    return dual

def reciprocity_assignments(low):
    accepted = set()
    for rows8 in itertools.permutations(low[1:4]):
        for rows4 in itertools.permutations(low[4:6]):
            rows = {0:rows8[0],3:rows8[1],4:rows8[2],1:rows4[0],2:rows4[1]}
            valid = True
            for i in range(5):
                for j in range(i):
                    left = evaluate(CHARACTERS[i],rows[j])
                    right = evaluate(CHARACTERS[j],rows[i])
                    if any(CODEGREES[j][0]*left[k] != CODEGREES[i][0]*right[k] for k in range(2)):
                        valid = False
                        break
                if not valid:
                    break
            if valid:
                accepted.add(tuple(tuple(rows[i]) for i in range(5)))
    return sorted(accepted)

def global_rows(B,q):
    result = []
    for v in itertools.product(*(range(math.isqrt(B[i][i])+1) for i in range(1,7))):
        a,b = evaluate(DIMENSIONS[1:],v)
        norm = a*a-5*b*b
        if not norm:
            continue
        # D/z lies in Z[(1+sqrt(5))/2] iff its doubled coefficients
        # are integers of the same parity.
        num_a = 2*(80*a-160*b)
        num_b = 2*(32*a-80*b)
        if num_a%norm or num_b%norm or (num_a//norm-num_b//norm)%2:
            continue
        vv = q.outer(v)
        if any(x>B[i+1][j+1] for x,(i,j) in zip(vv,q.PAIRS)):
            continue
        result.append((v,vv,(a,b)))
    return result

def moment_hull():
    basic = [(1,0,1,0),(-1,0,1,0),(F(1,2),0,F(-1,2),0),(F(-1,2),0,F(-1,2),0),(0,0,-1,0)]
    primitive = []
    for sign in [-1,1]:
        primitive.extend([
            (F(-1,4),F(sign,4),F(-1,4),F(-sign,4)),
            (F(1,4),F(sign,4),F(-1,4),F(sign,4)),
            (0,0,F(1,4),F(sign,4)),
        ])
    return basic+primitive+[tuple(-F(x,2) for x in row) for row in primitive]

def moment_columns(pairs,q):
    result = []
    for orbit in pairs:
        for phase in moment_hull():
            column = [8*sum(row[1][j] for row in orbit) for j in range(21)]
            for degree in range(2):
                values = [q.mul(row[2],phase[2*degree:2*degree+2],5) for row in orbit]
                for i in range(6):
                    for k in range(2):
                        value = 8*sum(row[0][i]*p[k] for row,p in zip(orbit,values))
                        require(F(value).denominator==1,'integral moment coefficient')
                        column.append(int(value))
            require(len(column)==45,'column length')
            result.append(column)
    return result

def verify(repo,certificate):
    q = load_helpers(repo)
    cert = json.loads(certificate.read_text())
    N = source(repo)
    sha = hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
    require(sha==cert['tensor_sha256'],'immutable tensor hash')
    dual = verify_characters(N,q)
    B = [[sum(N[k][i][l]*N[k][j][l] for k in range(7) for l in range(7)) for j in range(7)] for i in range(7)]
    require(q.charpoly(B)==q.polyprod([[1,-8]]*3+[[1,-4]]*2+[[1,-160,1280]]),'full Gram spectrum')
    require(tuple(sum(q.mul(d,d,5)[k] for d in DIMENSIONS) for k in range(2))==D,'global dimension')
    lows,nodes,forced = q.enumerate_low(B,DIMENSIONS,LOW_DIMENSIONS,transport)
    base = global_rows(B,q)
    signs = q.sign_branches(N,dual)
    require(signs==[[1,0,0,1,1,1,1]],'all pivotal sign branches')
    y = cert['separator']
    require(len(y)==45 and all(type(x)==int for x in y),'integer separating covector')
    results = []
    rejected = 0
    all_columns = set()
    for index,low in enumerate(lows):
        assignments = reciprocity_assignments(low)
        if not assignments:
            rejected += 1
            continue
        R,bound,pairs,rank = q.compatible_pairs(base,B,low,transport)
        columns = moment_columns(pairs,q)
        zs = [evaluate(DIMENSIONS,v) for v in low]
        known = [tuple(sum(v[i+1]*z[k] for v,z in zip(low,zs)) for k in range(2)) for i in range(6)]
        target = [8*x for x in bound]+[-8*x for z in known for x in z]+[8*(D[k]*signs[0][i+1]-known[i][k]) for i in range(6) for k in range(2)]
        require(all(q.dot(c,y)>=0 for c in columns),'every allowed moment column')
        target_dot = q.dot(target,y)
        require(target_dot<0,'strictly separated target')
        all_columns.update(tuple(c) for c in columns)
        results.append({'low_index':index,'low_rows':low,'character_assignments':len(assignments),'residual_rank':rank,'paired_row_types':len(pairs),'moment_columns':len(columns),'minimum_column_dot':min(q.dot(c,y) for c in columns),'target_dot':target_dot})
    require(rejected+len(results)==len(lows),'complete low-block coverage')
    require(len(results)>0,'nonempty certificate application')
    return {'status':'PASS','id':RID,'criterion':'quadratic_center_reciprocity_two_moment','scope':'general_complex_after_two_dimension_Galois_pseudo_unitarity','tensor_sha256':sha,'optimizer_used':False,'low_blocks':len(lows),'low_nodes':nodes,'reciprocity_excluded':rejected,'forced_Galois_unit_row':forced,'global_rows':len(base),'pivotal_indicators':signs[0],'hull_vertices':len(moment_hull()),'universal_covectors':1,'distinct_moment_columns':len(all_columns),'branches':results}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--certificate',type=Path,default=Path(__file__).with_name('r2603_center_moment_certificate.json'))
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    output = verify(args.repo,args.certificate)
    text = json.dumps(output,indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text)

if __name__=='__main__':
    main()
