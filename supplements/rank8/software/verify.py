"""Check every frozen rank-eight decision against its source tensor.

The source census is trusted for exhaustiveness.  This checker independently
validates its tensors and verifies every proposed categorification conclusion.
"""
import collections
import csv
import json
import subprocess
import sys
import importlib.util
from pathlib import Path


def _upper_verifier_root():
    """Find the complete current-stage verifier in a checkout or release ZIP."""
    here = Path(__file__).resolve().parent
    candidates = [here.parent / 'verification-repository']
    candidates.extend(p / 'verification-repository' for p in here.parents)
    candidates.extend(here.parents)
    for root in candidates:
        if ((root / 'tools/verify_upper_residual_20261002b.py').is_file()
                and (root / 'evidence/upper_residual_20261002b/decisions.json').is_file()):
            return root
    return None


# The previous entrypoint is retained unchanged in baseline_files for the
# isolated historical replay; a published release follows the latest stage.
if __name__ == '__main__' and (current_root := _upper_verifier_root()) is not None:
    spec = importlib.util.spec_from_file_location(
        'upper_residual_current', current_root / 'tools/verify_upper_residual_20261002b.py')
    current = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(current)
    current.main()
    raise SystemExit(0)

from analyze import (ROOT, read_source, mult, ckey, fp, dual, commutes,
                     rank2_certificate, near_group_certificate,
                     lower_subring_certificate, casimir_poly,
                     dnumber_certificate, noncomm_dnumber_certificate,
                     subring_dimension_certificate, primitive_certificate,
                     model_registry,rank7_negative_registry,
                     rank7_certified_subring_certificate,signed_witness_registry,
                     oriented_signed_certificate,integral_drinfeld_certificate,
                     published_negative_registry,published_appendix_certificate)
from exact import cyclotomic_failure, check_cyclotomic, t
from rings import matrices
import sympy as sy
import zero_spectrum
import involution_module
import field_automorphisms


def assert_fusion_tensor(R):
    n=len(R)
    assert n==8 and all(len(M)==n and all(len(row)==n for row in M) for M in R)
    assert all(type(a) is int and a>=0 for M in R for row in M for a in row)
    du=dual(R)
    assert all(du[du[i]]==i for i in range(n))
    for i in range(n):
        for j in range(n):
            assert R[0][i][j]==R[i][0][j]==int(i==j)
            assert R[i][j][0]==int(du[i]==j)
            for k in range(n):
                assert R[i][j][k]==R[du[i]][k][j]==R[k][du[j]][i]
    # The row-major convention reverses composition of left multiplication.
    for i in range(n):
        for j in range(n):
            for a in range(n):
                for b in range(n):
                    left=sum(R[i][a][k]*R[j][k][b] for k in range(n))
                    right=sum(R[j][i][k]*R[k][a][b] for k in range(n))
                    assert left==right


def verify_certificate(R,c,reg,rank7_negative,signed_witnesses,published_negative):
    kind=c['kind']
    if kind in ('graded_brauer_picard','graded_fiber_functor','solvable_equivariantization'):
        from oct2_extensions import verify_certificate as verify_graded
        verify_graded(R,c)
    elif kind=='near_group':
        assert near_group_certificate(R)==c
    elif kind=='rank_two':
        assert rank2_certificate(R)==c
    elif kind=='zero_spectrum':
        zero_spectrum.verify(R,c)
    elif kind=='lower_rank_subring':
        assert json.loads(json.dumps(lower_subring_certificate(R,reg)))==c
    elif kind=='rank7_certified_subring':
        assert rank7_certified_subring_certificate(R,rank7_negative)==c
    elif kind=='oriented_signed_sphericalization':
        assert commutes(R) and oriented_signed_certificate(R,signed_witnesses)==c
    elif kind=='integral_drinfeld':
        assert commutes(R) and integral_drinfeld_certificate(R)==c
    elif kind=='published_induction_exclusion':
        assert published_appendix_certificate(R,published_negative)==c
    elif kind in ('dnumber','rank8_noncomm_dnumber'):
        p=casimir_poly(R)
        if kind=='dnumber':
            assert commutes(R) and dnumber_certificate(p)==c
        else:
            assert not commutes(R) and noncomm_dnumber_certificate(R,p)==c
            # The nonlinear factor belongs only to the scalar summands:
            assert len(c['factor'])-1>=2
    elif kind=='involution_module':
        involution_module.verify(R,c)
    elif kind=='noncommuting_field_automorphisms':
        field_automorphisms.verify(R,c)
    elif kind=='subring_dimension':
        assert commutes(R) and json.loads(json.dumps(subring_dimension_certificate(R)))==c
    elif kind=='primitive_codegree':
        assert commutes(R) and primitive_certificate(casimir_poly(R))==c
    elif kind=='cyclotomic':
        assert commutes(R)
        check_cyclotomic([A.charpoly(t).as_poly() for A in matrices(R)],c)
    else:
        raise AssertionError('unknown certificate type '+str(kind))


