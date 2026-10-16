#!/usr/bin/env python3
"""Exact all-phase induction masses for R6_8_1660; necessary conditions only."""
from pathlib import Path
from fractions import Fraction as Q
import argparse,json
from all_indicators import C,need

def derive(raw):
 z=C([0,1]);q2=z**6+z**42;q3=z**4+z**44;q6=q2*q3;d=3+2*q2+2*q3+q6;D=4*(1+d*d)
 basis=[C(1),q2,q3,q6]
 def coords(x):
  a=[[v.a[i]for v in basis]+[x.a[i]]for i in range(16)];row=0
  for col in range(4):
   k=next(i for i in range(row,16)if a[i][col]);a[row],a[k]=a[k],a[row];c=a[row][col];a[row]=[v/c for v in a[row]]
   for j in range(16):
    if j!=row:
     c=a[j][col];a[j]=[v-c*w for v,w in zip(a[j],a[row])]
   row+=1
  need(all(not any(a[j])for j in range(row,16)),'mass outside the dimension field')
  return [a[i][-1]for i in range(4)]
 outs=[]
 for case in raw['cases']:
  if not case['cyclic_dimension_three_compatible']:continue
  nu=[]
  for n in range(1,49):
   vals=case['moments_ascending_zeta48_coefficients'][str(n)]
   g=C(int(n%2==0));sig=C(0)if n%2 else q2*(z**((9*n)%48)+z**((-9*n)%48))/2
   nu.append([C(1),g,C(vals['X']),C(vals['X']),sig,C(vals['T'])])
  need(nu[-1]==[C(1),C(1),d,d,q2,q2*d],'48th indicators equal dimensions')
  allmasses=[];masses=[]
  for k in range(48):
   v=[sum(nu[n-1][i]*z**((-k*n)%48)for n in range(1,49))*D/48 for i in range(6)]
   allmasses.append(v)
   if any(x!=0 for x in v):masses.append({'phase':k,'masses_K':[[str(q)for q in coords(x)]for x in v],'masses_over_d_K':[[str(q)for q in coords(x*(d-6-4*q2))]for x in v]})
  for n in range(1,49):
   for i in range(6):need(sum(allmasses[k][i]*z**((k*n)%48)for k in range(48))==D*nu[n-1][i],'inverse Fourier transform')
  expected={0,8,9,12,14,15,20,24,26,30,32,33,36,39,42,44}
  if case['chi3_pair']==[36,5]:expected={(-k)%48 for k in expected}
  need({m['phase']for m in masses}==expected,'full twist support')
  outs.append({'chi3_pair':case['chi3_pair'],'chi6_pair':case['chi6_pair'],'masses':masses})
 return {'status':'PASS','basis':['1','sqrt2','sqrt3','sqrt6'],'cases':outs,'scope':'Exact Fourier masses for two necessary conjugate choices; no categorification or exclusion claimed.'}

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--input',type=Path,default=Path(__file__).with_name('all_indicators.json'));ap.add_argument('--output',type=Path);args=ap.parse_args()
 out=derive(json.loads(args.input.read_text()));text=json.dumps(out,indent=2)+'\n'
 if args.output:args.output.write_text(text)
 print(json.dumps({'status':out['status'],'conjugate_cases':len(out['cases']),'phase_masses_per_case':288}))
if __name__=='__main__':main()
