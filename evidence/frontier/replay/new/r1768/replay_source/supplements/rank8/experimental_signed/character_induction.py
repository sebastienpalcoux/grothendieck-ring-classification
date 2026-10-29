"""Character-aware central induction with exact modular reciprocity.

Discovery may ask the inherited LP routine for an exact separating vector.
Verification uses only exact arithmetic and exhausts all low-column labellings.
No census identifiers enter the mathematical tests.
"""
import itertools,math
import sympy as s
from exact import require,pc,evaluate
from involution_module import generated_basis
from tensor_rotation import quadratic_data,low_failure,indicator_choices,system_rotation,farkas,check_farkas
from rings import Characters,dual
from higher_traces import high_columns

class Ineligible(ValueError):
    pass

def roots_degree_two(f):
    co=f.all_coeffs()
    if f.degree()==1:return [-co[1]/co[0]]
    if f.degree()!=2:raise Ineligible('a generating spectrum has degree greater than two')
    a,b,c=co;d=s.sqrt(b*b-4*a*c)
    return [s.expand((-b-d)/(2*a)),s.expand((-b+d)/(2*a))]

class CharacterTable:
    def __init__(self,R,data):
        self.n=n=len(R);self.du=dual(R);a=data['ch'];eigen={}
        if any(R[i][j]!=R[j][i] for i in range(n) for j in range(n)):
            raise Ineligible('commutative character-induction implementation only')
        for i in range(1,n):
            factors=a.N[i].charpoly().as_poly().factor_list()[1]
            if any(f.degree()>2 for f,m in factors):continue
            eigen[i]=sorted(set(x for f,m in factors for x in roots_degree_two(f)),key=str)
        seeds=[]
        for size in (1,2):
            for seed in itertools.combinations(eigen,size):
                z=generated_basis(R,seed)
                if z:seeds.append((math.prod(len(eigen[i]) for i in seed),seed,z))
            if seeds:break
        if not seeds:raise Ineligible('no one- or two-object quadratic-spectrum generating set')
        _,self.seed,(words,inv)=min(seeds,key=lambda z:(z[0],z[1]))
        roots=[x for i in self.seed for x in eigen[i]]+[s.sqrt(data['q'])]
        self.K=K=s.QQ.algebraic_field(*roots)
        if K.mod.degree()>16:raise Ineligible('character splitting-field implementation degree bound')
        root_values={i:[K.from_sympy(x) for x in eigen[i]] for i in self.seed}
        self.rows=[];self.codegrees=[]
        for vals in itertools.product(*(root_values[i] for i in self.seed)):
            given=dict(zip(self.seed,vals));images=[]
            for word in words:
                z=K.one
                for i in word:z*=given[i]
                images.append(z)
            row=tuple(sum((K(inv[j,k])*images[k] for k in range(n)),K.zero) for j in range(n))
            if any(row[i]*row[j]!=sum((K(R[i][j][k])*row[k] for k in range(n)),K.zero) for i in range(n) for j in range(n)):continue
            self.rows.append(row);self.codegrees.append(sum((row[i]*row[self.du[i]] for i in range(n)),K.zero))
        require(len(self.rows)==n and len(set(self.rows))==n,'incomplete exact character table')
        self.ds=[K.from_sympy(s.Rational(x.numerator,x.denominator)+s.Rational(y.numerator,y.denominator)*s.sqrt(data['q'])) for x,y in data['dimensions']]
        self.D=sum((d*d for d in self.ds),K.zero)
        self.fp=next((i for i,row in enumerate(self.rows) if list(row)==self.ds),None)
        require(self.fp is not None,'positive character absent from exact table')
        self.dims={};self.values={};self.allowed={};self.compatibility={}
    def prepare(self,v):
        v=tuple(v)
        if v in self.dims:return
        K=self.K;n=self.n
        self.dims[v]=sum((K(v[i])*self.ds[i] for i in range(n)),K.zero)
        for h,row in enumerate(self.rows):self.values[h,v]=sum((K(v[i])*row[i] for i in range(n)),K.zero)
        self.allowed[v]=[h for h,f in enumerate(self.codegrees) if self.dims[v]*f==self.D]
    def assignments(self,columns):
        cols=tuple(map(tuple,columns));n=self.n
        for v in cols:self.prepare(v)
        result=[]
        def recurse(chosen):
            j=len(chosen)
            if j==n:result.append(tuple(chosen));return
            for h in self.allowed[cols[j]]:
                if h in chosen or (j==0 and h!=self.fp):continue
                valid=True
                for i,k in enumerate(chosen):
                    key=(h,cols[j],k,cols[i])
                    if key not in self.compatibility:
                        self.compatibility[key]=self.dims[cols[j]]*self.values[h,cols[i]]==self.dims[cols[i]]*self.values[k,cols[j]]
                    if not self.compatibility[key]:valid=False;break
                if valid:recurse(chosen+[h])
        recurse([]);return result
    def automorphisms(self):
        if hasattr(self,'_automorphisms'):return self._automorphisms
        K=self.K;t=s.Symbol('t')
        f=s.Poly.from_list([s.Rational(x) for x in K.mod.to_list()],t,domain=K)
        roots=[]
        for g,m in f.factor_list()[1]:
            require(g.degree()==1 and m==1,'character field is not Galois')
            a,b=g.all_coeffs();roots.append(-K.from_sympy(b)/K.from_sympy(a))
        require(len(set(roots))==K.mod.degree(),'incomplete field automorphisms')
        self._automorphisms=roots;return roots
    def galois_pruning(self,columns,high):
        K=self.K;low=list(map(tuple,columns));hh=[(0,)+tuple(v) for v,z in high]
        types=[]
        for v in low+hh:
            self.prepare(v);require(self.dims[v]!=K.zero,'zero restriction dimension')
            types.append(tuple((self.D/f)*self.values[h,v]/self.dims[v]
                               for h,f in enumerate(self.codegrees)))
        available=set(types);missing=set()
        roots=self.automorphisms()
        for typ in available:
            if any(tuple(evaluate(x.to_list(),root,K) for x in typ) not in available for root in roots):
                missing.add(typ)
        return {'high_columns':len(hh),
                'forbidden':[list(v[1:]) for v,typ in zip(hh,types[len(low):]) if typ in missing],
                'missing_low':[j for j,typ in enumerate(types[:len(low)]) if typ in missing]}
    def metadata(self):
        return {'seed':list(self.seed),'field_polynomial':[str(x) for x in self.K.mod.to_list()],
                'characters':[[[str(x) for x in z.to_list()] for z in row] for row in self.rows],
                'automorphisms':[[str(x) for x in r.to_list()] for r in self.automorphisms()]}

