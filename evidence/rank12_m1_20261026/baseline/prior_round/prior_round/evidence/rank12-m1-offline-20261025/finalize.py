"""Build the offline ledger, research report and orderly portable package inputs."""
from pathlib import Path
import collections,csv,hashlib,json,platform
from state import current
ROOT=Path(__file__).resolve().parent

def main():
    ex,models=current();tensors=json.loads((ROOT/'tensors.json').read_text());P={r['id']:r for r in json.loads((ROOT/'profile.json').read_text())['records']}
    stages=[('Arithmetic / near-group','arithmetic.json'),('Cyclic isotypic summands','cyclic.json'),('Zero spectrum','spectra.json:zero_spectrum'),('Central field / dimension order','field_checks.json'),('Primary-3 with solvability gate','primary_full.json'),('Liptrap monomial obstruction','feudal.json'),('Replayed lower-rank exclusions','lower_known.json')]
    assigned={};stage_counts={}
    for label,source in stages:
        ids=[rid for rid,ev in ex.items()if rid not in assigned and any(e['source']==source for e in ev)]
        for rid in ids:assigned[rid]=label
        stage_counts[label]=len(ids)
    if len(assigned)!=len(ex):raise ValueError('every exclusion has an independently checked route')
    records=[];constructor_counts=collections.Counter()
    for rid,N in tensors.items():
        p=P[rid];status='excluded'if rid in ex else'unitarily_realized'if rid in models else'unresolved'
        ms=models.get(rid,[]);first=ms[0]if ms else None
        kind=first.get('constructor',first.get('kind'))if first else None
        if kind:constructor_counts[kind]+=1
        records.append(dict(id=rid,input_line=p['line'],rank=12,multiplicity=1,tensor_sha256=p['tensor_sha256'],status=status,commutative=p['commutative'],simple=p['simple'],exclusion_route=assigned.get(rid),exclusion_evidence=ex.get(rid,[]),model_name=first.get('name','Liptrap generalized Tambara-Yamagami reconstruction')if first else None,model_constructor=kind,model_certificate_count=len(ms)))
    summary=dict(input_count=632,excluded=len(ex),modeled=len(models),unresolved=632-len(ex)-len(models),input_uncompressed_sha256=json.loads((ROOT/'profile.json').read_text())['input_sha256'],stage_counts=stage_counts,preferred_model_constructor_counts=dict(constructor_counts),scope='Supplied rank-12 multiplicity-one rings; established-method pass with short discovery limits; arbitrary complex categorification for accepted exclusions; unitary existence for positives; no uniqueness of associators claimed.',online_revision_performed=False)
    if(summary['excluded'],summary['modeled'],summary['unresolved'])!=(393,127,112):raise ValueError('unexpected final totals')
    (ROOT/'ledger.json').write_text(json.dumps(dict(summary=summary,records=records),indent=2)+'\n')
    with (ROOT/'ledger.csv').open('w',newline='')as f:
        keys=['id','input_line','status','commutative','simple','exclusion_route','model_name','model_constructor','tensor_sha256'];w=csv.DictWriter(f,keys);w.writeheader();w.writerows({k:r.get(k)for k in keys}for r in records)
    unresolved=[dict(id=r['id'],tensor_sha256=r['tensor_sha256'],tensor=tensors[r['id']])for r in records if r['status']=='unresolved']
    (ROOT/'unresolved_tensors.json').write_text(json.dumps(unresolved,separators=(',',':'))+'\n')
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    fam=json.loads((ROOT/'unresolved_families.json').read_text());by=collections.defaultdict(list)
    for r in fam['records']:by[r['family']].append(r['id'])
    family_rows=[
      ('D120',r'$1^{\times4},2^{\times4},5^{\times4}$'),
      ('D48',r'$1^{\times8},2^{\times2},4^{\times2}$'),
      ('cubic_C7',r'$1^{\times8},(2a)^{\times2},(2a^2-2)^{\times2}$'),
      ('cubic_C9',r'$1^{\times4},2^{\times2},(1+2b)^{\times4},(2b^2-2)^{\times2}$'),
      ('quadratic_C2',r'$1^{\times2},(4+3\sqrt2)^{\times8},(5+3\sqrt2)^{\times2}$'),
      ('D144',r'$1^{\times2},2,3^{\times2},4^{\times3},(3\sqrt2)^{\times4}$'),
      ('D32',r'$1^{\times8},2^{\times2},(2\sqrt2)^{\times2}$'),
      ('D24',r'$1^{\times8},2^{\times4}$'),
      ('D40',r'$1^{\times4},2^{\times4},(\sqrt5)^{\times4}$'),
      ('quadratic_C6_sqrt10',r'$1^{\times6},(3+\sqrt{10})^{\times6}$'),
      ('quadratic_C6_sqrt13',r'$1^{\times6},((3+\sqrt{13})/2)^{\times6}$')]
    family_table='\n'.join(f'{label} & {len(by[name])} \\\\'for name,label in family_rows)
    ids_table='\n'.join(r'\texttt{'+name.replace('_',r'\_')+r'} & '+', '.join(rid.rsplit('_',1)[1]for rid in by[name])+r' \\'for name,label in family_rows)
    stage_table='\n'.join(f'{label} & {count} \\\\'for label,count in stage_counts.items())
    model_labels={
      'deligne_product':'Deligne products',
      'associative_C2_zest':r'Associative $C_2$ zesting',
      'liptrap_unitary_model':'Generalized Tambara--Yamagami (Liptrap)',
      'graded_pullback':'Graded pullbacks with Ising',
      'twisted_group_theoretical_c2':'Twisted group-theoretical categories',
      'ty_cyclic_equivariant':'TY equivariantizations',
      'su2':r'$\mathrm{SU}(2)$ and $\mathrm{PSU}(2)$',
      'pointed_group':'Pointed categories: nonabelian groups',
      'dihedral_rep':'Dihedral/dicyclic representation categories',
      'half_even_metaplectic':'Half even-metaplectic category',
      'odd_metaplectic':'Odd metaplectic category',
      'metaplectic_character_crossed_product':'Metaplectic crossed product',
      'group_theoretical':'Untwisted group-theoretical category',
      'haagerup_izumi_cyclic':r'Generalized Haagerup $C_6$',
      'pointed_equivariant':'Pointed equivariantization',
      'pointed':'Pointed category: abelian group',
      'ty':'Tambara--Yamagami category'}
    model_table='\n'.join(model_labels[kind]+' & '+str(count)+r' \\'for kind,count in sorted(constructor_counts.items(),key=lambda kv:-kv[1]))
    tex=r'''\documentclass[11pt]{article}
\usepackage[a4paper,margin=23mm]{geometry}
\usepackage[T1]{fontenc}\usepackage{lmodern,microtype}
\usepackage{amsmath,amssymb,booktabs,longtable,array,hyperref,fancyhdr}
\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{Rank 12, multiplicity one}\fancyhead[R]{Offline screening}\fancyfoot[C]{\thepage}
\widowpenalty=10000\clubpenalty=10000
\setlength{\headheight}{14pt}\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\newcommand{\FPdim}{\operatorname{FPdim}}\newcommand{\VEC}{\operatorname{Vec}}
\title{Rank-twelve multiplicity-one fusion rings\\\large Screening by established theoretical methods}
\author{Offline research record}\date{25 October 2026}
\begin{document}\maketitle
\begin{center}\small AI-generated research; independent human verification remains pending.\end{center}
\section{Result and scope}
For the supplied list of 632 based rings, the present established-method pass gives
\[
\boxed{632=393\ \text{excluded}+127\ \text{unitarily realized}+112\ \text{unresolved}.}
\]
Every accepted exclusion concerns arbitrary fusion categories over $\mathbb C$.
Every positive record supplies a categorical construction and an exact identification of
all $12^3=1728$ structure constants. The numbers count based rings admitting a
categorification, not tensor-equivalence classes of fusion categories. A necessary-test
pass or an unsuccessful construction search is never counted as a realization.

No repository or website has been revised. The input census was not rerun. IDs
$\mathrm{R12\_1\_i}$ refer to one-based physical input lines; basis labels in the code
are zero-based, with unit label zero. The uncompressed input has SHA-256
\begin{center}\scriptsize\texttt{6949e6fb8afd23f80b54e5a546a0dd34257430fd26c26b7acd8ff8444252f4d7}.\end{center}
All fusion axioms and pairwise nonisomorphism were checked. There are 374 commutative
and 258 noncommutative rings, 204 weakly integral rings, and five pointed rings.
A separate C++ verifier also found exactly 632 distinct associative rings and no duplicates.

\subsection*{Disjoint accounting of exclusions}
Overlapping witnesses are retained. The following display assigns each excluded ring
to its first listed route so that every ring is counted once.
\begin{center}\begin{tabular}{lr}\toprule Route & New exclusions\\\midrule
@STAGES@
\midrule Total & 393\\\bottomrule\end{tabular}\end{center}
The lower-rank transfer step replays six additional accepted results: the three
Liptrap obstructions $\mathrm{R10\_1\_118,122,180}$, the dimension-field/order obstructions
$\mathrm{R6\_1\_12,13}$, and the general signed proof for $\mathrm{R8\_1\_17}$.
Each transfer checks product and dual closure and the full embedded tensor.

\section{Theoretical exclusion checks}
The inventory covers the established criterion families used here and explains their scope.
The complete attempt records also retain tests that gave no conclusion.

\textbf{Arithmetic and support.}\par
Formal codegrees must be d-numbers \cite{Ostrik}. The regular Casimir has eigenvalues
$e_Ef_E$, where $e_E$ is an irreducible representation degree; multiplication by a
rational integer preserves the d-number property. The code checks the monic minimal
polynomial divisibilities exactly. Cyclotomicity is used for simple FP dimensions and,
on commutative input, all fusion-matrix eigenvalues. For a noncommutative ring we do
not assume that every regular-matrix eigenvalue is cyclotomic. Near-group and
two-dimension restrictions use their precise hypotheses \cite{Schopieray}.
The zero- and one-spectrum tests are support consequences of the pentagon equation
\cite{TPE}; all accepted witnesses are reevaluated with integers.

\textbf{Cyclic isotypic integrality.}\par
Let $g$ have order $n$, with $gX=X$, $Yg=Y$, and $gZ=Zg=Z$. If $m=N_{XY}^Z>0$,
then $m\FPdim(Z)/n$ is an algebraic integer. Indeed, a fixed simple object trivializes
the associator class on $\langle g\rangle$; its regular algebra $A$ exists.
The $Z$-isotypic summand of $X\otimes Y$ is an $A$-bimodule, whose FP dimension is
$m\FPdim(Z)/\FPdim(A)$. This argument uses no pivotality. The present multiplicities
are one. The checker isolates the Perron factor and proves nonintegrality of the
scaled monic polynomial. There are 208 witnesses, including overlaps.

\textbf{Subcategory index and central dimension order.}\par
For every proper based subring, $\FPdim(R)/\FPdim(S)$ must be an algebraic integer
\cite{EGNO}. Exact positive dimension characters and all 4012 proper embeddings are
retained. For weakly integral rings, or rings with exactly two FP values after the
Galois-pseudo-unitary reduction of \cite[Lemma 3.1]{Schopieray}, a distinguished central
simple has dimension $D/f_E$. Its forgotten dimension lies in the integer span of the
source dimensions. Thus every Casimir root must belong to that dimension field.
For a root $\lambda=e_Ef_E$, the candidate $e_ED/\lambda$ must lie in the dimension
order and have unit multiplicity $e_E$. Hermite normal form checks the order exactly;
noncommutative regular multiplicities must be sums of allowed squares $e_E^2$.
No pseudo-unitary conclusion is drawn without an explicit bridge.

\textbf{Unitary tests and their bridge.}\par
The primary-3 matrix is
\[
P_3=\sum_i\frac{N_i\otimes N_i\otimes N_i}{\FPdim(i)}.
\]
It must be positive semidefinite for a unitary category \cite{HLPW}. Six accepted
negative integer quadratic forms occur at IDs 91, 92, 197, 198, 220 and 221. These
rings have FP dimension 216. Any categorification is solvable by
\cite[Theorem 1.6]{ENOsolv}, hence unitarizable by \cite[Theorem 5.20]{GHR}.
This is why the exclusions are general. The coefficients of each quadratic form are
recomputed by independent integer tensor contractions; rational square-root intervals
certify strict negativity. Floating-point eigensolvers only discover the vectors.

The inherited full-$I(1)$ quadratic-compression, reciprocal-codegree, global twist-moment,
and short involution-module checks produced no additional disjoint exclusions.
Their exact passes or no-conclusion records remain available. No Isaacs conjecture,
braided-only classification, or proposed numerical modular datum is used as a general
categorification obstruction.

\section{Models and categorical hypotheses}
The preferred recorded constructions are distributed as follows; alternative models
are also retained. The replay checks 402 recorded model certificates/identifications.
\begin{center}\small\begin{tabular}{lr}\toprule Constructor & Rings\\\midrule
@MODELS@
\midrule Total &127\\\bottomrule\end{tabular}\end{center}
The standard families include pointed categories for all five groups of order 12,
$\mathrm{SU}(2)_{11}$, $\mathrm{PSU}(2)_{22}$, $\mathrm{PSU}(2)_{23}$, dihedral and
dicyclic representation categories, odd metaplectic and half even-metaplectic
categories \cite{Metaplectic}, Tambara--Yamagami categories, and all relevant
products of the accepted lower-rank multiplicity-one models.

\textbf{Equivariantization and zesting.}\par
Pointed actions are actual group automorphisms. TY actions preserve an explicitly
displayed nondegenerate symmetric bicharacter; both allowed parity coherences are
checked. Fusion coefficients are computed by exact stabilizer Fourier projection
\cite{Equiv}. A based-ring automorphism alone is not accepted as a tensor action.
For associative $C_2$ zesting \cite{Zesting}, the order-two current has a specified
central lift and lies in the neutral component. The 2-cocycle is $h^{ab}$.
For self-braiding $+1$ the scalar associator correction is trivial; for $-1$ it is
$i^{abc}$, whose coboundary cancels $(-1)^{abcd}$. The retained records identify
the relevant boson or fermion and the actual grading.

\textbf{Graded pullbacks and crossed products.}\par
For an accepted unitary rank-eight category with a $C_2$ grading having four simples
in each component, take the full subcategory of its product with Ising on pairs
of matching degrees. This gives twelve simples. Its existence follows directly from
closure under tensor product and duality. Additional crossed products start with
$\mathrm{TY}(C_5)^{C_2}$: multiplying equivariance by the nontrivial character on
the TY-odd component is an actual strict order-two tensor autoequivalence. The
canonical central $\mathrm{Rep}(C_2)$ boson is preserved, permitting the recorded
crossed products and zests.

\textbf{Group-theoretical categories.}\par
The constructions are $\mathcal C(G,\omega,H,1)$, the bimodule categories of the
separable subgroup algebra in $\VEC_G^\omega$. Quotient cocycles are checked before
use. For $H=C_2$, explicit graded bimodule actions and balanced relative tensor
quotients are constructed with fourth-root phases. All left, right, compatibility,
and quotient-descent equations are checked. Stabilizers are trivial or $C_2$, so
their one or two projective characters exhaust the simples. An independent
rank-eight twisted-bimodule control is reproduced exactly. The untwisted convolution
and balanced-bimodule implementations also agree on their common cases.

\textbf{Generalized Haagerup.}\par
$\mathrm{R12\_1\_326}$ is the standard generalized Haagerup $C_6$ based ring:
$g_ag_b=g_{a+b}$, $g_aX_b=X_{a+b}$, $X_ag_b=X_{a-b}$, and
$X_aX_b=g_{a-b}+\sum_cX_c$. Existence of actual unitary categories is recorded in
\cite[Example 4.5]{GI}; the numerical modular-data conjecture in that paper is
not needed. The full input tensor is matched exactly. The two categorical examples
in that reference count as one based ring here.

\section{What remains unresolved}
All 112 remaining cases are listed below by their exact FP dimension pattern.
Superscripts indicate multiplicities of dimensions. Put $a=2\cos(\pi/7)$ and
$b=2\cos(\pi/9)$, the largest roots of $t^3-t^2-2t+1$ and $t^3-3t-1$,
respectively. These patterns were verified as exact positive dimension characters,
not inferred from rounded eigenvalues.
\begin{center}\small\begin{tabular}{p{124mm}r}\toprule FP dimensions & Cases\\\midrule
@FAMILIES@
\midrule Total&112\\\bottomrule\end{tabular}\end{center}
The corresponding suffixes $i$ in $\mathrm{R12\_1\_i}$ are:
\begin{center}\small\begin{longtable}{@{}p{44mm}p{112mm}@{}}\toprule Family key&Input suffixes\\\midrule\endhead
@IDS@
\bottomrule\end{longtable}\end{center}
The JSON and CSV ledgers supply every ID, tensor hash and route; the separate unresolved
tensor file is ready for further work. There are only two simple based rings in this
input: $\mathrm{R12\_1\_116}$ is realized by $\mathrm{PSU}(2)_{23}$ and
$\mathrm{R12\_1\_118}$ fails the d-number test (factor $t^2-935t+1785$).
This observation is not a proof of an unrestricted-rank classification.

\section{Verification and explicit limitations}
\texttt{python verify.py} and \texttt{python -O verify.py} both pass. All 632 input
bindings, 4012 closed subring embeddings, accepted exclusion witnesses and all
402 recorded model certificates/identifications are checked. The accepted replay
uses Python, NumPy, SymPy and NetworkX, takes seconds on the recorded machine,
and requires neither a network service nor a discovery solver. The independent
C++ input audit is retained separately. Algebraic-number arithmetic is shared
infrastructure; this is not a Lean formalization or a substitute for independent
human verification of the categorical references and inherited proofs.

The short module scan uses fixed rank at most four, at most two generators and at most
4096 generator assignments, with a short per-involution time limit. The exploratory
commutative low-induction scan has column/combination node limits and a one-second
continuation limit; an interrupted initial attempt is retained as research history,
not a proof. Numerical primary searches can also give no conclusion. The inherited
complete oriented signed engine has rank at most eight and is used only inside an
already proved rank-eight subring, not silently extended to twelve.

No long induction-frame, conductor, modular-data, higher-indicator or pentagon search
was undertaken. The inventory distinguishes these uncompleted systems from exact
passes. The remaining list means unresolved by this established-method pass under
the requested short-computation constraint. It is not a claim that every consequence
of the literature or every possible established construction has been exhausted.
The constructions here use established methods; no novelty up to tensor equivalence
is claimed.

\begin{thebibliography}{99}\footnotesize\setlength{\itemsep}{2pt}\setlength{\parskip}{0pt}
\bibitem{Ostrik} V.~Ostrik, \emph{On formal codegrees of fusion categories}, Math. Res. Lett. 16 (2009), 895--901. \href{https://arxiv.org/abs/0810.3242}{arXiv:0810.3242}.
\bibitem{EGNO} P.~Etingof, S.~Gelaki, D.~Nikshych and V.~Ostrik, \emph{Tensor Categories}, AMS, 2015, especially Chapters 7--8.
\bibitem{Schopieray} A.~Schopieray, \emph{Categorification of integral group rings extended by one dimension}, J. London Math. Soc. 108 (2023), 1617--1641. \href{https://arxiv.org/abs/2208.07319}{arXiv:2208.07319}.
\bibitem{TPE} Z.~Liu, S.~Palcoux, Y.~Ren and G.~Vercleyen, \emph{Triangular Prism Equations and Categorification}. \href{https://arxiv.org/abs/2203.06522}{arXiv:2203.06522}, Theorems 6.7--6.8.
\bibitem{HLPW} L.~Huang, Z.~Liu, S.~Palcoux and J.~Wu, \emph{Complete Positivity of Comultiplication and Primary Criteria for Unitary Categorification}. \href{https://arxiv.org/abs/2210.00792}{arXiv:2210.00792}.
\bibitem{ENOsolv} P.~Etingof, D.~Nikshych and V.~Ostrik, \emph{Weakly group-theoretical and solvable fusion categories}. \href{https://arxiv.org/abs/0809.3031}{arXiv:0809.3031}, Theorem 1.6.
\bibitem{GHR} C.~Galindo, S.-M.~Hong and E.~C.~Rowell, \emph{Generalized and quasi-localizations of braid group representations}. \href{https://arxiv.org/abs/1105.5048}{arXiv:1105.5048}, Theorem 5.20.
\bibitem{Liptrap} J.~Liptrap, \emph{Generalized Tambara--Yamagami categories}. \href{https://arxiv.org/abs/1002.3166v2}{arXiv:1002.3166v2}, Definition 4.3, Theorem 4, Lemma 5.4. The retained feudal certificates give 21 unitary models and four arbitrary-complex obstructions.
\bibitem{Equiv} S.~Burciu and S.~Natale, \emph{Fusion rules of equivariantizations of fusion categories}. \href{https://arxiv.org/abs/1206.6625v2}{arXiv:1206.6625v2}.
\bibitem{Zesting} C.~Delaney, C.~Galindo, J.~Y.~Plavnik, E.~C.~Rowell and Q.~Zhang, \emph{Braided zesting and its applications}. \href{https://arxiv.org/abs/2005.05544}{arXiv:2005.05544}.
\bibitem{Metaplectic} P.~Gustafson, E.~C.~Rowell and Y.~Ruan, \emph{Metaplectic Categories, Gauging and Property F}. \href{https://arxiv.org/abs/1808.00698}{arXiv:1808.00698}, Sections 3.1 and 3.3.
\bibitem{GI} P.~Grossman and M.~Izumi, \emph{Drinfeld centers of fusion categories arising from generalized Haagerup subfactors}, Quantum Topol. 13 (2022), 593--668. \href{https://arxiv.org/abs/1501.07679v2}{arXiv:1501.07679v2}, Example 4.5.
\end{thebibliography}
\end{document}
'''
    for token,value in [('@STAGES@',stage_table),('@MODELS@',model_table),('@FAMILIES@',family_table),('@IDS@',ids_table)]:tex=tex.replace(token,value)
    (ROOT/'report.tex').write_text(tex)
    (ROOT/'README.md').write_text('''# Rank 12, multiplicity one: established-method offline pass

**632 supplied rings = 393 excluded over C + 127 unitarily realized + 112 unresolved.**

No GitHub repository or website was modified. Results concern based rings, not a count of tensor-equivalence classes. Independent human verification remains pending.

## Read first

- `report.pdf` / `report.tex`: conclusions, theoretical scope, precise limits and references.
- `ledger.csv`: one readable decision per permanent physical input line.
- `ledger.json`: hashes, all overlapping exclusion evidence and preferred construction.
- `unresolved_tensors.json`: all 112 remaining based tensors.
- `unresolved_families.json`: independently checked exact positive dimension characters.
- `verification.json`, `verification_optimized.json`: successful complete accepted-witness replays.

## Exact replay (short; no network or discovery solver)

Python 3.10 or newer, NumPy, SymPy and NetworkX are needed. Install `requirements.txt`, preserve this extracted layout, and run:

```sh
python verify.py
python -O verify.py
```

The complete accepted replay checks the source bindings and fusion axioms, every stored closed subring embedding, accepted arithmetic/support/cyclic/central-order/primary/Liptrap witnesses, the inherited lower-rank proofs, all 127 positive rings and all 402 recorded model identifications. Some standard algebraic-number infrastructure and standard tensor constructors are shared: independent witness checks do not mean an independent formalization of every referenced categorical theorem.

The C++ canonical input audit is in `independent_input/output`. Its source is `sources/census_verifier/verify_tables.cpp`; recompile it and feed the decompressed original table file to repeat that separate check. It found exactly 632 associative distinct based rings, with no duplicates. The input archive's own verification and provenance remain in `input/rank12_M1_verified`.

## Evidence and code

All tensors use N[i][j][k], coefficient of b_k in b_i*b_j. The unit is b_0. IDs R12_1_i use one-based physical lines and have not been reordered.

`arithmetic.json`, `subrings.json`, `cyclic.json`, `spectra.json`, `field_checks.json`, `primary_full.json`, `feudal.json`, and `lower_known.json` contain accepted witnesses and exact attempt records. `models.json`, `additional_models.json`, `group_models.json`, and `twisted_c2_models.json` contain explicit constructions, full model tensors and basis maps. `lower_rank*.json` and `sources/` preserve the accepted lower-rank premises and implementation snapshots.

`modules.json`, `induction.json`, reduced primary results and construction attempt inventories include feasible relaxations, search limits and unsuccessful candidates. These are never exclusion or existence proofs. In particular, a failed finite phase search is not a complex obstruction; the accepted negative Liptrap records cancel arbitrary nonzero complex variables by integer monomial relations. The ordinary and optimized witness replays do not rerun discovery.

The discovery scripts are included for transparency. They are separate from `verify.py` and may overwrite attempt receipts when deliberately rerun. The low-induction script resumes its bounded attempt ledger. Its initial interrupted log is historical research output, not a completed campaign. There is no long frame, conductor, modular-data or numerical pentagon search in this package.

All general exclusions using unitary positivity carry the proved solvability/unitarizability bridge. Two-FP-value Galois-pseudo-unitarity is not assumed to imply unitarity. No Isaacs conjecture or braided-only classification is promoted to a general exclusion.

`MANIFEST.sha256` binds the delivered snapshot. Generated verification times can change on replay. This is an offline established-method pass; the remaining 112 cases have not been declared impossible, and no novelty up to tensor equivalence is claimed for the recorded constructions.
''')
    (ROOT/'requirements.txt').write_text('numpy>=1.24\nsympy>=1.12\nnetworkx>=3.0\n# Discovery only, not needed by the accepted witness replay:\nscipy>=1.10\n')
    (ROOT/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),platform=platform.platform()),indent=2)+'\n')
    print('Final ledger',summary['excluded'],summary['modeled'],summary['unresolved'])
if __name__=='__main__':main()
