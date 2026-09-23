"""Secondary arithmetic controls; none replaces full certificate checking."""
import collections,copy,itertools,json,math
from pathlib import Path
import sympy as s
from exact import require,VerificationError
P=Path(__file__).resolve().parents[1]

def system(du):
    triples=list(itertools.combinations_with_replacement(range(1,5),3));orbits=[];mapping={}
    for tri in triples:
        if tri in mapping:continue
        orb=sorted({tri,tuple(sorted(du[i] for i in tri))});orbits.append(orb)
        for t in orb:mapping[t]=len(orbits)-1
    sy=s.symbols('v:'+str(len(orbits)))
    def entry(i,j,k):
        if i==0:return s.Integer(j==k)
        if j==0:return s.Integer(i==k)
        if k==0:return s.Integer(du[i]==j)
        return sy[mapping[tuple(sorted((i,j,du[k])))]]
    N=[s.Matrix(5,5,lambda j,k:entry(i,j,k)) for i in range(5)];polys=set()
    for i in range(1,5):
        for j in range(1,i):
            for e in N[i]*N[j]-N[j]*N[i]:
                p=s.Poly(e,*sy)
                if not p:continue
                if p.LC()<0:p=-p
                polys.add(p.as_expr())
    return {'dual':list(du),'orbits':[[list(t) for t in orb] for orb in orbits],
            'equations':[[[int(co),list(mon)] for mon,co in s.Poly(p,*sy).terms()] for p in sorted(polys,key=str)]}

def run(rows,cache,registry):
    report={}
    # Coordinate definitions are rederived from the ring axioms.
    for ty,du in [(0,(0,1,2,3,4)),(2,(0,1,2,4,3)),(4,(0,2,1,4,3))]:
        require(system(du)==json.load(open(P/'data'/f'census_system{ty}.json')),'equations differ from axioms')
    report['coordinate_systems']='20/13/10 variables; 21/12/13 associativity polynomials regenerated'
    # Independent arbitrary-integer Gram-vector enumeration.
    from gram_vectors import native
    gram_cases=0
    for Q in [s.eye(4),s.ones(4)+s.eye(4),s.diag(4,3,2,1),s.Matrix([[5,2,1,1],[2,4,1,1],[1,1,3,1],[1,1,1,2]])]:
        adj=Q.adjugate();det=Q.det();vv=[]
        for v in itertools.product(*(range(math.isqrt(int(Q[i,i]))+1) for i in range(4))):
            if not any(v):continue
            if any(v[i]*v[j]>Q[i,j] for i in range(4) for j in range(i,4)):continue
            if sum(v[i]*int(adj[i,j])*v[j] for i in range(4) for j in range(4))<=det:vv.append(v)
        require(tuple(vv)==native(Q),'native/reference Gram-vector mismatch');gram_cases+=1
    report['gram_vector_reference_cases']=gram_cases
    # Native low-matrix pruning agrees with complete Python row-sum joins
    # followed by exact nonnegative-principal-minor tests.
    import higher_traces,induction
    low_tests=0
    for r in rows:
        if r['m']>3:break
        try:d=higher_traces.quadratic_data(r['N'])
        except Exception:continue
        if d is None or not all(d['columns']) or math.prod(map(len,d['columns']))>10000:continue
        ref=[]
        for cols in induction.low_matrices(d['columns'],d['ch'].C):
            L=s.Matrix.hstack(*map(s.Matrix,cols));Q=d['ch'].C-L*L.T
            if any(x<0 for x in Q):continue
            if any(Q.extract(ix,ix).det()<0 for k in range(1,5) for ix in itertools.combinations(range(1,5),k)):continue
            ref.append(cols)
        require(ref==induction.low_matrices(d['columns'],d['ch'].C,gram_prune=True),'native/reference low join mismatch')
        low_tests+=1
        if low_tests==4:break
    require(low_tests==4,'insufficient independent low-join controls');report['low_join_reference_cases']=low_tests
    # Positive controls are theorem hypotheses and constructions, not a
    # demand that every incomplete obstruction solve the categorification.
    import cyclic_four,quadratic_parity,unified
    R=next(r['tensor'] for r in registry if r['name']=='Izumi C4+4')
    pc=json.load(open(P/'data/positive_cyclic_control.json'))
    require(cyclic_four.parameter(R)==pc['parameter']==1,'positive cyclic tensor mismatch')
    require(pc['branch'] in cyclic_four.branches(1),'positive cyclic branch missing')
    require(not cyclic_four.galois_failure(1,pc['branch']),'false Galois obstruction on positive branch')
    A,b,meta=cyclic_four.system(1,pc['branch'],pc['height'])
    require(meta==pc['meta'],'positive cyclic system mismatch')
    x=[s.Rational(0)]*meta['columns'];seen_control=set()
    for i,value in pc['nonzero_coordinates']:
        require(type(i) is int and 0<=i<len(x) and i not in seen_control,'invalid positive-control coordinate')
        seen_control.add(i);x[i]=s.Rational(value)
        require(x[i]>=0,'negative feasible-control coordinate')
    require(s.Matrix(A)*s.Matrix(x)==s.Matrix(b),'positive cyclic exact feasibility failed')
    report['cyclic_positive_control']='K(C4,4): exact rational feasible branch; no numerical LP invoked'
    # Reject incomplete branches and false hypotheses in the new criteria.
    by={unified.fingerprint(r['N']):r['N'] for r in rows}
    mutations=0
    for kind in ('cyclic_four_central','quadratic_parity_pseudo','signed_extension_positive'):
        key,c=next((k,c) for k,c in cache.items() if c['kind']==kind)
        bad=copy.deepcopy(c)
        if kind=='quadratic_parity_pseudo':bad['descent']['q']+=1
        elif kind=='signed_extension_positive':bad['branches'].append({})
        else:bad['branches']=bad['branches'][:-1]
        rejected=False
        try:unified.verify(by[key],bad)
        except Exception:rejected=True
        require(rejected,'mutated certificate was accepted');mutations+=1
    # Directly check the exact Farkas orientation and integrality guard.
    require(higher_traces.check_farkas([[1]],[-1],[1],False),'valid scalar Farkas ray rejected')
    require(not higher_traces.check_farkas([[1]],[-1],[-1],False),'invalid scalar Farkas ray accepted')
    require(not higher_traces.check_farkas([[1]],[-1],[1.0],False),'floating Farkas ray accepted')
    report['mutation_and_dual_ray_controls']=mutations+3
    print('PASS secondary controls: ring-coordinate equations, native/reference comparisons, positive and mutation controls.',flush=True)
    return report
