"""Generate manuscript tables from the frozen, machine-replayed JSON ledger."""
import json
from pathlib import Path

HERE=Path(__file__).resolve()
if HERE.parent.name == 'papers':
    ROOT=HERE.parents[1]
    PAPERS=HERE.parent
else:
    REPO=HERE.parents[1]
    ROOT=REPO/'supplements/rank7'
    PAPERS=REPO/'manuscripts/rank7/papers'
summary=json.loads((ROOT/'output/rank7_summary.json').read_text())
catalog=json.loads((ROOT/'data/model_catalog.json').read_text())

def esc(v):
    return str(v).replace('\\','\\textbackslash{}').replace('_','\\_')

max_m = summary['max_multiplicity']
bound_word = {4: 'four', 5: 'five'}.get(max_m, str(max_m))
complete=not any(c.get('unresolved',0) for c in summary['status_counts'].values())
status_caption=(f'Complete classification of the supplied rank-seven fusion-ring census through exact multiplicity {bound_word}.' if complete else f'Status of the supplied rank-seven fusion-ring census through exact multiplicity {bound_word}. Undecided entries are not assumed categorifiable.')
lines=[r'\begin{table}[H]',r'\centering',
       r'\caption{'+status_caption+r'}\label{tab:status}',
       r'\begin{tabular}{@{}r r r r r@{}}',r'\toprule',
       r'Exact multiplicity & Fusion rings & Excluded & Realized & Undecided\\',r'\midrule']
for m in range(1,summary['max_multiplicity']+1):
    c=summary['status_counts'][str(m)]
    lines.append(f"{m} & {summary['ring_counts'][str(m)]} & {c.get('excluded',0)} & {c.get('unitarily_realized',0)} & {c.get('unresolved',0)}"+r'\\')
stage_header='Criterion & ' + ' & '.join(f'$m={m}$' for m in range(1,max_m+1)) + r'\\'
lines.extend([r'\bottomrule',r'\end{tabular}',r'\end{table}','',
              r'{\small',
              r'\begin{longtable}{@{}l ' + 'r '*max_m + r'@{}}',
              r'\caption{Sequential exclusion counts, charged only to the first successful criterion. The later rows record additional theoretical and exact finite obstructions.}\label{tab:stages}\\',
              r'\toprule',stage_header,r'\midrule',r'\endfirsthead',
              r'\toprule',stage_header,r'\midrule',r'\endhead',
              r'\bottomrule',r'\endfoot'])
names={'near_group':'Near-group theorem',
       'dimension_15':'Global dimension 15',
       'zero_spectrum':'Zero spectrum',
       'lower_rank_subring':'Closed rank-four/five subring',
       'dnumber':'Formal-codegree $d$-number',
       'one_spectrum':'One spectrum',
       'cyclotomic':'Cyclotomicity',
       'spectral_involution_module':'Involution Fourier module',
       'certified_rank6_subring':'Closed rank-six subring',
       'integral_formal_codegree':'Integral codegree divisibility',
       'noncyclic_maximal_near_group':'Maximal near-group theorem',
       'cyclic_isotypic_integrality':'Cyclic isotypic integrality',
       'cyclic3_spectral_module':'Cubic Fourier-module obstruction',
       'general_induction':'General central induction',
       'character':'Character-aware central induction',
       'tensor_rotation':'Tensor rotation',
       'modular':'Complete center modular obstruction',
       'subcategory_divisibility':'Subcategory dimension quotient',
       'oriented_dimension_order':'Oriented dimension order',
       'localized_TPE_F210':'Localized triangular-prism equations',
       'solvable_minkowski_support':'Solvability and support inequality',
       'half_partition_tannakian':'Half-partition Tannakian criterion',
       'odd_pointed_tannakian_120':'Odd pointed group in dimension 120',
       'solvable_double_equivariantization_orbit_obstruction':'Double equivariantization in dimension 52',
       'D96_solvable_order16_orbit_obstruction':'Order-sixteen orbit obstruction'}
