"""Generate report tables directly from the accepted ledger."""
import json,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'deliverable'
ledger=json.load(open(D/'ledger.json'));rows=ledger['records']
def count(rank=None):return collections.Counter(r['status']for r in rows if rank is None or r['rank']==rank)
lines=[r'\begin{center}',r'\begin{tabular}{lrrrr}',r'\toprule Rank & Inputs & Excluded over $\C$ & Unitary models & Unresolved \\',r'\midrule']
for rank in [9,10,None]:
 c=count(rank);lines.append(f"{rank or 'Total'} & {sum(c.values())} & {c['excluded']} & {c['unitarily_realized']} & {c['unresolved']} "+r'\\')
lines += [r'\bottomrule',r'\end{tabular}',r'\end{center}']
(D/'counts.tex').write_text('\n'.join(lines)+'\n')
out=[]
for rank in [9,10]:
 out += [r'\subsection*{Rank '+str(rank)+'}',r'\begin{longtable}{llll}',r'\toprule Case / status & Case / status & Case / status & Case / status \\',r'\midrule\endhead']
 rr=[r for r in rows if r['rank']==rank];cells=[]
 for r in rr:
  symbol={'excluded':'E','unitarily_realized':'U','unresolved':'?'}[r['status']]
  cells.append(r'\texttt{'+r['id'].replace('_',r'\_')+r'}: \textbf{'+symbol+'}')
 for i in range(0,len(cells),4):out.append(' & '.join(cells[i:i+4]+['']*(4-len(cells[i:i+4])))+r' \\')
 out += [r'\bottomrule',r'\end{longtable}']
(D/'assignment.tex').write_text('\n'.join(out)+'\n')
unresolved=[r for r in rows if r['status']=='unresolved'];deferred={'R10_1_'+str(i)for i in [114,115,152,153,179,189]}
out=[r'\section{Remaining cases and the boundary of this release}']
if unresolved:
 out += ['The following inputs retain unresolved categorifiability status. They are not counted as models or exclusions.']
 for rank in [9,10]:
  ids=[r['id']for r in unresolved if r['rank']==rank]
  if ids:out += [r'\paragraph{Rank '+str(rank)+'.} '+', '.join(r'\texttt{'+i.replace('_',r'\_')+'}'for i in ids)+'.']
 out += [r'The six rank-ten cases $R10\_1\_114,115,152,153,179,189$ are explicitly deferred for a later research phase. The five quadratic cases have dimension profile $(1^4,(2+2\sqrt2)^2,(3+2\sqrt2)^4)$, and the last has invertible group $C_5$ and noninvertible dimension $2+\sqrt5$. Their surviving necessary tests do not establish existence. No new classification claim for these six is included in this release.']
 if any(r['id']not in deferred for r in unresolved):out+=['The listed rank-nine cases are still under active investigation in this working copy; the final ledger must be consulted before publication.']
else:out+=['Every supplied input is assigned an accepted existence or nonexistence proof.']
(D/'remaining.tex').write_text('\n\n'.join(out)+'\n')
extra=[]
if any(r['id']=='R10_1_21'and r['status']=='unitarily_realized'for r in rows):extra+=[r'\input{../work/resolve_rank10_quadratic/model21.tex}']
# Further accepted family proofs can be appended without changing the ledger.
p=ROOT/'work/consolidation/additional_report_sections.json'
if p.exists():extra += [r'\input{../'+x+'}'for x in json.load(open(p))]
(D/'additional_models.tex').write_text('\n'.join(extra)+'\n')
negative=ROOT/'work/consolidation/additional_exclusion_sections.json'
sections=json.load(open(negative)) if negative.exists() else []
(D/'additional_exclusions.tex').write_text('\n'.join(r'\input{../'+x+'}' for x in sections)+'\n')
print('Report tables generated for',len(rows),'inputs')
