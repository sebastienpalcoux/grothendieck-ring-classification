#!/usr/bin/env python3
"""Generate every finite-result table from the verified certificate summary."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LABELS={
 'dnumber':r'Formal-codegree $d$-number failure',
 'rank_two_moment':'Rank-two moment obstruction',
 'Sm':'Non-self-dual quadratic moments',
 'diagonal_involution_moments':'Diagonal involution moments',
 'near_group_root_length':r'$C_3$ near-group root length',
 'literature_near_group':'Automatic near-group classification',
 'cyclotomic':'Cyclotomicity obstruction',
 'subring':'Fusion-subring dimension divisibility',
 'involution_propagation_42':'Residual-involution propagation',
 'weak_integral':'Weak integrality and induction',
 'two_dimensions':'Two-dimension Galois reduction and induction',
 'signed':'Signed sphericalization',
}
def num(n):return f'{n:,}'.replace(',',r'\,')
def main():
 s=json.loads((ROOT/'verification/summary.json').read_text())
 usage=json.loads((ROOT/'verification/criterion_usage.json').read_text())
 c=json.loads((ROOT/'data/census_128_manifest.json').read_text())
 g=json.loads((ROOT/'verification/global_signed_catalog.json').read_text())
 if g.get('verified') is not True or g.get('bound')!=128:
  raise ValueError('shared signed cover has not been independently verified')
 if s['checked_rings']!=c['rings'] or sum(s['counts'].values())!=c['rings']:
  raise ValueError('certificate coverage differs from census')
 if s['counts'].get('unresolved',0) or s['counts'].get('realized')!=15:
  raise ValueError('the announced classification is not verified')
 if s['counts'].get('excluded')!=c['rings']-15:raise ValueError('exclusion coverage incomplete')
 out=ROOT/'papers/generated';out.mkdir(exist_ok=True)
 macros={'MultiplicityBound':c['bound'],'CensusSize':s['checked_rings'],
  'ExcludedCount':s['counts']['excluded'],'SignedRecords':s['signed_records'],
  'SignedTables':s['checked_signed_tables'],
  'GlobalSignedOrbits':g['total_orbits'],
  'GlobalSignedSurvivors':g['retained_orbits']}
 (out/'results.tex').write_text('% Generated from verification/summary.json; do not edit.\n'+''.join('\\newcommand{\\'+k+'}{'+num(v)+'}\n' for k,v in macros.items()))
 rows=[]
 for lo,hi in [(1,32),(33,64),(65,96),(97,128)]:
  total=sum(c['by_m'][str(m)] for m in range(lo,hi+1))
  positive=sum(s['by_multiplicity'].get(str(m),{}).get('realized',0) for m in range(lo,hi+1))
  rows.append(f'${lo}$--${hi}$ & ${num(total)}$ & ${positive}$'+r'\\')
 (out/'census_bands.tex').write_text(r'''% Generated from audited census and verified certificate summary.
\begin{table}[ht]
\centering
\begin{tabular}{lrr}
\toprule
Exact multiplicity range & Fusion rings & Categorifiable rings\\
\midrule
'''+ '\n'.join(rows)+r'''
\midrule
Total & $\CensusSize$ & $15$\\
\bottomrule
\end{tabular}
\caption{The complete census and its categorifiable subset.}
\label{tab:census-bands}
\end{table}
''')
 types=s['top_level_criteria'];unknown=set(types)-set(LABELS)-{'model'}
 if unknown:raise ValueError('unmapped criterion labels: '+repr(unknown))
 first=usage['first_multiplicity']
 groups=usage['grouped_first_multiplicity']
 if set(types)-{'model'} != set(LABELS) or any(k not in first for k in LABELS):
  raise ValueError('criterion usage or dispatch order does not match the table')
 last=max(groups.values())
 rows=[LABELS[k]+f' & ${first[k]}$ & ${num(types[k])}$'+r'\\' for k in LABELS]
 (out/'proof_counts.tex').write_text(r'''% Generated from accepted certificates; disjoint first successful tests.
\begin{table}[ht]
\centering
\begin{tabular}{p{.66\linewidth}rr}
\toprule
First successful top-level test, in dispatch order & First use $m$ & Rings\\
\midrule
'''+ '\n'.join(rows)+r'''
\midrule
Total excluded & & $\ExcludedCount$\\
\bottomrule
\end{tabular}
\caption{Archived disjoint certificate allocation, displayed in the order
of the revised dispatcher. A model is recognized before these tests. First
use is the least exact multiplicity with a certificate of this type;
nested tests in signed records are not counted again. The sequence puts
high-yield direct obstructions before the expensive signed searches.}
\label{tab:proof-counts}
\end{table}
\noindent The finer ledger groups individual checks by their underlying
mathematical criterion. Its latest first use is at multiplicity '''+str(last)+r'''.
In this fixed certificate allocation, all multiplicities from '''+str(last+1)+r''' to
$\MultiplicityBound$ require no additional criterion family. This describes
the completed run, not a proof that the collection of criteria is minimal.
For example, signed cyclotomicity is first decisive at multiplicity $95$,
but it applies the same cyclotomicity theorem used earlier for unsigned
characters. Signed-table parity is also used as an enumeration prefilter;
its removed candidate counts are recorded separately from the ring totals.
''')
 print('Generated verified manuscript tables:',out)
if __name__=='__main__':main()
