import sys,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import round3_smallest as C
R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']=='R6_4_6');fam=C.family(R);modules=C.module_data(R,fam);data,tab=C.H.I.reciprocity_data(R)
proto=json.load(open(Path(__file__).with_name('probe_twist.json')));branches=[];st=time.time()
for ix,cols in enumerate(data['lows']):
 rows=[x for x in proto if x['frame']==ix];rec={'columns':list(map(list,cols))}
 if 'ordinary' in rows[0]:rec['ordinary']=rows[0]['ordinary']
 else:
  ep=rows[0]['ep'];A,b,meta=C.system(R,data,tab,cols,ep,6,fam,modules)
  rec['cases']=[dict(indicators=x['ep'],system=meta,ray=x['ray']) for x in rows]
  C.require(all(x['excluded'] and x['rows']==len(A) and x['cols']==len(A[0]) for x in rows),'prototype system mismatch')
 branches.append(rec);print(ix,flush=True)
c={'kind':'c4_associator_stabilizer','version':1,'scope':'general','family':fam,'modules':modules,'method':'forced_twist_trace','reduction':{'kind':'two_fp_values'},'height':6,'q':data['q'],'prime_support':data['primes'],'column_counts':list(map(len,data['columns'])),'branches':branches}
out={'id':'R6_4_6','outcome':'general_excluded','certificate':c,'source':'exact rays from probe_twist.py; regenerated system metadata','seconds':time.time()-st}
Path(__file__).with_name('R6_4_6_height6.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
