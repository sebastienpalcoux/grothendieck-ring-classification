"""Exact matrix/quaternion identifications for the two periodic-cover arguments."""
from pathlib import Path
from fractions import Fraction as F
import json,itertools
HERE=Path(__file__).resolve().parent
rows=json.loads((HERE.parent/'d48/h8_pairs.json').read_text())
def need(x,m):
    if not x:raise ValueError(m)
def order(G,a):
    b=a;n=1
    while b:b=G[b][a];n+=1
    return n
def closure(G,gs):
    seen={0};stack=[0]
    while stack:
        x=stack.pop()
        for g in gs:
            y=G[x][g]
            if y not in seen:seen.add(y);stack.append(y)
    return seen
def iso(G,T):
    n=len(G);a,b=next((a,b) for a in range(1,n) for b in range(a+1,n) if len(closure(G,[a,b]))==n)
    for x in range(1,n):
        if order(T,x)!=order(G,a):continue
        for y in range(1,n):
            if order(T,y)!=order(G,b):continue
            p={0:0};stack=[0];bad=False
            while stack and not bad:
                u=stack.pop()
                for g,h in [(a,x),(b,y)]:
                    v=G[u][g];w=T[p[u]][h]
                    if v in p:
                        if p[v]!=w:bad=True;break
                    else:p[v]=w;stack.append(v)
            if not bad and len(set(p.values()))==n:
                need(all(p[G[i][j]]==T[p[i]][p[j]] for i,j in itertools.product(range(n),repeat=2)),'entire group table isomorphism')
                return [p[i] for i in range(n)]
    raise ValueError('group isomorphism absent')
# Exact arithmetic in Q(sqrt(2)), then Hamilton quaternions.
zero=(F(0),F(0));one=(F(1),F(0))
def add(x,y):return(x[0]+y[0],x[1]+y[1])
def neg(x):return(-x[0],-x[1])
def times(x,y):return(x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def qm(x,y):
    z=[zero]*4
    signs=[[1,1,1,1],[1,-1,1,-1],[1,-1,-1,1],[1,1,-1,-1]]
    # Index multiplication 1,i,j,k: xor indices, with these Hamilton signs.
    for i,j in itertools.product(range(4),repeat=2):
        v=times(x[i],y[j]);z[i^j]=add(z[i^j],v if signs[i][j]>0 else neg(v))
    return tuple(z)
unit=(one,zero,zero,zero);half=(F(1,2),F(0));root_half=(F(0),F(1,2))
gens=[(root_half,root_half,zero,zero),(half,half,half,half)]
qs=[unit];seen={unit}
for x in qs:
    for g in gens:
        y=qm(x,g)
        if y not in seen:seen.add(y);qs.append(y)
need(len(qs)==48,'binary octahedral quaternion group order')
need(all(sum((times(x,x)[0] for x in q),F())==1 and sum((times(x,x)[1] for x in q),F())==0 for q in qs),'all quaternion norms exactly one')
qi={q:i for i,q in enumerate(qs)};Q=[[qi[qm(a,b)] for b in qs] for a in qs]
G28=next(r['table'] for r in rows if r['smallgroup'][1]==28);p28=iso(G28,Q)
H28=next(r['subgroup'] for r in rows if r['smallgroup'][1]==28)
need(sorted(order(G28,h) for h in H28)==[1,2,4,4,4,4,4,4],'quaternion subgroup Q8')
vals=[(1,0,0,1)]+[v for v in itertools.product(range(3),repeat=4) if (v[0]*v[3]-v[1]*v[2])%3 and v!=(1,0,0,1)]
vi={v:i for i,v in enumerate(vals)}
def mm(x,y):
    a,b,c,d=x;e,f,g,h=y
    return((a*e+b*g)%3,(a*f+b*h)%3,(c*e+d*g)%3,(c*f+d*h)%3)
M=[[vi[mm(x,y)] for y in vals] for x in vals]
row29=next(r for r in rows if r['smallgroup'][1]==29);G29=row29['table'];p29=iso(G29,M)
N=[i for i in range(48) if (vals[p29[i]][0]*vals[p29[i]][3]-vals[p29[i]][1]*vals[p29[i]][2])%3==1]
def parity(p):return sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2
need(N==[i for i,p in enumerate(row29['projection_permutations']) if not parity(p)],'SL2 kernel agrees with S4 parity')
qT=[q for q in qs if all(not c[1] for c in q)]
need(len(qT)==24,'binary tetrahedral subgroup')
qti={q:i for i,q in enumerate(qT)};QT=[[qti[qm(a,b)] for b in qT] for a in qT]
ni={a:i for i,a in enumerate(N)};NT=[[ni[G29[a][b]] for b in N] for a in N]
pN=iso(NT,QT)
receipt={'status':'PASS','SmallGroup_48_28_to_unit_quaternions':p28,'SmallGroup_48_29_to_GL2_F3':p29,'SL2_F3_to_binary_tetrahedral':pN,'quaternion_coordinates':[[[str(a),str(b)] for a,b in q] for q in qs],'GL2_F3_matrices':vals,'SL2_source_indices':N,'all_group_table_coefficients_checked':True}
(HERE/'audit_d48_groups.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: exact binary-octahedral, GL2(3), and binary-tetrahedral full group isomorphisms')
