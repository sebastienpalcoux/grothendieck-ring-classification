"""Independent source, actual-algebra, and full-Hom audit of R419/R530.

All source data frozen locally. The seven scalar recouplings are Liptrap
Lemma5.4; every Fourier block is independently checked by audit_liptrap.
"""
from itertools import product
from functools import lru_cache
import json,time
from audit_liptrap import HERE,FIRST,need,audit as liptrap
from generic_c2_hom import audit as hom_audit

def scalar_recouplings(R,c):
    q=c['modulus'];S=set(c['serfs']);M=c['lords'];n=len(R)
    dual=[next(b for b in range(n) if R[a][b][0]) for a in range(n)]
    mul={(a,b):R[a][b].index(1) for a,b in product(range(n),repeat=2) if a in S or b in S}
    p={tuple(v[:-1]):v[-1] for v in c['phase_values']}
    nu=lambda a,b,m:p.get(('upsilon',a,b,m),0)
    chi=lambda a,b,m:p.get(('chi',a,b,m),0)
    tau=lambda m:p.get(('tau',m),0)
    @lru_cache(None)
    def alpha(a,b,d):
        values={(nu(a,b,m)+nu(mul[a,b],d,m)-nu(a,mul[b,d],m)-nu(b,d,mul[dual[a],m]))%q for m in M}
        need(len(values)==1,'pointed associator independent of chosen lord');return next(iter(values))
    @lru_cache(None)
    def F(a,b,d,k):
        if a in S and b in S and d in S:return alpha(a,b,d)
        if a in S and b in S:return nu(a,b,k)%q
        if a in S and d in S:return chi(a,d,k)%q
        if b in S and d in S:return -nu(b,d,dual[a])%q
        if a in S:return (alpha(dual[k],a,mul[dual[a],k])-nu(dual[k],a,mul[mul[dual[k],a],b]))%q
        if b in S:return (nu(k,dual[k],a)-nu(k,dual[k],mul[a,b])+chi(k,b,mul[a,b]))%q
        if d in S:return (nu(d,dual[k],dual[b])+tau(mul[b,d])-tau(b)-alpha(d,dual[k],k)-alpha(mul[d,dual[k]],mul[k,dual[d]],d))%q
        raise ValueError('three-lord matrix block is not used by subgroup bimodules')
    return F

def main():
    start=time.monotonic();frozen=HERE/'d32_nonsplit_frozen';rows=json.loads((frozen/'models.json').read_text());targets=json.loads((FIRST/'tensors.json').read_text());sd=json.loads((frozen/'cocycle_SD16_mod16.json').read_text());E=list(product(range(8),range(2)));ei={x:i for i,x in enumerate(E)};out=[]
    for row in rows:
        R=row['source_tensor'];cert=row['liptrap_certificate'];q=row['phase_modulus'];u=row['u'];degree=[tuple(x) for x in row['source_degrees']];labs=row['source_labels'];F0=scalar_recouplings(R,cert)
        source=liptrap(R,cert);need(source['serfs']==16 and source['lords']==8 and source['stabilizer_order']==2,'actual generalized Ising source')
        need(q in (16,32) and cert['modulus']==16,'phase field embedding')
        li={tuple(x):i for i,x in enumerate(labs)}
        for a,b in product(cert['serfs'],repeat=2):
            _,r,s,h=labs[a];_,rr,ss,hh=labs[b]
            expected=('g',(r+(-1)**s*rr)%4,s^ss,(h+hh+s*rr)%2)
            need(R[a][b][li[expected]]==1,'actual nonsplit central extension of D8')
        gm=lambda x,y:((x[0]+(u if x[1] else 1)*y[0])%8,x[1]^y[1])
        need(all(gm(gm(a,b),c)==gm(a,gm(b,c)) for a,b,c in product(E,repeat=3)),'actual universal grading group')
        need(degree==[(2*x[1],x[2]) if x[0]=='g' else (x[1],x[2]) for x in labs],'recorded degree labels')
        need(all(degree[c]==gm(degree[a],degree[b]) for a,b,c in product(range(len(R)),repeat=3) if R[a][b][c]),'all homogeneous fusion channels')
        def rot(g,h,k):
            if u==3:return sd[ei[g]][ei[h]][ei[k]]
            a,b=g;c,d=h;e,f=k;t=c+(-1)**d*e
            return 2*a*(-1)**b*((t-t%8)//8)%16
        fix=row['subgroup_correction'];c=row['subgroup_generator']
        need(fix==F0(c,c,c,c) and fix in (0,8),'restriction correction copied from actual source')
        def w(g,h,k):return (fix*g[1]*h[1]*k[1]+row['rotation_twist']*rot(g,h,k)+8*row['mixed_twist']*(g[0]%2)*h[1]*k[1])%16
        need(all(w(g,h,k)==0 for g,h,k in product(E,repeat=3) if (0,0) in (g,h,k)),'normalized unitary twisting cocycle')
        need(all((w(h,k,l)-w(gm(g,h),k,l)+w(g,gm(h,k),l)-w(g,h,gm(k,l))+w(g,h,k))%16==0 for g,h,k,l in product(E,repeat=4)),'all65536twisting cocycle equations')
        F=lambda a,b,d,k:(q//16)*(F0(a,b,d,k)+w(degree[a],degree[b],degree[d]))%q
        ans=hom_audit(row,R,F,c,q,set(cert['serfs']),targets[row['id']]);ans['source']=source;ans['u']=u;ans['rotation_twist']=row['rotation_twist'];out.append(ans);print(ans,flush=True)
    result=dict(status='PASS',records=out,new_models=[r['id'] for r in out if r['id'] in ('R12_1_419','R12_1_530')],scope='Existence only; no completeness of all generalized Ising sources inferred',seconds=time.monotonic()-start)
    (HERE/'d32_nonsplit_independent.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
