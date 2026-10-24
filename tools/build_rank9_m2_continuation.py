"""Integrate accepted proofs into the ordinary rank-nine M2 manuscript."""
from pathlib import Path
import re,subprocess
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'publications/rank9-m2/paper';E=ROOT/'evidence/rank9_m2_20261024/proofs'
sections=[
 ('Cyclic internal-end algebras and multiplicity','phase4/weak_b/CYCLIC_INTERNAL_END_OBSTRUCTION.md'),
 ('A nonsolvable dimension-sixty neutral component','phase4/weak_b/DIMENSION120_A5_OBSTRUCTION.md'),
 ('Cyclic generalized Tambara--Yamagami constructions','phase4/weak_a/CYCLIC_TY_MODELS.md'),
 ('An order-four cover and a coherent descended action','phase4/weak_a/MR_1254_MODEL.md'),
 ('Complete group-theoretical obstructions in dimensions 120 and 168','phase4/integral/GROUP_THEORETICAL_OBSTRUCTIONS.md'),
 ('Fermion parity and solvable descent in dimension 120','phase5/integral120/THEORY.md'),
 ('Odd central dimensions and the dimension-504 ring','phase5/case941/EXCLUSION_THEOREM.md'),
 ('A forced Lagrangian subcategory in dimension 168','phase5/integral168/GENERAL_EXCLUSION.md'),
 ('An isotropic orbifold model for R9_2_1848','phase5/quadratic_noncomm/REPORT.md')]
def literal_operators(text):
    """Keep ASCII mathematical operators out of Markdown emphasis syntax."""
    out=[];fenced=False;display=False
    for line in text.splitlines():
        if line.lstrip().startswith('```'):fenced=not fenced;out.append(line);continue
        if line.strip().startswith(('\\[','\\begin{')):display=True
        if fenced or display:
            out.append(line)
            if line.strip().startswith(('\\]','\\end{')):display=False
            continue
        line=re.sub(r'\*\*([^*]+)\*\*',r'\1',line)
        chunks=re.split(r'(`[^`]*`|\$[^$]*\$|\\\(.*?\\\))',line)
        for i in range(0,len(chunks),2):chunks[i]=re.sub(r'(?<!\\)([_*^])',r'\\\1',chunks[i])
        out.append(''.join(chunks))
    return '\n'.join(out)
parts=[]
for title,name in sections:
    s=(E/name).read_text();s=re.sub(r'^# [^\n]*\n','',s,count=1)
    if name.endswith('GROUP_THEORETICAL_OBSTRUCTIONS.md'):s=s.split('## 6. R9_2_941')[0]
    if name.endswith('quadratic_noncomm/REPORT.md'):s=s.split('## R9_2_1975:')[0]
    for marker in ('## Replay','## Reproducible arithmetic','## 6. Reproducible arithmetic','## 6. Exact replay'):
        s=s.split(marker)[0]
    s=s.replace("c_z(m)^2=chi(1,1)^(-1)","`c_z(m)^2=chi(1,1)^(-1)`")
    s=s.replace("c_(z tensor z')(m)=c_z(m)c_z'(m)chi(a,a')^(-1)","`c_(z tensor z')(m)=c_z(m)c_z'(m)chi(a,a')^(-1)`")
    s=s.replace('d_new(u^4)=14','`d_new(u^4)=14`').replace('J_F(u^4,u^4;1)=14','`J_F(u^4,u^4;1)=14`')
    s=re.sub(r',(?=[A-Z]\.)',', ',s)
    s=re.sub(r'^(#{2,6}) \d+\.\s*',r'\1 ',s,flags=re.M)
    s=re.sub(r'This file records new phase-five arguments[^\n]*\n(?:[^\n]*\n){0,4}','',s,count=1)
    s=s.replace('No earlier phase or online repository is changed.','')
    s=re.sub(r'\b(dimension|dimensions|rank|all|simples|mod|modulo|Theorem|Proposition|Section|Sections)(?=\d)',r'\1 ',s)
    s=s.replace('Subgroup conjugacy classes','Subgroup classes')
    parts.append('# '+title+'\n\n'+literal_operators(s))
(P/'continuation.md').write_text('\n\n'.join(parts))
subprocess.run(['pandoc',str(P/'continuation.md'),'--from=markdown+tex_math_single_backslash+autolink_bare_uris-superscript-subscript-intraword_underscores','--to=latex','--no-highlight','--lua-filter='+str(P/'inline_code.lua'),'-o',str(P/'continuation.tex')],check=True)
path=P/'rank9-m2.tex';s=path.read_text()
# Regeneration replaces the one current integration, including an earlier
# generated wrapper; it never appends another copy of the same mathematics.
s=s.replace('\\input{continuation.tex}','')
while True:
    cleaned=re.sub(r'\{\\setlength\{\\tabcolsep\}\{3pt\}\s*\}','',s)
    if cleaned==s:break
    s=cleaned