names.update({
 'relative_trace_lattice':'Relative-trace lattice',
 'dimension150_forced_central_boson':'Dimension-150 central boson',
 'relative_trace_lattice':'Relative-trace lattice',
 'dimension150_forced_central_boson':'Dimension-150 central boson',
 'relative_trace_lattice':'Relative-trace lattice',
 'dimension150_forced_central_boson':'Dimension-150 central boson',
 'dimension96_new_rank_one_module_branch':'Dimension-96 rank-one modules',
 'eight_p_equivariantization':'Dimension-$8p$ equivariantization',
 'dimension96_existing_order16_orbit':'Dimension-96 order-sixteen orbits',
 'dimension112_singer_normalizer':'Dimension-112 Singer normalizer',
 'dimension54_brauer_picard':'Dimension-54 Brauer--Picard',
 'dimension310_group_theoretical':'Dimension-310 group theory',
 'complete_oriented_signed_sphericalization':'Additional complete signed quotients',
})
names.update({
 'cyclic_stabilizer_divisibility':'Cyclic-stabilizer divisibility',
 'signed_C3_sphericality_dimension_block':'Signed three-parameter sphericality',
 'full_induction_compression_parity':'Full induced-unit compression and parity',
 'anti_invariant_involution_module':'Anti-invariant module spectral bounds',
 'three_fixed_dual_module_Gram':'Morita-dual Gram identities',
 'positive_semidefinite_module_Gram':'Positive-semidefinite Gram refinement',
 'C3_A4_Morita_formal_codegree':'$C_3$--$A_4$ Morita obstruction',
 'inverse_V4_Morita_near_group':'Inverse $V_4$ Morita obstruction',
 'simple_center_prime_power_lattice':'Simple-center prime-power lattice',
 'quadratic_center_Galois_two_moment':'Quadratic-center Galois two-moment obstruction',
 'twisted_v4_staged_morita_obstruction':'Twisted $V_4$ staged Morita obstruction',
 'quadratic_center_reciprocity_two_moment':'Character reciprocity and two center moments',
 'dihedral_Morita_R18_obstruction':'Dihedral Morita and full center STS',
 'quadratic_casimir_compression':'Quadratic Casimir compression',
 'oriented_signed_compression':'Complete signed quotient and compression',
 'quadratic_center_Galois_two_moment_q60':'Conductor-sixty center moments',
 'cyclic3_full_morita_rank13_descent':'Full cyclic Morita and rank-thirteen descent',
 'quadratic_center_coupled_cyclic_rotation':'Coupled cyclic rotations and fusion integrality',
})
pretty_models={
    'D12_even_local_modules':r'$D_{12}$ even category (\S\ref{sec:d12})',
    'D12_even_part':r'$D_{12}$ even category (\S\ref{sec:d12})',
    'D12':r'$D_{12}$ even category (\S\ref{sec:d12})',
    'Vec(C7)':r'$\operatorname{Vec}(C_7)$',
    'TY(C6)':r'$\operatorname{TY}(C_6)$',
    'Rep(D16)':r'$\operatorname{Rep}(D_{16})$',
    'Rep(D22)':r'$\operatorname{Rep}(D_{22})$',
    'Rep(SD16)':r'$\operatorname{Rep}(SD_{16})$',
    'Rep(A6)':r'$\operatorname{Rep}(A_6)$',
    'Rep(C13rtimesC4)':r'$\operatorname{Rep}(C_{13}\rtimes C_4)$',
    'Adj(SU(3)_5)':r'$\operatorname{Adj}(\mathrm{SU}(3)_5)$',
    'TY(C3)-parity-equivariantization':r'TY parity equivariantization (\S\ref{sec:tyequiv})',
    'TY(C3)-twisted-C4-equivariantization':r'TY twisted-$C_4$ equivariantization (\S\ref{sec:tyequiv})',
    'Vec(Q8)^S3':r'$\operatorname{Vec}(Q_8)^{S_3}$',
    'C(Q8rtimesS3,Chern,S3,1)':r'Twisted quaternion model (\S\ref{sec:chern})',
    'Rep(S5)':r'$\operatorname{Rep}(S_5)$',
    'Rep(SL2(F3))':r'$\operatorname{Rep}(SL_2(\mathbb F_3))$',
    'Rep(C13rtimesC3)':r'$\operatorname{Rep}(C_{13}\rtimes C_3)$',
    'Rep(C11rtimesC5)':r'$\operatorname{Rep}(C_{11}\rtimes C_5)$',
    'Rep(C7rtimesC6)':r'$\operatorname{Rep}(C_7\rtimes C_6)$',
    'Rep(C7 semidirect C6) = Rep(AGL(1,7))':r'$\operatorname{Rep}(C_7\rtimes C_6)$',
    'Rep(H24)':r'$\operatorname{Rep}(H_{24})$',
    'C(A5,1,A4,1)':r'$\mathcal C(A_5,1,A_4,1)$',
    'SO(7)_2':r'$\mathrm{SO}(7)_2$',
    'Zest(SU(2)_6)':r'$\operatorname{Zest}(\mathrm{SU}(2)_6)$',
    'SU(2)_6':r'$\mathrm{SU}(2)_6$',
    'PSU(2)_12':r'$\mathrm{PSU}(2)_{12}$',
    'PSU(2)_13':r'$\mathrm{PSU}(2)_{13}$'}
