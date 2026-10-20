"""Exact linear coefficients for low-word unit multiplicities.

The output has one rational and sqrt(5) coordinate per word, in that order.
For an orbit variable, multiply its column by its phase multiplicity unit.
known+sum(count*orbitcolumn) must have nonnegative integer rational entries
and zero sqrt(5) entries. Words refer to exact character-table indices.
"""
import hashlib,json,sys
from pathlib import Path
from fractions import Fraction as F
import sympy as s
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'criteria'))
import q5_modular_low as modular
q=modular.q


def coefficients(table,dom,words):
    K=table.K;n=K.mod.degree()
    def vector(x):
        c=[F(str(t)) for t in x.to_list()];return [F(0)]*(n-len(c))+c
    one=vector(K.one);root=vector(K.from_sympy(s.sqrt(5)))
    a0,b0=next((i,j) for i in range(n) for j in range(i+1,n) if one[i]*root[j]!=one[j]*root[i])
    det=one[a0]*root[b0]-one[b0]*root[a0]
    def quadratic(value):
        v=vector(value);a=(v[a0]*root[b0]-v[b0]*root[a0])/det;b=(one[a0]*v[b0]-one[b0]*v[a0])/det
        q.require(all(x==a*y+b*z for x,y,z in zip(v,one,root)),'whole orbit word coefficient is real quadratic')
        return a,b
    groups=[[(1,0,0,0,0,0,0)]+[tuple(v) for v in dom['low']]]+[[(0,)+tuple(v) for v,g,z in orb] for orb in dom['orbits']]
    values=[]
    for group in groups:
        for row in group:table.prepare(row)
        result=[]
        for word in words:
            k=len(word);factor=table.D**(k-2)
            for E in word:factor/=table.codegrees[E]
            total=K.zero
            for row in group:
                prod=K.one/table.dims[row]**(k-2)
                for E in word:prod*=table.values[E,row]
                total+=prod
            result.extend(str(x) for x in quadratic(factor*total))
        values.append(result)
    return {'words':words,'known':values[0],'orbits':values[1:],'domain_sha256':hashlib.sha256(json.dumps({'low':dom['low'],'orbits':dom['orbits']},sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'schema':'Each word contributes [rational,sqrt5] coefficients; orbit columns are unscaled by phase multiplicity.'}


def main():
    rid='R7_5_3895';data=json.loads((HERE.parent/'integral_gram'/(rid+'_full_field_verlinde_branch165.json')).read_text())
    N=next(r['tensor'] for r in json.loads((HERE/'source_frontier.json').read_text()) if r['id']==rid)
    ds,D,B,zs,T,signs=q.source_data(N,rid);table=modular.ExactQuadraticCharacterTable(N,ds,5)
    result=coefficients(table,data,[[1]*4,[1]*5]);result['id']=rid;result['source_sha256']=q.tensor_hash(N)
    target=HERE/(rid+'_full_field_word_coefficients.json');target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'id':rid,'known':result['known'],'orbits':len(result['orbits']),'path':str(target)}))

if __name__=='__main__':main()
