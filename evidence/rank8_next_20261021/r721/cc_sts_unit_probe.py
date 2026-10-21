exec(open(__file__.replace('cc_sts_unit_probe.py','s_matrix_probe.py')).read().split('for sign in[1,-1]:')[0].replace("__file__.replace('s_matrix_probe.py','twist_sums_probe.py')","__file__.replace('cc_sts_unit_probe.py','twist_sums_probe.py')"))
r=s.sqrt(17);theta=21+5*r
conv=lambda x:sum(s.Rational(str(v))*theta**j for j,v in enumerate(reversed(x.to_list())))
Dc=conv(a['D']);Sc=s.Matrix(22,22,lambda i,j:conv(S0[i][j]));QA=QA;QC=s.zeros(22);e=[]
for u,v in w['C_matching']:
 q=s.zeros(22,1);q[rc['C_labels'][u]]=1;q[rc['C_labels'][v]]=-1;e.append(q)
x,y,z=s.symbols('x y z');unknown=(x*e[0]*e[0].T+y*(e[0]*e[1].T+e[1]*e[0].T)+z*e[1]*e[1].T)/2
for sign in[1,-1]:
 for z4 in[1,-1]:
  zz=1 if z4==1 else(1+s.I)/s.sqrt(2);tt=[1]*5+[-1]*4+[1]+[zz,-zz,s.I*zz,-s.I*zz]+[0]*8
  Sm=Sc+Dc*(-QA+sign*(va*vc.T+vc*va.T)+unknown)
  gauss=-(1+r)/2
  eq=[]
  for ai in [0]+rc['A_labels']:
   for cj in rc['C_labels']:
    L=sum(Sm[ai,k]*tt[k]*Sm[k,cj]for k in range(14))+Sc[ai,14]*Sc[14,cj]*gauss
    eq.append(s.expand(L-Dc/tt[ai]/tt[cj]*Sm[ai,cj]))
  sol=s.solve(eq,[x,y,z]);print('SIGN',sign,'z4',z4,'CC',sol)