def reciprocity_data(R):
    if any(R[i][j]!=R[j][i] for i in range(len(R)) for j in range(len(R))):
        raise Ineligible('commutative input required')
    data=quadratic_data(R,gram_prune=True)
    if data is None:raise Ineligible('quadratic induction data unavailable')
    table=CharacterTable(R,data)
    return data,table

def pruned_system(R,data,L,ep,height,pruning):
    A,b,meta=system_rotation(R,data,L,ep,height)
    forbidden=set(map(tuple,pruning['forbidden']))
    labs=meta['labels'];keep=[j for j in range(len(A[0])) if j>=len(labs) or tuple(labs[j][0]) not in forbidden]
    return [[row[j] for j in keep] for row in A],b,keep

def certificate(R,height=6,progress=None):
    try:data,table=reciprocity_data(R)
    except Ineligible:return None
    branches=[]
    for ix,cols in enumerate(data['lows']):
        branch={'columns':[list(v) for v in cols]}
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:branch['ordinary']=why
        else:
            aa=table.assignments(cols);branch['labellings']=[list(p) for p in aa]
            if aa:
                L=s.Matrix.hstack(*map(s.Matrix,cols));_,high=high_columns(data,L)
                pruning=table.galois_pruning(cols,high);branch['galois']=pruning
                if pruning['missing_low']:
                    branches.append(branch);continue
                cases=[]
                for ep in indicator_choices(R):
                    if progress:progress(ix,list(ep))
                    A,b,keep=pruned_system(R,data,L,ep,height,pruning);y=farkas(A,b)
                    if y is None:return None
                    check_farkas(A,b,y)
                    cases.append({'indicators':list(ep),'y':y,'bTy':sum(x*z for x,z in zip(b,y))})
                branch['rotation']=cases
        branches.append(branch)
    return {'kind':'character_induction','height':height,'q':data['q'],'version':2,'table':table.metadata(),
            'column_counts':[len(v) for v in data['columns']],'branches':branches}

