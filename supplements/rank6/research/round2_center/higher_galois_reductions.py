"""Discover and exactly verify tensor-parametric general-scope reductions."""
import argparse,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import galois_pseudo_reduction as G
ap=argparse.ArgumentParser();ap.add_argument('ids',nargs='+');ap.add_argument('--seconds',type=int,default=180);args=ap.parse_args()
rows={r['id']:r['N'] for r in json.loads((ROOT/'data/census.json').read_text())}
for name in args.ids:
 started=time.monotonic()
 try:
  c=G.certificate(rows[name],timeout=args.seconds)
  report=G.verify(rows[name],c) if c else None
  record={'id':name,'outcome':'general_to_galois_pseudo_unitary' if c else 'no_exact_reduction','certificate':c,'report':report}
 except Exception as e:
  record={'id':name,'outcome':'incomplete','certificate':None,'error':type(e).__name__+': '+str(e)}
 record['seconds']=time.monotonic()-started
 Path(__file__).with_name('galois_reduction_'+name+'.json').write_text(json.dumps(record,separators=(',',':'))+'\n')
 print(json.dumps({k:v for k,v in record.items() if k!='certificate'}),flush=True)
