from rotation_probe import *
from cyclotomic_stabilizer_trace import integral_charpoly
from gram_vectors_general import native
from induction import low_failure
from higher_traces import indicator_choices

def base_system(R,data,cols,ep,objects):
 C=data['C'];ds=data['dims'];D=data['DD'];types=data['phases'];n=len(R);L=s.Matrix.hstack(*map(s.Matrix,cols));G=(data['ch'].C-L*L.T).extract(range(1,n),range(1,n));vectors=[]
 for v in native(G):
  z=sum((data['K'](v[i])*data['ds'][i+1] for i in range(n-1)),data['K'].zero)
  if not z or integral_charpoly(data['D']/z,data['K']) is None:continue
  co=integral_charpoly(z,data['K']);degree=len(co)-1;norm=abs(co[-1])
  if any(co[j]**degree%norm**j for j in range(1,degree+1)):continue
  vectors.append(tuple(v))
 labels=[(v,ti) for v in vectors for ti in range(len(types))];nh=len(labels);zv={v:sum((C(v[i])*ds[i+1] for i in range(n-1)),C.zero) for v in vectors};low=[sum((C(sum(c[i]*c[j] for c in cols))*ds[j] for j in range(n)),C.zero) for i in range(n)];A=[];b=[]
 def add(co,rhs):
  for row,val in rational_rows(co,rhs,C):A.append(row);b.append(val)
 for i in range(n-1):
  for j in range(i,n-1):add([C(v[i]*v[j]) for v,ti in labels],C(int(G[i,j])))
 for obj in range(1,n):
  for power,target in [(1,0),(2,ep[obj-1])]:add([C(v[obj-1])*zv[v]*types[ti][power-1] for v,ti in labels],C(target)*D-low[obj])
 rt=rotation_types(data['F'],3,(1,))
 for obj in range(1,n):
  H=sum(R[obj][obj][k]*R[k][obj][0] for k in range(n));forced=obj in objects;nv=len(A[0]);nn=len(rt)
  for row in A:row.extend([0]*nn)
  co=[C(v[obj-1])*zv[v]*types[ti][2] for v,ti in labels]+[C.zero]*(nv-nh)+[(D if forced else -D)*tt[0] for tt in rt];add(co,-low[obj]);add([C.zero]*nv+[C.one]*nn,C(H)/C(2 if forced else 1))
 return A,b,labels

if __name__=='__main__':
 rid=sys.argv[1];height=3;R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==rid);m.R=R;start=time.monotonic();data=__import__('round3_m4').data_for(R,height,60 if rid=='R6_6_1035' else None);print('data',rid,time.monotonic()-start,'F',data['F'],'types',len(data['phases']),'lows',len(data['lows']),flush=True);tab=table_for(R,data);mod=forced_module_data(R);objects=mod['objects'] if mod else [];out=[]
 for ix,cols in enumerate(data['lows']):
  why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
  if why:continue
  for ep in indicator_choices(R):
   for lab in tab.assignments(cols):
    A,b,labels=base_system(R,data,cols,ep,objects);A,b,meta=stronger_system(data,tab,cols,lab,A,b,labels);A,b,n=coupled(data,tab,cols,A,b,labels);A,b,labels,base=verlinde(R,data,tab,cols,lab,A,b,labels)
    C=data['C'];F=data['F'];allowed={j for j,ty in enumerate(data['phases']) if ty in {tuple(C.unit**((F//12)*a*k%F) for k in range(1,4)) for a in range(12)}}
    keep=[j for j in range(len(A[0])) if j>=len(labels) or not labels[j][0][3] or labels[j][1] in allowed];A=[[row[j] for j in keep] for row in A]
    print('startlp',rid,ix,ep,lab,len(A),len(A[0]),flush=True);aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)));sol=linprog(np.zeros(len(A[0])),A_eq=aa/scale[:,None],b_eq=bb/scale,bounds=(0,None),options={'time_limit':120},method='highs');print('lp',sol.status,sol.message,flush=True)
    out.append(dict(id=rid,low=ix,ep=ep,lab=lab,status=sol.status));Path(__file__).with_name(rid+'_higher.json').write_text(json.dumps(out,indent=2))
    if sol.status==0:sys.exit()
