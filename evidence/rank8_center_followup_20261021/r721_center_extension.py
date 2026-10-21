"""Exact, bounded R721 low-center action extension; scratch-only addendum.

This is necessary fusion data, not a center fusion ring or categorification.
Imports and rechecks the preceding fourth-moment certificate. No repo writes.
"""
import contextlib
import io
import itertools
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
with contextlib.redirect_stdout(io.StringIO()):
    import quartic_center_challenge as q

s = q.c.s
need = q.need
R,a,cols,high,sv,ds = q.prepare('R8_3_721',10)
K = a['K']
saved = q.read(q.P/'verlinde_low_721.json')
forced = q.check_721()['high_types']
pairs = q.pairs
words_all = [()] + [(i,) for i in range(1,5)] + pairs


def grouped_spectrum(case):
    inverse = [case['permutation'].index(i) for i in range(5)]
    groups = {}
    for j,(v,d,n) in enumerate(zip(sv,ds,[1]*5+case['multiplicities'])):
        if not n:
            continue
        lam = tuple(v[inverse[i]]/d for i in range(1,5))
        if lam not in groups:
            groups[lam] = [K.zero,0,[]]
        groups[lam][0] += K(n)*d*d/a['D']**2
        groups[lam][1] += n
        groups[lam][2].append(('low',j,n) if j<5 else ('high',j-5,n))
    need(len(groups)==9,'nine distinct simultaneous eigenvalue tuples')
    need(all(a['embedding'].sign(v[0])>0 for v in groups.values()),'positive vacuum weights')
    return groups


reference = grouped_spectrum(saved['cases'][0])
moments = {}


def moment(word):
    key = tuple(sorted(word))
    if key not in moments:
        value = K.zero
        for lam,(weight,mult,labels) in reference.items():
            term = weight
            for i in key:
                term *= lam[i-1]
            value += term
        moments[key] = q.rational(value)
    return moments[key]


def group_projector(n, positions):
    E = s.zeros(n)
    for j in positions:
        for k in positions:
            E[j,k] = int(j==k)-s.Rational(1,len(positions))
    return E


def matching_projector(n, positions, edges):
    E = s.zeros(n)
    for j,k in edges:
        v = s.zeros(n,1)
        v[positions[j]] = 1
        v[positions[k]] = -1
        E += v*v.T/2
    return E


def all_matchings_four():
    edges = list(itertools.combinations(range(4),2))
    result = [()]+[(edge,) for edge in edges]
    result += [pair for pair in itertools.combinations(edges,2) if len(set(sum(pair,())))==4]
    need([sum(len(m)==i for m in result) for i in range(3)] == [1,6,3], 'complete matching domain')
    return result


def build(case):
    spectrum = grouped_spectrum(case)
    need({k:v[0] for k,v in spectrum.items()} == {k:v[0] for k,v in reference.items()},'same nine vacuum weights')
    counts = case['multiplicities']
    types = [i for i,n in enumerate(counts) for _ in range(n)]
    n = 5+len(types)
    lo = {tuple(x['triple']):x['value'] for x in case['coefficients']}
    products = s.Matrix(n,10,lambda r,p: int(pairs[p][0]==pairs[p][1]) if r==0 else
        (lo[tuple(sorted(pairs[p]+(r,)))] if r<5 else forced[types[r-5]]['coefficients'][p]))
    W = s.eye(n)[:,:5].row_join(products)
    inds = W.rref()[1]
    V = W[:,inds]
    words = [words_all[i] for i in inds]
    need(V.cols==9,'entire vacuum cyclic space has dimension nine')
    G = V.T*V
    need(G == s.Matrix(9,9,lambda j,k:moment(words[j]+words[k])),'known word Gram equals spectral moments')
    Gi = G.inv()
    P = V*Gi*V.T
    Q = s.eye(n)-P
    Fs = [V*Gi*s.Matrix(9,9,lambda j,k:moment(words[j]+(i,)+words[k]))*Gi*V.T for i in range(1,5)]
    need(all(F.T==F and F*Q==s.zeros(n) for F in Fs),'fixed symmetric cyclic actions')
    need(all(F*H==H*F for F in Fs for H in Fs),'fixed cyclic actions commute')
    groups = {t:[5+j for j,v in enumerate(types) if v==t] for t in sorted(set(types))}
    A = groups[0] if 0 in groups else groups[1]
    C = groups[4] if 4 in groups else groups[8]
    D = groups[5]
    EA,EC,ED = [group_projector(n,g) for g in (A,C,D)]
    need(Q==EA+EC+ED,'hidden space is the sum of equal-type difference spaces')
    hidden = {tuple(q.rational(x) for x in lam):mult-1 for lam,(weight,mult,labels) in spectrum.items() if mult>1}
    expected = {tuple(map(s.Rational,(-1,0,0,0))):7}
    if len(A)>1: expected[tuple(map(s.Rational,(1,-2,-2,1)))] = len(A)-1
    if len(C)>1: expected[tuple(map(s.Rational,(1,0,0,-1)))] = len(C)-1
    need(hidden==expected,'all hidden simultaneous multiplicities')
    M = s.Matrix.hstack(*(s.Matrix(v) for v in cols),*(s.Matrix((0,)+tuple(high[t][0])) for t in types))
    Ls = [s.Matrix(8,8,lambda k,j:sum(cols[i][u]*R[u][j][k] for u in range(8))) for i in range(1,5)]
    return dict(n=n,counts=counts,permutation=case['permutation'],types=types,products=products,V=V,Q=Q,Fs=Fs,
                A=A,C=C,D=D,EA=EA,EC=EC,ED=ED,M=M,Ls=Ls,hidden=hidden)


