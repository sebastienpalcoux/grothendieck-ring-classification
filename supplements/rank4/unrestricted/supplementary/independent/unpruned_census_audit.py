#!/usr/bin/env python3
"""Disable both dimension prunings in a temporary enumerator, then filter in Python.
The Diophantine elimination remains the author's implementation: this tests
pruning and boundary consistency, not an independent all-rank completeness proof.
"""

def require(test, message='independent check failed'):
    if not test:
        raise RuntimeError(message)

import argparse,json,subprocess,tempfile,time
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('archive',type=Path);p.add_argument('--output',type=Path)
a=p.parse_args();root=a.archive/'supplementary/census';start=time.monotonic()
manifest=json.loads((root/'data/manifest.json').read_text())
M=manifest['maximum_multiplicity'];D=manifest['dimension_exclusive_bound']
source=(root/'enumerate.cpp').read_text()
require(source.count('bool bounded(const T&R,I D){') == 1, 'check failed (unpruned_census_audit.py:11)')
source=source.replace('bool bounded(const T&R,I D){','bool bounded(const T&R,I D){ return true;')
prune='if(2+2*b*b+2*c*c+d*d+2*e*e+f*f>=D)continue;'
require(source.count(prune) == 1, 'check failed (unpruned_census_audit.py:14)')
source=source.replace(prune,'/* dimension diagonal pruning disabled for audit */')
with tempfile.TemporaryDirectory()as t:
    t=Path(t);(t/'enumerate.cpp').write_text(source)
    subprocess.run(['g++','-O3','-std=c++17',str(t/'enumerate.cpp'),'-o',str(t/'enumerate')],check=True)
    raw=subprocess.run([str(t/'enumerate'),str(M),str(D)],check=True,text=True,capture_output=True).stdout
# Use independent direct determinant expansion, not Bareiss or rank4.py.
def det(M):
    if len(M)==1:return M[0][0]
    return sum((-1)**j*M[0][j]*det([r[:j]+r[j+1:]for r in M[1:]])for j in range(len(M)))
def tensor(tag,p):
    unit=[[int(i==j)for j in range(4)]for i in range(4)]
    if tag=='S':
        a,b,c,d,e,f,g,h,i,j=p
        return [unit,[[0,1,0,0],[1,a,b,c],[0,b,d,e],[0,c,e,f]],[[0,0,1,0],[0,b,d,e],[1,d,g,h],[0,e,h,i]],[[0,0,0,1],[0,c,e,f],[0,e,h,i],[1,f,i,j]]]
    a,b,c,d,e,f=p
    X=[[0,1,0,0],[1,a,b,b],[0,b,c,d],[0,b,d,c]]
    Y=[[0,0,1,0],[0,b,c,d],[0,d,e,f],[1,c,e,e]]
    return [unit,X,Y,list(map(list,zip(*Y)))]
kept=[];rawlines=raw.splitlines()
for line in rawlines:
    tag,*v=line.split();R=tensor(tag,list(map(int,v)))
    Q=[[D*int(i==j)-sum(R[k][i][z]*R[k][j][z]for k in range(4)for z in range(4))for j in range(4)]for i in range(4)]
    if all(det([row[:k]for row in Q[:k]])>0 for k in range(1,5)):kept.append(line)
expected=(root/'data/parameters.txt').read_text().splitlines()
require(len(set(rawlines)) == len(rawlines), 'check failed (unpruned_census_audit.py:39)')
require(set(kept) == set(expected) and len(kept) == len(expected), 'check failed (unpruned_census_audit.py:40)')
result={'passed':True,'unpruned_rings':len(rawlines),'strict_dimension_survivors':len(kept),
        'exact_parameter_set_equality':True,'seconds':round(time.monotonic()-start,3),
        'independence':'Authors elimination; both dimension prunings removed; independent direct determinant expansion in Python.'}
print(json.dumps(result,indent=2))
if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
