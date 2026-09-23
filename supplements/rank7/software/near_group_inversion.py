"""Fusion rules for inversion equivariantizations of odd near-group categories.

The generic function produces a based-ring candidate. Only the explicitly cited
C5+5 source is registered as a categorical realization. A based-ring symmetry
alone is never used as a substitute for a coherent tensor-category action.
"""
from pathlib import Path
import itertools,json
from exact import require
from rings import validate,permute

P=Path(__file__).resolve().parents[1]
REFERENCE=('M. Izumi, A Cuntz algebra approach to the classification of near-group '
           'categories, arXiv:1512.04288v2, Lemma 13.1, Example 13.8 and '
           'Theorems 13.17--13.18 (Section 13.3).')

def inversion_rules(n):
    require(isinstance(n,int) and not isinstance(n,bool) and n>0 and n%2==1,
            'the inversion rule parameter must be a positive odd integer')
    r=(n+7)//2;R=[[[0]*r for _ in range(r)] for _ in range(r)]
    def put(i,j,values):
        require(len(values)==r and all(isinstance(x,int) and x>=0 for x in values),'invalid product')
        R[i][j]=list(values);R[j][i]=list(values)
    def vector(*entries):
        v=[0]*r
        for k,c in entries:v[k]+=c
        return v
    def orbit(a):
        a%=n;a=min(a,(-a)%n)
        return vector((0,1),(1,1)) if not a else vector((3+a,1))
    for i in range(r):put(0,i,vector((i,1)))
    put(1,1,vector((0,1)));put(1,2,vector((3,1)));put(1,3,vector((2,1)))
    for j in range(4,r):put(1,j,vector((j,1)))
    for i in range(1,(n-1)//2+1):
        for j in range(i,(n-1)//2+1):
            put(3+i,3+j,[a+b for a,b in zip(orbit(i+j),orbit(i-j))])
        for a in (2,3):put(3+i,a,vector((2,1),(3,1)))
    x=vector((0,1),(2,(n+1)//2),(3,(n-1)//2),*((j,1) for j in range(4,r)))
    y=vector((1,1),(2,(n-1)//2),(3,(n+1)//2),*((j,1) for j in range(4,r)))
    put(2,2,x);put(3,3,x);put(2,3,y)
    validate(R)
    return R

def action_audit():
    n=5;theta=[(-i)%n for i in range(n)];a=[2*i*i%n for i in range(n)]
    # b_h for h != 0 is zeta_5^{exponent}/sqrt(5); b_0 is separately fixed.
    b=[None,4,1,1,4]
    require(all(theta[theta[i]]==i for i in range(n)),'not an involution')
    require(all(theta[(i+j)%n]==(theta[i]+theta[j])%n for i in range(n) for j in range(n)),'not a group automorphism')
    require(all((theta[i]*theta[j]-i*j)%n==0 for i in range(n) for j in range(n)),'bicharacter not preserved')
    require(all(a[theta[i]]==a[i] and b[theta[i]]==b[i] for i in range(n)),'source scalars not invariant')
    trace=sum(theta[i]==i for i in range(n));require(trace==1,'wrong trace on Hom(rho,rho^2)')
    return {'group_order':n,'permutation_S':theta,'permutation_T':theta,
            'fixed_unit_channel':0,'trace_on_noninvertible_multiplicity_space':trace,
            'positive_eigenspace_dimension':(n+trace)//2,'negative_eigenspace_dimension':(n-trace)//2,
            'quadratic_phase_exponents_mod_5':a,'nonzero_b_phase_exponents_mod_5':b,
            'dimension_polynomial':[1,-5,-5],'reference':REFERENCE,
            'scope':'The source supplies the C*-category and the coherent action; the finite check verifies its displayed permutation and scalar symmetries.'}

def models():
    audit=action_audit();return [{'name':'Inversion equivariantization of the Izumi C5+5 category',
        'N':inversion_rules(5),'reference':REFERENCE,'source_parameter':5,'action':audit,
        'proof':'Proposition near-group-inversion in the manuscript; source Theorems 13.17--13.18'}]

def build():
    rows=json.load(open(P/'data/census.json'));out=[]
    for model in models():
        matches=[]
        for r in rows:
            if r['m']!=max(x for v in model['N'] for w in v for x in w):continue
            for tail in itertools.permutations(range(1,6)):
                p=(0,)+tail
                if permute(model['N'],p)==r['N']:matches.append((r['id'],list(p)))
        require(matches and len({x[0] for x in matches})==1,'source model has no unique census class')
        rid,p=min(matches);out.append({**model,'id':rid,'basis_permutation':p})
    (P/'data/inversion_models.json').write_text(json.dumps(out,indent=2)+'\n');return out

def verify():
    rows={r['id']:r['N'] for r in json.load(open(P/'data/census.json'))};records=json.load(open(P/'data/inversion_models.json'));source=models()
    require(len(records)==len(source),'incomplete source registry')
    for rec,model in zip(records,source):
        require(all(rec[k]==v for k,v in model.items()),'altered inversion source record')
        p=rec['basis_permutation'];require(p[0]==0 and sorted(p)==list(range(6)),'invalid based permutation')
        require(permute(rec['N'],p)==rows[rec['id']],'inversion model does not match all structure constants')
    return {'models':len(records),'structure_constants_checked':216*len(records),'action_order':2}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--build',action='store_true');a=ap.parse_args()
    if a.build:build()
    print(json.dumps(verify(),indent=2))
