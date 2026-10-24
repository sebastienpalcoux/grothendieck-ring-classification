"""Generate manuscript tables only from the accepted multiplicity-two ledger."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence/rank9_m2_20261024';P=ROOT/'publications/rank9-m2/paper'
def esc(s):
 for a,b in [('\\',r'\textbackslash{}'),('&',r'\&'),('%',r'\%'),('_',r'\_'),('#',r'\#'),('^',r'\textasciicircum{}')]:s=s.replace(a,b)
 return s
models=json.loads((E/'models.json').read_text());models.sort(key=lambda x:int(x['id'].rsplit('_',1)[1]))
lines=[r'\begin{small}\setlength{\tabcolsep}{4pt}\begin{longtable}{p{.14\textwidth}p{.61\textwidth}p{.18\textwidth}}',r'\caption{All unitary models. The final column is the source-to-model permutation; indices are zero-based.}\label{tab:models}\\',r'\toprule Case & Construction & Basis map\\\midrule\endfirsthead\toprule Case & Construction & Basis map\\\midrule\endhead']
for r in models:
 lines.append(esc(r['id'])+' & '+esc(r['model'])+r' & \texttt{'+''.join(map(str,r['basis_map_source_to_model']))+r'}\\')
lines.append(r'\bottomrule\end{longtable}\end{small}');(P/'models.tex').write_text('\n'.join(lines)+'\n')
accepted=json.loads((E/'audit/phase2/accepted.json').read_text())
labels={'signed_nonzero_products':'Signed nonzero products','joint_integral_center':'Joint integral center','prime_descent':'Prime descent','solvable_rank_two_module':'Solvable rank-two module','joint_quadratic_center':'Joint quadratic center','folded_fermionic_so3':'Folded fermionic SO(3)','solvable_central_invertibles':'Solvable central invertibles','quadratic_neutral_block':'Quadratic neutral block','larger_fixed_block_morita':'Fixed-block Morita obstruction'}
lines=[r'\begin{small}\begin{longtable}{p{.36\textwidth}p{.56\textwidth}}',r'\caption{The 36 family exclusions. Listed integers are suffixes of $R9\_2\_n$.}\label{tab:families}\\',r'\toprule Family & Cases\\\midrule\endfirsthead\toprule Family & Cases\\\midrule\endhead']
for k,ids in accepted['new_exclusions'].items():lines.append(labels[k]+' & '+r',\allowbreak '.join(map(str,ids))+r'\\')
lines.append(r'\bottomrule\end{longtable}\end{small}');(P/'exclusion-families.tex').write_text('\n'.join(lines)+'\n')
U=json.loads((E/'unresolved.json').read_text())
lines=[r'\begin{center}\begin{tabular}{ll}\toprule Type & Suffixes of unresolved $R9\_2\_n$\\\midrule',r'Quadratic & '+', '.join(str(int(r['id'].rsplit('_',1)[1]))for r in U)+r'\\',r'\bottomrule\end{tabular}\end{center}']
(P/'unresolved.tex').write_text('\n'.join(lines)+'\n')
print(f'Generated {len(models)} model entries and {len(U)} open identifiers from the current ledger.')