def verify_witness(data,PA,PC):
    n = data['n'];Q=data['Q'];Fs=data['Fs'];PD=Q-PA-PC
    for E,rank in [(PA,len(data['A'])-1),(PC,len(data['C'])-1),(PD,7)]:
        need(E.T==E and E*E==E and E*data['V']==s.zeros(n,9),'orthogonal hidden projector')
        need(s.trace(E)==rank,'hidden projector rank')
    need(PA*PC==s.zeros(n),'orthogonal hidden tuple spaces')
    Ns = [Fs[0]-Q+2*(PA+PC),Fs[1]-2*PA,Fs[2]-2*PA,Fs[3]+PA-PC]
    for i,N in enumerate(Ns,1):
        need(N.T==N and all(x.q==1 and x>=0 for x in N),'symmetric nonnegative integer matrix')
        need(N[:,0]==s.eye(n)[:,i],'tensor unit column')
        need(all(N[:,j]==data['products'][:,pairs.index(tuple(sorted((i,j))))] for j in range(1,5)), 'all forced low products')
        need(data['M']*N==data['Ls'][i-1]*data['M'],'exact forgetful intertwining')
    need(all(Ns[i]*Ns[j]==Ns[j]*Ns[i] for i in range(4) for j in range(i+1,4)),'exact pairwise commutation')
    traces=[]
    for i,N in enumerate(Ns,1):
        # Reference multiplicities differ across Gram patterns; use the actual spectrum.
        actual_spectrum=grouped_spectrum({'multiplicities':data['counts'],'permutation':data['permutation']})
        expected1=sum((K(v[1])*lam[i-1] for lam,v in actual_spectrum.items()),K.zero)
        expected2=sum((K(v[1])*lam[i-1]**2 for lam,v in actual_spectrum.items()),K.zero)
        need(s.trace(N)==q.rational(expected1) and s.trace(N*N)==q.rational(expected2),'exact spectral trace and square trace')
        H=N[5:,5:]
        traces.append({'trace':int(s.trace(H)),'trace_square':int(s.trace(H*H)),
                       'largest_coefficient':max(map(int,N))})
    return Ns,traces


def check_case(case):
    d=build(case);n=d['n'];F=d['Fs'];out={'counts':d['counts'],'center_rank':n,'permutation':case['permutation']}
    if len(d['A'])==1 and len(d['C'])==4:
        # PA has rank zero. Thus N2=F2 on the entire space.
        block=F[1].extract(d['C'],d['C'])
        need(block==s.ones(4)*s.Rational(9,2),'forced 9/2 obstruction')
        out.update(status='exact_necessary_pattern_exclusion',fixed_expression='N_A2',
                   labels=d['C'],forced_block=[[str(x) for x in row] for row in block.tolist()])
    elif len(d['A'])==4 and len(d['C'])==1:
        # PC=0, so N1+N2=F1+F2-Q, regardless of PA.
        block=(F[0]+F[1]-d['Q']).extract(d['A'],d['A'])
        need(all(x.q==2 for x in block),'forced half-integral obstruction')
        out.update(status='exact_necessary_pattern_exclusion',fixed_expression='N_A1+N_A2',
                   labels=d['A'],forced_block=[[str(x) for x in row] for row in block.tolist()])
    elif len(d['A'])==len(d['C'])==1:
        Ns,traces=verify_witness(d,s.zeros(n),s.zeros(n))
        out.update(status='unique_exact_necessary_action_tuple',trace_data=traces,
                   matrices=[list(map(list,N.tolist())) for N in Ns])
    else:
        need(len(d['A'])==len(d['C'])==4,'both-split domain')
        # These block constants are the entire input to the row-norm lemma
        # in R721_CENTER_EXTENSION.md, proving no other projectors occur.
        for positions,expected in [(d['A'],[s.Rational(5,4),1,1,s.Rational(3,4)]),
                                   (d['C'],[s.Rational(17,4),s.Rational(9,2),s.Rational(9,2),s.Rational(9,4)])]:
            for Fi,value in zip(F,expected):
                need(Fi.extract(positions,positions)==s.ones(4)*value,'projection-classification block constants')
        choices=all_matchings_four();witnesses=[]
        for ma in choices:
            for mc in choices:
                if len(ma)!=len(mc):continue
                QA=matching_projector(n,d['A'],ma);QC=matching_projector(n,d['C'],mc)
                PA=QA+d['EC']-QC;PC=d['EA']-QA+QC
                Ns,traces=verify_witness(d,PA,PC)
                witnesses.append({'A_matching':ma,'C_matching':mc,'matching_size':len(ma),
                                  'trace_data':traces,
                                  'matrices':[list(map(list,N.tolist())) for N in Ns]})
        need(len(witnesses)==46 and [sum(w['matching_size']==i for w in witnesses) for i in range(3)]==[1,36,9], 'complete 46-tuple matching domain')
        out.update(status='46_exact_necessary_action_tuples_three_permutation_types',A_labels=d['A'],C_labels=d['C'],witnesses=witnesses)
    return out


results=[check_case(case) for case in saved['cases']]
need(len(results)==8,'all four patterns and both assignments')
print(json.dumps({'scope':'necessary low-center action data only; no category, complete center ring, or ring exclusion',
                  'pattern_exclusions':2,'remaining_Gram_patterns':2,
                  'case_results':results},indent=2,default=int))
