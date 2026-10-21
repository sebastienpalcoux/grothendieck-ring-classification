"""All distinguished forgetful product coordinates on new joint integer witness."""
from pathlib import Path
import json,itertools,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
R=next(row['tensor'] for row in json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text()) if row['id']=='R8_3_982')
P=json.loads((ROOT/'evidence/rank8_frontier_20261021/commutative_integer/R8_3_982_profile.json').read_text())['records'][2];S=json.loads((HERE/'frame2_system.json').read_text());W=json.loads((HERE/'joint_integer_result.json').read_text())['integer_core_values'];original=S['source_lower'][:]
for j,v in zip(S['metadata']['source_metadata']['retained_indices'],W):original[j]+=v
meta=S['metadata']['source_metadata']['source_metadata'];fp=meta['FP_character'];du=meta['dual_characters'];labels=[E for E in range(8)if E!=fp];triples=[(E,F,G)for E,F in itertools.combinations_with_replacement(labels,2)for G in labels];high=len(P['duality_orbits']);fusion=dict(zip(triples,original[high:high+196]));low=dict(zip(P['character_labels'],P['low_columns']));reports=[]
for E,F in itertools.combinations_with_replacement(labels,2):
 product=[sum(low[E][i]*low[F][j]*R[i][j][k]for i in range(8)for j in range(8))for k in range(8)]
 residual=[product[k]-int(k==0 and F==du[E])-sum(fusion[E,F,G]*low[G][k]for G in labels)for k in range(8)]
 reports.append({'pair':[E,F],'residual_high_restriction':residual,'unit_exact':residual[0]==0,'coordinate_nonnegative':min(residual)>=0})
out={'tensor_sha256':S['tensor_sha256'],'pairs':reports,'all28_unit_exact':all(r['unit_exact']for r in reports),'all196_high_coordinate_bounds':all(r['coordinate_nonnegative']for r in reports)}
(HERE/'forgetful_product_probe.json').write_text(json.dumps(out,indent=2)+'\n');print('all28unit',out['all28_unit_exact'],'all196nonnegative',out['all196_high_coordinate_bounds'])
