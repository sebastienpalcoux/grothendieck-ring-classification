#!/usr/bin/env python3
"""Reusable exact signed table arithmetic; every loop is coefficient bounded."""
import itertools
import sympy as s

def equations(p):
 a,b,c,d,e,f,g,h,i,j=p
 return (a*d-b*b+b*g+c*h-d*d-e*e+1,a*e-b*c+b*h+c*i-d*e-e*f,b*e-c*d+d*h-e*g+e*i-f*h,a*f+b*i-c*c+c*j-e*e-f*f+1,b*f-c*e+d*i-e*h+e*j-f*i,d*f-e*e+g*i-h*h+h*j-i*i+1)

def signed_tables(N,positive):
 dom=[tuple(range(-n,n+1,2)) for n in N]
 for k in positive:dom[k]=tuple(v for v in dom[k] if v>0)
 A,B,C,D,E,F,G,H,I,J=dom
 out=[];outer=completed=0
 for a,b,c,d,e,f in itertools.product(A,B,C,D,E,F):
  if b:
   for i in I:
    outer+=1
    hh=e*(d+f-a)+b*c-c*i
    if hh%b:continue
    h=hh//b
    if h not in H:continue
    gg=b*b+d*d+e*e-a*d-c*h-1
    if gg%b:continue
    g=gg//b
    if g not in G:continue
    jj=c*c+e*e+f*f-a*f-b*i-1
    if c:
     if jj%c:continue
     js=(jj//c,)
     if js[0] not in J:continue
    else:
     if jj:continue
     js=J
    for j in js:
     completed+=1
     p=(a,b,c,d,e,f,g,h,i,j)
     if not any(equations(p)):out.append(p)
  elif c:
   outer+=1
   hh=d*d+e*e-a*d-1
   ii=e*(d+f-a)
   jj=c*c+e*e+f*f-a*f-1
   if hh%c or ii%c or jj%c:continue
   h,i,j=hh//c,ii//c,jj//c
   if h not in H or i not in I or j not in J:continue
   gg=h*(d-f)+e*i-c*d
   if e:
    if gg%e:continue
    gs=(gg//e,)
    if gs[0] not in G:continue
   else:
    if gg:continue
    gs=G
   for g in gs:
    completed+=1
    p=(a,b,c,d,e,f,g,h,i,j)
    if not any(equations(p)):out.append(p)
  else:
   raise ValueError('Cannot eliminate b=c=0; choose gauges/ranges so one is nonzero.')
 return out,outer,completed

def matrices(p):
 a,b,c,d,e,f,g,h,i,j=p
 return [s.eye(4),s.Matrix([[0,1,0,0],[1,a,b,c],[0,b,d,e],[0,c,e,f]]),s.Matrix([[0,0,1,0],[0,b,d,e],[1,d,g,h],[0,e,h,i]]),s.Matrix([[0,0,0,1],[0,c,e,f],[0,e,h,i],[1,f,i,j]])]

def analyse(solutions,norms):
 q=s.symbols('q');report=[]
 for p in solutions:
  M=matrices(p)
  assert all(x*y==y*x for x in M for y in M)
  Q=sum((x*x for x in M),s.zeros(4))
  fac=s.factor_list(Q.charpoly(q).as_poly())[1]
  possible=[]
  for po,mult in fac:
   degree=po.degree();norm=abs(int(po.TC()))
   if all(norm**e%n**degree==0 for e,n in norms):possible.append(str(po.as_expr()))
  report.append({'tuple':p,'codegree_polynomial':str(s.factor(Q.charpoly(q).as_expr())),'norm_survivors':possible})
 return report
