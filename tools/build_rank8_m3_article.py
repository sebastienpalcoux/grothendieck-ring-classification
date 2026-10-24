#!/usr/bin/env python3
"""Integrate the accepted M3 ledger into the rank-eight article and mirrors."""
from pathlib import Path
from collections import Counter
import json
import re
import shutil
import subprocess
import sys
from rank8_publication import extension, EVIDENCE, ledger_path, model_path
import rank8_frontier as frontier
ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT/'manuscripts/rank8/paper'
MODEL_LABELS={
274:r'Phase-rotation $C_2$-equivariantization of $\operatorname{NG}(C_3,6)$',
331:r'$\operatorname{NG}(C_3,3)\boxtimes\operatorname{Vec}(C_2)$',
334:r'Reflection $C_2$-equivariantization of $\operatorname{NG}(C_3,6)$',
342:r'$\operatorname{Rep}(C_{13}\rtimes C_6)$',
448:r'Unitary Izumi--Xu $C_2$ extension ($2221$)',
458:r'Morita dual of the conformal $G_{2,3}\subset E_{6,1}$ algebra',
471:r'$\operatorname{NG}(C_3,3)\boxtimes\operatorname{Fib}$',
475:r'$(\operatorname{Fib}^{\boxtimes3})^{C_3}$ by cyclic permutation',
715:r'Morita dual of the nonsplit unitary $2D2$ extension',
721:r'Inherited Q-system Morita dual in the $C_2$ de-equivariantization of $\operatorname{GH}(C_8)$',
724:r'$\operatorname{Rep}(\operatorname{PSL}_2(11))$',
982:r'Triality-zero component of the known $E_{21}$ category for $SU(3)_{21}\subset(E_7)_1$ (Theorem~\ref{thm:creative-e21-model})',
1456:r'$\operatorname{Ad}(E_8)\boxtimes\operatorname{Vec}(C_2)$',
3278:r'Unitary $E_8$ fusion category',
3314:r'$\operatorname{Ad}(E_8)\boxtimes\operatorname{Fib}$',
3342:r'Twisted $\mathcal C(A_6,\omega,A_5,\psi)$ from a stable relative $\mu_2$ class',
}
def tex(value):
    text=str(value).replace('–','--').replace('—','---').replace('×',r'$\times$').replace('⋊',r'$\rtimes$')
    return ''.join({'&':r'\&','_':r'\_','%':r'\%','#':r'\#'}.get(c,c) for c in text)
def normalize(text):
    text=re.sub(r'\$R8\\_([0-9]+)\\_([0-9]+)\$',lambda m:r'$\sha{R8_'+m[1]+'_'+m[2]+'}$',text)
    text=re.sub(r'\\\(R8\\_([0-9]+)\\_([0-9]+)\\\)',lambda m:r'\sha{R8_'+m[1]+'_'+m[2]+'}',text)
    text=re.sub(r'R_\{8,3,([0-9]+)\}',lambda m:r'\sha{R8_3_'+m[1]+'}',text)
    text=re.sub(r'\\texttt\{R8\\_([0-9]+)\\_([0-9]+)\}',lambda m:r'\sha{R8_'+m[1]+'_'+m[2]+'}',text)
    return re.sub(r'\\texttt\{([^}]+)\}',lambda m:r'\path{'+m[1].replace(r'\_','_')+'}',text)
