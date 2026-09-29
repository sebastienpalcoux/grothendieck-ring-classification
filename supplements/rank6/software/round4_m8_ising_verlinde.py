"""Ising-projected full-character moments with low Verlinde fusion products."""
from round4_m8_ising import *
import round4_m8_ising as base

def system(R,data,cols,ep,lab):
    if any(R[i][i][0]!=1 for i in range(len(R))):raise Ineligible('self-dual source required for low cubic Verlinde rows')
    A,b,meta=base.system(R,data,cols,ep,lab)
    if A is None:return A,b,meta
    C=data['C'];types=data['phases'];tab=data['tab'];height=data['height'];n=len(R)
    G,vectors,spec=data['_branch_cache'][tuple(map(tuple,cols))];bad=set(map(tuple,spec.forbidden));vectors=[v for v in vectors if v not in bad]
    labels=[(v,ti) for v in vectors for ti in range(len(types)) if all((not v[g-1] and not v[ss-1]) or (v[g-1] and not v[ss-1] and types[ti]==tuple(C((-1)**k) for k in range(1,height+1))) or (v[ss-1] and not v[g-1] and types[ti] in data['ising_types'][ss][ep[ss-1]]) for g,ss in data['ising_labels'])]
    nv=len(A[0]);nold=nv;tuples=dict(zip(spec.vectors,spec.types));triple_vars={}
    def add(coeff,rhs):
        for row,value in rational_rows(coeff,rhs,C):A.append(row);b.append(value)
    for a,bb,cc in itertools.combinations_with_replacement(range(1,n),3):
        ha,hb,hc=[lab[x] for x in (a,bb,cc)]
        weights={v:tuples[v][ha]*tuples[v][hb]*tuples[v][hc]*tab.dims[v]**2/tab.D**2 for v in set(spec.vectors)}
        rhs=-sum((weights[v] for v in spec.low),C.zero)
        coeff=[weights[(0,)+v] for v,ti in labels]+[C.zero]*(nv-len(labels))+[-C.one]
        for row in A:row.append(0)
        triple_vars[a,bb,cc]=nv;nv+=1;add(coeff,rhs)
    allowed=sorted({(0,)+v for v,ti in labels})
    for a,bb in itertools.combinations_with_replacement(range(1,n),2):
        ca,cb=tuple(cols[a]),tuple(cols[bb]);fp=[sum(ca[i]*cb[j]*R[i][j][k] for i in range(n) for j in range(n)) for k in range(n)]
        qvars={}
        for v in allowed:
            bound=min(fp[k]//v[k] for k in range(n) if v[k])
            if bound:qvars[v]=(nv,bound);nv+=1
        for row in A:row.extend([0]*(nv-len(row)))
        for k in range(n):
            row=[0]*nv
            for cc in range(1,n):row[triple_vars[tuple(sorted((a,bb,cc)))]]+=cols[cc][k]
            for v,(j,M) in qvars.items():row[j]=v[k]
            A.append(row);b.append(fp[k]-int(a==bb and k==0))
        for v,(j,M) in qvars.items():
            row=[0]*(nv+1);row[j]=1;row[nv]=1
            for ii,(w,ti) in enumerate(labels):
                if w==v[1:]:row[ii]-=M
            for rr in A:rr.append(0)
            A.append(row);b.append(0);nv+=1
    meta=dict(meta,low_verlinde=True,restriction_products=True,equations=len(A),variables=len(A[0]))
    return A,b,meta

def probe(R,height,F,branch,lab,ep):
    d=data_for(R,height,F);cols=d['lows'][branch];A,b,meta=system(R,d,cols,ep,lab);y=cached_farkas(A,b)
    if y is not None:check_farkas(A,b,y)
    congruence=None
    if y is None:
        from modular_moments import check_congruence
        basis={}
        for i,(row,rhs) in enumerate(zip(A,b)):
            bits=sum((int(a)%2)<<j for j,a in enumerate(row)) | ((int(rhs)%2)<<len(row));w=1<<i
            while bits & ((1<<len(row))-1):
                pivot=(bits & -bits).bit_length()-1
                if pivot not in basis:basis[pivot]=(bits,w);break
                u,v=basis[pivot];bits^=u;w^=v
            else:
                if bits>>len(row):
                    congruence={'prime':2,'rows':[[j,1] for j in range(len(A)) if w>>j&1],'value':1}
                    check_congruence(A,b,[1]*len(A[0]),congruence);break
    return {'scope':'pseudo_unitary_necessary_single_branch','low':branch,'labelling':lab,'indicators':ep,'metadata':metadata(d),'system':meta,'exact_ray':y,'excluded':y is not None or congruence is not None,'congruence':congruence}

def verify_witness(R,c):
    from fractions import Fraction
    require(c.get('outcome')=='exact_necessary_relaxation_witness' and c.get('scope')=='pseudo_unitary_necessary_single_branch','wrong necessary witness scope')
    d=data_for(R,c['height'],c['conductor']);cols=tuple(map(tuple,c['columns']))
    require(cols in d['lows'],'witness frame outside exhaustive low domain')
    require(low_failure(cols,d['ch'].C,d['ds'],d['D'],d['K'],d['embedding'],d['ch'].du) is None,'witness fails ordinary low criterion')
    require(projection_failure(d,cols) is None,'witness fails Ising low projection')
    require(tuple(c['labelling']) in d['tab'].assignments(cols),'witness character labelling invalid')
    require(tuple(c['indicators']) in [tuple(x) for x in indicator_choices(R)],'witness indicator tuple invalid')
    A,b,meta=system(R,d,cols,c['indicators'],c['labelling'])
    require(json.loads(json.dumps(meta))==c['system'],'wrong necessary witness system')
    entries={}
    for j,num,den in c['primal']:
        require(type(j) is int and type(num) is int and type(den) is int and 0<=j<len(A[0]) and j not in entries and num>=0 and den>0,'invalid rational primal entry')
        entries[j]=Fraction(num,den)
    require(all(sum(Fraction(row[j])*v for j,v in entries.items())==rhs for row,rhs in zip(A,b)),'necessary witness equation fails')
    return {'passed':True,'equations':len(A),'variables':len(A[0]),'nonzero_primal_entries':len(entries),'optimizer_used':False,'categorification_claimed':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--height',type=int,default=3);ap.add_argument('--seconds',type=int,default=800);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']=='R6_8_1660');st=time.monotonic()
    def stop(*_):raise TimeoutError('explicit discovery budget')
    signal.signal(signal.SIGALRM,stop);signal.alarm(a.seconds)
    try:r=probe(R,a.height,24,0,[0,5,4,1,3,2],[1,1,1,-1,1]);r['outcome']='branch_excluded' if r['excluded'] else 'no_exact_obstruction'
    except TimeoutError as e:r={'outcome':'budget_incomplete','reason':str(e)}
    finally:signal.alarm(0)
    r['seconds']=time.monotonic()-st;a.output.write_text(json.dumps(r,separators=(',',':'))+'\n');print({k:v for k,v in r.items() if k!='exact_ray'},flush=True)
