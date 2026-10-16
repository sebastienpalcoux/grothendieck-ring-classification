"""Replay all34 involution applicability and four exact necessary Gram witnesses.

Self-contained except SymPy and the Python standard library. No optimizer,
legacy supplement imports, or assertions are used. Passing is not existence.
"""
import argparse,collections,gzip,hashlib,itertools,json,math
from fractions import Fraction as Q
from pathlib import Path
import sympy as s

SUFFIXES=[24,33,36,37,76,152,153,166,170,190,314,318,319,320,342,368,370,412,432,446,489,495,535,630,666,671,735,758,760,820,869]
IDS=['R8_1_9','R8_1_18','R8_1_49']+[f'R8_2_{i}' for i in SUFFIXES]
NEW_EIGHT={318,319,320,368,370,735,758,760}
FOUR={342,630,666,671}

def need(ok,message):
    if not ok:raise ValueError(message)

def mul(A,B,f):return tuple(sum(A[i*f+k]*B[k*f+j] for k in range(f)) for i in range(f) for j in range(f))
def transpose(A,f):return tuple(A[j*f+i] for i in range(f) for j in range(f))

def generated(R,seed):
    n=len(R);rows=[tuple(int(i==0) for i in range(n))];words=[()];at=0;V=s.Matrix(rows)
    while at<len(words):
        for j in seed:
            row=tuple(sum(rows[at][a]*R[a][j][b] for a in range(n)) for b in range(n));U=V.col_join(s.Matrix([row]))
            if U.rank()>len(rows):rows.append(row);words.append(words[at]+(j,));V=U
            if len(rows)==n:return words,V.inv()
        at+=1
    return None

def all_anti(R,g,fixed):
    """Complete bounded integral domain; three generators, not legacy two."""
    n=len(R);f=len(fixed);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    need(all(R[i][j]==R[j][i] for i in range(n) for j in range(n)),'commutative f2 source')
    I=tuple(int(i==j) for i in range(f) for j in range(f));Z=(0,)*(f*f);sets={0:[I]}
    for i in range(1,n):
        positions=[(a,b) for a in range(f) for b in range(f) if du[i]!=i or a<=b]
        bounds=[R[i][fixed[a]][fixed[b]] for a,b in positions]
        coeff=[int(c) for c in s.Poly(s.Matrix(R[i]).charpoly().as_expr()).sqf_part().all_coeffs()]
        regular=s.Matrix(R[i]);annihilator=s.zeros(n)
        for c in coeff:annihilator=annihilator*regular+c*s.eye(n)
        need(annihilator==s.zeros(n),'source squarefree annihilator')
        out=[]
        for vals in itertools.product(*(range(-b,b+1,2) for b in bounds)):
            v=[0]*(f*f)
            for (a,b),x in zip(positions,vals):
                v[a*f+b]=x
                if du[i]==i:v[b*f+a]=x
            v=tuple(v)
            if mul(v,transpose(v,f),f)!=mul(transpose(v,f),v,f):continue
            p=Z
            for c in coeff:p=tuple(x+c*y for x,y in zip(mul(p,v,f),I))
            if p==Z:out.append(v)
        sets[i]=out
    choices=[];two_generator_found=False
    for count in range(1,4):
        for seed in itertools.combinations(range(1,n),count):
            info=generated(R,seed)
            if info:choices.append((math.prod(len(sets[i]) for i in seed),seed,info))
        if choices:
            two_generator_found=count<=2
            break
    need(bool(choices),'missing finite presentation')
    nodes,seed,(words,inv)=min(choices,key=lambda x:(x[0],x[1]));allowed={i:set(v) for i,v in sets.items()};out=set()
    for values in itertools.product(*(sets[i] for i in seed)):
        given=dict(zip(seed,values))
        if any(mul(given[i],given[j],f)!=mul(given[j],given[i],f) for i in seed for j in seed):continue
        images=[]
        for word in words:
            v=I
            for i in word:v=mul(v,given[i],f)
            images.append(v)
        mats=[]
        for i in range(n):
            v=tuple(sum(inv[i,j]*images[j][a] for j in range(n)) for a in range(f*f))
            if v not in allowed[i]:break
            mats.append(tuple(int(x) for x in v))
        if len(mats)!=n:continue
        if any(transpose(mats[i],f)!=mats[du[i]] for i in range(n)):continue
        if any(mul(mats[i],mats[j],f)!=tuple(sum(R[i][j][k]*mats[k][a] for k in range(n)) for a in range(f*f)) for i in range(n) for j in range(n)):continue
        gauges=[tuple(tuple(signs[a]*signs[b]*T[a*f+b] for a in range(f) for b in range(f)) for T in mats) for signs in itertools.product((-1,1),repeat=f)]
        out.add(min(gauges))
    return sorted(out),{'generators':list(seed),'generator_tuples':nodes,'legacy_two_generator_domain_available':two_generator_found,'anti_representations_up_to_sign_gauge':len(out)}

