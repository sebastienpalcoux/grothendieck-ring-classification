#!/usr/bin/env python3
"""Finite exact R928 phase restrictions; no optimizer and no category claim.
Rebuilds all phase allocations from source-bound dimensions and N_W.
The categorical premises are stated in REPORT.md.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from itertools import combinations_with_replacement
import hashlib,json,math,sys
HERE=Path(__file__).resolve().parent
N=288
DEG=96
# Phi_288(x)=x^96-x^48+1; sparse integer coordinates in its power basis.
def root(k):
    k%=N; d={k:1}
    for i in range(k,DEG-1,-1):
        a=d.pop(i,0)
        if a:
            d[i-DEG//2]=d.get(i-DEG//2,0)+a
            d[i-DEG]=d.get(i-DEG,0)-a
    return tuple(sorted((i,a) for i,a in d.items() if a))
def add(*vs):
    d=Counter()
    for v in vs:
        for i,a in v:d[i]+=a
    return tuple(sorted((i,a) for i,a in d.items() if a))
def scale(k,v):return tuple((i,k*a) for i,a in v if k*a)
def mul(a,b):return add(*(scale(x*y,root(i+j)) for i,x in a for j,y in b))
RT=[root(i) for i in range(N)]
ONE=RT[0]
sqrt2=add(RT[N//8],RT[-N//8]);sqrt3=add(RT[N//12],RT[-N//12]);sqrt6=mul(sqrt2,sqrt3)
xi=RT[N//8]
def encode_dimension(d):return add(*(scale(int(a),b) for a,b in zip(d,(ONE,sqrt2,sqrt3,sqrt6))))
def need(b,msg):
    if not b:raise ValueError(msg)
