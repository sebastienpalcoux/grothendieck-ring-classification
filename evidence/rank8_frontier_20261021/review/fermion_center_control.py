#!/usr/bin/env python3
"""Actual Z(Ising) control for charge-aware fermionic pairing and G-row equations."""
from pathlib import Path
import argparse,hashlib,itertools,json
import sympy as s
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)

def compute():
    K=s.QQ.algebraic_field(s.exp(s.pi*s.I/8));u=K.from_sympy(s.exp(s.pi*s.I/8));r=u**2-u**6
    need(r*r==K(2)and u**8==-K.one,'exact Ising field')
    R=[[[1,0,0],[0,1,0],[0,0,1]],[[0,1,0],[1,0,1],[0,1,0]],[[0,0,1],[0,1,0],[1,0,0]]]
    dims=[K.one,r,K.one];S0=[[K.one,r,K.one],[r,K.zero,-r],[K.one,-r,K.one]];T0=[K.one,u,-K.one]
    labels=list(itertools.product(range(3),repeat=2));distinguished=[(0,0),(2,2),(1,1)];g=(2,0);gi=labels.index(g);D=K(4)
    S=[[S0[a][c]*S0[b][d]for c,d in labels]for a,b in labels];theta=[T0[a]/T0[b]for a,b in labels];ds=[dims[a]*dims[b]for a,b in labels]
    chi=[[K.one,r,K.one],[K.one,-r,K.one],[K.one,K.zero,-K.one]];beta=[K.one,K.one,K(2)]
    restrictions=[R[a][b]for a,b in labels]
    need(theta[gi]==-K.one,'actual central fermion')
    charges=[S[gi][z]/ds[z]for z in range(9)];need(all(m in(K.one,-K.one)for m in charges),'actual monodromy charges')
    permutation=[labels.index((2-a if a!=1 else 1,b))for a,b in labels]
    fixed=[];opposite=[];same=[]
    for z,w in enumerate(permutation):
        need(permutation[w]==z,'central fermion involution')
        need(theta[w]==-charges[z]*theta[z],'fermion balancing')
        if w==z:need(charges[z]==-K.one,'only negative-charge objects may be fixed');fixed.append(z)
        elif z<w:
            if charges[z]==K.one:need(theta[w]==-theta[z],'positive-charge opposite pair');opposite.append([z,w])
            else:need(theta[w]==theta[z],'negative-charge equal-twist pair');same.append([z,w])
    need(len(fixed)==3 and len(opposite)==3,'actual center tests fixed negative charges and opposite pairs')
    for E,A in enumerate(distinguished):
        ei=labels.index(A)
        values=[sum((K(x)*y for x,y in zip(v,chi[E])),K.zero)for v in restrictions]
        need(all(S[ei][z]==beta[E]*values[z]for z in range(9)),'distinguished partial-S normalization')
        need(sum((charges[z]*ds[z]*values[z]for z in range(9)),K.zero)==K.zero,'G-row orthogonality')
        need(sum((theta[z]*charges[z]*ds[z]*values[z]for z in range(9)),K.zero)==-D*chi[E][2],'G-row STS right-hand side and normalization')
    # Check the full modular identities, independently of the specialized rows.
    for a,b in itertools.product(range(9),repeat=2):
        need(sum((S[a][z]*S[z][b]for z in range(9)),K.zero)==(D*D if a==b else K.zero),'actual full S-square')
        need(sum((S[a][z]*theta[z]*S[z][b]for z in range(9)),K.zero)==D*S[a][b]/theta[a]/theta[b],'actual full center STS')
    return {'kind':'actual_center_fermion_charge_and_pair_control','model':'Z(Ising)=Ising tensor Ising_reverse','center_rank':9,
        'source_global_dimension':4,'central_fermion':[2,0],'distinguished_labels':distinguished,
        'negative_charge_fixed_objects':[labels[z]for z in fixed],
        'positive_charge_opposite_twist_pairs':[[labels[z],labels[w]]for z,w in opposite],
        'negative_charge_equal_twist_pairs':same,'all_full_S_square_and_STS_entries':81,
        'all_distinguished_G_orthogonality_and_STS_rows':3,
        'scope':'positive normalization/control for charge-aware necessary systems; no R941 existence claim',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();actual=json.loads(json.dumps(compute()));path=HERE/'fermion_center_control.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'fermion center control receipt differs')
    print('PASS actual Z(Ising) fermion: fixed negative-charge simples, opposite pairs, full modular identities and G rows')
