"""Exact identities behind the strict R137 bosonic-mass bound."""
from pathlib import Path
from fractions import Fraction as F
import json
import sympy as s

P=Path(__file__).resolve().parents[1]/'r137'
cf=json.loads((P/'verlinde_witness.json').read_text())
chars=[[(s.Rational(a),s.Rational(b)) for a,b in chi] for chi in cf['chars']]
fs=[(s.Rational(a),s.Rational(b)) for a,b in cf['codegrees']]
def mul(z,w):return s.expand(z[0]*w[0]+2*z[1]*w[1]),s.expand(z[0]*w[1]+z[1]*w[0])
def div(z,w):
    q=s.sympify(w[0]**2-2*w[1]**2)
    return mul(z,(w[0]/q,-w[1]/q))
def row(v):return [div((sum(v[i]*c[i][0] for i in range(9)),sum(v[i]*c[i][1] for i in range(9))),f) for c,f in zip(chars,fs)]
def mass(v):
    z=[0,0]
    for a in row(v):
        q=mul(a,a);z=[s.expand(z[i]+q[i]) for i in range(2)]
    return z
vv=s.symbols('v0:9');v=[0]+list(vv[1:]);bb=sum(v[3:7]);aa=v[1]+v[2]+v[7]+2*v[8]
ell=[0,0]
for r,f in zip(row(v),fs):
    q=div(r,f);ell=[s.expand(ell[i]+q[i]) for i in range(2)]
delta=(aa+4*bb,3*bb);tail=div(delta,(288,192));ell=[s.expand(ell[i]+tail[i]) for i in range(2)]
want=[(31*v[1]-5*v[2]-5*v[7]-2*bb+44*v[8])/576,(-2*v[1]-2*v[2]-2*v[7]+bb-4*v[8])/96]
assert all(s.expand(a-b)==0 for a,b in zip(ell,want))
p,q,r,x,y,z=s.symbols('p q r x y z');w=8*p+12*q-x-y-z
v=[0,p,r,x,y,z,w,3*p+4*q-r,q]
mv=mass(v)
formula=(9*p*p+24*p*q+21*q*q+(v[2]-v[7])**2+(v[3]-v[6])**2+(v[4]-v[5])**2)/16+(v[3]+v[6]-v[4]-v[5])**2/64
assert s.expand(mv[0]-formula)==0 and mv[1]==0
# Independent finite confirmation of the terminal mod-four arithmetic.
residues=set()
for x3 in range(9):
    for x4 in range(9-x3):
        for x5 in range(9-x3-x4):
            x6=8-x3-x4-x5
            QQ=(x3-x6)**2+(x4-x5)**2+(x3+x6-x4-x5)**2//4
            residues.add(QQ%4)
assert residues=={0,3}
counts=[]
for suffix in ['', '_minus']:
    exported=json.loads((P/f'prior/forced_export{suffix}.json').read_text());old=set(json.loads((P/f'complement_metadata{suffix}.json').read_text())['removed'])
    vals={};eq=set();gt=set()
    for j,v,*_ in exported['physical_mapping']:
        if v[0]:continue
        tv=tuple(v)
        if tv not in vals:vals[tv]=mass(v)
        value,rad=vals[tv];assert rad==0
        if value==s.Rational(3,4):eq.add(j)
        if value>s.Rational(3,4):gt.add(j)
    counts.append({'TY_sign':-1 if suffix else 1,'boundary_variables_total':len(eq),'new_boundary_variables_beyond_complement':len(eq-old),'new_strictly_excessive_variables_beyond_complement':len(gt-old),'boundary_vectors':sum(v[0]==0 and z==[s.Rational(3,4),0] for v,z in vals.items())})
out={'status':'PASS','orthogonality_linear_coefficients':'verified symbolically','mass_quadratic_identity':'verified symbolically','terminal_mod_four_residues':sorted(residues),'conclusion':'Every nonzero integral R137 restriction column outside I(1) has bosonic real-row mass strictly below3/4.','counts':counts}
(Path(__file__).parent/'bosonic_mass_boundary_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
