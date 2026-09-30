"""Exact common assignment of restriction, word coefficients and twist traces.

All routines here construct necessary systems. A solution is not a category.
Balancing uses S_(a*,b) for the word A_a A_b; complex duality is retained.
"""
from modular_character_induction import rational_rows
from round5_unified import count_system

def build_coupled(R,data,cols,lab,A,b,labels,kept,integral,wd,domains):
 """labels precede oldaux; kept indexes ORIGINAL labels; A is fixedprofile.
 data contains C, dims, DD and tab, all in sameambientcyclotomicfield.
 Return sparseexactinteger rows asdicts, rhs, labels, integrality.
 """
 C=data['C'];tab=data['tab'];ph=data['phases'];ss=count_system(wd,domains)
 for v in cols:tab.prepare(v)
 byv={}
 for j,(v,x) in enumerate(ss['labels']):byv.setdefault(tuple(v[1:]),[]).append(j)
 new=[];old2new={};gram2new={};integ=[]
 for k,orig in enumerate(kept):
  old2new[k]=[]
  if orig<len(labels):
   v,ti=labels[orig]
   for q in byv[tuple(v)]:
    j=len(new);old2new[k].append(j);gram2new.setdefault(q,[]).append(j)
    new.append((q,ti));integ.append(1)
  else:
   old2new[k].append(len(new));new.append(('aux',orig));integ.append(integral[k])
 rows=[];rhs=list(b)
 for row in A:
  nr={}
  for k,z in enumerate(row):
   if z:
    for j in old2new[k]:nr[j]=int(z)
  rows.append(nr)
 for row,value in zip(ss['rows'],ss['rhs']):
  nr={}
  for q,z in row.items():
   for j in gram2new.get(int(q),[]):nr[j]=int(z)
  rows.append(nr);rhs.append(int(value))
 dims=[sum((C(v[i])*data['dims'][i] for i in range(len(R))),C.zero) for v in cols]
 for p,w in enumerate(wd['words']):
  if len(w)!=2:continue
  a,bb=w
  ast=wd['low_duality'][a]
  sab=dims[ast]*tab.values[lab[ast],tuple(cols[bb])]
  target=sab-sum((C(wd['low_coefficients'][p][c])*dims[c] for c in range(len(cols))),C.zero)
  co=[]
  for q,ti in new:
   if q=='aux':co.append(C.zero);continue
   v,x=ss['labels'][q];dv=sum((C(v[i])*data['dims'][i] for i in range(len(R))),C.zero)
   co.append(C(x[p])*dv*ph[ti][0])
  for row,val in rational_rows(co,target,C):rows.append({j:int(z) for j,z in enumerate(row)if z});rhs.append(int(val))
 return {'rows':rows,'rhs':rhs,'labels':new,'integrality':integ,'coefficient_labels':ss['labels']}

