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
              r'\begin{table}[H]',r'\centering',
              r'\caption{Sequential exclusion counts, charged only to the first successful criterion. Costs generally rise toward the bottom.}\label{tab:stages}',
              r'\begin{tabular}{@{}l r r r r@{}}',r'\toprule',
              r'Criterion & $m=1$ & $m=2$ & $m=3$ & $m=4$\\',r'\midrule'])
names={'near_group':'Near-group theorem',
       'dimension_15':'Global dimension 15',
       'zero_spectrum':'Zero spectrum',
       'lower_rank_subring':'Closed rank-four/five subring',
       'dnumber':'Formal-codegree $d$-number',
       'subcategory_divisibility':'Subcategory dimension quotient',
       'oriented_dimension_order':'Oriented dimension order'}
pretty_models={
    'Vec(C7)':r'$\operatorname{Vec}(C_7)$',
    'TY(C6)':r'$\operatorname{TY}(C_6)$',
    'Rep(D16)':r'$\operatorname{Rep}(D_{16})$',
    'Rep(D22)':r'$\operatorname{Rep}(D_{22})$',
    'Rep(SD16)':r'$\operatorname{Rep}(SD_{16})$',
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
    lines.append(names[stage]+' & '+' & '.join(str(c.get(str(m),0)) for m in range(1,5))+r'\\')
lines.extend([r'\bottomrule',r'\end{tabular}',r'\end{table}','',
              r'\begin{table}[H]',r'\centering',
              r'\caption{Unitary model constructions identified by exact full-tensor based-ring isomorphism. Each row denotes a ring, not a count of categories.}\label{tab:models}',
              r'\begin{tabular}{@{}l l@{}}',r'\toprule',
              r'Census ID & Explicit model\\',r'\midrule'])
for item in sorted(catalog,key=lambda r:(r['multiplicity'],int(r['id'].split('_')[-1]))):
    model=pretty_models.get(item['name'])
    if model is None:
        c=item['category_code'];model=r'AnyonWiki $\mathrm{FC}^{7,1,'+str(c[2])+r'}_{'+','.join(map(str,c[3:]))+r'}$'
    lines.append(r'\texttt{'+esc(item['id'])+'} & '+model+r'\\')
lines.extend([r'\bottomrule',r'\end{tabular}',r'\end{table}', ''])
(ROOT/'papers/generated_tables.tex').write_text('\n'.join(lines))
