"""Source-bound final ledger of the five commutative integer-center screens.

This metadata gate does not replace the exact replay in verify_research.py.
It rejects unfinished endpoints and distinguishes a checked necessary-system
witness from a category model, general exclusion, or exhaustive integer search.
"""
from pathlib import Path
import argparse, hashlib, json, sys
HERE = Path(__file__).resolve().parent
STAGE = HERE.parent
sys.path.insert(0, str(STAGE / 'global_induction'))
import streaming as st
from exact import require

PLANNED = (65, 982, 1768, 1795, 3472)
CONTROLS = (
    'commutative_integer/verify_control.py',
    'commutative_integer/verify_lattice.py',
    'commutative_integer/verify_linear.py',
    'quadratic/atomic_galois_balance.py',
    'quadratic/galois_support_filter.py',
    'quadratic/joint_galois_balance.py',
    'quadratic/fp_fusion_bounds.py',
    'quadratic/pure_pointed_bounds.py',
    'quadratic/integer_phase_cuts.py',
    'quadratic_atomic_integer/unit_pair_constraints.py',
)
REPLAYS = (
    'quadratic/phase_integer_65.py',
    'commutative_integer/r982.py',
    'commutative_integer/r982_joint_probe.py',
    'commutative_integer/r982_unit_pair_probe.py',
    'commutative_integer/r982_phases.py',
    'commutative_integer/r982_rational.py',
    'quadratic_atomic_integer/final_verify.py',
    'quadratic/strong_integer_3472.py',
)
CONTROL_RECEIPTS = (
    'commutative_integer/control.json',
    'commutative_integer/lattice_validation.json',
    'commutative_integer/linear_validation.json',
    'quadratic/atomic_galois_balance_results.json',
    'quadratic/galois_support_control_results.json',
    'quadratic/joint_galois_balance_results.json',
    'quadratic/fp_fusion_bounds_results.json',
    'quadratic/pure_pointed_bounds_results.json',
    'quadratic/integer_phase_cuts_results.json',
    'quadratic_atomic_integer/unit_pair_control.json',
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(relative, number=None):
    path = STAGE / relative
    data = json.loads(path.read_text())
    if number is not None:
        source = st.load_ring(f'R8_3_{number}')
        require(data['id'] == source['id'] and data['tensor_sha256'] == source['tensor_sha256'],
                'final integer endpoint source identity differs')
    return data


def collect_pins(value, dependencies):
    if isinstance(value, dict):
        pins = value.get('source_sha256')
        if isinstance(pins, dict):
            for relative, digest in pins.items():
                path = (STAGE / relative).resolve()
                require(path.is_relative_to(STAGE.resolve()) and path.is_file(), 'invalid source dependency')
                require(sha(path) == digest, 'late source dependency changed: ' + relative)
                dependencies[relative] = digest
        for item in value.values(): collect_pins(item, dependencies)
    elif isinstance(value, list):
        for item in value: collect_pins(item, dependencies)


def build():
    records = []
    q65 = 'quadratic/phase_integer_65_results.json'
    d65 = load(q65, 65)
    require(d65['status'] in (
        'exact_integer_and_phase_compatible', 'phase_reconstruction_inconclusive',
        'ten_global_cuts_completed_no_compatible_integer_witness',
        'all_indicator_pattern_rejected_without_uniform_global_cut',
        'exact_integer_box_obstruction', 'exact_bounded_linear_obstruction',
        'exact_modular_obstruction', 'integer_search_inconclusive_after_exact_global_cuts',
        'completed_wall_budget_with_exact_cuts'), 'R65 final endpoint is unfinished or unrecognized')
    require(d65.get('rounds') and 'final_metadata' in d65, 'R65 final cut campaign lacks closure')
    records.append({'id': 'R8_3_65', 'status': d65['status'],
        'evidence': [q65, 'quadratic/joint_atomic_integer_65_results.json', 'quadratic/phase_65_results.json'],
        'exact_replay': [['quadratic/phase_integer_65.py']],
        'completed_scope': 'Complete support/Gram/S/cubic/joint-spectrum domain, finite exact bounds, selected integer-pattern phase tests and globally valid phase-fiber cuts.',
        'limitation': 'The bounded proposal/cut campaign is not exhaustive integer-center enumeration. A necessary-system witness is not a category; a pseudo-unitary obstruction requires a separate general lift.'})

    r982 = [f'commutative_integer/R8_3_982_frame{i}.json' for i in range(4)]
    for i, relative in enumerate(r982):
        data = load(relative, 982)
        require(data['Hermite']['outcome'] == 'integer_lattice_member', 'R982 signed lattice scope differs')
        require(('original_integer_witness' in data) == (i in (2, 3)), 'R982 integer-witness coverage differs')
    for i in (2, 3):
        relative = f'commutative_integer/R8_3_982_frame{i}_phases_h4.json'
        data = load(relative, 982)
        require(data['status'] == 'selected_integer_pattern_phase_incompatible' and len(data['attempts']) == 8,
                'R982 selected-pattern phase coverage incomplete')
        r982.append(relative)
    for relative in ('R8_3_982_joint_probe.json', 'R8_3_982_unit_pair_probe.json',
                     'R8_3_982_remaining_linear.json', 'R8_3_982_rational.json'):
        r982.append('commutative_integer/' + relative)
    rational = load('commutative_integer/R8_3_982_rational.json', 982)
    require([r['frame_index'] for r in rational['records']] == [0, 1] and
            all(r['status'] == 'exact_bounded_rational_feasible_relaxation' for r in rational['records']),
            'R982 remaining-frame rational coverage incomplete')
    records.append({'id': 'R8_3_982', 'status': 'completed_four_frame_scoped_integer_and_phase_screen',
        'evidence': r982,
        'exact_replay': [[p] for p in REPLAYS if '/r982' in p],
        'completed_scope': 'Four complete labeled low frames: exact signed lattice membership for all; exact bounded rational primals for frames0/1; integer/cubic/joint-Galois/unit-product witnesses for frames2/3, each rejected by all8 fixed-mass phase indicator cases.',
        'limitation': 'The two selected-pattern phase obstructions do not reject all integer patterns. Numerical MILP infeasibility proposals for the other frames are not proofs. The ring remains unresolved.'})

    for number in (1768, 1795):
        relative = f'quadratic_atomic_integer/R8_3_{number}_final.json'
        data = load(relative, number)
        require(data['status'] in ('joint_support_obstruction', 'exact_integer_box_obstruction',
            'exact_bounded_linear_obstruction', 'exact_modular_obstruction',
            'exact_integer_lattice_obstruction', 'integer_lattice_member_no_bounded_witness',
            'no_exact_integer_conclusion_within_cap',
            'exact_bounded_integer_feasible_relaxation'), 'quadratic final endpoint unfinished')
        if data['status'] == 'integer_lattice_member_no_bounded_witness':
            require('proposal' in data, 'bounded proposal still active or unrecorded')
        if data['status'] == 'no_exact_integer_conclusion_within_cap':
            require(data.get('Hermite', {}).get('outcome') == 'no_exact_lattice_conclusion'
                    and 'proposal' in data, 'capped lattice/proposal campaign still active or unrecorded')
        records.append({'id': f'R8_3_{number}', 'status': data['status'], 'evidence': [relative],
            'exact_replay': [['quadratic_atomic_integer/final_verify.py', '--ring', str(number)]],
            'completed_scope': 'Integral-center and complete spectral-support reductions, integer Gram/S/cubic, joint Galois balance, FP bounds and source-unit product constraints, with exact recorded box/lattice/witness checks.',
            'limitation': 'A capped Hermite attempt asserts neither lattice membership nor nonmembership; its resource limits are retained in the final receipt. When proved, signed lattice membership alone is weaker than bounded nonnegative integer feasibility. Numerical proposal failures are not exclusions; categorical general scope requires an independent lift.'})

    relative = 'quadratic/strong_integer_3472_results.json'
    data = load(relative, 3472)
    require(data['status'] in ('exact_integer_box_obstruction', 'exact_bounded_linear_obstruction',
        'exact_modular_obstruction', 'exact_bounded_integer_feasible_relaxation',
        'completed_exact_screens_integer_search_inconclusive'), 'R3472 final endpoint unfinished')
    records.append({'id': 'R8_3_3472', 'status': data['status'], 'evidence': [relative],
        'exact_replay': [['quadratic/strong_integer_3472.py']],
        'completed_scope': 'Complete full-character spectral support and joint balance, integer cubic equations, FP/pure-pointed/source-unit bounds, exact finite-box propagation and saved modular or bounded certificates.',
        'limitation': 'No complete Hermite membership or bounded integer enumeration is claimed. Explicitly inconclusive numerical searches remain inconclusive.'})

    dependencies = {}
    for record in records:
        source = st.load_ring(record['id'])
        record['tensor_sha256'] = source['tensor_sha256']
        for relative in record['evidence']:
            data = load(relative)
            dependencies[relative] = sha(STAGE / relative)
            collect_pins(data, dependencies)
    direct = set(CONTROLS + REPLAYS + ('commutative_integer/final_campaign.py',
                                    'commutative_integer/verify_research.py') + CONTROL_RECEIPTS)
    for pattern in ('*.py', '*.md', '*.tex'):
        direct.update(str(p.relative_to(STAGE)) for p in HERE.glob(pattern))
    for relative in direct:
        require((STAGE / relative).is_file(), 'missing final canonical dependency: ' + relative)
        dependencies[relative] = sha(STAGE / relative)
    return {'schema': 'rank8-frontier-final-integer-screen/v1',
        'status': 'all_planned_integer_attempts_finished',
        'planned_ids': [f'R8_3_{n}' for n in PLANNED],
        'scope': 'Completed explicitly scoped necessary-system screens; no claim of exhaustive categorification search or full integral-center enumeration.',
        'records': records, 'exact_controls': [[p] for p in CONTROLS],
        'dependencies_sha256': dict(sorted(dependencies.items()))}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--write', action='store_true')
    args = ap.parse_args(); result = build(); path = HERE / 'final_campaign.json'
    if args.write: path.write_text(json.dumps(result, separators=(',', ':')) + '\n')
    else: require(result == json.loads(path.read_text()), 'final integer campaign ledger differs')
    print('PASS final integer campaign ledger: five completed scoped endpoints', flush=True)


if __name__ == '__main__': main()
