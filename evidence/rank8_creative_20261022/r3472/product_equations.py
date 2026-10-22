"""Exact Frobenius/unit/dimension constraints; no associativity is assumed."""
import itertools

def dualities(g,rows):
    dims=[(1,0)]*g
    blocks=[]
    for row in rows:
        ids=list(range(len(dims),len(dims)+row['multiplicity']))
        blocks.append(ids);dims += [tuple(row['dimension'])]*len(ids)
    for pairs in itertools.product(*(range(len(ids)//2+1) for ids in blocks)):
        dual=[(-i)%g for i in range(g)]+list(range(g,len(dims)))
        for ids,k in zip(blocks,pairs):
            for j in range(k):dual[ids[2*j]],dual[ids[2*j+1]]=ids[2*j+1],ids[2*j]
        yield dims,dual

def equations(dims,dual,g):
    n=len(dims); keys={};variables=[]
    def orbit(triple):
        i,j,k=triple
        return min((i,j,k),(j,k,i),(k,i,j),(dual[k],dual[j],dual[i]),(dual[j],dual[i],dual[k]),(dual[i],dual[k],dual[j]))
    for triple in itertools.product(range(1,n),repeat=3):
        key=orbit(triple)
        if key not in keys:keys[key]=len(variables);variables.append(key)
    eq=[];rhs=[]
    def add(terms,target):
        row={}
        for triple,c in terms:
            if 0 in triple:
                i,j,k=triple
                others=[v for v in triple if v!=0]
                fixed=1 if not others else int(len(others)==2 and others[1]==dual[others[0]])
                target-=fixed*c
            else:
                key=keys[orbit(triple)];row[key]=row.get(key,0)+c
        if row or target:eq.append(row);rhs.append(target)
    for i in range(n):
      a,b=dims[i]
      for j in range(n):
        c,d=dims[j]
        for field,target in [(0,a*c+2*b*d),(1,a*d+b*c)]:
          add([((i,j,dual[k]),dims[k][field]) for k in range(n)],target)
    # Pointed subgroup is cyclic for the first branch's prime orders.
    for i in range(g):
      for j in range(g):
       for k in range(n):add([((i,j,dual[k]),1)],int(k==(i+j)%g))
    A=[[row.get(j,0) for j in range(len(variables))] for row in eq]
    return A,rhs,variables

