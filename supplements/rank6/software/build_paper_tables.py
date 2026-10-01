"""Regenerate manuscript tables and counting files from the frozen ledger."""
import json,collections,csv
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def stage_table(rows,decisions):
 path=P/'verification/classification/stages.json'
 if not path.exists():return
 report=json.loads(path.read_text());full_bound=max(r['m'] for r in rows)
 bound=max(map(int,report['stages'][-1]['by_multiplicity']))
 worker_counts=sorted({stage.get('jobs',report['jobs']) for stage in report['stages']})
 from release import continuation_stage_reports,CONTINUATION_PATHS
 stages=report['stages']+continuation_stage_reports(rows,decisions,report['stages'])
 labels={'rank_two':'Rank-two subring','dnumber':r'$d$-number','zero_spectrum':'Zero spectrum','lower_rank_subring':'Lower-rank subring',
         'involution_module':'Involution module','subring':'Dimension quotient','cyclotomic':'Cyclotomicity',
         'small_dimension_morita':'Morita descent','field_automorphisms':'Field automorphisms',
         'weighted_induction':'Weighted induction','general_induction':'Sphericalization/induction trees',
         'dimension_order':'Dimension order','character':'Character induction','tensor_rotation':'Tensor rotation','modular':'Modular induction',
         'retained_completion':'Deferred exact checks'}
 text=[]
 initial=[sum(r['m']==m for r in rows) for m in range(1,full_bound+1)]
 positive=[sum(r['m']==m and r['status'] not in ('excluded','unresolved') for r in decisions) for m in range(1,full_bound+1)]
 unknown=[sum(r['m']==m and r['status']=='unresolved' for r in decisions) for m in range(1,full_bound+1)]
 for first in range(1,bound+1,4):
  columns=list(range(first,min(first+4,bound+1)));global_columns=first==1
  extra=2 if global_columns else 0
  text += [r'\begin{table}[p]\centering\small',r'\setlength{\tabcolsep}{3pt}']
  text += [r'\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}l'+'r'*(len(columns)+extra)+r'@{}}\toprule',
           'Criterion & '+' & '.join('$m='+str(m)+'$' for m in columns)+(r' & Total removed & Seconds' if global_columns else '')+r'\\\midrule',
           'Input & '+' & '.join(str(initial[m-1]) for m in columns)+(r' & --- & ---' if global_columns else '')+r'\\']
  for stage in stages:
   cells=[str(stage['by_multiplicity'][str(m)]['removed'])+'/'+str(stage['by_multiplicity'][str(m)]['remaining']) for m in columns]
   label=labels.get(stage['stage'],stage['label'].replace('_',' '))
   label=label.replace('Continuation: ', 'Added: ')
   if stage['stage']=='general_induction':label='Sphericalization/induction'
   timing='---' if stage['wall_seconds'] is None else f"{stage['wall_seconds']:.1f}"
   text.append(label+' & '+' & '.join(cells)+(' & '+str(stage['removed'])+' & '+timing if global_columns else '')+r'\\')
  text += [r'\midrule',
           'Constructed models & '+' & '.join(str(positive[m-1]) for m in columns)+(r' & --- & ---' if global_columns else '')+r'\\',
           'Unresolved & '+' & '.join(str(unknown[m-1]) for m in columns)+(r' & --- & ---' if global_columns else '')+r'\\',
           r'\bottomrule\end{tabular*}']
  if global_columns:
   text.append(r'\caption{Historical executed ordered sieve and verified continuation, multiplicities one to four. Criterion cells are newly excluded / remaining; the total column covers the original multiplicities one through eight. Seconds are original pass wall times with '+(' or '.join(map(str,worker_counts)))+r' workers. Continuation dashes indicate that no comparable pass wall time is assigned. Timeouts remove nothing. The multiplicity-nine campaign is recorded separately.}\label{tab:stages}')
  else:
   text.append(r'\caption{The same ordered sieve, multiplicities five to eight. Sphericalization/induction checks retained proof trees for $m\le7$ and discovers proofs at $m=8$. Trees can use nested advanced filters; unfinished retained checks appear in the deferred row. Original advanced passes target $m\in\{'+','.join(map(str,report.get('advanced_multiplicities',[3,bound])))+r'\}$. Continuation rows apply additional complete certificates to the original survivors. This practical order is not claimed optimal.}\label{tab:stages-high}')
  text.append(r'\end{table}')
 (P/'papers/generated_stages.tex').write_text('\n'.join(text)+'\n')
 with (P/'data/exclusion_stages.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['step','criterion','multiplicity','entered','newly_excluded','remaining','stage_wall_seconds','errors','budget_exhausted'])
  for step,stage in enumerate(stages,1):
   for m in range(1,bound+1):
    c=stage['by_multiplicity'][str(m)];w.writerow([step,stage['stage'],m,c['entered'],c['removed'],c['remaining'],stage['wall_seconds'],stage['errors'],stage['budget_exhausted']])
 if full_bound>=9:
  from release import m9_stage_reports
  new_stages=m9_stage_reports(rows,decisions)
  newtext=[r'\begin{table}[p]\centering\small',r'\setlength{\tabcolsep}{4pt}',
           r'\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}p{0.46\textwidth}rrrr@{}}\toprule',
           r'Criterion & \shortstack{Excluded /\\remaining} & \shortstack{Worker\\seconds} & Errors & Budgets\\\midrule',
           r'Input & 0 / '+str(initial[8])+r' & --- & --- & ---\\']
  for stage in new_stages:
   label=labels.get(stage['stage'],stage['label']).replace('_',' ')
   newtext.append(label+' & '+str(stage['removed'])+' / '+str(stage['remaining'])+' & '+f"{stage['worker_seconds']:.1f}"+' & '+str(stage['errors'])+' & '+str(stage['budget_exhausted'])+r'\\')
  newtext += [r'\midrule',r'Constructed models & '+str(positive[8])+r' & --- & --- & ---\\',
              r'Unresolved & '+str(unknown[8])+r' & --- & --- & ---\\',r'\bottomrule\end{tabular*}',
              r'\caption{Separately executed exact-multiplicity-nine sieve and advanced continuation. Worker seconds sum the recorded per-tensor elapsed times and are not pass wall times. Errors and exhausted discovery budgets remove no rings. Every accepted exclusion has an independently replayed exact certificate. Earlier campaign timings and scope are unchanged.}\label{tab:stages-m9}',r'\end{table}']
  (P/'papers/generated_stages_m9.tex').write_text('\n'.join(newtext)+'\n')
  with (P/'data/exclusion_stages_m9.csv').open('w',newline='') as stream:
   writer=csv.writer(stream);writer.writerow(['step','campaign','criterion','multiplicity','entered','newly_excluded','remaining','worker_seconds','errors','budget_exhausted'])
   for step,stage in enumerate(new_stages,1):
    writer.writerow([step,stage['campaign'],stage['stage'],9,stage['entered'],stage['removed'],stage['remaining'],stage['worker_seconds'],stage['errors'],stage['budget_exhausted']])
 bound=full_bound
 (P/'data/resolution_frontier.json').write_text(json.dumps({'counts':[{ 'multiplicity':m,'models':positive[m-1],'unresolved':unknown[m-1]} for m in range(1,bound+1)],'smallest_unresolved_multiplicity':next((m for m in range(1,bound+1) if unknown[m-1]),None),'scope':'Exact tested multiplicities only. Historical stage tables cover multiplicities one through eight; the separately executed multiplicity-nine stages have their own table. An unresolved test does not prove that a new mathematical criterion is necessary; no claim is made above the source bound.'},indent=2)+'\n')
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
 for path in CONTINUATION_PATHS:
  if path.exists():
   for r in map(json.loads,path.read_text().splitlines()):stageby.setdefault(r['id'],r['stage'])
 from release import M9_PATHS
 for path in M9_PATHS:
  if path.exists():
   for r in map(json.loads,path.read_text().splitlines()):
    if r['id'] in stageby:raise ValueError('duplicate accepted proof stage')
    stageby[r['id']]=r['stage']
 with (P/'data/proof_mechanisms.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['id','multiplicity','first_accepted_stage','complete_certificate_kind_signature'])
  for d in decisions:
   if d['status']!='excluded':continue
   signature=';'.join(sorted(kinds(d['certificate'])))
   if d['id'] not in stageby:raise ValueError('excluded ring has no recorded accepted stage')
   w.writerow([d['id'],d['m'],stageby[d['id']],signature]);signatures[(signature,d['m'])]+=1
 groups=[{'signature':signature,'by_multiplicity':{str(m):signatures[(signature,m)] for m in range(1,bound+1)},'total':sum(signatures[(signature,m)] for m in range(1,bound+1))} for signature in sorted({s for s,m in signatures})]
 (P/'data/proof_mechanism_counts.json').write_text(json.dumps({'meaning':'Disjoint grouping by the entire set of primitive certificate kinds occurring in a retained proof tree. This records which joint mechanisms were used, not which are logically indispensable or historically first discovered. Each excluded tensor belongs to exactly one signature.','groups':groups,'total':sum(g['total'] for g in groups)},indent=2)+'\n')

def main():
 rows=json.load(open(P/'data/census.json'));ds=json.load(open(P/'data/decisions.json'));counts=collections.Counter(d['status'] for d in ds)
 if [(r['id'],r['m']) for r in rows]!=[(d['id'],d['m']) for d in ds]:
  raise ValueError('rebuild the complete source-bound release ledger before generating exports')
 character_examples={record['id']:record for name in ('character_induction.json','character_higher.json','multiplicity_three.json') for record in json.loads((P/'certificates'/name).read_text())}
 stats={'NegativeCount':counts['excluded'],'UnitaryCount':counts['unitarily_realized'],'SphericalOnlyCount':counts['spherically_realized_nonpseudounitary'],'PositiveCount':counts['unitarily_realized']+counts['spherically_realized_nonpseudounitary'],'UnresolvedCount':counts['unresolved']}
 stats['CompleteBound']=min((r['m'] for r in ds if r['status']=='unresolved'),default=max(r['m'] for r in rows)+1)-1
 stats['CompleteBands']=', '.join(str(m) for m in sorted({r['m'] for r in rows}) if not any(r['m']==m and r['status']=='unresolved' for r in ds))
 stats['CharacterExampleCount']=len(character_examples)
 stats['CensusCount']=len(rows);stats['CensusBound']=max(r['m'] for r in rows)
 stats['ConstructorCount']=sum(len(r['constructors']) for r in json.load(open(P/'data/model_catalog.json')))
 (P/'papers/generated_statistics.tex').write_text(''.join('\\newcommand{\\'+name+'}{'+str(v)+'}\n' for name,v in stats.items()))
 text=[r'\begin{table}[ht]\centering\small',r'\begin{tabular}{rrrrrr}\toprule',r'Exact multiplicity & Rings & Excluded & Unitary & S, not PU & Undecided\\\midrule']
 for m in range(1,max(r['m'] for r in rows)+1):
  c=collections.Counter(x['status'] for x in ds if x['m']==m);text.append(f"{m} & {sum(c.values())} & {c['excluded']} & {c['unitarily_realized']} & {c['spherically_realized_nonpseudounitary']} & {c['unresolved']}\\\\")
 text += [r'\midrule',f"Total & {len(rows)} & {counts['excluded']} & {counts['unitarily_realized']} & {counts['spherically_realized_nonpseudounitary']} & {counts['unresolved']}\\\\",r'\bottomrule\end{tabular}',r"\caption{Complete counting census; categorification is complete at exact multiplicities $\CompleteBands$ and partial in the other displayed bands. The column S, not PU denotes a spherical realization with no pseudo-unitary categorification. All excluded rings are ruled out generally.}\label{tab:classification}",r'\end{table}'];(P/'papers/generated_classification.tex').write_text('\n'.join(text)+'\n')
 labels={'small_dimension_morita':'Solvability descent and involution-return indicators','involution_module':'Involution-module representation obstruction','noncommuting_field_automorphisms':'Noncommuting dimension-field automorphisms','dnumber':'Formal-codegree $d$-number obstruction','rank_two':'Rank-two fusion subring','zero_spectrum':'Zero-spectrum obstruction','lower_rank_subring':'Complete lower-rank subring descent','subring':'Subcategory dimension divisibility','cyclotomic':'Cyclotomicity','signed_extension_positive':'Commutative signed sphericalization','pseudo_gate':'Direct general-to-positive reduction','weighted_induction':'Multiplicity-weighted noncommutative induction','signed_integral':'Signed reduction with the common induction test','oriented_signed':'Complete oriented signed sphericalization','oriented_pseudo_gate':'Further general-to-positive certificates'}
 labels.update({'general_center_rotation_integrality':'Center rotation integrality',
                'rank3_c2_neargroup_subring':'Rank-three near-group subring descent',
                'spectral_involution_module':'Spectral involution-module obstruction',
                'morita_order6':'Order-six Morita dual and grading obstruction',
                'full_morita_gram':'Full Morita-action Gram obstruction',
                'general_stabilizer_rotation':'Stabilizer and third-rotation obstruction',
                'ramified_signed_pseudo_exclusion':'Ramification and signed reduction',
                'ramified_signed_arithmetic_exclusion':'Ramification and signed arithmetic',
                'ramified_Casimir_trace_exclusion':'Ramification and Casimir trace',
                'general_stabilizer_rotation_higher':'Stabilizer and averaged third rotation',
                'general_cyclotomic_stabilizer_trace':'Stabilizer and cyclotomic traces',
                'biquadratic_spherical_trace':'Biquadratic norm and trace obstruction',
                'formal_codegree_trace_ideal':'Formal-codegree trace-ideal obstruction',
                'trace_ideal_signed_pseudo_exclusion':'Trace ideal and signed saturation',
                'inert_quadratic_pseudo_exclusion':'Local signed-spectrum saturation',
                'noncommutative_signed_exclusion':'Noncommutative signed-spectrum saturation',
                'general_integral_morita_rotation':'Integral Morita and Clifford rotation',
                'c4_associator_stabilizer':'Cyclic associator and stabilizer rotation',
                'general_ambient_full_character_rotation':'Full-character cyclotomic rotation',
                'general_cyclic_three_projection':'Cyclic order-three projection',
                'general_fibonacci_subfield_rotation':'Fibonacci subfield and rotation',
                'general_half_e6_projection':r'Half-$E_6$ projection',
                'general_ising_projection_rotation':'Ising projection and rotation',
                'general_low_verlinde_restriction':'Low Verlinde and restriction products',
                'split_quadratic_different_pseudo_exclusion':'Different ideal and signed saturation'})
 labels.update({
                'm9_completion_involution_pair':'Signed involution fields and indicators',
                'm9_completion_free_involution':'Free involution and indicators',
                'm9_completion_relative_center':'Relative center and Galois spin orbits',
                'm9_completion_dimension_fields':'Signed dimension fields and different ideals',
                'm9_completion_triangle_saturation':'Diagonal associativity and trace saturation',
                'm9_completion_quartic_trace':'Cyclic-quartic trace and complementary codegrees',
                'm9_completion_gauss_parity':'Two-adic saturation and quadratic Gauss sums',
                'm9_completion_signed_spectrum':'Indicator normalization and signed spectra'})
 kinds=collections.Counter(d['certificate']['kind'] for d in ds if d['status']=='excluded');text=['\\begin{table}[ht]\\centering','\\begin{tabular}{lr}\\toprule','First retained certificate & Rings\\\\\\midrule']
 for k,v in sorted(kinds.items(),key=lambda z:(-z[1],z[0])):text.append(labels.get(k,k.replace('_',' '))+f' & {v}\\\\')
 text += ['\\midrule',f"Total & {sum(kinds.values())}\\\\",'\\bottomrule\\end{tabular}','\\caption{Disjoint allocation of general exclusions. Nested criteria are not counted again.}\\label{tab:allocation}','\\end{table}'];(P/'papers/generated_allocation.tex').write_text('\n'.join(text)+'\n')
 from model_catalog import build_catalog,latex_table
 build_catalog();latex_table()
 lowtext=[r'\paragraph{The low-multiplicity residuals.}']
 for mult in [2,3,4]:
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
