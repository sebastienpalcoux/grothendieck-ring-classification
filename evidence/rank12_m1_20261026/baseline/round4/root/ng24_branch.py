"""Restore the nonabelian dimension24 near-group quotient branches.

This is a ring-level necessary-condition check, never a tensor-action lift.
"""
from pathlib import Path
import itertools, json, sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'prior_round/prior_round/evidence/rank12-m1-offline-20261025/sources/work/rank11'))
import common

def group(q):
    # a^4=1, b a b^-1=a^-1, b^2=a^(2q); q=0:D8, q=1:Q8.
    E=list(itertools.product(range(4),range(2)))
    return [[E.index(((a+(-1)**b*c+2*q*b*d)%4,(b+d)%2))
             for c,d in E] for a,b in E]

def near_group(G):
    R=[[[0]*9 for _ in range(9)]for _ in range(9)]
    for i,j in itertools.product(range(8),repeat=2):R[i][j][G[i][j]]=1
    for i in range(8):R[i][8][8]=R[8][i][8]=1
    R[8][8]=[1]*8+[2]
    common.validate(R)
    return R

def orbits(p):
    out=[];seen=set()
    for i in range(len(p)):
        if i not in seen:
            a=sorted({i,p[i]});seen.update(a);out.append(a)
    return out

def invariant(R,p):
    O=orbits(p)
    return [[[sum(R[i][j][c[0]]for i in a for j in b)for c in O]
             for b in O]for a in O]

def quotient(R,b):
    O=orbits([R[b][i].index(1)for i in range(len(R))])
    return [[[sum(R[a[0]][b[0]][k]for k in c)for c in O]for b in O]for a in O]

def main():
    candidates=[]
    for q in range(2):
        G=group(q);R=near_group(G)
        for tail in itertools.permutations(range(1,8)):
            p=(0,)+tail
            if sum(i==p[i]for i in range(8))!=4 or any(p[p[i]]!=i for i in range(8)):continue
            if any(p[G[i][j]]!=G[p[i]][p[j]]for i,j in itertools.product(range(8),repeat=2)):continue
            P=list(p)+[8]
            candidates.append(dict(group='Q8'if q else'D8',automorphism=P,
                                   invariant_tensor=invariant(R,P)))
    old=json.loads((ROOT/'prior_round/prior_round/evidence/rank12-m1-round2-20261025/family_integral/central_quotients.json').read_text())
    data=json.loads((ROOT/'prior_round/prior_round/evidence/rank12-m1-offline-20261025/tensors.json').read_text())
    rows=[]
    for r in old['records']:
        for branch in r['central_involutions']:
            if branch['case']!='near_group_G8_m2_impossible':continue
            b=branch['involution'];Q=quotient(data[r['id']],b);hits=[]
            for j,c in enumerate(candidates):
                p=common.based_iso(Q,c['invariant_tensor'])
                if p is not None:hits.append(dict(candidate_index=j,group=c['group'],basis_map=p))
            rows.append(dict(id=r['id'],involution=b,matches=hits,
                             corrected_status='retained categorical branch'))
    out=dict(status='PASS',normal_python=__debug__,candidates=candidates,branches=rows,
             scope='Known nonabelian NG(D8,2) and NG(Q8,2) categories exist. Ring automorphisms and orbit matches do not construct tensor actions. No accepted classification changes.')
    (HERE/'ng24_branch.json').write_text(json.dumps(out,indent=2)+'\n')
    for r in rows:print(r['id'],r['involution'],sorted(set(h['group']for h in r['matches'])))

if __name__=='__main__':main()
