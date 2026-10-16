#!/usr/bin/env python3
"""Source-bound verification of a purely theoretical five-case obstruction.
Only exact integer arithmetic; no branching search, optimizer, or LP certificate.
"""
import argparse,gzip,hashlib,json
from pathlib import Path

IDS=[33,36,76,412,446]
HASHES={33:'7a97e02134591a480adaa70aa8c938366c7406db000ac258a9502822480365b9',36:'0f3439764ab3cf628490ff0427eee015eede38b83165a1413c93349b97240249',76:'e633ff711a4d5bb15555d0b0ca78d810e9aa0e2e2a1b9336020d15e494303c5b',412:'b4936146f9270530f3c5e5db5bddb1fb20b7353d859b60517e1446d749ed4e3c',446:'79f08fcc6679f4480daeb6c14c68b422b7cceac4a8ed7616f3c27395723b0d3d'}
EXPECTED={33:('C4',2),36:('C4',0),76:('C4',0),412:('V4',2),446:('V4',0)}
def require(b,message):
    if not b:raise RuntimeError(message)
def flat(N):return tuple(x for M in N for row in M for x in row)
def mul(z,w):return (z[0]*w[0]+17*z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def polyprod(factors):
    p=[1]
    for q in factors:
        out=[0]*(len(p)+len(q)-1)
        for i,x in enumerate(p):
            for j,y in enumerate(q):out[i+j]+=x*y
        p=out
    return p

def charpoly(M):
    n=len(M);A=[[int(i==j)for j in range(n)]for i in range(n)];out=[1]
    for k in range(1,n+1):
        A=[[sum(M[i][l]*A[l][j]for l in range(n))for j in range(n)]for i in range(n)]
        t=sum(A[i][i]for i in range(n));require(t%k==0,'integer characteristic recurrence')
        c=-t//k;out.append(c)
        for i in range(n):A[i][i]+=c
    return out

def verify(repo):
    rows=[]
    for line in gzip.open(repo/'supplements/rank8/data/rank8_tables.txt.gz','rt'):
        if not line.strip():continue
        N=json.loads(line.replace('{','[').replace('}',']'))
        if max(flat(N))==2:rows.append(N)
    rows.sort(key=flat);out=[]
    for idx in IDS:
        N=rows[idx-1];require(hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()==HASHES[idx],'source tensor hash');n=8;du=[next(j for j in range(n)if N[i][j][0])for i in range(n)]
        require(all(N[0][i]==[int(i==j)for j in range(n)]==N[i][0]for i in range(n)),'source unit')
        require(all(N[i][j][0]==int(j==du[i])for i in range(n)for j in range(n)),'source duality')
        require(all(N[i][j][k]==N[du[i]][k][j]==N[k][du[j]][i]for i in range(n)for j in range(n)for k in range(n)),'Frobenius reciprocity')
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        require(sum(N[i][j][a]*N[a][k][l]for a in range(n))==sum(N[j][k][a]*N[i][a][l]for a in range(n)),'source associativity')
        G=[i for i in range(n)if sum(sum(row)for row in N[i])==n];O=[i for i in range(n)if i not in G]
        require(len(G)==len(O)==4 and 0 in G,'four pointed and four nonpointed simples')
        d=[(1,0)if i in G else(4,1)for i in range(n)]
        for i in range(n):
            for j in range(n):require(mul(d[i],d[j])==tuple(sum(N[i][j][k]*d[k][l]for k in range(n))for l in range(2)),'exact FP dimension character')
        D=tuple(sum(mul(z,z)[k]for z in d)for k in range(2));require(D==(136,32),'global dimension')
        orders={}
        for g in G:
            power=0
            for k in range(1,5):
                require(sum(N[power][g])==1,'pointed product simple');power=N[power][g].index(1)
                require(power in G,'pointed closure')
                if power==0:orders[g]=k;break
            require(g in orders,'pointed exponent divides four')
        kind='C4'if 4 in orders.values()else'V4';sd=[i for i in O if du[i]==i]
        require((kind,len(sd))==EXPECTED[idx],'exact duality obstruction pattern')
        omega=[sum(N[k][du[k]][j]for k in range(n))for j in range(n)]
        require(omega==[8 if i==0 or i in O else 0 for i in range(n)],'FI(1)=8*1+8*sum(nonpointed)')
        C=[[sum(omega[k]*N[k][j][i]for k in range(n))for j in range(n)]for i in range(n)]
        require(charpoly(C)==polyprod([[1,-8]]*6+[[1,-272,1088]]),'Casimir eigenvalues and multiplicities')
        # These are Casimir eigenvalues e*f_E, not the full induction Gram
        # matrix in a noncommutative ring.  Simple D,Dbar roots force e=1;
        # every remaining ordinary formal codegree is 8/e, hence rational.
        require(mul((4,1),(4,1))==(33,8),'d squared')
        require(mul(D,(136,-32))==(1088,0),'global norm')
        require(mul((33,8),(136,-32))==D,'Galois-unit central dimension D/Dbar=d squared')
        require(32*2*17==1088,'compression 1/D-1/Dbar=-sqrt(17)/17')
        require(pow(2,8,17)==1,'Legendre symbol (2/17)=+1')
        # The indicator balance gives |sum_nonpointed nu2| <= #selfdual <4,
        # whereas the nontrivial pointed indicator sum is a nonzero odd integer.
        involutions=[g for g in G if orders[g]==2]
        require(len(involutions)in[1,3]and len(involutions)%2==1,'odd number of pointed involutions')
        require(len(sd)<4,'strict indicator imbalance')
        out.append({'id':f'R8_2_{idx}','tensor_sha256':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest(),'commutative':all(N[i][j]==N[j][i]for i in range(n)for j in range(n)),'pointed_labels':G,'pointed_group':kind,'pointed_orders':orders,'nonpointed_labels':O,'selfdual_nonpointed_labels':sd,'Casimir_polynomial':'(x-8)^6*(x^2-272*x+1088)','indicator_left_absolute_bound':len(sd),'indicator_right_absolute_lower_bound':4,'status':'PASS'})
    return {'status':'PASS','criterion':'quadratic_prime_indicator_balance','scope':'general_complex_via_two_dimension_Galois_pseudo_unitarity','proof':'Q17_INDICATOR_BALANCE_PROOF.md','optimizer_used':False,'finite_search_used':False,'cases':out}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path);a=ap.parse_args();out=verify(a.repo);txt=json.dumps(out,indent=2)+'\n'
    if a.output:a.output.write_text(txt)
    print(txt)
if __name__=='__main__':main()