for stage in summary['stage_order']:
    c=summary['stage_counts'][stage]
    lines.append(names.get(stage,esc(stage))+' & '+' & '.join(str(c.get(str(m),0)) for m in range(1,max_m+1))+r'\\')
lines.extend([r'\end{longtable}',r'}','',
              r'\begin{table}[H]',r'\centering',r'\small',
              r'\caption{Unitary model constructions identified by exact full-tensor based-ring isomorphism. Each row denotes a ring, not a count of categories.}\label{tab:models}',
              r'\begin{tabular}{@{}l l@{}}',r'\toprule',
              r'Census ID & Explicit model\\',r'\midrule'])
for item in sorted(catalog,key=lambda r:(r['multiplicity'],int(r['id'].split('_')[-1]))):
    model=pretty_models.get(item['name'])
    if item['id']=='R7_4_35': model=r'$C_4^2$ near-group inversion Morita model'
    if item['id']=='R7_4_2665': model=r'$C_{16}$ near-group inversion Morita model'
    if model is None and item['id']=='R7_2_240':
        model=r'$D_{12}$ even category (\S\ref{sec:d12})'
    if model is None and 'category_code' not in item:
        model=esc(item['name'])
    if model is None:
        c=item['category_code'];model=r'AnyonWiki $\mathrm{FC}^{7,1,'+str(c[2])+r'}_{'+','.join(map(str,c[3:]))+r'}$'
    lines.append(r'\texttt{'+esc(item['id'])+'} & '+model+r'\\')
lines.extend([r'\bottomrule',r'\end{tabular}',r'\end{table}', ''])
(PAPERS/'generated_tables.tex').write_text('\n'.join(lines))

if max_m >= 5:
    current=json.loads((ROOT/'output/m5/summary.json').read_text())
    counts=current['new_status_counts']
    fragment=[r'\subsection{Recorded outcome'+(' and open frontier' if counts.get('unresolved',0) else '')+'}',
        f"Among the $5805$ new tensors, ${counts.get('excluded',0)}$ are excluded, "
        f"${counts.get('unitarily_realized',0)}$ has a verified unitary model, and "
        f"${counts.get('unresolved',0)}$ {'remains' if counts.get('unresolved',0)==1 else 'remain'} undecided."]
    ids=current['unresolved_ids']
    if ids:
        fragment.extend([r'The unresolved identifier is' if len(ids)==1 else r'The unresolved identifiers are', r'\begin{center}\small',
                         r'\begin{tabular}{@{}l l l@{}}'])
        for start in range(0,len(ids),3):
            cells=[r'\texttt{'+esc(i)+'}' for i in ids[start:start+3]]
            cells+=['']*(3-len(cells))
            fragment.append(' & '.join(cells)+r'\\')
        fragment.extend([r'\end{tabular}',r'\end{center}',
                         r'Each has its complete tensor and attempted checks in the companion data.'])
    else:
        fragment.append(r'Every supplied tensor in the band has a recorded general exclusion or unitary model.')
    fragment.extend([
        r'A feasible necessary system is not a categorical construction, and a',
        r'time-limited or incomplete search is not a nonexistence certificate.',
        r'No new tensor category is established by this continuation. The model in',
        r'Proposition~\ref{prop:m5-frobenius42} is the only new realized based-ring',
        r'type added to the catalog in this continuation.', ''])
    (PAPERS/'generated_m5_status.tex').write_text('\n'.join(fragment))
