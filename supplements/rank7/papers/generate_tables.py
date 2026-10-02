"""Generate manuscript tables from the frozen, machine-replayed JSON ledger."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
summary=json.loads((ROOT/'output/rank7_summary.json').read_text())
catalog=json.loads((ROOT/'output/rank7_model_catalog.json').read_text())

def esc(v):
    return str(v).replace('\\','\\textbackslash{}').replace('_','\\_')

lines=[r'\begin{table}[H]',r'\centering',
       r'\caption{Certified status of complete rank-seven fusion-ring census through exact multiplicity four. Undecided entries are not assumed categorifiable.}\label{tab:status}',
       r'\begin{tabular}{@{}r r r r r@{}}',r'\toprule',
       r'Exact multiplicity & Fusion rings & Excluded & Realized & Undecided\\',r'\midrule']
for m in range(1,summary['max_multiplicity']+1):
    c=summary['status_counts'][str(m)]
    lines.append(f"{m} & {summary['ring_counts'][str(m)]} & {c.get('excluded',0)} & {c.get('unitarily_realized',0)} & {c.get('unresolved',0)}"+r'\\')
lines.extend([r'\bottomrule',r'\end{tabular}',r'\end{table}','',
              r'\begin{table}[H]',r'\centering',r'\small',
              r'\caption{Sequential exclusion counts, charged only to the first successful criterion. The later rows apply prime-descent and exhaustive signed criteria to surviving tensors.}\label{tab:stages}',
              r'\begin{tabular}{@{}l r r r r@{}}',r'\toprule',
              r'Criterion & $m=1$ & $m=2$ & $m=3$ & $m=4$\\',r'\midrule'])
names={'near_group':'Near-group theorem',
       'dimension_15':'Global dimension 15',
       'zero_spectrum':'Zero spectrum',
       'lower_rank_subring':'Closed rank-four/five subring',
       'dnumber':'Formal-codegree $d$-number',
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
    'Rep(H24)':r'$\operatorname{Rep}(H_{24})$',
    'C(A5,1,A4,1)':r'$\mathcal C(A_5,1,A_4,1)$',
    'SO(7)_2':r'$\mathrm{SO}(7)_2$',
    'Zest(SU(2)_6)':r'$\operatorname{Zest}(\mathrm{SU}(2)_6)$',
    'SU(2)_6':r'$\mathrm{SU}(2)_6$',
    'PSU(2)_12':r'$\mathrm{PSU}(2)_{12}$',
    'PSU(2)_13':r'$\mathrm{PSU}(2)_{13}$'}
for stage in summary['stage_order']:
    c=summary['stage_counts'][stage]
    lines.append(names.get(stage,esc(stage))+' & '+' & '.join(str(c.get(str(m),0)) for m in range(1,5))+r'\\')
lines.extend([r'\bottomrule',r'\end{tabular}',r'\end{table}','',
              r'\begin{table}[H]',r'\centering',r'\small',
              r'\caption{Unitary model constructions identified by exact full-tensor based-ring isomorphism. Each row denotes a ring, not a count of categories.}\label{tab:models}',
              r'\begin{tabular}{@{}l l@{}}',r'\toprule',
              r'Census ID & Explicit model\\',r'\midrule'])
for item in sorted(catalog,key=lambda r:(r['multiplicity'],int(r['id'].split('_')[-1]))):
    model=pretty_models.get(item['name'])
    if model is None and item['id']=='R7_2_240':
        model=r'$D_{12}$ even category (\S\ref{sec:d12})'
    if model is None:
        c=item['category_code'];model=r'AnyonWiki $\mathrm{FC}^{7,1,'+str(c[2])+r'}_{'+','.join(map(str,c[3:]))+r'}$'
    lines.append(r'\texttt{'+esc(item['id'])+'} & '+model+r'\\')
lines.extend([r'\bottomrule',r'\end{tabular}',r'\end{table}', ''])
(ROOT/'papers/generated_tables.tex').write_text('\n'.join(lines))
