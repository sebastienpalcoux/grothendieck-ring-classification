#!/usr/bin/env python3
"""Rebuild the first failing system in a selected external ground backend.

Set SYMPY_GROUND_TYPES=python or =flint before starting this script.
Requires the unchanged source inputs bound by commitments.json.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys,json,gzip,argparse
from pathlib import Path
from common import DEFAULT_REPO,bound_inputs,require
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',type=Path,default=DEFAULT_REPO)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args();base,row,entry,commitments=bound_inputs(a.repo)
sys.path.insert(0,str(base/'software'))
import sympy as s
import signed_spherical_traces as st
from rings import Characters
from exact import pc
R=row['N'];sphere=entry['certificate']['sphere'];char=Characters(R,sphere['generator'])
c=next(x['obstruction']['certificate'] for x in sphere['characters'] if x['obstruction']['kind']=='signed_spherical_traces')
f=next(f for f,m in char.components if pc(f)==c['factor'])
data,tab=st.data_and_table(R,char,f,c['table'])
branch=c['branches'][85];case=branch['cases'][16];cols=data['lows'][85]
require(list(map(list,cols))==branch['columns'],'low matrix changed')
L=s.Matrix.hstack(*map(s.Matrix,cols));_,high=st.high_columns(data,L);sp=st.Spectrum(tab,cols,high)
require(sp.metadata()==branch['spectrum'],'spectrum changed')
A,b=st.equation_system(R,data,tab,cols,case['indicators'],c['height'],case['labelling'],sp)
result={'A':A,'b':b,'y':case['y'],'metadata':sp.metadata(),
        'raw_spectrum_strings':[str(t) for t in sorted(set(sp.types),key=str)],
        'high_columns':[[list(v),list(map(str,z))] for v,z in high]}
a.output.parent.mkdir(parents=True,exist_ok=True)
a.output.write_bytes(gzip.compress((json.dumps(result,separators=(',',':'))+'\n').encode(),mtime=0))
print(json.dumps({'backend':s.external.gmpy.GROUND_TYPES,'rows':len(A),'columns':len(A[0]),'output':str(a.output)}))
