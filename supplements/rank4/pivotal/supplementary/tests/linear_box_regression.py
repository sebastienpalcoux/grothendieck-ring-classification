#!/usr/bin/env python3
"""Compare generic row reduction with exhaustive integer boxes."""
import argparse,json,subprocess,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--output',type=Path,default=ROOT/'linear_box_results.json')
a=p.parse_args();start=time.monotonic()
with tempfile.TemporaryDirectory(prefix='rank4-linear-box-') as t:
    exe=Path(t)/'linear_box_test'
    subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'linear_box_regression.cpp'),'-o',str(exe)],check=True)
    result=subprocess.run([str(exe)],capture_output=True,text=True,check=True)
report=json.loads(result.stdout);report['seconds']=round(time.monotonic()-start,3)
a.output.parent.mkdir(parents=True,exist_ok=True)
a.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