s=s.replace('2,033 general complex\nexclusions, 32 rings with unitary models and 18 unresolved rings.','2,043 general complex\nexclusions, 36 rings with unitary models and four unresolved rings.')
s=s.replace('2,033 rings','2,043 rings').replace('2,033 are','2,043 are').replace('2,033 general','2,043 general')
s=s.replace('excluded from fusion categorification over $\\C$, 32 admitting a unitary','excluded from fusion categorification over $\\C$, 36 admitting a unitary')
s=s.replace('fusion categorification, and 18 unresolved rings.','fusion categorification, and four unresolved rings.')
s=s.replace('all 568 explicit negative-subring transfers and all 23,328 coefficients of\nthe 32 positive tensors.','the 568 explicit negative-subring transfers, the subsequent theoretical\ncertificates, and all 26,244 coefficients of the 36 positive tensors.')
s=s.replace('\\subsection{All 32 positive tensors}','\\subsection{All 36 positive tensors}')
a=s.index('\\section{What remains unresolved}');b=s.index('\\section{Exact evidence and reproduction}',a)
s=s[:a].rstrip()+'\n\n'+r'''\input{continuation.tex}

\section{What remains unresolved}
\input{unresolved.tex}
The four remaining rings are $R9\_2\_137,1607,1975,1976$, all with
dimension type $(1^4,2,(4+3\sqrt2)^4)$ and global dimension
$144+96\sqrt2$. General, pivotal, spherical, pseudo-unitary and unitary
existence remain undecided. The audited sphericalization and Galois gates
equate general existence with pseudo-unitary existence; they do not make
every original category pseudo-unitary or unitary. Braided categorification
is excluded for all four.

For each of the three commutative sources, the nonintegral objects have
two distinct $V_4$ stabilizers. The Tambara--Yamagami module associator
identifies them as perpendicular lines and forces the nonalternating
bicharacter. The unique isotropic involution gives a Morita dual of type
$(1^8,(4+3\sqrt2)^4)$, with invertible group $D_8$. A complete finite
fusion-ring reduction and an additional pointed-associator obstruction
leave two common uniform types. The associator restricts to class two on
the rotation $C_4$. A relation $rX=Xs$ with $|r|=4$ and $|s|=2$ would
make that nonzero class trivial on a cyclic stabilizer, so the type with
nonidentity quotient action is impossible with this forced associator.
The surviving two identity-action types still need compatible associators
and the required inverse Morita module. Their based tensors are not models.

The noncommutative case $1975$ retains three necessary Morita types;
all pass this cyclic-stabilizer obstruction. The new algebraic isotropic
orbifold construction for the explicit Radchenko--Wheeler realizations
gives a rank-twelve auxiliary category with invertibles $C_4\times C_2$,
which does not match the required $D_8$. Its canonical nonintegral algebra
route cannot directly give a rank-nine dual. This is a limitation of that
construction route, not a general nonexistence theorem.
Full arguments, exact domains and independent reviews are in
\path{phase5/quadratic_comm/}, \path{phase5/quadratic_noncomm/} and
\path{phase5/orbifold_scope/} of the replay archive. The criteria and model
searches make no further classification decision.

'''+s[b:]
s=s.replace('Only \\path{phase3/results/} is the current mathematical partition.','Only \\path{phase5/results/} is the current mathematical partition.')
a=s.index('After unpacking the archive');b=s.index('The fusion census repository',a)
s=s[:a]+r'''After unpacking the archive and installing its requirements, run
\begin{quote}\ttfamily
python3 verify.py\\
python3 verify.py --frontier
\end{quote}
The first command verifies archive hashes, accepted finite evidence, every
input identity and all 36 exact model transports. The second adds the
auxiliary Morita and algebraic-orbifold checks. The earlier research
snapshots and their supersession records remain preserved. Each categorical
argument has a separate review; computation checks its finite premises,
not the cited categorical theorems. Independent human verification and
formalization remain pending.

'''+s[b:]
s=s.replace('The eighteen open cases','The four open cases')
if '\\usepackage{fontspec}'not in s:
    s=s.replace('\\usepackage[T1]{fontenc}\\usepackage[utf8]{inputenc}','\\usepackage{fontspec}\n\\setmainfont{DejaVu Serif}\n\\setmonofont{DejaVu Sans Mono}')
    s=s.replace('\\setlength{\\emergencystretch}{3em}',r'''\usepackage{fvextra}
\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,commandchars=\\\{\}}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\setlength{\emergencystretch}{3em}''')
path.write_text(s)
text=path.read_text()
if '\\DefineVerbatimEnvironment{verbatim}'not in text:
    text=text.replace('\\usepackage{fvextra}','\\usepackage{fvextra}\n\\DefineVerbatimEnvironment{verbatim}{Verbatim}{breaklines,fontsize=\\small}')
text=re.sub(r'\\setmainfont\{DejaVu Serif\}(?:\[[^\n]*\])?',lambda _: '\\setmainfont{DejaVu Serif}[ItalicFont=DejaVu Serif,ItalicFeatures={FakeSlant=0.17}]',text,count=1)
text=text.replace('\\input{continuation.tex}','{\\setlength{\\tabcolsep}{3pt}\n\\input{continuation.tex}\n}')
path.write_text(text)
print('Integrated current rank-nine proofs and exact classification statement.')
