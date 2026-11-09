#!/usr/bin/env python3
"""Positive and adversarial certificate regressions; safe under Python -O.

Production rejections must raise the verifier's explicit VerificationError
rather than merely crash; independent-checker RuntimeErrors are checked
separately. Fixtures and mutations do not modify the release ledger.
"""
import argparse
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys
import time
from unittest.mock import patch
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'classification/software'))
from exact import VerificationError, require
from spherical import (check_sphere, sphere_certificate, cyclotomic_failure,
                       check_cyclotomic, check_nonabelian_factor)
from induction import (algebraic_floor, fourth_indicator_bound, fourth_indicator_gap,
                       check_low_witness, low_data, row_gap)
from rings import Characters
from exact import ec, pc, poly, t as field_t
import sympy as s
import rings
import rapid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'tests/results.json')
    args = parser.parse_args()
    started = time.monotonic()
    rows = [json.loads(line) for line in (ROOT/'census/data/rings.jsonl').read_text().splitlines()]
    records = [json.loads(line) for line in (ROOT/'classification/results/certificates.jsonl').read_text().splitlines()]
    models = json.loads((ROOT/'classification/models.json').read_text())
    pairs = list(zip(rows, records))
    results = []

    # This actual fusion ring has two factors giving valid d-number
    # obstructions. Reversing factor discovery order must not change the
    # chosen certificate, with or without optional FLINT acceleration.
    witness_ring = rings.sd_tensor((0,1,6,4,8,2,8,12,7,16))
    factors = list(rings.codegree_factors(witness_ring))
    expected = rings.dnumber(witness_ring)
    require(expected is not None and len(factors)==2, 'd-number order fixture changed')
    for factor_order in (factors, list(reversed(factors))):
        with patch.object(rings, 'codegree_factors', return_value=factor_order):
            require(rings.dnumber(witness_ring)==expected, 'SymPy factor order changes witness')
    if rapid.fmpz_mat is not None:
        unit, factors = rapid.casimir_polynomial(witness_ring).factor()
        class FactoredPolynomial:
            def __init__(self, ordered): self.ordered = ordered
            def factor(self): return unit, self.ordered
        for factor_order in (factors, list(reversed(factors))):
            with patch.object(rapid, 'casimir_polynomial', return_value=FactoredPolynomial(factor_order)):
                require(rapid.dnumber(witness_ring)==expected, 'FLINT factor order changes witness')
    require(rapid.dnumber(witness_ring)==expected, 'backends choose different d-number witnesses')
    results.append({'test':'d-number witness invariant under factor order', 'passed':True})

    def rejects(name, fn, required_message=None):
        try:
            fn()
        except VerificationError as exc:
            message = str(exc)
            require(required_message is None or required_message in message,
                    f'{name}: rejected for unexpected reason: {message}')
            results.append({'test': name, 'passed': True, 'rejection': message})
        else:
            raise RuntimeError(f'{name}: an invalid certificate was accepted')

    rep = next(model['matrices'] for model in models if model['model']=='Rep_A4')
    require(sphere_certificate(rep) is None, 'Rep(A4) positive control failed')
    results.append({'test':'Rep(A4) positive control', 'passed':True})
    forged = json.loads((ROOT/'tests/fixtures/rep_a4_false_exclusion.json').read_text())
    rejects('Rep(A4) null-obstruction exclusion', lambda: check_sphere(rep, forged),
            'low obstruction not verified')

    row, rec = next((r,c) for r,c in pairs if c['stage']=='central_induction'
                    and (c['certificate'].get('pseudo') or {}).get('kind')=='induction'
                    and len(c['certificate']['pseudo']['failures'])>=2)
    tensor, proof = row['tensor'], rec['certificate']
    check_sphere(tensor, proof)
    results.append({'test':'valid multi-branch central certificate', 'passed':True, 'ring_id':row['id']})

    changed = deepcopy(proof); changed['characters'].pop()
    rejects('omitted character orbit', lambda: check_sphere(tensor, changed), 'missing character branches')
    changed = deepcopy(proof); changed['pseudo']['failures'].pop()
    rejects('omitted low-matrix branch', lambda: check_sphere(tensor, changed), 'missing low-matrix branches')
    changed = deepcopy(proof)
    changed['pseudo']['failures'][1] = deepcopy(changed['pseudo']['failures'][0])
    rejects('duplicated low-matrix branch', lambda: check_sphere(tensor, changed), 'wrong low rows')
    changed = deepcopy(proof); changed['pseudo']['failures'][0]['columns'][1][1] += 1
    rejects('incorrect induction row', lambda: check_sphere(tensor, changed), 'wrong low rows')
    changed = deepcopy(proof); changed['pseudo']['failures'][0]['obstruction'] = None
    rejects('null obstruction in a real exclusion', lambda: check_sphere(tensor, changed), 'low obstruction not verified')
    changed = deepcopy(proof); changed['pseudo']['roots'].pop()
    rejects('omitted formal-codegree root', lambda: check_sphere(tensor, changed), 'wrong or incomplete roots')

    row, rec = next((r,c) for r,c in pairs if any(
        b['obstruction'].get('kind')=='polynomial_row' for b in
        (c['certificate'].get('pseudo') or {}).get('failures',[])))
    changed = deepcopy(rec['certificate'])
    branch = next(b for b in changed['pseudo']['failures'] if b['obstruction'].get('kind')=='polynomial_row')
    branch['obstruction']['gap'] = ['0']
    rejects('false strict-sign witness', lambda: check_sphere(row['tensor'], changed), 'low obstruction not verified')

    row, rec = next((r,c) for r,c in pairs if any(
        b['obstruction'].get('kind')=='norm' for b in c['certificate'].get('characters',[])))
    changed = deepcopy(rec['certificate'])
    branch = next(b for b in changed['characters'] if b['obstruction'].get('kind')=='norm')
    branch['obstruction']['polynomial'] = ['1','0']
    rejects('unrelated norm polynomial', lambda: check_sphere(row['tensor'], changed), 'unrelated norm factor')
    changed = deepcopy(rec['certificate'])
    next(b for b in changed['characters'] if b['obstruction'].get('kind')=='norm')['obstruction']['prime']=4
    rejects('composite norm witness', lambda: check_sphere(row['tensor'], changed), 'nonprime witness')

    row, rec = next((r,c) for r,c in pairs if any(
        b['obstruction'].get('kind')=='spherical_first_moment' for b in c['certificate'].get('characters',[])))
    changed = deepcopy(rec['certificate'])
    branch = next(b for b in changed['characters'] if b['obstruction']['kind']=='spherical_first_moment')
    branch['obstruction']['gap'] = ['0']
    rejects('false first-moment gap', lambda: check_sphere(row['tensor'], changed),
            'spherical first-moment bound not violated')
    changed = deepcopy(rec['certificate'])
    branch = next(b for b in changed['characters'] if b['obstruction']['kind']=='spherical_first_moment')
    branch['obstruction']['embedding'] = 100
    rejects('nonexistent first-moment embedding', lambda: check_sphere(row['tensor'], changed),
            'invalid real embedding')

    # Real irreducible examples exercise every relevant abelian/nonabelian
    # Galois type in degrees three and four. Repeated factors and a product
    # of quadratic fields must also remain admissible.
    galois_controls = [
        ('cyclic cubic', field_t**3-3*field_t-1, True),
        ('nonabelian cubic', field_t**3-4*field_t+1, False),
        ('cyclic quartic', field_t**4-4*field_t**2+2, True),
        ('biquadratic quartic', field_t**4-10*field_t**2+1, True),
        ('dihedral quartic', field_t**4-5*field_t**2+2, False),
        ('symmetric quartic', field_t**4-5*field_t**2+field_t+1, False),
        ('two quadratic factors', (field_t**2-2)*(field_t**2-3), True),
        ('repeated quadratic factor', (field_t**2-2)**2, True),
    ]
    for name, expression, abelian in galois_controls:
        cp=s.Poly(expression,field_t,domain=s.QQ)
        fixture=SimpleNamespace(cp=cp,cf=cp.factor_list()[1])
        why=cyclotomic_failure(fixture)
        require((why is None)==abelian, 'wrong cyclotomic control: '+name)
        if why is not None:check_cyclotomic(fixture,why)
        results.append({'test':'exact cyclotomic control: '+name, 'passed':True})

    cyclo_row, cyclo_rec = next((r,c) for r,c in pairs if any(
        b['obstruction'].get('kind')=='nonabelian_codegrees'
        for b in c['certificate'].get('characters',[])))
    cyclo_tensor,cyclo_proof=cyclo_row['tensor'],cyclo_rec['certificate']
    cyclo_index=next(i for i,b in enumerate(cyclo_proof['characters'])
                     if b['obstruction']['kind']=='nonabelian_codegrees')
    check_sphere(cyclo_tensor,cyclo_proof)
    results.append({'test':'valid nonabelian-codegree exclusion', 'passed':True,
                    'ring_id':cyclo_row['id']})
    changed=deepcopy(cyclo_proof)
    changed['characters'][cyclo_index]['obstruction']['factor']=pc(
        s.Poly(field_t**3-4*field_t+1,field_t,domain=s.QQ))
    rejects('unrelated cyclotomic polynomial',
            lambda:check_sphere(cyclo_tensor,changed),'unrelated cyclotomic factor')
    a=Characters(cyclo_tensor,cyclo_proof['generator'])
    changed=deepcopy(cyclo_proof)
    changed['characters'][cyclo_index]['obstruction']['kind']='codegree_field'
    rejects('obsolete field-containment witness',
            lambda:check_sphere(cyclo_tensor,changed),'unknown spherical obstruction')
    for invalid_factor in (None, [], [True, '0', '0', '1']):
        why={'kind':'nonabelian_codegrees','factor':invalid_factor}
        rejects('malformed cyclotomic factor '+repr(invalid_factor),
                lambda:check_cyclotomic(a,why),'unrelated cyclotomic factor')

    # Membership in the Casimir polynomial is necessary but not sufficient:
    # an actual abelian quartic factor cannot certify an exclusion.
    normal=s.Poly(field_t**4-4*field_t**2+2,field_t,domain=s.QQ)
    rejects('false nonabelian claim for an abelian quartic',
            lambda:check_nonabelian_factor(normal,
                {'kind':'nonabelian_codegrees','factor':pc(normal)}),
            'codegree splitting field is abelian')
    rational=s.Poly(field_t-1,field_t,domain=s.QQ)
    rejects('degree-one cyclotomic exclusion',
            lambda:check_nonabelian_factor(rational,
                {'kind':'nonabelian_codegrees','factor':pc(rational)}),
            'cyclotomic factor degree is not three or four')
    model_a=Characters(rep)
    rejects('false nonabelian exclusion of Rep(A4)',
            lambda:check_cyclotomic(model_a,
                {'kind':'nonabelian_codegrees','factor':pc(model_a.cf[0][0])}),
            'cyclotomic factor degree is not three or four')

    # R_3 exercises the third-indicator row inequality even before a ledger
    # is regenerated. A supplied false gap must not become an exclusion.
    row=next(r for r in rows if r['id']==3047)
    proof=sphere_certificate(row['tensor'])
    require(proof is not None and proof.get('pseudo') is not None,
            'third-indicator fixture no longer excluded')
    branch=next(b for b in proof['pseudo']['failures']
                if b['obstruction']['kind']=='third_indicator_row')
    check_sphere(row['tensor'],proof)
    results.append({'test':'valid third-indicator certificate','passed':True,'ring_id':3047})
    changed=deepcopy(proof)
    next(b for b in changed['pseudo']['failures']
         if b['obstruction']['kind']=='third_indicator_row')['obstruction']['gap']=['0']
    rejects('false third-indicator gap',lambda:check_sphere(row['tensor'],changed),
            'low obstruction not verified')

    # R_2 must now be excluded by the general fourth-indicator inequality,
    # including all low choices, without relying on a regenerated ledger.
    r2_row=next(r for r in rows if r['id']==2463)
    r2_proof=sphere_certificate(r2_row['tensor'])
    require(r2_proof is not None and r2_proof.get('pseudo') is not None,
            'fourth-indicator fixture no longer excluded')
    failures=r2_proof['pseudo']['failures']
    require(len(failures)==4 and all(
        b['obstruction']['kind']=='fourth_indicator_row'
        and type(b['obstruction']['floor']) is int and b['obstruction']['floor']==16
        for b in failures),'R2 fourth-indicator branches or floors changed')
    require(sorted(b['obstruction']['gap'] for b in failures)==[['108'],['44'],['44'],['76']],
            'R2 fourth-indicator gaps changed')
    check_sphere(r2_row['tensor'],r2_proof)
    results.append({'test':'valid R2 fourth-indicator certificate','passed':True,
                    'ring_id':2463,'low_choices':len(failures)})
    r2_characters=Characters(r2_row['tensor'],r2_proof['generator'])
    f,K,ds,D,pD,emb=r2_characters.fp()
    for wrong_floor in (15,17):
        changed=deepcopy(r2_proof);branch=changed['pseudo']['failures'][0]
        why=branch['obstruction'];why['floor']=wrong_floor
        Q,W=low_data(branch['columns'],r2_characters.C,ds,K)
        # Even a gap consistent with the forged floor cannot certify it.
        why['gap']=ec(fourth_indicator_gap(why['object'],W,ds,D,K,wrong_floor))
        rejects(f'false fourth-indicator floor {wrong_floor}',
                lambda:check_sphere(r2_row['tensor'],changed),'incorrect fourth-indicator floor')
    for wrong_floor in (True,16.0,'16',None):
        changed=deepcopy(r2_proof);why=changed['pseudo']['failures'][0]['obstruction']
        if wrong_floor is None:why.pop('floor')
        else:why['floor']=wrong_floor
        rejects(f'invalid fourth-indicator floor {type(wrong_floor).__name__}',
                lambda:check_sphere(r2_row['tensor'],changed),'invalid fourth-indicator floor')
    changed=deepcopy(r2_proof)
    changed['pseudo']['failures'][0]['obstruction']['gap']=['0']
    rejects('false fourth-indicator gap',lambda:check_sphere(r2_row['tensor'],changed),
            'low obstruction not verified')

    # Actual pointed models give an exact integer boundary (an involution)
    # and a non-self-dual control. Tiny rational offsets detect rounding.
    for name,expected in [('Vec_C2xC2',9),('Vec_C4',1)]:
        tensor=next(model['matrices'] for model in models if model['model']==name)
        a=Characters(tensor);f,K,ds,D,pD,emb=a.fp()
        i=next(i for i in range(1,4) if (a.du[i]==i)==(name=='Vec_C2xC2'))
        bound=fourth_indicator_bound(i,ds,K,a.du,tensor)
        require(algebraic_floor(bound,K,emb)==expected,'wrong pointed-model fourth floor')
        if name=='Vec_C2xC2':
            require(bound==K(9),'involution floor is not an exact integer boundary')
            tiny=K.one/K(10**40)
            require(algebraic_floor(bound-tiny,K,emb)==8
                    and algebraic_floor(bound+tiny,K,emb)==9,
                    'algebraic floor rounded across an integer boundary')
    results.append({'test':'exact fourth-indicator floor boundaries','passed':True})

    # A checker must accept a valid supplied witness even if discovery chose another one.
    alternative_found=False
    for row,rec in pairs:
        if rec['stage']!='central_induction':continue
        proof=rec['certificate'];a=Characters(row['tensor'],proof['generator'])
        f,K,ds,D,pD,emb=a.fp()
        for bi,branch in enumerate(proof['pseudo']['failures']):
            Q,W=low_data(branch['columns'],a.C,ds,K)
            for i in range(1,4):
                gap=row_gap(i,W,ds,D,K,a.du)
                witness={'kind':'polynomial_row','object':i,'nonselfdual':a.du[i]!=i,'gap':ec(gap)}
                if emb.sign(gap)>0 and witness!=branch['obstruction']:
                    changed=deepcopy(proof);changed['pseudo']['failures'][bi]['obstruction']=witness
                    check_sphere(row['tensor'],changed)
                    results.append({'test':'valid non-first obstruction accepted','passed':True,'ring_id':row['id']})
                    alternative_found=True;break
            if alternative_found:break
        if alternative_found:break
    require(alternative_found,'no alternative witness found for acceptance regression')

    spec=importlib.util.spec_from_file_location('release_certificate_verifier',ROOT/'classification/verify.py')
    verifier=importlib.util.module_from_spec(spec);spec.loader.exec_module(verifier);verifier.initialize(models)
    row, rec = next((r,c) for r,c in pairs if c['stage']=='model')
    changed = deepcopy(rec)
    changed['certificate']['model'] = next(m['model'] for m in models if m['model']!=rec['certificate']['model'])
    rejects('wrong positive-model fusion-data identification', lambda: verifier.verify_record((row,changed)), 'model tensor mismatch')

    # The separate central implementation must not leave an FP-orbit claim unproved.
    spec=importlib.util.spec_from_file_location('independent_central',ROOT/'independent/independent_central_audit.py')
    independent=importlib.util.module_from_spec(spec);spec.loader.exec_module(independent)
    independent.verify((cyclo_row,cyclo_rec))
    results.append({'test':'independent nonabelian-codegree exclusion',
                    'passed':True,'ring_id':cyclo_row['id']})
    changed=deepcopy(cyclo_rec)
    changed['certificate']['characters'][cyclo_index]['obstruction']['factor']=pc(
        s.Poly(field_t**3-4*field_t+1,field_t,domain=s.QQ))
    for name,fn,message in [
        ('independent unrelated cyclotomic factor',
         lambda:independent.verify((cyclo_row,changed)),
         'unrelated nonabelian codegree factor'),
        ('independent false nonabelian quartic',
         lambda:independent.check_nonabelian_witness(independent.pol(pc(normal)),
             {'kind':'nonabelian_codegrees','factor':pc(normal)}),
         'codegree root field is normal, hence abelian'),
    ]:
        try:fn()
        except RuntimeError as exc:
            require(message in str(exc),'unexpected independent cyclotomic rejection')
            results.append({'test':name,'passed':True,'rejection':str(exc)})
        else:raise RuntimeError('independent checker accepted a forged cyclotomic certificate')
    r2_record={'id':r2_row['id'],'stage':'central_induction','certificate':r2_proof}
    counts=independent.verify((r2_row,r2_record))
    require(counts.get('low_fourth_indicator_row')==4,
            'independent checker missed R2 fourth-indicator branches')
    results.append({'test':'independent R2 fourth-indicator certificate','passed':True,'ring_id':2463})
    for field,value,message in [('floor',15,'incorrect fourth-indicator floor'),
                                ('floor',17,'incorrect fourth-indicator floor'),
                                ('floor',True,'invalid fourth-indicator floor'),
                                ('gap',['0'],'local inequality survives')]:
        changed=deepcopy(r2_record)
        changed['certificate']['pseudo']['failures'][0]['obstruction'][field]=value
        try:
            independent.verify((r2_row,changed))
        except RuntimeError as exc:
            require(message in str(exc),'unexpected independent fourth-indicator rejection')
            results.append({'test':f'independent false fourth-indicator {field} {value}',
                            'passed':True,'rejection':str(exc)})
        else:
            raise RuntimeError('independent checker accepted a forged fourth-indicator certificate')
    row, rec = next((r,c) for r,c in pairs if c['stage']=='central_induction' and any(
        b['obstruction'].get('kind')=='galois_global_dimension' for b in c['certificate']['characters']))
    changed=deepcopy(rec);changed['certificate']['pseudo']=None
    try:
        independent.verify((row,changed))
    except RuntimeError as exc:
        require('FP orbit has no exclusion proof' in str(exc), 'unexpected independent-check failure')
        results.append({'test':'independent checker missing FP proof','passed':True,'rejection':str(exc)})
    else:
        raise RuntimeError('independent checker accepted an unproved FP orbit')

    result={'all_checks_passed':True,'tests':len(results),'optimized_python':bool(sys.flags.optimize),
            'seconds':round(time.monotonic()-started,3),'results':results}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
