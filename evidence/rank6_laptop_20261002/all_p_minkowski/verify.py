"""Verify all-p Lim certificates for both rank-six residual fusion tensors.
No numerical search, SciPy, NumPy, or absolute paths. SymPy only.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sympy as s
from arithmetic import Embedding, polynomial, require


def verify_record(record, expected_tensor=None):
    N=record['tensor'];r=len(N)
    require(r==6 and all(len(M)==r and all(len(row)==r for row in M) for M in N), 'tensor shape')
    require(all(type(x)is int and x>=0 for M in N for row in M for x in row), 'nonnegative integer tensor')
    digest=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
    require(digest==record['tensor_sha256'], 'tensor hash')
    if expected_tensor is not None:
        require(N==expected_tensor, 'external census mismatch')
    f=polynomial(record['field_polynomial'])
    require(f.is_irreducible, 'number-field polynomial reducible')
    K=s.QQ.alg_field_from_poly(f,alias='a')
    embedding=Embedding(f,record['root_interval'])
    read=lambda coefficients:K([s.Rational(x) for x in coefficients])
    d=list(map(read,record['dimensions']))
    require(len(d)==r and d[0]==K.one, 'dimension-vector normalization')
    require(all(embedding.sign(x)==1 for x in d), 'positive dimensions')
    require(all(N[0][i][j]==N[i][0][j]==int(i==j) for i,j in itertools.product(range(r),repeat=2)), 'unit')
    for i,j in itertools.product(range(r),repeat=2):
        require(sum((K(N[i][j][k])*d[k] for k in range(r)),K.zero)==d[i]*d[j], 'exact FP character')
    P=[[[K(N[i][j][k])*d[k]/(d[i]*d[j]) for k in range(r)] for j in range(r)] for i in range(r)]
    require(all(sum(row,K.zero)==K.one for M in P for row in M), 'stochastic fusion coefficients')
    noninvertible=[i for i in range(r) if d[i]!=K.one]
    couplings={}
    for entry in record['couplings']:
        triple=tuple(entry['ijk'])
        require(triple not in couplings, 'duplicate triple')
        couplings[triple]=entry['entries']
    require(set(couplings)==set(itertools.product(noninvertible,repeat=3)), 'incomplete noninvertible-triple coverage')
    stored_entries=generated_entries=0
    for i,j,k in itertools.product(range(r),repeat=3):
        mu=P[i][j];nu=P[j][k]
        values={}
        if (i,j,k) in couplings:
            for l,m,n,coefficients in couplings[(i,j,k)]:
                label=(l,m,n)
                require(all(type(x)is int and 0<=x<r for x in label), 'coupling label')
                require(label not in values, 'duplicate coupling entry')
                q=read(coefficients)
                require(embedding.sign(q)>=0, 'negative coupling probability')
                values[label]=q
            stored_entries+=len(values)
        else:
            support_mu=[l for l,x in enumerate(mu) if x]
            support_nu=[m for m,x in enumerate(nu) if x]
            if len(support_mu)==1:
                l=support_mu[0]
                for m,n in itertools.product(range(r),repeat=2):
                    q=nu[m]*P[i][m][n]
                    if q:values[(l,m,n)]=q
            else:
                require(len(support_nu)==1, 'automatic coupling unavailable')
                m=support_nu[0]
                for l,n in itertools.product(range(r),repeat=2):
                    q=mu[l]*P[l][k][n]
                    if q:values[(l,m,n)]=q
            require(all(embedding.sign(q)>=0 for q in values.values()), 'negative automatic coupling')
            generated_entries+=len(values)
        lm=[[K.zero for unused in range(r)]for unused in range(r)]
        ln=[[K.zero for unused in range(r)]for unused in range(r)]
        mn=[[K.zero for unused in range(r)]for unused in range(r)]
        for (l,m,n),q in values.items():
            lm[l][m]+=q;ln[l][n]+=q;mn[m][n]+=q
        for a,b in itertools.product(range(r),repeat=2):
            require(lm[a][b]==mu[a]*nu[b], 'independence marginal mismatch')
            require(ln[a][b]==mu[a]*P[a][k][b], 'left conditional marginal mismatch')
            require(mn[a][b]==nu[a]*P[i][a][b], 'right conditional marginal mismatch')
    return {'id':record['id'],'status':'PASS','tensor_sha256':digest,
            'scope':'every Corollary 3.4 Lim inequality, every real p>=1 and every nonnegative vector; no categorification conclusion',
            'rank':r,'triples_checked':r**3,'stored_noninvertible_triples':len(couplings),
            'automatic_triples':r**3-len(couplings),'stored_nonzero_entries':stored_entries,
            'automatic_nonzero_entries':generated_entries,'marginal_equalities_checked':3*r**5,
            'arithmetic':'exact rational number fields; coefficient signs by real-root isolation'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates',type=Path,default=Path(__file__).resolve().with_name('certificates.json'))
    parser.add_argument('--tensors',type=Path,help='optional external unresolved_tensors.json; compares both full tensors')
    args=parser.parse_args()
    records=json.loads(args.certificates.read_text())
    expected=None
    if args.tensors:
        expected={x['id']:x.get('N',x.get('tensor')) for x in json.loads(args.tensors.read_text())}
    require([x['id'] for x in records]==['R6_4_155','R6_8_1660'], 'unexpected case list')
    results=[verify_record(x,None if expected is None else expected[x['id']]) for x in records]
    print(json.dumps({'status':'PASS','results':results},indent=2))

if __name__=='__main__':
    main()
