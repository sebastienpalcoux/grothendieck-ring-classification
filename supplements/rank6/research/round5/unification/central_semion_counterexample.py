"""Exact pointed counterexample to a proposed central semion splitting rule."""
import itertools,json

def need(x,m):
 if not x:raise ValueError(m)
def w(a,b,c):return 2*a*((b+c)//4)%8
add=lambda a,b:(a+b)%4
gamma=lambda x:3*x%8
n=0
for a,b,c,d in itertools.product(range(4),repeat=4):
 need((w(b,c,d)+w(a,add(b,c),d)+w(a,b,c)-w(add(a,b),c,d)-w(a,b,add(c,d)))%8==0,'pentagon');n+=1
for x,y in itertools.product(range(4),repeat=2):
 need((gamma(x)+gamma(y)-gamma(add(x,y))-w(2,x,y)-w(x,y,2)+w(x,2,y))%8==0,'half-braiding hexagon')
for x in range(4):need((2*gamma(x)+w(2,2,x)+w(x,2,2)-w(2,x,2))%8==0,'lift square')
need(gamma(2)==6,'self-braiding must be -i')
print(json.dumps(dict(passed=True,pentagon_checks=n,hexagon_checks=16,lift_square_checks=4,self_braiding_exponent_mod8=6,underlying_fusion_group='C4',proposed_product_fusion_group='C2xC2')))
