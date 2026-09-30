from pathlib import Path
import fitz,json,itertools,hashlib
P=Path(__file__).parent;source=P.parent/'r629/1001.5416.pdf';page=fitz.open(source)[19];nodes={}
for block in page.get_text('dict')['blocks']:
 if block['type']:continue
 for line in block['lines']:
  for s in line['spans']:
   x0,y0,x1,y1=s['bbox']
   if 350<y0<450 and x1<300 and s['text'].strip().isdigit():nodes[int(s['text'])]=((x0+x1)/2,(y0+y1)/2)

if len(nodes)!=12:raise RuntimeError("wrong graph vertex count")

def near(pt):
 d,k=min((((pt.x-v[0])**2+(pt.y-v[1])**2)**.5,k)for k,v in nodes.items())
 if d>=4:raise RuntimeError(f'graph endpoint not at vertex: {pt}, {d}, {k}')
 return k
mats={c:[[0]*12 for _ in range(12)]for c in ['brown','blue']};edges=[]
for dr in page.get_drawings():
 if dr['rect'].x1>300 or dr['rect'].y0<350 or dr['rect'].y1>450:continue
 c=dr['color'];key='blue'if c==(0.,0.,1.)else 'brown'if c and abs(c[0]-.6)<1e-6 and abs(c[1]-.4)<1e-6 else None
 if key is None:continue
 items=dr['items'];i=near(items[0][1]);j=near(items[-1][-1]);mats[key][i-1][j-1]+=1
 if i!=j:mats[key][j-1][i-1]+=1
 edges.append([key,i,j,len(items)])
B=mats['brown'];comp={0}
while True:
 nxt=comp|{j for i in comp for j,n in enumerate(B[i])if n}
 if nxt==comp:break
 comp=nxt
print('component',sorted(i+1 for i in comp));N=next(r['N']for r in json.load(open(P.parent/'data/model_input_tensors.json'))if r['id']=='R6_4_22');matches=[]
for perm in itertools.permutations(sorted(comp-{0})):
 order=[0]+list(perm)
 if [[B[i][j]for j in order]for i in order]==N[4]:matches.append([i+1 for i in order])
print('exact matches N4',matches);print('commute',all(sum(mats['blue'][i][k]*B[k][j]for k in range(12))==sum(B[i][k]*mats['blue'][k][j]for k in range(12))for i in range(12)for j in range(12)))
json.dump(dict(source='https://arxiv.org/pdf/1001.5416',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),page=20,figure='11(a)',nodes=nodes,edges=edges,matrices=mats,component=sorted(i+1 for i in comp),matches_to_N4=matches),open(P/'b2_7_graph_extraction.json','w'),indent=2)
