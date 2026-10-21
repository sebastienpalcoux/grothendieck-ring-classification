"""Exact low cubic Verlinde coefficients, including complex dual rows."""
import itertools
import source
need=source.need


def linear_data(data):
    R,a,b,characters,cols,Q,high,meta=data
    K=b['K'];D=b['D'];multiplicities=b['multiplicities'];codegrees=b['codegrees']
    dual_chars=[]
    for ch in characters:
        dual=[ch[j]for j in a['du']]
        matches=[i for i,chi in enumerate(characters)if chi==dual]
        need(len(matches)==1,'unique dual character');dual_chars.append(matches[0])
    need(dual_chars==[0,1,3,2,4],'distinguished duality including complex pair')
    allcols=list(cols)+[(0,)+tuple(v)for v,z in high]
    values=[[D/codegrees[E]/K(multiplicities[E])*source.modular.value(ch,col,K)
             for E,ch in enumerate(characters)]for col in allcols]
    dims=[sum((K(x)*y for x,y in zip(col,b['ds'])),K.zero)for col in allcols]
    coefficients=[]
    for E,F in itertools.combinations_with_replacement(range(1,5),2):
        for G in range(1,5):
            cf=[v[E]*v[F]*v[dual_chars[G]]/dim/D**2 for v,dim in zip(values,dims)]
            coefficients.append(((E,F,G),sum(cf[:5],K.zero),cf[5:]))
    return coefficients,dual_chars


def evaluate(K,coefficient_data,counts):
    values=[]
    for triple,low,high in coefficient_data:
        value=low+sum((K(n)*v for n,v in zip(counts,high)),K.zero)
        c=value.to_list();integer=len(c)<=1 and(not c or(c[0].denominator==1 and c[0]>=0))
        values.append({'indices':list(triple),'power_basis':source.c.ec(value),'nonnegative_integer':bool(integer)})
    return values


if __name__=='__main__':
    d=source.data();co,dual=linear_data(d)
    print('PASS:40 exact distinguished cubic formulas, complex dual indices',dual)
