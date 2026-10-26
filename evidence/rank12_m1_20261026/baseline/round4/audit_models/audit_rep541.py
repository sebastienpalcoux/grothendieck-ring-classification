"""Fresh character-inner-product proof of the ordinary R541 model."""
from itertools import product
from functools import lru_cache
import json,time
from audit_liptrap import HERE,FIRST,SECOND,need

@lru_cache(None)
def reduce24(exponents):
    a=[0]*24
    for e in exponents:a[e%24]+=1
    # Phi24(x)=x^8-x^4+1.
    for i in range(23,7,-1):
        a[i-4]+=a[i];a[i-8]-=a[i];a[i]=0
    return tuple(a[:8])

def main():
    start=time.monotonic();G=list(product(range(3),range(8)))
    mul=lambda x,y:((x[0]+(-1)**x[1]*y[0])%3,(x[1]+y[1])%8)
    need(all(mul(mul(a,b),c)==mul(a,mul(b,c)) for a,b,c in product(G,repeat=3)),'actual finite semidirect group')
    # Eight linear characters, and four representations induced from C3xC4.
    chars=[]
    for k in range(8):chars.append({(a,b):(3*k*b%24,) for a,b in G})
    for j in range(4):chars.append({(a,b):() if b%2 else ((3*j*b+8*a)%24,(3*j*b-8*a)%24) for a,b in G})
    need(sum(len(c[0,0])**2 for c in chars)==24,'complete dimension sum')
    for i,j in product(range(12),repeat=2):
        v=[0]*8
        for g in G:
            w=reduce24(tuple(a-b for a,b in product(chars[i][g],chars[j][g])))
            v=[a+b for a,b in zip(v,w)]
        need(v==[24*int(i==j)]+[0]*7,'complete irreducible orthogonality')
    T=[[[0]*12 for _ in chars] for _ in chars]
    for i,j,k in product(range(12),repeat=3):
        v=[0]*8
        for g in G:
            w=reduce24(tuple(a+b-c for a,b,c in product(chars[i][g],chars[j][g],chars[k][g])))
            v=[a+b for a,b in zip(v,w)]
        need(v[1:]==[0]*7 and v[0]>=0 and v[0]%24==0,'integer exact character multiplicity')
        T[i][j][k]=v[0]//24
    witness=json.loads((SECOND/'audit_models/rep_C3rtimesC8.json').read_text())[0]
    need(T==witness['model_tensor'],'independent tensor from ordinary characters')
    source=json.loads((FIRST/'tensors.json').read_text())[witness['id']];p=witness['basis_map_source_to_model']
    need(p[0]==0 and sorted(p)==list(range(12)),'unital permutation')
    need(all(source[a][b][c]==T[p[a]][p[b]][p[c]] for a,b,c in product(range(12),repeat=3)),'all1728coefficients')
    out=dict(status='PASS',id=witness['id'],group='C3 semidirect C8 by inversion',exact_character_inner_products=1728,complete_irreducible_orthogonality=True,seconds=time.monotonic()-start)
    (HERE/'rep541_reaudit.json').write_text(json.dumps(out,indent=2)+'\n');print(out)

if __name__=='__main__':main()
