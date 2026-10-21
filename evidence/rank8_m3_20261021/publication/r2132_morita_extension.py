"""Exact premises for the nonsolvable dimension-sixty extension obstruction."""
import argparse
import json
import sys
from pathlib import Path
from itertools import permutations
sys.path.insert(0,str(Path(__file__).resolve().parent))
from finite_group_exact import *
RID='R8_3_2132'
SHA='98c9fb73edbd05a2a38222776e7cc4912954bff817611ac5c3bd8ece1c83cd61'
KIND='nonsolvable_dimension60_extension'

def certificate(R):
    require(digest(R)==SHA,'source tensor hash')
    d=[(1,0),(1,0),(0,1),(5,0),(5,0),(0,1),(2,0),(2,0)]
    require(quadratic_dimensions(R,d,30)==120,'total dimension')
    neutral=[0,1,3,4,6,7];odd=[2,5];grading(R,neutral,odd)
    require(sum(d[i][0]**2 for i in neutral)==60,'neutral dimension')
    require(adjoint(R,neutral)==neutral,'neutral equals its adjoint')
    inv=[i for i in neutral if d[i]==(1,0)];require(inv==[0,1],'exactly two invertibles')
    action=[]
    for j in range(8):
        row=R[1][j];require(sum(row)==1,'invertible basis permutation');action.append(row.index(1))
    require(action==[1,0,5,4,3,2,6,7],'unique sign action')
    cycles=[];todo=set(neutral)
    while todo:
        i=min(todo);orbit=sorted({i,action[i]});todo-=set(orbit);cycles.append(orbit)
    require(cycles==[[0,1],[3,4],[6],[7]],'de-equivariantization orbits')
    base=[]
    for orbit in cycles:
        degree=d[orbit[0]][0]
        if len(orbit)==2:base.append(degree)
        else:
            require(degree%2==0,'free base orbit has even equivariant dimension')
            base.extend([degree//2]*2)
    require(sorted(base)==[1,1,1,1,1,5] and sum(x*x for x in base)==30,'forced near-group base')
    # Bind the old general negative to an independent canonical NG(C5,4) tensor.
    T=[[[0]*6 for _ in range(6)] for _ in range(6)]
    for i in range(5):
        for j in range(5):T[i][j][(i+j)%5]=1
        T[i][5][5]=T[5][i][5]=1
    T[5][5]=[1,1,1,1,1,4]
    old=next(x for x in json.loads((ROOT/'supplements/rank6/data/census.json').read_text()) if x['id']=='R6_4_19')
    decision=next(x for x in json.loads((ROOT/'supplements/rank6/data/decisions.json').read_text()) if x['id']=='R6_4_19')
    require(decision['status']=='excluded' and decision['existence']['general']=='no','published general negative')
    require(decision['certificate']['kind']=='small_dimension_morita' and decision['certificate']['branch']=='dimension30','dimension-thirty theorem source')
    require(decision['certificate']['allowed_simple_dimensions']==[1,2],'dimension-thirty theorem scope')
    mapping=None
    for tail in permutations(range(1,6)):
        p=(0,)+tail
        if all(T[i][j][k]==old['N'][p[i]][p[j]][p[k]] for i in range(6) for j in range(6) for k in range(6)):
            mapping=list(p);break
    require(mapping is not None,'canonical near-group tensor identifies old general negative')
    G=alternating();require(len(G)==60,'A5 order')
    nontrivial=[C for C in classes(G) if len(C)>1]
    require(sorted(map(len,nontrivial))==[12,12,15,20],'A5 conjugacy classes')
    generated_orders=[len(generated(sorted(C))) for C in nontrivial]
    require(generated_orders==[60]*4,'no nontrivial proper normal subgroup')
    require(any(compose(g,h)!=compose(h,g) for g in G for h in G),'A5 is nonabelian')
    require(any(d[i][1] for i in odd),'nonintegral graded component')
    return {'kind':KIND,'id':RID,'tensor_sha256':SHA,'neutral_basis':neutral,'odd_basis':odd,
            'neutral_dimension':60,'neutral_adjoint_basis':neutral,'invertibles':inv,'sign_permutation':action,
            'neutral_sign_orbits':cycles,'forced_deequivariantization_dimensions':sorted(base),
            'negative_near_group':'R6_4_19','negative_decision_sha256':digest(decision),
            'canonical_near_group_to_source':mapping,'negative_tensor_sha256':digest(old['N']),
            'A5_nontrivial_class_sizes':sorted(map(len,nontrivial)),'normal_closure_orders':generated_orders,
            'pointed_transport_component_rank':60,'pointed_transport_component_dimension':60}

def verify(R,c):
    require(c==certificate(R),'dimension-sixty certificate replay differs');return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
    R=source(RID,SHA);c=certificate(R)
    record={'id':RID,'tensor_sha256':SHA,'scope':'general_complex_fusion_category','status':'excluded','certificate':c}
    path=Path(__file__).with_suffix('.json')
    if a.write:path.write_text(json.dumps(record,indent=2)+'\n')
    else:verify(R,json.loads(path.read_text())['certificate'])
    print(json.dumps({'status':'PASS','id':RID,'scope':record['scope'],'certificate':c},indent=2))
if __name__=='__main__':main()
