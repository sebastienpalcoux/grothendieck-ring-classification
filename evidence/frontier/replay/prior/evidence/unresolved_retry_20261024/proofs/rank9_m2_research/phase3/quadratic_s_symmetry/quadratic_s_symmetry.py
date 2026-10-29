"""Labelled distinguished columns with quadratic-character S symmetry.

The character label is an additional nonnegative LP index. No integral low
frame is selected or assumed. All original joint-center constraints remain.
"""
import collections,hashlib,json,math,sys,time
from pathlib import Path
from fractions import Fraction as Q
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'phase2/quadratic_theory'))
import quadratic_center as qc
HERE=Path(__file__).parent

def characters(ch,q,D):
    out=[]
    for f,m in ch.components:
        if f.degree()>2:continue
        K,ds,codegree,_=ch.component(f)
        if f.degree()==1:
            vectors=[[ (Q(str(qc.ec(x)[-1])) if qc.ec(x) else Q(0),Q(0)) for x in ds]]
        else:
            co=list(map(Q,f.all_coeffs()));a,b,c=co;disc=b*b-4*a*c
            square=disc/q
            if square<=0 or square.denominator!=1:continue
            h=math.isqrt(square.numerator)
            if h*h!=square:continue
            vectors=[]
            for sign in [-1,1]:
                vec=[]
                for x in ds:
                    z=list(map(lambda t:Q(str(t)),qc.ec(x)));z=[Q(0)]*(2-len(z))+z
                    vec.append((z[1]-b*z[0]/(2*a),sign*Q(h)*z[0]/(2*a)))
                vectors.append(vec)
        for vec in vectors:
            assert vec[0]==(Q(1),Q(0))
            assert all(vec[i]==vec[ch.du[i]] for i in range(ch.n))
            for i in range(ch.n):
                for j in range(ch.n):
                    assert qc.mul(vec[i],vec[j],q)==tuple(sum(ch.R[i][j][k]*vec[k][c] for k in range(ch.n)) for c in range(2))
            fval=(Q(0),Q(0))
            for i in range(ch.n):fval=qc.add(fval,qc.mul(vec[i],vec[ch.du[i]],q))
            out.append({'values':vec,'codegree':fval,'dimension':qc.div(D,fval,q)})
    return out

def build(R,height=3,duality=False):
    base=qc.base(R);q=base['q'];ch=base['ch'];chars=characters(ch,q,base['D']);known=collections.Counter(c['dimension'] for c in chars)
    assert all(n<=base['counts'][d] for d,n in known.items())
    original=qc.base;qc.base=lambda r:base
    try:A,b,meta=qc.system(R,height)
    finally:qc.base=original
    types,bound=qc.trace_types(q,base['primes'],height)
    selected=[];labels=[];keys=[];j=0
    for v,z in base['cols']:
        if not v[0]:
            for ti,_ in enumerate(types):selected.append(j);labels.append((None,None));keys.append(('high',v,ti));j+=1
            continue
        for h,c in enumerate(chars):
            if c['dimension']==z and (not duality or all(v[i]==v[ch.du[i]] for i in range(ch.n))):selected.append(j);labels.append((h,v));keys.append(('label',v,h))
        if base['counts'][z]>known[z]:selected.append(j);labels.append((None,None));keys.append(('anonymous',v,0))
        j+=1
    assert j<=len(A[0])
    for k in range(j,len(A[0])):selected.append(k);labels.append((None,None));keys.append(('extra',(),k))
    AA=[[row[j] for j in selected] for row in A];bb=list(b);extra=[]
    if duality:
        index={key:j for j,key in enumerate(keys)};assert len(index)==len(keys)
        groups=[];seen=set()
        for j,(kind,v,ti) in enumerate(keys):
            if j in seen:continue
            if kind in ('high','anonymous'):
                partner=index.get((kind,tuple(v[ch.du[i]] for i in range(ch.n)),ti))
                if partner is None:seen.add(j);continue
                group=sorted({j,partner})
            else:group=[j]
            seen.update(group);groups.append(group)
        AA=[[sum(row[j] for j in group) for group in groups] for row in AA]
        labels=[labels[group[0]] for group in groups];selected=list(range(len(groups)))
    for h in range(len(chars)):
        AA.append([int(label==h) for label,v in labels]);bb.append(1);extra.append(('label_count',h))
    for h in range(len(chars)):
        for k in range(h):
            rows=[[0]*len(selected),[0]*len(selected)]
            for j,(label,v) in enumerate(labels):
                if label not in (h,k):continue
                other=k if label==h else h
                ev=tuple(sum(v[i]*chars[other]['values'][i][c] for i in range(ch.n)) for c in range(2))
                val=qc.mul(chars[other]['dimension'],ev,q)
                if label==h:val=qc.scale(val,-1)
                for c in range(2):rows[c][j]=val[c]
            for c,row in enumerate(rows):
                den=math.lcm(*(Q(x).denominator for x in row));integer=[int(x*den) for x in row];g=math.gcd(*integer) or 1
                if any(integer):AA.append([x//g for x in integer]);bb.append(0);extra.append(('S_symmetry',h,k,c))
    meta['original_variables']=meta['variables'];meta['variables']=len(selected)
    meta['central_duality_orbits']=duality
    meta['labelled_characters']=[{'values':[[str(a),str(b)] for a,b in c['values']],'codegree':list(map(str,c['codegree'])),'dimension':list(map(str,c['dimension']))} for c in chars]
    meta['extra_rows']=extra
    return AA,bb,meta

def run(rid,height=3,control=False,duality=False):
    start=time.monotonic();R=qc.inputs(rid);A,b,m=build(R,height,duality)
    print(rid,'built',len(A),len(A[0]),'labels',len(m['labelled_characters']),flush=True)
    if control:
        import numpy as np
        from scipy.optimize import linprog
        from scipy.sparse import csc_matrix
        aa=np.array(A,dtype=float);rhs=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(np.max(abs(aa),axis=1),abs(rhs)))
        sol=linprog(np.zeros(aa.shape[1]),A_eq=csc_matrix(aa/scale[:,None]),b_eq=rhs/scale,bounds=(0,None),method='highs',options={'time_limit':120})
        ray=None;why={'control_numerical_feasible':bool(sol.success),'message':sol.message};outcome='known_model_control_survives' if sol.success else 'control_not_confirmed'
    else:
        ray,why=qc.exact_separator(A,b,timeout=90);outcome='candidate_exclusion_pending_independent_audit' if ray else 'no_conclusion'
    result={'id':rid,'kind':'quadratic_labelled_low_S_symmetry','height':height,'outcome':outcome,'metadata':m,'ray':ray,'solver_report':why,'seconds':time.monotonic()-start,'tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),'system_sha256':hashlib.sha256(json.dumps({'A':A,'b':b},separators=(',',':')).encode()).hexdigest()}
    if ray:result['bTy']=sum(x*y for x,y in zip(b,ray));result['minimum_ATy']=min(sum(row[j]*y for row,y in zip(A,ray)) for j in range(len(A[0])))
    (HERE/f'{rid}_h{height}{"_dual" if duality else ""}.json').write_text(json.dumps(result,indent=2)+'\n');print(rid,outcome,round(result['seconds'],3),result.get('bTy'),flush=True)
    return result

if __name__=='__main__':
    rid=sys.argv[1];run(rid,int(sys.argv[2]) if len(sys.argv)>2 else 3,'--control' in sys.argv,'--duality' in sys.argv)
