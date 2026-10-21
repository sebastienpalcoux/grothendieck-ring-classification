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


def galois_balance_data(data):
    """Each fixed distinguished fusion matrix has a rational spectrum."""
    R,a,b,characters,cols,Q,high,meta=data
    K=b['K'];K0=a['K'];z=K.from_sympy(K0.to_sympy(K0.unit));ii=K.from_sympy(source.s.I)
    need(K.unit==z+ii,'explicit compositum primitive element')
    trace=K(-K0.mod.to_list()[1]);images=[z+ii,z-ii,trace-z+ii,trace-z-ii]
    need(len(set(images))==4,'four distinct field automorphisms')
    for image in images:
        need(sum((K(c)*image**j for j,c in enumerate(reversed(K.mod.to_list()))),K.zero)==K.zero,'field embedding polynomial')
    def conjugates(x):
        return {sum((K(c)*image**j for j,c in enumerate(reversed(x.to_list()))),K.zero)for image in images}
    def key(x):return tuple(str(c)for c in x.to_list())
    allcols=list(cols)+[(0,)+tuple(v)for v,z in high];out=[]
    for E,ch in enumerate(characters):
        ratios=[]
        for col in allcols:
            dim=sum((K(x)*d for x,d in zip(col,b['ds'])),K.zero)
            ratios.append(b['D']/b['codegrees'][E]/K(b['multiplicities'][E])*source.modular.value(ch,col,K)/dim)
        seen=set()
        for value in ratios:
            if value in seen:continue
            orbit=conjugates(value);seen.update(orbit)
            if len(orbit)==1:continue
            ordered=sorted(orbit,key=key);reference=ordered[0]
            for partner in ordered[1:]:
                low=ratios[:5].count(reference)-ratios[:5].count(partner)
                high_coeff=[int(x==reference)-int(x==partner)for x in ratios[5:]]
                out.append({'character':E,'eigenvalue':list(key(reference)),
                    'conjugate_eigenvalue':list(key(partner)),'low_difference':low,
                    'high_difference_coefficients':high_coeff})
    return out
