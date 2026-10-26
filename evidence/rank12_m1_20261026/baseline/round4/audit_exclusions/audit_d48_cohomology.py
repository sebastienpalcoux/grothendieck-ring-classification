"""Independent checks underlying the D48 relative-cohomology coverage proof.

Reuses only the explicit cocycle constructors. Rechecks all cocycle identities,
cohomological cycle evaluations, subgroup Schur classes and structural maps.
No fusion-model search is performed and no other directory is written.
"""
from pathlib import Path
from collections import Counter
import sys,json,itertools
sys.dont_write_bytecode=True
import numpy as np
HERE=Path(__file__).resolve().parent;D48=HERE.parent/'d48'
sys.path.insert(0,str(D48))
from h8_models import s4_cocycles,schur_cover
def need(x,m):
    if not x:raise ValueError(m)
def order(G,a):
    x=a;n=1
    while x:x=G[x][a];n+=1
    return n
def cocycle(G,W,mod):
    G=np.asarray(G);n=len(G);b=np.arange(n)[:,None,None];c=np.arange(n)[None,:,None];d=np.arange(n)[None,None,:]
    need(not W[0].any() and not W[:,0].any() and not W[:,:,0].any(),'normalized')
    for a in range(n):
        delta=W-W[G[a,:,None,None],c,d]+W[a,G[:,:,None],d]-W[a,b,G[None,:,:]]+W[a,:,:,None]
        need(not (delta%mod).any(),'all 3-cocycle identities')
def cyc(G,W,mod):
    out=[]
    for a in range(len(G)):
        power=0;v=0
        for _ in range(order(G,a)):
            v+=int(W[a,power,a]);power=G[power][a]
        out.append(v%mod)
    return out
def alternating(W,xyz):
    return sum((1 if p in [(0,1,2),(1,2,0),(2,0,1)] else -1)*int(W[tuple(xyz[i] for i in p)]) for p in itertools.permutations(range(3)))%8
