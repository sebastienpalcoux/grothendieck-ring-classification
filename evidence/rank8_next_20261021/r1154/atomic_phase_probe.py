"""Exact linear constraints on actual twist sums per high restriction type."""
import sys,json,itertools
from pathlib import Path
UP=Path(__file__).resolve().with_name('triple_projection.py')
exec(compile(UP.read_text().split('failures=[];')[0],str(UP),'exec'))
action_receipt=json.load(open(HERE/'a2_action_probe.json'))
need(action_receipt['verifier_sha256']==digest(HERE/'a2_action_probe.py'),'action verifier binding')
chs=chars;highvals=[[md.value(ch,(0,)+tuple(v),K)for ch in chs]for v in domain['high_columns']]
lowvals=[[md.value(ch,v,K)for ch in chs]for v in cols]
def rrefK(A):
    A=[r[:]for r in A];at=0;pivs=[]
    for j in range(len(A[0])-1):
        k=next((k for k in range(at,len(A))if A[k][j]!=K.zero),None)
        if k is None:continue
        A[at],A[k]=A[k],A[at];pivot=A[at][j];A[at]=[v/pivot for v in A[at]]
        for k in range(len(A)):
            if k!=at and A[k][j]!=K.zero:
                f=A[k][j];A[k]=[v-f*w for v,w in zip(A[k],A[at])]
        pivs.append(j);at+=1
    need(all(any(v!=K.zero for v in r[:-1])or r[-1]==K.zero for r in A),'consistent phase sums')
    return A[:at],pivs
out=[]
for ix in action_receipt['surviving_pattern_indices']:
    counts=domain['completions'][ix];types=[i for i,n in enumerate(counts)if n];rows=[]
    for E,F in itertools.combinations_with_replacement(range(5),2):
        target=a['codegrees'][F]*K(a['multiplicities'][F])*md.value(chs[E],cols[F],K)-sum((v[E]*v[F]for v in lowvals),K.zero)
        rows.append([highvals[i][E]*highvals[i][F]for i in types]+[target])
    rr,pivs=rrefK(rows);free=[j for j in range(len(types))if j not in pivs];forced=[]
    for ir,j in enumerate(pivs):
        if all(rr[ir][k]==K.zero for k in free):
            val=rr[ir][-1];forced.append({'type':types[j],'multiplicity':counts[types[j]],'sum':c.ec(val),'unit_norm_if_singleton':val*val==K.one})
    out.append({'index':ix,'types':types,'rank':len(pivs),'free_types':[types[k]for k in free],'forced':forced,'rref':[[c.ec(v)for v in r]for r in rr]})
print(json.dumps({'schema':'r1154-atomic-phase-probe/v1','results':out},indent=2))
