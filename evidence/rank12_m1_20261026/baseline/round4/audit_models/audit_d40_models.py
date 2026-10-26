"""Fresh full-Hom verification of the two Liptrap C2 Morita models."""
from pathlib import Path
from itertools import product
import json,sys,time
from audit_liptrap import audit as check_source,need,FIRST,SECOND,HERE

sys.path.insert(0,str(SECOND/'family_graded'))
# Used only to obtain representative module actions; all module equations and
# all tensor multiplicities below are independently checked.
from feudal_dual import construct,reconstruct

def verify_model(rid,model):
    par=model['parameters'];R=par['feudal_tensor'];cert=par['feudal_certificate'];c=par['subgroup_generator']
    check_source(R,cert)
    F0,mul,dual=reconstruct(R,cert)
    twist=par.get('grading_twist')
    if twist:
        U=twist['grading_group_table'];degree=twist['grading'];omega=twist['cocycle']
        need(all(U[0][a]==U[a][0]==a for a in range(len(U))),'grading group unit')
        need(all(U[U[a][b]][d]==U[a][U[b][d]] for a,b,d in product(range(len(U)),repeat=3)),'grading group associativity')
        need(all(degree[k]==U[degree[a]][degree[b]] for a,b,k in product(range(len(R)),repeat=3) if R[a][b][k]),'actual categorical grading')
        need(all((omega[b][d][e]-omega[U[a][b]][d][e]+omega[a][U[b][d]][e]-omega[a][b][U[d][e]]+omega[a][b][d])%4==0 for a,b,d,e in product(range(len(U)),repeat=4)),'all grading cocycle equations')
        need(all(omega[a][b][d]==0 for a,b,d in product(range(len(U)),repeat=3) if 0 in (a,b,d)),'normalized grading cocycle')
        q=20 if all(v%2==0 for A in omega for row in A for v in row) else 40
        F=lambda a,b,d,k:((q//5)*F0(a,b,d,k)+(q//4)*omega[degree[a]][degree[b]][degree[d]])%q
    else:q=10;F=lambda a,b,d,k:2*F0(a,b,d,k)%q
    need(cert['modulus']==5,'actual source phase embedding')
    need(mul[c,c]==0 and F(c,c,c,c)==0,'actual separable C2 algebra')
    original,info=construct(R,cert,c,twist=twist)
    need(original==model['model_tensor'],'stored constructor tensor')
    O=[]
    for o in info['objects']:
        D=o['D'];L=o['L'];RR=o['R']
        need(set(D)=={o['z'],mul[c,o['z']],mul[o['z'],c],mul[mul[c,o['z']],c]},'full orbit support')
        for x in D:
            need((L[x]+L[mul[c,x]]+F(c,c,x,x))%q==0,'left module associativity')
            need((RR[x]+RR[mul[x,c]]-F(x,c,c,x))%q==0,'right module associativity')
            need((L[x]+RR[mul[c,x]]-RR[x]-L[mul[x,c]]-F(c,x,c,mul[mul[c,x],c]))%q==0,'commuting bimodule actions')
        O.append(dict(S=D,L={x:(mul[c,x],L[x]) for x in D},R={x:(mul[x,c],RR[x]) for x in D},grade=lambda x:x))
    def hom(A,B):
        remaining={(a,b) for a,b in product(A['S'],B['S']) if A['grade'](a)==B['grade'](b)};answer=0
        while remaining:
            root=min(remaining);ph={root:0};queue=[root];consistent=True
            for a,b in queue:
                for typ in ('L','R'):
                    x,e=A[typ][a];y,f=B[typ][b];v=(ph[a,b]+f-e)%q
                    need(A['grade'](x)==B['grade'](y),'intertwiner same grade')
                    if (x,y) in ph:
                        if ph[x,y]!=v:consistent=False
                    else:ph[x,y]=v;queue.append((x,y))
            remaining-=set(queue);answer+=int(consistent)
        return answer
    for i,A in enumerate(O):
        for j,B in enumerate(O):need(hom(A,B)==int(i==j),'simple pairwise inequivalent modules')
    S=set(cert['serfs'])
    need(sum(len(A['S'])**2*(1 if A['S'][0] in S else 5)//4 for A in O)==40,'simple object completeness by dimension')
    T=[[[0]*12 for _ in O] for _ in O]
    for i,A in enumerate(O):
        for j,B in enumerate(O):
            raw={(x,y,k) for x,y in product(A['S'],B['S']) for k,v in enumerate(R[x][y]) if v};remaining=set(raw);reduction={}
            while remaining:
                root=min(remaining);reduction[root]=(root,0);queue=[root]
                for x,y,k in queue:
                    r,ph=reduction[x,y,k];xx,e=A['R'][x];yy=mul[c,y];z,f=B['L'][yy]
                    need(z==y,'inverse algebra action');nxt=(xx,yy,k);value=(ph+F(x,c,yy,k)+f-e)%q
                    if nxt in reduction:need(reduction[nxt]==(r,value),'balanced holonomy')
                    else:reduction[nxt]=(r,value);queue.append(nxt)
                need(len(queue)==2,'free balancing action');remaining-=set(queue)
            reps=sorted({r for r,e in reduction.values()});L={};RR={}
            for x,y,k in reps:
                xx,e=A['L'][x];kk=mul[c,k];r,f=reduction[xx,y,kk];L[x,y,k]=(r,(e-F(c,x,y,kk)+f)%q)
                yy,e=B['R'][y];kk=mul[k,c];r,f=reduction[x,yy,kk];RR[x,y,k]=(r,(e+F(x,y,c,kk)+f)%q)
            P=dict(S=reps,L=L,R=RR,grade=lambda z:z[2])
            for k,C in enumerate(O):T[i][j][k]=hom(C,P)
    need(T==model['model_tensor'],'independent full-Hom tensor')
    p=model['basis_map_source_to_model'];N=json.loads((FIRST/'tensors.json').read_text())[rid]
    need(p[0]==0 and sorted(p)==list(range(12)),'unital based bijection')
    need(all(N[a][b][d]==T[p[a]][p[b]][p[d]] for a,b,d in product(range(12),repeat=3)),'all 1728 census coefficients')
    return dict(id=rid,status='PASS',source_rank=len(R),source_phase_modulus=cert['modulus'],bimodule_phase_modulus=q,independent_Hom_coefficients=1728,actual_algebra=True,actual_associator=True)

if __name__=='__main__':
    start=time.monotonic();records=[]
    r=json.loads((SECOND/'family_graded/feudal_dual_results.json').read_text())[0];records.append(verify_model(r['id'],r['models'][0]));print(records[-1],flush=True)
    r=next(r for r in json.loads((SECOND/'family_graded/feudal_twist_results.json').read_text()) if r['id']=='R12_1_263');records.append(verify_model(r['id'],r['models'][0]));print(records[-1],flush=True)
    (HERE/'d40_model_reaudit.json').write_text(json.dumps(dict(status='PASS',records=records,seconds=time.monotonic()-start),indent=2)+'\n')
