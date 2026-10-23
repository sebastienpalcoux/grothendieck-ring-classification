"""Independent tensor receipts and replay of the less standard constructions.

The mathematical construction audit is recorded in THEORY.md. This checker
does not claim to solve pentagons for standard cited categories.
"""
import collections, gzip, hashlib, itertools, json, sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'work/models'))
from match_models import ty,prod
from cyclic_equivariant import cyclic_equivariant
from extra_models import crossed

def require(c,msg):
    if not c: raise ValueError(msg)

def main():
    tensors={}
    for n in (9,10):
        with gzip.open(BASE/f'inputs/rank{n}_M1_verified/FusionRingMultiplicationTables.txt.gz','rt') as f:
            for i,s in enumerate(f,1):
                if s.strip(): tensors[f'R{n}_1_{i}']=json.loads(s.replace('{','[').replace('}',']'))
    files=list((BASE/'work/models').glob('known_models*.json'))+list((BASE/'work/root_models').glob('*models.json'))
    seen=set();records=collections.defaultdict(list);kinds=collections.Counter();replayed=collections.Counter()
    for path in files:
        for rec in json.load(open(path)):
            S=tensors[rec['id']];n=len(S)
            require(hashlib.sha256(json.dumps(S,separators=(',',':')).encode()).hexdigest()==rec['tensor_sha256'],'source hash')
            for model in rec['models']:
                key=(rec['id'],json.dumps(model,sort_keys=True))
                if key in seen:continue
                seen.add(key);T=model['model_tensor'];p=model['basis_map_source_to_model'];kind=model['constructor'];par=model['parameters']
                require(len(T)==n and sorted(p)==list(range(n)) and p[0]==0,'unital basis bijection')
                require(all(S[i][j][k]==T[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(n),repeat=3)),'all tensor coefficients')
                kinds[kind]+=1;records[rec['id']].append(model)
                if kind=='associative_C2_zest':
                    R=par['base_tensor'];g=par['grading'];h=par['central_invertible']
                    require(g[0]==g[h]==0 and set(g)=={0,1},'C2 grading')
                    require(sum(R[h][h])==1 and R[h][h][0]==1,'involution')
                    action=[]
                    for i in range(n):
                        require(R[h][i]==R[i][h] and sum(R[h][i])==1,'central invertible')
                        action.append(R[h][i].index(1))
                    for i,j,k in itertools.product(range(n),repeat=3):
                        require(not R[i][j][k] or g[k]==(g[i]^g[j]),'homogeneous product')
                        require(T[i][j][action[k] if g[i]*g[j] else k]==R[i][j][k],'zested product')
                    replayed[kind]+=1
                elif kind=='central_extension_quotient':
                    R=par['base_tensor'];d=par['grading'];h=par['central_boson'];p0,q,r=(par[k]for k in ('p','q','r'));G=par['central_extension_group_table']
                    require(R==[[[int(abs(a-b)<=c<=min(a+b,8-a-b) and (a+b+c)%2==0) for c in range(5)]for b in range(5)]for a in range(5)],'SU2 level4 base')
                    require(d==[0,1,0,1,0] and h==4,'boson and grading')
                    require(all(G[G[a][b]][c]==G[a][G[b][c]]for a,b,c in itertools.product(range(8),repeat=3)),'extension associativity')
                    for i,j,k in itertools.product(range(10),repeat=3):
                        x,e=divmod(i,2);y,f=divmod(j,2);z,t=divmod(k,2)
                        shift=(p0*d[x]*d[y]+q*e*f+r*e*d[y])%2
                        require(T[i][j][k]==R[x][y][4-z if shift else z]*int(t==(e^f)),'quotient coefficients')
                    replayed[kind]+=1
                elif kind in ('ty_cyclic_equivariant','ty_cyclic_equivariant_twisted'):
                    R=ty(tuple(par['orders']));require(R==par['base_tensor'],'TY tensor')
                    a=len(R)-1;s=par['automorphism'];m=par['group_order']
                    require(len(par['orders'])==1 and s[a]==a,'cyclic TY')
                    require(all((s[i]*s[j]-i*j)%a==0 for i,j in itertools.product(range(a),repeat=2)),'orthogonal bicharacter automorphism')
                    parity=par.get('parity',[0]*len(R))
                    require(all(parity[i]==0 for i in range(a)) and parity[a]in(0,1),'parity character')
                    out,_=cyclic_equivariant(R,s,m,parity)
                    require(out==T,'equivariant fusion coefficients');replayed[kind]+=1
                elif kind=='ising_swap_c4_subextension':
                    R=prod(ty((2,)),ty((2,)));s=[3*(i%3)+i//3 for i in range(9)]
                    require(R==par['base_tensor'] and s==par['swap'],'canonical swap')
                    C=crossed(R,s);L=par['selected_labels']
                    require(len(L)==9 and L[0]==0,'selected labels')
                    require(all(not C[i][j][k] or k in L for i in L for j in L for k in range(18)),'fusion subcategory closure')
                    require(T==[[[C[i][j][k]for k in L]for j in L]for i in L],'subextension tensor');replayed[kind]+=1
    # Favor concise established models; omit redundant conditional descriptions.
    priority=['pointed','pointed_dihedral','rep_dihedral','rep_dicyclic','su2','ty','deligne_product','deligne_product_registry','odd_metaplectic','permutation_equivariant','pointed_equivariant','ty_crossed','ty_cyclic_equivariant','ty_cyclic_equivariant_twisted','graded_pullback','ising_swap_c4_subextension','group_theoretical_general','group_theoretical','untwisted_group_theoretical','central_extension_quotient','associative_C2_zest','half_even_metaplectic','twisted_c2_bimodules']
    selected=[]
    for rid,models in sorted(records.items(),key=lambda kv:tuple(map(int,kv[0].replace('R','').split('_')))):
        m=min(models,key=lambda m:priority.index(m['constructor']))
        selected.append({'id':rid,'status':'unitarily_realized','model':m})
    (HERE/'selected_models.json').write_text(json.dumps(selected,indent=2)+'\n')
    report={'status':'PASS','distinct_input_models':len(records),'unique_model_receipts':len(seen),'constructors':dict(kinds),'nonstandard_recipe_replays':dict(replayed),'note':'79 tensor-model inputs; add HI C5 and four additional Liptrap-positive inputs for the 84-case baseline.'}
    (HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
