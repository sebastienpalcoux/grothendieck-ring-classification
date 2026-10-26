#!/usr/bin/env python3
from itertools import product
# All exponents are modulo8.
def w(a,b,c):return 2*a*((b+c)//4)%8
def add(a,b):return(a+b)%4
def c(x):return 3*x%8
for a,b,e,f in product(range(4),repeat=4):
    if(w(b,e,f)+w(a,add(b,e),f)+w(a,b,e)-w(add(a,b),e,f)-w(a,b,add(e,f)))%8:
        raise ValueError('3-cocycle')
for x,y in product(range(4),repeat=2):
    if(c(add(x,y))-c(x)-c(y)-w(x,2,y)+w(2,x,y)+w(x,y,2))%8:
        raise ValueError('half-braiding')
for x in range(4):
    if(2*c(x)+w(2,2,x)+w(x,2,2)-w(2,x,2))%8:raise ValueError('central square')
if c(2)!=6 or w(2,2,2)!=4:raise ValueError('reverse semion')
print('PASS: exact C4 cocycle, central order-two reverse semion, free action, X*=sX')
