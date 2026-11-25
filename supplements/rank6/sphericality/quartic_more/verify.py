"""Run the extended half-mass and non-half-mass quartic certificates."""
from half_bound import CONDUCTORS,bound
from half_candidates import run as test_half
from three_nonhalf import run as test_nonhalf
from two_nonhalf import run as test_two_nonhalf, FIELDS,CYCLIC
from nonhalf_bound import bound as mixed_bound
from field_caps import check as check_caps
from c20_candidates import run as test_c20
from silvergold import run as test_silvergold
from c20_bound import bound as c20_bound
from math import isqrt
from fractions import Fraction as F

if __name__=='__main__':
    for cs,adjust in zip(CONDUCTORS,(0,4,4,4,16,2,2,2,2,4)):
        assert bound(cs,64,adjust)
    test_half()
    test_nonhalf(False)
    check_caps()
    s,t=F(1,2),F(5,8)
    for cs in [r[:3] for r in FIELDS]+[r[:2] for r in CYCLIC]:
        assert mixed_bound(cs,256,s,s,t,t,F(1,4),F(1,8))
        assert mixed_bound(cs,256,s,s,t,F(11,16),F(1,2),F(1,4))
    assert mixed_bound((8,28,56),256,t,t,t,t,t,F(0))
    test_two_nonhalf(False)
    short={(L,N) for N in range(1,360) for L in range(10,N//2+1,5)
           if 3*L>N and L*L%N==0 and 0<L*L-4*N<=N*N//10
           and 5*isqrt((L*L-4*N)//5)**2==L*L-4*N}
    assert short=={(10,20)}
    for case in [(F(11,20),F(11,20),F(11,20),None,False),
                 (F(3,5),F(3,5),F(3,5),None,False),
                 (F(1,2),F(1,2),F(1,2),F(1,2),False),
                 (F(1,2),F(1,2),F(1,2),None,True)]:
        assert c20_bound(128,*case)
    test_c20(False)
    sg=(8,5,40)
    assert mixed_bound(sg,76,s,s,s,s,s,F(1,2))
    assert mixed_bound(sg,48,s,s,s,s,s,F(1,2),shift_min=F(1),chi_bounds={5:(F(45,100),F(224,1000))})
    for H in (9,16):
        t=F(3,4)-F(1,H)
        for b in range(1,H//4+1):
            u=F(3,4)-F(b,H);w=F(1,4)+F(b*b,H)
            if u not in (F(19,36),F(9,16)):
                assert mixed_bound(sg,300,u,u,t,t,int(w+1)-w,None)
    test_silvergold(False)
