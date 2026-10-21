#!/usr/bin/env python3
"""Independent low-only S-symmetry obstruction for R8_3_1463.

No frontier cone, partial-S integrality filter, native frame enumerator,
twist trace, indicator equation, or STS equation is used. The only shared
algebraic primitives are the frozen exact character/number-field tools.
"""
from pathlib import Path
from fractions import Fraction
import argparse, hashlib, itertools, json, math, sys

HERE=Path(__file__).resolve().parent
STAGE=HERE.parent
BASE=STAGE.parent/'rank8_m3_20261021'
sys.path.insert(0,str(BASE/'criteria'))
import global_induction as frozen
from rings import Characters,codegree_poly
from exact import discover_roots,check_roots,vector
s=frozen.s

def need(ok,message):
    if not ok:raise ValueError(message)

def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def restrictions(ds,beta,K,B):
    """Separate exact finite affine enumeration of all unit-multiplicity columns."""
    degree=K.mod.degree();matrix=s.Matrix.hstack(*(vector(d,degree) for d in ds[1:]))
    rhs=vector(beta-K.one,degree);rr,piv=matrix.row_join(rhs).rref()
    if 7 in piv:return []
    free=[j for j in range(7) if j not in piv]
    bounds=[min(int(B[0,i]),math.isqrt(int(B[i,i]))) for i in range(1,8)]
    out=[]
    for choice in itertools.product(*(range(bounds[j]+1) for j in free)):
        v=[s.S.Zero]*7
        for j,value in zip(free,choice):v[j]=s.Integer(value)
        for row,j in enumerate(piv):v[j]=rr[row,7]-sum(rr[row,k]*v[k] for k in free)
        if all(z.q==1 and 0<=z<=bounds[j] for j,z in enumerate(v)):
            col=(1,)+tuple(map(int,v))
            need(sum((K(n)*d for n,d in zip(col,ds)),K.zero)==beta,'dimension equation')
            out.append(col)
    return sorted(out)

def psd(matrix):
    """Exact rational Schur complements, with the singular pivot criterion."""
    A=[list(map(Fraction,row)) for row in matrix]
    for p in range(len(A)):
        pivot=A[p][p]
        if pivot<0:return False
        if not pivot:
            if any(A[p][j] for j in range(p+1,len(A))):return False
            continue
        for i in range(p+1,len(A)):
            for j in range(i,len(A)):
                A[i][j]-=A[i][p]*A[p][j]/pivot;A[j][i]=A[i][j]
    return True

