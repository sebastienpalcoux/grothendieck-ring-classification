"""Run one assertion-enabled replay stage and record repository file reads."""
from pathlib import Path
import hashlib, importlib.util, json, os, runpy, sys
if not __debug__:
    raise RuntimeError('Proof stages require assertions enabled.')
PACKAGE=Path(__file__).resolve().parents[1];ROOT=PACKAGE.parents[1]
report=Path(sys.argv[1]);target=Path(sys.argv[2]).resolve();arguments=sys.argv[3:]
opened={target,Path(__file__).resolve()}
def audit(event,args):
    if event!='open' or not isinstance(args[0],(str,bytes,os.PathLike)):return
    p=Path(os.fsdecode(args[0])).resolve()
    if p.suffix=='.pyc':
        try:p=Path(importlib.util.source_from_cache(str(p)))
        except ValueError:return
    try:p.relative_to(ROOT)
    except ValueError:return
    if p.is_file():opened.add(p)
sys.addaudithook(audit)
sys.argv=[str(target)]+arguments;sys.path.insert(0,str(target.parent))
runpy.run_path(str(target),run_name='__main__')
files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(opened)if p.is_file()}
report.write_text(json.dumps(files,indent=2)+'\n')
