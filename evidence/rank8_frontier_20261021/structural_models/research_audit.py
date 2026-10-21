#!/usr/bin/env python3
"""Source-bound research coverage index, not a mathematical proof verifier."""
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
FRONTIER = HERE.parent
REPO = HERE.parents[2]
IDS = [65,436,439,455,567,721,731,901,903,921,925,926,928,941,982,985,
       1055,1154,1203,1350,1463,1615,1617,1660,1661,1739,1768,1795,
       2842,2885,3258,3344,3413,3472]


def require(test, message):
    if not test:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record():
    manifest = {}

    def reference(path):
        path = Path(path)
        require(path.is_file(), f'missing audit source: {path}')
        rel = str(path.relative_to(REPO))
        manifest[rel] = digest(path)
        return rel

    def read(path):
        reference(path)
        return json.loads(Path(path).read_text())

    census = read(REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json')
    sources = {r['id']:r for r in census}
    ledger = {r['id']:r for r in read(REPO/'supplements/rank8/output/m3/ledger.json')}
    baseline = read(REPO/'evidence/rank8_m3_20261021/pipeline/residual_attempts.json')
    require({r['id'] for r in baseline} == {f'R8_3_{i}' for i in IDS}, 'baseline34 audit changed')
    rows = {}
    for old in baseline:
        ident = old['id']
        tensor = sources[ident]['tensor']
        sha = hashlib.sha256(json.dumps(tensor,separators=(',',':')).encode()).hexdigest()
        require(sha == old['tensor_sha256'] == sources[ident]['tensor_sha256'], 'baseline source binding')
        rows[ident] = {'id': ident, 'tensor_sha256': sha,
                       'general_status': 'unresolved', 'true_exotic_certified': False,
                       'prior_unitary_status': ledger[ident].get('unitary_status','not_separately_decided'),
                       'prior_unitary_obstruction_source': ledger[ident].get('unitary_obstruction_source'),
                       'prior_published_attempts': [{k:v for k,v in a.items() if k != 'seconds'}
                                                    for a in old['attempts']],
                       'new_attempts': [],
                       'limitations': ['No completed search here exhausts all complex associators or all constructions.',
                                       'A feasible necessary-condition system is not a categorification.',
                                       'Numbers of attempts are not a definition or certificate of true exoticness.']}

    accepted = read(FRONTIER/'accepted.json')
    accepted_ids = {r['id'] for r in accepted['decisions']}
    for decision in accepted['decisions']:
        ident = decision['id']
        require(ident in rows and decision['tensor_sha256'] == rows[ident]['tensor_sha256'], 'accepted source binding')
        rows[ident]['general_status'] = decision['status']
        rows[ident]['accepted_certificate'] = decision['certificate']
        for key in ('evidence','proof'):
            reference(REPO/decision['certificate'][key])
        for verifier in decision['certificate'].get('verifiers',[]):
            reference(REPO/verifier)

    def add(ident, domain, outcome, scope, evidence, proof=None, verifiers=(), details=None,
            limitation='This restricted domain does not exhaust general categorifications.'):
        require(ident in rows, 'attempt outside baseline34')
        evidence = [evidence] if isinstance(evidence,(str,Path)) else list(evidence)
        entry = {'domain':domain, 'outcome':outcome, 'scope':scope,
                 'evidence':[reference(Path(p)) for p in evidence],
                 'verifiers':[reference(Path(p)) for p in verifiers],
                 'limitation':limitation}
        if proof:
            entry['proof'] = reference(Path(proof))
        if details is not None:
            entry['details'] = details
        rows[ident]['new_attempts'].append(entry)

    path = HERE/'near_group_scaling.json'
    for r in read(path)['certificates']:
        require(r['tensor_sha256'] == rows[r['id']]['tensor_sha256'], 'NG source binding')
        add(r['id'], 'all_NG_Cn_n_and_five_single_operation_routes_all_positive_n',
            'family_excluded', 'general_complex_construction_family', path,
            HERE/'NEAR_GROUP_SCALING.md', [HERE/'near_group_scaling.py'],
            {k:v for k,v in r.items() if k not in ('id','tensor_sha256')},
            'No arbitrary chains, inserted Morita changes, or noncentral condensations are covered.')

    path = HERE/'structural_scope.json'
    for r in read(path)['certificates']:
        require(r['tensor_sha256'] == rows[r['id']]['tensor_sha256'], 'structural source binding')
        add(r['id'], 'exact_adjoint_closure_braiding_and_specified_factorization_routes',
            'scoped_routes_excluded', 'general_complex_braided_or_construction_family', path,
            HERE/'STRUCTURAL_SCOPE.md', [HERE/'verify_structural_scope.py'], r)

    path = HERE/'r455/conditional_fourier.json'
    r = read(path)
    require(r['source_tensor_sha256'] == rows[r['id']]['tensor_sha256'], 'HI source binding')
    add(r['id'], 'all_strict_Evans_Gannon_HI_C3_matrix_neutrals_and_full_subgroup_Fourier_dual',
        'conditional_family_excluded', 'general_complex_with_strict_HI_presentation_hypothesis', path,
        HERE/'r455/README.md', [HERE/'r455/verify_conditional_fourier.py'],
        {'Groebner_basis':r['Groebner_basis'],'elementary_branch_residuals':r['elementary_branch_residuals']},
        r['remaining_gap'])

    path = HERE/'c3_morita_dual.json'
    for r in read(path)['records']:
        require(r['tensor_sha256'] == rows[r['id']]['tensor_sha256'], 'C3 Morita source binding')
        add(r['id'],'complete_C3_subgroup_algebra_Morita_dual_based_ring',r['outcome'],
            'conditional_on_any_general_complex_categorification',path,HERE/'C3_MORITA_DUAL.md',
            [HERE/'c3_morita_dual.py'],
            {k:r[k] for k in ('dual_simple_count','dual_invertible_group',
                             'dual_noninvertible_uniqueness_constraint_rank','fusion_coefficients_checked')},
            'Same based ring does not mean tensor equivalence; other algebra objects and Morita chains remain open.')
    path = HERE/'r65_rank_two_modules.json'
    r = read(path)
    require(r['tensor_sha256'] == rows[r['id']]['tensor_sha256'], 'R65 rank2 source binding')
    add(r['id'],'all_connected_rank_two_based_modules_and_pointed_cocycle_branch',r['outcome'],
        'general_complex_necessary_module_constraints',path,HERE/'R65_MODULES.md',
        [HERE/'r65_rank_two_modules.py'],r,r['limitation'])

    q = FRONTIER/'quadratic'
    for fn, domain, proof, verifier in [
            ('simultaneous_split_results.json','complete_C2_simultaneous_split_module_quotients','SIMULTANEOUS_SPLIT_MODULE.md','simultaneous_split.py'),
            ('normal_split_spectral_results.json','complete_normal_C2_split_spectral_and_transport_test','NORMAL_SPLIT_SPECTRAL.md','normal_split_spectral.py'),
            ('residual_split_1055_results.json','complete_C2_difference_representations','RESIDUAL_QUADRATIC_SEARCH.md','residual_split_1055.py'),
            ('cubic_split_module_results.json','complete_C3_Fourier_difference_representations','CUBIC_SPLIT_MODULE.md','cubic_split_module.py')]:
        data = read(q/fn)
        items = data.get('records',[data])
        for r in items:
            if r.get('id') not in rows:
                continue
            require(r['tensor_sha256'] == rows[r['id']]['tensor_sha256'], 'split source binding')
            result = 'accepted_general_exclusion' if r['id'] in accepted_ids else r.get('outcome','no_conclusion')
            stats = {key:r[key] for key in ('finite_cases_after_proved_phase_gauge','representation_count',
                     'normal_generator_domain','reduced_simultaneous_domain','independent_full_box') if key in r}
            if 'exact_solutions' in r:
                stats['exact_necessary_solution_count'] = len(r['exact_solutions'])
            if 'search' in r:
                stats['complete_search_outcome'] = r['search'].get('outcome',r.get('outcome'))
            add(r['id'],domain,result,'general_complex_necessary_module_constraints',q/fn,q/proof,[q/verifier],stats,
                'An exact surviving based/Fourier module is necessary data only; no module associator is constructed.')
    path = q/'rank_two_and_models_results.json'
    for r in read(path)['records']:
        require(r['tensor_sha256'] == rows[r['id']]['tensor_sha256'], 'rank2 source binding')
        rank2 = r['rank_two_module_search']
        add(r['id'],'all_connected_rank_two_based_modules_up_to_permutation',rank2['outcome'],
            'general_complex_necessary_module_constraints',path,q/'RESIDUAL_QUADRATIC_SEARCH.md',
            [q/'rank_two_and_models.py'],{k:v for k,v in rank2.items() if k!='classes'},
            'No pentagon or algebra multiplication is supplied for the feasible based modules.')
        models = r['generalized_near_group_model_search']
        add(r['id'],'all_generalized_near_group_dimension_families_with_integer_multipliers',models['outcome'],
            'construction_family_dimension_necessary_condition',path,q/'RESIDUAL_QUADRATIC_SEARCH.md',
            [q/'rank_two_and_models.py'],models,
            'Dimension matches are not models; division by de-equivariantization is outside this separate family sieve.')
    path = q/'structural_constructions_results.json'
    data = read(path)
    for r in data['records']:
        require(r['tensor_sha256'] == rows[r['id']]['tensor_sha256'], 'quadratic construction source binding')
        add(r['id'],'complete_subrings_gradings_equivariantizations_and_rank4_GNG_branches',
            'specified_construction_routes_excluded','general_complex_construction_families',path,
            q/'STRUCTURAL_CONSTRUCTIONS.md',[q/'structural_constructions.py'],r,
            'These construction negatives do not exclude all complex categorifications; rank-four dependence is explicitly pinned in the receipt.')

    n = FRONTIER/'noncommutative'
    data = read(n/'central_support_results.json')
    for r in data:
        ident = r['id']
        require(r['tensor_sha256'] == rows[ident]['tensor_sha256'], 'NC source binding')
        add(ident,'complete_central_image_low_induction_and_Gram_moment_constraints','necessary_data_survives',
            'pseudo_unitary_only',n/'central_support_results.json',n/'README.md',
            [n/'verify_all.py',n/'verify_independent.py'],
            {'low_count':r['low_count'],'passing_low_count':r['passing_low_count']},
            'This is a pseudo-unitary necessary-condition test; surviving data need not lift to a center.')
    for r in read(n/'matricial_structure.json'):
        if r['id'] in rows:
            add(r['id'],'exact_matrix_block_involution_and_pointed_bimodule_cocycle_constraints',
                'necessary_structure_compatible','based_ring_and_pointed_coherence_constraints',
                n/'matricial_structure.json',n/'README.md',[n/'verify_all.py'],
                {k:v for k,v in r.items() if k not in ('palindromic_odd_multiplicity_edges',)})
    def decision_statuses(obj):
        found = []
        if isinstance(obj,dict):
            if 'decision' in obj:
                found.append(obj['decision'].get('status','unspecified'))
            for key,val in obj.items():
                if key != 'decision':
                    found.extend(decision_statuses(val))
        elif isinstance(obj,list):
            for val in obj:
                found.extend(decision_statuses(val))
        return found
    for pattern,domain in [('certified_*.json','finite_order_higher_rotation_LP'),
                           ('modular_*.json','joint_rotation_and_partial_STS_LP'),
                           ('spectral_modular_*.json','integral_fusion_eigenvalue_and_partial_STS_LP'),
                           ('integral_gram_*.json','complete_integer_Gram_frames_with_rotation_LP'),
                           ('integral_modular_*.json','fixed_integer_Gram_multiplicities_joint_rotation_and_STS')]:
        for path in sorted(n.glob(pattern)):
            r = read(path)
            if r.get('id') not in rows:
                continue
            if r.get('tensor_sha256'):
                require(r['tensor_sha256'] == rows[r['id']]['tensor_sha256'], 'NC LP source binding')
            statuses = decision_statuses(r)
            add(r['id'],domain,'; '.join(sorted(set(statuses))) or r.get('status','see_linked_exact_receipt'),
                'pseudo_unitary_only',path,n/'README.md',[n/'verify_all.py'],
                {'height':r.get('height'),'low_index':r.get('low_index'),
                 'exact_or_numeric_branch_statuses':statuses},
                'Individual infeasible branches do not exclude the ring; numeric undecided is not an exact result.')
    for filename,domain in [('central_fusion_721.json','fixed_cubic_forgetful_tensor_relaxations'),
                            ('verlinde_low_721.json','nonnegative_integer_low_cubic_Verlinde_coefficients'),
                            ('central_integral_filters_1154.json','all_integer_Gram_patterns_cubic_Verlinde_and_Galois_balance'),
                            ('cubic_tensor_1154.json','all_surviving_Gram_patterns_all_ten_low_pair_forgetful_tensor_cones')]:
        path=n/filename
        r=read(path)
        require(r['tensor_sha256']==rows[r['id']]['tensor_sha256'],'central fusion source binding')
        details={key:r[key]for key in ('domain','gram_pattern_count','input_gram_patterns')if key in r}
        if 'cases'in r:details['case_count']=len(r['cases'])
        for key in ('cubic_survivor_indices','spectral_survivor_indices','combined_survivor_indices'):
            if key in r:details[key.replace('indices','count')]=len(r[key])
        add(r['id'],domain,'exact_necessary_data_survives','pseudo_unitary_only',path,
            n/'README.md',[n/'verify_all.py'],details,
            r.get('conclusion','Necessary central data survives; full integer fusion and associator coherence are not constructed.'))

    g = FRONTIER/'global_induction'
    for pattern in ('results/*.json','frame_results/*.json','fixed_results/*.json'):
        for path in sorted(g.glob(pattern)):
            r = read(path)
            if r.get('id') not in rows:
                continue
            require(r['tensor_sha256'] == rows[r['id']]['tensor_sha256'], 'global induction source binding')
            meta = r.get('metadata',{})
            add(r['id'],r.get('method','fixed_integral_low_frame_global_induction'),r.get('status','see_receipt'),
                r.get('scope','pseudo_unitary_induction_relaxation'),path,g/'PROOF.md',
                [g/'verify_streaming.py',g/'verify_frames.py'],
                {'height':r.get('height'),'frame_index':r.get('frame_index'),
                 'rows':meta.get('rows'),'variables':meta.get('variables'),
                 'low_frames':meta.get('low_frames'),'high_columns':meta.get('high_columns')},
                'A running/partial computation is incomplete; a feasible relaxation does not construct integer center data or an associator.')

    integral = FRONTIER/'integral'
    for r in read(integral/'results.json'):
        ident = r['id']
        require(r['tensor_sha256'] == rows[ident]['tensor_sha256'], 'integral source binding')
        outcome = 'accepted_general_exclusion' if ident in accepted_ids else 'proposed_general_exclusion_pending_acceptance'
        verifier = ('verify_central_731.py' if ident == 'R8_3_731' else 'structural_certificate.py')
        add(ident,r['criterion'],outcome,r['scope'],
            [integral/'results.json']+[integral/f for f in r['certificate_files']],
            integral/'PROOF.md',[integral/verifier],
            limitation='General exclusion is used only after independent review and entry in accepted.json.')

    # Status is controlled exclusively by the parent's accepted ledger.
    ordered = [rows[f'R8_3_{i}'] for i in IDS]
    return {'schema':'rank8-frontier-per-ring-research-audit/v1',
            'scope':'research coverage and source binding; linked proof verifiers provide mathematical replay',
            'research_status':accepted.get('research_status','ongoing'),
            'baseline_ring_count':34,
            'accepted_general_exclusions':sum(r['general_status']=='excluded' for r in ordered),
            'true_exoticness_claim':'No ring is certified truly exotic by attempt counts or necessary-condition survival.',
            'rows':ordered,'artifact_sha256':dict(sorted(manifest.items()))}


def markdown(data):
    lines=['# Frontier research coverage for the original 34 rings','',
           'This index separates accepted general exclusions, restricted construction obstructions,',
           'exact survival of necessary conditions, and unfinished computations. No remaining ring',
           'is certified truly exotic merely because several attempts failed. The JSON retains',
           'the prior published attempts and the exact domain, scope, evidence, verifier and',
           'limitation of every new attempt. Numerical undecided results are not proofs.','',
           '| Ring | Current general status | New domains and outcomes |',
           '|---|---|---|']
    for row in data['rows']:
        summary='; '.join(a['domain'].replace('_',' ')+': '+a['outcome'].replace('_',' ')
                         for a in row['new_attempts'])
        lines.append('| '+row['id']+' | '+row['general_status']+' | '+summary.replace('|','/')+' |')
    lines += ['', 'The universal cyclic near-group filter covers all positive orders, but only the',
              'listed direct/Morita and single-operation routes. The remaining untested domains',
              'include arbitrary associators, noncentral algebra condensations, and unrestricted',
              'chains with Morita changes. Explicit limitations are preserved ring by ring.', '',
              'Run `research_audit.py` to verify this index against its evidence snapshot.',
              'That check verifies aggregation and source binding; it does not replace the',
              'separately linked mathematical replay programs. `--write` refreshes the index',
              'after genuinely new evidence or accepted decisions are added.', '']
    return '\n'.join(lines)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    actual=record()
    jp=HERE/'per_ring_research_audit.json'
    mp=HERE/'per_ring_research_audit.md'
    rendered=markdown(actual)
    if args.write:
        jp.write_text(json.dumps(actual,indent=2)+'\n')
        mp.write_text(rendered)
    else:
        require(actual == json.loads(jp.read_text()),'research evidence snapshot changed; explicitly refresh after review')
        require(rendered == mp.read_text(),'research Markdown differs')
    print(f"PASS:34 source-bound research rows; {actual['accepted_general_exclusions']} accepted general exclusions; no automatic exoticness label.")


if __name__=='__main__':
    main()
