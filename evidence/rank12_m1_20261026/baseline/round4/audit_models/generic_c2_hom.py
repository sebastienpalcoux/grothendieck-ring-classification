"""Previously independent full-Hom C2 audit, generalized to any feudal source.
No constructor import or character projection.
"""
from itertools import product
from audit_liptrap import need

def audit(row,R,F,c,q,serfs,target):
    def mul(a,b):
        need(a in serfs or b in serfs,'single fusion product')
        return R[a][b].index(1)
    need(c in serfs and mul(c,c)==0 and F(c,c,c,c)==0,'actual regular C2 algebra')
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
    dimsq=lambda A:len(A['S'])**2*(1 if A['S'][0] in serfs else 2)//4
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
    p=row['basis_map'];need(p[0]==0,'unit preserved')
    need(sorted(p)==list(range(12)),'bijective based identification')
    need(all(target[a][b][c]==T[p[a]][p[b]][p[c]] for a,b,c in product(range(12),repeat=3)),'all 1728 input tensor coefficients')
    return dict(id=row['id'],status='PASS',cocycle_equations=16**4,source_module_axioms='all',independent_Hom_coefficients=12**3,balanced_basis_states=balanced,phase_modulus=q)

