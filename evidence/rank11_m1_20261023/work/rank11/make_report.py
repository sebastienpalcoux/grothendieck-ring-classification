"""Build the review report from the accepted ledger and proof sections."""
from pathlib import Path
import json,collections,re
HERE=Path(__file__).resolve().parent
OUT=HERE/'report';OUT.mkdir(exist_ok=True)
L=json.loads((HERE/'ledger.json').read_text())
counts=L['counts']
def tex(x):
    return str(x).replace('\\',r'\textbackslash{}').replace('_',r'\_').replace('&',r'\&').replace('%',r'\%').replace('#',r'\#')
names={
1:r'$\operatorname{Rep}(D_{32})$',10:r'$\operatorname{TY}(C_{12})^{C_2}$, positive parity',
24:r'$\mathrm{SU}(2)_6^{C_2}$, odd parity coherence',26:r'$\mathrm{SU}(2)_{10}$',28:r'$\mathrm{PSU}(2)_{20}$',
30:r'$\mathrm{SO}(8)_2$',37:r'$\mathrm{SO}(15)_2$',45:r'$\operatorname{Rep}(D_{38})$',46:r'$\mathrm{PSU}(2)_{21}$',
48:r'$\mathrm{Vec}_{C_{16}}^{\omega_1}$, equivariantized by $a\mapsto15a$',
57:r'$V_4$ zest of $\mathrm{SO}(8)_2$, parameters $(0,0,0,2)$',
64:r'$\operatorname{TY}(C_3\times C_2^2)^{C_2}$, positive parity',
68:r'$\mathrm{SU}(2)_6^{C_2}$, trivial parity coherence',
72:r'$\operatorname{TY}(C_{12})^{C_2}$, negative parity',
75:r'$\operatorname{TY}(C_{15})^{C_2}$, negative parity',
103:r'$C_2$ zest of $\mathrm{SU}(2)_{10}$',
104:r'$\mathcal C(G_{32},\omega,V_4,1)$, nonsplit Jordan construction',
105:r'$V_4$ zest of $\mathrm{SO}(8)_2$, parameters $(0,0,0,1)$',
112:r'$\mathrm{Vec}_{C_{16}}^{C_2}$, action $a\mapsto7a$',
113:r'$\operatorname{TY}(C_3\times C_2^2)^{C_2}$, negative parity',
146:r'$\mathrm{Vec}_{C_{16}}^{\omega_1}$, equivariantized by $a\mapsto7a$',
150:r'$V_4$ zest of $\mathrm{SO}(8)_2$, parameters $(2,0,0,3)$',
157:r'$\operatorname{TY}(C_3^2)^{C_2}$, positive parity',171:r'$\operatorname{TY}(C_{10})$',
176:r'$\operatorname{TY}(C_3^2)^{C_2}$, negative parity',
179:r'Izumi $Q_8$ near-group category, equivariantized by $C_3$',182:r'$\mathrm{Vec}_{C_{11}}$'}
parts=[r'''\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern,microtype,amsmath,amssymb,amsthm,booktabs,longtable,array}
\usepackage[margin=25mm]{geometry}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{enumitem}
\usepackage{xurl}
\usepackage[colorlinks=true,linkcolor=blue!45!black,urlcolor=blue!45!black,citecolor=blue!45!black]{hyperref}
\usepackage{bookmark}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt plus1pt}
\setlength{\emergencystretch}{3em}
\setlist{nosep}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small Rank 11, multiplicity one}
\fancyhead[R]{\small Categorification audit}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{14pt}
\newtheorem{theorem}{Theorem}
\newtheorem{proposition}{Proposition}
\newtheorem{lemma}{Lemma}
\providecommand{\FPdim}{\operatorname{FPdim}}
\providecommand{\Rep}{\operatorname{Rep}}
\providecommand{\Vec}{\operatorname{Vec}}
\providecommand{\BrPic}{\operatorname{BrPic}}
\providecommand{\Irr}{\operatorname{Irr}}
\providecommand{\Hom}{\operatorname{Hom}}
\providecommand{\End}{\operatorname{End}}
\providecommand{\id}{\operatorname{id}}
\providecommand{\Aut}{\operatorname{Aut}}
\providecommand{\rk}{\operatorname{rank}}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\begin{document}
\begin{center}
{\Large\bfseries Rank-eleven multiplicity-one fusion rings}\\[5pt]
{\large Exclusions, coherent models, and exact verification}\\[6pt]
23 October 2026
\end{center}
\section{Result and mathematical scope}
The input consists of 182 physical multiplication-table lines. All 182 satisfy
the fusion-ring axioms, and exact invariant refinement separates every pair.
There are 153 commutative and 29 noncommutative rings. Identifiers
\texttt{R11\_1\_i} always retain physical input line $i$; no sorting or basis
change is allowed to redefine an identifier.
''']
parts.append(r'\begin{center}\begin{tabular}{lr}\toprule Status & Rings\\\midrule'+'\n')
for key,label in [('excluded',r'Excluded over $\mathbb C$'),('unitarily_realized','Unitary realization verified'),('unresolved','Unresolved after recorded attempts'),('in_progress','Still under investigation')]:
    if counts.get(key) or key=='unresolved':parts.append(label+' & '+str(counts.get(key,0))+r'\\'+'\n')
