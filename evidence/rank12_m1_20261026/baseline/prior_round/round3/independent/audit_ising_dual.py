"""Independent full-Hom audit of Ising/dihedral twisted pullback bimodules.

Does not import the constructor or use its stabilizer-character projection.
"""
from pathlib import Path
from itertools import product
import json,time

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]

def need(condition,message):
    if not condition:raise ValueError(message)

def audit(row):
    par=row['parameters'];u=par['u'];gr=par['grading'];rot=par.get('rotation_cocycle',0);bits=par.get('abelian_cubes',[0,0,0]);q=par.get('modulus',8)
    E=list(product(range(8),range(2)))
    def gm(g,h):return ((g[0]+(u if g[1] else 1)*h[0])%8,(g[1]+h[1])%2)
    def formula_omega(g,h,k):
        a,b=g;c,d=h;e,f=k
        carry=(c+(-1)**d*e-(c+(-1)**d*e)%8)//8
        return (rot*a*(-1)**b*carry+4*(bits[0]*(a%2)*(c%2)*(e%2)+bits[1]*b*d*f+bits[2]*(a%2)*d*f))%q
    if 'source_omega' in row:
        ei={g:i for i,g in enumerate(E)};wt=row['source_omega']
        omega=lambda g,h,k:wt[ei[g]][ei[h]][ei[k]]
    else:
        need(q==8 and (rot==0 or u==7),'rotation formula modulus and inversion action')
        omega=formula_omega
    need(all((omega(h,k,l)-omega(gm(g,h),k,l)+omega(g,gm(h,k),l)-omega(g,h,gm(k,l))+omega(g,h,k))%q==0 for g,h,k,l in product(E,repeat=4)),'all 65536 source cocycle equations')
    need(all(omega(g,h,k)==0 for g,h,k in product(E,repeat=3) if (0,0) in (g,h,k)),'normalized cocycle')
    labs=[(a,g) for a in range(3) for g in E if int(a==2)==(g[0]*gr[0]+g[1]*gr[1])%2]
    need([[a,list(g)] for a,g in labs]==row['source_labels'],'actual matched-grading label list')
    def ising(a,b):return (0,1) if a==b==2 else (2,) if 2 in (a,b) else (a^b,)
    R=[[[int(c in ising(a,b) and gm(g,h)==k) for c,k in labs] for b,h in labs] for a,g in labs]
    need(R==row['source_tensor'],'independently reconstructed source fusion rules')
    n=len(R);c=next(i for i,(a,g) in enumerate(labs) if [a,list(g)]==par['algebra_generator'])
    invs=[i for i,(a,g) in enumerate(labs) if a!=2]
    def mul(a,b):
        need(a in invs or b in invs,'unique source product required')
        return next(k for k,v in enumerate(R[a][b]) if v)
    def F(a,b,c,k):
        aa,bb,cc,kk=[labs[x][0] for x in (a,b,c,k)];s=omega(labs[a][1],labs[b][1],labs[c][1])
        if aa==cc==2 and bb!=2:return (s+(q//2)*bb*kk)%q
        if aa!=2 and bb==2 and cc!=2:return (s+(q//2)*aa*cc)%q
        need((aa,bb,cc)!=(2,2,2),'three-odd matrix associator is never used')
        return s
    need(c in invs and mul(c,c)==0 and F(c,c,c,c)==0,'actual regular C2 algebra')
    O=[]
    for o in row['bimodules']:
        D=o['D'];lp={int(k):v for k,v in o['L'].items()};rp={int(k):v for k,v in o['R'].items()}
        need(set(D)=={o['z'],mul(c,o['z']),mul(o['z'],c),mul(mul(c,o['z']),c)},'full bimodule support orbit')
        for x in D:
            need((lp[x]+lp[mul(c,x)]+F(c,c,x,x))%q==0,'source left axiom')
            need((rp[x]+rp[mul(x,c)]-F(x,c,c,x))%q==0,'source right axiom')
            need((lp[x]+rp[mul(c,x)]-rp[x]-lp[mul(x,c)]-F(c,x,c,mul(mul(c,x),c)))%q==0,'source mixed axiom')
        O.append(dict(S=D,L={x:(mul(c,x),lp[x]) for x in D},R={x:(mul(x,c),rp[x]) for x in D},grade=lambda x:x))
    def hom(A,B):
        remaining={(a,b) for a,b in product(A['S'],B['S']) if A['grade'](a)==B['grade'](b)};answer=0
        while remaining:
            root=min(remaining);ph={root:0};queue=[root];consistent=True
            for a,b in queue:
                for typ in ('L','R'):
                    x,e=A[typ][a];y,f=B[typ][b];v=(ph[a,b]+f-e)%q
                    need(A['grade'](x)==B['grade'](y),'Hom actions preserve matching grade')
                    if (x,y) in ph:
                        if ph[x,y]!=v:consistent=False
                    else:ph[x,y]=v;queue.append((x,y))
            remaining-=set(queue);answer+=int(consistent)
        return answer
    for i,A in enumerate(O):
        for j,B in enumerate(O):need(hom(A,B)==int(i==j),'pairwise simple and inequivalent')
    dimsq=lambda A:len(A['S'])**2*(2 if labs[A['S'][0]][0]==2 else 1)//4
    need(sum(dimsq(A) for A in O)==32,'all simples exhausted by global dimension')
    T=[[[0]*len(O) for _ in O] for _ in O];balanced=0
    for i,A in enumerate(O):
        for j,B in enumerate(O):
            raw={(x,y,k) for x,y in product(A['S'],B['S']) for k,v in enumerate(R[x][y]) if v};remaining=set(raw);reduce={}
            while remaining:
                root=min(remaining);reduce[root]=(root,0);queue=[root]
                for x,y,k in queue:
                    root0,ph=reduce[x,y,k];xx,e=A['R'][x];yy=mul(c,y);zz,f=B['L'][yy]
                    need(zz==y,'C2 inverse left action')
                    nxt=(xx,yy,k);value=(ph+F(x,c,yy,k)+f-e)%q
                    if nxt in reduce:need(reduce[nxt]==(root0,value),'all balanced relation cycles')
                    else:reduce[nxt]=(root0,value);queue.append(nxt)
                need(len(queue)==2,'free balanced quotient orbit');remaining-=set(queue)
            S=sorted({r for r,e in reduce.values()});balanced+=len(S);L={};RR={}
            for x,y,k in S:
                xx,e=A['L'][x];kk=mul(c,k);root,f=reduce[xx,y,kk];L[x,y,k]=(root,(e-F(c,x,y,kk)+f)%q)
                yy,e=B['R'][y];kk=mul(k,c);root,f=reduce[x,yy,kk];RR[x,y,k]=(root,(e+F(x,y,c,kk)+f)%q)
            P=dict(S=S,L=L,R=RR,grade=lambda z:z[2])
            for k,C in enumerate(O):T[i][j][k]=hom(C,P)
    need(T==row['model_tensor'],'all independently reconstructed Hom dimensions')
    target=json.loads((HERE/'frozen/target_tensors.json').read_text())[row['id']];p=row['basis_map']
    need(sorted(p)==list(range(12)),'bijective based identification')
    need(all(target[a][b][c]==T[p[a]][p[b]][p[c]] for a,b,c in product(range(12),repeat=3)),'all 1728 input tensor coefficients')
    return dict(id=row['id'],status='PASS',cocycle_equations=16**4,source_module_axioms='all',independent_Hom_coefficients=12**3,balanced_basis_states=balanced,parameters=par)

if __name__=='__main__':
    t=time.monotonic();data=json.loads((HERE/'frozen/ising_twisted_dual_models.json').read_text());out=[]
    for row in data['models']:
        record=audit(row);out.append(record);print(record,flush=True)
    (HERE/'ising_twisted_dual_independent.json').write_text(json.dumps(dict(status='PASS',records=out,seconds=time.monotonic()-t),indent=2)+'\n')
