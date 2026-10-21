"""Exact low-low-low Verlinde coefficients from a complete restriction multiset.

Scope: a pseudo-unitary categorification, and the distinguished central
objects must be selfdual. This does not construct the remaining S rows.
"""
import itertools
import character_modular as modular
import central_fusion
c=modular.c

def linear_coefficients(R,a,cols,permutation):
    """Return the low contribution and each high-column cubic contribution."""
    K=a['K'];chs=modular.characters(R,a)
    c.require(permutation in modular.assignments(a,chs,cols),'symmetric character assignment')
    c.require(all(ch[i]==ch[a['du'][i]] for ch in chs for i in range(8)),'selfdual distinguished simples')
    L=c.s.Matrix.hstack(*map(c.s.Matrix,cols));Q,high=modular.full.base.grams.high_columns(a,L)
    allcols=[tuple(v) for v in cols]+[(0,)+tuple(v) for v,z in high]
    values=[[a['D']/a['codegrees'][E]/K(a['multiplicities'][E])*modular.value(ch,v,K) for E,ch in enumerate(chs)] for v in allcols]
    dims=[sum((K(x)*y for x,y in zip(v,a['ds'])),K.zero) for v in allcols]
    inverse=[permutation.index(i) for i in range(5)];out=[]
    for triple in itertools.combinations_with_replacement(range(1,5),3):
        i,j,k=[inverse[z] for z in triple]
        coefficients=[sv[i]*sv[j]*sv[k]/d/a['D']**2 for sv,d in zip(values,dims)]
        out.append((triple,sum(coefficients[:5],K.zero),coefficients[5:]))
    return out

def coefficients(R,a,cols,counts,permutation):
    K=a['K'];chs=modular.characters(R,a)
    c.require(permutation in modular.assignments(a,chs,cols),'symmetric character assignment')
    c.require(all(ch[i]==ch[a['du'][i]] for ch in chs for i in range(8)),'selfdual distinguished simples')
    L=c.s.Matrix.hstack(*map(c.s.Matrix,cols));Q,high=modular.full.base.grams.high_columns(a,L)
    c.require(len(counts)==len(high) and all(isinstance(n,int) and n>=0 for n in counts),'integral high multiplicities')
    allcols=[(tuple(v),1) for v in cols]+[((0,)+tuple(v),n) for (v,z),n in zip(high,counts) if n]
    values=[[a['D']/a['codegrees'][E]/K(a['multiplicities'][E])*modular.value(ch,v,K) for E,ch in enumerate(chs)] for v,n in allcols]
    dims=[sum((K(x)*y for x,y in zip(v,a['ds'])),K.zero) for v,n in allcols]
    inverse=[permutation.index(i) for i in range(5)]
    triples=list(itertools.combinations_with_replacement(range(1,5),3));out=[]
    for triple in triples:
        i,j,k=[inverse[z] for z in triple]
        value=sum((K(n)*sv[i]*sv[j]*sv[k]/d for (v,n),sv,d in zip(allcols,values,dims)),K.zero)/a['D']**2
        co=list(map(c.s.Rational,c.ec(value)));integer=(not co) or (len(co)==1 and co[0].q==1 and co[0]>=0)
        out.append({'triple':list(triple),'field_coefficients':[str(x) for x in co],'nonnegative_integer':bool(integer),'value':int(co[0]) if integer and co else (0 if integer else None)})
    return out

def system(R,a,cols,counts,permutation):
    co=coefficients(R,a,cols,counts,permutation)
    c.require(all(row['nonnegative_integer'] for row in co),'all low Verlinde coefficients nonnegative integral')
    A,b,meta=central_fusion.system(R,a,cols,counts)
    for j,record in enumerate(co):
        row=[0]*len(A[0]);row[j]=1;A.append(row);b.append(record['value'])
    return A,b,dict(meta,verlinde_rows=len(co),character_assignment=list(permutation)),co
