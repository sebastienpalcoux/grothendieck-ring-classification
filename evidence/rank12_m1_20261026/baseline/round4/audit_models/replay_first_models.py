"""Fresh bounded replay of all first-round positive records, including lift licenses.

The prior constructor is reused for ordinary formulas. Category existence is a
separate reviewed premise; this script does not infer it from a tensor match.
"""
from pathlib import Path
from itertools import product
import collections, hashlib, json, sys, time
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
FIRST=HERE.parents[1]/'prior_round/prior_round/evidence/rank12-m1-offline-20261025'
sys.path.insert(0,str(FIRST))
import verify as old

def need(v,msg):
    if not v: raise ValueError(msg)

def inspect(kind,p):
    """Check the actual selected current lies in a reviewed lift family."""
    if kind=='deligne_product':
        name=p['left_name']
        choices={'Vec(C2)':old.mm.group((2,)),'Fib':old.mm.su2(3,True),
                 'Vec(C3)':old.mm.group((3,)),'Ising':old.mm.ty((2,)),
                 'Rep(S3)':old.mm.rep_dihedral(3),'PSU(2)_5':old.mm.su2(5,True)}
        need(name in choices and p['left_tensor']==choices[name],'actual named left factor')
    if kind=='graded_pullback':
        need(p['left_name']=='Ising' and p['left_tensor']==old.mm.ty((2,)),'actual Ising factor')
    if kind=='associative_C2_zest':
        k=p['base_constructor']; q=p['base_parameters'];h=p['central_invertible'];A=p['base_tensor']
        inspect(k,q)
        need(all(sum(A[h][i])==1 and A[h][i]==A[i][h] for i in range(len(A))),'invertible central underlying object')
        if k in ('pointed','dihedral_rep','odd_metaplectic','half_even_metaplectic'): return 'canonical braided lift'
        if k=='pointed_equivariant':
            G=q['group_table'];need(all(G[a][b]==G[b][a] for a,b in product(range(len(G)),repeat=2)),'symmetric pointed equivariant base')
            return 'strict braided pointed action'
        if k=='graded_pullback':
            need(q['labels'][h]==[1,0],'exact inherited Ising fermion')
            return 'restricted ambient Ising half-braiding'
        if k=='metaplectic_character_crossed_product':
            need(h==1,'canonical equivariance boson')
            return 'canonical Rep(C2) half-braiding preserved by character action'
        if k=='deligne_product':
            n=len(q['right_tensor']);rn=q['right_name']
            if h%n==0:return 'left-factor canonical half-braiding'
            # Explicitly licensed right factors. TY and pseudo-PSU are not
            # silently treated as braided; their currents must come from left.
            if n==4:
                need(rn not in ('TY(C3)','pseudo-PSU(2)_6'),'unbraided right factor current')
            elif n==6:
                need(('\\Rep(' in rn or rn.startswith('$PSU') or rn=='$SO(5)_2$' or rn.startswith('$\\Vec_{C_2}\\boxtimes\\mathrm{Ising}') or rn.startswith('$\\Vec_{C_2}\\boxtimes\\Rep') or rn.startswith('$\\Vec_{C_2}\\boxtimes PSU') or rn.startswith('$\\mathrm{Fib}\\boxtimes') or rn.startswith('$\\Vec_{C_2}\\boxtimes\\Vec')),'reviewed braided right factor')
            else:raise ValueError('unexpected factor rank')
            return 'product of actual braided-factor half-braidings'
        raise ValueError('unreviewed central lift '+k)
    return None

def main():
    start=time.monotonic();data=json.loads((FIRST/'tensors.json').read_text());counts=collections.Counter();rings=set();zests=[];bindings=[]
    for file in ('models','additional_models','group_models','twisted_c2_models'):
        for row in json.loads((FIRST/(file+'.json')).read_text()):
            rid=row['id'];R=data[rid];need(old.common.sha(R)==row['tensor_sha256'],'source hash')
            rings.add(rid)
            for m in row['models']:
                k=m['constructor'];p=m['parameters'];lift=inspect(k,p)
                M=old.rebuild(k,p);S=m['model_tensor'];b=m['basis_map_source_to_model']
                need(M==S or old.common.based_iso(M,S) is not None,'constructor to stored tensor')
                need(b[0]==0 and sorted(b)==list(range(12)),'unit preserving basis permutation')
                need(all(R[a][c][d]==S[b[a]][b[c]][b[d]] for a,c,d in product(range(12),repeat=3)),'all1728coefficients')
                counts[k]+=1;bindings.append(dict(id=rid,constructor=k,file=file,coefficients=1728))
                if lift:zests.append(dict(id=rid,base=p['base_name'],current=p['central_invertible'],lift=lift))
    ordinary=len(bindings)
    for row in json.loads((FIRST/'feudal.json').read_text())['records']:
        if row['model']:rings.add(row['id']);counts['liptrap_unitary_model']+=1
    need(ordinary==381 and sum(counts.values())==402 and len(rings)==127,'full first-round accounting')
    out=dict(status='PASS',ordinary_records=ordinary,liptrap_separately_reaudited=21,total_records=402,rings=127,constructor_counts=dict(counts),zest_lift_licenses=zests,bindings=bindings,seconds=time.monotonic()-start,optimized=not __debug__)
    (HERE/'first_model_reaudit.json').write_text(json.dumps(out,indent=2)+'\n')
    print({k:v for k,v in out.items() if k not in ('bindings','constructor_counts','zest_lift_licenses')})

if __name__=='__main__':main()
