"""Recreate all conductor lists, trace lattices and dual tests outside the 24 fields.
Run with Python 3.10+ and a C++17 compiler. Verification uses the standard
library, integer arithmetic and rational intervals, with no optimizer.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = 'higher_degree_quartic_'
FILES = ['bounds.py','cyclic_fields.py','biquadratic.cpp','cyclic.cpp','polytope.py',
         'cyclic_polytope.py','biquadratic_polytope.json','cyclic_polytope.json']


def main():
    if not __debug__:
        raise ValueError('Use unoptimized Python so that all assertions are enabled.')
    with tempfile.TemporaryDirectory() as temporary:
        root=Path(temporary)
        env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
        def run(*args):
            return subprocess.run(list(map(str,args)),cwd=root,env=env,check=True,
                                  stdout=subprocess.PIPE,text=True).stdout
        for name in FILES:
            shutil.copyfile(HERE/(PREFIX+name),root/(PREFIX+name))
        print(run(sys.executable,PREFIX+'bounds.py'),end='',flush=True)
        bound=json.loads((root/(PREFIX+'bounds_certificate.json')).read_text())
        assert bound['exceptional_fields']['count']==24
        rows=[r['conductors']+[r['trace_cap']] for r in bound['fields']['biquadratic'] if r['trace_cap']]
        assert len(rows)==710
        (root/(PREFIX+'biquadratic_fields.txt')).write_text(''.join(' '.join(map(str,r))+'\n' for r in rows))
        print(run(sys.executable,PREFIX+'cyclic_fields.py'),end='',flush=True)
        assert len((root/(PREFIX+'cyclic_fields.txt')).read_text().splitlines())==232
        def branch(name):
            run('g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',
                PREFIX+name+'.cpp','-o',root/name)
            output=run(root/name,PREFIX+name+'_fields.txt', PREFIX+name+'_candidates.txt')
            report=dict((k,int(v)) for k,v in (l.split() for l in output.splitlines()))
            expected=(96433626,258) if name=='biquadratic' else (7581015,281)
            countkey='canonical_primitive_tuples' if name=='biquadratic' else 'canonical_tuples'
            assert (report[countkey],report['dnumbers'])==expected
            weights=json.loads((root/(PREFIX+name+'_polytope.json')).read_text())
            assert len(weights['certificates'])==expected[1] and not weights['survivors']
            verifier='polytope.py' if name=='biquadratic' else 'cyclic_polytope.py'
            print(name,output,run(sys.executable,PREFIX+verifier,'--verify'),sep='\n',flush=True)
        with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(branch,['biquadratic','cyclic']))
        print('PASS: 539 primitive presentations excluded; the remaining list consists of 24 fields.')

if __name__=='__main__':main()
