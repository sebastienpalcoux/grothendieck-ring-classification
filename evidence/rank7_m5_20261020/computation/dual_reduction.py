"""Exact elimination of dual restriction variables, with full-ray lifting.

This evidence-local implementation retains the original character-induction
certificate vocabulary.  Discovery sums paired columns.  Replay does not use
that quotient: it checks the lifted ray on every original, retained column,
with each omitted duality equality represented by its two sparse entries.
"""
import hashlib,json,sys,time
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path[:0]=[str(ROOT/'supplements/rank7/software'),str(ROOT/'supplements/rank7')]
import balanced_traces as bt
import tensor_rotation as tr
import character_induction as ci
import higher_traces as ht
from exact import require


def sparse_duality(labels,du):
    """The identical ordering and signs as balanced_traces.system."""
    positions={(tuple(v),ti):j for j,(v,ti) in enumerate(labels)}
    require(len(positions)==len(labels),'duplicate restriction/trace variable')
    out=[];seen=set()
    for v,ti in sorted(positions):
        w=tuple(v[du[i]-1] for i in range(1,len(du)))
        pair=tuple(sorted((v,w)))
        if v==w or (pair,ti) in seen:continue
        seen.add((pair,ti))
        out.append((positions.get((v,ti)),positions.get((w,ti))))
    return out


def without_duality(R,data,L,ep,height):
    A,b,meta=bt.build_system(R,data,L,ep,height)
    labels=meta['labels'];nvars=len(A[0]);q=data['q']
    D=data['global_dimension'];d=data['dimensions'];base_rows=len(b)
    eqs=sparse_duality(labels,bt.dual(R));galois_count=0
    if q>1:
        norm=D[0]**2-q*D[1]**2
        ratio=((D[0]**2+q*D[1]**2)/norm,2*D[0]*D[1]/norm)
        def hat(z):
            y=bt.mul(ratio,(z[0],-z[1]),q)
            return y if bt.positive_pair(y,q) else (-y[0],-y[1])
        def dim(v):
            return tuple(sum((bt.Q(v[i])*d[i][k] for i in range(len(R))),bt.Q(0)) for k in range(2))
        low=Counter(dim(list(L[:,j])) for j in range(L.cols))
        hd=[dim([0]+v) for v,ti in labels]
        allvals=set(low)|set(hd);allvals|={hat(z) for z in allvals};seen=set()
        for z in sorted(allvals):
            w=hat(z);require(hat(w)==z,'Galois dimension involution failed')
            pair=tuple(sorted((z,w)))
            if z==w or pair in seen:continue
            seen.add(pair)
            A.append([int(v==z)-int(v==w) for v in hd]+[0]*(nvars-len(hd)))
            b.append(low[w]-low[z]);galois_count+=1
    meta.update(balance_rows=len(eqs)+galois_count,duality_rows=len(eqs),
                galois_rows=galois_count,sparse_duality=eqs,base_rows=base_rows)
    return A,b,meta


class SparseDualSystem:
    def __init__(self,A,b,meta,keep):
        self.A=A;self.b=b;self.meta=meta;self.keep=keep
        self.base=meta['base_rows'];self.eqs=meta['sparse_duality']
    def full_rhs(self):
        return self.b[:self.base]+[0]*len(self.eqs)+self.b[self.base:]
    def full_ray(self,y):
        """Lift a ray of the quotient system into the original equalities."""
        require(len(y)==len(self.b),'incorrect reduced ray length')
        keep=set(self.keep)
        scores={j:sum(row[j]*z for row,z in zip(self.A,y))
                for pair in self.eqs for j in pair if j is not None and j in keep}
        dual=[]
        for plus,minus in self.eqs:
            dual.append(-scores[plus] if plus in keep else scores[minus] if minus in keep else 0)
        return y[:self.base]+dual+y[self.base:]
    def reduced_matrix(self):
        keep=set(self.keep);paired=set();groups=[]
        for plus,minus in self.eqs:
            paired.update(j for j in (plus,minus) if j is not None)
            if plus in keep and minus in keep:groups.append((plus,minus))
            # A lone retained variable is forced to zero by its duality row.
        groups.extend((j,) for j in self.keep if j not in paired)
        require(groups,'no retained reduced variables')
        return [[sum(row[j] for j in group) for group in groups] for row in self.A]
    def check(self,b,y,raise_error=True):
        okay=(b==self.full_rhs() and len(y)==len(b) and all(type(z) is int for z in y))
        if okay:
            z=y[self.base:self.base+len(self.eqs)]
            ordinary=y[:self.base]+y[self.base+len(self.eqs):]
            scores=[sum(row[j]*v for row,v in zip(self.A,ordinary)) for j in self.keep]
            position={j:i for i,j in enumerate(self.keep)}
            for (plus,minus),v in zip(self.eqs,z):
                if plus in position:scores[position[plus]]+=v
                if minus in position:scores[position[minus]]-=v
            okay=all(v>=0 for v in scores) and sum(v*w for v,w in zip(b,y))<0
        if raise_error:require(okay,'lifted full-column Farkas certificate fails')
        return okay


