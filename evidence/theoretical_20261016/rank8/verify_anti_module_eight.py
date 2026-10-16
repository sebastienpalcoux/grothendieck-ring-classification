"""Source-bound arithmetic for eight short anti-invariant-module proofs.

This does not enumerate matrix candidates. It verifies the exact source
relations and the spectral/norm arithmetic used in the written proof.
"""
import argparse,gzip,hashlib,json,itertools
from pathlib import Path
import sympy as s

def need(value,message):
    if not value: raise ValueError(message)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
    root=parser.parse_args().repo.resolve()
    flat=lambda R:tuple(v for M in R for row in M for v in row)
    tensors=[json.loads(line.replace('{','[').replace('}',']')) for line in gzip.open(root/'supplements/rank8/data/rank8_tables.txt.gz','rt')]
    tensors=sorted((R for R in tensors if max(flat(R))==2),key=flat)
    ledger={r['id']:r for r in json.loads((root/'supplements/rank8/data/decisions.json').read_text())}
    A=[[1,0,1,1],[0,1,1,1],[1,1,0,1],[1,1,1,2]]
    B=[[0,1,1,1],[1,1,0,1],[1,0,1,1],[1,1,1,2]]
    C=[[0,1,1,1],[1,0,1,1],[1,1,2,1],[1,1,1,2]]
    # index, involution, fixed labels, generator, bound type, root type
    specs=[(318,4,[1,2,3,7],5,'A','small'),(319,4,[1,2,3,7],5,'A','unit'),
           (320,6,[1,2,5,7],3,'A','imag'),(368,3,[4,5,6,7],1,'C','imag'),
           (370,3,[4,5,6,7],1,'B','imag'),(735,1,[4,5,6,7],2,'B','small'),
           (758,1,[4,5,6,7],2,'C','unit'),(760,1,[4,5,6,7],2,'B','unit')]
    z=s.Symbol('z');result=[]
    for index,g,fixed,x,kind,roots in specs:
        rid=f'R8_2_{index}';R=tensors[index-1]
        sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
        need(sha==ledger[rid]['tensor_sha256'],'source tensor '+rid)
        need(R[g][g]==[1]+[0]*7,'order two '+rid)
        need(all(sum(R[i][g])==1 for i in range(8)),'right invertible '+rid)
        need([i for i in range(8) if R[i][g][i]]==fixed,'right fixed labels '+rid)
        dual=next(j for j in range(8) if R[x][j][0])
        need(R[x][dual]==R[dual][x],'normal generator '+rid)
        bound=[[R[x][a][b] for b in fixed] for a in fixed]
        need(bound=={'A':A,'B':B,'C':C}[kind],'restricted fusion bound '+rid)
        large=z*z-6*z+(-1 if kind=='C' else 1)
        polynomial=(z*z-1)*large
        if roots=='small':polynomial*=z*z+2*z-1
        if roots=='imag':polynomial*=z*z+1
        polynomial=s.Poly(polynomial,z)
        N=s.Matrix(R[x]);evaluation=s.zeros(8)
        for c in polynomial.all_coeffs():evaluation=evaluation*N+c*s.eye(8)
        need(evaluation==s.zeros(8),'annihilator '+rid)
        need(s.Poly(large,z).is_irreducible,'large pair rational conjugacy')
        minimum=sum(v%2 for row in bound for v in row)
        maximum=sum(v*v for row in bound for v in row)
        need(minimum==12 and maximum==(20 if kind=='C' else 16),'norm interval')
        large_cost=36-2*s.Poly(large,z).nth(0)
        need(large_cost>maximum,'large conjugate pair exclusion')
        if roots!='small':
            need(4<minimum,'unit-modulus contradiction')
            reason='All remaining eigenvalues have modulus one, so squared Frobenius norm is 4, below 12.'
        else:
            small=s.Poly(z*z+2*z-1,z)
            need(small.is_irreducible,'small pair rational conjugacy')
            small_cost=4-2*small.nth(0)
            options=[(pairs,(4-2*pairs)+small_cost*pairs) for pairs in range(3)]
            viable=[pairs for pairs,norm in options if minimum<=norm<=maximum]
            need(viable==[2],'two copies forced')
            trace=2*(-2)
            even_diagonals=[i for i in range(4) if bound[i][i]==2]
            need(even_diagonals==[3] and sum(bound[i][i]%2 for i in range(4))==2,'trace bound')
            need(abs(trace)>2,'trace contradiction')
            reason='Norm 12 forces two small quadratic pairs and trace -4; entry parity instead bounds the trace in [-2,2].'
        result.append({'id':rid,'tensor_sha256':sha,'involution':g,'right_fixed_labels':fixed,
                       'generator':x,'dual_generator':dual,'restricted_bound':bound,
                       'annihilator_coefficients':[int(v) for v in polynomial.all_coeffs()],
                       'annihilator_factorization':str(s.factor(polynomial.as_expr())),
                       'squared_Frobenius_norm_interval':[minimum,maximum],
                       'large_quadratic_pair_cost':int(large_cost),'contradiction':reason})
    print(json.dumps({'status':'PASS','criterion':'involution_anti_module_spectral',
                      'categorical_scope':'general complex fusion category',
                      'proof':'evidence/theoretical_20261016/rank8/ANTI_MODULE_EIGHT_GENERAL_PROOF.md',
                      'cases':result},indent=2))

if __name__=='__main__':main()
