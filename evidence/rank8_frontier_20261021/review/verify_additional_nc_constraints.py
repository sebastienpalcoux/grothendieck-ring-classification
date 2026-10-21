"""Independent domain/S-symmetry checks and exact replay of additional NC constraints.

Shares frozen scalar algebra primitives and the previously reviewed joint-rotation
matrix builder. Re-enumerates low columns/frames and high Gram vectors by full
integer boxes, with no native Gram or affine-restriction enumerator. No solver.
"""
from pathlib import Path
import argparse, hashlib, itertools, json, math, sys
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
sys.path.insert(0,str(BASE/'noncommutative_followup'))
import additional_central_constraints as producer
import additional_joint_rotation as joint
c=producer.c
s=c.s

def require(ok,message):
    if not ok: raise ValueError(message)

def coord(x,degree):
    a=list(map(lambda t:F(str(t)),c.ec(x)))
    return tuple([F(0)]*(degree-len(a))+a)

def independent_low(a):
    B=a['Gram'];K=a['K'];degree=K.mod.degree();ds=[coord(x,degree) for x in a['ds']]
    null=[]
    for u in B.nullspace():
        den=math.lcm(*(int(x.q) for x in u));null.append(tuple(int(x*den) for x in u))
    sets=[];boxes=[]
    for fc,r in zip(a['codegrees'][1:],a['multiplicities'][1:]):
        bounds=[min(int(B[0,i])//r,math.isqrt(int(B[i,i]))) for i in range(1,8)]
        target=coord(a['D']/fc,degree);out=[];boxes.append(math.prod(x+1 for x in bounds))
        for tail in itertools.product(*(range(x+1) for x in bounds)):
            v=(r,)+tail
            if any(sum(x*y for x,y in zip(v,u)) for u in null):continue
            if tuple(sum(F(v[i])*ds[i][j] for i in range(8)) for j in range(degree))!=target:continue
            out.append(v)
        sets.append(sorted(out))
    unit=(1,0,0,0,0,0,0,0);w=a['multiplicities'][1:];frames=[]
    for cols in itertools.product(*sets):
        if any(unit[j]+sum(w[i]*cols[i][j] for i in range(4))!=B[0,j] for j in range(8)):continue
        if any(w[i]==w[j] and sets[i]==sets[j] and cols[i]>cols[j] for i in range(4) for j in range(i+1,4)):continue
        frames.append((unit,)+cols)
    return sets,sorted(frames),boxes

def independent_assignments(R,a,characters,cols):
    K=a['K'];D=a['D'];fs=a['codegrees'];ms=a['multiplicities'];out=[];tested=0
    for chi in characters[:4]:
        require(chi[0]==K.one,'scalar unit')
        for i,j in itertools.product(range(8),repeat=2):
            require(chi[i]*chi[j]==sum((K(R[i][j][k])*chi[k] for k in range(8)),K.zero),'all scalar multiplication identities')
    for p in itertools.permutations(range(5)):
        if p[0]!=0:continue
        if any(fs[i]!=fs[p[i]] or ms[i]!=ms[p[i]] for i in range(5)):continue
        tested+=1;table=[]
        for E in range(5):
            table.append([D/fs[E]/K(ms[E])*sum((K(v)*z for v,z in zip(cols[p[F]],characters[E])),K.zero) for F in range(5)])
        if all(table[i][j]==table[j][i] for i,j in itertools.product(range(5),repeat=2)):out.append(list(p))
    return out,tested

def independent_high(a,L):
    Q=(a['Gram']-L*L.T)[1:,1:];n=Q.rows;rank=Q.rank()
    ix=next(ix for ix in itertools.combinations(range(n),rank) if Q.extract(ix,ix).det()!=0)
    S=Q.extract(ix,ix);det=int(S.det());adj=S.adjugate();require(det>0,'positive Gram principal determinant')
    null=[]
    for u in Q.nullspace():
        den=math.lcm(*(int(x.q) for x in u));null.append(tuple(int(x*den) for x in u))
    bounds=[math.isqrt(int(Q[i,i])) for i in range(n)];out=[];raw=0
    for v in itertools.product(*(range(x+1) for x in bounds)):
        if not any(v):continue
        if any(v[i]*v[j]>Q[i,j] for i in range(n) for j in range(i,n)):continue
        if any(sum(x*y for x,y in zip(v,u)) for u in null):continue
        if sum(v[ix[i]]*int(adj[i,j])*v[ix[j]] for i in range(rank) for j in range(rank))>det:continue
        raw+=1;z=tuple(sum(F(v[i])*a['dimensions'][i+1][j] for i in range(n)) for j in range(2));q=a['q'];norm=z[0]**2-q*z[1]**2
        if not norm:continue
        D=a['global_dimension'];ratio=((D[0]*z[0]-q*D[1]*z[1])/norm,(D[1]*z[0]-D[0]*z[1])/norm)
        if (2*ratio[0]).denominator!=1 or (ratio[0]**2-q*ratio[1]**2).denominator!=1:continue
        if z[1] and (4*z[0]**2/norm).denominator!=1:continue
        out.append((v,z))
    return sorted(out),{'full_box_size':math.prod(x+1 for x in bounds),'Gram_vectors_before_arithmetic':raw,'retained_high_vectors':len(out),'residual_rank':rank}

def compute():
    sources={r['id']:r for r in json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text())}
    saved=json.loads((BASE/'noncommutative_followup/additional_central_constraints.json').read_text());rot={r['id']:r for r in json.loads((BASE/'noncommutative_followup/additional_joint_rotation_h6.json').read_text())}
    joint.full.base.install();out=[]
    for rec in saved:
        ident=rec['id'];source=sources[ident];R=source['tensor'];require(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==rec['tensor_sha256']==source['tensor_sha256'],'source tensor hash')
        a=c.w.spectral(R);sets,frames,boxes=independent_low(a)
        require([list(map(list,cs)) for cs in frames]==[x['columns'] for x in rec['frames']],'complete independent low frame list')
        if rec['splitting_field_extension_by_i_used']:
            oldK=a['K'];K=s.QQ.algebraic_field(oldK.ext,s.I);move=lambda x:K.from_sympy(oldK.to_sympy(x));a=dict(a,K=K,D=move(a['D']),ds=list(map(move,a['ds'])),codegrees=list(map(move,a['codegrees'])))
        K=a['K'];chars=[]
        for chi in rec['full_characters']:
            chars.append([sum((K(s.Rational(co))*K.unit**(len(value)-1-i) for i,co in enumerate(value)),K.zero) for value in chi])
        counts=[];tests=0
        for cs,fr in zip(frames,rec['frames']):
            ass,n=independent_assignments(R,a,chars,cs);tests+=n
            require(ass==fr['complete_symmetric_S_assignments'],'independent full character S symmetry')
            counts.append(len(ass))
        result={'id':ident,'low_full_boxes':boxes,'low_column_counts':list(map(len,sets)),'complete_low_frames':len(frames),'dimension_compatible_bijections_tested':tests,'symmetric_assignment_counts':counts}
        if ident in rot:
            a=c.w.data(R);require(a['lows']==frames,'primary low frame ordering identity')
            require([i for i,n in enumerate(counts) if n]==[2],'unique full-S frame')
            L=s.Matrix.hstack(*map(s.Matrix,frames[2]));high,stats=independent_high(a,L);require(high==joint.full.base.grams.high_columns(a,L)[1],'independent complete high domain identity')
            rr=rot[ident];eps=joint.full.base.h.indicator_choices(R);require([x['indicators'] for x in rr['cases']]==list(map(list,eps)),'complete indicator domain')
            cases=[]
            for ep,case in zip(eps,rr['cases']):
                A,b,meta=joint.full.system(R,a,L,ep,6);require(meta==case['metadata'],'system metadata');dec=case['decision']
                if dec['status']=='exact_infeasible_relaxation':
                    y=dec['ray'];require(len(y)==len(b),'ray dimension');scores=[sum(y[i]*A[i][j] for i in range(len(A))) for j in range(len(A[0]))];rhs=sum(x*z for x,z in zip(y,b));require(min(scores)>=0 and rhs<0,'full exact separator inequalities');answer={'indicators':list(ep),'status':dec['status'],'columns_checked':len(scores),'minimum_column_pairing':min(scores),'rhs_pairing':rhs,'scores_sha256':hashlib.sha256(json.dumps(scores,separators=(',',':')).encode()).hexdigest()}
                else:
                    require(dec['status']=='exact_feasible_relaxation','no numerical decisions accepted');p={j:F(x) for j,x in dec['primal']};require(len(p)==len(dec['primal']) and all(0<=j<len(A[0]) and x>=0 for j,x in p.items()),'exact primal domain');require(all(sum(F(row[j])*x for j,x in p.items())==bb for row,bb in zip(A,b)),'all exact primal equations');answer={'indicators':list(ep),'status':dec['status'],'support_size':len(p),'equations_checked':len(b)}
                cases.append(answer)
            result.update(high_domain=stats,rotation_cases=cases)
        out.append(result);print('PASS',ident,'independent domains and full S; exact rotation certificates where supplied',flush=True)
    return {'scope':'necessary central/S/rotation constraints after reviewed general Galois-PU gates; no categorical model or ring nonexistence','independence':'independent full-box low/high domains and S permutations; shared scalar spectral primitives and previously reviewed joint-rotation builder; no native enumerator, LP solver or producer ray verifier','cases':out}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();result=compute();path=HERE/'additional_nc_constraints.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:require(result==json.loads(path.read_text()),'saved independent review agrees')
    print('PASS: complete additional NC independent domain and exact-certificate review')
if __name__=='__main__':main()
