"""Generate the explicitly scoped disposition of each original residual case."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[3])
repo = parser.parse_args().repo.resolve()
folder = repo/'evidence/theoretical_20261016/rank8'
audit = json.loads((folder/'all44_subcategory_indices_normal.json').read_text())
groups = []

def add(ids, scope, strategy, gap, evidence):
    groups.append((ids, scope, strategy, gap, evidence))

add(['R8_1_9','R8_1_18','R8_1_49'], 'unresolved; no braided categorification',
    'Order-four generalized near-group rings with noninvertible dimension 2+sqrt(5); general existence is equivalent to pseudo-unitary existence by the two-dimension Galois bridge.',
    'The old scalar-gauge central-lift calculations have not been reconstructed. Even a central lift need not be a boson. The new 2D2 central-lift obstruction alone does not supply the additional descended lift required for a contradiction.',
    ['evidence/upper_residual_20261002b/r8_nonintegral/SCOPED_RESULTS.md','evidence/theoretical_20261016/rank8_m1/'])
add(['R8_2_24'], 'unresolved; unitary categorification excluded',
    'A C2 extension of the 2D2 neutral subcategory with C4 invertibles; the label-fixing tensor-auto-equivalence kernel excludes its square relation in the unitary case.',
    'The required uniqueness and auto-equivalence classification are unitary results; no classification of all nonunitary neutral categories is available here.',
    ['evidence/upper_residual_20261002b/r8_nonintegral/SCOPED_RESULTS.md'])
add(['R8_2_33','R8_2_36','R8_2_76','R8_2_412','R8_2_446'], 'unresolved',
    'Order-four generalized near-group family with noninvertible dimension 4+sqrt(17); the conductor-17 dimension-block bound is attained.',
    'The bound is an equality, not a contradiction; no associator construction or general exclusion has been established.', [])
add(['R8_2_35','R8_2_38','R8_2_346','R8_2_406'], 'excluded over C',
    'Two-dimension Galois bridge followed by the conductor-40 dimension-block bound: 9/160 exceeds 1/40.',
    'None for the asserted general exclusion.', ['evidence/theoretical_20261016/rank8/DIMENSION_BLOCK_FOUR_PROOF.md'])
add(['R8_2_37','R8_2_170'], 'unresolved',
    'Quasi-trivial C2 extensions of the 2D2 neutral ring; a label-swapping tensor auto-equivalence would control the candidate crossed product.',
    'The multiplication and coherent square of the required auto-equivalence are not determined by the published order-eight auto-equivalence count. An abstract group order does not construct an extension.', [])
add(['R8_2_152','R8_2_153','R8_2_166','R8_2_495'], 'unresolved; unitary categorification excluded',
    'Faithful C2 extensions of the 2D2 neutral category whose odd components have no invertible simple; this contradicts the unitary Brauer-Picard classification.',
    'The unitary uniqueness theorem cannot be promoted to an unrestricted categorification theorem.',
    ['evidence/upper_residual_20261002b/r8_nonintegral/SCOPED_RESULTS.md'])
add(['R8_2_190','R8_2_489'], 'unresolved',
    'Both contain a Fibonacci-times-C2 fusion subring. Their other dimensions are d and phi*d, with d=phi+sqrt((5+sqrt(5))/2).',
    'A central lift or tensor factorization of the Fibonacci subcategory has not been established. The dimension pattern by itself does not yield such a factorization.', [])
add(['R8_2_209'], 'excluded over C',
    'The C3 pointed subcategory has FP index with nonintegral trace 145/3.',
    'None for the asserted general exclusion.', ['evidence/theoretical_20261016/rank8/R209_GENERAL_PROOF.md'])
add(['R8_2_260'], 'excluded over C',
    'Cyclic-module divisibility for the fixed C3 action: Norm((3+2sqrt(3))/3)=-1/3 forces 3 to divide N33^3=2.',
    'None for the asserted general exclusion.', ['evidence/theoretical_20261016/CYCLIC_MODULE_DIVISIBILITY.md','evidence/theoretical_20261016/rank8/CYCLIC_STABILIZER_DIVISIBILITY.md'])
add(['R8_2_314','R8_2_432'], 'unresolved',
    'Each noncommutative ring contains two rank-four PSU(2)_6-type subrings sharing an invertible; the global dimension is 48+32sqrt(2).',
    'The subcategory-index and dimension-block calculations do not contradict existence; an associativity or compatibility obstruction is still required.', [])
add(['R8_2_318','R8_2_319','R8_2_320','R8_2_368','R8_2_370','R8_2_735','R8_2_758','R8_2_760'], 'excluded over C',
    'The four-dimensional anti-invariant module of the regular involution algebra would have a normal integral generator with incompatible spectral norm and entry parity. For 318/735, the sole surviving spectrum also contradicts the trace bound.',
    'None for the asserted general exclusion; no pivotality or sphericality is assumed.',
    ['evidence/theoretical_20261016/rank8/ANTI_MODULE_EIGHT_GENERAL_PROOF.md','evidence/theoretical_20261016/rank8/anti_module_eight_normal.json'])
add(['R8_2_342','R8_2_666'], 'unresolved',
    'Quadratic sqrt(2) family with global FP dimension 96+64sqrt(2); the complete involution anti-module domain has one sign-gauge class, and all six dual-module Gram systems have exact integral factor witnesses.',
    'The relevant half-dimensions are algebraic integers, so cyclic-module divisibility gives no contradiction. Passing the necessary module conditions does not construct a categorification.',
    ['evidence/theoretical_20261016/compression/README.md','evidence/theoretical_20261016/rank8/FRONTIER_MODULE_AUDIT.md','evidence/theoretical_20261016/rank8/frontier_modules_normal.json'])
add(['R8_2_535','R8_2_630','R8_2_671'], 'unresolved',
    'Quadratic sqrt(10) family with global FP dimension 120+36sqrt(10); the conductor-40 bound is attained.',
    'The remaining formal codegrees are rational, so the equality consequence gives no additional contradiction. For 630/671 the unique anti-module class passes all six dual-module Gram systems with exact integral factors; these necessary witnesses do not construct a category.', ['evidence/theoretical_20261016/rank8/FRONTIER_MODULE_AUDIT.md','evidence/theoretical_20261016/rank8/frontier_modules_normal.json'])
add(['R8_2_380','R8_2_673'], 'excluded over C',
    'Regular-C2 Morita duality produces ten dihedral invertibles and two simples of each dimension x=4+sqrt(6), y=3+2sqrt(6). The C5 fixed action forces 5|b,c in b+2c=8.',
    'None for the asserted general exclusion.', ['evidence/theoretical_20261016/CYCLIC_MODULE_DIVISIBILITY.md','evidence/theoretical_20261016/rank8/CYCLIC_STABILIZER_DIVISIBILITY.md'])
add(['R8_2_745'], 'excluded over C',
    'Regular-C2 Morita duality gives a dihedral generalized near-group category whose adjoint subcategory would have a normal order-two invertible subgroup in D10.',
    'No such normal subgroup exists; no gap for the asserted general exclusion.', ['evidence/theoretical_20261016/rank8/R745_GENERAL_PROOF.md'])
add(['R8_2_820','R8_2_869'], 'unresolved',
    'Simple based rings with no proper nontrivial fusion subrings and global FP dimension (315+135sqrt(5))/2.',
    'Subcategory-index methods are vacuous. A construction or a stronger center/associativity obstruction is needed.', [])
add(['R8_2_857'], 'excluded over C',
    'A primitive conductor-32 Fourier bound forces any sphericalization dimension field to have degree eight. Three signed Jacobi-matrix branches give respectively an oversized fusion coefficient, field degree at most four, or an excluded spherical section.',
    'None for the asserted general exclusion. The exact folded even level-30 SU(2) tensor identification provides its structural interpretation.',
    ['evidence/theoretical_20261016/compression/R857_GENERAL_PROOF.md','evidence/theoretical_20261016/compression/R857_general_certificate.json','evidence/theoretical_20261016/rank8/R857_FOLDED_A31_IDENTIFICATION.md'])

metadata = {}
for ids, scope, strategy, gap, evidence in groups:
    for identifier in ids:
        if identifier in metadata:
            raise ValueError('Duplicate case '+identifier)
        metadata[identifier] = {'disposition':scope, 'strategy_or_proof':strategy, 'remaining_gap':gap, 'evidence':evidence}
if set(metadata) != {r['id'] for r in audit['cases']}:
    raise ValueError('Coverage differs from original residual set')
cases = []
for r in audit['cases']:
    cases.append({k:r[k] for k in ('id','tensor_sha256','index_condition','proper_nontrivial_fusion_subring_count')} | metadata[r['id']])
excluded = sum(r['disposition']=='excluded over C' for r in cases)
if excluded != 18:
    raise ValueError('Eighteen general exclusions expected')
result = {'source_stage':'upper_residual_20261002c', 'source_case_count':44,
          'new_general_exclusions':excluded, 'still_generally_unresolved':44-excluded,
          'warning':'PASS is only an exact necessary-condition result. Scoped exclusions are not general exclusions. This is not a completed classification.',
          'index_audit':'evidence/theoretical_20261016/rank8/all44_subcategory_indices_normal.json', 'cases':cases}
(folder/'all44_coverage.json').write_text(json.dumps(result,indent=2)+'\n')
lines = ['# All 44 original rank-eight residual cases', '',
         'Eighteen general exclusions are proved in this update; 26 cases remain unresolved in general. Every original case has an explicit disposition below. Passing an index test is only a necessary condition and is not evidence of a categorification.', '',
         'The exact source-bound audit checks every proper nontrivial closed fusion subring: 40 cases pass all their indices, R8_2_209 fails, and three simple based rings have no such subring. The full index values, minimal polynomials, positive dimension characters, and tensor hashes are in `all44_subcategory_indices_normal.json`; the optimized replay is separate.', '',
         '| Case | Disposition | Index test | Strategy or proof; remaining gap |',
         '|---|---|---|---|']
for r in cases:
    lines.append('| '+r['id']+' | '+r['disposition']+' | '+r['index_condition']+' ('+str(r['proper_nontrivial_fusion_subring_count'])+' subrings) | '+r['strategy_or_proof']+' **Gap:** '+r['remaining_gap']+' |')
lines += ['', 'The companion `all44_coverage.json` includes source tensor hashes and evidence paths. The unrestricted ledger retains every scoped or unresolved case.']
(folder/'ALL44_COVERAGE.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'status':'PASS','cases':44,'general_exclusions':excluded,'general_unresolved':44-excluded}))