def compute():
    source=next(r for r in json.loads((BASE/'pipeline/census_m3.json').read_text()) if r['id']=='R8_3_1463')
    R=source['tensor'];need(digest(R)==source['tensor_sha256'],'tensor identity')
    ch=Characters(R);f,K,ds,D,pD,embedding=ch.fp()
    need(f.degree()==4 and pD.degree()==4 and pD.TC()==57600,'FP formal-codegree norm')
    nonfp=[]
    for factor,multiplicity in ch.components:
        if factor==f:continue
        component=ch.component(factor);dimension_polynomial=component[3]
        need(dimension_polynomial.degree()==2 and dimension_polynomial.TC()==80,'non-FP dimension norm')
        need(Fraction(80**2,57600)==Fraction(1,9),'nonintegral norm quotient')
        nonfp.append(list(map(str,dimension_polynomial.all_coeffs())))
    need(len(nonfp)==2,'all non-FP ordinary character factors')
    roots=discover_roots(ch.p,K);need(roots is not None,'character splitting');check_roots(ch.p,K,roots)
    chars=[tuple(sum((K(co)*z**j for j,co in enumerate(cf)),K.zero) for cf in ch.coeff) for z in roots]
    need(len(set(chars))==8,'complete distinct character table')
    for row in chars:
        need(row[0]==K.one,'character unit')
        need(all(row[i]*row[j]==sum((K(R[i][j][k])*row[k] for k in range(8)),K.zero) for i in range(8) for j in range(8)),'all character multiplication identities')
        need(all(row[ch.du[i]]==row[i] for i in range(8)),'real character duality')
    fc=[sum((row[i]*row[ch.du[i]] for i in range(8)),K.zero) for row in chars]
    for E,row in enumerate(chars):
        for F,other in enumerate(chars):
            need(sum((row[i]*other[ch.du[i]] for i in range(8)),K.zero)==(fc[E] if E==F else K.zero),'complete character orthogonality')
    betas=[D/x for x in fc];fp=chars.index(tuple(ds));need(betas[fp]==K.one,'unit distinguished dimension')
    codegrees=discover_roots(codegree_poly(R),K);need(codegrees is not None,'codegree splitting');check_roots(codegree_poly(R),K,codegrees)
    need(sorted(map(str,fc))==sorted(map(str,codegrees)),'complete codegree multiset')
    codegrees.remove(D)
    sets=[restrictions(ds,D/x,K,ch.C) for x in codegrees]
    need(list(map(len,sets))==[20,9,4,4,12,12,6],'complete restriction domains')
    target=tuple(int(ch.C[0,j]) for j in range(1,8));same=[(i,j) for i in range(7) for j in range(i+1,7) if sets[i]==sets[j]]
    buckets={}
    for left in itertools.product(*(range(len(sets[g])) for g in range(3))):
        total=tuple(sum(sets[g][left[g]][k] for g in range(3)) for k in range(1,8))
        buckets.setdefault(total,[]).append(left)
    frames=[];row_matches=0;canonical_matches=0
    for right in itertools.product(*(range(len(sets[g])) for g in range(3,7))):
        total=tuple(sum(sets[g][right[g-3]][k] for g in range(3,7)) for k in range(1,8))
        for left in buckets.get(tuple(t-z for t,z in zip(target,total)),[]):
            row_matches+=1;choice=left+right
            if any(choice[i]>choice[j] for i,j in same):continue
            canonical_matches+=1;cols=[sets[g][choice[g]] for g in range(7)]
            residual=[[int(ch.C[i,j])-sum(v[i]*v[j] for v in cols) for j in range(1,8)] for i in range(1,8)]
            if any(x<0 for row in residual for x in row) or not psd(residual):continue
            frames.append(tuple(cols))
    frames.sort();need(len(frames)==len(set(frames))==2024,'complete independent low frames')
    unit=(1,)+(0,)*7;allcols={unit}|{v for cs in sets for v in cs}
    dims={v:sum((K(n)*d for n,d in zip(v,ds)),K.zero) for v in allcols}
    eligible={v:[E for E,beta in enumerate(betas) if beta==dims[v]] for v in allcols}
    S={(E,v):betas[E]*sum((K(n)*x for n,x in zip(v,chars[E])),K.zero) for v in allcols for E in range(8)}
    tested=0;survivors=[];per_frame=[]
    for index,frame in enumerate(frames):
        cols=(unit,)+frame;labels=[]
        for assignment in itertools.product(*(eligible[v] for v in cols)):
            if len(set(assignment))!=8:continue
            tested+=1
            if all(S[assignment[i],cols[j]]==S[assignment[j],cols[i]] for i in range(8) for j in range(i+1,8)):
                labels.append(assignment)
        if labels:survivors.append(index)
        per_frame.append(labels)
    need(not survivors,'a symmetric low character labeling survives')
    return {'result':'PASS','id':source['id'],'tensor_sha256':source['tensor_sha256'],
            'scope':'pseudo_unitary_nonexistence_by_distinguished_S_symmetry',
            'restriction_counts':list(map(len,sets)),'raw_cartesian_size':math.prod(map(len,sets)),
            'row_matching_choices':row_matches,'canonical_row_matching_choices':canonical_matches,
            'complete_frames':len(frames),'frame_sha256':digest(frames),
            'dimension_compatible_bijections_checked':tested,'symmetric_frames':survivors,
            'character_multiplication_and_orthogonality_checked':True,
            'non_FP_dimension_polynomials':nonfp,'non_FP_common_field_norm_base':'1/9',
            'uses_partial_S_integrality':False,'uses_native_frame_enumeration':False,
            'uses_twists_indicators_or_STS':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=compute();path=HERE/'r1463_low_symmetry.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'independent low-symmetry receipt')
    print('PASS R1463 independent low-only S symmetry:',result['complete_frames'],'complete frames;',result['dimension_compatible_bijections_checked'],'bijections; none symmetric')

if __name__=='__main__':main()