BIB={
'NgHigherPivotal':r'''S.-H.~Ng and P.~Schauenburg, \emph{Higher Frobenius--Schur indicators for pivotal categories}, Contemp. Math. \textbf{441} (2007), 63--90; arXiv:math/0503167v2, Theorem~5.1 and its proof.''',
'IntegralPublished':r'''M.~A.~Alekseyev, W.~Bruns, J.~Dong and S.~Palcoux, \emph{Classifying integral Grothendieck rings up to rank 5 and beyond}, Lett. Math. Phys. \textbf{116} (2026), Paper 141, Proposition~5.7; doi:10.1007/s11005-026-02164-7.''',
'NSWHigherGauss':r'''S.-H.~Ng, A.~Schopieray and Y.~Wang, \emph{Higher Gauss sums of modular categories}, Selecta Math. (N.S.) \textbf{25} (2019), Paper 53; arXiv:1812.11234v2, Theorem~4.4.''',
'RWQuadraticFocus':r'''D.~Radchenko and C.~Wheeler, \emph{Real quadratic fields and finite quantum dilogarithms I}, arXiv:2609.21892v2 (2026), Sections~4.3 and~5.4.''',
'LPRSimpleFocus':r'''Z.~Liu, S.~Palcoux and Y.~Ren, \emph{Interpolated family of non-group-like simple integral fusion rings of Lie type}, Internat. J. Math. \textbf{34} (2023), no.~6, 2350030; arXiv:2102.01663v4, Theorem~5.1.''',
'GrossmanIzumiCentersNext':r'''P.~Grossman and M.~Izumi, \emph{Drinfeld centers of fusion categories arising from generalized Haagerup subfactors}, arXiv:1501.07679v2 (2019), equations~(2.21)--(2.22), Example~4.4 and Section~6.''',
'GrossmanIzumiMetricNext':r'''P.~Grossman and M.~Izumi, \emph{Infinite families of potential modular data related to quadratic categories}, arXiv:1906.07397v2 (2019), Definition~6.1 and Section~6.1.6.''',
'DeshpandeVerlindeFollowup':r'''T.~Deshpande, \emph{On twisted Verlinde formulae for modular categories}, arXiv:1811.08447v1 (2018), Theorem~1.1.''',
'CosteGannonRuelleFollowup':r'''A.~Coste, T.~Gannon and P.~Ruelle, \emph{Finite Group Modular Data}, Nucl. Phys. B \textbf{581} (2000), 679--717; arXiv:hep-th/0001158v2, Section~2.2.''',
'UsherFermionic':r'''R.~Usher, \emph{Fermionic $6j$-symbols in superfusion categories}, arXiv:1606.03466 (2016), Theorem~5.4 and Corollary~5.8.''',
'BrownTransferFrontier':r'''K.~S.~Brown, \emph{Lectures on the Cohomology of Groups}, lecture notes, Section~3.3, equation~(3.12); \url{https://pi.math.cornell.edu/~kbrown/papers/cohomology_hangzhou.pdf}.''',
'SchauenburgPointedFrontier':r'''P.~Schauenburg, \emph{A Higher Frobenius--Schur Indicator Formula for Group-Theoretical Fusion Categories}, arXiv:1502.02906 (2015), Definition~2.2 and Proposition~4.1.''',
'CoquereauxQuantumMcKay':r'''R.~Coquereaux, \emph{Quantum McKay correspondence and global dimensions for fusion and module-categories associated with Lie groups}, J. Algebra \textbf{398} (2014), 258--283; arXiv:1209.6621v2.''',
'ThorntonNear':r'''J.~Thornton, \emph{On braided near-group categories}, arXiv:1102.4640, Theorem~1.3.''',
'LPRV':r'''Z.~Liu, S.~Palcoux, Y.~Ren and G.~Vercleyen, \emph{Triangular Prism Equations and Categorification}, arXiv:2203.06522v5 (2025), Theorem~3.9.''',
'NearGroupTPE2026':r'''H.~He, Z.~Liu, F.~Lu, S.~Palcoux and Y.~Ren, \emph{Triangular prism equations for near-group categories: algebraic solutions and a unitary conjecture}, arXiv:2610.11652v1 (2026).''',
'DGNO':r'''V.~Drinfeld, S.~Gelaki, D.~Nikshych and V.~Ostrik, \emph{On braided fusion categories I}, Selecta Math. \textbf{16} (2010), 1--119; arXiv:0906.0620.''',
'SchopierayBraidedGNG':r'''A.~Schopieray, \emph{Irrational braided generalized near-groups}, arXiv:2212.14009 (2022).''',
'BurciuNataleEquivariantization':r'''S.~Burciu and S.~Natale, \emph{Fusion rules of equivariantizations of fusion categories}, J. Math. Phys. \textbf{54} (2013), 013511; arXiv:1206.6625.''',
'DeshpandeCenter':r'''T.~Deshpande, \emph{On centers of bimodule categories and induction-restriction functors}, arXiv:1611.04486 (2016), Section~2.7, equation~(39), Lemma~4.3 and Corollary~4.5.''',
'OstrikModules':r'''V.~Ostrik, \emph{Module categories, weak Hopf algebras and modular invariants}, Transform. Groups \textbf{8} (2003), 177--206; arXiv:math/0111139, Theorem~2 and Remark~12.''',
'EdieGolden':r'''C.~Edie-Michell, \emph{A complete classification of unitary fusion categories tensor generated by an object of dimension $(1+\sqrt5)/2$}, arXiv:1904.08909v2, Definition~2.5.''',
'DongWeak':r'''J.~Dong, \emph{Classification of certain weakly integral fusion categories}, arXiv:2103.04553v3, Theorem~1.2 and Corollary~4.16.''',
'CMSIzumiXu':r'''F.~Calegari, S.~Morrison and N.~Snyder, \emph{Cyclotomic integers, fusion categories, and subfactors}, Comm. Math. Phys. \textbf{303} (2011), 845--896, Appendix~A by V.~Ostrik, Propositions~A.4.1 and~A.6.1 and Section~A.5.''',
'NaiduMorita':r'''D.~Naidu, \emph{Categorical Morita equivalence for group-theoretical categories}, Comm. Algebra \textbf{35} (2007), 3544--3565; arXiv:math/0605530, Theorem~3.4.''',
'DMNO':r'''A.~Davydov, M.~M\"uger, D.~Nikshych and V.~Ostrik, \emph{The Witt group of non-degenerate braided fusion categories}, J. Reine Angew. Math. \textbf{677} (2013), 135--177; arXiv:1009.2117v2, Section~3.3.''',
'GuiQSystems':r'''B.~Gui, \emph{Q-systems and extensions of completely unitary vertex operator algebras}, arXiv:1908.03484v3, Theorems~2.21 and~2.28, Corollary~3.32.''',
'MorrisonPenneysSpokes':r'''S.~Morrison and D.~Penneys, \emph{Constructing spoke subfactors using the jellyfish algorithm}, arXiv:1208.3637v2, Section~5.1 and Theorem~5.5.''',
'GJSCyclic':r'''P.~Grossman, D.~Jordan and N.~Snyder, \emph{Cyclic extensions of fusion categories via the Brauer--Picard groupoid}, arXiv:1211.6414v2, Theorem~4.9 and Remarks~4.10--4.11.''',
'CartanEilenberg':r'''H.~Cartan and S.~Eilenberg, \emph{Homological Algebra}, Princeton University Press (1956), Chapter~XII, Section~10.''',
'GSAsaedaMorita':r'''P.~Grossman and N.~Snyder, \emph{The Brauer--Picard group of the Asaeda--Haagerup fusion categories}, Trans. Amer. Math. Soc. \textbf{368} (2016), 2289--2331; arXiv:1202.4396v2.''',
'HuangOddHI2026':r'''T.-C.~Huang, \emph{Cyclic Haagerup--Izumi fusion categories at every odd order}, arXiv:2609.15986v1 (2026).''',
'GSYOddHI2026':r'''T.~Gannon, A.~Schopieray and H.~Yadav, \emph{On Haagerup--Izumi fusion categories}, arXiv:2609.25185v1 (2026).''',
'GSHaagerup':r'''P.~Grossman and N.~Snyder, \emph{Quantum subgroups of the Haagerup fusion categories}, Comm. Math. Phys. \textbf{311} (2012), 617--643; arXiv:1102.2631v2, Theorem~1.5.'''}
def main():
    ext=extension(ROOT)
    if ext is None:raise ValueError('Accepted M3 publication ledger required')
    rows=json.loads((ROOT/ledger_path(ROOT)).read_text());new=[r for r in rows if r['multiplicity']==3]
    by_id={r['id']:r for r in new};models=[r for r in json.loads((ROOT/model_path(ROOT)).read_text()) if r['multiplicity']==3]
    model_ids={r['id'] for r in models}
    stated=[275,276,344,345,810,812,2492,2494,2620,2622,1051,2415,307,2132,347,916,1348,76,735,738,1422,1805,920,986,1453,1019,1057,1067,1197,2392,2836,2904,3082]
    if any(by_id[f'R8_3_{i}']['status']!='excluded' for i in stated):raise ValueError('A stated theorem is absent from the accepted ledger')
    text=r'''\section{The multiplicity-three continuation}
\label{sec:m3-continuation}
The supplied extension has $3527$ rings of exact multiplicity three and
$4500$ cumulatively. Every tensor, identifier, decision and model through multiplicity two
is preserved. The new raw tensor file has uncompressed SHA-256
\par\noindent\sha{7baaa0a2018e11a0464c3f19da9030195421f04a73806c22363cf9d5eeb92a84}.
The independently checked tensor axioms and preservation of earlier tensors
do not constitute an independent exhaustive enumeration. The optimized
producer source is now supplied and matches the completion receipt;
enumeration completeness remains producer-reported.

\begin{theorem}[Current exact-multiplicity-three status]\label{thm:m3-current}
The $3527$ supplied rings of exact multiplicity three have the following
recorded categorification status:
\begin{center}\begin{tabular}{@{}lr@{}}\toprule
Status & Rings\\\midrule
'''
    for name,n in [('General complex exclusion',ext['excluded']),('Unitary construction',ext['unitarily_realized'])]:text+=name+f' & ${n}$\\\\\n'
    if ext['pseudo_unitarily_realized']:text+=f"Further pseudo-unitary construction & ${ext['pseudo_unitarily_realized']}$\\\\\n"
    text+=f"Unresolved general categorification & ${ext['unresolved']}$\\\\\n"
    text+=r'''\bottomrule\end{tabular}\end{center}
Positive identifications use full ordered tensor comparisons or, for
$\sha{R8_3_721}$, the exact coefficient bound and complete-census uniqueness
proved in Theorem~\ref{thm:r721-qsystem-model}. A recorded construction proves
existence, without claiming uniqueness up to tensor equivalence.
\end{theorem}
The source-bound combined ledger is
\par\noindent{\small\path{supplements/rank8/output/m3/ledger.json}}.
Its exact-M3 first-exclusion
allocation follows. Overlapping obstructions are retained in the evidence
rather than counted twice.
\begin{center}\small\begin{longtable}{@{}p{.75\textwidth}r@{}}\toprule
First accepted criterion & Rings\\\midrule\endhead
'''
    for kind,n in sorted(Counter((r.get('certificate') or {}).get('kind') or r['criterion'] for r in new if r['status']=='excluded').items()):text+=tex(kind.replace('_',' '))+f' & ${n}$\\\\\n'
    text+=r'''\bottomrule\end{longtable}\end{center}
The lower-multiplicity classification below retains its original scope and
proof inputs. Its historical allocation is separate from this table.
\input{m3_criteria}
\input{m3_biquadratic}
\input{m3_convex}
\input{m3_module}
\input{m3_structural}
\input{m3_positivity}
\input{m3_models}
\subsection{Exact model inventory}
\begin{center}\small\begin{longtable}{@{}p{.18\textwidth}p{.55\textwidth}p{.18\textwidth}@{}}\toprule
Census ID & Construction & Scope\\\midrule\endhead
'''
    for model in models:
        label=MODEL_LABELS.get(int(model['id'].split('_')[-1]))
        if label is None:label=tex(model.get('model') or model['constructors'][0]['model'])
        text+=r'\sha{'+model['id']+'} & '+label+' & '+tex(model.get('model_scope','unitary'))+r'\\'+'\n'
    text+=r'''\bottomrule\end{longtable}\end{center}
Every model in this inventory admits a unitary realization. For
$\sha{R8_3_448}$, the original pseudo-unitary existence result is
supplemented by the unitary $2221$ planar-algebra construction above.
\subsection{The remaining general questions and replay scope}
'''
    text+=f"There remain ${ext['unresolved']}$ unresolved exact-M3 tensors. "
    text+=r'''The source tensors and per-case attempted criteria are recorded in
\path{data/remaining_cases.py} and
\path{evidence/rank8_m3_20261021/pipeline/residual_attempts.json}.
The inventory distinguishes an exact contradiction, a necessary-condition
survivor, a time limit, and an inapplicable test. Passing these conditions
supplies no coherent associator; an unsuccessful construction search
supplies no exclusion. Any claim of categorical novelty requires a separate
comparison up to tensor equivalence.
'''
    if ext['unresolved']:
        profiles={r['id']:r for r in json.loads((ROOT/EVIDENCE/'pipeline/survivor_profiles.json').read_text())}
        text+=r'''\subsubsection{Individually investigated candidates}
These are unresolved categorification candidates, not asserted categories
or established exotic examples. A unitary exclusion does not settle the
general complex question. The last column gives ranks of nontrivial
proper fusion subrings, as checked on the exact source tensors.
\begin{center}\small\begin{longtable}{@{}lcccc@{}}\toprule
Census ID & Commutative & Invertibles & Unitary status & Proper subring ranks\\\midrule\endhead
'''
        for row in new:
            if row['status']!='unresolved':continue
            q=profiles[row['id']];ranks=sorted({x['rank'] for x in q['proper_subrings'] if x['rank']>1})
            unitary='excluded' if row.get('unitary_status')=='excluded' else 'unresolved'
            text+=r'\sha{'+row['id']+'} & '+('yes' if q['commutative'] else 'no')+' & '+str(len(q['invertibles']))+' & '+unitary+' & '+(', '.join(map(str,ranks)) if ranks else '--')+r'\\'+'\n'
        text+=r'\bottomrule\end{longtable}\end{center}'+'\n'
    text+=r'''\input{m3_model_search}
The aggregate command is
\begin{quote}\small
\texttt{python }\path{supplements/rank8/software/verify_m3_continuation.py}.
\end{quote}
It checks the accepted ledger against the source, baseline criteria,
continuation certificates and explicit model tensors. Its full receipt
binds the exact ledger digest, manifests and proof-source hashes. Under
Python optimization, inherited assertion-based checkers run in an isolated
interpreter with assertions enabled. Metadata-only mode checks these
identities and reconciliation without replaying the mathematics.
'''
    census=json.loads((ROOT/'data/counts.json').read_text()).get('census_extensions',{}).get('rank8_m3')
    if census:
        marker=r'\begin{theorem}[Current exact-multiplicity-three status]'
        text=text.replace(marker,'The census release is pinned to Git commit\n'+r'\par\noindent\sha{'+census['census_commit']+'}.\n'+r'The source and audit are \path{results/rank8/tables.txt.gz} and \path{verification/rank8/audit.json} in that repository.'+'\n\n'+marker,1)
    text=text.replace(r'\path{supplements/rank8/output/m3/ledger.json}',r'\path{'+ledger_path(ROOT)+'}')
    if ext.get('frontier'):
        text=text.replace(r'\path{evidence/rank8_m3_20261021/pipeline/residual_attempts.json}',
                          r'\path{'+ext['attempts_source']+'}')
        text=text.replace(r'\path{data/remaining_cases.py} and'+'\n'+r'\path{'+ext['attempts_source']+'}.', r'\path{data/remaining_cases.py} and the per-case audit\par\noindent'+'\n'+r'{\small\path{'+ext['attempts_source']+'}}.')
        text=text.replace('These are unresolved categorification candidates, not asserted categories\nor established exotic examples.',
            'We call the remaining rings extensively investigated exotic candidates in the operational sense: each survived the documented case-specific campaign of known and newly developed exclusion tests and model searches, including complete finite domains and specified unbounded construction families. This term asserts neither categorifiability nor novelty of a future realization.')
        text=text.replace(r'\texttt{python }\path{supplements/rank8/software/verify_m3_continuation.py}.',
            r'\texttt{python }\path{supplements/rank8/software/verify_m3_continuation.py}\\'+'\n'+r'\texttt{--output }\path{frontier-validation/baseline_normal.json}.')
        text=text.replace('It checks the accepted ledger against the source, baseline criteria,',
            'It checks the original M3 ledger against the source, baseline criteria,')
        accepted_ids=set(ext['frontier']['resolved_ids'])
        if not {'R8_3_731','R8_3_3344'} <= accepted_ids:
            raise ValueError('Both integral proofs must be accepted before publishing their combined section')
        heading=(r'\subsection{Further investigation of the original frontier}'+'\n'
                 +f"The previous release left $34$ exact-M3 rings unresolved. The historical frontier recorded ${ext['frontier']['new_decisions']}$ further general exclusion claims; the R436 claim is now conditional and is withheld from the current general ledger. The current totals also include the later accepted constructions above, leaving ${ext['unresolved']}$ questions. "
                 +'The earlier ledger and replay receipts are retained byte for byte; accepted changes are recorded in a separate overlay ledger.\n')
        proof_files=[
            'quadratic/simultaneous_split_section.tex','structural_models/r436_general_tpe.tex','integral/manuscript.tex',
            'structural_models/scoped_construction_search.tex',
            'quadratic/quadratic_residual_section.tex','quadratic/connected_algebra_section.tex',
            'quadratic/cm_real_sts_section.tex',
            'central_integrality/galois_pu_method.tex',
            'noncommutative_followup/noncommutative_method.tex',
            'review/integral_center_subcategory.tex',
            'central_integrality/fixed_gram_method.tex',
            'commutative_integer/integer_central_cubic.tex',
            'quadratic/joint_galois_section.tex',
            'quadratic_atomic_integer/integral_center_filter.tex',
            'quadratic_atomic_integer/unit_pair_method.tex',
            'commutative_integer/phase_compatibility.tex',
            'commutative_integer/r982_integer_section.tex',
            'quadratic/integer_phase_cut_section.tex',
            'quartic_integer_center/method.tex',
            'review/r941_fusion_traces.tex',
            'r928_semion_rotation/method.tex',
            'review/fermion_dimension_counterexample.tex']
        if 'R8_3_925' in accepted_ids:proof_files.append('global_induction/frame_hull.tex')
        if 'R8_3_926' in accepted_ids:proof_files.append('global_induction/spectral_frame.tex')
        if 'R8_3_1463' in accepted_ids:proof_files.append('global_induction/low_s_symmetry.tex')
        if 'R8_3_901' in accepted_ids:proof_files.append('quadratic/octic_low_s_section.tex')
        if accepted_ids & {'R8_3_903','R8_3_985','R8_3_1615','R8_3_1617','R8_3_1660','R8_3_1661','R8_3_3413','R8_3_3258','R8_3_1055'}:
            proof_files.append('global_induction/labeled_modular_theorem.tex')
        if 'R8_3_439' in accepted_ids:proof_files.append('r439_centerless_rank5/method.tex')
        if 'R8_3_567' in accepted_ids:proof_files.append('r567_centerless_integer/method.tex')
        if 'R8_3_455' in accepted_ids:proof_files.append('r455_center_integer/method.tex')
        if 'R8_3_903' in accepted_ids:proof_files.append('global_induction/sts_903_application.tex')
        if 'R8_3_1615' in accepted_ids:proof_files.append('global_induction/sts_1615_application.tex')
        if 'R8_3_1617' in accepted_ids:proof_files.append('global_induction/sts_1617_application.tex')
        if 'R8_3_1660' in accepted_ids:proof_files.append('global_induction/sts_1660_application.tex')
        if 'R8_3_1661' in accepted_ids:proof_files.append('global_induction/sts_1661_application.tex')
        if 'R8_3_985' in accepted_ids:proof_files.append('global_induction/sts_985_application.tex')
        if 'R8_3_3413' in accepted_ids:proof_files.append('global_induction/atomic_3413_application.tex')
        if 'R8_3_1055' in accepted_ids:proof_files.append('global_induction/atomic_1055_application.tex')
        if 'R8_3_3258' in accepted_ids:proof_files.append('global_induction/atomic_sts_application.tex')
        proofs='\n'.join((ROOT/frontier.EVIDENCE/name).read_text() for name in proof_files)
        if 'R8_3_439' in accepted_ids:
            proofs=proofs.replace('Other associators\n'+
                'on the same based ring remain open; no model is inferred.',
                r'This structural filter alone does not decide other associators; the centerless Morita obstruction in Section~\ref{subsec:r439-centerless-morita} excludes the required dual.')
        if {'R8_3_439','R8_3_455','R8_3_567'} <= accepted_ids:
            proofs=proofs.replace('The remaining three noncommutative central tests',
                'Earlier central tests for three further noncommutative rings')
        proofs=proofs.replace(r'\begin{quote}\small\path{evidence/rank8_frontier_20261021/r567_centerless_integer/verlinde_exclusion.py}',r'\begin{quote}\footnotesize\path{evidence/rank8_frontier_20261021/r567_centerless_integer/verlinde_exclusion.py}')
        proofs=proofs.replace('For an arbitrary categorification take its canonical sphericalization',r'For an arbitrary categorification take its canonical sphericalization~\cite[Section~5.1]{OstrikPiv3}')
        proofs=proofs.replace(r'requires $\delta/f$ to be integral.',r'requires $\delta/f$ to be integral~\cite[Theorem~2.13 and Corollary~2.14]{OstrikPiv3}.')
        proofs=proofs.replace('A number-field model and Galois conjugation',r'A number-field model~\cite[Theorem~2.30 and the following remark]{ENO} and Galois conjugation')
        if 'R8_3_721' in model_ids:
            proofs=proofs.replace('unitarity; both rings remain unresolved by this proposition.',
                r'unitarity. This proposition alone decides neither ring; $\sha{R8_3_721}$ is realized separately in Theorem~\ref{thm:r721-qsystem-model}.')
        frontier_text=heading+normalize(proofs)
        if ext.get('creative'):
            frontier_text=frontier_text.replace(
                'and the two complete selected-pattern phase checks leave\n'+
                r'\sha{R8_3_982} unresolved; they provide neither a category model nor'+'\n'+
                'a general noncategorifiability theorem.',
                'and the two complete selected-pattern phase checks left\n'+
                r'\sha{R8_3_982} unresolved at that checkpoint. They provide neither a category'+'\n'+
                'model nor a general noncategorifiability theorem; the later realization is\n'+
                r'Theorem~\ref{thm:creative-e21-model}.')
        (PAPER/'m3_frontier.tex').write_text(frontier_text)
        text += r'''\input{m3_frontier}
'''
        followup=ROOT/'evidence/rank8_center_followup_20261021'
        if followup.is_dir():
            check=subprocess.run([sys.executable,str(followup/'verify.py'),'--root',str(ROOT),
                                  '--metadata-only'],cwd=ROOT,text=True,capture_output=True)
            if check.returncode or json.loads(check.stdout).get('status')!='METADATA_PASS':
                raise ValueError('Separate center follow-up replay required:\n'+check.stdout+check.stderr)
            extra=(followup/'center_followup.tex').read_text()+'\n'+(followup/'r1154_center_followup.tex').read_text()
            # The paired action equations need two alignment pairs.
            extra=extra.replace(r'\begin{split}',r'\begin{aligned}').replace(r'\end{split}',r'\end{aligned}')
            extra=extra.replace('In the pair order\n$(11,12,13,14,22,23,24,33,34,44)$, put',
                'Use the pair order\n\\[ (11,12,13,14,22,23,24,33,34,44). \\]\nPut')
            extra=extra.replace('$207,208,376,377,898,899,1407,1408$ and are exactly the first row of the table.',
                '\\[207,208,376,377,898,899,1407,1408,\\]\nand are exactly the first row of the table.')
            extra=extra.replace(r'''The portable replay scripts \texttt{r1154\_quartic\_necessary\_filters.py},
\texttt{r1154\_quartic\_coordinate\_propagation.py}, and
\texttt{r1154\_quartic\_reconcile.py} bind their inputs by SHA-256 and give''',
                r'''The portable replay scripts are
\begin{quote}\small
\path{r1154_quartic_necessary_filters.py}\\
\path{r1154_quartic_coordinate_propagation.py}\\
\path{r1154_quartic_reconcile.py}.
\end{quote}
They bind their inputs by SHA-256 and give''')
            extra=extra.replace('module specialization of Deshpande, \\emph{On twisted Verlinde formulae\nfor modular categories}, Theorem~1.1, arXiv:1811.08447.',
                                r'module specialization of the twisted Verlinde formula~\cite[Theorem~1.1]{DeshpandeVerlindeFollowup}.')
            extra=extra.replace(r'$\operatorname{Rep}(S_3)$.  In particular',
                                r'$\operatorname{Rep}(S_3)$~\cite[Section~2.2]{CosteGannonRuelleFollowup}.  In particular')
            if 'R8_3_721' in model_ids:
                extra=extra.replace('The following small exact continuation changes no general exclusion or\nrealization count.  It strengthens the necessary center data for',
                    'This earlier exact continuation changed no general exclusion or\nrealization count. It strengthened the necessary center data for')
                extra=extra.replace('is not a center fusion ring or a categorical model.  The previously',
                    r'is not a center fusion ring or a categorical model. The later Q-system construction of $\sha{R8_3_721}$ appears in Theorem~\ref{thm:r721-qsystem-model}. The previously')
            extra+=r'''
\subsection{Separate replay of the center-product refinement}
The source-bound proofs, complete surviving matrix tuples, rejected pattern
indices and independent arithmetic reconstructions are in
\path{evidence/rank8_center_followup_20261021/}. Run
\begin{quote}\small
\verb|python evidence/rank8_center_followup_20261021/verify.py --root .|
\end{quote}
in normal Python and with \texttt{-O}. This separately checked refinement
preserves the original continuation ledger and its $25$ additional ring
exclusions. At this stage both rings were unresolved. These necessary
data alone do not constitute fusion categories; the later construction of
$\sha{R8_3_721}$ is Theorem~\ref{thm:r721-qsystem-model}. The remaining
center patterns for $\sha{R8_3_1154}$ are refined below.
'''
            (PAPER/'m3_center_followup.tex').write_text(normalize(extra))
            text+=r'\input{m3_center_followup}'+'\n'
        if ext.get('next'):
            next_root=ROOT/'evidence/rank8_next_20261021'
            additions=(next_root/'r721/r65_scoped_addendum.tex').read_text()+'\n'
            additions+=(next_root/'r1154/R1154_ADVANCED_CENTER_ADDENDUM.tex').read_text().replace(
                r'\section{Three remaining center patterns',r'\subsection{Three remaining center patterns')
            additions+=r'''
\paragraph{Separate exact evidence.}
The accepted construction and scoped refinements, with normal and
optimized-Python receipts and independent reviews, are recorded in
\begin{quote}\small\path{evidence/rank8_next_20261021/}.\end{quote}
Their publication overlay preserves
the earlier ledgers and source-bound proof files.
'''
            (PAPER/'m3_next_refinements.tex').write_text(normalize(additions))
            text+=r'\input{m3_next_refinements}'+'\n'
        text += r'''
\subsection{Continuation evidence and reproducibility}
The new proofs and construction-family audits are in
\path{evidence/rank8_frontier_20261021/}. The original M3 command above
replays the original ledger. The separate continuation command is
\begin{quote}\small
\verb|python tools/verify_rank8_frontier.py|
\end{quote}
Run each command with normal Python and with \texttt{-O}. The continuation
receipt binds the unchanged original ledger, every accepted new decision,
the proof sources and the exact replay logs. Scoped failed construction
searches and feasible necessary-condition witnesses retain their stated
domains; they are not proofs of nonexistence or categorifiability.
'''
    # These research sections are authored manuscript sources. Preserve them
    # and restore their inputs whenever the generated continuation is rebuilt.
    if ext.get('research'):
        marker=r'\subsection{Continuation evidence and reproducibility}'
        research_inputs=''.join(r'\input{'+name+'}\n' for name in
                               ('m3_research_20261022','m3_pointed_followup'))
        for name in ('m3_research_20261022.tex','m3_pointed_followup.tex'):
            if not (PAPER/name).is_file():raise ValueError('Missing authored research section: '+name)
        text=text.replace(marker,research_inputs+'\n'+marker,1)
        text+=r'''
The 22 October research overlay replays separately with
\begin{quote}\small\verb|python3 tools/verify_rank8_research_20261022.py|\end{quote}
It accepts the general exclusions of $\sha{R8_3_65}$ and $\sha{R8_3_1795}$.
'''
    if ext.get('creative'):
        creative=(ROOT/'evidence/rank8_creative_20261022/r3472/integrated_manuscript.tex').read_text()
        creative=creative.replace('It therefore leaves the unresolved list. The exact-multiplicity-three\ncounts become',
            'It therefore left the unresolved list at this historical checkpoint.\nThe exact-multiplicity-three counts at that checkpoint were')
        creative=creative.replace('$5$ unresolved cases; cumulatively through multiplicity three they are',
            '$5$ unresolved cases; cumulatively through multiplicity three they were')
        if by_id['R8_3_3472']['status']=='excluded':
            creative=creative.replace('conditional Morita restrictions; R3472 remains unresolved.',
                r'conditional Morita restrictions. R3472 was unresolved at this checkpoint; its later general exclusion is Theorem~\ref{thm:r3472-general-exclusion}.')
            creative=creative.replace('$4402$, $93$ and $5$, respectively.',
                r'$4402$, $93$ and $5$, respectively. The later exclusion of $\sha{R8_3_3472}$ in Theorem~\ref{thm:r3472-general-exclusion} gives the current totals in Theorem~\ref{thm:m3-current}.')
        (PAPER/'m3_creative_20261022.tex').write_text(creative)
        text=text.replace(r'\input{m3_pointed_followup}',
                          r'\input{m3_pointed_followup}'+'\n'+r'\input{m3_creative_20261022}')
        focus=ROOT/'evidence/r3472_focus_20261022/manuscript.tex'
        if by_id['R8_3_3472']['status']=='excluded':
            focus=ROOT/'evidence/r3472_exclusion_20261022/manuscript.tex'
            if not focus.is_file():raise ValueError('Missing accepted R3472 exclusion manuscript')
        if focus.is_file():
            shutil.copy2(focus,PAPER/'m3_r3472_focus.tex')
            text=text.replace(r'\input{m3_creative_20261022}',
                              r'\input{m3_creative_20261022}'+'\n'+r'\input{m3_r3472_focus}')
        text=text.replace(r'\input{m3_model_search}',r'''\paragraph{Historical search stages.}
The following earlier campaigns retain their original proof domains and
checkpoint results. Their historical unresolved lists are superseded by
Theorem~\ref{thm:m3-current}; in particular the known model of
$\sha{R8_3_982}$ is established in Theorem~\ref{thm:creative-e21-model}.
\input{m3_model_search}''')
        text+=r'''
The exceptional-model overlay and new necessary-condition checks replay with
\begin{quote}\small\verb|python3 tools/verify_rank8_creative_20261022.py|\end{quote}
Run also with \texttt{-O}. The flag \texttt{--metadata-only} validates
recorded receipts; \texttt{--historical} additionally replays earlier
mathematics from the pinned historical archive. The separate archive is
\begin{quote}\small\path{supplements/rank8/release/rank8-certified-creative-20261022.zip}.\end{quote}
Only $\sha{R8_3_982}$ changed status in that historical overlay, leaving
five unresolved cases at that checkpoint.
'''
        if by_id['R8_3_3472']['status']=='excluded':
            text+=r'''
The subsequent exact center-indicator certificate excludes
$\sha{R8_3_3472}$ over $\mathbb C$ by
Theorem~\ref{thm:r3472-general-exclusion}. Its full source-derived replay is
\begin{quote}\small
\texttt{python3 }\path{evidence/r3472_exclusion_20261022/replay.py}.
\end{quote}
The self-contained terminal checker is
\begin{quote}\small
\texttt{python3 }\path{evidence/r3472_exclusion_20261022/terminal/check.py}.
\end{quote}
It verifies $1648$ exact integer bound deductions and the final rational
separator; the complete package also checks the categorical reduction,
domain coverage and construction of the necessary system.
'''
    (PAPER/'m3_continuation.tex').write_text(text)
    (PAPER/'m3_criteria.tex').write_text((ROOT/EVIDENCE/'criteria/criteria_m3.tex').read_text().replace('Certified subrings and a compositum compression criterion','Certified subrings and compositum compression'))
    (PAPER/'m3_convex.tex').write_text(normalize((ROOT/EVIDENCE/'criteria/global_convex_m3.tex').read_text()))
    for name in ('module','positivity','biquadratic'):shutil.copy2(ROOT/f'tools/templates/rank8_m3_{name}.tex',PAPER/f'm3_{name}.tex')
    structural='\n'.join((ROOT/EVIDENCE/p).read_text() for p in ('models/psl2_11/structural_m3.tex','pipeline/structural_m3.tex','models/d90_structural.tex'))
    if ext.get('frontier') and 'R8_3_731' in set(ext['frontier']['resolved_ids']):
        structural=structural.replace('A restricted dimension-660 candidate', 'Earlier dimension-660 screening')
        structural=structural.replace('The residual ring $R8\\_3\\_731$', 'The ring $R8\\_3\\_731$')
        structural=structural.replace('General complex categorification remains unresolved.',
            r'These were the original restricted tests. The present continuation excludes general complex categorification as well; see Section~\ref{sec:rank8-a5-complement}.')
    if 'R8_3_436' in ext['unitary_excluded_ids']:
        structural+='\n'+(ROOT/EVIDENCE/'models/r436_unitary_scope.tex').read_text()
    if 'R8_3_455' in ext['unitary_excluded_ids']:
        structural+='\n'+(ROOT/EVIDENCE/'models/r455_unitary_scope.tex').read_text()
    (PAPER/'m3_structural.tex').write_text(normalize(structural))
    constructions=(ROOT/'tools/templates/rank8_m3_known_models.tex').read_text()+'\n'+(ROOT/EVIDENCE/'models/new_constructions.tex').read_text().replace('{CMS}','{CMSIzumiXu}').replace('{Izumi}','{IzumiNear}')
    if 'R8_3_3342' in {r['id'] for r in models}:constructions+='\n\\subsection{A twisted group-theoretical construction}\n'+(ROOT/EVIDENCE/'models/psl2_11/r360/manuscript.tex').read_text()
    if 'R8_3_721' in model_ids:
        constructions+='\n'+(ROOT/'evidence/rank8_next_20261021/r721/r721_qsystem_model.tex').read_text()
        constructions=constructions.replace('The exhaustive crosswalk is\n'+
            r'\path{evidence/rank8_next_20261021/r721/census_dimension_crosswalk.py}.',
            'The exhaustive crosswalk is\n'+r'\begin{quote}\small\path{evidence/rank8_next_20261021/r721/census_dimension_crosswalk.py}.\end{quote}')
    (PAPER/'m3_models.tex').write_text(normalize(constructions))
    (PAPER/'m3_model_search.tex').write_text(normalize((ROOT/EVIDENCE/'models/model_search_scope.tex').read_text()))
    path=PAPER/'rank8.tex';s=path.read_text()
    if r'\newtheorem{example}' not in s:
        s=s.replace(r'\newtheorem{remark}[theorem]{Remark}',r'\newtheorem{remark}[theorem]{Remark}'+'\n'+r'\newtheorem{example}[theorem]{Example}')
    s=re.sub(r'pdftitle=\{Rank-eight Grothendieck rings: [^}]+\}','pdftitle={Rank-eight Grothendieck rings: categorification through multiplicity three}',s)
    s=s.replace('complete classification through multiplicity two}','categorification through multiplicity three}')
    s=re.sub(r'\\date\{[^}]+\}',lambda _:r'\date{22 October 2026}' if ext.get('research') else r'\date{21 October 2026}',s)
    abstract=(f'We investigate complex categorification of the supplied $4500$ rank-eight fusion rings of multiplicity at most three. The exact-multiplicity-three continuation treats $3527$ new tensors: ${ext["excluded"]}$ general exclusions, ${ext["unitarily_realized"]}$ unitary models, and ${ext["unresolved"]}$ unresolved cases. '
      'The complete classification through multiplicity two is preserved: $896$ exclusions and $77$ unitary models. Unified obstructions combine signed sphericalization, full character-labeled central induction, modular symmetry and rotations, integer central restriction and cubic fusion constraints, and module-category and Morita arguments. Positive constructions include group representations, near-group equivariantizations, exceptional subfactor categories, a twisted group-theoretical category and Morita duals. An inherited generalized-Haagerup Q-system realizes $\\sha{R8_3_721}$, using a categorical vertex obstruction, exact coefficient bounds and uniqueness in the supplied complete census. Tensor comparisons and exact replay certificates accompany the constructions; individual attempt inventories record the unresolved cases.')
    if ext.get('research'):
        abstract=abstract.replace('Tensor comparisons and exact replay certificates accompany the constructions; individual attempt inventories record the unresolved cases.',
          'Pointed-induction Fourier criteria exclude $\\sha{R8_3_65}$ and $\\sha{R8_3_1795}$ in every pointed associator class. Every remaining categorification admits a spherical structure and has a pseudo-unitary Galois conjugate; none can have a braided Morita representative. Tensor comparisons and exact replay certificates accompany these results.')
    if ext.get('creative'):
        abstract=abstract.replace('Pointed-induction Fourier criteria',
          'The triality-zero component of the known unitary $E_{21}$ category for $SU(3)_{21}\\subset(E_7)_1$ realizes $\\sha{R8_3_982}$ by an exact comparison of all $512$ fusion coefficients. Pointed-induction Fourier criteria')
        if by_id['R8_3_3472']['status']=='excluded':
            abstract=abstract.replace('Tensor comparisons and exact replay certificates accompany these results.',
              'A complete center-frame and Galois twist-orbit reduction, followed by an exact integer rotation certificate, excludes $\\sha{R8_3_3472}$ over $\\mathbb C$. The terminal contradiction replays with rational arithmetic and no optimization solver. Tensor comparisons and exact replay certificates accompany these results.')
        elif (ROOT/'evidence/r3472_focus_20261022/manuscript.tex').is_file():
            abstract=abstract.replace('Tensor comparisons and exact replay certificates accompany these results.',
              'For $\\sha{R8_3_3472}$, every Morita partner has one or seven invertible simples, with precisely two possible based rings in the seven-invertible case. Direct Radchenko--Wheeler parent quotients remain impossible after arbitrary pointed stabilization. These restrictions and maximal third indicators leave the ring unresolved. Tensor comparisons and exact replay certificates accompany these results.')
    s=re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}',lambda _:r'\begin{abstract}'+'\n'+abstract+'\n'+r'\end{abstract}',s,flags=re.S)
    replacements={
      'all $877$ of exact multiplicity two.':'all $877$ of exact multiplicity two, and the supplied extension adds $3527$ of exact multiplicity three.',
      'every rank-eight subring in this manuscript also has multiplicity at most two.':'every rank-eight subring in this historical multiplicity-two stage also has multiplicity at most two.',
      'and the two remaining unresolved rank-six cases. Run':'and the complete current unresolved inventory. Run',
      'The rank-eight full-certificate audit covers all $973$ input tensors,':'The historical rank-eight multiplicity-two full-certificate audit covers all $973$ input tensors,',
      'The source is the public \\emph{Fusion Ring Census}':'The historical multiplicity-two source is the public \\emph{Fusion Ring Census}',
      'Rank-seven Grothendieck rings: a complete classification through multiplicity four':'Rank-seven Grothendieck rings: a complete classification through multiplicity five',
      'This work does\nnot certify a multiplicity-three census or classify categories up to\ntensor equivalence. Nothing here implies that no new criterion is needed\nbeyond multiplicity two.':'The multiplicity-three input is checked as described in Section~\\ref{sec:m3-continuation}; exhaustive enumeration is not independently rerun. This work does not classify categories up to tensor equivalence or claim that no further criterion is needed.'}
    for old,newtext in replacements.items():s=s.replace(old,newtext)
    if r'\input{m3_continuation}' not in s:s=s.replace(r'\section{Necessary criteria and their exact application}',r'\input{m3_continuation}'+'\n\n'+r'\section{Historical multiplicity-two criteria and their exact application}')
    for key,entry in BIB.items():
        item=r'\bibitem{'+key+'} '+entry+'\n'
        pattern=r'\\bibitem\{'+re.escape(key)+r'\}.*?(?=\\bibitem|\\end\{thebibliography\})'
        s,count=re.subn(pattern,lambda _:item,s,flags=re.S)
        if not count:s=s.replace(r'\end{thebibliography}',item+r'\end{thebibliography}')
    path.write_text(s);mirror=ROOT/'supplements/rank8/paper';mirror.mkdir(parents=True,exist_ok=True)
    from audit_corrections_20261024 import active as audit_active, revise_generated_tex
    if audit_active(ROOT):
        for source in PAPER.glob('*.tex'):
            source.write_text(revise_generated_tex(source.name,source.read_text(),ROOT))
    for p in PAPER.glob('*.tex'):shutil.copy2(p,mirror/p.name)
    print(json.dumps({'status':'PASS','new_models':len(models),'new_exclusions':ext['excluded'],'unresolved':ext['unresolved']},indent=2))
if __name__=='__main__':main()
