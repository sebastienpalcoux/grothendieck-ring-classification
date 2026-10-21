"""Exact symbolic primitive-eighth-root refinement, with no Galois assumption."""
import json
import sys
sys.dont_write_bytecode=True
import sympy as s
from modular_completion import prepare
from twist_balancing import need

def main():
    source,R,a,S0,columns,Ns,Q,vectors,va,vc=prepare()
    root=s.sqrt(17);alpha=21+5*root
    convert=lambda x:s.expand(sum(s.Rational(str(v))*alpha**j for j,v in enumerate(reversed(x.to_list()))))
    D=convert(a['D']);fixed=s.Matrix(22,22,lambda i,j:convert(S0[i][j])/D)
    e=vectors[1];x,y,z,omega=s.symbols('x y z omega',nonzero=True)
    # x,y,z are merely matrix parameters; do not assume they are nonzero.
    x,y,z=s.symbols('x y z')
    unknown=(x*e[0]*e[0].T+y*(e[0]*e[1].T+e[1]*e[0].T)+z*e[1]*e[1].T)/2
    twists=[1]*5+[-1]*4+[1]+[omega,-omega,s.I*omega,-s.I*omega]
    solution={x:0,y:-s.I/omega**2,z:0};checked=0
    for sign in (1,-1):
        S=fixed-Q[0]+sign*(va*vc.T+vc*va.T)+unknown
        equations=[]
        for i in [0,5,6,7,8]:
            for j in (10,11,12,13):
                # All D-row entries here are fixed and equal. Their ordinary
                # twist sum was proved by the low-low STS certificate.
                lhs=sum(S[i,k]*twists[k]*S[k,j]for k in range(14))+fixed[i,14]*fixed[14,j]*(-(1+root)/2)
                equations.append(s.expand(lhs-S[i,j]/twists[i]/twists[j]))
        solved=s.solve(equations,(x,y,z))
        need(solved==solution,'unique C-difference S block for arbitrary omega')
        need(all(s.simplify(e.subs(solution))==0 for e in equations),'all selected STS entries exactly zero')
        checked+=len(equations)
    block=s.Matrix([[0,-s.I/omega**2],[-s.I/omega**2,0]])
    need(block*block==-s.eye(2)/omega**4,'S-square on the invariant C-difference space')
    print(json.dumps(dict(ring='R8_3_721',source_tensor_sha256=source['tensor_sha256'],
          scope='Necessary twist refinement only; no category is constructed.',
          arbitrary_C_twists=['omega','-omega','i*omega','-i*omega'],
          selected_STS_equations_checked=checked,cross_signs_checked=[1,-1],
          forced_C_difference_S=[['0','-i/omega^2'],['-i/omega^2','0']],
          S_square_on_C_difference_space='-omega^(-4) * identity',
          C_objects_selfdual_reason='The four twists are pairwise distinct and duality preserves their common restriction type and twist.',
          conclusion='omega^4=-1: the four C twists are precisely the primitive eighth roots.'),indent=2))

if __name__=='__main__':main()
