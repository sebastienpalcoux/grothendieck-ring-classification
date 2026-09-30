"""Finite-level moment identities forced by dimension-block norm saturation.

For a real saturated character chi, construct Ind_B^{SL2(Z/f)} chi as a
signed monomial representation on the projective line. Every saturated
cyclic representation embeds in copies of this induced module. Its starting
vector lies in the exact compression-eigenvalue space K. Thus every matrix
identity sum_n c_n K* S* T^n S K=0 yields
sum_n c_n sum_Z |L_chi(FZ)|^2 theta_Z^n=0.

This module computes only necessary linear identities, without optimizers.
It does not infer a category, a full modular completion, or feasibility.
"""
import argparse,itertools,json,math,sys
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import sympy as s
from exact import require,evaluate
from dimension_block_support import saturated_characters

def nullspace(A,C):
    if not A:return []
    A=[list(row) for row in A];m=len(A);n=len(A[0]);piv=[];i=0
    for j in range(n):
        k=next((k for k in range(i,m) if A[k][j]),None)
        if k is None:continue
        A[i],A[k]=A[k],A[i];q=A[i][j];A[i]=[x/q for x in A[i]]
        for k in range(m):
            if k!=i and A[k][j]:q=A[k][j];A[k]=[x-q*y for x,y in zip(A[k],A[i])]
        piv.append(j);i+=1
        if i==m:break
    out=[]
    for j in range(n):
        if j in piv:continue
        v=[C.zero]*n;v[j]=C.one
        for k,p in enumerate(piv):v[p]=-A[k][j]
        out.append(v)
    return out

def induced_model(f,chi):
    units=[x for x in range(f) if math.gcd(x,f)==1]
    require(set(chi)==set(units) and all(x in (-1,1) for x in chi.values()),'real quadratic character required')
    require(all(chi[a*b%f]==chi[a]*chi[b] for a in units for b in units),'not a character')
    primitive=[v for v in itertools.product(range(f),repeat=2) if math.gcd(*v,f)==1]
    canonical={};reps=[]
    for v in primitive:
        if v in canonical:continue
        i=len(reps);reps.append(v)
        for u in units:
            w=(u*v[0]%f,u*v[1]%f);require(w not in canonical,'unit action not free');canonical[w]=(i,chi[u])
    n=len(reps)
    require(n==f*math.prod(s.Rational(p+1,p) for p in s.factorint(f)),'incomplete projective line')
    def operator(g):
        a,b,c,d=g;M=s.zeros(n)
        for j,(x,y) in enumerate(reps):
            i,sign=canonical[((a*x+b*y)%f,(c*x+d*y)%f)];M[i,j]=sign
        return M
    S=operator((0,-1,1,0));T=operator((1,1,0,1));I=s.eye(n)
    require(S*S==chi[-1%f]*I and T**f==I and (S*T)**3==S*S,'invalid induced modular representation')
    U=sum((T**k for k in range(f)),s.zeros(n))/f
    H=sum((chi[b]*operator((b,0,0,pow(b,-1,f))) for b in units),s.zeros(n))/len(units)
    Q=U*H;require(Q==Q.T and Q*Q==Q,'invalid U/torus projector')
    Z=s.Matrix.hstack(*Q.columnspace());G=Z.T*Z;A=G.inv()*Z.T*Q*S*Z
    require(Z*A==Q*S*Z,'compression leaves U/torus space')
    return dict(f=f,character=chi,S=S,T=T,projector=Q,basis=Z,gram=G,compression=A,representatives=reps)

