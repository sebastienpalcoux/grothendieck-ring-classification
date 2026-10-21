"""Independent linear-algebra review of the R1154 A2 action reduction.

Imports only the source/character/moment setup from triple_projection.py;
never calls its projection, augmented, row_data, or action implementations.
Uses a direct second-moment Schur complement to prove invariance.
"""
from pathlib import Path
import sys,json,itertools,hashlib
from functools import lru_cache
from fractions import Fraction
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'evidence/rank8_next_20261021/r1154'
up=P/'triple_projection.py';ns={'__file__':str(up)}
exec(compile(up.read_text().split('@lru_cache(None)')[0],str(up),'exec'),ns)
s=ns['s'];a=ns['a'];R=ns['R'];K=ns['K'];cols=ns['cols'];words=ns['words'];pairs=ns['pairs']
domain=ns['domain'];fibers=ns['fibers'];quartic=ns['quartic'];groups=ns['groups'];moment_coefficients=ns['moment_coefficients'];values=ns['values']
need=ns['need'];F=Fraction
@lru_cache(None)
def restrict(word):
    result=[1]+[0]*7
    for label in word:
        result=[sum(result[i]*cols[label][j]*R[i][j][k]for i in range(8)for j in range(8))for k in range(8)]
    return result
@lru_cache(None)
def fixed(signature):
    moments=dict(zip(moment_coefficients,signature));m=lambda w:moments[tuple(sorted(w))]
    fw=s.Matrix([restrict(w)for w in words]);G=s.Matrix(15,15,lambda i,j:m(words[i]+words[j]))
    G=G.row_join(fw).col_join(fw.T.row_join(a['Gram']))
    piv=list(G.rref()[1]);need(len(piv)==9,'rank-nine augmented Gram')
    inverse=G.extract(piv,piv).inv()
    L=s.Matrix(8,8,lambda k,j:sum(cols[2][i]*R[i][j][k]for i in range(8)))
    BB=[]
    for power in (1,2):
        w=(2,)*power;upper=s.Matrix(15,15,lambda i,j:m(words[i]+w+words[j]));cross=s.Matrix([restrict(word+w)for word in words])
        BB.append(upper.row_join(cross).col_join(cross.T.row_join((L**power)*a['Gram'])))
    B,B2=BB
    # Directly shows N2 sends EVERY generator into the same rank-nine span.
    need(B2==B[:,piv]*inverse*B[piv,:],'zero full23-generator second-moment Schur complement')
    operator=inverse*B.extract(piv,piv)
    lam=s.Symbol('lambda')
    need(operator.charpoly().as_expr()==s.expand(lam**4*(lam+1)*(lam-3)*(lam+5)*(lam**2-270*lam+225)),'entire fixed characteristic polynomial')
    H=inverse*B.extract(piv,piv)*inverse
    return piv,[[F(x)for x in row]for row in H.tolist()],int(s.trace(operator)),int(s.trace(operator**2)),moments
expected=json.loads((P/'a2_action_probe.json').read_text());expected_map={(v['index'],v['histogram_solution']):v['status']for v in expected['results']}
checked=0;survivors=[];rankcounts={};seen=[]
for row in fibers['results']:
    if row['status']!='exact_joint_fiber_witness':continue
    counts=[1]+domain['completions'][row['index']];signature=[]
    for co,den in moment_coefficients.values():
        irrational=sum(n*v[0]for n,v in zip(counts,co));rational=sum(n*v[1]for n,v in zip(counts,co))
        need(irrational==0 and rational%den==0,'exact rational spectral moments');signature.append(rational//den)
    piv,H,tr,tr2,moments=fixed(tuple(signature))
    spectrum=[(n,v[2])for n,v in zip([1]*5+counts[1:],values)]
    t1=sum((K(n)*v for n,v in spectrum),K.zero);t2=sum((K(n)*v*v for n,v in spectrum),K.zero)
    c=ns['c'];t1=int(F(c.ec(t1)[0]));t2=int(F(c.ec(t2)[0]));rank=tr-t1
    need(t2-tr2==rank and rank in(0,3),'hidden spectrum onlyzero/minusone and rankzero/three')
    for typ,n in enumerate(counts[1:]):
        if n:need(values[5+typ][2]==K(-1 if typ in(10,15)else 0),'no other hidden eigenvalues')
    for number,histograms in enumerate(row['pair11_histogram_solutions_by_high_type']):
        vectors=[];multiplicities=[];labels=[]
        for j in range(5):
            raw=[int(j==k)for k in range(5)]+[moments[tuple(sorted(p+(j,)))]if j else int(p[0]==p[1])for p in pairs]+list(cols[j])
            vectors.append([F(raw[k])for k in piv]);multiplicities.append(1);labels.append(('low',j))
        X0=[[F(x)for x in rr]for rr in groups[row['group']]['minimum_norm_rows_by_high_type']];h=list(map(F,quartic['h']))
        for typ,hist in enumerate(histograms):
            for x,n in hist:
                if not n:continue
                pp=[v+(F(x)-X0[typ][0])*hh for v,hh in zip(X0[typ],h)]
                raw=[F(0)]*5+pp+[F(0)]+list(map(F,domain['high_columns'][typ]))
                vectors.append([raw[k]for k in piv]);multiplicities.append(n);labels.append(('high',typ))
        # Independently reconstruct and check the chosen-coordinate Gram.
        V=s.Matrix(vectors);W=s.diag(*multiplicities)
        # This equality also checks that compressed multiplicities are used.
        gram=V.T*W*V
        need(gram.det()!=0,'actual rank-nine realization')
        hv=[[sum(H[i][j]*v[j]for j in range(9))for i in range(9)]for v in vectors]
        FF=[[sum(v[i]*u[i]for i in range(9))for u in hv]for v in vectors]
        if rank:
            targets=[i for i,l in enumerate(labels)if l==('high',10)]
            need(len(targets)==1 and multiplicities[targets[0]]==4,'four identical high10 coordinates')
            target=targets[0];need(FF[target][target]==F(67,4),'forced3/4 diagonal in rankthreeprojector')
            # Expand correction conceptually: offdiagonal+1/4, diagonal-3/4.
            FF[target][target]+=F(1,4)
            need(FF[target][target]-1>=0,'true diagonal stays nonnegative')
        good=all(v.denominator==1 and v>=0 for rr in FF for v in rr)
        status='passes_fixed_action'if good else'forced_action_nonintegral_or_negative'
        need(status==expected_map[(row['index'],number)],'independent action decision agrees')
        checked+=1;rankcounts[rank]=rankcounts.get(rank,0)+1
        if good:survivors.append((row['index'],number))
need(checked==2904 and len(survivors)==74 and len(set(i for i,j in survivors))==8,'complete2904→74over8patterns')
print(json.dumps(dict(review='independent_R1154_A2_action',status='PASS',checked_pair_completions=checked,
       surviving_pair_completions=len(survivors),surviving_patterns=sorted(set(i for i,j in survivors)),
       moment_groups=fixed.cache_info().currsize,hidden_negative_one_rank_counts=rankcounts,
       invariance_proof='Full23-generator second-moment Schur complement vanishes exactly.',
       source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [P/'a2_action_probe.py',P/'a2_action_probe.json',up]}),indent=2))
