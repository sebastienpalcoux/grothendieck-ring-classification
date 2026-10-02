"""Bounded exact number-field arithmetic and real-root sign isolation."""
import sympy as s
T=s.Symbol('t')

def require(condition, message='certificate condition failed'):
    if not condition:
        raise ValueError(message)

def polynomial(coefficients):
    return s.Poly.from_list([s.Rational(x) for x in coefficients], T, domain=s.QQ)

class Embedding:
    def __init__(self, f, interval):
        self.f=f
        self.lo,self.hi=map(s.Rational,interval)
        self.cache={}
        require(self.lo<self.hi and f.count_roots(self.lo,self.hi)==1, 'invalid root interval')
    def sign(self, value):
        if not value:
            return 0
        coefficients=tuple(s.Rational(x) for x in value.to_list())
        if coefficients in self.cache:
            return self.cache[coefficients]
        for unused in range(256):
            low=high=s.S.Zero
            for coefficient in coefficients:
                products=(low*self.lo,low*self.hi,high*self.lo,high*self.hi)
                low,high=min(products)+coefficient,max(products)+coefficient
            if low>0 or high<0:
                result=1 if low>0 else -1
                self.cache[coefficients]=result
                return result
            self.lo,self.hi=self.f.refine_root(self.lo,self.hi,steps=6)
        raise ValueError('sign isolation exceeded the explicit refinement bound')
