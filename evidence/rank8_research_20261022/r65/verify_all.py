"""Exact source/pointed/Fourier sanity checks and decisive separator replay."""
from pathlib import Path
from fractions import Fraction as Q
import argparse, hashlib, json, math, sys
import sympy as s
from pointed_phase_cone import HERE, st, require, verify


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def basic_checks():
    source=st.load_ring('R8_3_65');R=source['tensor'];n=8
    require(st.digest(R)==source['tensor_sha256'],'source tensor digest')
    dims=[(1,0) if j in (0,1,2,7) else (0,1) for j in range(n)]
    def mul(a,b): return (a[0]*b[0]+a[1]*b[1],
                          a[0]*b[1]+a[1]*b[0]+11*a[1]*b[1])
    for i in range(n):
        for j in range(n):
            require(mul(dims[i],dims[j])==tuple(sum(R[i][j][l]*dims[l][k]
                    for l in range(n)) for k in range(2)),'two FP dimensions')
    # Source fusion matrices have rows indexed by the right input.
    B=[[sum(R[a][i][l]*R[a][j][l] for a in range(n) for l in range(n))
        for j in range(n)] for i in range(n)]
    pointed=[0,1,7,2]
    require(all(B[i][j]==8*int(i==j) for i in pointed for j in pointed),
            'pointed induction supports are not disjoint')
    require(all(R[pointed[a]][pointed[b]][l]==int(l==pointed[(a+b)%4])
                for a in range(4) for b in range(4) for l in range(n)),
            'pointed C4 indexing differs')
    D=tuple(sum(mul(d,d)[k] for d in dims) for k in range(2))
    require(D==(8,44),'global dimension differs')
    # Explicit cocycle indicator product, represented by powers of i.
    indicators=[]
    for k in range(4):
        row={}
        for a,order in ((1,4),(3,4),(2,2)):
            exponent=sum(k*a*(((a*j)%4+a)//4) for j in range(1,order))%4
            row[str(a)]=exponent
            require(exponent==(k if a in (1,3) else 2*k)%4,'pointed indicator phase')
        indicators.append(row)
    F=s.Matrix([[s.I**(a*j) for a in range(4)] for j in range(4)])
    require(F.inv()*s.Matrix([1,0,0,0])==s.ones(4,1)/4,'Fourier fibre inversion')
    traces={}
    for order in (8,16):
        traces[str(order)]=[str(Q(int(s.mobius(order//math.gcd(order,p))),
                                     int(s.totient(order//math.gcd(order,p)))))
                            for p in range(1,5)]
    require(traces=={'8':['0','0','0','-1'],'16':['0','0','0','0']},
            'relative trace phases differ')
    return {'tensor_sha256':source['tensor_sha256'],
            'pointed_source_indices_in_group_order':pointed,
            'pointed_Gram_submatrix':[[B[i][j] for j in pointed] for i in pointed],
            'global_dimension_in_1_d':D,'fourier_fibre_mass_in_1_d':[2,11],
            'cyclic_indicators_as_powers_of_i':indicators,'relative_traces':traces}


def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    report=basic_checks()
    decisive=['pointed_phase_k0_fourier.json','pointed_phase_k1_fourier.json','pointed_phase_k2.json']
    for name in decisive: verify(HERE/name)
    root=HERE.parents[2]
    paths=[HERE/name for name in ['pointed_phase_cone.py','verify_all.py','PROOF.md']+decisive]
    # Pin every imported repository Python module, including the all-order
    # trace domain, exact matrix arithmetic, and old necessary filters.
    for module in list(sys.modules.values()):
        path=getattr(module,'__file__',None)
        if path:
            path=Path(path).resolve()
            if root in path.parents and path.suffix=='.py': paths.append(path)
    report.update(status='six_branches_covering_all_four_pointed_classes_verified_exactly',
                  previous_k0_subgroup_dual_proof_required=False,
                  sources={str(path.relative_to(root)):sha(path) for path in sorted(set(paths))})
    dest=HERE/'verification.json'
    encoded=st.encode(report)
    if args.write: dest.write_text(json.dumps(encoded,indent=2)+'\n')
    else: require(encoded==json.loads(dest.read_text()),'verification receipt differs')
    print('PASS R65 exact pointed-phase/Fourier exclusion, six branches/all four classes')


if __name__=='__main__': main()
