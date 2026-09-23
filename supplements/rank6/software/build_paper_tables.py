"""Regenerate manuscript tables and counting files from the frozen ledger."""
import json,collections,csv
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def stage_table(rows,decisions):
 path=P/'verification/classification/stages.json'
 if not path.exists():return
 report=json.loads(path.read_text());bound=max(r['m'] for r in rows)
 worker_counts=sorted({stage.get('jobs',report['jobs']) for stage in report['stages']})
 labels={'rank_two':'Rank-two subring','dnumber':r'$d$-number','zero_spectrum':'Zero spectrum','lower_rank_subring':'Lower-rank subring',
         'involution_module':'Involution module','subring':'Dimension quotient','cyclotomic':'Cyclotomicity',
         'small_dimension_morita':'Morita descent','field_automorphisms':'Field automorphisms',
         'weighted_induction':'Weighted induction','general_induction':'Sphericalization/induction trees',
         'dimension_order':'Dimension order','character':'Character induction','tensor_rotation':'Tensor rotation','modular':'Modular induction',
         'retained_completion':'Deferred exact checks'}
 text=[r'\begin{table}[p]\centering\small',r'\setlength{\tabcolsep}{3pt}']
 initial=[sum(r['m']==m for r in rows) for m in range(1,bound+1)]
 positive=[sum(r['m']==m and r['status'] not in ('excluded','unresolved') for r in decisions) for m in range(1,bound+1)]
 unknown=[sum(r['m']==m and r['status']=='unresolved' for r in decisions) for m in range(1,bound+1)]
 for first in range(1,bound+1,4):
  columns=list(range(first,min(first+4,bound+1)));global_columns=first==1
  extra=2 if global_columns else 0
  text += [r'\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}l'+'r'*(len(columns)+extra)+r'@{}}\toprule',
           'Criterion & '+' & '.join('$m='+str(m)+'$' for m in columns)+(r' & Total removed & Seconds' if global_columns else '')+r'\\\midrule',
           'Input & '+' & '.join(str(initial[m-1]) for m in columns)+(r' & --- & ---' if global_columns else '')+r'\\']
  for stage in report['stages']:
   cells=[str(stage['by_multiplicity'][str(m)]['removed'])+'/'+str(stage['by_multiplicity'][str(m)]['remaining']) for m in columns]
   label=labels.get(stage['stage'],stage['label'].replace('_',' '))
   if stage['stage']=='general_induction':label='Sphericalization/induction'
   text.append(label+' & '+' & '.join(cells)+(' & '+str(stage['removed'])+' & '+f"{stage['wall_seconds']:.1f}" if global_columns else '')+r'\\')
  text += [r'\midrule',
           'Constructed models & '+' & '.join(str(positive[m-1]) for m in columns)+(r' & --- & ---' if global_columns else '')+r'\\',
           'Unresolved & '+' & '.join(str(unknown[m-1]) for m in columns)+(r' & --- & ---' if global_columns else '')+r'\\',
           r'\bottomrule\end{tabular*}']
  if first+4<=bound:text.append(r'\par\vspace{1.3em}')
 text += [
  r'\caption{The executed ordered sieve. Criterion cells are newly excluded / remaining. Seconds are recorded pass wall times; '+(' or '.join(map(str,worker_counts)))+r' workers per stage are recorded in the ledger. Sphericalization/induction checks retained proof trees for $m\le7$ and discovers proofs at $m=8$. Trees can use nested advanced filters; unfinished retained checks appear in the deferred row. Older residuals are retained. Later dimension-order, character, tensor-rotation and modular discovery targets $m\in\{'+','.join(map(str,report.get('advanced_multiplicities',[3,bound])))+r'\}$. Timeouts remove nothing. This practical order is not claimed optimal.}\label{tab:stages}',r'\end{table}']
 (P/'papers/generated_stages.tex').write_text('\n'.join(text)+'\n')
 with (P/'data/exclusion_stages.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['step','criterion','multiplicity','entered','newly_excluded','remaining','stage_wall_seconds','errors','budget_exhausted'])
  for step,stage in enumerate(report['stages'],1):
   for m in range(1,bound+1):
    c=stage['by_multiplicity'][str(m)];w.writerow([step,stage['stage'],m,c['entered'],c['removed'],c['remaining'],stage['wall_seconds'],stage['errors'],stage['budget_exhausted']])
 (P/'data/resolution_frontier.json').write_text(json.dumps({'counts':[{ 'multiplicity':m,'models':positive[m-1],'unresolved':unknown[m-1]} for m in range(1,bound+1)],'smallest_unresolved_multiplicity':next((m for m in range(1,bound+1) if unknown[m-1]),None),'scope':'Exact tested multiplicities only. An unresolved test does not prove that a new mathematical criterion is necessary; no claim is made above the source bound.'},indent=2)+'\n')
 def kinds(value):
  found=set()
  if isinstance(value,dict):
   if isinstance(value.get('kind'),str):found.add(value['kind'])
   for child in value.values():found.update(kinds(child))
  elif isinstance(value,list):
   for child in value:found.update(kinds(child))
  return found
 signatures=collections.Counter();stageby={}
 accepted=P/'certificates/classification.jsonl'
 if accepted.exists():stageby={r['id']:r['stage'] for r in map(json.loads,accepted.read_text().splitlines())}
 with (P/'data/proof_mechanisms.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['id','multiplicity','first_accepted_stage','complete_certificate_kind_signature'])
  for d in decisions:
   if d['status']!='excluded':continue
   signature=';'.join(sorted(kinds(d['certificate'])))
   w.writerow([d['id'],d['m'],stageby.get(d['id'],'retained'),signature]);signatures[(signature,d['m'])]+=1
 groups=[{'signature':signature,'by_multiplicity':{str(m):signatures[(signature,m)] for m in range(1,bound+1)},'total':sum(signatures[(signature,m)] for m in range(1,bound+1))} for signature in sorted({s for s,m in signatures})]
 (P/'data/proof_mechanism_counts.json').write_text(json.dumps({'meaning':'Disjoint grouping by the entire set of primitive certificate kinds occurring in a retained proof tree. This records which joint mechanisms were used, not which are logically indispensable or historically first discovered. Each excluded tensor belongs to exactly one signature.','groups':groups,'total':sum(g['total'] for g in groups)},indent=2)+'\n')

def main():
 rows=json.load(open(P/'data/census.json'));ds=json.load(open(P/'data/decisions.json'));counts=collections.Counter(d['status'] for d in ds)
 character_examples={record['id']:record for name in ('character_induction.json','character_higher.json','multiplicity_three.json') for record in json.loads((P/'certificates'/name).read_text())}
 stats={'NegativeCount':counts['excluded'],'UnitaryCount':counts['unitarily_realized'],'SphericalOnlyCount':counts['spherically_realized_nonpseudounitary'],'PositiveCount':counts['unitarily_realized']+counts['spherically_realized_nonpseudounitary'],'UnresolvedCount':counts['unresolved']}
 stats['CharacterExampleCount']=len(character_examples)
 stats['CensusCount']=len(rows);stats['CensusBound']=max(r['m'] for r in rows)
 stats['ConstructorCount']=sum(len(r['constructors']) for r in json.load(open(P/'data/model_catalog.json')))
 (P/'papers/generated_statistics.tex').write_text(''.join('\\newcommand{\\'+name+'}{'+str(v)+'}\n' for name,v in stats.items()))
 text=[r'\begin{table}[ht]\centering\small',r'\begin{tabular}{rrrrrr}\toprule',r'Exact multiplicity & Rings & Excluded & Unitary & S, not PU & Undecided\\\midrule']
 for m in range(1,max(r['m'] for r in rows)+1):
  c=collections.Counter(x['status'] for x in ds if x['m']==m);text.append(f"{m} & {sum(c.values())} & {c['excluded']} & {c['unitarily_realized']} & {c['spherically_realized_nonpseudounitary']} & {c['unresolved']}\\\\")
 text += [r'\midrule',f"Total & {len(rows)} & {counts['excluded']} & {counts['unitarily_realized']} & {counts['spherically_realized_nonpseudounitary']} & {counts['unresolved']}\\\\",r'\bottomrule\end{tabular}',r"\caption{Complete counting census; categorification is complete through multiplicity two and partial above. The column S, not PU denotes a spherical realization with no pseudo-unitary categorification. All excluded rings are ruled out generally.}\label{tab:classification}",r'\end{table}'];(P/'papers/generated_classification.tex').write_text('\n'.join(text)+'\n')
 labels={'small_dimension_morita':'Solvability descent and involution-return indicators','involution_module':'Involution-module representation obstruction','noncommuting_field_automorphisms':'Noncommuting dimension-field automorphisms','dnumber':'Formal-codegree $d$-number obstruction','rank_two':'Rank-two fusion subring','zero_spectrum':'Zero-spectrum obstruction','lower_rank_subring':'Complete lower-rank subring descent','subring':'Subcategory dimension divisibility','cyclotomic':'Cyclotomicity','signed_extension_positive':'Commutative signed sphericalization','pseudo_gate':'Direct general-to-positive reduction','weighted_induction':'Multiplicity-weighted noncommutative induction','signed_integral':'Signed reduction with the common induction test','oriented_signed':'Complete oriented signed sphericalization','oriented_pseudo_gate':'Further general-to-positive certificates'}
 kinds=collections.Counter(d['certificate']['kind'] for d in ds if d['status']=='excluded')
 kind_order=['rank_two','dnumber','zero_spectrum','lower_rank_subring','involution_module',
             'subring','cyclotomic','small_dimension_morita',
             'noncommuting_field_automorphisms','weighted_induction',
             'signed_extension_positive','oriented_signed','pseudo_gate',
             'oriented_pseudo_gate','signed_integral']
 assert set(kinds)==set(kind_order),set(kinds)^set(kind_order)
 text=['\\begin{table}[ht]\\centering','\\begin{tabular}{lr}\\toprule','Retained proof family & Rings\\\\\\midrule']
 for k in kind_order:text.append(labels[k]+f' & {kinds[k]}\\\\')
 text += ['\\midrule',f"Total & {sum(kinds.values())}\\\\",'\\bottomrule\\end{tabular}',r'\caption{Disjoint retained proof families, listed in the order of the corresponding sieve stages. Several signed and positive-dimension families occur within the sphericalization/induction stage. Nested criteria are not counted a second time.}\label{tab:allocation}','\\end{table}'];(P/'papers/generated_allocation.tex').write_text('\n'.join(text)+'\n')
 from model_catalog import build_catalog,latex_table
 build_catalog();latex_table()
 lowtext=[r'\paragraph{The low-multiplicity residuals.}']
 for mult in [2,3]:
  entries=[r'\RR{%s}{%s}'%(d['m'],d['index']) for d in ds if d['m']==mult and d['status']=='unresolved']
  if not entries:
   lowtext.append('Every ring at exact multiplicity %s is decided.'%mult);continue
  lowtext.append('At exact multiplicity %s the unresolved records are'%mult)
  lowtext.append(r'\[\begin{gathered}')
  for offset in range(0,len(entries),6):lowtext.append(r',\;'.join(entries[offset:offset+6])+(r'\\' if offset+6<len(entries) else '.'))
  lowtext.append(r'\end{gathered}\]')
 (P/'papers/generated_low_residuals.tex').write_text('\n'.join(lowtext)+'\n')
 byid={r['id']:r for r in rows};unresolved=[dict(byid[d['id']],diagnostic=d['diagnostic'],existence=d['existence']) for d in ds if d['status']=='unresolved'];(P/'data/unresolved_tensors.json').write_text(json.dumps(unresolved,separators=(',',':'))+'\n')
 with (P/'data/decisions.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['id','multiplicity','index','commutative','status','general','pivotal','spherical','pseudo_unitary','unitary','criterion_or_models'])
  for d in ds:w.writerow([d['id'],d['m'],d['index'],d['commutative'],d['status'],*[d['existence'][k] for k in ('general','pivotal','spherical','pseudo_unitary','unitary')],d['certificate']['kind'] if 'certificate'in d else '; '.join(d.get('models',[d.get('diagnostic','')]))])
 with (P/'oeis/counts.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['multiplicity','rank6_fusion_rings','cumulative']);cum=0
  for m in range(1,max(r['m'] for r in rows)+1):a=sum(r['m']==m for r in rows);cum+=a;w.writerow([m,a,cum])
 with (P/'data/rank6_counts.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['multiplicity','classes'])
  for m in range(1,max(r['m'] for r in rows)+1):w.writerow([m,sum(r['m']==m for r in rows)])
 (P/'oeis/bfile_rank6_unassigned.txt').write_text('# Rank six; exact multiplicity; accession unassigned.\n'+'\n'.join(f"{m} {sum(r['m']==m for r in rows)}" for m in range(1,max(r['m'] for r in rows)+1))+'\n')
 bym=collections.Counter(byid[rid]['m'] for rid in character_examples)
 text=[r'\begin{table}[ht]\centering',r'\begin{tabular}{cr}\toprule',r'Exact multiplicity & Example certificates\\\midrule']
 text += [str(m)+' & '+str(bym[m])+r'\\' for m in sorted(bym)]
 text += [r'\midrule Total & '+str(len(character_examples))+r'\\\bottomrule',r'\end{tabular}',r'\caption{Illustrative character-aware induction certificates for Theorem~\ref{thm:character-induction}, generated from the supplied exact proof examples. These are examples of the mechanism, not a disjoint allocation of the current census.}\label{tab:character-applications}',r'\end{table}']
 (P/'papers/generated_character_applications.tex').write_text('\n'.join(text)+'\n')
 stage_table(rows,ds)
 print(dict(counts))
if __name__=='__main__':main()
