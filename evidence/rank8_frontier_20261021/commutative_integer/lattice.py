"""Exact small-prime lattice consistency, with independently replayable separators.

The bit-plane elimination uses Python unbounded integers only. A negative
result is a covector checked against EVERY original integer column. Passing
this test establishes consistency modulo the stated prime, not Z-membership.
"""
from pathlib import Path
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from features import verify_modular
from exact import require


def modular(system,p):
    require(p in (2,3),'bit-plane solver supports primes 2 and 3')
    m=len(system.rhs);n=len(system.columns);width=n+1+m;size=(width+7)//8
    planes=[[bytearray(size)for _ in range(m)]for _ in range(p-1)]
    for j,col in enumerate(system.columns):
        byte=j>>3;bit=1<<(j&7)
        for i,value in enumerate(col):
            r=value%p
            if r:planes[r-1][i][byte]|=bit
    for i,b in enumerate(system.rhs):
        r=b%p
        if r:planes[r-1][i][n>>3]|=1<<(n&7)
        j=n+1+i;planes[0][i][j>>3]|=1<<(j&7)
    rows=[tuple(int.from_bytes(plane[i],'little')for plane in planes)for i in range(m)]
    del planes
    mask=(1<<n)-1;rhsbit=1<<n;basis={}
    def add3(x,y):
        a,b=x;c,d=y
        return ((c&~(a|b))|(a&~(c|d))|(b&d),
                (d&~(a|b))|(b&~(c|d))|(a&c))
    for i,row in enumerate(rows):
        while True:
            support=(row[0]if p==2 else row[0]|row[1])&mask
            if not support:break
            bit=support&-support;pivot=bit.bit_length()-1
            if pivot not in basis:
                if p==3 and row[1]&bit:row=(row[1],row[0])
                basis[pivot]=row;break
            old=basis[pivot]
            if p==2:row=(row[0]^old[0],)
            elif row[0]&bit:row=add3(row,(old[1],old[0]))
            else:row=add3(row,old)
        else:raise RuntimeError('unreachable')
        if not support:
            residue=next((r for r,plane in enumerate(row,1)if plane&rhsbit),0)
            if residue:
                covector=[next((r for r,plane in enumerate(row,1)if (plane>>(n+1+k))&1),0)for k in range(m)]
                certificate={'prime':p,'covector':covector,'rhs_residue':residue}
                verify_modular(system,certificate)
                return {'outcome':'modular_obstruction','prime':p,'rank':len(basis),'processed_rows':i+1,'certificate':certificate}
    # Exact row operations show consistency: zero A rows have zero b. The
    # deterministic rank receipt is replayed from the source-derived system.
    h=hashlib.sha256()
    for pivot,row in sorted(basis.items()):
        h.update(str(pivot).encode()+b':')
        for plane in row:h.update(plane.to_bytes(size,'little'))
    return {'outcome':'consistent_mod_prime','prime':p,'rank':len(basis),'rows':m,'columns':n,'echelon_sha256':h.hexdigest()}


def verify_result(system,result):
    if result['outcome']=='modular_obstruction':return verify_modular(system,result['certificate'])
    require(result==modular(system,result['prime']),'modular consistency receipt differs')
    return True


def verify_separator(system,certificate):
    """Verify a lattice obstruction directly, without trusting HNF discovery."""
    y=certificate['covector'];require(len(y)==len(system.rhs)and all(isinstance(x,int)for x in y),'invalid integral covector')
    b=sum(x*v for x,v in zip(y,system.rhs))
    if certificate['kind']=='rational_annihilator':
        require(all(sum(x*v for x,v in zip(y,col))==0 for col in system.columns),'covector does not annihilate original columns')
        require(b!=0 and b==certificate['rhs_value'],'rational annihilator misses rhs')
    else:
        require(certificate['kind']=='integral_modular_annihilator','unknown lattice separator')
        d=certificate['modulus'];require(isinstance(d,int)and d>1,'invalid lattice modulus')
        require(all(sum(x*v for x,v in zip(y,col))%d==0 for col in system.columns),'covector fails original-column congruence')
        require(b%d!=0 and b%d==certificate['rhs_residue'],'modular annihilator misses rhs')
    return True


def hermite(system,batch=64,progress=None):
    """Exact row-HNF of the column lattice, kept at its current rank.

    Nonmembership is returned ONLY with a full-original-column checked
    annihilator. Membership is a necessary lattice condition, not a
    nonnegative integer solution. No numerical optimizer is used.
    """
    import math
    from fractions import Fraction as Q
    from flint import fmpz_mat
    m=len(system.rhs);basis=[]
    for start in range(0,len(system.columns),batch):
        H=fmpz_mat(basis+list(system.columns[start:start+batch])).hnf()
        basis=[]
        for i in range(H.nrows()):
            row=tuple(int(H[i,j])for j in range(m))
            if any(row):basis.append(row)
        if progress:progress(min(start+batch,len(system.columns)),len(basis))
    pivots=[next(j for j,x in enumerate(row)if x)for row in basis]
    require(pivots==sorted(set(pivots))and all(row[p]>0 for row,p in zip(basis,pivots)),'HNF is not in row-echelon form')
    h=hashlib.sha256()
    for row in basis:h.update((repr(row)+'\n').encode())
    report={'rank':len(basis),'rows':m,'columns':len(system.columns),'row_Hermite_sha256':h.hexdigest()}
    remaining=list(system.rhs);coefficients=[]
    for k,(row,p)in enumerate(zip(basis,pivots)):
        value=Q(remaining[p],row[p])
        if value.denominator!=1:
            y=[Q(0)]*m;y[p]=Q(1,row[p])
            for i in range(k-1,-1,-1):
                q=pivots[i];y[q]=-sum((Q(basis[i][j])*y[j]for j in range(q+1,m)),Q(0))/basis[i][q]
            d=math.lcm(*(x.denominator for x in y));yy=[int(x*d)for x in y]
            cert={'kind':'integral_modular_annihilator','modulus':d,'covector':yy,'rhs_residue':sum(x*b for x,b in zip(yy,system.rhs))%d}
            verify_separator(system,cert)
            return {**report,'outcome':'integer_lattice_obstruction','certificate':cert}
        n=int(value);coefficients.append(n)
        if n:remaining=[x-n*v for x,v in zip(remaining,row)]
    if any(remaining):
        j=next(i for i,x in enumerate(remaining)if x);y=[Q(0)]*m;y[j]=Q(1)
        for i in range(len(basis)-1,-1,-1):
            p=pivots[i];y[p]=-sum((Q(basis[i][q])*y[q]for q in range(p+1,m)),Q(0))/basis[i][p]
        d=math.lcm(*(x.denominator for x in y));yy=[int(x*d)for x in y]
        cert={'kind':'rational_annihilator','covector':yy,'rhs_value':sum(x*b for x,b in zip(yy,system.rhs))}
        verify_separator(system,cert)
        return {**report,'outcome':'integer_lattice_obstruction','certificate':cert}
    require(all(sum(n*row[i]for n,row in zip(coefficients,basis))==system.rhs[i]for i in range(m)),'HNF lattice membership coefficients fail')
    return {**report,'outcome':'integer_lattice_member','Hermite_basis_coefficients':coefficients,
            'scope':'signed integer column-lattice membership only; nonnegative bounded integer feasibility remains separate'}


def verify_hermite(system,result):
    if result['outcome']=='integer_lattice_obstruction':return verify_separator(system,result['certificate'])
    require(result==hermite(system),'exact Hermite lattice receipt differs')
    return True
