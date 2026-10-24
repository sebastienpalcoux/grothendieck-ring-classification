from center import *
sys.path.insert(0,str(ROOT/'phase3/quadratic_s_symmetry'))
from quadratic_s_symmetry import characters

def build(R,height=3,duality=True):
 data=base(R);a=chars(R);DD=data['D'];cs=characters(a,2,DD)
 for c in cs:c['degree']=1
 val=[(Q(a.N[i].trace()-a.A[i].trace(),4),Q(0))for i in range(9)]
 cs.append({'values':val,'codegree':(Q(4),Q(0)),'dimension':qc.div(DD,(Q(4),Q(0)),2),'degree':2})
 # On a central class v this normalized degree-two trace is its scalar eigenvalue.
 assert val[0]==(1,0)
 prev=qc.base;qc.base=lambda _:data
 try:A,b,meta=qc.system(R,height)
 finally:qc.base=prev
 types,_=qc.trace_types(2,[2,3],height);choose=[];labels=[];keys=[];j=0
 for v,z in data['cols']:
  if v[0]:
   for h,c in enumerate(cs):
    if z==c['dimension']and v[0]==c['degree']and(not duality or all(v[i]==v[a.du[i]]for i in range(9))):choose.append(j);labels.append((h,v));keys.append(('label',v,h))
   if z==(Q(9),Q(6)):
    choose.append(j);labels.append((None,None));keys.append(('anon',v,0))
   j+=1
  else:
   for ti in range(len(types)):choose.append(j);labels.append((None,None));keys.append(('high',v,ti));j+=1
 for k in range(j,len(A[0])):choose.append(k);labels.append((None,None));keys.append(('extra',(),k))
 AA=[[row[k]for k in choose]for row in A];bb=list(b)
 if duality:
  index={key:j for j,key in enumerate(keys)};groups=[];seen=set()
  for j,(kind,v,ti)in enumerate(keys):
   if j in seen:continue
   if kind in('high','anon'):
    k=index.get((kind,tuple(v[a.du[i]]for i in range(9)),ti))
    if k is None:seen.add(j);continue
    group=sorted({j,k})
   else:group=[j]
   seen.update(group);groups.append(group)
  AA=[[sum(row[k]for k in g)for g in groups]for row in AA];labels=[labels[g[0]]for g in groups]
 if not duality:groups=[[j]for j in range(len(keys))]
 extras=[]
 for h in range(len(cs)):AA.append([int(k==h)for k,v in labels]);bb.append(1);extras.append(['label_count',h])
 for h in range(len(cs)):
  for k in range(h):
   rows=[[],[]]
   for lab,v in labels:
    value=(Q(0),Q(0))
    if lab in(h,k):
     other=k if lab==h else h
     ev=tuple(sum(v[i]*cs[other]['values'][i][c]for i in range(9))for c in range(2))
     value=mul(cs[other]['dimension'],ev,2)
     if lab==h:value=qc.scale(value,-1)
    for c in range(2):rows[c].append(value[c])
   for c,row in enumerate(rows):
    if any(row):
     den=math.lcm(*(x.denominator for x in row));ints=[int(x*den)for x in row];g=math.gcd(*ints);AA.append([x//g for x in ints]);bb.append(0);extras.append(['Ssym',h,k,c])
 # The two omitted characters have values ±i sqrt(2) on the large simples,
 # value1 on invertibles and -2 on b8. Sum their S-symmetry equations.
 realpart=[1,0,0,0,0,1,1,1,-2];dimcomplex=(Q(9),Q(6))
 for h,ch in enumerate(cs):
  rows=[[],[]]
  for group in groups:
   value=(Q(0),Q(0))
   for j in group:
    kind,v,ti=keys[j]
    if kind=='anon':
     ev=tuple(sum(v[i]*ch['values'][i][c]for i in range(9))for c in range(2))
     value=qc.add(value,mul(ch['dimension'],ev,2))
    elif kind=='label'and ti==h:
     value=qc.add(value,qc.scale(dimcomplex,-2*sum(v[i]*realpart[i]for i in range(9))))
   for c in range(2):rows[c].append(value[c])
  for c,row in enumerate(rows):
   if any(row):
    den=math.lcm(*(x.denominator for x in row));ints=[int(x*den)for x in row];g=math.gcd(*ints);AA.append([x//g for x in ints]);bb.append(0);extras.append(['Ssym_complex_pair_sum',h,c])
 meta['labels']=[{'degree':c['degree'],'dimension':list(map(str,c['dimension'])),'values':[[str(x),str(y)]for x,y in c['values']]}for c in cs];meta['duality']=duality;meta['extra_rows']=extras;meta['variables']=len(AA[0])
 gv=(0,0,0,0,0,1,0,0,0)
 meta['singleton_g_variables']=[{'index':col,'packet':keys[group[0]][2],'trace_values':[[str(x),str(y)]for x,y in types[keys[group[0]][2]]]}for col,group in enumerate(groups)if keys[group[0]][0]=='high'and keys[group[0]][1]==gv]
 return AA,bb,meta

if __name__=='__main__':
 height=int(sys.argv[1])if len(sys.argv)>1 else 3;start=time.monotonic();R=qc.inputs('R9_2_1975');A,b,meta=build(R,height)
 print('SYMMETRY',len(A),len(A[0]),flush=True);ray,why=qc.exact_separator(A,b,timeout=90)
 out={'id':'R9_2_1975','outcome':'candidate_exclusion'if ray else'no_conclusion','ray':ray,'metadata':meta,'solver_report':why,'seconds':time.monotonic()-start}
 if ray:assert qc.verify_ray(A,b,ray);out['bTy']=sum(x*y for x,y in zip(b,ray))
 Path(__file__).with_name('symmetry_h'+str(height)+'.json').write_text(json.dumps(out,indent=2)+'\n');print(out['outcome'],out.get('bTy'),out['seconds'],flush=True)
