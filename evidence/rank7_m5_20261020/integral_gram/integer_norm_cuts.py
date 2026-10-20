"""Exact linear consequences of integer fusion-product squared norms.

For a positive product P, write its coefficients as n_Y>=0.  For any
rational source vector x, n_Y^2-(x.v_Y)n_Y >= -g*(x.v_Y), where
g*(t)=max_{k>=0 integer}(tk-k^2).  On known induced-unit simples use the
integer chord n^2 >= (2a+1)n-a(a+1), with any fixed integer a.  Summing
and using the monoidal forgetful map gives the exported global inequality.
All coefficients below are rebuilt from the canonical source characters.
"""
import sys
from fractions import Fraction as F

import explore as e

sys.path.insert(0,str(e.HERE.parent/'computation'))
from word_coefficients import coefficients

q=e.q


def conjugate_square(t,positive=True):
    t=F(t);k=t.numerator//(2*t.denominator)
    candidates={k,k+1}
    if positive:candidates={0,max(0,k),max(0,k+1)}
    return max(t*n-n*n for n in candidates)


def coefficient_cut(table,dom,label,N,dual,V,record):
    q.require(record['id']==dom['id'],'integer norm cut source identity')
    low=[(1,0,0,0,0,0,0)]+[tuple(v) for v in dom['low']]
    assigned=dict(zip(label,low));K=table.K
    conjugates={i:table.rows.index(tuple(row[dual[j]] for j in range(7))) for i,row in enumerate(table.rows)}
    E,F0=record['characters'];x=list(map(F,record['x']));base=record['low_coefficients_at_witness']
    q.require(len(x)==len(base)==7 and all(type(a)==int for a in base),'rational multiplier and integral low chord centers')
    product=[sum(assigned[E][i]*assigned[F0][j]*N[i][j][k] for i in range(7) for j in range(7)) for k in range(7)]
    alpha=[2*a+1-sum(t*z for t,z in zip(x,v)) for a,v in zip(base,low)]
    constant=sum(t*a for t,a in zip(x,product))-sum(a*(a+1) for a in base)
    W=coefficients(table,dom,[[E,F0,conjugates[E],conjugates[F0]]])
    triple_index={tuple(t):i for i,t in enumerate(V['triples'])}
    nknown=[];ncols=[]
    for G in label:
        if G==table.fp:
            nknown.append(F(int(E==conjugates[F0])));ncols.append([F(0)]*len(dom['orbits']))
        else:
            j=triple_index[tuple(sorted((E,F0,conjugates[G])))];nknown.append(F(V['known'][2*j]));ncols.append([F(c[2*j]) for c in V['orbits']])
    target=constant+sum(a*b for a,b in zip(alpha,nknown))-F(W['known'][0])
    col=[]
    for j,orb in enumerate(dom['orbits']):
        gsum=sum(conjugate_square(sum(a*b for a,b in zip(x,(0,)+tuple(v)))) for v,g,z in orb)
        col.append(F(W['orbits'][j][0])+gsum-sum(a*b[j] for a,b in zip(alpha,ncols)))
    return {'coefficients':list(map(str,col)),'rhs':str(target),'sense':'>=',
            'domain_sha256':V['domain_sha256'],'characters':[E,F0],
            'quartic_word':W['words'][0],'x':list(map(str,x)),
            'source_product':product,'low_chord_centers':base,
            'low_linear_weights':list(map(str,alpha)),'constant':str(constant)}


def append_cuts(columns,rhs,labels,cuts):
    for cut in cuts:
        costs=list(map(F,cut['coefficients']))
        for j,col in enumerate(columns):
            col.append(labels[j]['multiplicity_unit']*costs[labels[j]['orbit']] if j<len(labels) else F(0))
        rhs.append(F(cut['rhs']))
        slack=[F(0)]*len(rhs);slack[-1]=-1;columns.append(slack)
    return columns,rhs,labels