def verify(R,c):
    data,table=reciprocity_data(R)
    require(c['kind']=='character_induction' and c['q']==data['q'] and c.get('version')==2,'invalid character induction metadata')
    require(c['table']==table.metadata(),'incorrect or incomplete character table')
    require(c['column_counts']==[len(v) for v in data['columns']],'incomplete low-column sets')
    require(len(c['branches'])==len(data['lows']),'missing induction branches')
    for cols,branch in zip(data['lows'],c['branches']):
        require(branch['columns']==[list(v) for v in cols],'incorrect low columns')
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:require(branch.get('ordinary')==why,'incorrect ordinary obstruction');continue
        aa=table.assignments(cols);require(branch.get('labellings')==[list(p) for p in aa],'incomplete character labellings')
        if not aa:continue
        L=s.Matrix.hstack(*map(s.Matrix,cols));_,high=high_columns(data,L)
        pruning=table.galois_pruning(cols,high);require(pruning==branch.get('galois'),'incorrect Galois-pruning certificate')
        if pruning['missing_low']:continue
        eps=indicator_choices(R);cases=branch['rotation']
        require([x['indicators'] for x in cases]==list(map(list,eps)),'missing indicator choices')
        L=s.Matrix.hstack(*map(s.Matrix,cols))
        for ep,case in zip(eps,cases):
            A,b,keep=pruned_system(R,data,L,ep,c['height'],pruning);check_farkas(A,b,case['y'])
            require(case['bTy']==sum(x*y for x,y in zip(b,case['y'])),'incorrect Farkas value')

def lift_general(R,c,timeout=90):
    from proofs import sphere_certificate,signed_adjoint_parity,gauge_original,signed_component_certificate
    from oriented_signed import enumerate_all,from_values
    from oriented_extension import nc_certificate
    a=Characters(R);f,K,ds,D,pD,e=a.fp()
    gate='weak_integrality' if pD.degree()==1 else 'two_FP_values' if len(set(ds))==2 else None
    if gate:return {'kind':'oriented_pseudo_gate','gate':gate,'pseudo':c}
    sphere=sphere_certificate(R,lambda _:c)
    if sphere is None:return None
    vals,p,stats=enumerate_all(R,timeout);branches=[]
    for v in vals:
        T=from_values(R,p,v);b={'values':list(v)};why=signed_adjoint_parity(R,T);g=gauge_original(T,R)
        if why:b['obstruction']=why
        elif g:b['obstruction']={'kind':'gauge_original','signs':g}
        elif any(T[i][j]!=T[j][i] for i in range(len(R)) for j in range(len(R))):
            cc=nc_certificate(R,T)
            if cc is None:return None
            b['noncommutative']=cc
        else:
            aa=Characters(T);cc=[{'factor':pc(ff),'obstruction':signed_component_certificate(R,T,aa,ff,sphere)} for ff,_ in aa.components]
            if any(x['obstruction'] is None for x in cc):return None
            b['characters']=cc;b['generator']=aa.k
        branches.append(b)
    return {'kind':'oriented_signed','sphere':sphere,'branches':branches}

def general_certificate(R,height=6,timeout=90):
    c=certificate(R,height)
    return None if c is None else lift_general(R,c,timeout)

if __name__=='__main__':
    import argparse,json,time
    from pathlib import Path
    P=Path(__file__).resolve().parents[1];ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('ring');ap.add_argument('--height',type=int,default=6);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    require(not args.output.exists(),'refusing to overwrite existing output')
    R=next(r['N'] for r in json.load(open(P/'data/census.json')) if r['id']==args.ring)
    st=time.monotonic();c=certificate(R,args.height,lambda ix,ep:print('branch',ix,'indicators',ep,flush=True))
    if c:verify(R,c)
    args.output.write_text(json.dumps({'id':args.ring,'scope':'pseudo_unitary','certificate':c,'seconds':time.monotonic()-st},separators=(',',':'))+'\n')
    print('VERIFIED EXCLUSION' if c else 'NO EXCLUSION',time.monotonic()-st,flush=True)
