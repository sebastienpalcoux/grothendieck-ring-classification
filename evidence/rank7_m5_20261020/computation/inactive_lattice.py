"""Exact inactive-variable lattice quotient tests for finite active counts.

Discovery may compute an integer Hermite basis.  Replay only requires that
every inactive column is contained in the recorded echelon lattice.  This
one-sided containment suffices for exclusions; the HNF routine is not trusted.
"""
from fractions import Fraction as Q
import hashlib,json,math


def require(value,message):
    if not value:raise ValueError(message)


class EchelonLattice:
    def __init__(self,basis,width=None):
        self.basis=[list(row) for row in basis]
        self.width=width if width is not None else len(basis[0])
        self.pivots=[]
        for row in self.basis:
            require(len(row)==self.width and all(type(x) is int for x in row),'integer lattice row')
            pivot=next((i for i,x in enumerate(row) if x),None)
            require(pivot is not None and row[pivot]>0,'positive echelon pivot')
            require(not self.pivots or pivot>self.pivots[-1],'strictly increasing pivots')
            self.pivots.append(pivot)
        self.support=[[(i,x) for i,x in enumerate(row) if x] for row in self.basis]

    def coordinates(self,vector):
        require(len(vector)==self.width,'lattice vector width')
        rest=list(map(Q,vector));coordinates=[]
        for row,pivot,support in zip(self.basis,self.pivots,self.support):
            c=rest[pivot]/row[pivot];coordinates.append(c)
            if c:
                for i,x in support:rest[i]-=c*x
        return coordinates,rest

    def contains(self,vector):
        if all(type(x) is int for x in vector):
            rest=vector[:]
            for row,pivot,support in zip(self.basis,self.pivots,self.support):
                if rest[pivot]%row[pivot]:return False
                c=rest[pivot]//row[pivot]
                if c:
                    for i,x in support:rest[i]-=c*x
            return not any(rest)
        coordinates,rest=self.coordinates(vector)
        return not any(rest) and all(x.denominator==1 for x in coordinates)

    def require_contains_generators(self,columns):
        for j,col in enumerate(columns):require(self.contains(col),'inactive generator outside recorded lattice: '+str(j))


def hermite_basis(columns,width=None):
    """Discovery helper. No native normal-form algorithm is needed in replay."""
    if not columns:return []
    from flint import fmpz_mat
    matrix=fmpz_mat(columns).hnf()
    return [row for i in range(matrix.nrows()) if any(row:=[int(matrix[i,j]) for j in range(matrix.ncols())])]


def prepare(inactive_columns,rhs,active_columns,basis=None):
    """Return exact integer modular/equality tests on active multiplicities.

    A test has constant - coefficients*counts == 0, either in Z (modulus 0)
    or modulo its positive modulus.  Every possible completion by integer
    inactive counts necessarily passes all tests; signs are unrestricted.
    """
    if basis is None:basis=hermite_basis(inactive_columns,len(rhs))
    lattice=EchelonLattice(basis,len(rhs))
    lattice.require_contains_generators(inactive_columns)
    coordinates=[lattice.coordinates(v) for v in [rhs]+active_columns]
    tests=[]
    def add(values,modular):
        denominator=math.lcm(*(v.denominator for v in values))
        integers=[int(v*denominator) for v in values]
        modulus=denominator if modular else 0
        divisor=math.gcd(modulus,*integers) or 1
        modulus//=divisor;integers=[x//divisor for x in integers]
        if modulus==1 or not any(integers):return
        if modulus:
            integers=[x%modulus for x in integers]
            if not any(integers):return
        tests.append({'constant':integers[0],'coefficients':integers[1:],'modulus':modulus})
    for i in range(len(basis)):add([c[i] for c,r in coordinates],True)
    for i in range(len(rhs)):add([r[i] for c,r in coordinates],False)
    unique={json.dumps(test,sort_keys=True):test for test in tests}
    tests=list(unique.values())
    return {'basis':basis,'width':len(rhs),'active_count':len(active_columns),
            'inactive_count':len(inactive_columns),'tests':tests,
            'system_sha256':hashlib.sha256(json.dumps([inactive_columns,rhs,active_columns],separators=(',',':')).encode()).hexdigest()}


def check_counts(prepared,counts,return_failure=False):
    require(len(counts)==prepared['active_count'] and all(type(x) is int for x in counts),'integer active count vector')
    for j,test in enumerate(prepared['tests']):
        value=test['constant']-sum(a*b for a,b in zip(test['coefficients'],counts))
        residue=value%test['modulus'] if test['modulus'] else value
        if residue:return (False,{'test':j,'residue':residue}) if return_failure else False
    return (True,None) if return_failure else True


def verify_prepared(record,inactive_columns,rhs,active_columns):
    expected=prepare(inactive_columns,rhs,active_columns,basis=record['basis'])
    require(record==expected,'recorded lattice quotient differs from exact reconstruction')
    return expected


def controls():
    import itertools
    cases=[([[2,1,0],[0,3,0]],[1,0,1],[[1,0,0],[0,0,1]]),
           ([[2,1],[0,3]],[1,2],[[1,0],[0,1]]),
           ([],[1,0],[[1,0],[0,1]])]
    checked=0
    for inactive,rhs,active in cases:
        prepared=prepare(inactive,rhs,active)
        replay=verify_prepared(prepared,inactive,rhs,active)
        lattice=EchelonLattice(replay['basis'],len(rhs))
        for counts in itertools.product(range(-3,4),repeat=len(active)):
            residual=[rhs[j]-sum(v[j]*c for v,c in zip(active,counts)) for j in range(len(rhs))]
            require(check_counts(replay,list(counts))==lattice.contains(residual),'quotient/direct reduction disagreement')
            checked+=1
    print(json.dumps({'status':'PASS','optimized_python':not __debug__,'finite_count_controls':checked}))


if __name__=='__main__':controls()
