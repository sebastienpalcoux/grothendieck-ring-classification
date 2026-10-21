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
SCREENING_FOCUS = {
65:'Free C4 generalized-near-group structure; complete rank-two based-module necessary data and connected-algebra underlying-object necessary filters; all nontrivial group-equivariantizations excluded; full character-field central constraints and specified unbounded model families tested.',
439:'Complete C3 Fourier necessary representations and Morita fusion tensor; forced untwisted S3 associator and rank-five Morita dual with an associator inequivalent to the known model; complete connected-algebra underlying-object necessary filters and central constraints; actual crossed and all-level SU(2)/adjoint construction families excluded.',
455:'Haagerup neutral and TY bridge; complete strict Evans-Gannon Fourier obstruction with explicit abstract-to-strict gap; connected-algebra underlying-object necessary filters, general Galois-PU reduction, central data and specified unbounded model-family filters tested.',
567:'Complete C3 Fourier necessary representations and Morita fusion tensor; forced nontrivial S3 pointed C2 restriction obstructs full-S3 algebra; complete connected-algebra underlying-object necessary filters and central constraints; actual crossed and all-level SU(2)/adjoint construction families excluded.',
721:'All six known Asaeda-Haagerup Morita categories compared; all integer-scaled near-group sources and all-level SU(2)/adjoint families excluded; complete integer central Gram domain, rotation/STS/cubic/forgetful constraints and connected-algebra underlying-object necessary filters tested.',
903:'Complete connected-algebra underlying-object necessary filters, labeled central-induction frame constraints, all-level SU(2)/adjoint quantum-group products and unbounded generalized-near-group parameter families tested.',
928:'General Galois-PU reduction, quaternionic rational block, pointed cocycle constraints, full central induction/rotation/STS data, complete connected-algebra underlying-object necessary filters, all-level SU(2)/adjoint products and specified unbounded near-group families tested.',
941:'General Galois-PU reduction, split rational block and pointed algebra route, central induction/rotation/STS data, complete connected-algebra underlying-object necessary filters, all-level SU(2)/adjoint products and specified unbounded near-group families tested; Morita coherence remains open.',
982:'Complete connected-algebra underlying-object necessary filters and labeled central-induction/STS constraints, together with all-level SU(2)/adjoint quantum-group products and unbounded generalized-near-group parameter families tested.',
1154:'General Galois-PU reduction; all 14,211 integer central Gram patterns filtered to 1,238 cubic/spectral survivors and 1,230 exact joint rotation/STS survivors; complete connected-algebra underlying-object necessary filters and specified unbounded model families tested.',
1615:'Complete connected-algebra underlying-object necessary filters, full labeled central-induction constraints and repeated exact known/new exclusions, plus all-level SU(2)/adjoint quantum-group products and unbounded generalized-near-group family tests.',
1617:'Complete connected-algebra underlying-object necessary filters, full labeled central-induction constraints and repeated exact known/new exclusions, plus all-level SU(2)/adjoint quantum-group products and unbounded generalized-near-group family tests.',
1660:'Complete connected-algebra underlying-object necessary filters, full labeled central-induction constraints and repeated exact known/new exclusions, plus all-level SU(2)/adjoint quantum-group products and unbounded generalized-near-group family tests.',
1661:'Complete connected-algebra underlying-object necessary filters, full labeled central-induction constraints and repeated exact known/new exclusions, plus all-level SU(2)/adjoint quantum-group products and unbounded generalized-near-group family tests.',
1768:'Complete rank-two based-module necessary data and connected-algebra underlying-object necessary filters; every proper subring, grading and nontrivial finite-group equivariantization tested; exact global central constraints and specified unbounded construction families tested.',
1795:'Complete rank-two based-module necessary data and connected-algebra underlying-object necessary filters; every proper subring, grading and nontrivial finite-group equivariantization tested; exact global central constraints and specified unbounded construction families tested.',
3472:'Complete rank-two based-module necessary data and connected-algebra underlying-object necessary filters; every proper subring, grading and nontrivial finite-group equivariantization tested; full character-field central constraints and specified unbounded construction families tested.'}
SCREENING_DEFINITION = ('Extensively investigated exotic candidate means that the ring survived the documented, case-specific campaign of known and newly developed exclusion tests and explicit model searches, including complete finite domains and specified unbounded construction families. It proves neither existence of a fusion category nor novelty of a future realization. Each case lists exactly what was exhausted, what survived and the remaining hypotheses.')
ACTIVE_STATES={'running','queued','discovery_in_progress','constructing_complete_domain',
               'solving_complete_sparse_cone','pseudo_certificate_verified'}