parts.append(r'''\bottomrule\end{tabular}\end{center}
An exclusion proves that no complex fusion category has the indicated based
ring. A model proves existence of a unitary category, including coherence of
the construction and an exact identification of all $11^3=1331$ coefficients.
Neither assertion classifies all possible associators of a realized ring.
No timeout, unsuccessful model search, floating-point test, or failed
relaxation is used to assign an exclusion.

\medskip
\noindent\textbf{AI-generated research \textperiodcentered\ independent verification pending.}
The proofs, code and data were developed with AI assistance. Independent
human verification and Lean formalization remain pending. Exact automated
checks establish only their stated scope.

\begin{theorem}[Classification of the supplied multiplicity-one census]
Of the 182 supplied rank-eleven multiplicity-one fusion rings, exactly 27
admit a fusion categorification over $\mathbb C$. Each admits a unitary
realization. The remaining 155 admit no complex fusion categorification.
\end{theorem}
The theorem concerns based-ring isomorphism classes in the supplied dataset.
Enumeration completeness is producer-reported: every duality stratum
completed and the complete source is supplied, while independent integration
checks establish tensor validity and uniqueness. The full enumeration was
not independently repeated. The census provenance is retained separately in
\url{https://github.com/sebastienpalcoux/fusion-ring-census}.
The canonical manuscript and per-input classification evidence are in
\url{https://github.com/sebastienpalcoux/grothendieck-ring-classification}.

\section{Known criteria and the order of the audit}
The audit first reused the literature and accepted lower-rank project methods:
formal-codegree d-numbers, character-trace cyclotomicity, primitive codegrees,
integral center dimensions, all fusion-subring indices, near-group and
Tambara--Yamagami restrictions, zero/one-spectrum obstructions, cyclic
isotypic integrality, module matrices, and inherited solvability arguments.
It then applied complete signed-sphericalization and scalar-character checks
before the center-dimension and reciprocity refinements. Model searches used
established families before constructing additional coherent actions.

The detailed criterion-by-criterion inventory is
\path{work/rank11/criteria_audit/CRITERIA_AUDIT.md}. It records hypotheses,
sources, implementation boundaries, and conditions which are only unitary or
braided. It covers the surveyed literature and the accepted project corpus;
it does not claim that every conceivable theorem or consequence of the
literature has been algorithmically decided.

The exact arithmetic audit checks 919 proper nontrivial fusion subrings,
286 distinct irreducible field polynomials, and the irreducible algebra-block
decomposition of all 29 noncommutative inputs. Cyclotomicity is checked on
character traces in the noncommutative case. The four arithmetic receipts give
97 excluded inputs. The cyclic test gives 66 exclusions with overlap. The
zero/one-spectrum and module proofs use actual algebra and pentagon
constraints, with independent integer replays. Overlapping proofs are retained
in the ledger and are counted only once.

The signed analysis covers all 59 nonintegral inputs surviving the initial
arithmetic and cyclic tests. It checks every admissible sign branch and every
possible spherical dimension character. In particular, the six mixed
dimension-40 branches are handled directly; they are not assumed
pseudo-unitary. The dimension-lattice and two-character arguments below use
that reduction as an explicit proof dependency.

For the final integral pair, all primary positivity criteria and the
noncommutative Schur-product criterion pass by exact matrix identities.
Nonnegative rational coupling certificates establish all of the tested
Minkowski inequalities for every real $p\geq1$ and every nonnegative input
vector. These are genuine all-parameter passes, not numerical searches for
witnesses. The new graded-extension argument below resolves the pair.
The independent Titsworth--Hagge data crosswalk also checks their rank-eleven
dimension-32 tensor: it is exactly input 30, already realized here.

\subsection{Evidence and reproducibility}
\path{work/rank11/ledger.json} is the per-input record of status, original
tensor hashes, proof files, certificates, and replay commands.
\path{work/rank11/ledger.csv} is its compact human-readable counterpart.
The input hash and mathematical assertions are bound to the original tensor,
not to approximate dimensions or an isomorphism signature alone.
Run the portable replay from the extracted package root:
\begin{quote}\ttfamily
python work/rank11/replay\_all.py
\end{quote}
The accompanying README documents supported options, dependencies and the
recorded complete replay. Discovery programs are kept distinct from accepted
certificate checks. Checks reject mismatches explicitly even under
\texttt{python -O}. The model audit independently reconstructs the highest-risk
coherence equations and fusion coefficients.
''')
parts.append(r'\clearpage\section{Verified models}\small\begin{longtable}{r p{0.84\textwidth}}\toprule Line & One verified realization\\\midrule\endhead'+'\n')
for r in L['records']:
    if r['status']!='unitarily_realized':continue
    n=r['input_line'];name=names.get(n,tex(r['models'][0]['model']))
    parts.append(str(n)+' & '+name+r'\\[3pt]'+'\n')
