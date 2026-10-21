"""Exact R8_3_721 center twist refinement. No floating point, no writes.

Reuses frozen exact character helpers, not old full-census searches. The saved
complete center action classification is an input, not rerun here. See README.
"""
from pathlib import Path
import hashlib
import itertools
import json
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / 'evidence/rank8_frontier_20261021/noncommutative'
FOLLOW = ROOT / 'evidence/rank8_center_followup_20261021'
sys.path.insert(0, str(OLD))
import central_support as c
import character_modular as md
import rotation_search as base

def need(condition, message):
    if not condition:
        raise AssertionError(message)

def rref(rows, K, allow_inconsistent=False):
    A = [row[:] for row in rows]
    pivots = []
    for k in range(len(A[0])-1):
        rr = len(pivots)
        j = next((i for i in range(rr, len(A)) if A[i][k] != K.zero), None)
        if j is None:
            continue
        A[rr], A[j] = A[j], A[rr]
        pivot = A[rr][k]
        A[rr] = [x/pivot for x in A[rr]]
        for j in range(len(A)):
            if j != rr:
                value = A[j][k]
                A[j] = [x-value*y for x,y in zip(A[j], A[rr])]
        pivots.append(k)
    need(allow_inconsistent or not any(all(x == K.zero for x in row[:-1]) and row[-1] != K.zero for row in A), 'linear system consistent')
    return A[:len(pivots)], pivots

