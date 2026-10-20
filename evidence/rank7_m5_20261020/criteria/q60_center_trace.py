"""Exploratory exact q=60 saturated center-trace obstruction.

Scope is pseudo-unitary until a separate general-to-positive reduction is
supplied. Discovery uses an LP; every claimed separator is checked exactly.
"""
import argparse
import collections
import hashlib
import functools
import importlib.util
import itertools
import json
import math
import sys
import time

from quadratic_compression import HERE, ROOT, tensor_hash

spec = importlib.util.spec_from_file_location('qct_base', ROOT / 'evidence/unified_20261016/rank7/verify_quadratic_center_trace.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
require = base.require
sys.path.insert(0, str(ROOT / 'supplements/rank7/software'))

CONFIG = {
    'R7_5_443': {'dimensions': [(1,0),(1,0),(4,1),(5,1),(5,1),(4,1),(6,2)],
                'codegrees': [12,5,4,6,6],
                'separating_factors': [[1,-683],[1,-422],[1,-230],[1,-184],[1,298],[1,-15896,-26866796]]},
    'R7_5_1214': {'dimensions': [(1,0),(1,0),(4,1),(4,1),(5,1),(5,1),(6,2)],
                 'codegrees': [5,12,12,4,4],
                 'separating_factors': [[1,-953],[1,-24],[1,28],[1,-16436,-22501976],[1,712,-572]]},
}


def source_data(N, rid):
    cfg = CONFIG[rid]
    d = cfg['dimensions']; D = (240,60)
    require(all(N[i][j] == N[j][i] for i in range(7) for j in range(7)), 'commutative source')
    for i,j in itertools.product(range(7), repeat=2):
        require(base.mul(d[i], d[j], 15) == tuple(sum(N[i][j][k]*d[k][l] for k in range(7)) for l in range(2)), 'dimension character')
    require(tuple(sum(base.mul(z,z,15)[j] for z in d) for j in range(2)) == D, 'global dimension')
    B = [[sum(N[k][i][j]*N[k][l][j] for k in range(7) for j in range(7)) for l in range(7)] for i in range(7)]
    require(base.charpoly(B) == base.polyprod([[1,-z] for z in cfg['codegrees']] + [[1,-480,3600]]), 'formal codegrees')
    M = [[sum(base.WEIGHTS[k]*N[k][j][i] for k in range(7)) for j in range(7)] for i in range(7)]
    require(base.charpoly(M) == base.polyprod(cfg['separating_factors']), 'character fields')
    zs = [(D[0]//z,D[1]//z) for z in cfg['codegrees']] + [(31,8)]
    zs.sort(key=functools.cmp_to_key(lambda z,w:base.quadratic_sign((z[0]-w[0],z[1]-w[1]),15)))
    def transport(v):
        a,b = [sum(x*z[j] for x,z in zip(v,d)) for j in range(2)]
        return tuple(x+z[1]*(a-4*b) for x,z in zip(v,d))
    for j in range(7):
        unit = tuple(int(i==j) for i in range(7))
        require(transport(transport(unit)) == unit, 'Galois row involution')
    dual = [next(j for j in range(7) if N[i][j][0]) for i in range(7)]
    return d,D,B,zs,transport,base.sign_branches(N,dual)


def global_rows(B,d):
    rows = []
    for v in itertools.product(*(range(math.isqrt(B[i][i])+1) for i in range(1,7))):
        a,b = [sum(x*z[j] for x,z in zip(v,d[1:])) for j in range(2)]
        norm = a*a-15*b*b
        if not norm or 60*a % norm or 60*b % norm:
            continue
        q = base.outer(v)
        if any(z>B[i+1][j+1] for z,(i,j) in zip(q,base.PAIRS)):
            continue
        rows.append((v,q,(a,b)))
    return rows


def trace_columns(pairs,D):
    # All coefficients scaled by 8. The primitive-60 second trace is -1/8.
    basic = [(8,0,8,0),(-8,0,8,0),(4,0,-4,0),(-4,0,-4,0),(0,0,-8,0)]
    restricted = basic+[(0,-1,-1,0)]
    unrestricted = basic+[(0,1,-1,0),(0,-1,-1,0),(0,0,0,1),(0,0,0,-1)]
    cols = []
    for orbit in pairs:
        z = orbit[0][2]
        rational = z[0]*D[1] == z[1]*D[0]
        require(not rational or len(orbit)==1, 'rational normalized row fixed')
        gram = [sum(row[1][j] for row in orbit) for j in range(21)]
        for ph in unrestricted if rational else restricted:
            col = [8*x for x in gram]
            for degree in range(2):
                values = [base.mul(row[2], ph[2*degree:2*degree+2], 15) for row in orbit]
                col.extend(sum(row[0][i]*value[k] for row,value in zip(orbit,values)) for i in range(6) for k in range(2))
            cols.append(col)
    return cols


def separate(cols, rhs, pool):
    for i,y in enumerate(pool):
        if base.dot(rhs,y)<0 and all(base.dot(c,y)>=0 for c in cols):
            return i
    from tensor_rotation import farkas
    A = [list(row) for row in zip(*cols)]
    y = farkas(A, rhs)
    if y is None:
        return None
    require(base.dot(rhs,y)<0 and all(base.dot(c,y)>=0 for c in cols), 'exact separating inequality')
    pool.append(y)
    return len(pool)-1


def run(rid):
    start=time.monotonic()
    N=next(row['tensor'] for row in json.loads((ROOT/'supplements/rank7/output/m5/census.json').read_text()) if row['id']==rid)
    d,D,B,zs,transport,signs=source_data(N,rid)
    lows,nodes,forced=base.enumerate_low(B,d,zs,transport)
    print(json.dumps({'event':'lows','id':rid,'count':len(lows),'seconds':time.monotonic()-start}),flush=True)
    rows=global_rows(B,d)
    print(json.dumps({'event':'rows','count':len(rows),'seconds':time.monotonic()-start}),flush=True)
    pool=[];branches=[];unresolved=[];stats=collections.Counter()
    for ix,low in enumerate(lows):
        R,bound,pairs,rank=base.compatible_pairs(rows,B,low,transport)
        gramcols=[[sum(row[1][j] for row in orbit) for j in range(21)] for orbit in pairs]
        prime=next((p for p in [2,3,5,7,11,13] if not base.span_contains(gramcols,bound,p)),None)
        if prime:
            branches.append({'low':low,'modular_prime':prime});stats['modular']+=1;continue
        cols=trace_columns(pairs,D)
        known=[tuple(sum(v[i+1]*z[k] for v,z in zip(low,zs)) for k in range(2)) for i in range(6)]
        separators=[]
        for sign in signs:
            rhs=[8*x for x in bound]+[-8*x for z in known for x in z]+[8*(D[k]*sign[i+1]-known[i][k]) for i in range(6) for k in range(2)]
            sep=separate(cols,rhs,pool)
            separators.append(sep)
            if sep is None:unresolved.append({'low_index':ix,'sign':sign,'pairs':len(pairs)})
        branches.append({'low':low,'separators':separators})
        stats['trace']+=1
        if ix%100==0:print(json.dumps({'event':'progress','index':ix,'pool':len(pool),'unresolved':len(unresolved)}),flush=True)
    result={'id':rid,'scope':'pseudo_unitary','status':'candidate_exclusion' if not unresolved else 'no_exclusion',
            'source_sha256':tensor_hash(N),'low_frames':len(lows),'low_nodes':nodes,'forced_row':forced,
            'global_rows':len(rows),'pivotal_signs':signs,'separators':pool,'branches':branches,
            'unresolved':unresolved,'statistics':dict(stats),'seconds':time.monotonic()-start}
    (HERE/(rid+'_q60_trace.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('separators','branches','unresolved')}),flush=True)


def verify(rid, certificate_data=None, write_receipt=True):
    """Reconstruct the entire exact domain. No optimizer is imported or used."""
    start=time.monotonic()
    path=HERE/(rid+'_q60_trace.json')
    cert=json.loads(path.read_text()) if certificate_data is None else certificate_data
    N=next(row['tensor'] for row in json.loads((ROOT/'supplements/rank7/output/m5/census.json').read_text()) if row['id']==rid)
    require(cert['scope']=='pseudo_unitary' and cert['status']=='candidate_exclusion', 'certificate scope')
    require(cert['source_sha256']==tensor_hash(N), 'source hash')
    d,D,B,zs,transport,signs=source_data(N,rid)
    lows,nodes,forced=base.enumerate_low(B,d,zs,transport)
    rows=global_rows(B,d)
    require(cert['low_frames']==len(lows) and cert['low_nodes']==nodes and cert['forced_row']==list(forced), 'low inventory')
    require(cert['global_rows']==len(rows) and cert['pivotal_signs']==signs, 'row and sign inventories')
    require(len(cert['branches'])==len(lows) and cert['unresolved']==[], 'complete branch cover')
    pool=cert['separators']
    require(all(len(y)==45 and all(type(v)is int for v in y) for y in pool), 'integer separating covectors')
    counts=collections.Counter()
    minimum_gap=None
    for low,branch in zip(lows,cert['branches']):
        require(branch['low']==[list(v) for v in low], 'low branch ordering')
        R,bound,pairs,rank=base.compatible_pairs(rows,B,low,transport)
        if 'modular_prime' in branch:
            prime=branch['modular_prime']
            require(prime in [2,3,5,7,11,13], 'prime test domain')
            gramcols=[[sum(row[1][j] for row in orbit) for j in range(21)] for orbit in pairs]
            require(not base.span_contains(gramcols,bound,prime), 'modular span obstruction')
            counts['modular']+=1
            continue
        cols=trace_columns(pairs,D)
        known=[tuple(sum(v[i+1]*z[k] for v,z in zip(low,zs)) for k in range(2)) for i in range(6)]
        require(len(branch['separators'])==len(signs), 'all pivotal sign choices covered')
        for sign,idx in zip(signs,branch['separators']):
            require(type(idx)is int and 0<=idx<len(pool), 'separator index')
            y=pool[idx]
            rhs=[8*x for x in bound]+[-8*x for z in known for x in z]+[8*(D[k]*sign[i+1]-known[i][k]) for i in range(6) for k in range(2)]
            gap=-base.dot(rhs,y)
            require(gap>0, 'strict separating target')
            require(all(base.dot(col,y)>=0 for col in cols), 'all allowed moment columns separated')
            minimum_gap=gap if minimum_gap is None else min(gap,minimum_gap)
        counts['trace']+=1
    require(dict(counts)==cert['statistics'], 'branch statistics')
    receipt={'status':'PASS','id':rid,'scope':'pseudo_unitary','optimizer_used':False,
             'optimized_python':not __debug__,'source_sha256':tensor_hash(N),
             'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
             'low_frames':len(lows),'global_rows':len(rows),'separators':len(pool),
             'minimum_strict_integer_gap':minimum_gap,'statistics':dict(counts),
             'seconds':time.monotonic()-start}
    target=HERE/(rid+'_q60_trace_'+('optimized' if not __debug__ else 'normal')+'_replay.json')
    if write_receipt:
        target.write_text(json.dumps(receipt,indent=2)+'\n')
        print(json.dumps(receipt),flush=True)
    return receipt


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('ring',choices=CONFIG);parser.add_argument('--replay',action='store_true')
    args=parser.parse_args();(verify if args.replay else run)(args.ring)
