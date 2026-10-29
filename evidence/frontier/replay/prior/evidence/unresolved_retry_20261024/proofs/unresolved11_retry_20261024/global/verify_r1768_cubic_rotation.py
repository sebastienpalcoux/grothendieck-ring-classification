"""Exact finite phase sum for the trivalent linear associativity comparison.

Categorical contraction is derived in R1768_CUBIC_ROTATION.md.
This receipt does not establish a multiplication on 1+sigma.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

def require(test,message):
    if not test:
        raise RuntimeError(message)

def saw(x):
    y=x-x.numerator//x.denominator
    return Q(0) if y==0 else y-Q(1,2)

dedekind=sum(saw(Q(k,12))*saw(Q(k,12)) for k in range(1,12))
exponent=Q(146,144)-dedekind-Q(1,4)
require(dedekind==Q(55,72) and exponent==0,"eta multiplier")
matrix=[]
for i in range(2):
    row=[]
    for j in range(2):
        total=0
        for a in range(12):
            for l in range(12):
                for m in range(12):
                    for n in range(12):
                        if (a,a)!=(n,(n+6*(i+j))%12):
                            continue
                        require(i==j and a==n,"off-diagonal coset cancellation")
                        qsign=(-1)**(i*(l+1))
                        bsign=(-1)**(i*(l+a+m))
                        prefactor=(-1)**(i+i*(a+m))
                        term=prefactor*qsign*bsign
                        require(term==1,"termwise phase cancellation")
                        total+=term
        row.append(Q(total,1728))
    matrix.append(row)
require(matrix==[[Q(1),Q(0)],[Q(0),Q(1)]],"rotation comparison")
receipt={"dedekind_sum":"55/72","eta_exponent_pi_i":"0",
         "lambda":"1","linear_associativity_matrix":[[str(x) for x in row] for row in matrix],
         "conclusion":"both multiplication directions survive; no algebra existence proven",
         "status":"PASS"}
Path(__file__).with_name("r1768_cubic_rotation_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print("PASS: linear associativity comparison is I_2; nonlinear algebra equation remains")
