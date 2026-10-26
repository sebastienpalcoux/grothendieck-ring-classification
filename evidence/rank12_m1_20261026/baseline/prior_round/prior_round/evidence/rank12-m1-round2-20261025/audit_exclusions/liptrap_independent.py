"""Independent arbitrary-C* replay of the seven used Liptrap negatives.

Unknown chi, upsilon and normalized tau are formal Laurent variables. Every
reported contradiction is checked as a zero exponent vector over Z, not as a
failed finite phase search. No import of first-round setup or solver.
"""
from itertools import product
from collections import Counter
import json
from independent_audit import BASE,HERE,dual,require

def check(R,c):
    n=len(R);du=dual(R);S=[i for i in range(n)if sum(R[i][du[i]])==1];M=[i for i in range(n)if i not in S]
    mul=lambda a,b:R[a][b].index(1)
    require(S==c['serfs']and M==c['lords'],'serfs/lords binding')
    require(all(not R[m][q][z]for m,q,z in product(M,repeat=3)),'feudal parity')
    H=[a for a in S if mul(a,M[0])==M[0]];h=len(H)
    require(H==c['stabilizer']and all([a for a in S if mul(a,m)==m]==H==[a for a in S if mul(m,a)==m]for m in M),'common left/right stabilizer')
    require(all(mul(a,b)==mul(b,a)for a,b in product(H,repeat=2)),'abelian stabilizer')
    ix={a:i for i,a in enumerate(H)};G=[[ix[mul(a,b)]for b in H]for a in H]
    characters=[]
    for vals in product(range(h),repeat=h-1):
        v=(0,)+vals
        if all(v[G[a][b]]==(v[a]+v[b])%h for a,b in product(range(h),repeat=2)):characters.append(v)
    require(len(characters)==h,'complete finite group character list')
    forms=[]
    for rows in product(characters,repeat=h-1):
        F=((0,)*h,)+rows
        if len(set(F))!=h or any(F[a][b]!=F[b][a]for a,b in product(range(h),repeat=2)):continue
        if all(F[G[a][b]][z]==(F[a][z]+F[b][z])%h for a,b,z in product(range(h),repeat=3)):forms.append(F)
    require(len(forms)==c['bicharacter_count'],'all nondegenerate symmetric bicharacters')
    choices=list(product(range(len(forms)),repeat=len(M)))
    require(len(choices)==c['assignment_count'],'all bicharacter assignments')
    require(c.get('variable_tau')is True,'tau unrestricted at every lord')
    equations=[]
    def add(terms,right=None):
        row=Counter()
        for coeff,key in terms:
            if key[0]=='tau'or(key[1]!=0 and key[2]!=0):row[key]+=coeff
        row={k:v for k,v in row.items()if v}
        if row or right is not None:equations.append((row,right))
    for a,b,m in product(S,S,M):
        amb=mul(mul(a,m),b)
        add([(1,('chi',b,a,du[m])),(-1,('chi',a,b,amb)),(-1,('tau',amb)),(-1,('tau',m)),(1,('tau',mul(a,m))),(1,('tau',mul(m,b)))])
    for a,b,z,m in product(S,S,S,M):
        add([(1,('upsilon',a,b,m)),(-1,('upsilon',a,b,mul(m,du[z]))),(1,('chi',mul(a,b),z,m)),(-1,('chi',a,z,m)),(-1,('chi',b,z,mul(du[a],m)))])
    for m in M:add([(1,('tau',m)),(1,('tau',du[m]))])
    for im,m in enumerate(M):
        for ia,a in enumerate(H):
            for ib,b in enumerate(H):
                rhs=[F[ia][ib]for F in forms]
                if(a and b)or any(rhs):add([(1,('chi',a,b,m))],(im,ia,ib))
    require(sorted(r['assignment_index']for r in c['contradictions'])==list(range(len(choices))),'complete assignment coverage')
    for proof in c['contradictions']:
        total=Counter();rhs=0;assignment=choices[proof['assignment_index']]
        for index,coefficient in proof['row_combination']:
            require(type(index)is int and type(coefficient)is int and 0<=index<len(equations),'integer relation bounds')
            row,right=equations[index]
            for variable,power in row.items():total[variable]+=coefficient*power
            if right is not None:
                im,ia,ib=right;rhs+=coefficient*forms[assignment[im]][ia][ib]
        require(all(v==0 for v in total.values()),'all arbitrary complex variables cancel identically')
        require(rhs%h!=0 and rhs%h==proof['nonzero_rhs_mod_stabilizer_order'],'nontrivial root of unity remains')
    return dict(equations=len(equations),nondegenerate_bicharacters=len(forms),assignments=len(choices),arbitrary_complex_unknowns=True,variable_tau=True)

if __name__=='__main__':
    data=json.loads((BASE/'tensors.json').read_text());out=[]
    for r in json.loads((BASE/'feudal.json').read_text())['records']:
        if r['certificate']:out.append(dict(id=r['id'],**check(data[r['id']],r['certificate'])))
    sub=json.loads((BASE/'subrings.json').read_text())
    for r in json.loads((BASE/'lower_known.json').read_text())['class_proofs']:
        if r['certificate']['kind']=='liptrap_complex_obstruction':
            R=sub['classes'][r['class_index']]['tensor'];out.append(dict(id=r['known_source_id'],**check(R,r['certificate'])))
    receipt=dict(status='PASS',records=out)
    (HERE/'liptrap_independent.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
