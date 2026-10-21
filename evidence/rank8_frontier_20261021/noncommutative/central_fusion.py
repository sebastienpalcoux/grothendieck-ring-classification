"""Forgetful tensor equations and low-block Frobenius reciprocity."""
import itertools
import integral_gram
c=integral_gram.c;full=integral_gram.full

def system(R,a,cols,counts):
    L=c.s.Matrix.hstack(*map(c.s.Matrix,cols));Q,high=full.base.grams.high_columns(a,L)
    active=[((0,)+tuple(v),i) for i,((v,z),count) in enumerate(zip(high,counts)) if count]
    triples=list(itertools.combinations_with_replacement(range(1,5),3));pairs=list(itertools.combinations_with_replacement(range(1,5),2))
    labels=[('low',triple) for triple in triples]+[('high',pair,index) for pair in pairs for v,index in active]
    A=[];b=[]
    # The four nonunit distinguished objects are selfdual: all irreducible
    # trace characters are fixed by i -> i*. Thus low fusion coefficients
    # N_ij^k are symmetric in i,j,k; N_ij^1 is delta_ij.
    for i,j in pairs:
        target=[sum(cols[i][u]*cols[j][v]*R[u][v][k] for u in range(8) for v in range(8))-int(i==j and k==0) for k in range(8)]
        for k in range(8):
            row=[0]*len(labels)
            for ell in range(1,5):row[triples.index(tuple(sorted((i,j,ell))))]+=cols[ell][k]
            for v,index in active:row[labels.index(('high',(i,j),index))]=v[k]
            A.append(row);b.append(target[k])
    return A,b,{'rows':len(A),'variables':len(labels),'active_high_indices':[i for v,i in active]}
