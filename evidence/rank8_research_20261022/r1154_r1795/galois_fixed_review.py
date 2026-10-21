"""Exact transport enumeration with A2 and A4 fixed by Galois covariance.

Only source tensors/characters and frozen pair histograms are imported.
No discovery Galois script or permutation routine is imported. The extension
of quadratic conjugation to the full cyclotomic field is NOT assumed to be
an involution. Arbitrary signed permutations are covered by integral
transport tables between identical known-row classes.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from functools import lru_cache
import hashlib,itertools,json,math,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'evidence/rank8_next_20261021/r1154'
up=P/'triple_projection.py';ns={'__file__':str(up)}
exec(compile(up.read_text().split('moment_coefficients={}')[0],str(up),'exec'),ns)
K=ns['K'];a=ns['a'];c=ns['c'];dims=ns['dims'];values=ns['values']
cols=ns['cols'];domain=ns['domain'];fibers=ns['fibers'];quartic=ns['quartic'];groups=ns['groups']

def need(ok,msg):
    if not ok:raise ValueError(msg)
def key(z):
    v=tuple(map(F,c.ec(z)))
    return (F(0),)*(2-len(v))+v
def conjugate(z):
    u,v=key(z)
    return K(u.numerator)/K(u.denominator)*(K(1684)-K([1,0]))+K(v.numerator)/K(v.denominator)
def rational(z):
    u,v=key(z);need(u==0 and v.denominator==1,'integer exact moment');return int(v)
def add(x,y):return tuple(a+b for a,b in zip(x,y))

need(K.mod.to_list()==[K.dom(1),K.dom(-1684),K.dom(28159)],'quadratic field polynomial')
need(conjugate(conjugate(K([1,0])))==K([1,0]),'quadratic conjugation')
initial=json.loads((P/'a2_action_probe.json').read_text())
cases=[r for r in initial['results']if r['status']=='passes_fixed_action'and r['index']in(6971,8766,8772)]
need(len(cases)==36,'all accepted surviving pair histograms')

@lru_cache(None)
def transports(rows,columns):
    """All nonnegative integral matrices with prescribed ordered margins."""
    nr,nc=len(rows),len(columns);out=[]
    def vectors(total,bounds,j=0,prefix=()):
        if j==len(bounds)-1:
            if 0<=total<=bounds[j]:yield prefix+(total,)
            return
        for x in range(max(0,total-sum(bounds[j+1:])),min(total,bounds[j])+1):
            yield from vectors(total-x,bounds,j+1,prefix+(x,))
    def visit(i,remaining,partial):
        if i==nr-1:
            if sum(remaining)==rows[i]:out.append(partial+(remaining,))
            return
        for v in vectors(rows[i],remaining):visit(i+1,tuple(a-b for a,b in zip(remaining,v)),partial+(v,))
    if sum(rows)==sum(columns):visit(0,columns,())
    return tuple(out)

def solve(case):
    ix=case['index'];histid=case['histogram_solution']
    fr=next(r for r in fibers['results']if r['index']==ix)
    hist=fr['pair11_histogram_solutions_by_high_type'][histid]
    counts=[1]*5+domain['completions'][ix]
    occupied=[i for i,n in enumerate(counts)if n]
    for i in occupied:need(conjugate(values[i][1])*values[i][1]==K.one,'reciprocal A1 eigenvalue')
    def moment(w):
        z=K.zero
        for n,d,vs in zip(counts,dims,values):
            term=K(n)*d*d/(a['D']**2)
            for i in w:term*=vs[i]
            z+=term
        return rational(z)
    # Each record is one class of identical Y rows, except every low label
    # stays individual because the right side G[0:5,0:5] distinguishes it.
    records=[]
    for i in range(5):
        Y=(int(i==1),)+tuple(moment((1,j,i))if i else int(j==1)for j in range(1,5))
        records.append({'type':i,'low':i,'n':1,'y':Y})
    X0=[[F(z)for z in rr]for rr in groups[fr['group']]['minimum_norm_rows_by_high_type']]
    h=list(map(F,quartic['h']))
    for typ,hh in enumerate(hist):
        for x,n in hh:
            if not n:continue
            pp=[v+(F(x)-X0[typ][0])*hj for v,hj in zip(X0[typ],h)]
            need(all(v.denominator==1 and v>=0 for v in pp),'integer pair row')
            records.append({'type':5+typ,'low':None,'n':n,'y':(0,)+tuple(int(v)for v in pp[:4]),'pair11':x})
    need(sum(r['n']for r in records)==sum(counts),'expanded rank')
    Ylow=[r['y']for r in records[:5]]
    need(all(Ylow[i][j]==Ylow[j][i]for i in range(5)for j in range(5)),'symmetric low N1 block')
    # Check every known column scalar product directly against the complete
    # modular spectrum, independently of the histogram discovery code.
    for i in range(5):
        for j in range(5):
            word=(1,1)+(()if i==0 else(i,))+(()if j==0 else(j,))
            need(sum(r['n']*r['y'][i]*r['y'][j]for r in records)==moment(word),'known five-column Gram')
    vac=[d/a['D']for d in dims]
    clusters=defaultdict(list)
    for i,r in enumerate(records):clusters[key(vac[r['type']])].append(i)
    clusterkeys=sorted(clusters)
    blocks=[];dimension_maps=[]
    for k in clusterkeys:
        rr=clusters[k];z=conjugate(vac[records[rr[0]]['type']]);choices=[]
        for kk in clusterkeys:
            zz=vac[records[clusters[kk][0]]['type']]
            for eps in(1,-1):
                if z==eps*zz:choices.append((kk,eps))
        need(len(choices)==1,'unique signed target dimension cluster')
        target,eps=choices[0];cc=clusters[target]
        rowmargin=tuple(records[i]['n']for i in rr);colmargin=tuple(records[j]['n']for j in cc)
        need(sum(rowmargin)==sum(colmargin),'dimension-cluster cardinalities agree')
        tables=transports(rowmargin,colmargin);effects={}
        for table in tables:
            if any(table[ii][jj] and (records[i]['low'] in (2,4) or records[j]['low'] in (2,4)) and records[i]['low'] != records[j]['low'] for ii,i in enumerate(rr) for jj,j in enumerate(cc)):
                continue
            effect=[0]*25
            for ii,i in enumerate(rr):
                for jj,j in enumerate(cc):
                    n=table[ii][jj]
                    if not n:continue
                    r,s=records[i],records[j]
                    for p in range(5):
                        for q in range(5):effect[5*p+q]+=eps*n*r['y'][p]*s['y'][q]
                    if r['low']is not None and s['low']is not None:effect[5*r['low']+s['low']]-=eps*n
            effects.setdefault(tuple(effect),table)
        blocks.append((tuple(effects),effects,rr,cc))
        dimension_maps.append({'source_types':sorted({records[i]['type']for i in rr}),
          'target_types':sorted({records[j]['type']for j in cc}),'sign':eps,
          'transport_tables':len(tables),'distinct_effects':len(effects)})
    # Balance products of effect-domain sizes, then enumerate both halves.
    sides=[[],[]];sizes=[1,1]
    for block in sorted(blocks,key=lambda b:len(b[0]),reverse=True):
        j=0 if sizes[0]<=sizes[1]else 1;sides[j].append(block);sizes[j]*=len(block[0])
    def sums(bs):
        states={(0,)*25:()}
        for effects,_,_,_ in bs:
            nxt={}
            for old,choices in states.items():
                for num,effect in enumerate(effects):nxt.setdefault(add(old,effect),choices+(num,))
            states=nxt
        return states
    left=sums(sides[0]);right=sums(sides[1]);match=None
    for x,xx in left.items():
        y=tuple(-v for v in x)
        if y in right:match=(xx,right[y]);break
    witness=None
    if match is not None:
        selected=[]
        for bs,choices in zip(sides,match):
            for block,n in zip(bs,choices):
                effects,lookup,rr,cc=block;e=effects[n]
                selected.append({'source_classes':rr,'target_classes':cc,'table':lookup[e]})
        # Expand the compressed solution to an actual labelled signed
        # permutation and directly recheck the advertised five-column equation.
        positions=[];expanded=[]
        for rec in records:
            positions.append(list(range(len(expanded),len(expanded)+rec['n'])))
            expanded.extend([rec]*rec['n'])
        permutation=[None]*len(expanded);signs=[None]*len(expanded)
        source_used=[0]*len(records);target_used=[0]*len(records)
        for item in selected:
            rr,cc,table=item['source_classes'],item['target_classes'],item['table']
            for ii,i in enumerate(rr):
                for jj,j in enumerate(cc):
                    z=conjugate(vac[records[i]['type']]);zz=vac[records[j]['type']]
                    eps=1 if z==zz else -1
                    need(z==eps*zz,'expanded witness sign')
                    for _ in range(table[ii][jj]):
                        src=positions[i][source_used[i]];dst=positions[j][target_used[j]]
                        source_used[i]+=1;target_used[j]+=1
                        permutation[src]=dst;signs[src]=eps
        need(sorted(permutation)==list(range(len(expanded))),'expanded witness is a permutation')
        need(source_used==target_used==[r['n']for r in records],'all transport margins used')
        for p in range(5):
            for q in range(5):
                lhs=sum(signs[i]*r['y'][p]*expanded[permutation[i]]['y'][q]for i,r in enumerate(expanded))
                rhs=signs[p]if permutation[p]==q else 0
                need(lhs==rhs,'direct labelled Y-transpose G Y equals low G')
        witness={'classes':records,'transports':selected,'expanded_permutation':permutation,'expanded_signs':signs}
    return {'index':ix,'histogram_solution':histid,'rank':sum(counts),
      'status':'passes_Galois_low_columns'if match is not None else'Galois_low_columns_impossible',
      'dimension_maps':dimension_maps,'raw_half_combinations':sizes,
      'distinct_half_sums':[len(left),len(right)],'witness':witness}

results=[]
for case in cases:
    result=solve(case);results.append(result)
    print(json.dumps({k:result[k]for k in('index','histogram_solution','status','raw_half_combinations','distinct_half_sums')}),file=sys.stderr,flush=True)
sources=[up,P/'a2_action_probe.json',P/'joint_quartic_fibers.json',ns['domainpath'],ns['quarticpath']]
out={'schema':'r1154-galois-fixed-a2-a4-transport/v1','status':'PASS',
 'id':'R8_3_1154','tensor_sha256':ns['r']['tensor_sha256'],
 'scope':'Necessary signed Galois permutation on five known A1 columns, fixing A2 and A4 as forced by covariance of N2 and N4+N1; no Galois involution assumed; no categorification assertion.',
 'checked_pair_histograms':len(results),'survivors':sum(r['witness']is not None for r in results),
 'results':results,'source_sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in sources},
 'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(out,indent=2,default=str))