def identities(data,character):
    pack=saturated_characters(data);C=pack['E'];F=pack['EF'];f=character['conductor'];lam=character['fourier']
    require(lam*lam==C.one/C(f),'real saturated character required')
    units=[b for b in range(f) if math.gcd(b,f)==1]
    ambient_units=[a for a in range(pack['F']) if math.gcd(a,pack['F'])==1]
    def character_value(a):
        dims=tuple(evaluate(x.to_list(),pack['C'].unit**a,pack['C']) for x in pack['dims'])
        j=next(j for j,b in enumerate(pack['reps']) if dims==tuple(evaluate(x.to_list(),pack['C'].unit**b,pack['C']) for x in pack['dims']))
        value=character['weights'][j]
        require(value in (C.one,-C.one),'complex character not implemented')
        return 1 if value==C.one else -1
    chi={b:character_value(next(a for a in ambient_units if a%f==b)) for b in units}
    model=induced_model(f,chi);Z=model['basis'];A=model['compression'];r=A.rows
    K=nullspace([[C(A[i,j])-lam*C(i==j) for j in range(r)] for i in range(r)],C)
    require(K,'saturated induced eigenspace empty')
    vectors=[[sum((C(Z[i,j])*v[j] for j in range(r)),C.zero) for i in range(Z.rows)] for v in K]
    def act(M,v):return [sum((C(M[i,j])*v[j] for j in range(M.cols) if M[i,j]),C.zero) for i in range(M.rows)]
    conj=lambda z:evaluate(z.to_list(),C.unit**(F-1),C)
    dot=lambda x,y:sum((conj(a)*b for a,b in zip(x,y)),C.zero)
    SK=[act(model['S'],v) for v in vectors];current=SK;moments=[]
    for n in range(f):
        moments.append([dot(v,w) for v in SK for w in current]);current=[act(model['T'],v) for v in current]
    require(current==SK,'moment period differs from conductor')
    require(F%f==0,'induced spectral projectors require conductor roots in the coefficient field')
    spectral_matrices=[]
    for a in range(f):
        spectral_matrices.append([sum((C.unit**((-a*n*(F//f))%F)*moments[n][j] for n in range(f)),C.zero)/C(f) for j in range(len(K)**2)])
    require(all(sum((M[j] for M in spectral_matrices),C.zero)==moments[0][j] for j in range(len(K)**2)),'spectral projector resolution failed')
    forbidden_root_powers=[a for a,M in enumerate(spectral_matrices) if not any(M)]
    relations=nullspace([list(row) for row in zip(*moments)],C)
    require(all(all(sum((c*x for c,x in zip(rel,row)),C.zero)==C.zero for row in zip(*moments)) for rel in relations),'moment relation verification failed')
    # Exact cyclic closure of the complete equality eigenspace.
    span=[]
    def add(v):
        v=list(v)
        for pivot,b in span:
            if v[pivot]:q=v[pivot];v=[x-q*y for x,y in zip(v,b)]
        pivot=next((i for i,x in enumerate(v) if x),None)
        if pivot is None:return False
        q=v[pivot];span.append((pivot,[x/q for x in v]));return True
    for v in vectors:add(v)
    j=0
    while j<len(span):
        v=span[j][1]
        for M in (model['S'],model['T']):add(act(M,v))
        j+=1
    return dict(conductor=f,field_conductor=F,character=chi,lambda_value=lam,
                induced_dimension=Z.rows,fixed_character_dimension=r,equality_dimension=len(K),
                cyclic_dimension=len(span),moment_span_rank=f-len(relations),
                relations=relations,moment_matrices=moments,equality_vectors=vectors,
                spectral_matrices=spectral_matrices,forbidden_root_powers=forbidden_root_powers)

def phase_equations(data,columns,low_columns,certificate):
    """Return cyclotomic equations on complete (column, phase-index) variables.

    columns omit the unit coordinate. Variables have column-major order with
    len(data['phases']) consecutive slots. Rotation auxiliary columns can be
    padded with zero by the caller. Every nonzero L column must already have
    its phase support restricted to conductor f; forbidden slots are zero here
    and are returned explicitly for deletion by the caller.
    """
    pack=saturated_characters(data);E=pack['E'];C=pack['C'];F=pack['F'];EF=pack['EF'];f=certificate['conductor']
    require(F%f==0,'equality phase equations require all conductor roots in the retained field')
    ch=next(ch for ch in pack['characters'] if ch['conductor']==f and ch['fourier']==certificate['lambda_value'])
    embed=lambda z:z if E==C else evaluate(z.to_list(),E.unit**(EF//F),E)
    def weight(v):
        q=sum((C(n)*x for n,x in zip(v,data['dims'])),C.zero)/data['DD']
        z=sum((a*embed(evaluate(q.to_list(),C.unit**b,C)) for a,b in zip(ch['weights'],pack['reps'])),E.zero)
        return z*evaluate(z.to_list(),E.unit**(EF-1),E)
    low=sum((weight(v) for v in low_columns),E.zero);nt=len(data['phases']);nvar=len(columns)*nt
    rows=[[E.zero]*nvar for _ in certificate['relations']]
    rhs=[-low*sum(rel,E.zero) for rel in certificate['relations']];forbidden=[]
    roots={tuple(C.unit**((F//f)*j*k) for k in range(1,len(data['phases'][0])+1)):j for j in range(f)}
    for i,v in enumerate(columns):
        a=weight((0,)+tuple(v))
        if not a:continue
        for ti,phase in enumerate(data['phases']):
            power=roots.get(tuple(phase))
            if power is None:forbidden.append(i*nt+ti);continue
            theta=E.unit**((EF//f)*power)
            for row,rel in zip(rows,certificate['relations']):row[i*nt+ti]=a*sum((c*theta**n for n,c in enumerate(rel)),E.zero)
    return rows,rhs,forbidden

def mixed_phase_equations(data,columns,low_columns):
    """Orthogonality moments between saturated characters of distinct conductors.

    Every occupied irreducible constituent of a saturated cyclic module has
    exact level f: it factors at f and contains a primitive conductor-f torus
    character. Distinct f therefore have disjoint irreducible supports, so
    their whole cyclic modules are orthogonal. This gives the mixed moments.
    """
    pack=saturated_characters(data);E=pack['E'];C=pack['C'];F=pack['F'];EF=pack['EF']
    embed=lambda z:z if E==C else evaluate(z.to_list(),E.unit**(EF//F),E)
    conj=lambda z:evaluate(z.to_list(),E.unit**(EF-1),E)
    def coefficient(v,ch):
        q=sum((C(n)*x for n,x in zip(v,data['dims'])),C.zero)/data['DD']
        return sum((a*embed(evaluate(q.to_list(),C.unit**b,C)) for a,b in zip(ch['weights'],pack['reps'])),E.zero)
    nt=len(data['phases']);rows=[];rhs=[];forbidden=set();metadata=[]
    for ch,other in itertools.combinations(pack['characters'],2):
        if ch['conductor']==other['conductor']:continue
        f=math.gcd(ch['conductor'],other['conductor']);require(F%f==0,'mixed roots not in retained field')
        low=sum((conj(coefficient(v,ch))*coefficient(v,other) for v in low_columns),E.zero)
        block=[[E.zero]*(len(columns)*nt) for _ in range(f)]
        roots={tuple(C.unit**((F//f)*j*k) for k in range(1,len(data['phases'][0])+1)):j for j in range(f)}
        for i,v in enumerate(columns):
            v=(0,)+tuple(v);a=conj(coefficient(v,ch))*coefficient(v,other)
            if not a:continue
            for ti,phase in enumerate(data['phases']):
                power=roots.get(tuple(phase))
                if power is None:forbidden.add(i*nt+ti);continue
                theta=E.unit**((EF//f)*power)
                for n,row in enumerate(block):row[i*nt+ti]=a*theta**n
        rows.extend(block);rhs.extend([-low]*f)
        metadata.append(dict(conductors=[ch['conductor'],other['conductor']],moment_orders=list(range(f))))
    return rows,rhs,sorted(forbidden),metadata

def encode(value):
    if hasattr(value,'to_list'):return list(map(str,value.to_list()))
    if isinstance(value,dict):return {k:encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return list(map(encode,value))
    return value

if __name__=='__main__':
    from round3_m4 import data_for
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path(__file__).with_suffix('.json'));args=ap.parse_args();out=[]
    census=json.loads((P/'data/census.json').read_text())
    for ident in ('R6_5_1204','R6_8_1660'):
        R=next(r['N'] for r in census if r['id']==ident);data=data_for(R,3,24);pack=saturated_characters(data)
        for ch in pack['characters']:
            result=identities(data,ch);record=dict(id=ident,**encode(result));out.append(record)
            print({k:v for k,v in record.items() if k not in ('relations','moment_matrices','equality_vectors','spectral_matrices')},flush=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n')
