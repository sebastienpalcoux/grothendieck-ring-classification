#!/usr/bin/env python3
"""Independent actual-model fusion targets for the commutative integer system."""
from pathlib import Path
import argparse,hashlib,itertools,json,sys
import sympy as s
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=BASE.parents[1]
sys.path.insert(0,str(BASE/'quadratic'));sys.path.insert(0,str(BASE/'commutative_integer'))
from features import build,check_integer
from atomic_spectrum import AtomicSpectrum,table_for
from review_cm_real_sts import fib_group
from atomic_galois_balance import append_galois_balance,control as spectral_control
from fp_fusion_bounds import tighten_fusion_bounds
from galois_support_filter import filter_support
from verify_lattice import run as lattice_controls

def need(ok,msg):
    if not ok:raise ValueError(msg)

def compute():
    R=fib_group(True);C=AtomicSpectrum(R,4);T=table_for(R,C.a);K=T.K;S=build(C,T)
    saved=json.loads((BASE/'commutative_integer/control.json').read_text());values=saved['integer_witness']
    need(S.metadata==saved['metadata'],'known complete source-domain metadata');check_integer(S,values)
    ii=K.from_sympy(s.I);labels=[]
    for E,ch in enumerate(T.characters):
        e=0 if T.beta[E]==K.one else 1
        need(e==0 or T.beta[E]==(T.ds[4]**2),'actual distinguished Fibonacci dimension')
        js=[j for j in range(4)if ch[1]==ii**j];need(len(js)==1,'actual C4 charge label');labels.append((e,js[0]))
    need(len(set(labels))==8,'all actual distinguished model labels')
    def fib(a,b,c):return int(c in([0,1]if a==b==1 else[a+b]))
    checked=0
    for j,label in enumerate(S.column_labels):
        if label[0]!='fusion_coefficient':continue
        _,E,F,G=label;a,e=labels[E];b,f=labels[F];c,g=labels[G]
        target=fib(a,b,c)**2*int((e+f)%4==g)
        need(values[j]==target,'distinguished cubic agrees with actual center fusion tensor');checked+=1
    need(checked==196,'all intended cubic equations tested')
    # Independent actual 64-by64 fusion matrices, not a spectral polynomial
    # obtained from the proposed eigenvalues or their Galois orbits.
    actual_labels=list(itertools.product(range(2),range(2),range(4),range(4)))
    polynomials=[]
    for e,j in labels:
        matrix=s.Matrix([[fib(e,a,c)*fib(e,b,d)*int(h==z)*int((j+k)%4==w)
                          for c,d,z,w in actual_labels]for a,b,h,k in actual_labels])
        polynomials.append(list(map(int,matrix.charpoly().all_coeffs())))
    spectral=spectral_control()
    need(polynomials==spectral['all_eight_integer_characteristic_polynomials'],'all actual fusion matrix characteristic polynomials')
    balanced=append_galois_balance(S,C,T);check_integer(balanced,values)
    bounded=tighten_fusion_bounds(balanced,C,T);check_integer(bounded,values)
    filtered,report=filter_support(C,T);need(report['outcome']=='necessary_support_survives','actual center survives spectral support cuts')
    groups=C.meta['low_character_labels'];lowset={(groups[g],tuple(v))for g,v,z in filtered.low}
    highset={frozenset((0,)+tuple(C.a['high'][j][0])for j in orb)for orb in filtered.orbits}
    actual_count=1
    for value,label in zip(values,S.column_labels):
        if not value:continue
        if label[0]=='low':need((label[1],tuple(label[2]))in lowset,'actual low support retained');actual_count+=value
        elif label[0]=='high_orbit':need(frozenset(label[2])in highset,'actual high support retained');actual_count+=value*len(label[2])
    need(actual_count==64,'actual total center rank')
    controls=lattice_controls()
    paths=[Path(__file__)]+[BASE/'commutative_integer'/x for x in('features.py','bounds.py','equations.py','lattice.py','verify_control.py','verify_lattice.py','control.json','lattice_validation.json','PROOF.md','integer_central_cubic.tex')]
    paths +=[BASE/'quadratic'/x for x in('atomic_galois_balance.py','fp_fusion_bounds.py','galois_support_filter.py','atomic_galois_balance_results.json','fp_fusion_bounds_results.json','galois_support_control_results.json')]
    return {'kind':'independent_actual_commutative_integer_model_control','status':'PASS','actual_model':'Z(Fib tensor Vec(C4))',
        'actual_center_rank':actual_count,'actual_distinguished_labels':labels,'all_actual_distinguished_cubic_targets':checked,
        'all_eight_actual_fusion_matrix_characteristic_polynomials':polynomials,
        'exact_Galois_rows_satisfied':len(balanced.rhs)-len(S.rhs),'FP_tightened_bounds_preserve_actual_witness':True,
        'missing_conjugate_filter_preserves_every_actual_support':True,'lattice_box_and_compression_controls':controls,
        'scope':'the general necessary-system theorem and actual-model normalization are reviewed; target-specific outcomes require separate exact receipts',
        'files_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();actual=json.loads(json.dumps(compute()));path=HERE/'commutative_integer_control_review.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'independent integer-control receipt differs')
    print('PASS commutative integer theorem control:196 actual cubic targets,8 actual64x64characteristic polynomials,Galois/FP/support and1180exact controls')
