"""Exact finite input for PALINDROMIC_EXCLUSION.md; no floating arithmetic."""
from pathlib import Path
import hashlib
import itertools
import json
import runpy

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/"prior"
rid="R8_3_1768"
expected="240509807c67da437c86f2a51efeb831364734feb93ed18a1d2f32087ebc1af0"
N=runpy.run_path(str(BASE/"data/current_remaining_cases.py"))["TENSORS"][rid]

def require(c,msg):
    if not c: raise RuntimeError(msg)

tensor_hash=hashlib.sha256(json.dumps(N,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
require(tensor_hash==expected,"exact tensor SHA256")
profile=json.loads((BASE/"evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/inputs/R8_3_1768.json").read_text())
require(profile["tensor_sha256"]==expected,"archived profile tensor binding")
r=next(x for x in profile["research"] if x["source"]=="evidence/rank8_creative_20261022/r1768/verification.json")
require(r["source_sha256"]=="2a2472719aa4e953b7f514dfb4f811a4bef162b2c779cf4bb367a6c21bb977b8","inherited indicator proof binding")
receipt=r["data"]
require(receipt["fibre_indicator_branches"]==40 and receipt["exact_infeasible_branches"]==39,"complete inherited branch count")
eps=[1]+receipt["surviving_branch"]["indicators"]
require(eps==[1,-1,1,1,1,1,1,1],"inherited forced indicators")
require(all(N[i][j][k]==N[j][i][k] for i,j,k in itertools.product(range(8),repeat=3)),"commutativity")
dual=[]
for i in range(8):
    choices=[j for j in range(8) if N[i][j][0]]
    require(choices==[i] and N[i][i][0]==1,"selfduality")
    dual.append(i)
require(N[2][2]==[1,0,1,1,2,2,2,2],"displayed square")
left=[sum(N[2][1][a]*N[a][dual[2]][k] for a in range(8)) for k in range(8)]
right=[sum(N[2][dual[2]][a]*N[1][a][k] for a in range(8)) for k in range(8)]
require(left==right==[0,1,2,2,2,2,1,1],"two contractions of X2 g X2*")
bad=[k for k in range(8) if eps[k]!=eps[1] and left[k]%2]
require(bad==[6,7],"two exact odd opposite-sign constituents")
out={
 "id":rid,"verification":"PASS","tensor_sha256":tensor_hash,
 "forced_indicators":eps,"X":2,"V":1,"restriction_XVXstar":left,
 "opposite_sign_odd_constituents":[{"index":k,"multiplicity":left[k],"indicator":eps[k]} for k in bad],
 "conclusion":"Contradiction to palindromic pairing parity, conditional only on the published forced indicators and existence-to-positive gate.",
 "computation_scope":"Exact tensor identities and inherited receipt binding. Categorical proof is separate in PALINDROMIC_EXCLUSION.md."
}
(HERE/"palindromic_exclusion_receipt.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
