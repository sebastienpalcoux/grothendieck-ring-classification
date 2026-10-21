"""Joint Galois spectral multiplicities for the complete quartic integer domain."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import argparse,hashlib,itertools,json
import verify as base
need=base.need;HERE=Path(__file__).resolve().parent;FRONTIER=HERE.parent


def one(number,patterns):
    base.rotation.install();rec=base.source.data(number)
    frozen=json.loads((FRONTIER/'quartic_integer_center/source.json').read_text())
    need(rec==next(r for r in frozen['records']if r['id']==f'R8_3_{number}'),'complete source binding')
    R=rec['tensor'];a=base.rotation.bq.data(R);K=a['K'];chars=base.modular.characters(R,a)
    need(chars[0]==a['ds'],'FP character first')
    columns=[tuple(c)for c in rec['low_columns']]+[(0,)+tuple(v)for v in rec['canonical_high_vectors']]
    values=[]
    for col in columns:
        dim=sum((K(v)*d for v,d in zip(col,a['ds'])),K.zero)
        values.append(tuple(a['coords'](a['D']/a['codegrees'][E]/K(a['multiplicities'][E])*base.modular.value(ch,col,K)/dim)for E,ch in enumerate(chars)))
    def conj(t,e2,e3):return tuple((z[0],z[1]*e2,z[2]*e3,z[3]*e2*e3)for z in t)
    need(len(values)==70,'five distinct low simples counted once and65 high types')
    conjugates={(t,e2,e3):conj(t,e2,e3)for t in values for e2,e3 in itertools.product((-1,1),repeat=2)}
    cases=[];survivors=[]
    for index,pattern in enumerate(patterns):
        weights=[1]*5+pattern;counts=Counter()
        for t,m in zip(values,weights):counts[t]+=m
        failure=None
        for t in sorted(counts):
            for e2,e3 in itertools.product((-1,1),repeat=2):
                ct=conjugates[t,e2,e3]
                if counts[t]!=counts[ct]:
                    failure={'tuple':[list(map(str,z))for z in t],'signs':[e2,e3],
                             'multiplicity':counts[t],'conjugate_multiplicity':counts[ct]};break
            if failure is not None:break
        cases.append({'pattern_index':index,'passes':failure is None,'first_exact_failure':failure})
        if failure is None:survivors.append(index)
    return {'id':f'R8_3_{number}','tensor_sha256':rec['tensor_sha256'],
        'low_high_joint_eigenvalue_tuples':[[list(map(str,z))for z in t]for t in values],
        'matrix_character_divisor':2,'complete_pattern_count':len(patterns),'cases':cases,'surviving_indices':survivors,
        'scope':'joint spectra of commuting integral center fusion matrices; general-complex necessary condition after the verified Galois-pseudo-unitary gate'}


def known_control():
    s=base.s;r=s.sqrt(5);phi=(1+r)/2
    N=s.Matrix([[0,1],[1,1]]);F=s.kronecker_product(N,N)
    S=s.kronecker_product(s.Matrix([[1,phi],[phi,-1]]),s.Matrix([[1,phi],[phi,-1]]))
    dims=[1,phi,phi,phi**2];eigen=[s.simplify(S[3,j]/dims[j])for j in range(4)]
    need((F*S-S*s.diag(*eigen)).applyfunc(s.simplify)==s.zeros(4),'actual Z(Fib) integer fusion matrix and S eigenvectors')
    tuples=[(s.Integer(1),z)for z in eigen]
    conjugate=[tuple(s.simplify(x.xreplace({r:-r}))for x in t)for t in tuples]
    need(Counter(tuples)==Counter(conjugate),'actual center joint Galois multiplicities')
    return {'actual_category':'Z(Fib)','distinguished_integer_fusion_matrices':[s.eye(4).tolist(),F.tolist()],
        'joint_eigenvalue_tuples':[[str(v)for v in t]for t in tuples],'nontrivial_Galois_balance':True}


def run(write):
    path=HERE/'joint_spectrum.json';p=FRONTIER/'quartic_integer_center/gram_cubic.json';prior=json.loads(p.read_text());need(len(prior['patterns'])==343,'complete joint integer domain')
    records=[one(n,prior['patterns'])for n in(928,941)]
    out={'kind':'joint_distinguished_center_Galois_multiplicity_balance','actual_known_model_control':known_control(),'integer_domain_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'records':records}
    if write:path.write_text(json.dumps(out,indent=2,default=int)+'\n')
    else:need(out==json.loads(path.read_text()),'joint spectral receipt')
    for r in records:print(r['id'],'joint Galois survivors',len(r['surviving_indices']),flush=True)
    print('PASS complete quartic joint spectral balance',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');run(p.parse_args().write)
