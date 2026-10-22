"""Read-only accepted replay: arithmetic, all forty branches, final alpha cone."""
import sys
sys.dont_write_bytecode=True
import json
from verify_all import HERE,run,fibres
if __name__=='__main__':
 result=run()
 fibres.f.require(result==json.loads((HERE/'verification.json').read_text()),'final receipt changed')
 print(json.dumps(result,indent=2),flush=True)
