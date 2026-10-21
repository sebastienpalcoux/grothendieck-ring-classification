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
65:'Free C4 generalized-near-group structure; complete rank-two based-module and connected-algebra underlying-object necessary filters; all nontrivial group-equivariantizations and the specified integer-scaling/Morita routes from standard Haagerup-Izumi sources excluded; full character-field, CM-real STS, joint integer central constraints and exact global phase cuts tested, with subsequent bounded integer search inconclusive.',
721:'All six known Asaeda-Haagerup Morita categories compared; all integer-scaled near-group sources and all-level SU(2)/adjoint families excluded; complete integer central Gram domain, rotation/STS/cubic/forgetful constraints and connected-algebra underlying-object necessary filters tested.',
928:'General Galois-PU reduction and quaternionic rational block; complete joint integer Gram/cubic domain forces a central semion, leaving 15 parity patterns and ten exact correlated height-six moment witnesses; four exact integer witnesses and six explicitly unresolved bounded integer attempts; connected-algebra underlying-object filters and specified unbounded model families tested.',
941:'General Galois-PU reduction; complete joint integer Gram/cubic domain forces a central fermion after the ordinary rank-four quotient excludes the bosonic branch; 93 complete charge allocations give 77 exact correlated-cone exclusions; the final permutation and mixed-fusion-trace filter retains fourteen moment witnesses, eleven with exact integer counts and three unresolved bounded integer attempts; superproduct and specified unbounded model routes tested.',
982:'Complete connected-algebra underlying-object filters and all four labeled central-induction frames tested; all four pass signed lattice membership, two selected integer witnesses fail every allowed fixed-mass phase branch, and the other two frames have exact bounded rational witnesses; specified unbounded model families excluded, while other integer patterns remain unresolved.',
1154:'General Galois-PU reduction; all 14,211 integer central Gram patterns filtered to 1,238 cubic/spectral survivors and 1,230 exact joint rotation/STS survivors; complete connected-algebra underlying-object necessary filters and specified unbounded model families tested.',
1768:'Complete rank-two based-module and connected-algebra underlying-object necessary filters; every proper subring, grading and nontrivial group-equivariantization tested; joint integer Gram/S/cubic/Galois and source-unit constraints pass signed lattice membership without a bounded nonnegative integer witness; specified unbounded construction families tested.',
1795:'Complete rank-two based-module and connected-algebra underlying-object filters; all proper subrings, gradings and group-equivariantization routes tested; strengthened integer central equations pass exact box and mod2/mod3 checks, while capped Hermite work determines no integer-lattice status and bounded search yields no exact integer witness; specified unbounded model families tested.',
3472:'Complete rank-two based-module and connected-algebra underlying-object filters; all proper subrings, gradings and group-equivariantization routes tested; full-character spectral support, joint Galois balance and strengthened integer equations pass the recorded exact box/modular screens, with bounded integer search inconclusive and no claim of exhausting larger-field STS.'}
SCREENING_DEFINITION = ('Extensively investigated exotic candidate means that the ring survived the documented, case-specific campaign of known and newly developed exclusion tests and explicit model searches, including complete finite domains and specified unbounded construction families. It proves neither existence of a fusion category nor novelty of a future realization. Each case lists exactly what was exhausted, what survived and the remaining hypotheses.')
ACTIVE_STATES={'running','queued','discovery_in_progress','constructing_complete_domain',
               'solving_complete_sparse_cone','pseudo_certificate_verified','pending',
               'hermite_running','integer_domain_building','awaiting_independent_review'}


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