def modules(R,g,fixed,T):
    done=set();labels=[];n=len(R);f=len(fixed)
    for x in range(n):
        if x in done:continue
        if x in fixed:labels.extend([(x,1),(x,-1)]);done.add(x)
        else:
            y=next(j for j,c in enumerate(R[x][g]) if c);labels.append((x,0));done.update((x,y))
    F={x:k for k,x in enumerate(fixed)};Ms=[]
    for i in range(n):
        M=[]
        for x,sx in labels:
            row=[]
            for y,sy in labels:
                if sx and sy:
                    v=R[i][x][y]+sx*sy*T[i][F[x]*f+F[y]];need(v%2==0 and v>=0,'split multiplicity');v//=2
                elif not sx and not sy:
                    xg=next(k for k,c in enumerate(R[x][g]) if c);v=R[i][x][y]+R[i][xg][y]
                else:v=R[i][x][y]
                row.append(v)
            M.append(row)
        Ms.append(s.Matrix(M))
    r=len(labels);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    need(Ms[0]==s.eye(r),'module identity')
    need(all(Ms[i].T==Ms[du[i]] for i in range(n)),'module transpose')
    need(all(Ms[i]*Ms[j]==sum((R[i][j][k]*Ms[k] for k in range(n)),s.zeros(r)) for i in range(n) for j in range(n)),'module relations')
    return labels,Ms

def arithmetic(index):
    if index==342:return 2,[(1,0),(2,2),(2,2),(2,2),(3,2),(1,0),(3,2),(4,2)]
    if index==666:return 2,[(1,0),(1,0),(2,2),(3,2),(3,2),(2,2),(2,2),(4,2)]
    if index==630:return 10,[(1,0),(1,0),(2,1),(3,1),(3,1),(2,1),(4,1),(4,1)]
    if index==671:return 10,[(1,0),(1,0),(3,1),(4,1),(4,1),(3,1),(2,1),(2,1)]
    raise ValueError('unknown arithmetic')

