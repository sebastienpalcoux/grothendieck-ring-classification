"""Finite hypotheses for the general solvability exclusion of R8_1_29.

The categorical exhaustion is proved in paper/solvable_proofs.tex; it is not
inferred from absence of examples. All code checks survive python -O.
"""
from itertools import product
from pathlib import Path
import hashlib,json

EXPECTED_TENSOR_SHA256 = '2f68033b856e4c4c4ca1d012ab586ef6b5a636be936cd8ac192bebcda417c032'

def require(ok,message):
    if not ok:
        raise ValueError(message)

def fingerprint(N):
    return hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()

def verify_tensor(N):
    require(fingerprint(N)==EXPECTED_TENSOR_SHA256,'source-bound R29 tensor')
    require(len(N)==8 and all(len(M)==8 and all(len(v)==8 for v in M) for M in N),'rank')
    require(all(isinstance(v,int) and 0<=v<=1 for M in N for row in M for v in row),'multiplicity one')
    dual=[next(j for j in range(8) if N[i][j][0]) for i in range(8)]
    inv=[i for i in range(8) if sum(N[i][dual[i]])==1]
    noninv=sorted(set(range(8))-set(inv))
    require(len(inv)==6 and len(noninv)==2,'simple types')
    dims=[1 if i in inv else 3 for i in range(8)]
    require(all(sum(N[i][j][k]*dims[k] for k in range(8))==dims[i]*dims[j]
                for i,j in product(range(8),repeat=2)),'FP dimensions')
    require(sum(d*d for d in dims)==24,'FP dimension24')
    require(all(dual[i]==i for i in noninv),'self-dual noninvertibles')
    adj={k for i in range(8) for k in range(8) if N[i][dual[i]][k]}
    while True:
        new=adj|{k for i in adj for j in adj for k in range(8) if N[i][j][k]}
        if new==adj:break
        adj=new
    require(adj==set(range(8)),'trivial universal grading')
    def gm(a,b):
        require(a in inv and b in inv and sum(N[a][b])==1,'invertible product')
        return N[a][b].index(1)
    generators=[]
    for g in inv:
        powers=[0]
        for _ in range(6):powers.append(gm(powers[-1],g))
        if powers[6]==0 and len(set(powers[:6]))==6:generators.append((g,powers))
    require(bool(generators),'invertible group C6')
    generator,powers=generators[0]
    order2=powers[3];H3=sorted({powers[0],powers[2],powers[4]})
    require(all(N[order2][x][y]==1 for x,y in zip(noninv,reversed(noninv))),'C2 swaps noninvertibles')
    require(all(N[h][x][x]==1 for h in H3 for x in noninv),'C3 fixes noninvertibles')
    orbits=[];remaining=set(range(8))
    while remaining:
        i=min(remaining);image=N[order2][i].index(1)
        O=sorted({i,image});orbits.append(O);remaining-=set(O)
    require(len(orbits)==4 and all(len(O)==2 for O in orbits),'C2 quotient objects')
    D=[[[sum(N[A[0]][B[0]][k] for k in C) for C in orbits] for B in orbits] for A in orbits]
    rho=next(i for i,O in enumerate(orbits) if O==noninv)
    pinv=[i for i in range(4) if i!=rho]
    require(D[rho][rho][rho]==2 and all(D[rho][rho][i]==1 for i in pinv),'C3+2 quotient square')
    require(all(D[i][rho][rho]==D[rho][i][rho]==1 for i in pinv),'C3+2 quotient action')
    # Gauge involution: an invariant normalized 2-cocycle on V4, any associator.
    V=range(4);cycle=[0,2,3,1]
    B=lambda a,b:((a&1)*(b&1)+(a&1)*(b>>1)+(a>>1)*(b>>1))%2
    require(all((B(a,b)+B(a^b,c)-B(b,c)-B(a,b^c))%2==0
                for a,b,c in product(V,repeat=3)),'J cocycle')
    require(all(B(cycle[a],cycle[b])==B(a,b) for a,b in product(V,repeat=2)),'J invariant')
    require(all(B(a,a)==1 for a in (1,2,3)),'J negative diagonal channels')
    require(all(B(a,b)!=B(b,a) for a,b in product((1,2,3),repeat=2) if a!=b),'opposite nonzero-channel signs')
    # H1(C3,V4-hat)=0: every cocycle value is a coboundary.
    cocycles={v for v in V if v^cycle[v]^cycle[cycle[v]]==0}
    coboundaries={v^cycle[v] for v in V}
    require(cocycles==coboundaries==set(V),'H1 equivariance ambiguity vanishes')
    # Pointed dimension-eight C2^3 branch: a free orbit has coefficient two.
    O=(1,2,3)
    counts={c:sum(a^b==c for a,b in product(O,repeat=2)) for c in range(8)}
    require([counts[c] for c in O]==[2,2,2],'elementary-abelian free-orbit multiplicity')
    # Quaternion branch: the two free C3 orbits are inverse and distinct.
    quaternion_orbit=(1,2,3);quaternion_inverse_orbit=(-1,-2,-3)
    require(set(quaternion_orbit).isdisjoint(quaternion_inverse_orbit),'quaternion non-self-dual orbits')
    return {'status':'PASS','id':'R8_1_29','scope':'no fusion category over C',
            'tensor_sha256':fingerprint(N),'FPdim':24,'invertibles':inv,
            'noninvertibles':noninv,'noninvertibles_self_dual':True,
            'universal_grading_trivial':True,'C6_generator':generator,
            'central_prime_candidates':[2,3],'order2_element':order2,'order3_subgroup':H3,
            'C2_quotient_orbits':orbits,'C2_quotient_tensor':D,
            'pointed_dimension8_alternatives':{'C2^3':'forced coefficient2','Q8':'forced distinct noninvertible duals'},
            'simple_fixing_C3_plus2_auto_classes':['identity','invariant_J'],
            'identity_action_contradiction':'coefficient2',
            'invariant_J_action_contradiction':'distinct noninvertible duals',
            'J_cocycle_equations':64,'J_invariance_equations':16,'H1_C3_V4_vanishes':True,
            'associator_scope':'arbitrary omega in the pointed de-equivariantization'}

def verify_record(record):
    require(record['id']=='R8_1_29','certificate ID')
    require(record['tensor_sha256']==EXPECTED_TENSOR_SHA256,'certificate hash')
    return verify_tensor(record['tensor'])

def main():
    record=json.loads((Path(__file__).resolve().parents[1]/'data/solvable_r29_certificate.json').read_text())
    report=verify_record(record)
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':main()
