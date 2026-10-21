"""Exact fusion constraints for the rank-eight dual of A=1+rho.

The source is the C4 generalized-Haagerup based ring with multiplicity two.
Dual basis: 1,a,a',b,b',d,c,e, dimensions 1,a,a,a+1,a+1,2a+1,2a,2a+2.
"""
from pathlib import Path
import itertools,json,sys
import sympy as s
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from construction_reductions import need,validate

def source():
    N=[[[0]*8 for _ in range(8)]for _ in range(8)]
    for i,j in itertools.product(range(4),repeat=2):
        N[i][j][(i+j)%4]=1
        N[i][4+j][4+(i+j)%4]=1
        N[4+i][j][4+(i-j)%4]=1
        N[4+i][4+j][(i-j)%4]=1
        for k in range(4):N[4+i][4+j][4+k]=2
    validate(N)
    return N

B=s.Matrix.hstack(*map(s.Matrix,[
    [1,0,0,0,1,0,0,0],
    [0,0,0,0,1,1,1,1],[0,0,0,0,1,1,1,1],
    [0,0,1,0,1,1,2,1],[0,0,1,0,1,1,2,1],
    [1,0,0,0,3,2,2,2],[0,0,0,0,2,2,2,2],
    [0,1,0,1,2,3,2,3]]))
# a^2=3a+2.
dims=[(1,0),(0,1),(0,1),(1,1),(1,1),(1,2),(0,2),(2,2)]
def mul(u,v):return(u[0]*v[0]+2*u[1]*v[1],u[0]*v[1]+u[1]*v[0]+3*u[1]*v[1])

def prepare(da,db):
    du=[0,2,1,3,4,5,6,7]if da else list(range(8))
    if db:du[3],du[4]=4,3
    todo=set(itertools.product(range(8),repeat=3));orbits=[];loc={}
    while todo:
        at=min(todo);orb={at};pending=[at]
        while pending:
            i,j,k=pending.pop()
            for z in [(du[i],k,j),(k,du[j],i),(du[j],du[i],du[k])]:
                if z not in orb:orb.add(z);pending.append(z)
        for z in orb:loc[z]=len(orbits)
        todo-=orb;orbits.append(sorted(orb))
    N=source();rows=[]
    def equation(terms,rhs):
        row=[0]*(len(orbits)+1)
        for at,v in terms:row[loc[at]]+=int(v)
        row[-1]=int(rhs);rows.append(row)
    for i,j,k in itertools.product(range(8),repeat=3):
        if i==0 or j==0 or k==0:
            equation([((i,j,k),1)],int(k==j)if i==0 else int(k==i)if j==0 else int(j==du[i]))
    for i,j in itertools.product(range(8),repeat=2):
        for h in (0,1):equation([((i,j,k),dims[k][h])for k in range(8)],mul(dims[i],dims[j])[h])
    # I(X) tensor_A I(Y) = I(X tensor A tensor Y).
    for i,j,z in itertools.product(range(8),repeat=3):
        rhs=sum(N[i][a][u]*N[u][j][t]*B[t,z]for a in(0,4)for u in range(8)for t in range(8))
        equation([((x,y,z),B[i,x]*B[j,y])for x in range(8)for y in range(8)if B[i,x]*B[j,y]],rhs)
    E=s.Matrix(rows);R,pivots=E.rref();good=len(orbits)not in pivots
    record=dict(dual_a=bool(da),dual_b=bool(db),variables=len(orbits),equations=len(rows),linear_consistent=good)
    if good:
        free=[i for i in range(len(orbits))if i not in pivots];record['free_variables']=len(free)
        record['free_orbits']=[orbits[j]for j in free]
        record['rref']=[[str(v)for v in R.row(i)]for i in range(len(pivots))]
        record['pivots']=list(pivots);record['free_indices']=free;record['orbits']=orbits
    return record

def main():
    records=[]
    for da,db in itertools.product(range(2),repeat=2):
        rec=prepare(da,db);records.append(rec)
        print({k:v for k,v in rec.items()if k not in('rref','orbits','free_orbits','free_indices','pivots')},flush=True)
    (HERE/'r721_dual_linear.json').write_text(json.dumps(records,indent=2)+'\n')

if __name__=='__main__':main()