def completed_final_domains():
    """Require every explicitly planned late finite campaign to be closed."""
    paths=[]
    path=FRONTIER/'commutative_integer/final_campaign.json'
    require(path.is_file(),'the late five-case integer campaign ledger is missing')
    ledger=json.loads(path.read_text());paths.append(path)
    require(ledger.get('status')=='all_planned_integer_attempts_finished',
            'the late five-case integer campaign remains active')
    expected={f'R8_3_{i}'for i in(65,982,1768,1795,3472)}
    require(set(ledger.get('planned_ids',[]))==expected and
            {r['id']for r in ledger.get('records',[])}==expected,
            'the late integer campaign does not cover its five planned cases')
    require(all(r.get('status')and r['status']not in ACTIVE_STATES for r in ledger['records']),
            'a late integer attempt is still active')
    for relative,sha in ledger.get('dependencies_sha256',{}).items():
        dependency=FRONTIER/relative
        require(dependency.is_file()and digest(dependency)==sha,'late commutative integer dependency changed')
    path=FRONTIER/'r928_semion_rotation/final_campaign.json'
    require(path.is_file(),'the late noncommutative moment and joint-spectrum ledger is missing')
    nc=json.loads(path.read_text());paths.append(path)
    require(nc.get('status')=='all_planned_semion_attempts_finished'and nc.get('pending_attempts')==[],
            'a planned noncommutative moment or joint-spectrum attempt remains active')
    require(set(nc.get('planned_ids',[]))=={f'R8_3_{i}'for i in(721,928,941,1154)},
            'the late noncommutative ledger omits a planned joint-spectrum target')
    for relative,sha in nc.get('dependencies_sha256',{}).items():
        dependency=FRONTIER/relative
        require(dependency.is_file()and digest(dependency)==sha,'late noncommutative campaign dependency changed')
    path=FRONTIER/'quartic_integer_center/r941_integer_counts.json'
    require(path.is_file(),'the planned sixteen-case fermionic integer stage is unfinished')
    integer=json.loads(path.read_text());paths.append(path)
    require(integer.get('status')=='all_planned_integer_count_attempts_finished'and len(integer.get('cases',[]))==16,
            'the fermionic integer stage does not account for all sixteen surviving cones')
    require(all(case.get('result',{}).get('status')in('exact_nonnegative_integer_witness',
            'exact_supported_integer_lattice_obstruction','integer_feasibility_unresolved')for case in integer['cases']),
            'a planned fermionic integer attempt is still active')
    path=FRONTIER/'review/r941_fusion_traces.json'
    require(path.is_file(),'the final fermionic permutation and fusion-trace gate is unfinished')
    trace= json.loads(path.read_text());paths.append(path)
    require(trace.get('status')=='exact_complete'and trace.get('complete_charge_allocation_count')==93
            and trace.get('mixed_traces_per_allocation')==420 and len(trace.get('cases',[]))==93,
            'the final fermionic trace gate does not cover its complete planned domain')
    for relative,sha in trace.get('files_sha256',{}).items():
        dependency=REPO/relative
        require(dependency.is_file()and digest(dependency)==sha,'final fermionic trace dependency changed')
    for relative,count in [('quartic_integer_center/r941_paired_rotation.json',93),
                           ('r928_semion_rotation/results.json',15),
                           ('r928_semion_rotation/pair_rotation.json',10),
                           ('r455_center_integer/joint_rotation.json',48)]:
        path=FRONTIER/relative;require(path.is_file(),f'planned finite center test missing: {relative}')
        data=json.loads(path.read_text());paths.append(path)
        require(len(data.get('cases',[]))==count,'planned late finite center domain incomplete')
        require(all(case.get('decision',{}).get('status')in
                    ('exact_feasible_relaxation','exact_infeasible_relaxation')for case in data['cases']),
                'a planned late finite center case lacks an exact terminal decision')
    return paths


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

    directory=FRONTIER/'review';path=directory/'integral_center_subcategory.json'
    for r in read(path)['records']:
        if r['id']not in rows:continue
        require(r['tensor_sha256']==rows[r['id']]['tensor_sha256'],'integral center source binding')
        add(r['id'],'complete_integral_center_subcategory_divisibility_and_solvability',
            'all_nonunit_integral_dimensional_center_simples_excluded',
            'general_complex_necessary_center_structure',path,directory/'INTEGRAL_CENTER_SUBCATEGORY.md',
            [directory/'integral_center_subcategory.py'],r,
            'This structural theorem is not alone a categorification exclusion; it also applies to the specified R439 Morita dual, not to every category with its positive rank-five based ring.')
    directory=FRONTIER/'integral_center_filter'
    for number in (439,567):
        path=directory/f'R8_3_{number}_h6.json';r=read(path);meta=r['metadata'];ident=meta['id']
        require(meta['tensor_sha256']==rows[ident]['tensor_sha256'],'integral center rotation source binding')
        decisions=[case['decision']['status']for case in r['cases']]
        add(ident,'all_eight_indicator_branches_height6_rotation_without_integral_center_simples',
            'one_exact_necessary_indicator_branch_survives',nc_scope(ident),path,directory/'README.md',
            [directory/'verify_original.py'],
            {'high_column_count':len(meta['high_columns']),
             'forbidden_integral_indices':meta['forbidden_integral_indices'],
             'branch_count':len(decisions),'exact_negative_count':decisions.count('exact_infeasible_relaxation'),
             'exact_primal_count':decisions.count('exact_feasible_relaxation')},
            'The exact surviving primal is a necessary relaxation; the subsequent integer Gram and cubic tests strengthen it.')
    directory=FRONTIER/'rank5_integer_gram';path=directory/'results.json';r=read(path)
    add('R8_3_439','complete_integer_central_Gram_domain_of_forced_rank5_Morita_dual',
        '58_exact_integer_Gram_patterns_survive','general_complex_necessary_after_Galois_and_Morita_reductions',
        path,directory/'PROOF.md',[directory/'verify.py'],
        {'rank5_tensor_sha256':r['rank5_tensor_sha256'],'low_frame_index':r['low_frame_index'],
         'high_vector_count':len(r['high_vectors']),'forbidden_integral_indices':r['rational_dimension_forbidden_indices'],
         'spectral_forbidden_indices':r['spectral_forbidden_indices'],'enumeration':r['enumeration'],
         'complete_integer_Gram_pattern_count':r['solution_count']},
        'The two complete integer enumerations certify necessary multiplicities; all58 are tested by the subsequent cubic exclusion.')
    path=directory/'positive_control.json';r=read(path)
    add('R8_3_439','integral_columns_restored_rank5_Gram_and_all_twenty_low_cubic_control',
        'exact_necessary_data_control_passes','arithmetic_positive_control_for_essential_integral_center_filter',
        path,directory/'PROOF.md',[directory/'positive_control.py'],
        {key:r[key]for key in ('complete_integer_control_domain_count','selected_pattern_index',
                             'nonunit_integral_high_indices','cubic_values')},r['scope'])
    directory=FRONTIER/'r439_centerless_rank5';path=directory/'verlinde_exclusion.json';r=read(path)
    add('R8_3_439','all_58_forced_rank5_integer_Gram_patterns_distinguished_cubic_Verlinde_coefficient',
        'accepted_general_exclusion'if'R8_3_439'in accepted_ids else'proposed_general_exclusion_pending_review',
        r['scope'],path,directory/'PROOF.md',[directory/'verlinde_exclusion.py'],
        {key:r[key]for key in ('integer_Gram_pattern_count','coefficient_histogram','known_model_control')},
        'General status is supplied only by the reviewed accepted ledger; the cubic normalization has a known Fibonacci-center control as well as the separate restored-integral-column control.')
    directory=FRONTIER/'r567_centerless_integer';source_domain=read(directory/'source.json')
    require(source_domain['tensor_sha256']==rows['R8_3_567']['tensor_sha256'],'R567 full character source binding')
    path=directory/'rotation_spectral.json'
    if path.exists():
        r=read(path);statuses=[case['decision']['status']for case in r['cases']]
        add('R8_3_567','joint_height6_rotation_with_full_complex_partial_S_integrality_and_no_integral_center',
            '; '.join(sorted(set(statuses))),nc_scope('R8_3_567'),path,directory/'GRAM_PROOF.md',
            [directory/'rotation_spectral.py',directory/'source.py'],
            {'complete_high_vector_count':len(source_domain['high_vectors']),
             'integral_forbidden_indices':source_domain['integral_forbidden_indices'],
             'spectral_forbidden_indices':[r['index']for r in source_domain['spectral_exclusions']],
             'branch_statuses':statuses},
            'This rational relaxation remains feasible; the subsequent complete integer Gram and cubic tests are stronger.')
    path=directory/'gram.json';r=read(path)
    require(r['tensor_sha256']==rows[r['id']]['tensor_sha256'],'R567 integer-Gram source binding')
    add(r['id'],'complete_original_R567_integer_central_Gram_and_duality_domain',
        '155_duality_compatible_necessary_patterns_survive',nc_scope(r['id']),path,directory/'GRAM_PROOF.md',
        [directory/'source.py',directory/'gram.py'],
        {key:r[key]for key in ('low_index','integer_Gram_count','duality_compatible_count','enumeration')},
        'Two complete integer enumerations agree on1071 Grams before duality;155 remain for subsequent cubic tests, without a center construction.')
    path=directory/'verlinde_exclusion.json'
    if path.exists():
        r=read(path)
        require(r['tensor_sha256']==rows['R8_3_567']['tensor_sha256'],'R567 cubic source binding')
        add('R8_3_567','all_155_duality_compatible_integer_Gram_patterns_distinguished_cubic_Verlinde_coefficient',
            'accepted_general_exclusion'if'R8_3_567'in accepted_ids else'proposed_general_exclusion_pending_review',
            'general_complex_after_reviewed_Galois_PU_reduction_and_integral_center_theorem',
            path,directory/'PROOF.md',[directory/'verlinde_exclusion.py'],
            {key:r[key]for key in ('complete_integer_Gram_count','complete_duality_compatible_count',
                                 'coefficient_histogram','actual_known_model_control')if key in r},
            'The accepted ledger alone controls the general status; complete integer domains and exact cubic values are separately replayed.')

    directory=FRONTIER/'r455_center_integer';path=directory/'results.json';r=read(path)
    require(r['source']['tensor_sha256']==rows['R8_3_455']['tensor_sha256'],'R455 integer-center source binding')
    add('R8_3_455','complete_integer_Gram_twenty_low_cubic_and_Galois_center_domain',
        '12_necessary_integer_patterns_survive_before_joint_rotations',nc_scope('R8_3_455'),path,
        directory/'PROOF.md',[directory/'verify.py'],
        {'complete_integer_Gram_count':r['integer_Gram_count'],'enumeration':r['enumeration'],
         'cubic_survivor_count':len(r['cubic_survivors']),'all_filter_survivor_count':len(r['all_tests_survivors'])},
        'These twelve necessary patterns are all excluded by the subsequent complete joint rotation domain.')
    path=directory/'joint_rotation.json';r=read(path)
    add('R8_3_455','all_48_integer_pattern_and_indicator_branches_joint_height6_rotation_STS',
        'accepted_general_exclusion'if'R8_3_455'in accepted_ids else'proposed_general_exclusion_pending_review',
        nc_scope('R8_3_455'),path,directory/'PROOF.md',[directory/'verify_all.py'],
        {'complete_branch_count':len(r['cases']),'all_patterns_excluded':r['all_patterns_excluded'],
         'actual_known_center_and_trace_controls':r['controls']},
        'General status follows the separately reviewed accepted ledger and exact full trace-domain completeness.')

    directory=FRONTIER/'quartic_integer_center';path=directory/'gram_cubic.json';r=read(path)
    for binding in r['source_bindings']:
        ident=binding['id'];require(binding['tensor_sha256']==rows[ident]['tensor_sha256'],'quartic integer source binding')
        add(ident,'complete_integer_Gram_and_all_twenty_distinguished_cubic_coefficients',
            '343_exact_necessary_integer_patterns_survive',nc_scope(ident),[path,directory/'source.json'],
            directory/'PROOF.md',[directory/'source.py',directory/'gram_cubic.py'],
            {'complete_joint_pattern_count':r['complete_joint_pattern_count'],
             'native_search_nodes':r['search_nodes'],'independent_Python_nodes':r['independent_Python_nodes']},
            'All343 patterns are necessary center data; their existence does not construct a modular category.')
        add(ident,'forced_order_two_central_lift_and_complete_tensor_orbit_graph',
            'central_invertible_forced_in_all_integer_patterns',nc_scope(ident),
            FRONTIER/'review/quartic_central_orbits.json',FRONTIER/'review/QUARTIC_CENTRAL_ORBITS.md',
            [FRONTIER/'review/verify_quartic_central_orbits.py'],
            {'source_invertible_index':7 if ident.endswith('_928')else 3,
             'forced_low_translate_high_indices':[40,41,42,43,57]},
            'A central lift does not imply a tensor-factor decomposition of the nonbraided source category.')
    path=directory/'r941_fermionic.json';r=read(path)
    add('R8_3_941','complete_bosonic_central_lift_quotient_and_fermionic_alternative',
        'bosonic_branch_excluded_fermionic_lift_forced',nc_scope('R8_3_941'),path,
        directory/'R941_FERMION.md',[directory/'r941_fermionic.py'],r,
        'The ordinary rank-four bound applies only to the Tannakian branch; no ordinary rank-four classification is imposed on a fermionic quotient.')
    path=directory/'r941_charges.json'
    if path.exists():
        r=read(path)
        add('R8_3_941','complete_integer_fermion_monodromy_charge_allocations',
            'exact_charge_allocations_survive',nc_scope('R8_3_941'),path,directory/'R941_FERMION.md',
            [directory/'r941_charges.py'],
            {key:r[key]for key in('input_Gram_cubic_patterns','surviving_pattern_count','complete_charge_allocation_count',
                                 'rref_assignments_tested','independent_full_box_assignments_tested')},
            'A surviving charge allocation fixes necessary eigenvalue multiplicities only; it is not a center or associator.')
    path=directory/'r941_super_constructions.json'
    if path.exists():
        r=read(path)
        add('R8_3_941','all_direct_rank_two_super_products_and_specified_published_near_group_center_routes',
            'specified_super_construction_families_excluded','general_complex_scoped_construction_obstructions',path,
            directory/'R941_FERMION.md',[directory/'r941_super_constructions.py'],r,r['limitation'])
    path=directory/'r941_paired_rotation.json'
    if path.exists():
        r=read(path);statuses=[v['decision']['status']for v in r['cases']]
        add('R8_3_941','all_fermion_charge_allocations_correlated_height6_rotation_STS_and_fermion_S_row',
            '; '.join(sorted(set(statuses))),nc_scope('R8_3_941'),
            [path,FRONTIER/'review/r941_fermion_operator_review.json',
             FRONTIER/'review/r941_fermion_campaign_review.json'],directory/'R941_FERMION.md',
            [directory/'r941_paired_rotation.py',FRONTIER/'review/verify_r941_fermion_operator.py',
             FRONTIER/'review/verify_r941_fermion_campaign.py'],
            {key:r[key]for key in('complete_charge_allocation_count','input_integer_pattern_count',
                                 'charge_surviving_pattern_count','exact_excluded_count','exact_feasible_count')},
            'The complete finite correlated cone is necessary data and does not classify superfusion associators.')
    path=directory/'r941_integer_counts.json'
    if path.exists():
        r=read(path)
        add('R8_3_941','all_sixteen_surviving_correlated_fermion_cones_supported_modular_and_bounded_integer_attempts',
            'finite_attempts_finished_with_exact_witnesses_or_explicit_unresolved_integer_feasibility',
            nc_scope('R8_3_941'),[path,FRONTIER/'review/r941_integer_witness_review.json'],
            directory/'R941_FERMION.md',[directory/'r941_integer_counts.py',
             FRONTIER/'review/verify_r941_integer_witnesses.py'],
            {key:r[key]for key in('status','planned_allocation_indices','exact_integer_witness_count',
                                 'exact_modular_exclusion_count','unresolved_integer_feasibility_count')},r['scope'])
    path=FRONTIER/'review/r941_fusion_traces.json'
    if path.exists():
        r=read(path)
        for relative,sha in r['files_sha256'].items():
            dependency=REPO/relative
            require(digest(dependency)==sha,'fermionic trace source binding');reference(dependency)
        add('R8_3_941','complete_involutive_permutation_fixed_point_bounds_and_420_mixed_fusion_traces_per_charge_allocation',
            'fourteen_correlated_survivors_eleven_integer_witnesses_three_unresolved_integer_cases',
            nc_scope('R8_3_941'),path,FRONTIER/'review/R941_FUSION_TRACE_REVIEW.md',
            [FRONTIER/'review/verify_r941_fusion_traces.py'],
            {key:r[key]for key in('status','complete_charge_allocation_count','mixed_traces_per_allocation',
                                 'actual_center_control','paired_surviving_allocations','paired_allocations_removed',
                                 'retained_exact_integer_witness_allocations','retained_integer_feasibility_unresolved')},
            'This final finite necessary-condition gate removes two earlier witnesses; fourteen moment systems remain, with no categorical construction implied.')
    add('R8_3_941','proposed_negative_scalar_character_obstruction_for_a_central_fermion',
        'universal_implication_refuted_by_an_actual_unitary_pointed_counterexample',
        'scoped_obstruction_validation',FRONTIER/'review/fermion_no_negative_character.json',
        FRONTIER/'review/FERMION_DIMENSION_CHARACTER_COUNTEREXAMPLE.md',
        [FRONTIER/'review/fermion_no_negative_character.py'],
        {'counterexample':'explicit unitary Vec^omega(Q8) with a freely acting central fermion but every scalar character positive on its source label'},
        'This counterexample rejects an invalid universal implication; it neither constructs nor excludes R941.')
    directory=FRONTIER/'r928_semion_rotation'
    for filename,domain,verifier in [('results.json','all_semion_parity_patterns_with_fixed_even_twist_moments','verify.py'),
                                   ('pair_rotation.json','complete_correlated_semion_pair_twist_cones','pair_rotation.py')]:
        path=directory/filename
        if not path.exists():continue
        r=read(path);statuses=[v['decision']['status']for v in r['cases']]
        add('R8_3_928',domain,'; '.join(sorted(set(statuses))),nc_scope('R8_3_928'),path,
            FRONTIER/'review/QUARTIC_CENTRAL_ORBITS.md',[directory/verifier],
            {'complete_case_count':len(r['cases']),'exact_infeasible_count':statuses.count('exact_infeasible_relaxation'),
             'exact_feasible_count':statuses.count('exact_feasible_relaxation')},
            'These are finite necessary moment systems; exact primal survival is not a semionic construction.')
    path=directory/'final_campaign.json'
    if path.exists():
        r=read(path)
        for relative in r['dependencies_sha256']:reference(FRONTIER/relative)
        for item in r['records']:
            ident=item['id']
            add(ident,'latest_complete_joint_Galois_spectra_and_correlated_semion_integer_attempts',
                'documented_finite_domains_finished',nc_scope(ident),path,
                FRONTIER/'review/QUARTIC_CENTRAL_ORBITS.md',
                [FRONTIER/v for v in r['canonical_no_argument_verifiers']],item,
                'Six bounded R928 integer searches remain unresolved integer-feasibility problems; numerical negative solver outcomes are not exclusions. Exact positive integer witnesses are necessary data only.')

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
            specific_proof=g/proof
            if r.get('variant')=='cm_real_sts':
                specific_proof=q/'CM_REAL_STS.md'
                reference(q/'atomic_cm_real_sts.py')
                reference(q/'review_cm_real_sts.py')
                reference(q/'review_cm_real_sts_results.json')
            add(r['id'],r.get('method','fixed_integral_low_frame_global_induction'),r.get('status','see_receipt'),
                r.get('scope')or'incomplete_no_mathematical_conclusion',path,specific_proof,
                [g/specific_verifier],
                {'height':r.get('height'),'variant':r.get('variant'),'frame_index':r.get('frame_index'),
                 'rows':meta.get('rows'),'variables':meta.get('variables'),
                 'low_frames':meta.get('low_frames'),'high_columns':meta.get('high_columns'),
                 'complete_exact_certificate':r.get('status')in('excluded','exact_feasible_relaxation','this_frame_indicator_excluded')and'certificate'in r},
                'A running/partial computation is incomplete; a feasible relaxation does not construct integer center data or an associator.')

    directory=FRONTIER/'commutative_integer';path=directory/'final_campaign.json'
    if path.exists():
        data=read(path)
        require(data.get('status')=='all_planned_integer_attempts_finished',
                'the final five-case integer ledger is not terminal')
        for relative,sha in data['dependencies_sha256'].items():
            dependency=FRONTIER/relative
            require(digest(dependency)==sha,'final commutative integer source binding');reference(dependency)
        for item in data['records']:
            ident=item['id'];require(item['tensor_sha256']==rows[ident]['tensor_sha256'],
                                   'final integer target source binding')
            verifier_paths=sorted({command[0]for command in item['exact_replay']})
            add(ident,'final_joint_integer_Gram_full_S_cubic_Galois_bounds_unit_product_and_scoped_phase_screen',
                item['status'],'necessary_center_data_scoped_by_each_source_receipt',
                [path]+[FRONTIER/relative for relative in item['evidence']],directory/'PROOF.md',
                [directory/'verify_research.py']+[FRONTIER/relative for relative in verifier_paths],
                {key:item[key]for key in('completed_scope','exact_replay')},item['limitation'])

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
        final_paths=completed_final_domains()
        final_bindings={reference(p):digest(p)for p in final_paths}
        require(assessment.get('late_campaign_dependencies')==final_bindings,
                'a planned late finite campaign is unfinished or changed after screening')
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
        require(actual['research_status']=='completed_scoped_campaign',
                'the accepted ledger has not declared the scoped campaign complete')
        queue_path,_=completed_queue()
        final_paths=completed_final_domains()
        running=[(row['id'],attempt['domain'])for row in actual['rows']for attempt in row['new_attempts']
                 if attempt['outcome']in ACTIVE_STATES or attempt['outcome']=='proposed_general_exclusion_pending_review']
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
            'completion_queue_sha256':digest(queue_path),
            'late_campaign_dependencies':{str(p.relative_to(REPO)):digest(p)for p in final_paths},
            'records':items},indent=2)+'\n')
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
