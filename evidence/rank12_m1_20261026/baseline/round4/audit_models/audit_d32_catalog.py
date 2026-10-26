"""Full independent Hom recomputation of the categorically complete D32 list."""
from itertools import product
import json,sys,time
from audit_liptrap import HERE,FIRST,need
from generic_c2_hom import audit as hom_audit
sys.path.insert(0,str(HERE.parent/'d32'))
import exhaustive_catalog as cat

def equiv_hom(N,sigma,parity):
    seen=set();objects=[];n=len(N)
    for a in range(n):
        if a in seen:continue
        O=sorted({a,sigma[a]});seen.update(O)
        for sign in range(2 if len(O)==1 else 1):
            U={x:(sigma[x],(parity[x]+2*sign)%4 if len(O)==1 else 0) for x in O}
            objects.append(dict(O=O,U=U))
    T=[[[0]*len(objects) for _ in objects] for _ in objects]
    for i,A in enumerate(objects):
        for j,B in enumerate(objects):
            for k,C in enumerate(objects):
                remaining={(a,b,c) for a,b,c in product(A['O'],B['O'],C['O']) if N[a][b][c]};dim=0
                while remaining:
                    root=min(remaining);queue=[root];phase={root:0};good=True
                    for a,b,c in queue:
                        aa,x=A['U'][a];bb,y=B['U'][b];cc,z=C['U'][c];nxt=(aa,bb,cc);v=(phase[a,b,c]+x+y-z)%4
                        need(N[aa][bb][cc]==1,'equivariant Hom support')
                        if nxt in phase:
                            if phase[nxt]!=v:good=False
                        else:phase[nxt]=v;queue.append(nxt)
                    remaining-=set(queue);dim+=int(good)
                T[i][j][k]=dim
    return T

def main():
    start=time.monotonic();receipt=json.loads((HERE.parent/'d32/exhaustive_catalog.json').read_text());targets=json.loads((FIRST/'tensors.json').read_text());refs={r['u']:r for r in json.loads((HERE.parent/'d32/models.json').read_text())};cache={};out=[]
    for record in receipt['records']:
        rid=record['id'];p=record['basis_map_source_to_model']
        need(cat.D[rid]==targets[rid],'actual frozen input')
        if record['branch']=='generalized_Ising':
            u=record['u'];ns=record['nonsplit'];key=(u,ns)
            if key not in cache:
                if ns:
                    r=refs[u];R=r['source_tensor'];degree=[tuple(x) for x in r['source_degrees']];F0,_,_=cat.lip.reconstruct(R,r['liptrap_certificate']);cs=[r['source_labels'].index(['g',0,1,a]) for a in (0,1)];S=set(r['liptrap_certificate']['serfs'])
                else:
                    R,degree,F0,cs=cat.split(u);S={i for i in range(len(R)) if R[i][next(j for j in range(len(R)) if R[i][j][0])]==[1]+[0]*(len(R)-1)}
                cache[key]=(R,degree,F0,cs,S)
            R,degree,F0,cs,S=cache[key];c=cs[record['inverse_lift_sign']];fix=F0(c,c,c,c)
            need(fix==record['subgroup_correction'],'exact algebra restriction correction')
            def F(a,b,d,k):
                g,h,j=[degree[x] for x in (a,b,d)]
                return (F0(a,b,d,k)+fix*g[1]*h[1]*j[1]+record['rotation']*cat.group_omega(u,g,h,j)+8*record['mixed']*(g[0]%2)*h[1]*j[1])%16
            M,info=cat.bimodule.construct(R,F,c,q=16)
            row=dict(id=rid,bimodules=info['objects'],model_tensor=M,basis_map=p)
            checked=hom_audit(row,R,F,c,16,S,targets[rid]);out.append(dict(parameters=record,status=checked['status'],independent_full_Hom_coefficients=1728))
        else:
            orders=record['orders'];els,G=cat.group(orders);N=[[[0]*9 for _ in range(9)] for _ in range(9)]
            for a,b in product(range(8),repeat=2):N[a][b][G[a][b]]=1
            for a in range(8):N[a][8][8]=N[8][a][8]=N[8][8][a]=1
            sigma=record['automorphism']+[8];parity=[0]*8+[record['parity']];B=record['invariant_bicharacter']
            need(all(B[sigma[a]][sigma[b]]==B[a][b] for a,b in product(range(8),repeat=2)),'strict actual TY tensor action')
            M=equiv_hom(N,sigma,parity)
            need(p[0]==0 and sorted(p)==list(range(12)),'unital permutation')
            need(all(targets[rid][a][b][c]==M[p[a]][p[b]][p[c]] for a,b,c in product(range(12),repeat=3)),'all independent equivariant Hom coefficients')
            out.append(dict(parameters=record,status='PASS',independent_full_Hom_coefficients=1728))
    need(len(out)==142,'all142categorical parameters')
    result=dict(status='PASS',generalized_Ising_parameters=96,TY_parameters=46,total_categories=142,coefficients_each=1728,records=out,seconds=time.monotonic()-start)
    (HERE/'d32_catalog_independent.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='records'})

if __name__=='__main__':main()
