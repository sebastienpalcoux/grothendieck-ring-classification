"""Replay the compressed complete triple census and its bounded-row filter."""
import gzip,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def digest(p):
 with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
archive=HERE/'joint_triple_after_a2.json.gz';rowpath=HERE/'bounded_high0_rows.json'
with gzip.open(archive,'rb')as f:data=json.load(f)
need(data['complete']and data['all_histogram_solutions_enumerated'],'complete triple histogram archive')
need(data['verifier_sha256']==digest(HERE/'joint_triple_after_a2.py'),'archive enumerator binding')
for name,value in data['source_sha256'].items():need(digest(ROOT/name)==value,'archive source binding '+name)
bounds=json.load(rowpath.open());need(bounds['verifier_sha256']==digest(HERE/'bounded_high0_rows.py'),'bounded row verifier binding')
by={(r['index'],r['pair_histogram']):{rr['pair11']:set(rr['surviving_triple133'])for rr in r['rows']}for r in bounds['results']}
filtered=[]
for row in data['results']:
 key=(row['index'],row['histogram_solution']);witnesses=row.pop('witnesses');row['histogram_count']=len(witnesses)
 if key in by:
  accepted=[i for i,his in enumerate(witnesses)if all(all(z in by[key][v['pair11']]for z,n in v['triple133_histogram']if n)for v in his if v['type']==0)]
  filtered.append({'index':key[0],'pair_histogram':key[1],'incoming_triple_histograms':len(witnesses),'surviving_triple_histogram_indices':accepted,'surviving_triple_histograms':len(accepted)})
sha=hashlib.sha256();size=0
with gzip.open(archive,'rb')as f:
 while chunk:=f.read(1024*1024):sha.update(chunk);size+=len(chunk)
data['compressed_complete_histograms']={'file':archive.name,'bytes':archive.stat().st_size,'gzip_sha256':digest(archive),'uncompressed_bytes':size,'uncompressed_sha256':sha.hexdigest()};data['histogram_total']=sum(r['histogram_count']for r in data['results'])
summary=HERE/'joint_triple_after_a2.summary.json';need(json.load(summary.open())==data,'complete triple summary replay')
result={'schema':'r1154-bounded-high0-triple-filter/v1','incoming_patterns':3,'incoming_triple_histograms':sum(r['incoming_triple_histograms']for r in filtered),'remaining_patterns':len({r['index']for r in filtered if r['surviving_triple_histograms']}),'surviving_triple_histograms':sum(r['surviving_triple_histograms']for r in filtered),'results':filtered,'source_sha256':{p.name:digest(p)for p in [archive,rowpath]}}
need(json.load((HERE/'bounded_high0_triple_filter.json').open())==result,'bounded row filtering replay')
print(json.dumps({'status':'PASS','complete_triple_histograms':data['histogram_total'],'remaining_triple_histograms_after_bounded_rows':result['surviving_triple_histograms'],'remaining_patterns':result['remaining_patterns'],'verifier_sha256':digest(Path(__file__))}))
