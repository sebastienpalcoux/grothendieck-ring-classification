"""The split-module criterion for self-dual direct sums, not only simples."""
from pathlib import Path
import itertools,json,math,time
import sympy as s
from split_module_polynomial import require,search_setup,PRIME
HERE=Path(__file__).resolve().parent
def setup(R,g,weights):
    n=len(R);require(len(weights)==n and all(isinstance(w,int) and w>=0 for w in weights),'invalid object')
    require(all(R[i][j]==R[j][i] for i in range(n) for j in range(n)),'commutativity required')
    require(g!=0 and R[g][g]==[1]+[0]*(n-1),'involution required')
    du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    require(all(weights[i]==weights[du[i]] for i in range(n)),'object not self-dual')
    fixed=[i for i in range(n) if R[g][i][i]];require(fixed,'no fixed object')
    N=sum((weights[i]*s.Matrix(R[i]) for i in range(n)),s.zeros(n))
    A=[[int(N[i,j]) for j in fixed] for i in fixed];require(A==list(map(list,zip(*A))),'nonsymmetric block')
    f=len(fixed);parent=list(range(f));entries=[]
    def root(i):
        while i!=parent[i]:i=parent[i]
        return i
    for i in range(f):
        for j in range(i,f):
            a=A[i][j];allowed=list(range(-a,a+1,2));gauge=False
            if i!=j and a%2 and root(i)!=root(j):
                parent[root(i)]=root(j);allowed=[v for v in allowed if v>0];gauge=True
            entries.append([i,j,allowed,gauge])
    coefficients=[int(c) for c in N.charpoly().as_poly().sqf_part().all_coeffs()]
    V=s.zeros(n)
    for c in coefficients:V=V*N+c*s.eye(n)
    require(V==s.zeros(n),'source polynomial identity')
    return dict(fixed=fixed,bounds=A,entries=entries,polynomial=coefficients,cases=math.prod(len(e[2]) for e in entries),prime=PRIME)
def verify(R,c):
    require(c['kind']=='rank8_split_module_object_polynomial','wrong certificate')
    a=search_setup(setup(R,c['involution'],c['generator_object']),c['search']['cases'])
    require(a['outcome']=='excluded' and a==c['search'],'object certificate did not replay')
def main():
    base=HERE.parent;rows={r['id']:r for r in json.loads((base/'pipeline/census_m3.json').read_text())};out=[]
    previous=json.loads((HERE/'split_module_polynomial_results.json').read_text())
    for item in previous:
        if item['outcome']!='no_conclusion':continue
        row=rows[item['id']];R=row['tensor'];start=time.monotonic();candidates=[];reports=[];cert=None
        atoms=[]
        for i in range(1,8):
            j=row['dual'][i]
            if j<i:continue
            weights=[0]*8;weights[i]=1
            if j!=i:weights[j]=1
            atoms.append(weights)
        objects=[a for a in atoms if sum(a)>1]+[[a[i]+b[i] for i in range(8)] for a,b in itertools.combinations(atoms,2)]
        for g in row['invertibles']:
            if not g or R[g][g][0]!=1 or not any(R[g][i][i] for i in range(8)):continue
            for weights in objects:
                a=setup(R,g,weights)
                candidates.append((a['cases'],g,weights,a))
        for count,g,weights,a in sorted(candidates,key=lambda v:v[0]):
            if count>2000000:
                reports.append({'involution':g,'generator_object':weights,'outcome':'enumeration_budget','cases':count});continue
            result=search_setup(a);reports.append({'involution':g,'generator_object':weights,'search':result})
            if result['outcome']=='excluded':
                cert={'kind':'rank8_split_module_object_polynomial','involution':g,'generator_object':weights,'search':result};verify(R,cert);break
        record={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'outcome':'excluded' if cert else 'no_conclusion','certificate':cert,'attempts':reports,'seconds':round(time.monotonic()-start,3)}
        out.append(record);(HERE/'split_module_object_results.json').write_text(json.dumps(out,indent=2)+'\n');print(row['id'],record['outcome'],record['seconds'],flush=True)
if __name__=='__main__':main()
