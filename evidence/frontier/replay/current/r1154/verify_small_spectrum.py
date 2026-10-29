#!/usr/bin/env python3
"""Optional finite zero/one-spectrum replay; compiler required, no category claim."""
from pathlib import Path
import hashlib,importlib.util,json,os,shutil,subprocess,tempfile
P=Path(__file__).resolve().parent
compiler=shutil.which('g++')
if not compiler:raise RuntimeError('Optional native check requires g++ with C++17 support.')
spec=importlib.util.spec_from_file_location('tensors',P.parent/'current_remaining_cases.py')
tensors=importlib.util.module_from_spec(spec);spec.loader.exec_module(tensors)
records=[]
with tempfile.TemporaryDirectory(prefix='r1154-spectrum-') as tmp:
 executable=Path(tmp)/('small_spectrum.exe' if os.name=='nt' else 'small_spectrum')
 subprocess.run([compiler,'-O2','-std=c++17',str(P/'small_spectrum.cpp'),'-o',str(executable)],check=True,capture_output=True,text=True,timeout=30)
 for name,N,expected in [('rank7',json.loads((P/'rank7_dual_1.json').read_text()),858857),('rank8',tensors.TENSORS['R8_3_1154'],293728)]:
  data=(P/f'{name}.txt').read_text();flat=list(map(int,data.split()));n=flat[0]
  if n!=len(N) or flat[1:]!=[v for row in N for col in row for v in col]:raise ValueError(f'{name} input tensor mismatch')
  result=subprocess.run([str(executable)],input=data,capture_output=True,text=True,check=True,timeout=30)
  want=f'No zero/one spectrum witness; eligible configurations={expected}\n'
  if result.stdout!=want:raise ValueError(f'{name} unexpected result: {result.stdout}')
  records.append({'case':name,'eligible_configurations':expected,'zero_or_one_spectrum_witness':False})
receipt={'status':'PASS','scope':'Finite necessary zero/one-spectrum tests only; no associators or categorification inferred.','records':records}
(P/'small_spectrum_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
