"""Complete exact character tables from a separating spectrum of degree <=2.

This removes the discovery constructor's one/two-generator restriction.
It adds no mathematical condition to the inherited reciprocity criterion.
"""
import sys
import sympy as s
from quadratic_compression import ROOT
sys.path.insert(0,str(ROOT/'supplements/rank7/software'))
from character_induction import CharacterTable, roots_degree_two
from rings import Characters
from exact import require


class ExactQuadraticCharacterTable(CharacterTable):
    def __init__(self,R,dimensions,radicand):
        a=Characters(R)
        self.n=n=len(R);self.du=a.du;self.seed=(a.k,)
        require(all(R[i][j]==R[j][i] for i in range(n) for j in range(n)), 'commutative character table')
        require(all(f.degree()<=2 for f,m in a.components), 'quadratic separating spectrum')
        roots=[v for f,m in a.components for v in roots_degree_two(f)]
        self.K=K=s.QQ.algebraic_field(*roots,s.sqrt(radicand))
        self.rows=[];self.codegrees=[]
        for f,m in a.components:
            _,ds,_,_=a.component(f)
            for root in roots_degree_two(f):
                row=tuple(K.from_sympy(s.expand(sum(s.Rational(c)*root**(len(v.to_list())-1-j)
                                   for j,c in enumerate(v.to_list())))) for v in ds)
                require(row[0]==K.one and all(row[i]*row[j]==sum((K(R[i][j][k])*row[k] for k in range(n)),K.zero)
                                               for i in range(n) for j in range(n)), 'exact multiplicative character')
                self.rows.append(row)
                self.codegrees.append(sum((row[i]*row[a.du[i]] for i in range(n)),K.zero))
        require(len(self.rows)==n and len(set(self.rows))==n, 'complete distinct character table')
        self.ds=[K.from_sympy(v+w*s.sqrt(radicand)) for v,w in dimensions]
        self.D=sum((d*d for d in self.ds),K.zero)
        self.fp=next((i for i,row in enumerate(self.rows) if list(row)==self.ds),None)
        require(self.fp is not None,'positive character in complete table')
        for i,row in enumerate(self.rows):
            for j,other in enumerate(self.rows):
                require(sum((row[k]*other[a.du[k]] for k in range(n)),K.zero)==(self.codegrees[i] if i==j else K.zero), 'character orthogonality')
        self.dims={};self.values={};self.allowed={};self.compatibility={}
