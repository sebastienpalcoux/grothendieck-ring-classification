#!/usr/bin/env python3
"""Verify complete exact row equivalence and transported Farkas inequalities.

Standard library only. This is a first-failure-system comparison, not the
full-ring replay. No discovered or replacement inequality is accepted.
"""
import gzip,json
from collections import defaultdict,deque
from common import PACKET,require,digest
receipt=json.loads((PACKET/'full_replay_receipt.json').read_text())
for name in ('system_python.json.gz','system_flint.json.gz','row_equivalence.json'):
 require(digest(PACKET/name)==receipt['packet_files_sha256'][name],'packet hash mismatch: '+name)
py,fl=[json.loads(gzip.decompress((PACKET/name).read_bytes())) for name in ('system_python.json.gz','system_flint.json.gz')]
proof=json.loads((PACKET/'row_equivalence.json').read_text())
require(py['high_columns']==fl['high_columns'],'different high columns')
require(py['metadata']==fl['metadata'],'different spectral metadata')
require(len(py['b'])==len(fl['b'])==419,'wrong row count')
require(all(len(row)==1237 for row in py['A']+fl['A']),'wrong column count')
perm=proof['signed_row_permutation']
require(sorted(x[0] for x in perm)==sorted(x[1] for x in perm)==list(range(419)),'not a row permutation')
transported=[0]*419
for i,j,sign in perm:
 require(sign in (-1,1),'invalid sign')
 require(py['A'][i]==[sign*x for x in fl['A'][j]] and py['b'][i]==sign*fl['b'][j],'equations differ')
 transported[j]=sign*py['y'][i]
require(transported==proof['transformed_y'],'incorrect transported vector')
def inequality(system,y):
 require(len(y)==len(system['b']) and all(type(x) is int for x in y),'invalid vector')
 vals=[sum(row[j]*v for row,v in zip(system['A'],y) if v) for j in range(1237)]
 rhs=sum(b*v for b,v in zip(system['b'],y))
 return min(vals),rhs
require(inequality(py,py['y'])==(0,-941616),'original Python witness does not pass')
require(inequality(fl,fl['y'])==(-36864,-941616),'initial flint failure changed')
require(inequality(fl,transported)==(0,-941616),'transported flint witness does not pass')
require(sum(i!=j for i,j,sg in perm)==210 and all(sg==1 for i,j,sg in perm),'unexpected permutation')
print(json.dumps({'status':'PASS','scope':'first failing case, exact row equivalence','rows':419,'columns':1237,'moved_rows':210,'sign_changes':0,'min_transported_ATy':0,'bTy':-941616}))
