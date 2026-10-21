"""Exact bosonic quotient obstruction and forced fermionic translated twists."""
from pathlib import Path
import argparse,gzip,hashlib,itertools,json
import sympy as s
import source
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2];need=source.need
RANK4='manuscripts/rank4/papers/companion_sections/14_finite_certification.tex'
RANK4_SHA='0ec47c3c3da2c46bfee20b06214b9f7704edea841955cb2c86b7b0522f199e8b'

def run():
    data=source.run();need(data==json.loads((HERE/'source.json').read_text()),'source receipt')
    row=data['records'][1];R=row['tensor'];g=3
    perm=[next(k for k in range(8)if R[g][i][k])for i in range(8)]
    need(all(R[g][i]==[int(k==perm[i])for k in range(8)]and R[g][i]==R[i][g]
        and perm[i]!=i and perm[perm[i]]==i for i in range(8)),'central free involution')
    orbits=sorted({tuple(sorted((i,perm[i])))for i in range(8)})
    Q=[[[sum(R[A[0]][B[0]][k]for k in C)for C in orbits]for B in orbits]for A in orbits]
    need(all(sum(R[i][j][k]for k in C)==Q[a][b][c]for a,A in enumerate(orbits)
             for b,B in enumerate(orbits)for c,C in enumerate(orbits)for i in A for j in B),'quotient representative independence')
    need(all(sum(Q[i][j][a]*Q[a][k][h]for a in range(4))==sum(Q[j][k][a]*Q[i][a][h]for a in range(4))
             for i,j,k,h in itertools.product(range(4),repeat=4)),'quotient associativity')
    a=source.c.data(R);K=a['K'];D=a['D'];dims=[a['ds'][o[0]]for o in orbits]
    need(sum((v*v for v in dims),K.zero)*K(2)==D,'quotient FP dimension')
    positive_roots=[]
    for q in (2,3):positive_roots.append(next(x for x in source.discover_roots(s.Poly(source.c.w.t**2-q,source.c.w.t),K)if a['embedding'].sign(x)>0))
    r2,r3=positive_roots;expect=K(72)+K(48)*r2+K(40)*r3+K(28)*r2*r3
    need(D/K(2)==expect and a['embedding'].sign(expect-K(72))>0,'exact quotient dimension')
    theorem=(REPO/RANK4).read_bytes();need(hashlib.sha256(theorem).hexdigest()==RANK4_SHA,'rank-four theorem pin')
    need(b'Every rank-four complex fusion category satisfies' in theorem,'unrestricted theorem statement')
    need(21**2>12**2*3 and 72>45,'24+12sqrt3 <45 <72 < quotient dimension')
    histpath=REPO/'supplements/rank4/data/historical_32.json.gz';hist=json.loads(gzip.decompress(histpath.read_bytes()))[169]
    p=[0,3,1,2]
    need(all(hist[i][j][k]==Q[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(4),repeat=3)),'full64 historical tensor match')
    mappingpath=REPO/'supplements/rank4/data/through32_mapping.json.gz';mapping=json.loads(gzip.decompress(mappingpath.read_bytes()))[169]
    need(mapping['label']=='F_{6,19}'and mapping['old_zero_based_index']==169,'historical label binding')
    translates=[]
    for E,col in enumerate(row['low_columns']):
        tr=[0]*8
        for i,m in enumerate(col):tr[perm[i]]+=m
        need(tr[0]==0,'translated low is high')
        j=row['canonical_high_vectors'].index(tr[1:]);ch=[s.Rational(v)for v in row['full_characters'][E][g]]
        m=row['irreducible_dimensions'][E];need(ch[1:]==[0,0,0]and abs(ch[0])==m,'invertible scalar on irreducible')
        twist=-ch[0]/m;need(twist in(-1,1),'fermionic translated twist')
        translates.append({'low_index':E,'high_index':j,'monodromy':int(-twist),'forced_twist':int(twist),
                           'moments_1_through_6':[int(twist**k)for k in range(1,7)]})
    grams=json.loads((HERE/'gram_cubic.json').read_text());need(len(grams['patterns'])==343,'complete joint pattern receipt')
    need(all(all(m[t['high_index']]==1 for t in translates)for m in grams['patterns']),'forced unique translates in every pattern')
    return {'id':row['id'],'tensor_sha256':row['tensor_sha256'],'order_two_object':g,'free_source_permutation':perm,
        'bosonic_branch':{'outcome':'excluded_by_unrestricted_rank_four_bound','orbits':orbits,'quotient_tensor':Q,
            'quotient_global_dimension':'72+48sqrt(2)+40sqrt(3)+28sqrt(6)','historical_label':'F_{6,19}',
            'historical_source_to_quotient_basis_map':p,
            'dependencies':[{'path':RANK4,'sha256':RANK4_SHA},
                {'path':str(histpath.relative_to(REPO)),'sha256':hashlib.sha256(histpath.read_bytes()).hexdigest()},
                {'path':str(mappingpath.relative_to(REPO)),'sha256':hashlib.sha256(mappingpath.read_bytes()).hexdigest()}]},
        'fermionic_branch':{'outcome':'necessary_central_lift_has_twist_minus_one','translated_low_twists':translates},
        'source_receipt_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),
        'gram_receipt_sha256':hashlib.sha256((HERE/'gram_cubic.json').read_bytes()).hexdigest(),
        'scope':'under the independently verified Galois-PU reduction, unique central lift and positive source indicator; no rank-four bound is applied to a fermionic quotient'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    actual=json.loads(json.dumps(run(),default=int));path=HERE/'r941_fermionic.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'fermionic branch receipt differs')
    print('PASS941: bosonic rank-four quotient excluded; five fermionic translated twists fixed.')