ps,S,vs=s4_cocycles();ps2,S2,beta=schur_cover()
need(ps==ps2 and S==S2 and len(vs)==8,'common S4 coordinates, eight cocycles')
for bits,V in vs:cocycle(S,V,4)
need(len({tuple(cyc(S,V,4)) for _,V in vs})==8,'eight distinct S4 classes')
idx={p:i for i,p in enumerate(ps)}
par=[sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2 for p in ps]
pairs=json.loads((D48/'h8_pairs.json').read_text())+json.loads((D48/'h4_pairs.json').read_text())
frozen=json.loads((D48/'cohomology_fingerprints.json').read_text());group_receipts=[];pair_receipts=[]
for gi in [28,29,30,48]:
    fam=[r for r in pairs if r['smallgroup'][1]==gi];row=fam[0];G=row['table'];n=len(G)
    need(n==48 and all(r['table']==G for r in fam),'common exact group table')
    pr=np.array([idx[tuple(v-1 for v in p)] for p in row['projection_permutations']]);q=np.array(row['quotient_character']);sg=np.array(par)[pr]
    need(len(set(pr))==24 and all(pr[G[a][b]]==S[pr[a]][pr[b]] for a,b in itertools.product(range(n),repeat=2)),'central S4 quotient')
    ker=[a for a in range(n) if pr[a]==0]
    need(len(ker)==2 and all(G[a][b]==G[b][a] for a in ker for b in range(n)),'central kernel order two')
    if gi==48:
        need(all(q[G[a][b]]==(q[a]+q[b])%2 for a,b in itertools.product(range(n),repeat=2)),'C2 character')
        need(len({(int(pr[a]),int(q[a])) for a in range(n)})==48,'explicit S4 times C2 isomorphism')
    if gi==30:
        need(all(q[G[a][b]]==(q[a]+q[b])%4 for a,b in itertools.product(range(n),repeat=2)),'C4 quotient')
        N=[a for a in range(n) if q[a]==0]
        need(len(N)==12 and {int(pr[a]) for a in N}=={i for i in range(24) if not par[i]},'kernel explicitly A4')
        need(any(q[a]==1 and order(G,a)==4 for a in range(n)),'C4 quotient split')
    if gi==29:
        N=[a for a in range(n) if sg[a]==0]
        need(len(N)==24 and any(sg[a] and order(G,a)==2 for a in range(n)),'index two kernel and determinant section')
        H=row['subgroup'];K=set(H)&set(N)
        need(len(K)==4 and any(order(G,a)==4 for a in K),'D8 intersection with kernel cyclic order four')
    for hrow in fam:
        H=hrow['subgroup'];o=Counter(order(G,a) for a in H);comm=all(G[a][b]==G[b][a] for a,b in itertools.product(H,repeat=2))
        typ='C4' if len(H)==4 and o[4] else 'V4' if len(H)==4 else 'C2^3' if o[2]==7 else 'C4xC2' if comm else 'Q8' if o[2]==1 else 'D8'
        expected={'C4':1,'V4':2,'C2^3':8,'C4xC2':2,'Q8':1,'D8':2}[typ]
        hi={a:i for i,a in enumerate(H)};fps=set()
        need(all(G[a][b] in hi for a,b in itertools.product(H,repeat=2)),'subgroup closure')
        for P in hrow['schur_cocycles']:
            need(all((P[hi[b]][hi[c]]+P[hi[a]][hi[G[b][c]]]-P[hi[G[a][b]]][hi[c]]-P[hi[a]][hi[b]])%2==0 for a,b,c in itertools.product(H,repeat=3)),'all Schur 2-cocycle identities')
            fps.add(tuple((P[i][j]-P[j][i])%2 for i,a in enumerate(H) for j,b in enumerate(H) if G[a][b]==G[b][a]))
        need(len(fps)==len(hrow['schur_cocycles'])==expected,'all Schur classes distinct and cardinality complete')
        pair_receipts.append({'smallgroup':[48,gi],'subgroup':H,'subgroup_type':typ,'Schur_classes':expected,'status':'PASS'})
    if gi not in [30,48]:continue
    B=np.asarray(beta)[pr[:,None],pr[None,:]]
    extras=[4*q[:,None,None]*q[None,:,None]*q[None,None,:],4*sg[:,None,None]*q[None,:,None]*q[None,None,:],4*q[:,None,None]*B[None,:,:]] if gi==48 else [2*q[:,None,None]*((q[None,:,None]+q[None,None,:])//4)]
    for W in extras:cocycle(G,W%8,8)
    old=next(r for r in frozen if r['smallgroup'][1]==gi);triples=old['commuting_triples']
    need(triples==[list(t) for t in itertools.combinations(range(1,n),3) if all(G[a][b]==G[b][a] for a,b in itertools.combinations(t,2))],'exact commuting triples')
    fingerprints={};choices=list(itertools.product(range(2),repeat=3)) if gi==48 else [(k,) for k in range(4)]
    for bits,V in vs:
        base=2*V[pr[:,None,None],pr[None,:,None],pr[None,None,:]]
        for coefficients in choices:
            W=(base+sum((c*e for c,e in zip(coefficients,extras)),np.zeros_like(base)))%8
            fp=cyc(G,W,8)+[alternating(W,xyz) for xyz in triples]
            match=next(r for r in old['rows'] if r['parameters']['bits']==list(bits) and r['parameters']['extra']==list(coefficients))
            need(fp==match['fingerprint'],'every saved fingerprint independently recomputed')
            fingerprints.setdefault(tuple(fp),[]).append([list(bits),list(coefficients)])
    bound=64 if gi==48 else 16
    need(len(fingerprints)==bound,'reaches theoretical cohomology upper bound')
    group_receipts.append({'smallgroup':[48,gi],'parameter_choices':len(vs)*len(choices),'distinct_U1_classes':len(fingerprints),'theoretical_upper_bound':bound,'status':'PASS'})
need(len(pair_receipts)==10,'ten complete candidate pairs')
out={'status':'PASS','S4_two_primary_classes':8,'full_cohomology_groups':group_receipts,'subgroup_Schur_class_checks':pair_receipts,'scope':'Exact cocycles, invariants, quotient maps and all subgroup Schur classes; periodic-cover arguments and LHS bounds in audit_d48_cohomology.md. Fusion-model exhaustion is separately owned by D48 agent.'}
(HERE/'audit_d48_cohomology.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS D48: all cocycle identities; 8/16/64 distinct classes; complete Schur classes for ten pairs')
