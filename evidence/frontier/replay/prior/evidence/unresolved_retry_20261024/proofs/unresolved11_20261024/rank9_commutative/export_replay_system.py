"""Export a reconstructed and exactly replayed necessary system for portability."""
import gzip,hashlib,json,runpy,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
rid=sys.argv[1]
sys.argv=[str(HERE/'screen_integral_center.py'),rid,'4','180','1','--verify']
ns=runpy.run_path(sys.argv[0],run_name='__main__')
payload={'A':ns['A'],'b':ns['b'],'ray':ns['ray'],
         'system_sha256':ns['system_sha'],'tensor_sha256':ns['tensor_sha'],
         'scope':'conditional exclusion of TY sign +1, not a full source-ring exclusion',
         'theorems':['NO_CENTRAL_BOSON.md','TY_SPECTRUM.md']}
path=HERE/f'{rid}_tau1_exact_system.json.gz'
with gzip.open(path,'wt') as f:json.dump(payload,f,separators=(',',':'))
files=[HERE/'screen_integral_center.py',Path(ns['qs'].__file__),Path(ns['qc'].__file__)]
binding={str(f.relative_to(HERE.parents[1])):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
binding['export_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
(HERE/f'{rid}_tau1_source_binding.json').write_text(json.dumps(binding,indent=2)+'\n')
print('EXPORTED',path.name,flush=True)
