"""Full joint-Galois check on the new integer/full-phase witness."""
from pathlib import Path
from types import SimpleNamespace
import json,itertools,sys,time
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2];OLD=ROOT/'evidence/rank8_frontier_20261021'
sys.path.insert(0,str(OLD/'commutative_integer'));sys.path.insert(0,str(OLD/'quadratic'));sys.path.insert(0,str(OLD/'global_induction'))
import streaming as st
from exact import require,evaluate
from joint_galois_balance import rows_for_labels
start=time.monotonic();source=st.load_ring('R8_3_982');R=source['tensor'];du=[next(j for j in range(8)if R[i][j][0])for i in range(8)]
reference=json.loads((OLD/'global_induction/complete_results/R8_3_982_sts_frame_h4.json').read_text());table=reference['metadata']['character_table'];x=s.Symbol('x');poly=s.Poly.from_list(list(map(s.Rational,table['cyclotomic_polynomial'])),x);K=s.QQ.alg_field_from_poly(poly,alias='zeta');z=K([1,0]);characters=[tuple(K(list(map(s.Rational,v)))for v in row)for row in table['characters']]
require(reference['tensor_sha256']==source['tensor_sha256'],'character table source tensor differs')
require(poly==s.Poly(s.cyclotomic_poly(24,x),x) and len(set(characters))==8,'complete cyclotomic character field differs')
for row in characters:
 require(all(row[i]*row[j]==sum((K(R[i][j][k])*row[k]for k in range(8)),K.zero)for i in range(8)for j in range(8)),'character source multiplication fails')
 require(all(row[du[i]]==evaluate(row[i].to_list(),z**-1,K)for i in range(8)),'character duality fails')
codegrees=[sum((row[i]*row[du[i]]for i in range(8)),K.zero)for row in characters]
require(codegrees==[K(list(map(s.Rational,v)))for v in table['codegrees']],'formal codegrees differ')
core=json.loads((HERE/'frame2_system.json').read_text());meta=core['metadata']['source_metadata']['source_metadata'];fp=meta['FP_character'];ds=characters[fp];D=sum((v*v for v in ds),K.zero);T=SimpleNamespace(K=K,degree=8,characters=characters,ds=ds,D=D,beta=[D/f for f in codegrees])
P=json.loads((OLD/'commutative_integer/R8_3_982_profile.json').read_text())['records'][2];vectors={v['index']:(0,)+tuple(v['vector'])for v in P['high_vectors']};labels=[('high_orbit',tuple(o['indices']),tuple(vectors[j]for j in o['indices']))for o in P['duality_orbits']];Es=[E for E in range(8)if E!=fp];labels += [('fusion_coefficient',E,F,G)for E,F in itertools.combinations_with_replacement(Es,2)for G in Es]
rows,rhs,rowlabels,report=rows_for_labels(T,labels,P['low_columns']);w=json.loads((HERE/'joint_integer_result.json').read_text())['integer_core_values'];original=core['source_lower'][:];keep=core['metadata']['source_metadata']['retained_indices']
for j,a in zip(keep,w):original[j]+=a
fail=[i for i,(row,b)in enumerate(zip(rows,rhs))if sum(a*v for a,v in zip(row,original))!=b]
reduced_rows=[[row[j] if j<len(row)else 0 for j in keep]for row in rows];reduced_rhs=[b-sum(a*v for a,v in zip(row,core['source_lower']))for row,b in zip(rows,rhs)]
out={'tensor_sha256':source['tensor_sha256'],'rows':reduced_rows,'rhs':reduced_rhs,'report':report,'failed_rows':fail,'outcome':'exact_joint_Galois_survivor'if not fail else'new_integer_phase_witness_fails_joint_Galois'}
(HERE/'new_joint_galois.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print(out['outcome'],'joint rows',len(rows),'failures',len(fail),'seconds',time.monotonic()-start,flush=True)
