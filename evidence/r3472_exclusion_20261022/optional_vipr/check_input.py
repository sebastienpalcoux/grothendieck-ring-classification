import json,hashlib,re
from fractions import Fraction as Q
from pathlib import Path
if not __debug__:
    raise RuntimeError('Proof input verification requires assertions enabled.')
P=Path(__file__).resolve().parents[1];R=P/'optional_vipr'
p=json.loads((P/'terminal/models.json').read_text())['field'];p['rows']=[dict(r)for r in p['rows']]
bounds=json.loads((P/'terminal/certified_all_bounds.json').read_text())['bounds'];n=len(bounds)
assert n==572 and len(p['rows'])==628
mode=None;integer=False;integer_cols=set();rows={};rhs={};bd={};rtypes={}
for line in (R/'frozen_field.mps').read_text().splitlines():
 t=line.split()
 if not t:continue
 if t[0]=='NAME':continue
 if t[0]in ['ROWS','COLUMNS','RHS','BOUNDS','ENDATA']:mode=t[0];continue
 if mode=='ROWS':rtypes[t[1]]=t[0]
 elif mode=='COLUMNS':
  if len(t)>1 and t[1]=="'MARKER'":integer=t[2]=="'INTORG'";continue
  j=int(t[0][1:]);
  if integer:integer_cols.add(j)
  for k in range(1,len(t),2):
   if t[k]=='OBJ':assert Q(t[k+1])==0;continue
   i=int(t[k][1:]);a=Q(t[k+1]);rows.setdefault(i,{})[j]=rows.setdefault(i,{}).get(j,Q(0))+a
 elif mode=='RHS':
  for k in range(1,len(t),2):rhs[int(t[k][1:])]=Q(t[k+1])
 elif mode=='BOUNDS':
  typ,_,name,value=t;j=int(name[1:]);assert typ in ['LI','UI'];bd[j,typ]=Q(value)
assert integer_cols==set(range(n));assert {i for i in range(628)if rtypes.get('R'+str(i))=='E'}==set(range(628))
for i,(row,b)in enumerate(zip(p['rows'],p['rhs'])):assert {j:a for j,a in rows.get(i,{}).items()if a}==row and rhs.get(i,0)==b,('MPS row',i)
for j,(l,u)in enumerate(bounds):assert bd[j,'LI']==l and bd[j,'UI']==u,('MPS bound',j)
lines=(R/'frozen_field_complete.vipr').read_text().splitlines();i=1;assert lines[i].split()==['VAR',str(n)];names=[lines[i+1+j].strip()for j in range(n)];mapping={j:int(name.removeprefix('t_X'))for j,name in enumerate(names)};assert set(mapping.values())==set(range(n));i+=1+n;assert lines[i].split()==['INT',str(n)];assert {int(lines[i+1+j])for j in range(n)}==set(range(n));i+=1+n;assert lines[i].split()==['OBJ','min']and lines[i+1].strip()=='0';i+=2;assert lines[i].split()==['CON','1772','1144'];i+=1
vrows=[]
for line in lines[i:i+1772]:
 t=line.split();name,sense,b,count=t[:4];count=int(count);assert len(t)==4+2*count;row={mapping[int(t[4+2*k])]:Q(t[5+2*k])for k in range(count)};assert len(row)==count;vrows.append((sense,Q(b),row))
for j,(row,b)in enumerate(zip(p['rows'],p['rhs'])):assert vrows[j]==('E',Q(b),row),('VIPR row',j)
expected=set()
for j,(l,u)in enumerate(bounds):expected.add(('G',Q(l),((j,Q(1)),)));expected.add(('L',Q(u),((j,Q(1)),)))
actual={(s,b,tuple(sorted(row.items())))for s,b,row in vrows[628:]};assert actual==expected and len(actual)==1144
receipt={'status':'PASS','model_rows':628,'variables':572,'integer_variables':572,'bound_constraints':1144,'mps_sha256':hashlib.sha256((R/'frozen_field.mps').read_bytes()).hexdigest(),'vipr_sha256':hashlib.sha256((R/'frozen_field_complete.vipr').read_bytes()).hexdigest(),'scope':'Exact MPS and VIPR CON input identity only; no DER proof audit here.'}
assert receipt==json.loads((R/'input_verification.json').read_text());print(json.dumps(receipt,indent=2))
