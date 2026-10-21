"""Complete C3 Fourier split-module systems for 439/567, with positive control331.

Arithmetic is exact in Z[z]/(z^2+z+1). These are necessary module data;
the surviving representations do not supply categorifications.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,math
HERE=Path(__file__).resolve().parent
ZERO=(0,0);ONE=(1,0);ROOTS=[ONE,(0,1),(-1,-1)]


def need(v,m):
    if not v:raise ValueError(m)


def add(a,b):return(a[0]+b[0],a[1]+b[1])
def scale(n,a):return(n*a[0],n*a[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]-a[1]*b[1])
def conj(a):return(a[0]-a[1],-a[1])
def matmul(A,B):return[[add(mul(A[i][0],B[0][j]),mul(A[i][1],B[1][j]))for j in range(2)]for i in range(2)]
def star(A):return[[conj(A[j][i])for j in range(2)]for i in range(2)]
def domain(a):return sorted({(u0-u2,u1-u2)for u0 in range(a+1)for u1 in range(a-u0+1)for u2 in [a-u0-u1]})
def equal_sum(S,coeff):
    return [[tuple(sum(coeff[k]*S[k][i][j][a]for k in range(8))for a in range(2))for j in range(2)]for i in range(2)]


def search(row,g):
    R=row['tensor'];digest=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    need(digest==row['tensor_sha256'],'source digest')
    dual=[next(j for j in range(8)if R[i][j][0])for i in range(8)]
    inv=[i for i in range(8)if R[i][dual[i]]==[1]+[0]*7]
    def ring_product(a,b):
        hits=[j for j,z in enumerate(R[a][b])if z]
        need(len(hits)==1 and R[a][b][hits[0]]==1,'not simple product')
        return hits[0]
    g2=ring_product(g,g);need(g2 not in [0,g]and ring_product(g,g2)==0,'C3 generator')
    F=[i for i in range(8)if R[i][g][i]];need(len(F)==2,'two fixed simples required')
    need(all(R[g][v][v]for v in F),'left fixed action')
    h=next(i for i in inv if i and R[i][i][0]and ring_product(i,F[0])==F[1])
    x,y=F;need(ring_product(h,y)==x and ring_product(x,h)==y,'odd involution swaps both fixed simples')
    theta=1 if ring_product(ring_product(h,g),h)==g else -1
    need(ring_product(ring_product(h,g),h)==(g if theta==1 else g2),'conjugation relation')
    powers=[0,g,g2];odd=[ring_product(z,h)for z in powers]
    need(sorted(powers+odd+F)==list(range(8)),'source generation')
    I=[[ONE,ZERO],[ZERO,ONE]];H=[[ZERO,ONE],[ONE,ZERO]]
    bounds=[[R[x][v][w]for w in F]for v in F]
    domains=[domain(b)for line in bounds for b in line]
    all_domains=[[[domain(R[k][v][w])for w in F]for v in F]for k in range(8)]
    count=0;solutions=[]
    for phase in range(3):
        G=[[ROOTS[phase],ZERO],[ZERO,ROOTS[(theta*phase)%3]]]
        G2=matmul(G,G)
        for vals in itertools.product(*domains):
            count+=1;X=[list(vals[:2]),list(vals[2:])]
            if matmul(G,X)!=X or matmul(X,H)!=matmul(H,X):continue
            S=[None]*8
            for i,M in zip(powers,[I,G,G2]):S[i]=M
            for i,M in zip(odd,[H,matmul(G,H),matmul(G2,H)]):S[i]=M
            S[x]=X;S[y]=matmul(H,X)
            if any(star(S[k])!=S[dual[k]]for k in range(8)):continue
            if any(S[k][i][j]not in all_domains[k][i][j]for k in range(8)for i,j in itertools.product(range(2),repeat=2)):continue
            if any(matmul(S[i],S[j])!=equal_sum(S,R[i][j])for i,j in itertools.product(range(8),repeat=2)):continue
            solutions.append({'phase':phase,'matrices':S})
    need(count==3*math.prod(len(d)for d in domains),'incomplete finite search')
    need(len(solutions)==2 and {z['phase']for z in solutions}=={1,2},'unexpected Fourier solutions')
    need(all(all(v==ZERO for line in z['matrices'][x]for v in line)for z in solutions),'nonzero noninvertible action survives')
    return {'id':row['id'],'tensor_sha256':digest,'group_generator':g,'odd_involution':h,
            'fixed':F,'odd_conjugation_exponent':theta,'noninvertible_generator':x,
            'entry_bounds':bounds,'finite_cases_after_proved_phase_gauge':count,
            'exact_solutions':solutions,'outcome':'two conjugate necessary Fourier representations; no exclusion or construction',
            'positive_model_control':row['id']=='R8_3_331'}


def run():
    rows={r['id']:r for r in json.loads((HERE.parents[1]/'rank8_m3_20261021/pipeline/census_m3.json').read_text())}
    return json.loads(json.dumps({'kind':'complete_C3_Fourier_split_module_search',
            'records':[search(rows[f'R8_3_{i}'],g)for i,g in [(439,1),(567,1),(331,3)]]}))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');a=p.parse_args();actual=run();path=HERE/'cubic_split_module_results.json'
    if a.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(json.loads(path.read_text())==actual,'saved evidence differs')
    print('PASS: complete C3 Fourier systems for439/567 and positive control331; exact necessary representations survive')