def pruned_system(R,data,L,ep,height,pruning):
    original=tr.system
    tr.system=without_duality
    try:A,b,meta=tr.system_rotation(R,data,L,ep,height)
    finally:tr.system=original
    forbidden=set(map(tuple,pruning['forbidden']));labels=meta['labels']
    keep=[j for j in range(len(A[0])) if j>=len(labels) or tuple(labels[j][0]) not in forbidden]
    system=SparseDualSystem(A,b,meta,keep)
    return system,system.full_rhs(),keep


def check_farkas(A,b,y,raise_error=True):
    if isinstance(A,SparseDualSystem):return A.check(b,y,raise_error)
    return ht.check_farkas(A,b,y,raise_error)


def farkas(A,b):
    if not isinstance(A,SparseDualSystem):return ht.farkas(A,b)
    start=time.monotonic();matrix=A.reduced_matrix()
    print(json.dumps({'event':'dual_reduced_system','original_rows':len(b),
        'reduced_rows':len(A.b),'original_columns':len(A.keep),
        'reduced_columns':len(matrix[0]),'seconds':time.monotonic()-start}),flush=True)
    digest=hashlib.sha256(json.dumps([matrix,A.b],separators=(',',':')).encode()).hexdigest()
    target=HERE/'exact_rays'/('dual_'+digest+'.json')
    if target.exists():
        y=json.loads(target.read_text())['reduced_y'];ht.check_farkas(matrix,A.b,y)
    else:
        y=ht.farkas(matrix,A.b)
        if y is None:return None
    lifted=A.full_ray(y);A.check(b,lifted)
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps({'system_sha256':digest,'reduced_y':y,'y':lifted,
        'bTy':sum(v*w for v,w in zip(b,lifted))},separators=(',',':'))+'\n')
    print(json.dumps({'event':'dual_exact_ray','system_sha256':digest,
        'seconds':time.monotonic()-start}),flush=True)
    return lifted


def install(discovery=False):
    ci.pruned_system=pruned_system;ci.check_farkas=check_farkas
    if discovery:ci.farkas=farkas


def source_hashes():
    paths=[Path(__file__),HERE/'source_frontier.json']
    paths += [ROOT/'supplements/rank7/software'/name for name in
              ('balanced_traces.py','higher_traces.py','tensor_rotation.py','character_induction.py')]
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def controls():
    """Compare dense original rows, including nontrivial dual swaps, exactly."""
    import os,sympy as s
    os.environ['RANK6_REFERENCE_GRAM']='1'
    comparisons=0;duality_rows=0;galois_rows=0
    rings=[[[[int((i+j)%order==k) for k in range(order)] for j in range(order)] for i in range(order)] for order in (3,4)]
    rings.append([[[1,0],[0,1]],[[0,1],[1,1]]])
    for R in rings:
        data=ht.quadratic_data(R,gram_prune=True)
        require(data is not None,'positive pointed control ineligible')
        for cols in data['lows']:
            L=s.Matrix.hstack(*map(s.Matrix,cols))
            for ep in ht.indicator_choices(R):
                for height in (3,4):
                    A,b,meta=tr.system_rotation(R,data,L,ep,height)
                    duality_rows+=meta['duality_rows'];galois_rows+=meta['galois_rows']
                    sparse,rhs,keep=pruned_system(R,data,L,ep,height,{'forbidden':[]})
                    require(rhs==b,'sparse/dense right sides differ')
                    dual=[]
                    for plus,minus in sparse.eqs:
                        row=[0]*len(A[0])
                        if plus is not None:row[plus]+=1
                        if minus is not None:row[minus]-=1
                        dual.append(row)
                    dense=sparse.A[:sparse.base]+dual+sparse.A[sparse.base:]
                    require(A==dense,'sparse/dense matrix entries differ')
                    for y in ([0]*len(b),list(range(len(b))),[-i for i in range(len(b))]):
                        require(ht.check_farkas(A,b,y,False)==sparse.check(b,y,False),'full-column checker disagrees')
                    comparisons+=1
    # Synthetic asymmetric/pruned dual pairs exercise the forced-zero case.
    cases=[([0,1,2],[(0,1)]),([0,2],[(0,1)]),([1,2],[(0,1)]),([2],[(0,1)])]
    for keep,eqs in cases:
        system=SparseDualSystem([[2,3,0],[-1,5,2]],[-1,0],
            {'base_rows':1,'sparse_duality':eqs},keep)
        y=[1,1];lifted=system.full_ray(y)
        require(system.check(system.full_rhs(),lifted),'synthetic lifted ray failed')
        require(not system.check(system.full_rhs(),[0]*len(lifted),False),'zero ray accepted')
    require(duality_rows and galois_rows,'controls lack duality or quadratic Galois rows')
    out={'status':'PASS','dense_matrix_comparisons':comparisons,'duality_rows_compared':duality_rows,
         'galois_rows_compared':galois_rows,'synthetic_pruning_controls':len(cases),
         'optimized_python':not __debug__,'source_hashes':source_hashes()}
    (HERE/('dual_reduction_controls_optimized.json' if not __debug__ else 'dual_reduction_controls.json')).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':controls()
