#!/usr/bin/env python3
"""Independent low/high domains, integer Gram/duality and real cubic review R567."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import argparse,hashlib,itertools,json
import verify_additional_nc_constraints as old
import verify_r439_verlinde as exact

HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=BASE.parents[1]
need=exact.need;s=old.s;c=old.c

def generic_charpoly(x,K):
    n=K.mod.degree();cols=[]
    for j in range(n):
        coeff=list(reversed((x*K.unit**j).to_list()))
        coeff += [0]*(n-len(coeff))
        cols.append(s.Matrix(list(map(s.Rational,coeff))))
    return s.Matrix.hstack(*cols).charpoly().all_coeffs()

def vec_s3_control():
    """Actual center of Vec(S3), including the two-dimensional character sector."""
    # Source group labels: e, two 3-cycles, three transpositions.
    chars=[[1]*6,[1,1,1,-1,-1,-1],[2,-1,-1,0,0,0]]
    degrees=[1,1,2];f=[6,6,3]
    low=[(1,0,0,0,0,0),(1,0,0,0,0,0),(2,0,0,0,0,0)]
    high=[((0,0,0,1,1,1),2),((0,1,1,0,0,0),3)]
    restrictions=[(v,1)for v in low]+high
    need(sum(m*sum(v)**2 for v,m in restrictions)==36,'VecS3 center global dimension')
    # The distinguished center objects are Rep(S3) simples; exact target tensor.
    R=[[[1,0,0],[0,1,0],[0,0,1]],[[0,1,0],[1,0,0],[0,0,1]],
       [[0,0,1],[0,0,1],[1,1,1]]]
    answers=[]
    for E,G,J in itertools.product(range(3),repeat=3):
        value=F(0)
        for v,m in restrictions:
            row=[F(6,f[i]*degrees[i])*sum(x*y for x,y in zip(chars[i],v))for i in range(3)]
            value+=F(m,36*sum(v))*row[E]*row[G]*row[J]
        need(value==R[E][G][J],'known VecS3 noncommutative-character normalization')
        answers.append(int(value))
    return {'source_category':'Vec(S3)','distinguished_sector':'Rep(S3)',
            'irreducible_character_degrees':degrees,'formal_codegrees':f,
            'distinguished_restrictions':low,'all_27_exact_coefficients':answers,
            'matrix_character_normalization_and_multiplicity_control':True}

def compute():
    census_path=REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json'
    row=next(r for r in json.loads(census_path.read_text())if r['id']=='R8_3_567')
    R=row['tensor'];need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==row['tensor_sha256'],'source tensor')
    a=c.w.spectral(R);sets,frames,boxes=old.independent_low(a)
    saved=next(r for r in json.loads((BASE/'noncommutative_followup/additional_central_constraints.json').read_text())if r['id']=='R8_3_567')
    need([list(map(list,f))for f in frames]==[r['columns']for r in saved['frames']],'independent complete low frame agreement')
    K0=a['K'];K=s.QQ.algebraic_field(K0.ext,s.I)
    move=lambda x:K.from_sympy(K0.to_sympy(x))
    b=dict(a,K=K,D=move(a['D']),ds=list(map(move,a['ds'])),codegrees=list(map(move,a['codegrees'])))
    chars=[]
    for chi in saved['full_characters']:
        chars.append([sum((K(s.Rational(co))*K.unit**(len(v)-1-j)for j,co in enumerate(v)),K.zero)for v in chi])
    need(b['multiplicities']==[1,1,1,1,2],'C4 plus M2 sector dimensions')
    for i in range(8):
        regular_trace=sum(R[i][j][j]for j in range(8))
        need(K(regular_trace)==sum((chars[E][i]for E in range(4)),K.zero)+K(2)*chars[4][i],
             'matrix character independently recovered from regular trace')
    for E,G in itertools.product(range(5),repeat=2):
        z=sum((chars[E][i]*chars[G][a['du'][i]]for i in range(8)),K.zero)
        need(z==(b['codegrees'][E]*K(b['multiplicities'][E])if E==G else K.zero),'full character orthogonality with matrix multiplicity')
    survivor=[];assign_counts=[]
    for ix,cols in enumerate(frames):
        ass,tests=old.independent_assignments(R,b,chars,cols)
        need(ass==saved['frames'][ix]['complete_symmetric_S_assignments'],'complete exact full-S assignments')
        assign_counts.append(len(ass))
        if ass:survivor.append((ix,cols,ass))
    need(len(survivor)==1 and survivor[0][0]==2,'unique low frame')
    ix,cols,ass=survivor[0];a=c.w.data(R)
    L=s.Matrix.hstack(*map(s.Matrix,cols));high,high_stats=old.independent_high(a,L)
    Q=(a['Gram']-L*L.T)[1:,1:];H=[v for v,z in high]
    need(len(H)==45,'complete independent high domain')
    integral=[j for j,(v,z)in enumerate(high)if z[1]==0]
    spectral=[]
    for j,(v,z)in enumerate(high):
        col=(0,)+v;dim=sum((K(x)*d for x,d in zip(col,b['ds'])),K.zero)
        for E,chi in enumerate(chars):
            eigenvalue=b['D']/b['codegrees'][E]/K(b['multiplicities'][E])*sum((K(x)*d for x,d in zip(col,chi)),K.zero)/dim
            poly=generic_charpoly(eigenvalue,K)
            if any(x.q!=1 for x in poly):
                spectral.append({'index':j,'character':E,'eigenvalue':list(map(str,eigenvalue.to_list())),
                                 'exact_characteristic_polynomial':list(map(str,poly))});break
    need(integral==[0,34]and[r['index']for r in spectral]==[9,13,16,24,27,30,32,33,42],'complete necessary filters')
    ii=K.from_sympy(s.I)
    need(all(x.q==1 for x in generic_charpoly(ii,K))and
         any(x.q!=1 for x in generic_charpoly((K.one+ii)/K(2),K)),'nonreal integrality positive and negative controls')
    allowed=[j for j in range(45)if j not in integral+[r['index']for r in spectral]]
    reduced=[(v[0],v[4],v[2],v[3])for v in H];lift=[0,0,2,3,1,1,1]
    need(all(v==tuple(w[k]for k in lift)for v,w in zip(H,reduced)),'exact four-coordinate high lift')
    small=Q.extract([0,4,2,3],[0,4,2,3]);need(all(Q[i,j]==small[lift[i],lift[j]]for i,j in itertools.product(range(7),repeat=2)),'full Gram lift')
    patterns,states=exact.gram_patterns(small,reduced,allowed)
    du=a['du'];lookup={v:i for i,v in enumerate(H)}
    dual=[]
    for v in H:
        full=(0,)+v;other=tuple(full[du[i]]for i in range(1,8));need(other in lookup,'full high domain dual closure');dual.append(lookup[other])
    compatible=[m for m in patterns if all(m[i]==m[dual[i]]for i in range(45))]
    gram_path=BASE/'r567_centerless_integer/gram.json';primary=json.loads(gram_path.read_text())
    need(len(patterns)==1071 and len(compatible)==155,'complete integer and dual counts')
    need([list(v)for v in H]==primary['high_vectors']and [list(m)for m in compatible]==primary['solutions'],'independent complete pattern equality')
    need(hashlib.sha256(json.dumps(patterns,separators=(',',':')).encode()).hexdigest()==primary['all_integer_Gram_solutions_sha256'],'all integer patterns before duality agree')
    ds=[exact.pair(1)if i not in(3,4)else exact.pair(3,2)for i in range(8)]
    chi=[exact.pair(1)if i not in(3,4)else exact.pair(3,-2)for i in range(8)]
    D=exact.pair(48,24);f=exact.pair(48,-24);beta=exact.div(D,f)
    need(all(exact.mul(chi[i],chi[j])==exact.value(chi,R[i][j])for i,j in itertools.product(range(8),repeat=2)),'independent radical conjugate-FP character')
    histogram=Counter();values=[]
    for m in compatible:
        restrictions=[(v,1)for v in cols]+[((0,)+v,mv)for v,mv in zip(H,m)if mv]
        pairs=[(exact.mul(beta,exact.value(chi,v)),exact.value(ds,v),count)for v,count in restrictions]
        coefficient=exact.div(exact.total(exact.scale(count,exact.div(exact.mul(exact.mul(x,x),x),z))for x,z,count in pairs),exact.mul(D,D))
        need(exact.total(exact.scale(count,exact.mul(x,x))for x,z,count in pairs)==exact.mul(D,D),'full scalar S-row norm')
        need(not exact.nonnegative_integer(coefficient),'every integer pattern has a nonintegral111 coefficient')
        key=tuple(exact.encode(coefficient));histogram[key]+=1;values.append(list(key))
    need(dict(histogram)=={('1/3','0'):84,('4/3','0'):71},'exact cubic histogram')
    inputs=[census_path,HERE/'verify_additional_nc_constraints.py',HERE/'verify_r439_verlinde.py',
            BASE/'noncommutative_followup/additional_scope_gates.json',BASE/'noncommutative_followup/additional_central_constraints.json',
            BASE/'r567_centerless_integer/source.py',BASE/'r567_centerless_integer/source.json',
            BASE/'r567_centerless_integer/gram.py',gram_path,BASE/'r567_centerless_integer/cubic.py',
            HERE/'INTEGRAL_CENTER_SUBCATEGORY.md',HERE/'integral_center_subcategory.json']
    return {'kind':'independent_complete_integer_and_cubic_Verlinde_review_R567',
            'source_sha256':{str(p.relative_to(REPO)):exact.sha(p)for p in inputs},
            'tensor_sha256':row['tensor_sha256'],'complete_low_boxes':boxes,'low_column_counts':list(map(len,sets)),
            'low_frame_count':len(frames),'symmetric_assignment_counts':assign_counts,
            'high_domain':high_stats,'integral_forbidden':integral,'spectral_forbidden':spectral,
            'allowed_count':len(allowed),'independent_integer_patterns':len(patterns),
            'independent_duality_compatible_patterns':len(compatible),'memoized_Gram_states':states,
            'all_cubic111_coefficients':values,'histogram':[{'value':list(k),'count':v}for k,v in sorted(histogram.items())],
            'known_noncommutative_character_control':vec_s3_control(),
            'result':'PASS; no PU R567 category and, by the separately verified unrestricted Galois-PU gate, no complex categorification'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    result=json.loads(json.dumps(compute(),default=int));path=HERE/'r567_verlinde_direct.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'independent R567 review receipt mismatch')
    print('PASS: independent complete R567 domains,1071 integer Grams,155 dual-compatible patterns, all cubic111 failures, and known VecS3-center control.')
