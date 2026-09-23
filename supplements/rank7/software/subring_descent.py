"""Generic closed-subring transfer using the rank-four/five classification theorems."""
import itertools,json
from pathlib import Path
from prepare import key,flatten,dual
from exact import require
P=Path(__file__).resolve().parents[1]
_cache=None

def registry():
    global _cache
    if _cache is None:
        d=json.load(open(P/'data/lower_rank_positive_models.json'))
        _cache={n:{key(x['tensor']) for x in d if len(x['tensor'])==n} for n in (4,5)}
        require(len(_cache[4])==15 and len(_cache[5])==17,'lower-rank positive registry incomplete')
    return _cache

def closed_subrings(R):
    n=len(R);du=dual(R)
    for k in range(2,n):
        for tail in itertools.combinations(range(1,n),k-1):
            J=(0,)+tail;S=set(J)
            if any(du[i] not in S for i in J):continue
            if any(v and h not in S for i in J for j in J for h,v in enumerate(R[i][j])):continue
            yield J,[[[R[i][j][k] for k in J] for j in J] for i in J]

def certificate(R):
    reg=registry()
    for J,S in closed_subrings(R):
        n=len(J);m=max(flatten(S))
        if n in (4,5) and m<=({4:128,5:20}[n]) and key(S) not in reg[n]:
            return {'kind':'lower_rank_subring','subset':list(J),'rank':n,'multiplicity':m,'theorem':f'DP{n}.1.1'}
    return None

def verify(R,c):
    require(c['kind']=='lower_rank_subring','wrong subring criterion')
    J=c['subset'];n=len(J);S=None
    for jj,ss in closed_subrings(R):
        if list(jj)==J:S=ss;break
    require(S is not None and n==c['rank'] and n in (4,5),'invalid closed subring')
    m=max(flatten(S));require(m==c['multiplicity'] and m<={4:128,5:20}[n],'outside cited theorem range')
    require(key(S) not in registry()[n],'subring has a positive model')
