"""Short exact orbit-ring obstruction for forced central C2 lifts."""
from pathlib import Path
import collections,itertools,json,sys,time
import sympy as s
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025'
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'sources/work/rank11'))
import common
DATA=json.loads((BASE/'tensors.json').read_text())
PROFILES={r['id']:r for r in json.loads((BASE/'profile.json').read_text())['records']}
FAMILIES=json.loads((BASE/'unresolved_families.json').read_text())['records']

def matchings(xs):
    if not xs:yield[];return
    a=xs[0]
    for i in range(1,len(xs)):
        for rest in matchings(xs[1:i]+xs[i+1:]):yield[(a,xs[i])]+rest

def orbit(R,p):
    seen=set();O=[]
    for i in range(len(R)):
        if i not in seen:
            o=sorted({i,p[i]});seen.update(o);O.append(o)
    return O

def quotient(R,p):
    O=orbit(R,p);Q=[]
    for a in O:
        row=[]
        for b in O:
            vals=[sum(R[a[0]][b[0]][k]for k in c)for c in O]
            common.require(all([sum(R[i][j][k]for k in c)for c in O]==vals for i in a for j in b),'well-defined quotient')
            row.append(vals)
        Q.append(row)
    return O,Q

def invariant_orbits(R,p):
    O=orbit(R,p);Q=[]
    for a in O:
        row=[]
        for b in O:
            v=[sum(R[i][j][k]for i in a for j in b)for k in range(len(R))]
            common.require(all(len({v[k]for k in c})==1 for c in O),'invariant product')
            row.append([v[c[0]]for c in O])
        Q.append(row)
    return O,Q

def automorphisms(R,profile):
    G=profile['invertibles'];X=[i for i in range(12)if i not in G]
    common.require(len(G)==8 and len(X)==4,'type1^8,2^4')
    for fixed in itertools.combinations(G[1:],3):
        outside=[g for g in G if g not in (0,)+fixed]
        for pairs in matchings(outside):
            p=list(range(12))
            for a,b in pairs:p[a]=b;p[b]=a
            if any(p[R[g][h].index(1)]!=R[p[g]][p[h]].index(1)for g,h in itertools.product(G,repeat=2)):continue
            for xpairs in matchings(X):
                for a,b in xpairs:p[a]=b;p[b]=a
                if all(R[i][j][k]==R[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)):yield p[:]

def main():
    start=time.monotonic();candidates=[]
    for rid,profile in PROFILES.items():
        q=profile['squared_dimensions']
        if q is None or sum(q)!=24 or sorted(q)!=[1]*8+[4]*4:continue
        R=DATA[rid]
        for p in automorphisms(R,profile):
            O,Q=invariant_orbits(R,p)
            candidates.append(dict(id=rid,automorphism=p,orbits=O,orbit_tensor=Q))
    records=[]
    for f in FAMILIES:
        if f['family']!='D48':continue
        rid=f['id'];R=DATA[rid];profile=PROFILES[rid];ds=[round(v)for v in profile['fp_hint']];rows=[]
        for b in profile['invertibles'][1:]:
            if R[b][b][0]!=1 or any(R[b][i]!=R[i][b]for i in range(12)):continue
            p=[R[b][i].index(1)for i in range(12)]
            fixed=[i for i in range(12)if p[i]==i];pattern=collections.Counter(ds[i]for i in fixed)
            row=dict(involution=b,fixed_dimensions=dict(pattern))
            if pattern=={2:2,4:2}:
                O,Q=quotient(R,p);hits=[]
                for j,c in enumerate(candidates):
                    iso=common.based_iso(Q,c['orbit_tensor'])
                    if iso is not None:hits.append(dict(candidate_index=j,target_id=c['id'],quotient_basis_map=iso))
                row.update(case='rank12_m1_dimension24',source_orbits=O,quotient_tensor=Q,matches=hits)
            elif not pattern:
                O,Q=quotient(R,p);common.validate(Q)
                t=s.Symbol('t');C=s.Matrix([[sum(Q[a][i][k]*Q[a][j][k]for a,k in itertools.product(range(6),repeat=2))for j in range(6)]for i in range(6)])
                factors=s.factor_list(C.charpoly(t).as_expr())[1];fail=[]
                for expr,m in factors:
                    F=s.Poly(expr,t).monic();a=F.all_coeffs();n=F.degree()
                    for j in range(1,n+1):
                        if (int(a[j])**n)%(abs(int(a[-1]))**j):fail.append(dict(factor=list(map(int,a)),index=j))
                row.update(case='free_rank6_quotient',source_orbits=O,quotient_tensor=Q,dnumber_failures=fail)
            elif pattern=={2:2}:row.update(case='near_group_G8_m2_impossible')
            else:row.update(case='rank9_dimension24_type_1_4_2_5')
            rows.append(row)
        records.append(dict(id=rid,central_involutions=rows))
        print(rid,[(r['involution'],r['case'],sorted({m['target_id']for m in r.get('matches',[])}))for r in rows],flush=True)
    out=dict(candidates=candidates,records=records,elapsed_seconds=time.monotonic()-start)
    (OUT/'central_quotients.json').write_text(json.dumps(out,indent=2)+'\n')
    print('DONE',len(candidates),out['elapsed_seconds'])

if __name__=='__main__':main()