parts.append(r'''\bottomrule\end{longtable}\normalsize
Here $D_m$ denotes a dihedral group of order $m$. Parameters, exact phases,
basis bijections and source hashes are in the individual model certificates;
the abbreviated names in the table are not the complete construction data.
\clearpage\section{Coherent model constructions}
''')
parts.append((HERE/'known_models/MODELS.tex').read_text())
if (HERE/'known_models/JORDAN.tex').exists():parts.append((HERE/'known_models/JORDAN.tex').read_text())
non=HERE/'nonintegral/NONINTEGRAL.tex'
if non.exists():parts.append(non.read_text())
else:parts.append(r'\section{Nonintegral proofs}\textbf{Draft: proof section not yet assembled.}')
d120=HERE/'criteria_audit/D120.tex'
if d120.exists():
    body=d120.read_text()
    if r'\begin{document}' in body:body=body.split(r'\begin{document}',1)[1].split(r'\end{document}',1)[0].replace(r'\maketitle','')
    parts.append(body)
if (HERE/'integral/C4.tex').exists():parts.append((HERE/'integral/C4.tex').read_text())
pending=[r for r in L['records']if r['status'] in ['in_progress','unresolved']]
if pending:
    parts.append(r'\section{Remaining cases and attempted approaches}')
    parts.append('The remaining input lines are '+', '.join(str(r['input_line'])for r in pending)+'. ')
    attempts=HERE/'integral/ATTEMPTS.tex'
    if attempts.exists():parts.append(attempts.read_text())
    else:parts.append('Their investigation is still in progress; this draft does not classify them as unresolved.\n')
parts.append(r'\section{Complete status index}')
for status,label in [('excluded','Excluded'),('unitarily_realized','Unitary models'),('unresolved','Unresolved'),('in_progress','In progress')]:
    ids=[str(r['input_line'])for r in L['records']if r['status']==status]
    if ids:parts.append(r'\paragraph{'+label+' ('+str(len(ids))+').} '+', '.join(ids)+'.\n')
parts.append(r'''Every number above denotes the suffix in \texttt{R11\_1\_i}. The original
input has uncompressed SHA-256
\begin{quote}\small\ttfamily
3186c410888e0bc7f30c9e423e0184a156\linebreak
18246bc9f4d0ef503e708c4081eff8
\end{quote}
''')
bibs=[]
for p in [HERE/'nonintegral/NONINTEGRAL-bib.tex',HERE/'criteria_audit/D120-bib.tex',HERE/'integral/C4-bib.tex']:
    if p.exists():bibs.append(p.read_text())
if bibs:
    text='\n'.join(bibs);pieces=re.split(r'(?=\\bibitem\{)',text);seen=set();unique=[]
    for piece in pieces:
        m=re.match(r'\\bibitem\{([^}]+)\}',piece)
        if m and m.group(1)not in seen:seen.add(m.group(1));unique.append(piece)
    parts.append(r'\begin{thebibliography}{99}'+'\n'+'\n'.join(unique)+r'\end{thebibliography}')
parts.append(r'\end{document}')
(OUT/'rank11_report.tex').write_text('\n'.join(parts))
print(OUT/'rank11_report.tex')
