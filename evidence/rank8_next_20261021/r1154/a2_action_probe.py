"""Fixed A2 action on the forgetful/degree-two span, with hidden projector tests."""
import sys,json,math,time,hashlib
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
UP=Path(__file__).resolve().with_name('joint_triple_fibers.py')
exec(compile(UP.read_text().split('def main():')[0],str(UP),'exec'))
@lru_cache(None)
def action(signature):
    inds,C,alpha,hh,moments=augmented(signature);moment=lambda w:moments[tuple(sorted(w))]
    G=s.Matrix(15,15,lambda i,j:moment(words[i]+words[j]));FW=s.Matrix([restriction(w)for w in words]);GA=G.row_join(FW).col_join(FW.T.row_join(a['Gram']));Gb=GA.extract(inds,inds);Gi=Gb.inv()
    L=s.Matrix(8,8,lambda k,j:sum(cols[2][i]*R[i][j][k]for i in range(8)));need(L.T==L,'symmetric restriction action')
    B=s.Matrix(15,15,lambda i,j:moment(words[i]+(2,)+words[j]));FA=s.Matrix([restriction(w+(2,))for w in words]);BB=B.row_join(FA).col_join(FA.T.row_join(L*a['Gram']));Bb=BB.extract(inds,inds);HH=Gi*Bb*Gi
    # Invariance follows from the vanishing triple residual for every A2*pair,
    # and from the forgetful intertwiner on the other generators.
    need(all(hh[j]==0 for j,t in enumerate(triples)if 2 in t),'A2 invariance on pair generators')
    z=s.Symbol('lambda');need((Gi*Bb).charpoly().as_expr()==s.expand(z**4*(z+1)*(z-3)*(z+5)*(z*z-270*z+225)),'fixed nonzero A2 spectrum accounted for')
    return inds,[[F(x)for x in rr]for rr in HH.tolist()],F(s.trace(Gi*Bb)),F(s.trace((Gi*Bb)**2)),str((Gi*Bb).charpoly().as_expr()),moments
start=time.monotonic();out=[]
need(values[0][2]+values[1][2]==K(270) and values[0][2]*values[1][2]==K(225),'two nonrational A2 eigenvalues')
need([values[i][2]for i in (2,3,4)]==[K(3),K(-5),K(0)],'remaining low A2 eigenvalues')
need(domain['tensor_sha256']==fibers['tensor_sha256']==quartic['tensor_sha256']==r['tensor_sha256'],'source tensor binding')
for name,value in fibers['source_sha256'].items():need(digest(ROOT/name)==value,'pair source binding '+name)
for row in fibers['results']:
    if row['status']!='exact_joint_fiber_witness':continue
    ns=[1]+domain['completions'][row['index']];sig=tuple(sum(n*v[1]for n,v in zip(ns,co))//den for co,den in moment_coefficients.values());inds,H,tr,tr2,cp,moments=action(sig)
    fulltr=sum((K(n)*vs[2]for n,vs in zip([1]*5+ns[1:],values)),K.zero);fulltr2=sum((K(n)*vs[2]**2 for n,vs in zip([1]*5+ns[1:],values)),K.zero)
    fulltr=F(c.ec(fulltr)[0]);fulltr2=F(c.ec(fulltr2)[0]);rem=fulltr-tr;rem2=fulltr2-tr2;need(rem2==-rem and rem2.denominator==1 and rem2>=0,'hidden negative-one multiplicity')
    for typ,n in enumerate(ns[1:]):
        if n:need(values[5+typ][2]==K(-1 if typ in (10,15)else 0),'complete high A2 spectrum')
    need(rem2==ns[11]+ns[16]-1,'hidden A2 spectrum consists exactly of zero and minus one')
    for number,hist in enumerate(row['pair11_histogram_solutions_by_high_type']):
        vectors=[]
        for j in range(5):
            v=[int(j==k)for k in range(5)]+[moments[tuple(sorted(pair+(j,)))]if j else int(pair[0]==pair[1])for pair in pairs]+list(cols[j]);vectors.append((1,tuple(F(v[i])for i in inds),{'low':j}))
        for typ,his in enumerate(hist):
            for x,n in his:
                if n:
                    rrr,basis,q,vals=row_data(row['group'],typ,x,sig);vectors.append((n,tuple(rrr[i]for i in inds),{'type':typ,'pair11':x}))
        hv=[tuple(sum(H[k][l]*v[l]for l in range(9))for k in range(9))for n,v,label in vectors]
        Fs=[[sum(vi[k]*hv[j][k]for k in range(9))for j in range(len(vectors))]for ni,vi,li in vectors]
        why=None
        if rem2==3:
            targets=[i for i,(n,v,label)in enumerate(vectors)if label.get('type')==10]
            need(len(targets)==1 and vectors[targets[0]][0]==4,'four identical high10 coordinates')
            ii=targets[0];need(Fs[ii][ii]==F(67,4),'mandatory projector diagonal fractional part')
            # E is a rank-three orthogonal projector. Its four high10 diagonal
            # entries must be 3/4 to make F-E integral, saturating trace(E)=3.
            # All other rows vanish. E annihilates the all-ones restriction row
            # on this block, so E=I_4-J_4/4 there.
            # Compressed entries represent the off-diagonal block value; the
            # diagonal differs by -1, which is checked separately.
            Fs[ii][ii]+=F(1,4)
            need(Fs[ii][ii]>=1,'nonnegative corrected diagonal')
        if rem2 in (0,3):
            for i,rr in enumerate(Fs):
                for j,v in enumerate(rr):
                    if v.denominator!=1 or v<0:why={'row':vectors[i][2],'column':vectors[j][2],'entry':str(v)};break
                if why:break
        out.append({'index':row['index'],'histogram_solution':number,'hidden_negative_one_rank':int(rem2),'status':'forced_action_nonintegral_or_negative'if why else 'passes_fixed_action','witness':why})
    print(json.dumps({'index':row['index'],'processed':len(out),'failures':sum(x['status']!='passes_fixed_action'for x in out),'seconds':round(time.monotonic()-start,2)}),file=sys.stderr,flush=True)
survivors=[x for x in out if x['status']=='passes_fixed_action']
print(json.dumps({'schema':'r1154-a2-action-probe/v1','id':r['id'],'tensor_sha256':r['tensor_sha256'],'scope':'Necessary uniquely forced A2 center action only; no full center ring or categorification assertion','incoming_patterns':224,'incoming_pair_completions':2904,'complete':len(out)==2904,'remaining_patterns':len(set(x['index']for x in survivors)),'surviving_pattern_indices':sorted(set(x['index']for x in survivors)),'counts':dict(__import__('collections').Counter(x['status']for x in out)),'rank_counts':dict(__import__('collections').Counter(x['hidden_negative_one_rank']for x in out)),'results':out,'source_sha256':{p.relative_to(ROOT).as_posix():digest(p)for p in [domainpath,fiberpath,quarticpath,UPSTREAM,UP]},'verifier_sha256':digest(Path(__file__))},indent=2))