def completed_queue():
    path=FRONTIER/'global_induction/complete_queue.json'
    require(path.is_file(),'final completion queue receipt is missing')
    queue=json.loads(path.read_text())
    require(queue.get('status')=='all_serial_attempts_finished',
            'the planned serial exact queue has not finished')
    targets=[tuple(x)for x in queue['targets']]
    records=queue['records']
    require(len(records)==len(targets)and
            [(r['id'],r['variant'])for r in records]==targets,
            'completion queue does not account for every planned target')
    require(all(r.get('status')not in ACTIVE_STATES for r in records),
            'a completion queue record is still active')
    for r in records:
        if r.get('status')in('excluded','exact_feasible_relaxation'):
            require(r.get('optimized_exact_replay')=='PASS'and r.get('replay_exit_code')==0,
                    'completed exact queue result lacks successful optimized replay')
    return path,queue


def require(test, message):
    if not test:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(use_screening=True):
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
                       'general_status': 'unresolved', 'categorification_or_novelty_proved': False,
                       'screening_stage':'active_structural_and_construction_research',
                       'prior_unitary_status': ledger[ident].get('unitary_status','not_separately_decided'),
                       'prior_unitary_obstruction_source': ledger[ident].get('unitary_obstruction_source'),
                       'prior_published_attempts': [{k:v for k,v in a.items() if k != 'seconds'}
                                                    for a in old['attempts']],
                       'new_attempts': [],
                       'limitations': ['No completed search here exhausts all complex associators or all constructions.',
                                       'A feasible necessary-condition system is not a categorification.',
                                       'Extensively investigated exotic candidate is a research-screening description, not a proof of categorifiability or novelty.']}

    accepted = read(FRONTIER/'accepted.json')
    accepted_ids = {r['id'] for r in accepted['decisions']}
    for decision in accepted['decisions']:
        ident = decision['id']
        require(ident in rows and decision['tensor_sha256'] == rows[ident]['tensor_sha256'], 'accepted source binding')
        rows[ident]['general_status'] = decision['status']
        rows[ident]['screening_stage']='general_exclusion_accepted_after_review'
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
    path=HERE/'s3_full_condensation.json'
    data=read(path)
    for r in data['records']:
        require(r['tensor_sha256']==rows[r['id']]['tensor_sha256'],'full S3 source binding')
        add(r['id'],'full_S3_condensation_with_trivial_pointed_cocycle_and_all_dual_rank5_tensors',r['outcome'],
            'conditional_general_complex_Morita_construction_branch',path,HERE/'S3_FULL_CONDENSATION.md',
            [HERE/'s3_full_condensation.py'],
            {'hypothesis':r['hypothesis'],'module_rank':r['right_S3_module_rank'],
             'dual_rank':r['conditional_dual_rank'],'complete_based_tensor_count':data['based_tensor_isomorphism_representatives']},
            r['limitation'])
    path=HERE/'known_model_routes.json'
    for r in read(path)['records']:
        require(r['tensor_sha256']==rows[r['id']]['tensor_sha256'],'known model route source binding')
        domain=('complete_retained_SU2_Morita_family_and_actual_near_group_inversion_crossed_product'
                if r['id']in('R8_3_439','R8_3_567')else
                'all_near_group_orders_and_multiplicities_with_integer_scalings_and_Morita_duals')
        add(r['id'],domain,'specified_families_excluded','general_complex_construction_families',
            [path,HERE/'rank5_route_bindings.json'],HERE/'KNOWN_MODEL_ROUTES.md',
            [HERE/'known_model_routes.py',HERE/'rank5_route_bindings.py'],r,r['limitation'])
    path=HERE/'pointed_s3_scope.json'
    for r in read(path)['records']:
        require(r['tensor_sha256']==rows[r['id']]['tensor_sha256'],'pointed S3 scope source binding')
        add(r['id'],'complete_pointed_S3_cocycle_and_subgroup_Morita_branch_after_forced_indicators',
            r['outcome'],r['scope'],path,HERE/'POINTED_S3_SCOPE.md',
            [HERE/'pointed_s3_scope.py'],r,r['limitation'])
    path = HERE/'r65_rank_two_modules.json'
    r = read(path)
    require(r['tensor_sha256'] == rows[r['id']]['tensor_sha256'], 'R65 rank2 source binding')
    add(r['id'],'all_connected_rank_two_based_modules_and_pointed_cocycle_branch',r['outcome'],
        'general_complex_necessary_module_constraints',path,HERE/'R65_MODULES.md',
        [HERE/'r65_rank_two_modules.py'],r,r['limitation'])
    add(r['id'],'all_nontrivial_finite_group_equivariantizations',
        'family_excluded','general_complex_construction_family',path,HERE/'R65_MODULES.md',
        [HERE/'r65_rank_two_modules.py'],r['nontrivial_finite_group_equivariantizations'],
        'The pinned rank-four theorem excludes central Tannakian condensation, not general noncentral Morita constructions.')
    path=HERE/'algebra_candidates.json'
    for r in read(path)['records']:
        require(r['tensor_sha256']==rows[r['id']]['tensor_sha256'],'structural algebra source binding')
        add(r['id'],'all_connected_separable_algebra_underlying_objects_entrywise_and_PSD_Gram',
            'complete_necessary_object_filter_survives','general_complex_algebra_construction_constraints',path,
            HERE/'ALGEBRA_CANDIDATES.md',[HERE/'algebra_candidates.py'],
            {key:r[key]for key in ('bounded_selfdual_vectors_tested','invertible_stabilizer_survivors',
                'entrywise_Gram_survivors','PSD_Gram_survivors','independent_complete_Python_domain',
                'one_plus_simple_surviving_indices')},r['limitation'])

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
    path=q/'connected_algebra_candidates_results.json'
    for r in read(path)['records']:
        if r['id']not in rows:continue
        require(r['tensor_sha256']==rows[r['id']]['tensor_sha256'],'quadratic algebra source binding')
        add(r['id'],'all_connected_separable_algebra_underlying_objects_entrywise_and_PSD_Gram',
            'complete_necessary_object_filter_survives','general_complex_algebra_construction_constraints',path,
            q/'CONNECTED_ALGEBRA_CANDIDATES.md',[q/'connected_algebra_candidates.py'],
            {key:r[key]for key in ('bounded_selfdual_vectors_tested','invertible_stabilizer_survivors',
                'entrywise_Gram_survivors','PSD_Gram_survivors','one_plus_simple_surviving_indices')},
            'Every actual connected separable algebra passes this filter; surviving objects have no associative multiplication or module structure certified.')

    general_nc=set()
    for folder,filename,proof,verifier in [
        ('central_integrality','general_galois_pu_gate.json','GENERAL_GALOIS_PU.md','general_galois_pu_gate.py'),
        ('noncommutative_followup','scope_gates.json','README.md','verify_scope_gates.py'),
        ('noncommutative_followup','additional_scope_gates.json','ADDITIONAL_SCOPE_GATES.md','additional_scope_gates.py')]:
        directory=FRONTIER/folder;path=directory/filename
        for r in read(path):
            require(r['tensor_sha256']==rows[r['id']]['tensor_sha256'],'NC Galois reduction binding')
            general_nc.add(r['id'])
            add(r['id'],'complete_signed_sphericalization_and_general_Galois_PU_reduction',r['outcome'],
                r['scope'],path,directory/proof,[directory/verifier],
                {k:r[k]for k in ('complete_signed_count','normalized_indicator_domains_used','conclusion')if k in r},
                'This proves a scope reduction, not categorifiability or unitarity. Necessary PU constraints apply after Galois conjugation.')
    def nc_scope(ident):
        return 'general_complex_necessary_after_proved_Galois_PU_reduction'if ident in general_nc else'pseudo_unitary_only'
    directory=FRONTIER/'noncommutative_followup';path=directory/'su2_all_frontier.json'
    for r in read(path)['records']:
        require(r['tensor_sha256']==rows[r['id']]['tensor_sha256'],'SU2 family source binding')
        add(r['id'],'all_levels_SU2_adjoint_finite_products_integer_multiplier_chains_and_Morita_duals',r['outcome'],
            'general_complex_construction_family_dimension_obstruction',path,directory/'SU2_FAMILY.md',
            [directory/'su2_all_frontier.py',directory/'su2_product_family.py'],
            {key:r[key]for key in ('complete_order_candidates','allowed_order_sequence','exponent_box_size',
                'dimension_bounded_product_count','positive_integer_scaling_matches')},r['not_covered'])
    path=directory/'generalized_near_group_all_frontier.json'
    for r in read(path)['records']:
        require(r['tensor_sha256']==rows[r['id']]['tensor_sha256'],'generalized NG source binding')
        add(r['id'],'all_generalized_near_group_dimension_parameters_with_integer_scalings',r['outcome'],
            r['scope'],path,directory/'GENERALIZED_NEAR_GROUP_TABLE.md',
            [directory/'generalized_near_group_all_frontier.py'],r,
            'This is a necessary dimension-family test; retained parameter triples are not categories, and integral targets lie outside its irrational quadratic parameter theorem.')
    path=directory/'additional_central_constraints.json'
    for r in read(path):
        require(r['tensor_sha256']==rows[r['id']]['tensor_sha256'],'additional central source binding')
        add(r['id'],'complete_central_image_and_full_character_S_assignments',r['outcome'],
            nc_scope(r['id']),path,directory/'ADDITIONAL_SCOPE_GATES.md',
            [directory/'additional_central_constraints.py'],
            {key:r[key]for key in ('low_count','ordinary_surviving_count','full_S_surviving_count','splitting_field_extension_by_i_used')},
            'The retained full-S assignments and necessary induction frames are not modular categories or categorifications.')
    path=directory/'additional_joint_rotation_h6.json'
    for r in read(path):
        require(r['tensor_sha256']==rows[r['id']]['tensor_sha256'],'additional joint rotation binding')
        decisions=[case['decision']['status']for case in r['cases']]
        add(r['id'],'all_indicator_branches_joint_height6_rotations_on_unique_full_S_frame',
            'one_exact_necessary_indicator_branch_survives',nc_scope(r['id']),path,
            directory/'ADDITIONAL_SCOPE_GATES.md',[directory/'additional_joint_rotation.py'],
            {'height':r['height'],'complete_branch_count':len(r['cases']),
             'exact_negative_count':decisions.count('exact_infeasible_relaxation'),
             'exact_primal_count':decisions.count('exact_feasible_relaxation'),
             'surviving_indicators':[case['indicators']for case in r['cases']if case['decision']['status']=='exact_feasible_relaxation']},
            'This determines necessary pointed-cocycle signs through the separate structural bridge; the surviving exact primal is not a model.')

    n = FRONTIER/'noncommutative'
    data = read(n/'central_support_results.json')
    for r in data:
        ident = r['id']
        require(r['tensor_sha256'] == rows[ident]['tensor_sha256'], 'NC source binding')
        add(ident,'complete_central_image_low_induction_and_Gram_moment_constraints','necessary_data_survives',
            nc_scope(ident),n/'central_support_results.json',n/'README.md',
            [n/'verify_all.py',n/'verify_independent.py'],
            {'low_count':r['low_count'],'passing_low_count':r['passing_low_count']},
            'This PU necessary-condition test applies after the separately proved Galois reduction; surviving data need not lift to a center.')
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
                nc_scope(r['id']),path,n/'README.md',[n/'verify_all.py'],
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
        add(r['id'],domain,'exact_necessary_data_survives',nc_scope(r['id']),path,
            n/'README.md',[n/'verify_all.py'],details,
            r.get('conclusion','Necessary central data survives; full integer fusion and associator coherence are not constructed.'))

    directory=FRONTIER/'central_integrality';path=directory/'fixed_gram_rotation_1154_h6.json'
    fixed=read(path);meta=fixed['metadata'];ident=meta['id']
    require(meta['tensor_sha256']==rows[ident]['tensor_sha256'],'fixed Gram1154 source binding')
    add(ident,'all_1238_cubic_surviving_integer_Gram_patterns_joint_height6_rotation_and_STS',
        'complete_exact_necessary_data_survives',nc_scope(ident),path,directory/'RESEARCH_RECORD.md',
        [directory/'fixed_gram_rotation_1154.py'],
        {'height':meta['height'],'complete':fixed['complete'],
         'pattern_count':len(meta['pattern_indices']),'certificate_family_count':len(fixed['cases']),
         'unresolved_indices':fixed['unresolved_indices']},
        'This finite-height exact system leaves feasible patterns; neither full center fusion nor associators are constructed.')

    g = FRONTIER/'global_induction'
    global_domains={
        'results':('PROOF.md','column_generation.py'),
        'frame_results':('PROOF.md','frame_generation.py'),
        'fixed_results':('PROOF.md','fixed_frame.py'),
        'spectral_results':('PARTIAL_S_AND_STS.md','spectral_generation.py'),
        'sts_results':('PARTIAL_S_AND_STS.md','sts_generation.py'),
        'generic_results':('LOW_S_SYMMETRY.md','generic_generation.py'),
        'atomic_results':('ATOMIC_MODULAR.md','atomic_generation.py'),
        'atomic_spectrum_results':('ATOMIC_SPECTRUM.md','atomic_spectrum_generation.py'),
        'complete_results':('PROOF.md','complete_phase_one.py')}
    for folder,(proof,verifier)in global_domains.items():
        pattern=folder+'/*.json'
        for path in sorted(g.glob(pattern)):
            r = read(path)
            if r.get('id') not in rows:
                continue
            require(r['tensor_sha256'] == rows[r['id']]['tensor_sha256'], 'global induction source binding')
            meta = r.get('metadata',{})
            specific_verifier='verify_accepted_generic.py'if path.name.endswith('_low_s.json')else verifier
            add(r['id'],r.get('method','fixed_integral_low_frame_global_induction'),r.get('status','see_receipt'),
                r.get('scope')or'incomplete_no_mathematical_conclusion',path,g/proof,
                [g/specific_verifier],
                {'height':r.get('height'),'frame_index':r.get('frame_index'),
                 'rows':meta.get('rows'),'variables':meta.get('variables'),
                 'low_frames':meta.get('low_frames'),'high_columns':meta.get('high_columns'),
                 'complete_exact_certificate':r.get('status')in('excluded','exact_feasible_relaxation','this_frame_indicator_excluded')and'certificate'in r},
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

    # Mathematical status is controlled exclusively by the parent's accepted
    # ledger. Screening completion is an explicit reviewed campaign decision,
    # never inferred from an attempt counter or a feasible cone.
    completion=HERE/'screening_completion.json'
    if use_screening and completion.exists():
        assessment=read(completion)
        queue_path,_=completed_queue();reference(queue_path)
        require(assessment['completion_queue_sha256']==digest(queue_path),
                'completion queue differs from the explicit screening assessment')
        remaining={ident for ident,row in rows.items()if row['general_status']=='unresolved'}
        require({r['id']for r in assessment['records']}==remaining,'screening decision predates the current accepted ledger; explicitly refresh it')
        require(assessment['definition']==SCREENING_DEFINITION,'screening definition changed')
        for item in assessment['records']:
            row=rows[item['id']];number=int(item['id'].rsplit('_',1)[1])
            require(item['tensor_sha256']==row['tensor_sha256']and item['case_specific_focus']==SCREENING_FOCUS[number],
                    'screening assessment source or case focus changed')
            row['screening_stage']='extensively_investigated_exotic_candidate'
            row['screening_case_specific_focus']=item['case_specific_focus']
            row['screening_definition']=SCREENING_DEFINITION
    ordered = [rows[f'R8_3_{i}'] for i in IDS]
    return {'schema':'rank8-frontier-per-ring-research-audit/v1',
            'scope':'research coverage and source binding; linked proof verifiers provide mathematical replay',
            'research_status':accepted.get('research_status','ongoing'),
            'baseline_ring_count':34,
            'accepted_general_exclusions':sum(r['general_status']=='excluded' for r in ordered),
            'candidate_terminology':'After completed extensive known/new exclusion and construction screening, a remaining ring may be called an extensively investigated exotic candidate in the user-defined sense; categorifiability and novelty remain unproved.',
            'rows':ordered,'artifact_sha256':dict(sorted(manifest.items()))}


def markdown(data):
    lines=['# Frontier research coverage for the original 34 rings','',
           'This index separates accepted general exclusions, restricted construction obstructions,',
           'exact survival of necessary conditions, and unfinished computations. No remaining ring',
           'is asserted categorifiable or novel from survival. After extensive completed screening,',
           'the user-defined label exotic candidate describes that research status. The JSON retains',
           'the prior published attempts and the exact domain, scope, evidence, verifier and',
           'limitation of every new attempt. Numerical undecided results are not proofs.','',
           '| Ring | Current general status | Screening stage | New domains and outcomes |',
           '|---|---|---|---|']
    for row in data['rows']:
        summary='; '.join(a['domain'].replace('_',' ')+': '+a['outcome'].replace('_',' ')
                         for a in row['new_attempts'])
        lines.append('| '+row['id']+' | '+row['general_status']+' | '+row['screening_stage'].replace('_',' ')+' | '+summary.replace('|','/')+' |')
    if any(r['screening_stage']=='extensively_investigated_exotic_candidate'for r in data['rows']):
        lines+=['',SCREENING_DEFINITION,'']
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
    parser.add_argument('--mark-screening-complete',action='store_true',
        help='Explicit final campaign assessment after all planned exact queues finish; requires --write. Never changes a categorification status.')
    args=parser.parse_args()
    require(not args.mark_screening_complete or args.write,'screening completion requires explicit --write')
    actual=record(use_screening=not args.mark_screening_complete)
    if args.mark_screening_complete:
        queue_path,_=completed_queue()
        running=[(row['id'],attempt['domain'])for row in actual['rows']for attempt in row['new_attempts']
                 if attempt['outcome']in ACTIVE_STATES]
        require(not running,'planned exact research is still running; finish or explicitly close its receipt before final screening')
        items=[]
        for row in actual['rows']:
            if row['general_status']!='unresolved':continue
            number=int(row['id'].rsplit('_',1)[1]);require(number in SCREENING_FOCUS,'remaining ring lacks case-specific assessment')
            items.append({'id':row['id'],'tensor_sha256':row['tensor_sha256'],
                          'case_specific_focus':SCREENING_FOCUS[number],
                          'categorification_or_novelty_proved':False})
        (HERE/'screening_completion.json').write_text(json.dumps({'kind':'explicit_final_extensive_screening_assessment',
            'definition':SCREENING_DEFINITION,
            'completion_queue_path':str(queue_path.relative_to(REPO)),
            'completion_queue_sha256':digest(queue_path),'records':items},indent=2)+'\n')
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
    print(f"PASS:34 source-bound research rows; {actual['accepted_general_exclusions']} accepted general exclusions; candidate screening distinguished from existence or novelty.")


if __name__=='__main__':
    main()
