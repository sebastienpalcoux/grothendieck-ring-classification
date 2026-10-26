"""Independent monomial-equivariance reconstruction of R449."""
from itertools import product
import json,time
from audit_liptrap import need,HERE,FIRST,SECOND

def main():
    start=time.monotonic();row=json.loads((SECOND/'family_graded/c4_model.json').read_text());model=row['models'][0];par=model['parameters']
    sigma=par['automorphism'];parity=par['parity'];labs=par['labels'];n=6
    need(sigma==[0,4,3,2,1,5] and parity==[0,0,0,0,0,1],'orthogonal inversion and TY parity')
    def fusion(a,b,c):
        if a<5 and b<5:return int(c==(a+b)%5)
        if a==b==5:return int(c<5)
        return int(c==5)
    need(all((sigma[a]*sigma[b]-a*b)%5==0 for a,b in product(range(5),repeat=2)),'preserved nondegenerate symmetric cyclic bicharacter')
    need(all((parity[a]+parity[b]-parity[c])%2==0 for a,b,c in product(range(n),repeat=3) if fusion(a,b,c)),'monoidal square coherence')
    need(all(((a+b)//4+((a+b)%4+c)//4-(b+c)//4-(a+(b+c)%4)//4)%2==0 for a,b,c in product(range(4),repeat=3)),'full C4 tensor-action carry coherence')
    expected=[];seen=set()
    for a in range(n):
        if a in seen:continue
        O=[a] if sigma[a]==a else [a,sigma[a]];seen.update(O)
        expected += [[O,j] for j in range(4//len(O))]
    need(labs==expected,'full orbit/stabilizer simple list')
    objects=[]
    for O,j in labs:
        d=len(O);U={a:(sigma[a],(2*j*d+parity[a]*d)%8 if k==d-1 else 0) for k,a in enumerate(O)}
        for a in O:
            x=a;ph=0
            for _ in range(4):x,e=U[x];ph+=e
            need(x==a and ph%8==4*parity[a],'fourth-power equivariance equals actual action coherence')
        objects.append(dict(O=O,U=U))
    T=[[[0]*12 for _ in objects] for _ in objects]
    for i,A in enumerate(objects):
        for j,B in enumerate(objects):
            for k,C in enumerate(objects):
                todo={(x,y,z) for x,y,z in product(A['O'],B['O'],C['O']) if fusion(x,y,z)};dimension=0
                while todo:
                    root=min(todo);queue=[root];ph={root:0};consistent=True
                    for x,y,z in queue:
                        xx,a=A['U'][x];yy,b=B['U'][y];zz,c=C['U'][z];nxt=(xx,yy,zz);v=(ph[x,y,z]+a+b-c)%8
                        need(fusion(xx,yy,zz)==1,'actual tensor functor on Hom channel')
                        if nxt in ph:
                            if ph[nxt]!=v:consistent=False
                        else:ph[nxt]=v;queue.append(nxt)
                    todo-=set(queue);dimension+=int(consistent)
                T[i][j][k]=dimension
    need(T==model['model_tensor'],'independent monomial intertwiner tensor')
    target=json.loads((FIRST/'tensors.json').read_text())['R12_1_449'];p=model['basis_map_source_to_model']
    need(p[0]==0 and sorted(p)==list(range(12)),'unital basis bijection')
    need(all(target[a][b][c]==T[p[a]][p[b]][p[c]] for a,b,c in product(range(12),repeat=3)),'all 1728 coefficients')
    out=dict(status='PASS',id='R12_1_449',actual_TY_orthogonal_action=True,actual_C4_carry_coherence=True,independent_monomial_Hom_coefficients=1728,seconds=time.monotonic()-start)
    (HERE/'c4_equivariant_reaudit.json').write_text(json.dumps(out,indent=2)+'\n');print(out)

if __name__=='__main__':main()