def main():
    rr=read_source()
    grouped={m:sorted([R for R in rr if mult(R)==m],
                      key=lambda R:tuple(a for M in R for row in M for a in row)) for m in (1,2)}
    reg, models=model_registry()
    rank7_negative=rank7_negative_registry()
    signed_witnesses=signed_witness_registry()
    published_negative=published_negative_registry()
    proof_process=subprocess.run([sys.executable,str(ROOT/'experimental_signed/verify_imported.py')],
                                 check=True,text=True,capture_output=True,timeout=1800)
    assert 'ALL IMPORTED EXACT PROOF TREES CHECKED' in proof_process.stdout
    appendix_process=subprocess.run([sys.executable,str(ROOT/'experimental_signed/verify_appendix.py')],
                                    check=True,text=True,capture_output=True,timeout=120)
    assert 'checked_exact_full_tensor_transfers 6' in appendix_process.stdout
    decisions=json.loads((ROOT/'data/decisions.json').read_text())
    positive=json.loads((ROOT/'data/realized_models.json').read_text())
    counts=json.loads((ROOT/'data/classification_counts.json').read_text())
    assert len(decisions)==973 and len(positive)==len({z['id'] for z in positive})
    assert len({ckey(R) for R in rr})==973
    assert [len(grouped[m]) for m in (1,2)]==[96,877]
    positive_by_id={z['id']:z for z in positive}
    tally=collections.Counter()
    for i,z in enumerate(decisions):
        m,j=z['multiplicity'],z['index']
        assert z['id']==f'R8_{m}_{j}'
        R=grouped[m][j-1]
        assert_fusion_tensor(R)
        assert z['tensor_sha256']==fp(R) and z['commutative']==commutes(R)
        status=z['status']
        assert status in ('excluded','unitarily_realized','unresolved')
        if status=='excluded':
            assert z['id'] not in positive_by_id and 'models' not in z
            verify_certificate(R,z['certificate'],reg,rank7_negative,signed_witnesses,published_negative)
            tally[(m,'excluded',z['certificate']['kind'])]+=1
        elif status=='unitarily_realized':
            x=positive_by_id[z['id']]
            assert x['multiplicity']==m and x['tensor_sha256']==fp(R)
            assert x['tensor']==R and z['models']==[c['model'] for c in x['constructors']]
            for c in x['constructors']:
                assert c['reference'].strip() and ckey(c['tensor'])==ckey(R)
                p=c['basis_map_source_to_model']
                assert len(p)==8 and p[0]==0 and sorted(p)==list(range(8))
                assert all(R[a][b][h]==c['tensor'][p[a]][p[b]][p[h]]
                           for a in range(8) for b in range(8) for h in range(8))
            assert models.get(ckey(R)) or all(sum(R[a][b])==1 for a in range(8) for b in range(8))
            tally[(m,'realized','model')]+=1
        else:
            assert z['id'] not in positive_by_id and 'certificate' not in z and 'models' not in z
            tally[(m,'unresolved','none')]+=1
        if i%200==0:
            print('VERIFIED',i+1,'of',len(decisions),flush=True)
    assert len(positive_by_id)==sum(v for (m,s,k),v in tally.items() if s=='realized')
    for m,c in zip((1,2),counts):
        assert c['multiplicity']==m and c['fusion_rings']==len(grouped[m])
        assert c['excluded']==sum(v for (n,s,k),v in tally.items() if n==m and s=='excluded')
        assert c['realized']==tally[(m,'realized','model')]
        assert c['unresolved']==tally[(m,'unresolved','none')]
        assert c['fusion_rings']==c['excluded']+c['realized']+c['unresolved']
    stages=list(csv.DictReader((ROOT/'data/exclusion_stages.csv').open()))
    assert len(stages)%2==0
    for stage in {z['stage'] for z in stages}:
        for m in (1,2):
            row=next(z for z in stages if z['stage']==stage and int(z['multiplicity'])==m)
            linked_kind={'noncomm_dnumber':'rank8_noncomm_dnumber',
                         'field_automorphisms':'noncommuting_field_automorphisms',
                         'published_appendix_transfer':'published_induction_exclusion'}.get(stage,stage)
            expected=sum(v for (n,s,k),v in tally.items()
                         if n==m and s=='excluded' and linked_kind==k)
            assert int(row['new_exclusions'])==expected,(stage,m,expected)
    report={'census_size':len(decisions),'source_complete_through':2,
            'counts':counts,'criterion_counts':{f'm{m}:{kind}':v for (m,s,kind),v in sorted(tally.items()) if s=='excluded'},
            'fully_checked':True,
            'scope':'all exact rank-eight census records at multiplicities 1 and 2; unresolved cases are not classified'}
    (ROOT/'verification'/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('VERIFIED',json.dumps(report['counts'],separators=(',',':')))


if __name__=='__main__':main()