def verify_grams(R,index,g,fixed,T,branch):
    q,ds=arithmetic(index);ds=[tuple(map(Q,d)) for d in ds]
    multiply=lambda a,b:(a[0]*b[0]+q*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    for i,j in itertools.product(range(8),repeat=2):need(multiply(ds[i],ds[j])==tuple(sum(R[i][j][k]*ds[k][a] for k in range(8)) for a in (0,1)),'positive dimension character')
    need(all(a>=0 and b>=0 and a+b>0 for a,b in ds),'positive FP dimensions')
    labels,Ms=modules(R,g,fixed,T);r=len(labels);dims=[tuple(d/(2 if sign else 1) for d in ds[x]) for x,sign in labels]
    weighted=lambda v:tuple(sum(v[i]*dims[i][a] for i in range(r)) for a in (0,1))
    done=set();dualcols=[]
    for i in range(r):
        if i in done:continue
        j=next(j for j in range(r) if Ms[g][i,j]);need(sum(Ms[g][i,jj] for jj in range(r))==1 and Ms[g][j,i]==1,'involution permutation')
        v=[0]*r;v[i]=1
        if i==j:dualcols.extend([v[:],v[:]])
        else:v[j]=1;dualcols.append(v)
        done.update((i,j))
    B=s.Matrix.hstack(*map(s.Matrix,dualcols));need(B*B.T==s.eye(r)+Ms[g],'distinguished Gram')
    dualdims=collections.Counter(weighted(v) for v in dualcols);dualdims[(Q(1),Q(0))]-=1
    if not dualdims[(Q(1),Q(0))]:del dualdims[(Q(1),Q(0))]
    need([v['module_simple'] for v in branch['gram_witnesses']]==list(range(1,r)),'all non-unit module objects')
    for witness in branch['gram_witnesses']:
        m=witness['module_simple'];columns=witness['columns']
        need(all(len(v)==r and all(isinstance(x,int) and x>=0 for x in v) and any(v) for v in columns),'nonnegative nonzero integral columns')
        Qm=sum((int(Ms[i][m,m])*Ms[i] for i in range(8)),s.zeros(r));Qm[m,m]-=1
        B=s.Matrix.hstack(*map(s.Matrix,columns));need(B*B.T==Qm,'exact Gram factorization')
        expected=collections.Counter({multiply(d,dims[m]):count for d,count in dualdims.items()})
        need(collections.Counter(weighted(v) for v in columns)==expected,'dual dimension class counts')
    return {'module_rank':r,'dual_rank':1+sum(dualdims.values()),'exact_integral_Gram_witnesses':len(branch['gram_witnesses'])}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3]);root=parser.parse_args().repo.resolve()
    folder=root/'evidence/theoretical_20261016/rank8';witnesses=json.loads((folder/'four_remaining_gram_witnesses.json').read_text())
    flat=lambda R:tuple(v for M in R for row in M for v in row)
    rows=[json.loads(line.replace('{','[').replace('}',']')) for line in gzip.open(root/'supplements/rank8/data/rank8_tables.txt.gz','rt')]
    bym={m:sorted((R for R in rows if max(flat(R))==m),key=flat) for m in (1,2)}
    ledger={r['id']:r for r in json.loads((root/'supplements/rank8/data/decisions.json').read_text())}
    coverage=[];reports={}
    for rid in IDS:
        _,m,index=rid.split('_');index=int(index);R=bym[int(m)][index-1];sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest();need(sha==ledger[rid]['tensor_sha256'],'source '+rid)
        invs=[g for g in range(1,8) if R[g][g]==[1]+[0]*7 and all(sum(R[x][g])==1 for x in range(8))]
        gs=[{'involution':g,'right_fixed_labels':[x for x in range(8) if R[x][g][x]]} for g in invs]
        positive=[v for v in gs if v['right_fixed_labels']]
        need(bool(positive)==(int(m)==2 and index in NEW_EIGHT|FOUR),'complete applicability inventory '+rid)
        need(ledger[rid]['status']==('excluded' if int(m)==2 and index in NEW_EIGHT else 'unresolved'),'preserved disposition '+rid)
        coverage.append({'id':rid,'tensor_sha256':sha,'commutative':all(R[i][j]==R[j][i] for i in range(8) for j in range(8)),'involutions':gs})
        if rid not in witnesses:continue
        w=witnesses[rid];g=w['involution'];fixed=w['right_fixed_labels'];need({'involution':g,'right_fixed_labels':fixed} in gs and len(fixed)==2,'four-case involution')
        reps,info=all_anti(R,g,fixed)
        given=[tuple(tuple(v for row in M for v in row) for M in branch['anti_matrices']) for branch in w['branches']]
        need(given==reps,'complete anti-representation domain')
        checked=[verify_grams(R,index,g,fixed,T,branch) for T,branch in zip(reps,w['branches'])]
        reports[rid]=info|{'branches':checked}
    need(len(coverage)==34 and len(reports)==4,'coverage totals')
    print(json.dumps({'status':'PASS','input_frontier_count':34,'new_spectral_exclusions':8,'remaining_unresolved':26,
                      'four_case_witnesses':reports,'involution_coverage':coverage,
                      'scope':'Exact necessary-condition witnesses only. They do not construct categorifications or assert simultaneous compatibility of dual actions.',
                      'legacy_guard':'The legacy helper stops at two generators. This independent replay exhausts three-generator presentations instead.'},indent=2))

if __name__=='__main__':main()
