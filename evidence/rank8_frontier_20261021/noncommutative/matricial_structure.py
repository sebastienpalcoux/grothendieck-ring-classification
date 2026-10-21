"""Rational block and pointed-bimodule checks, independent of LP discovery."""
import itertools,json
import central_support as c
s=c.s

def mul(R,a,b):
    return s.Matrix([sum(a[i]*b[j]*R[i][j][k] for i in range(8) for j in range(8)) for k in range(8)])

def structure(R):
    a=c.w.spectral(R);du=a['du'];basis=[s.eye(8)[:,i] for i in range(8)]
    inv=[i for i in range(8) if R[i][du[i]]==[int(j==0) for j in range(8)]]
    out={'matrix_block_formal_codegree':str(a['codegrees'][-1].to_sympy_dict()) if False else c.ec(a['codegrees'][-1]),
         'scalar_dimension':4,'matrix_block_size':2,'dual_fixed_basis_count':sum(i==du[i] for i in range(8)),
         'matrix_involution_trace':sum(i==du[i] for i in range(8))-4}
    # The four scalar characters in these rings are all dual-invariant.
    sc=c.w.ScalarCharacters(R)
    for f,m in sc.components:
        K,ds,D,pD=sc.component(f);c.require(all(ds[i]==ds[du[i]] for i in range(8)),'scalar involution')
    out['matrix_involution_type']='symplectic' if out['matrix_involution_trace']==-2 else 'orthogonal'
    sd=[i for i in range(8) if du[i]==i];edges=[]
    for y,z in itertools.combinations(sd,2):
        for x in range(8):
            n=sum(R[x][y][j]*R[j][du[x]][z] for j in range(8))
            if n%2:edges.append([y,z,x,n]);break
    out['palindromic_odd_multiplicity_edges']=edges
    if len(inv)!=2:return out
    g=inv[1];left=[R[g][i].index(1) for i in range(8)];right=[R[i][g].index(1) for i in range(8)]
    c.require(all(sum(R[g][i])==sum(R[i][g])==1 for i in range(8)),'invertible actions')
    out.update(invertible=g,left_action=left,right_action=right,central=left==right)
    remaining=set(range(8));orbits=[]
    while remaining:
        i=min(remaining);orbit=sorted({i,left[i],right[i],left[right[i]]});remaining-=set(orbit)
        stabilizer=[(p,q) for p,q in itertools.product(range(2),repeat=2) if (left if p else list(range(8)))[(right if q else list(range(8)))[i]]==i]
        attempts=[]
        for omega in (0,1):
            vals=[(-1)**(omega*(x[0]*y[0]*z[0]+x[1]*y[1]*z[1])) for x,y,z in itertools.product(stabilizer,repeat=3)]
            c.require(all(v==1 for v in vals),'unexpected pointed bimodule stabilizer obstruction')
            attempts.append({'omega_exponent':omega,'checked_triples':len(vals),'restricted_cocycle_trivial':True})
        orbits.append({'basis':orbit,'stabilizer':list(map(list,stabilizer)),'cohomology_attempts':attempts})
    out['pointed_bimodule_orbits']=orbits
    if left!=right:return out
    e=(basis[0]-basis[g])/2
    reps=[min(x['basis']) for x in orbits if 0 not in x['basis']]
    Q=s.Matrix.hstack(e,*(mul(R,e,basis[i]) for i in reps));c.require(Q.rank()==4,'negative pointed quotient dimension')
    table=[]
    for i,j in itertools.product(range(4),repeat=2):
        z=Q.gauss_jordan_solve(mul(R,Q[:,i],Q[:,j]))[0]
        c.require(all(v.q==1 for v in z),'integral negative quotient multiplication')
        table.append(list(map(int,z)))
    out['negative_quotient']={'representatives':reps,'multiplication':table,'squares':[table[i*4+i] for i in range(1,4)]}
    return out

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    C=json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text());out=[]
    for r in C:
        if int(r['id'].split('_')[-1]) in (721,928,941,1154):out.append({'id':r['id'],'tensor_sha256':r['tensor_sha256'],**structure(r['tensor'])})
    p=c.HERE/'matricial_structure.json'
    if args.write:p.write_text(json.dumps(out,indent=2)+'\n')
    else:c.require(json.loads(p.read_text())==out,'matricial structure replay differs')
    print('PASS: four matricial/pointed structural checks')

if __name__=='__main__':main()
