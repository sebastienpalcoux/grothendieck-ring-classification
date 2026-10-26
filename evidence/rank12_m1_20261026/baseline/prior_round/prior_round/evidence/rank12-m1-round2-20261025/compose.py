"""Bind the independently audited continuation to the full permanent ledger."""
from pathlib import Path
import collections,copy,csv,hashlib,json,sys
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'rank12-m1-offline-20261025'
sys.path[:0]=[str(BASE),str(BASE/'sources/work/rank11')]
import common
def read(p):return json.loads((ROOT/p).read_text())
def require(c,m):
 if not c:raise ValueError(m)

def build():
 old=json.loads((BASE/'ledger.json').read_text());data=json.loads((BASE/'tensors.json').read_text());families={r['id']:r for r in json.loads((BASE/'unresolved_families.json').read_text())['records']};previous={r['id']:r for r in old['records']}
 models=collections.defaultdict(list);negative={}
 def add_model(rid,m,source):
  if rid not in families:return
  p=m['basis_map_source_to_model'];M=m['model_tensor'];R=data[rid]
  require(sorted(p)==list(range(12))and p[0]==0,'unit preserving model map')
  require(all(R[i][j][k]==M[p[i]][p[j]][p[k]]for i in range(12)for j in range(12)for k in range(12)),'all new model coefficients '+rid)
  models[rid].append(dict(m,evidence_source=source))
 def add_negative(rid,c,source):
  require(rid in families and rid not in negative,'new distinct negative '+rid);negative[rid]=dict(certificate=c,evidence_source=source)
 for r in read('audit_models/new_models.json'):
  for m in r['models']:add_model(r['id'],m,'audit_models/new_models.json')
 for r in read('family_integral/results.json')['accepted_models']:add_model(r['id'],r['model'],'family_integral/results.json')
 for r in read('family_quadratic/results.json')['models']:
  add_model(r['id'],dict(name=r['model']+(' (bosonic zest)'if r['zested']else''),constructor=r['constructor'],parameters=dict(m=r['m'],zested=r['zested']),model_tensor=r['model_tensor'],basis_map_source_to_model=r['basis_map_source_to_model'],categorical_existence_source=r['categorical_existence_source']),'family_quadratic/results.json')
 for r in read('family_graded/results.json')['records']:
  if r['status']=='excluded':add_negative(r['id'],r['certificate'],'family_graded/results.json')
  else:
   for m in r['models']:add_model(r['id'],m,'family_graded/results.json')
 for r in read('d24_pointed_extensions/models.json')['models']:add_model(r['id'],r['model'],'d24_pointed_extensions/models.json')
 for r in read('d24_pointed_extensions/exclusions.json')['records']:add_negative(r['id'],r,'d24_pointed_extensions/exclusions.json')
 for name in ('root/group_graph_models.json','root/sl23_twist_models.json'):
  for r in read(name)['models']:add_model(r['id'],{k:v for k,v in r.items()if k not in ('id','status','tensor_sha256')},name)
 for r in read('family_cubic/results.json')['records']:add_negative(r['id'],r['certificate'],'family_cubic/results.json')
 for r in read('root/quadratic_exclusions.json'):add_negative(r['id'],r,'root/quadratic_exclusions.json')
 require(not set(models)&set(negative),'no new positive/negative conflict')
 require((len(negative),len(models))==(32,14),'expected new counts')
 records=[]
 for oldr in old['records']:
  r=copy.deepcopy(oldr);rid=r['id'];r['first_round_status']=r['status'];r['first_round_audit']='retained; no erroneous classification found'
  if rid in negative:
   r.update(status='excluded',exclusion_route=negative[rid]['certificate'].get('kind',negative[rid]['certificate'].get('criterion','theoretical_continuation')),continuation_exclusion=negative[rid],scope='arbitrary_complex_categorification')
  elif rid in models:
   m=models[rid][0];r.update(status='unitarily_realized',model_name=m['name'],model_constructor=m['constructor'],model_certificate_count=len(models[rid]),continuation_models=models[rid],scope='unitary_existence; no uniqueness claim')
  elif rid in families:
   f=families[rid]['family'];gates=dict(spherical='necessary',pseudo_unitary='automatic by weak integrality',braided='excluded by noncommutative fusion rules'if not r['commutative']else'not settled here')
   if f.startswith('quadratic_C6'):
    gates.update(pseudo_unitary='a Galois conjugate is pseudo-unitary; original need not be',unitarizable='not established')
   elif f in ('D48','D32','D144'):gates['unitarizable']='necessary by two-prime solvability and unitarizability'
   else:gates['unitarizable']='not established'
   r.update(unresolved_family=f,hypothetical_category=gates)
  records.append(r)
 counts=collections.Counter(r['status']for r in records);require(counts==dict(excluded=425,unitarily_realized=141,unresolved=66),'complete counts')
 remain=[r['id']for r in records if r['status']=='unresolved'];fc=collections.Counter(families[rid]['family']for rid in remain)
 summary=dict(input_count=632,excluded=425,modeled=141,unresolved=66,first_round=dict(excluded=393,modeled=127,unresolved=112),first_round_retractions=0,new_exclusions=32,new_modeled=14,remaining_family_counts=dict(fc),online_revision_performed=False,scope='Offline audit and theoretical continuation; counts of supplied based rings, not tensor-equivalence classes.',independent_human_verification='pending')
 (ROOT/'ledger.json').write_text(json.dumps(dict(summary=summary,records=records),indent=2)+'\n')
 fields=['id','input_line','tensor_sha256','first_round_status','status','commutative','simple','exclusion_route','model_name','unresolved_family']
 with(ROOT/'ledger.csv').open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(records)
 (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 (ROOT/'new_decisions.json').write_text(json.dumps(dict(exclusions=negative,models=models),indent=2)+'\n')
 (ROOT/'unresolved_tensors.json').write_text(json.dumps([dict(id=rid,tensor_sha256=common.sha(data[rid]),tensor=data[rid],exact_dimension_character=families[rid],hypothetical_category=next(r['hypothetical_category']for r in records if r['id']==rid))for rid in remain],separators=(',',':'))+'\n')
 tex=(ROOT/'report_template.tex').read_text();subs={'EXCLUDED':425,'MODELED':141,'UNRESOLVED':66,'NEWNEG':32,'NEWPOS':14,'D40SECTION':(ROOT/'d40_report.tex').read_text()}
 table=r'\begin{center}\small\begin{longtable}{@{}lp{119mm}@{}}\toprule Suffixes&Construction\\\midrule\endhead'+'\n'
 rows=[('25',r'$\mathcal C(A_5\times C_2,1,\operatorname{graph}\chi,1)$'),('30',r'$\mathcal C(S_4\times C_2,1,V_4,1)$, $V_4=\langle((34),0),((12),1)\rangle$'),('79,80',r'Full $S_3$ triality gaugings of $SO(8)_1$'),('156,263',r'$C_2$ Morita duals of explicitly reconstructed $D_8$-graded categories over $\Vec_{C_5}$'),('322,323',r'Bosonic associative $C_2$ zests of the two triality gaugings'),('417',r'$\mathcal C(S_4\times_{C_2}C_4,1,C_4,1)$, $C_4=\langle((1324),1)\rangle$'),('428,513',r'$\mathcal C(A_4\times C_2,\omega,H,1)$ for the stored relative cocycles and diagonal $H=C_2$'),('449',r'$\mathrm{TY}(C_5,\chi)^{C_4}$ with the explicit weak inversion action'),('541',r'$\Rep(C_3\rtimes C_8)$ with inversion action'),('597',r'Twisted subgroup bimodules for $A_4\times C_2$; independently also for $SL(2,3)$')]
 table+='\n'.join(a+'&'+b+r'\\'for a,b in rows)+r'\bottomrule\end{longtable}\end{center}'
 subs['MODELTABLE']=table
 desc={'D120':r'$1^4,2^4,5^4$','D48':r'$1^8,2^2,4^2$','D32':r'$1^8,2^2,(2\sqrt2)^2$','D144':r'$1^2,2,3^2,4^3,(3\sqrt2)^4$','quadratic_C6_sqrt10':r'$1^6,(3+\sqrt{10})^6$','quadratic_C6_sqrt13':r'$1^6,((3+\sqrt{13})/2)^6$'}
 rt=r'\begin{center}\begin{tabular}{lr}\toprule FP dimension multiset&Cases\\\midrule'+'\n'
 rt+='\n'.join(desc[k]+'&'+str(fc[k])+r'\\'for k in ('D120','D48','D32','D144','quadratic_C6_sqrt10','quadratic_C6_sqrt13'))+r'\midrule Total&66\\\bottomrule\end{tabular}\end{center}'
 subs['REMAININGTABLE']=rt
 for key,value in subs.items():tex=tex.replace('@'+key+'@',str(value))
 require('@'not in tex.replace('@{}',''),'no report placeholders')
 (ROOT/'report.tex').write_text(tex)
 print(json.dumps(summary,indent=2))
if __name__=='__main__':build()
