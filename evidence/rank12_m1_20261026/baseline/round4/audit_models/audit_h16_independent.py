"""Fresh twisted-group-algebra and all-decomposition trace audit of H16 cases.

No discovery fusion routine is imported.  Input characters are certified as
actual irreducibles by primitive central idempotents in the twisted group
algebra, rather than accepting orthogonality alone.
"""
import json, time
from itertools import product
from functools import lru_cache
from audit_liptrap import HERE,FIRST,need

def gaussian(cs):
    # The exported Q(zeta_96) entries have these four exact forms only.
    terms={i:c for i,c in enumerate(cs) if c}
    need(set(terms)<={32,64,56,88},'Gaussian character coordinates')
    need(terms.get(32,0)==terms.get(64,0) and terms.get(56,0)==terms.get(88,0),'paired cyclotomic coordinates')
    # zeta^32+zeta^64=-1; zeta^56+zeta^88=-i.
    return complex(-terms.get(32,0),-terms.get(56,0))

def one_case(row,record,targets):
    G,H,P=row['table'],row['subgroup'],row['psi'];n=len(G);hs=set(H);hi={h:i for i,h in enumerate(H)}
    need(n==48 and len(H)==16 and G[0]==list(range(n)),'group/unit sizes')
    inv=[next(j for j in range(n) if G[i][j]==0) for i in range(n)]
    need(all(G[G[a][b]][c]==G[a][G[b][c]] for a,b,c in product(range(n),repeat=3)),'group associativity')
    need(all(G[a][b] in hs for a,b in product(H,repeat=2)),'subgroup')
    def psi(a,b):return P[hi[a]][hi[b]]
    need(all(psi(0,a)==psi(a,0)==0 for a in H),'normalized subgroup cocycle')
    need(all((psi(b,c)-psi(G[a][b],c)+psi(a,G[b][c])-psi(a,b))%2==0 for a,b,c in product(H,repeat=3)),'actual twisted regular algebra')
    obs=row['objects'];byz={};chars=[];orbits=[]
    for ob in obs:
        z=ob['z'];K=ob['stab'];need(K[0]==0 and set(K)==hs&{G[G[z][h]][inv[z]] for h in H},'actual stabilizer')
        ch={a:gaussian(v) for a,v in zip(K,ob['char'])};chars.append(ch)
        byz.setdefault(z,[]).append(len(chars)-1)
        orb={}
        # First lexicographic transport, distinct from discovery's overwritten one.
        for u,v in product(H,repeat=2):orb.setdefault(G[G[u][z]][inv[v]],(u,v))
        orbits.append(orb)
    need(sum(len(orbits[ii[0]]) for ii in byz.values())==48,'all double cosets')
    need(len(set().union(*(set(orbits[ii[0]]) for ii in byz.values())))==48,'double coset coverage')
    dims=[]
    for z,ii in byz.items():
        K=obs[ii[0]]['stab'];sz=len(K);ks=set(K)
        conj=lambda a:G[G[inv[z]][a]][z]
        alpha=lambda a,b:(psi(a,b)-psi(conj(a),conj(b)))%2
        # Center dimension of a twisted group algebra = number of alpha-regular
        # conjugacy classes; central primitive idempotent check follows below.
        unseen=set(K);center=0
        while unseen:
            a=min(unseen);cl={G[G[b][a]][inv[b]] for b in K};unseen-=cl
            center+=all(alpha(a,b)==alpha(b,a) for b in K if G[a][b]==G[b][a])
        need(center==len(ii),'full primitive center dimension')
        coeff=[]
        for i in ii:
            ch=chars[i];d=ch[0];need(d.imag==0 and d.real in [1,2],'positive fiber degree');d=int(d.real)
            dims.append(16//sz*d)
            # sz times the central idempotent of this character.
            A={a:d*((-1)**alpha(a,inv[a]))*ch[inv[a]] for a in K};coeff.append(A)
            need(A[0]==d*d,'regular-block rank d squared')
            for b in K:
                left={G[b][a]:A[a]*((-1)**alpha(b,a)) for a in K}
                right={G[a][b]:A[a]*((-1)**alpha(a,b)) for a in K}
                need(left==right,'central character idempotent')
            # The trace of L_b on this block divided by d recovers the input
            # character, binding the certified block to the supplied values.
            for b in K:need(A[inv[b]]*((-1)**alpha(inv[b],b))==d*ch[b],'block trace character')
        for ia,A in enumerate(coeff):
            for ib,B in enumerate(coeff):
                C={a:0j for a in K}
                for a,b in product(K,repeat=2):C[G[a][b]]+=A[a]*B[b]*((-1)**alpha(a,b))
                need(all(C[a]==(sz*A[a] if ia==ib else 0) for a in K),'orthogonal idempotents in actual algebra')
        need(all(sum(A[a] for A in coeff)==(sz if a==0 else 0) for a in K),'idempotent completeness')
    need(sorted(dims)==record['dimensions'],'recorded complete category type')
    ans=dict(smallgroup=row['smallgroup'],rank=len(obs),dimensions=sorted(dims),actual_irreducible_characters=True)
    if len(obs)!=12:return ans
    @lru_cache(None)
    def trace(i,x,a,b):
        if x not in orbits[i] or G[a][x]!=G[x][b]:return 0j
        u,v=orbits[i][x];h=G[G[inv[u]][a]][u];k=G[G[inv[v]][b]][v]
        phase=psi(a,u)+psi(v,k)-psi(u,h)-psi(b,v)
        return ((-1)**phase)*chars[i][h]
    R=[[[0]*12 for _ in range(12)] for _ in range(12)]
    for k,ob in enumerate(obs):
        z=ob['z'];K=ob['stab']
        for i,j in product(range(12),repeat=2):
            total=0j
            for a in K:
                c=G[G[inv[z]][a]][z];coef=chars[k][a].conjugate()
                # Sum over every factorization z=x*y. Balanced tensoring
                # identifies |H| such factorizations; divide only at the end.
                for x in range(48):
                    b=G[G[inv[x]][a]][x]
                    if b in hs:total+=coef*trace(i,x,a,b)*trace(j,G[inv[x]][z],b,c)
            den=16*len(K);need(total.imag==0 and total.real>=0 and total.real%den==0,'exact balanced Hom dimension')
            R[i][j][k]=int(total.real)//den
    units=[i for i in range(12) if all(R[i][j][k]==R[j][i][k]==int(j==k) for j,k in product(range(12),repeat=2))]
    need(len(units)==1,'unique unit');p=[units[0]]+[i for i in range(12) if i!=units[0]]
    R=[[[R[a][b][c] for c in p] for b in p] for a in p]
    need(R==record['model_tensor'],'independent all-factorization reconstruction')
    for m in record['matches']:
        S=targets[m['id']];p=m['source_to_model']
        need(all(S[a][b][c]==R[p[a]][p[b]][p[c]] for a,b,c in product(range(12),repeat=3)),'original tensor binding')
    ans.update(full_tensor_coefficients=1728,matches=[m['id'] for m in record['matches']])
    return ans

def main():
    start=time.monotonic();src=HERE/'h16_frozen';cases=json.loads((src/'h16_all_cases.json').read_text());records=json.loads((src/'h16_audit.json').read_text())['cases'];targets=json.loads((FIRST/'tensors.json').read_text())
    need(len(cases)==len(records)==12,'full twelve-case binding')
    out=[one_case(c,r,targets) for c,r in zip(cases,records)]
    need(sum(r['rank']==12 for r in out)==6 and sum(r['rank']==18 for r in out)==6,'six target six wrong-rank categories')
    result=dict(status='PASS',scope='Residual H16 part of the conditional GT catalogue; no universal GT inference',cases=out,seconds=time.monotonic()-start)
    (HERE/'h16_catalog_independent.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',len(out),'cases',result['seconds'])

if __name__=='__main__':main()
