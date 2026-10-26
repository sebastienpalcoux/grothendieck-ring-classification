"""Short exact replay of the cubic-family exclusions. No search or network.

The categorical steps are proved in findings.md; this checks all their based-ring
premises and exact algebraic-number contradictions. Python 3.10+ and SymPy.
"""
from pathlib import Path
import hashlib, itertools, json
import sympy as s

ROOT = Path(__file__).resolve().parent
u, t = s.symbols('u t')

def require(test, message):
    if not test:
        raise ValueError(message)

def sha(R):
    return hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()

def product(R, i, j):
    row = R[i][j]
    require(sum(row) == 1, 'simple product')
    return row.index(1)

def polynomial(coeff):
    return s.Poly.from_list(list(map(s.Rational, coeff)), u).as_expr()

def quotient_norm(q, p):
    n = s.degree(p, u)
    M = s.Matrix.hstack(*[
        s.Matrix([s.Poly(s.rem(q*u**j, p, u), u).nth(k) for k in range(n)])
        for j in range(n)
    ])
    return s.factor(M.det()), M.charpoly(t).as_poly().monic()

def check_character(R, row):
    p = polynomial(row['field_polynomial'])
    require(s.Poly(p, u).is_irreducible, 'irreducible dimension field')
    ds = [polynomial(c) for c in row['dimensions_in_field']]
    interval = (s.Rational(18,10), s.Rational(181,100)) if row['family']=='cubic_C7' else (s.Rational(187,100), s.Rational(189,100))
    require(s.Poly(p,u).count_roots(*interval)==1, 'designated positive field embedding')
    # The dimensions here have nonnegative u/u^2 coefficient and their interval
    # minima are positive, so this uses no floating point sign decisions.
    for d in ds:
        P = s.Poly(d,u)
        require(P.degree() <= 2 and all(P.nth(k)>=0 for k in (1,2)), 'dimension shape')
        require(d.subs(u,interval[0])>0, 'positive dimension character')
    require(ds[0] == 1, 'unit dimension')
    for i,j in itertools.product(range(12),repeat=2):
        require(s.rem(ds[i]*ds[j]-sum(R[i][j][k]*ds[k]for k in range(12)),p,u)==0, 'exact dimension homomorphism')
    return p,ds

def verify_case(row, R, certificate):
    rid=row['id'];n=12
    require(sha(R)==row['tensor_sha256']==certificate['tensor_sha256'], 'source tensor binding '+rid)
    require(len(R)==n and all(len(A)==n and all(len(v)==n for v in A)for A in R), 'rank twelve')
    require(all(type(v)is int and v in (0,1) for A in R for z in A for v in z), 'multiplicity one')
    require(all(R[0][i][k]==R[i][0][k]==int(i==k)for i,k in itertools.product(range(n),repeat=2)), 'unit')
    dual=[next(j for j in range(n)if R[i][j][0])for i in range(n)]
    require(all(sum(R[i][j][0]for j in range(n))==1 and dual[dual[i]]==i for i in range(n)), 'unique involutive dual')
    p,ds=check_character(R,row)
    G=[i for i in range(n)if sum(R[i][dual[i]])==1]
    require(all(ds[g]==1 for g in G), 'pointed dimensions')
    if row['family']=='cubic_C7':
        x=certificate['X'];H=certificate['H'];b=u*u-1
        require(ds[x]==2*b, 'selected larger cubic dimension')
        require(H==[g for g in G if R[g][x][x]], 'full left stabilizer')
        require(len(H)==4 and all(product(R,g,h)in H for g,h in itertools.product(H,repeat=2)), 'order-four subgroup')
        require(all(R[x][h][x]for h in H), 'right stabilizer')
        require(R[x][dual[x]][x]==1, 'X occurs once in its dual product')
        norm,poly=quotient_norm(b/2,p)
        require(norm==s.Rational(-1,8), 'nonintegral norm')
        require(poly.as_expr()==t**3-t**2-t/4+s.Rational(1,8), 'exact monic quotient polynomial')
        return dict(id=rid,status='excluded',route='paired_nonlinear_stabilizer',norm=str(norm))
    require(row['family']=='cubic_C9', 'recognized family')
    X=1+2*u;Y=2*u*u-2
    require(len(G)==4 and sorted(str(d)for d in ds).count('1')==4,'four original invertibles')
    require(sum(d==2 for d in ds)==2 and sum(d==X for d in ds)==4 and sum(d==Y for d in ds)==2,'original C9 type')
    require(all(R[i][j]==R[j][i]for i,j in itertools.product(range(n),repeat=2)), 'commutative source ring')
    g,T,h=certificate['g'],certificate['T'],certificate['h']
    require(g in G and g!=0 and product(R,g,g)==0 and ds[T]==2,'C2 and dimension-two object')
    require(R[g][T][T]and R[T][g][T]and dual[T]==T,'near-group action')
    require(R[T][T]==[int(k in (0,g,T))for k in range(n)],'Rep(S3) rank-three rule')
    require(h in G and h not in (0,g)and product(R,product(R,h,g),dual[h])==g,'other invertible normalizes C2')
    integral=[i for i,d in enumerate(ds)if d in (1,2)]
    require(integral==certificate['integral_subring'],'integral subring binding')
    require(sum(ds[i]**2 for i in integral)==12,'dimension-twelve subcategory')
    require(all(not R[i][j][k] for i,j in itertools.product(integral,repeat=2)for k in range(n)if k not in integral),'closed integral subcategory')
    nonintegral=[i for i in range(n)if i not in integral]
    require(all(product(R,g,i)==product(R,i,g)!=i for i in nonintegral),'free paired C2 action on every cubic simple')
    # The rank-three Morita lemma proves the integral dual pointed of order12.
    # Free C2-orbits carry exactly two bimodule structures, preserving 4X+2Y.
    require(s.rem(Y*Y-(6+2*X+2*Y),p,u)==0,'dual-product dimension identity')
    require(s.Matrix([[s.Poly(v,u).nth(k)for v in (1,X,Y)]for k in range(3)]).det()!=0,'independent dimension basis')
    # Two Y labels force left and right actions through S2, with stabilizers6.
    require(6*6//12==3,'intersection subgroup has order divisible by three')
    for m in (1,2):
        norm,poly=quotient_norm(m*Y/3,p)
        require(norm==s.Rational(-8*m**3,9) and norm.q!=1,'nonintegral C3 bimodule dimension norm')
    return dict(id=rid,status='excluded',route='RepS3_Morita_then_paired_stabilizer',possible_multiplicities=[1,2],norms=['-8/9','-64/9'])

def main():
    rows=json.loads((ROOT/'input_families.json').read_text())
    data=json.loads((ROOT/'input_tensors.json').read_text())
    certs={r['id']:r for r in json.loads((ROOT/'results.json').read_text())['records']}
    require(len(rows)==20 and set(data)==set(certs)=={r['id']for r in rows},'all twenty source rings')
    checked=[verify_case(r,data[r['id']],certs[r['id']]['certificate'])for r in rows]
    result=dict(status='PASS',excluded=20,direct_C7=16,Morita_C9=4,records=checked,optimized_python=not __debug__)
    (ROOT/('verification_optimized.json'if not __debug__ else'verification.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='records'},indent=2))

if __name__=='__main__':main()
