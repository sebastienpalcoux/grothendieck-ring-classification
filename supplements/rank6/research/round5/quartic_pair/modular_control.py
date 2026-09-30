"""Categorical positive control for generalized composite rotations: Z(Vec_C3)."""
import json,sys
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
from exact import field,t,require
from round5_modular_checks import check_variant
import scipy.optimize
def denied(*_,**__):raise RuntimeError('numerical optimizer disabled during replay')
scipy.optimize.linprog=scipy.optimize.milp=denied
R=[[[int((a+b)%3==c) for c in range(3)] for b in range(3)] for a in range(3)]
C=field(s.Poly(s.cyclotomic_poly(15,t),t));data=dict(C=C,F=15,DD=C(3),dims=[C.one]*3);labels=[(a,b) for a in range(3) for b in range(3)]
W=[[int(a==c) for c in range(3)] for a,b in labels];ds=[C.one]*9;ee=[5*a*b%15 for a,b in labels];S=[[C.unit**((-5*(a*d+b*c))%15)/C(3) for c,d in labels] for a,b in labels]
checks=check_variant(R,data,W,ds,S,ee,[4,6,8,9,10,12,14,15,16])
require(checks['passed'],'known categorical control failed')
print(json.dumps(dict(passed=True,optimizer_used=False,python_optimized=not __debug__,category='Vec(C3)',center='Z(Vec(C3))',checks=checks),indent=2))
