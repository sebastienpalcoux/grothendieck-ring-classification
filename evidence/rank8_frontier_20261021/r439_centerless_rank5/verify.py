"""Rank-five induction constraints with trivial invertibles in the center.

Conditional on the independently proved R439 Morita reduction. No
uniqueness of the known rank-five associator is assumed. Default replay
is read-only and checks exact witnesses, not numerical feasibility.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse,hashlib,itertools,json,math,sys,zipfile
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'supplements/rank5/software'))
import higher_traces as h
from proofs import multiplication_matrix
sys.path.insert(0,str(HERE.parent/'noncommutative'))
import certified_lp as lp
sys.path.insert(0,str(ROOT/'evidence/rank8_m3_20261021/criteria'))
import tensor_rotation
s=h.s;need=h.require
ARCHIVE=ROOT/'evidence/prepublication_20261017/rank5/rank5_current_replay.zip'
ARCHIVE_SHA='264fd1b7f1851cbce142ea248a19bc2d0196ba44f350b2f5852e1e77a647a92d'
TENSOR_SHA='84487a759f44be4a988082680fa8c3b28bcd0d159d639f38409825e19c5761e6'

def source():
    need(hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()==ARCHIVE_SHA,'frozen rank-five archive binding')
    with zipfile.ZipFile(ARCHIVE) as z:
        path=next(p for p in z.namelist() if p.endswith('data/current/classification_tensors.json'))
        rows=json.loads(z.read(path));found=[r for r in rows if r['m']==3 and r['j']==40]
    need(len(found)==1,'unique R5_3_40 source row');R=found[0]['N']
    need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==TENSOR_SHA,'full125 source tensor binding')
    h.validate(R);return R

def spectral(R,a):
    K=a['K'];D=a['D'];ch=a['ch']
    roots=h.discover_roots(h.codegree_poly(R),K);h.check_roots(h.codegree_poly(R),K,roots)
    roots.remove(D);codegrees=[D]+roots;characters=[]
    for f,m in ch.components:
        zz=h.discover_roots(f,K);h.check_roots(f,K,zz)
        for z in zz:
            chi=[sum((K(co)*z**j for j,co in enumerate(cf)),K.zero) for cf in ch.coeff]
            need(all(chi[i]*chi[j]==sum((K(R[i][j][k])*chi[k] for k in range(5)),K.zero) for i in range(5) for j in range(5)),'scalar character multiplication')
            characters.append(chi)
    need(len(characters)==5,'complete commutative characters');done=set();ordered=[]
    for fc in codegrees:
        i=next(i for i,chi in enumerate(characters) if i not in done and sum((chi[j]*chi[ch.du[j]] for j in range(5)),K.zero)==fc)
        done.add(i);ordered.append(characters[i])
    for i,x in enumerate(ordered):
        for j,y in enumerate(ordered):
            need(sum((x[k]*y[ch.du[k]] for k in range(5)),K.zero)==(codegrees[i] if i==j else K.zero),'complete character orthogonality')
    return codegrees,ordered

def value(chi,col,K):return sum((K(v)*x for v,x in zip(col,chi)),K.zero)

def assignments(a,fc,chars,cols):
    K=a['K'];D=a['D'];out=[]
    for tail in itertools.permutations(range(1,5)):
        perm=(0,)+tail
        if any(fc[i]!=fc[perm[i]] for i in range(5)):continue
        S=[[D/fc[E]*value(chars[E],cols[perm[F]],K) for F in range(5)] for E in range(5)]
        if all(S[E][F]==S[F][E] for E in range(5) for F in range(5)):out.append(perm)
    return out

def high_filter(a,fc,chars,cols):
    K=a['K'];L=s.Matrix.hstack(*map(s.Matrix,cols));Qm,high=h.high_columns(a,L)
    spectral_bad=[];center_bad=[]
    for index,(v,z) in enumerate(high):
        if z==(Q(1),Q(0)):center_bad.append(index)
        dim=sum((K(x)*d for x,d in zip((0,)+v,a['ds'])),K.zero)
        for E,chi in enumerate(chars):
            ev=a['D']/fc[E]*value(chi,(0,)+v,K)/dim
            polynomial=multiplication_matrix(ev,K,a['factor']).charpoly().all_coeffs()
            if any(x.q!=1 for x in polynomial):
                spectral_bad.append({'index':index,'column':list(v),'character':E,
                    'eigenvalue':h.ec(ev),'characteristic_polynomial':list(map(str,polynomial))});break
    need(center_bad==[i for i,(v,z) in enumerate(high) if v[0]>0 and not any(v[1:])],
         'all high columns supported on the nonunit invertible are exactly dimension one in this complete domain')
    return Qm,high,spectral_bad,center_bad

def system(R,a,fc,chars,cols,perm,forbid_invertibles,height=6):
    n=len(R);tail=n-1;K=a['K'];q=a['q'];d=a['dimensions'];D=a['global_dimension']
    Qm,high,spectral_bad,center_bad=high_filter(a,fc,chars,cols)
    types,bound=h.trace_types(q,a['primes'],height)
    labels=[(v,z,ti) for v,z in high for ti in range(len(types))];nvars=len(labels)
    L=s.Matrix.hstack(*map(s.Matrix,cols));LL=L*L.T
    low=[tuple(sum((Q(int(LL[i,j]))*d[j][k] for j in range(n)),Q(0)) for k in range(2)) for i in range(n)]
    need(low[0]==D,'distinguished unit dimension identity')
    eps=h.indicator_choices(R);need(eps==[(1,1,1,1)],'all four second indicators are forced positive')
    ep=eps[0];rows=[];rhs=[]
    for i,j in itertools.combinations_with_replacement(range(tail),2):
        rows.append({k:Q(v[i]*v[j]) for k,(v,z,ti) in enumerate(labels) if v[i]*v[j]});rhs.append(Q(int(Qm[i,j])))
    moments=[[h.mul(z,tt,q) for tt in types[ti]] for v,z,ti in labels]
    for power in (1,2):
        for i in range(tail):
            for k in range(2):
                rows.append({j:v[i]*moments[j][power-1][k] for j,(v,z,ti) in enumerate(labels) if v[i]*moments[j][power-1][k]})
                rhs.append(-low[i+1][k]+(ep[i]*D[k] if power==2 else 0))
    for obj in range(1,n):
        powers=[[1]+[0]*tail]
        for order in range(1,height+1):powers.append([sum(powers[-1][i]*R[i][obj][j] for i in range(n)) for j in range(n)])
        for order in range(3,height+1):
            divisors=[int(r) for r in s.divisors(order) if r<order]
            rotations=tensor_rotation.rotation_types(q,order,divisors);start=nvars;nvars+=len(rotations)
            rows.append({start+j:Q(1) for j in range(len(rotations))});rhs.append(Q(powers[order][0]))
            for at,r in enumerate(divisors):
                power=order//r
                for k in range(2):
                    row={};constant=sum((Q(powers[r][i])*low[i][k] for i in range(n)),Q(0))
                    for j,(v,z,ti) in enumerate(labels):
                        coeff=sum(powers[r][i]*v[i-1] for i in range(1,n));entry=-coeff*moments[j][power-1][k]
                        if entry:row[j]=entry
                    for j,trace in enumerate(rotations):
                        entry=h.mul(D,trace[at],q)[k]
                        if entry:row[start+j]=entry
                    rows.append(row);rhs.append(constant)
    # Full distinguished-row STS, including both equal-codegree assignments.
    need(perm in assignments(a,fc,chars,cols),'complete symmetric S assignment')
    sqrtq=next(x for x in h.discover_roots(s.Poly(h.t*h.t-q,h.t),K) if a['embedding'].sign(x)>0)
    V=s.Matrix.hstack(h.vector(K.one,2),h.vector(sqrtq,2));Vinv=V.inv()
    coords=lambda x:tuple(Q(str(v)) for v in Vinv*h.vector(x,2))
    traces=[K(s.Rational(tt[0][0]))+K(s.Rational(tt[0][1]))*sqrtq for tt in types]
    highvalues=[[value(ch,(0,)+v,K) for ch in chars] for v,z in high]
    lowvalues=[[value(ch,v,K) for ch in chars] for v in cols]
    for E,F in itertools.combinations_with_replacement(range(n),2):
        target=fc[F]*value(chars[E],cols[perm[F]],K)-sum((v[E]*v[F] for v in lowvalues),K.zero)
        coefficients=[coords(v[E]*v[F]*tr) for v in highvalues for tr in traces];target=coords(target)
        for k in range(2):
            rows.append({j:v[k] for j,v in enumerate(coefficients) if v[k]});rhs.append(target[k])
    # Each known S-row describes the entire spectrum of an integral
    # fusion matrix N_(A_E), so irrational conjugates have equal counts.
    # Low simples occur once; high multiplicities are sums of trace weights.
    spectral_balance=[]
    for E,chi in enumerate(chars):
        highkeys=[];lowkeys=[]
        for col in [*cols,*[(0,)+v for v,z in high]]:
            dim=sum((K(v)*d for v,d in zip(col,a['ds'])),K.zero)
            key=coords(a['D']/fc[E]*value(chi,col,K)/dim)
            (lowkeys if len(lowkeys)<len(cols) else highkeys).append(key)
        pairs=sorted({(u,abs(v)) for u,v in lowkeys+highkeys if v})
        for u,v in pairs:
            plus=(u,v);minus=(u,-v)
            delta=lowkeys.count(plus)-lowkeys.count(minus)
            sparse={j*len(types)+k:Q(int(key==plus)-int(key==minus))
                    for j,key in enumerate(highkeys) for k in range(len(types))
                    if key in (plus,minus)}
            rows.append(sparse);rhs.append(Q(-delta))
            spectral_balance.append({'character':E,'positive_radical_eigenvalue':[str(u),str(v)],
                                     'low_multiplicity_difference':delta})
    integral_bad=[i for i,(v,z) in enumerate(high) if z[1]==0]
    need(integral_bad==[i for i,(v,z) in enumerate(high) if not any(v[2:])],
         'all integral central restrictions have integral source support')
    forbidden=sorted({r['index'] for r in spectral_bad}|(set(integral_bad) if forbid_invertibles else set()))
    for index in forbidden:
        rows.append({index*len(types)+j:Q(1) for j in range(len(types))});rhs.append(Q(0))
    A=[];b=[]
    for sparse,constant in zip(rows,rhs):
        denominator=math.lcm(constant.denominator,*(v.denominator for v in sparse.values()));row=[0]*nvars
        for j,v in sparse.items():row[j]=int(v*denominator)
        constant=int(constant*denominator);g=math.gcd(constant,*row) or 1
        A.append([x//g for x in row]);b.append(constant//g)
    return A,b,{'height':height,'high_columns':len(high),'trace_types':len(types),'order_bound':int(bound),
                'rows':len(A),'variables':nvars,'forbid_nonunit_center_invertibles':forbid_invertibles,
                'forbid_nonunit_integral_center_simples':forbid_invertibles,
                'spectral_exclusions':spectral_bad,'dimension_one_high_indices':center_bad,
                'integral_dimension_high_indices':integral_bad,
                'galois_spectral_balance':spectral_balance,
                'forbidden_high_indices':forbidden,'character_assignment':list(perm),
                'system_sha256':hashlib.sha256(json.dumps([A,b],separators=(',',':')).encode()).hexdigest()}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');args=ap.parse_args()
    R=source();a=h.quadratic_data(R);fc,chars=spectral(R,a);frames=[];survivors=[]
    for index,cols in enumerate(a['lows']):
        ordinary=h.low_failure(cols,a['ch'].C,a['ds'],a['D'],a['K'],a['embedding'],a['ch'].du)
        permutations=[] if ordinary else assignments(a,fc,chars,cols)
        frames.append({'index':index,'columns':[list(v) for v in cols],'ordinary_obstruction':ordinary,'full_S_assignments':[list(p) for p in permutations]})
        survivors.extend((index,cols,p) for p in permutations)
    need([i for i,cols,p in survivors]==[12,12],'complete low/S domain')
    path=HERE/'results.json';saved=None if args.write else json.loads(path.read_text());cases=[]
    for index,cols,perm in survivors:
        for forbidden in (False,True):
            A,b,meta=system(R,a,fc,chars,cols,perm,forbidden)
            if args.write:decision=lp.decide(A,b)
            else:
                case=saved['cases'][len(cases)];need(case['metadata']==meta,'reconstructed exact system')
                decision=case['decision']
            lp.verify(A,b,decision)
            cases.append({'low_index':index,'metadata':meta,'decision':decision})
            print('R5_3_40',perm,'centerless',forbidden,decision['status'],flush=True)
    result={'target':'R439 via its forced rank-five Morita partner R5_3_40',
            'scope':'pseudo_unitary_rank5_center_constraints; applicability to general R439 via independently proved Galois and full-S3 Morita reductions',
            'source_archive_sha256':ARCHIVE_SHA,'rank5_tensor_sha256':TENSOR_SHA,
            'rank5_tensor':R,'global_dimension_minimal_polynomial':h.pc(a['ch'].fp()[4]),
            'column_counts':list(map(len,a['columns'])),'all_low_frames':frames,
            'formal_codegrees':[h.ec(f) for f in fc],'complete_characters':[[h.ec(v) for v in chi] for chi in chars],
            'cases':cases,'centerless_excluded':all(c['decision']['status']=='exact_infeasible_relaxation' for c in cases if c['metadata']['forbid_nonunit_center_invertibles']),
            'positive_control_exists':any(c['decision']['status']=='exact_feasible_relaxation' for c in cases if not c['metadata']['forbid_nonunit_center_invertibles'])}
    result=json.loads(json.dumps(result,default=int))
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==saved,'complete centerless rank-five replay')
    print('PASS centerless_excluded=',result['centerless_excluded'],'positive_control_exists=',result['positive_control_exists'])

if __name__=='__main__':main()
