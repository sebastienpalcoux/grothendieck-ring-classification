"""Reject mutations invisible to the multiplicativity equations alone."""
import json,subprocess,sys,tempfile,copy
from pathlib import Path
HERE=Path(__file__).resolve().parent
record=json.loads((HERE/'cyclic8_center_tensor.json').read_text())
mutations=[]
v=copy.deepcopy(record);v['F']=[[0]*6 for _ in range(22)];mutations.append(('zero restriction',v))
v=copy.deepcopy(record);v['F'].pop();mutations.append(('missing row',v))
v=copy.deepcopy(record);v['labels'][0]=['not the unit'];mutations.append(('wrong label',v))
v=copy.deepcopy(record);v['F'][0]=[0,1,0,0,0,0];mutations.append(('wrong unit',v))
with tempfile.TemporaryDirectory(prefix='center-mutations-') as td:
    for j,(label,v) in enumerate(mutations):
        p=Path(td)/f'mutant_{j}.json';p.write_text(json.dumps(v))
        result=subprocess.run([sys.executable,'-O',str(HERE/'exact_cyclic8_center.py'),'--tensor-certificate',str(p)],capture_output=True,text=True,timeout=20)
        if result.returncode==0:
            raise RuntimeError(f'mutation accepted: {label}')
        if 'AssertionError' not in result.stderr:
            raise RuntimeError(f'mutation did not fail an explicit certificate check: {label}: {result.stderr}')
        print(f'rejected: {label}')