def main():
    base.install()
    rows = json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text())
    source = next(r for r in rows if r['id'] == 'R8_3_721')
    need(source['tensor_sha256'] == '76e26a815651476dfda5c2aa654f0d1327bdc890e08086cb6dbfe39ef9a1cdc5', 'source tensor identity')
    R = source['tensor']; a = c.w.data(R); K = a['K']
    cols = a['lows'][10]; chs = md.characters(R,a)
    high = md.full.base.grams.high_columns(a,c.s.Matrix.hstack(*map(c.s.Matrix,cols)))[1]
    allcols = list(cols) + [(0,)+tuple(v) for v,z in high]
    vals = [[md.value(ch,v,K) for ch in chs] for v in allcols]
    ds = [md.value(chs[0],v,K) for v in allcols]
    need(ds[0] == K.one, 'FP character first')
    cases = json.loads((OLD/'verlinde_low_721.json').read_text())['cases']
    sts_results = []
    for case in cases:
        active = [i for i,n in enumerate(case['multiplicities']) if n]
        perm = case['permutation']; equations = []
        need(tuple(perm) in md.assignments(a,chs,cols), 'symmetric low S assignment')
        for E,F in itertools.combinations_with_replacement(range(5),2):
            target = (a['codegrees'][F]*K(a['multiplicities'][F])*md.value(chs[E],cols[perm[F]],K)
                      -sum((v[E]*v[F] for v in vals[:5]),K.zero))
            equations.append([vals[t+5][E]*vals[t+5][F] for t in active] + [target])
        reduced,pivots = rref(equations,K,allow_inconsistent=(perm==[0,1,2,3,4]))
        need(pivots == list(range(4)), 'unique four ordinary twist sums')
        sums = {t:reduced[j][-1] for j,t in enumerate(active)}
        n = 5+sum(case['multiplicities'])
        if perm == [0,1,2,3,4]:
            need(sums[3] == K(-7) and case['multiplicities'][3] == 1, 'identity assignment singleton twist minus seven')
            obstruction = 'singleton_type_3_twist_minus_7'
        elif 8 in active:
            need(sums[8] == K.zero and case['multiplicities'][8] == 1, 'unsplit C singleton twist zero')
            obstruction = 'singleton_type_8_twist_zero'
        else:
            need(sums[3] == K.one and sums[4] == K.zero, 'B and C twist sums')
            if n == 22:
                need(sums[0] == K(-4), 'four A twists all minus one by equality in triangle inequality')
            obstruction = None
        sts_results.append(dict(center_rank=n,permutation=perm,counts=case['multiplicities'],
                                active_types=active,sums={str(t):c.ec(v) for t,v in sums.items()},obstruction=obstruction))
    actions = json.loads((FOLLOW/'r721_center_extension_receipt.json').read_text())['case_results'][7]
    need(actions['center_rank']==22 and actions['permutation']==[0,1,3,2,4], 'remaining rank22 assignment')
    types = [i for i,n in enumerate(actions['counts']) for _ in range(n)]
    columns = list(cols)+[(0,)+tuple(high[t][0]) for t in types]
    dimensions = [md.value(chs[0],v,K) for v in columns]
    perm = actions['permutation']; inverse = [perm.index(i) for i in range(5)]
    S = [[a['D']/a['codegrees'][inverse[i]]/K(a['multiplicities'][inverse[i]])
          *md.value(chs[inverse[i]],v,K) for v in columns] for i in range(5)]
    counts = [0,0,0]; survivors = []; representatives = {}
    for witness in actions['witnesses']:
        size = witness['matching_size']; counts[size]+=1; equations=[]
        Ns = witness['matrices']
        for i in range(1,5):
            for j in range(22):
                equations.append([K(Ns[i-1][k][j])*dimensions[k]-(S[i][j] if k==j else K.zero)
                                  for k in range(22)] + [K.zero])
        for j in range(22):
            if j<5 or types[j-5] in (0,3):
                value = -1 if j>=5 and types[j-5]==0 else 1
                equations.append([K(int(k==j)) for k in range(22)] + [K(value)])
        reduced,pivots = rref(equations,K)
        zero_twists = [j for row,j in zip(reduced,pivots) if row[-1]==K.zero
                       and all(v==K.zero for k,v in enumerate(row[:-1]) if k!=j)]
        need(len(zero_twists)==4-2*size, 'precisely unmatched C twists vanish')
        C = actions['C_labels']; matched = set(sum((list(edge) for edge in witness['C_matching']),[]))
        need(zero_twists==[C[k] for k in range(4) if k not in matched], 'zero twists exactly unmatched C vertices')
        for u,v in witness['C_matching']:
            equation=[K(int(k in (C[u],C[v]))) for k in range(22)]+[K.zero]
            test,piv=rref(equations+[equation],K)
            need(test==reduced and piv==pivots, 'each matched C pair has opposite twists')
        record=dict(matching_size=size,A_matching=witness['A_matching'],C_matching=witness['C_matching'],
                    linear_rank=len(pivots),zero_twist_labels=zero_twists)
        representatives.setdefault(size,record)
        if not zero_twists: survivors.append(record)
    need(counts==[1,36,9] and len(survivors)==9, 'all46 labelled tuples covered, nine survive')
    # FS2 induction formula: all selfdual source simples have signs +/-1;
    # the conjugate pair has indicator0. A,B and distinguished twists square1.
    v0,v3,v4,v5 = [allcols[t+5] for t in (0,3,4,5)]
    d0,d3,d4,d5 = [ds[t+5] for t in (0,3,4,5)]
    known = [sum((d*K(v[j]) for d,v in zip(ds[:5],cols)),K.zero)+K(4)*d0*K(v0[j])+d3*K(v3[j]) for j in range(8)]
    fs2=[]
    for signs in itertools.product([-1,1],repeat=5):
        eps=[1,0,0]+list(signs)
        A=[[d4*K(v4[j]),d5*K(v5[j]),a['D']*K(eps[j])-known[j]] for j in range(8)]
        i,j,det=next((i,j,A[i][0]*A[j][1]-A[i][1]*A[j][0]) for i,j in itertools.combinations(range(8),2)
                     if A[i][0]*A[j][1]!=A[i][1]*A[j][0])
        x=(A[i][2]*A[j][1]-A[i][1]*A[j][2])/det
        y=(A[i][0]*A[j][2]-A[i][2]*A[j][0])/det
        if all(row[0]*x+row[1]*y==row[2] for row in A):
            fs2.append(dict(indicators=eps,C_square_twist_sum=c.ec(x),D_square_twist_sum=c.ec(y)))
    need(len(fs2)==1 and fs2[0]['C_square_twist_sum']==[], 'unique FS2 solution: C squared twist sum zero')
    inputs=[OLD/'verlinde_low_721.json',FOLLOW/'r721_center_extension_receipt.json',
            c.OLD.parent/'pipeline/census_m3.json']
    output=dict(ring='R8_3_721',tensor_sha256=source['tensor_sha256'],
                scope='Necessary center constraints only. Rank16 and two rank22 action types excluded; source ring remains unresolved.',
                field='Q(theta), theta^2-42 theta+16=0, theta=21+5 sqrt(17)',
                inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
                sts_cases=sts_results,rank22_action_counts=counts,rank22_representatives=list(representatives.values()),
                rank22_surviving_labelled_actions=len(survivors),rank22_surviving_permutation_types=1,
                fs2_solution=fs2[0],
                remaining_twist_form='A=(-1,-1,-1,-1); B=(1); C=(z,-z,i*z,-i*z) up to relabeling; sum D= sum D^2=-(1+sqrt(17))/2')
    print(json.dumps(output,indent=2))

if __name__=='__main__': main()
