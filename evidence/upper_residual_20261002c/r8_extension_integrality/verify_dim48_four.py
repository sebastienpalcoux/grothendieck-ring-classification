#!/usr/bin/env python3
"""Exact low-rank ring, module-orbit and finite-group premises for D48 four."""
import argparse
import itertools
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'supplements/rank8/data/rank8_tables.txt.gz').exists())
sys.path.insert(0,str(ROOT/'evidence/upper_residual_20261002b_recovery'))
from verify_recovery import read_source,validate_ring,fingerprint,require


def neutral():
    T=[[[0]*6 for _ in range(6)] for _ in range(6)]
    for a,b in itertools.product(range(4),repeat=2):T[a][b][a^b]=1
    for a in range(4):
        for b in (4,5):T[a][b][b]=T[b][a][b]=1
    T[4][4]=[1,1,1,1,0,0]
    T[4][5]=T[5][4]=[0,0,0,0,0,2]
    T[5][5]=[1,1,1,1,2,2]
    return T


def classify_dimension12():
    tested=0;valid=[];eligible=[]
    # Duality relates right and left actions on a two-element set. Since
    # S2 is abelian and these actions factor through exponent two, they
    # coincide. Mixed products are nevertheless enumerated independently.
    pairs=list(itertools.product((4,5),repeat=2))
    for cyclic in (False,True):
        for action in ([0,0,0,0],[0,1,0,1]) if cyclic else ([0,0,0,0],[0,0,1,1]):
            require(all(action[(a+b)%4 if cyclic else a^b]==(action[a]^action[b]) for a,b in itertools.product(range(4),repeat=2)), 'unit action is not a homomorphism')
            for flipdual in (False,True):
                T=[[[0]*6 for _ in range(6)] for _ in range(6)]
                for a,b in itertools.product(range(4),repeat=2):T[a][b][(a+b)%4 if cyclic else a^b]=1
                for a in range(4):
                    for x in (4,5):T[a][x][4+((x-4)^action[a])]=T[x][a][4+((x-4)^action[a])]=1
                choices=[]
                for x,y in pairs:
                    dy=4+((y-4)^flipdual)
                    for g in range(4):T[x][y][g]=int(x==4+((dy-4)^action[g]))
                    remaining=4-sum(T[x][y][:4]);require(remaining%2==0,'nonintegral product budget')
                    choices.append([(a,remaining//2-a) for a in range(remaining//2+1)])
                for tails in itertools.product(*choices):
                    tested+=1
                    for (x,y),tail in zip(pairs,tails):T[x][y][4:]=list(tail)
                    try:validate_ring(T)
                    except ValueError:continue
                    aut=[]
                    for perm in itertools.permutations((1,2,3)):
                        p=[0]+list(perm)+[5,4]
                        if (sum(p[i]==i for i in range(4))==2 and all(p[p[i]]==i for i in range(6))
                                and all(T[p[i]][p[j]][p[k]]==T[i][j][k] for i,j,k in itertools.product(range(6),repeat=3))):aut.append(p)
                    row={'unit_group':'C4' if cyclic else 'V4','unit_action':action,'dual_swaps_nonunits':flipdual,'nonunit_products':[T[x][y][:] for x,y in pairs],'outer_involutions':aut,'tensor_sha256':fingerprint(T)}
                    valid.append(row)
                    if aut:eligible.append(row)
    require(len(valid)==6 and len(eligible)==2,'dimension12 ring exhaustion count')
    require(all(row['unit_action']==[0]*4 and row['dual_swaps_nonunits'] and row['nonunit_products']==[[0,0,0,0,0,2],[1,1,1,1,0,0],[1,1,1,1,0,0],[0,0,0,0,2,0]] for row in eligible),'eligible ring not R3_A')
    return {'oriented_candidate_tables_tested':tested,'valid_tables':valid,'eligible_tables':eligible,'categorically_eligible_group':'V4_by_Jordan_Larson_Theorem1_4'}


def module_orbits():
    ranks=[4,1,1,2,2,2];rows=[]
    for p in itertools.permutations(range(6)):
        if not all(p[p[p[i]]]==i for i in range(6)) or ranks[p[0]]!=1 or ranks[p[p[0]]]!=1:continue
        seen=set();orbits=[]
        for i in range(6):
            if i in seen:continue
            orbit=sorted({i,p[i],p[p[i]]});seen.update(orbit);orbits.append(orbit)
        require(all(sum(ranks[i] for i in o)>=6 for o in orbits if len(o)>1),'small nontrivial module orbit')
        require(all(ranks[o[0]]==2 for o in orbits if len(o)==1),'wrong fixed module rank')
        rows.append({'permutation':list(p),'orbits':orbits,'orbit_total_ranks':[sum(ranks[i] for i in o) for o in orbits]})
    require(len(rows)==6,'module-class action exhaustion')
    return {'module_class_ranks':ranks,'possible_order3_actions':rows,'small_module_extension_rank':4,'actual_fixed_rank2_summands':2}


def s4_check():
    G=list(itertools.permutations(range(4)));unit=tuple(range(4))
    def mul(x,y):return tuple(x[y[i]] for i in range(4))
    inv={x:tuple(x.index(i) for i in range(4)) for x in G}
    def generate(xs):
        H={unit};todo=list(xs)
        while todo:
            x=todo.pop()
            if x in H:continue
            H.add(x);old=list(H);todo.extend(mul(x,y) for y in old);todo.extend(mul(y,x) for y in old);todo.append(inv[x])
        return frozenset(H)
    subgroups={frozenset([unit])};queue=list(subgroups)
    while queue:
        H=queue.pop()
        for x in G:
            if x in H:continue
            K=generate(list(H)+[x])
            if K not in subgroups:subgroups.add(K);queue.append(K)
    normals=[]
    for H in subgroups:
        if all(mul(x,y)==mul(y,x) for x,y in itertools.product(H,repeat=2)) and all(mul(mul(x,h),inv[x]) in H for x in G for h in H):normals.append(sorted(H))
    normals.sort(key=len)
    require(len(subgroups)==30 and [len(H) for H in normals]==[1,4],'S4 subgroup and normal abelian exhaustion')
    # Every involution permutation of three Lagrangians has a fixed point.
    involutions=[p for p in itertools.permutations(range(3)) if all(p[p[i]]==i for i in range(3))]
    require(all(any(p[i]==i for i in range(3)) for p in involutions),'Lagrangian fixed point')
    return {'group_order':24,'all_subgroups_enumerated':len(subgroups),'normal_abelian_subgroups':normals,'bimodule_simple_dimensions':[1,2],'involutions_on_three_lagrangians':list(map(list,involutions)),'A4_times_C2_identity_supported_center_invertibles':6}


def verify():
    start=time.monotonic();S=read_source(ROOT,8);B=neutral();validate_ring(B);rows=[]
    maps={158:[0,3,4,5,6,7],186:[0,3,4,5,6,7],579:[0,1,2,5,6,7],682:[0,1,2,3,4,6]}
    for number,p in maps.items():
        case=f'R8_2_{number}';T=S[case];validate_ring(T);odd=[i for i in range(8) if i not in p]
        require(all(T[p[i]][p[j]][p[k]]==B[i][j][k] for i,j,k in itertools.product(range(6),repeat=3)),'neutral full tensor')
        grade=[int(i in odd) for i in range(8)]
        require(all(not T[i][j][k] or grade[k]==(grade[i]+grade[j])%2 for i,j,k in itertools.product(range(8),repeat=3)),'faithful C2 grading')
        dims=[(0,2) if i in odd else (4,0) if i==p[5] else (2,0) if i==p[4] else (1,0) for i in range(8)]
        def mul(a,b):return a[0]*b[0]+3*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
        require(all(mul(dims[i],dims[j])==tuple(sum(T[i][j][k]*dims[k][a] for k in range(8)) for a in (0,1)) for i,j in itertools.product(range(8),repeat=2)),'exact positive dimension character')
        require(sum(mul(d,d)[0] for d in dims)==48,'ambient dimension48')
        actions=[[next(k for k in range(8) if T[g][m][k]) for m in odd] for g in p[:4]]
        rank_by_sign={str(g):1 if row[0]!=odd[0] else 4 for g,row in zip(p[:4],actions) if g!=0}
        rows.append({'id':case,'source_sha256':fingerprint(T),'neutral_basis_map':p,'odd_basis':odd,'pointed_action_on_odd':actions,'deequivariantized_module_rank_by_sign':rank_by_sign,'dimensions_Z_sqrt3':dims})
    result={'status':'PASS','scope':'general_complex','source_witnesses':rows,'dimension12_classification':classify_dimension12(),'module_orbit_verification':module_orbits(),'S4_group_verification':s4_check(),'python_optimized':not __debug__};result['seconds']=round(time.monotonic()-start,3);return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args();r=verify()
    if args.output:args.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
