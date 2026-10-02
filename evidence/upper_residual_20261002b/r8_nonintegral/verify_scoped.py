#!/usr/bin/env python3
"""Structural applications of scoped categorical results; no general ledger writes."""
import itertools
import json
from pathlib import Path
from verify_nonintegral import ROOT, load_recovery, require, tensor

def two_d_two():
    B=tensor(4)
    for i in range(4):
        B[0][i][i]=B[i][0][i]=1
    B[1][1][0]=1
    B[1][2][3]=B[2][1][3]=1
    B[1][3][2]=B[3][1][2]=1
    B[2][2]=B[3][3]=[1,0,2,2]
    B[2][3]=B[3][2]=[0,1,2,2]
    return B

def subrings(N,B):
    return [list(p) for p in ((0,)+q for q in itertools.permutations(range(1,8),3))
            if all(N[p[i]][p[j]][k]==0 for i,j in itertools.product(range(4),repeat=2)
                   for k in range(8) if k not in p)
            and all(B[i][j][k]==N[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(4),repeat=3))]

def verify():
    rec=load_recovery();source=rec.read_source(ROOT,8)
    receipts=[]
    B=two_d_two();rec.validate_ring(B)
    for case in ('R8_2_24','R8_2_152','R8_2_153','R8_2_166','R8_2_495'):
        N=source[case];matches=subrings(N,B)
        require(len(matches)==2,'unique 2D2 subring up to swapping nonunits')
        p=matches[0];even=list(p);odd=[i for i in range(8) if i not in even]
        require(all(N[i][j][k]==0 for i,j in itertools.product(odd,repeat=2) for k in odd),'C2 grading')
        inv=[i for i in range(8) if all(sum(N[i][j])==1 for j in range(8))]
        if case=='R8_2_24':
            require(len(inv)==4 and all(N[i][j][k]==N[j][i][k] for i,j,k in itertools.product(range(8),repeat=3)),'commutative C4-invertible case')
            u=next(i for i in odd if i in inv)
            require(N[u][u][p[1]]==1 and sum(N[u][u])==1,'odd invertible square is neutral g')
        else:
            require(set(inv).issubset(even),'odd component has no invertible object')
        receipts.append({'id':case,'scope':'unitary_impossible','neutral_model_to_source':p,
                         'odd_indices':odd,'source_sha256':rec.fingerprint(N)})
    from extension_models import psu_flip
    bases={name:[[[psu_flip(pseudo,False)[i][j][k] for k in range(4)]for j in range(4)]for i in range(4)]
           for name,pseudo in (('ordinary',False),('pseudo',True))}
    for case in ('R8_2_312','R8_2_315','R8_2_317'):
        N=source[case];P=subrings(N,bases['pseudo'])
        require(P,'pseudo-PSU subring')
        g=P[0][1]
        if case=='R8_2_312':
            fixed=[i for i in range(8) if i not in P[0] and N[g][i][i]==1 and sum(N[g][i])==1]
            require(fixed,'additional g-fixed simple forces trivial pointed associator')
            facts={'pseudo_subring':P[0],'g_fixed_indices':fixed}
            scope='pseudo_unitary_impossible'
        else:
            O=subrings(N,bases['ordinary']);require(O and O[0][1]==g,'ordinary/pseudo common invertible')
            facts={'pseudo_subring':P[0],'ordinary_subring':O[0],'shared_g':g}
            scope='unitary_impossible'
        receipts.append({'id':case,'scope':scope,'source_sha256':rec.fingerprint(N),**facts})
    for case in ('R8_1_9','R8_1_18','R8_1_49'):
        N=source[case]
        inv=[i for i in range(8) if all(sum(N[i][j])==1 for j in range(8))]
        require(len(inv)==4,'four invertibles')
        non=[i for i in range(8) if i not in inv]
        dims=[(1,0) if i in inv else (2,1) for i in range(8)] # Z[sqrt5].
        def mul(x,y):
            a,b=x;c,d=y;return(a*c+5*b*d,a*d+b*c)
        for i,j in itertools.product(range(8),repeat=2):
            value=tuple(sum(N[i][j][k]*dims[k][a] for k in range(8)) for a in (0,1))
            require(value==mul(dims[i],dims[j]),'exact two-dimension FP character')
        require(all({next(k for k,c in enumerate(N[g][x]) if c) for g in inv}==set(non) for x in non),'transitive generalized near-group action')
        require(mul((2,1),(2,1))==(9,4),'d squared equals 1+4d')
        receipts.append({'id':case,'scope':'braided_impossible','source_sha256':rec.fingerprint(N),
                         'fpdim_noninvertible':'2+sqrt(5)',
                         'existence_scopes_equivalent':['general','pivotal','spherical','pseudo_unitary'],
                         'unitary_status':'unresolved','central_bosonicity':'unproved'})
    return {'status':'PASS','general_ledger_changes':False,'scoped_applications':receipts,
            'theoretical_sources':'SCOPED_RESULTS.md','optimization_safe':True}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args()
    text=json.dumps(verify(),indent=2)
    if args.output:args.output.write_text(text+'\n')
    print(text)
