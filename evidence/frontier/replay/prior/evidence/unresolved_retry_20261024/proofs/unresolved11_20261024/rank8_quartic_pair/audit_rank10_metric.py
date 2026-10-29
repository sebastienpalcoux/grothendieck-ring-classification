#!/usr/bin/env python3
"""Independent exact metric-C5 modular-data audit in SymPy's number field.

This is a necessary modular-data check, never a categorical realization.
"""
from pathlib import Path
import hashlib,itertools,json
import sympy as s
from sympy import QQ
HERE=Path(__file__).resolve().parent
x=s.symbols('x')
K=QQ.algebraic_field((s.Poly(x**4+x**3+x**2+x+1,x),s.exp(2*s.pi*s.I/5)))
z=K.unit;zero=K.zero;one=K.one
rt=one+2*(z+z**4);d=2+rt;dp=2-rt
def need(condition,message):
    if not condition:raise ValueError(message)
def conjugate(a):
    result=zero
    for coefficient in a.to_list():result=result*z**4+coefficient
    return result
def encode(a):return [str(v) for v in a.to_list()]
def multiply(A,B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))),zero) for j in range(len(B[0]))] for i in range(len(A))]
def build(q=1,c=2):
    # Labels: 1,U,B1..B4,C1..C4,Y,P1,P2,X.
    params=[(0,d),(0,dp)]+[(ell,(-one-rt)/2) for ell in range(1,5)]+[(ell,(-one+rt)/2) for ell in range(1,5)]
    dimensions=[one,d*d]+[one+d]*4+[one+3*d]*4+[d,2*d,2*d,5*d]
    restrictions=[(0,0,0,0,0),(0,1,1,1,1)]
    restrictions += [tuple(int(i==c*ell%5) for i in range(5)) for ell in range(1,5)]
    restrictions += [tuple(int(i not in (0,c*ell%5)) for i in range(5)) for ell in range(1,5)]
    pure=[(1,0,0,0,0),(0,1,0,0,1),(0,0,1,1,0),(1,1,1,1,1)]
    S=[[zero for _ in range(14)] for _ in range(14)]
    for i,(ell,w) in enumerate(params):
        for j,v in enumerate(restrictions):
            chi=one+w*sum((v[k]*z**(ell*k%5) for k in range(5)),zero)
            phase=z**(-ell*params[j][0]*pow(2*q,-1,5)%5)
            S[i][j]=dimensions[i]*chi*phase/(10*d)
        for j,v in enumerate(pure,10):
            chi=w*sum((v[k]*z**(ell*k%5) for k in range(5)),zero)
            S[i][j]=S[j][i]=dimensions[i]*chi/(10*d)
    block=[[-3*one/10,2*one/5,2*one/5,-one/2],
           [2*one/5,(3+rt)/10,(3-rt)/10,zero],
           [2*one/5,(3-rt)/10,(3+rt)/10,zero],
           [-one/2,zero,zero,one/2]]
    for i,j in itertools.product(range(4),repeat=2):S[i+10][j+10]=block[i][j]
    theta=[z**(-ell*ell*pow(4*q,-1,5)%5) for ell,w in params]
    theta += [one,z**(3*q%5),z**(-3*q%5),-one]
    return S,theta,dimensions,[0,1,5,4,3,2,9,8,7,6,10,11,12,13]
def run():
    S,T,dims,dual=build()
    need(all(S[i][j]==S[j][i] for i,j in itertools.product(range(14),repeat=2)),'S symmetric')
    need(all(S[0][i]==dims[i]/(10*d) for i in range(14)),'positive first row')
    need(sum((a*a for a in dims),zero)==100*d*d,'global dimension')
    need(sum((a*a*t for a,t in zip(dims,T)),zero)==10*d,'central charge +1')
    S2=multiply(S,S)
    need(all(S2[i][j]==(one if dual[i]==j else zero) for i,j in itertools.product(range(14),repeat=2)),'S squared equals duality')
    need(all(conjugate(S[i][j])==S[dual[i]][j] for i,j in itertools.product(range(14),repeat=2)),'conjugation equals duality')
    STS=multiply([[S[i][j]*T[j] for j in range(14)] for i in range(14)],S)
    correct=[[conjugate(T[i])*conjugate(S[i][j])*conjugate(T[j]) for j in range(14)] for i in range(14)]
    need(STS==correct,'positive-monodromy STS identity with conjugated S')
    wrong=conjugate(T[2])*S[2][2]*conjugate(T[2])
    need(STS[2][2]!=wrong,'old convention error reproduced')
    fusion=[]
    for i in range(14):
        row=[]
        for j in range(14):
            product=[]
            for k in range(14):
                coefficient=sum((S[i][ell]*S[j][ell]*conjugate(S[k][ell])/S[0][ell] for ell in range(14)),zero)
                values=coefficient.to_list();need(len(values)<=1,'rational Verlinde coefficient')
                value=values[0] if values else QQ.zero
                need(value.denominator==1 and value>=0,'nonnegative integral Verlinde coefficient')
                product.append(int(value))
            row.append(product)
        fusion.append(row)
    need(all(fusion[0][i][j]==int(i==j) for i,j in itertools.product(range(14),repeat=2)),'fusion unit')
    need(all(fusion[i][j][0]==int(j==dual[i]) for i,j in itertools.product(range(14),repeat=2)),'fusion duality')
    lamX=[one,-one]+[zero]*8+[-one,zero,zero,one]
    lamY=[one,-one]+[-2*one]*4+[2*one]*4+[-3*one,4*one,4*one,-5*one]
    need([S[13][j]/S[13][0] for j in range(14)]==lamX,'formal-codegree-four row')
    need([S[10][j]/S[10][0] for j in range(14)]==lamY,'formal-codegree-one-hundred row')
    Sbar,Tbar,dimsbar,dualbar=build(4,3)
    need(Sbar==[[conjugate(a) for a in row] for row in S] and Tbar==[conjugate(a) for a in T],'second presentation is complex conjugate')
    out={'status':'PASS','q':1,'c':2,'rank':14,'field':'Q(zeta_5)','positive_monodromy_convention':True,'correct_identity':'S theta S = theta^-1 conjugate(S) theta^-1','old_STS_error_at_2_2_descending_Qzeta5_coefficients':encode(STS[2][2]-wrong),'S_squared_charge_conjugation':True,'multiplicative_central_charge':1,'all_2744_Verlinde_coefficients_nonnegative_integers':True,'maximum_fusion_multiplicity':max(v for row in fusion for product in row for v in product),'fusion_tensor_sha256':hashlib.sha256(json.dumps(fusion,separators=(',',':')).encode()).hexdigest(),'other_surviving_q_c':[4,3],'second_is_complex_conjugate':True,'scope':'Necessary modular data only. No fusion-category associators, center realization, or source categorification have been established.'}
    (HERE/'audit_rank10_metric_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)
if __name__=='__main__':run()
