"""Independent finite coverage audit for the proposed D40 converse.

Uses binary lifting to count Z/4 kernels, independent of the producer's
Smith reduction. Reconstructs every relative twist, including tensor duplicates.
"""
from pathlib import Path
import itertools,json,sys,time
import numpy as np

ROUND=Path(__file__).resolve().parents[2]
BASE=ROUND.parent/'rank12-m1-offline-20261025'
GRADED=ROUND/'family_graded'
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(GRADED))
from feudal_dual import construct,common

def require(x,msg):
    if not x:raise ValueError(msg)

def bitcolumn(v):
    return sum(1<<int(i)for i in np.flatnonzero(np.asarray(v)%2))

def insert(v,piv):
    while v:
        i=v.bit_length()-1
        if i not in piv:piv[i]=v;return True
        v^=piv[i]
    return False

def binary_kernel(M):
    m,n=M.shape;piv={}
    for row in M:insert(bitcolumn(row),piv)
    free=[j for j in range(n)if j not in piv];basis=[]
    for j in free:
        v=1<<j
        for i,row in sorted(piv.items()):
            if (row&v).bit_count()%2:v^=1<<i
        require(all((row&v).bit_count()%2==0 for row in piv.values()),'binary null vector')
        basis.append(v)
    return len(piv),basis

def log2_image_mod4(M):
    """Exact base-two logarithm of the image size of M over Z/4.

    Every mod-two kernel vector v lifts iff Mv/2 lies in im(M mod2).
    Its obstruction in that cokernel is linear; the number of lifts of
    every liftable vector is 2^(n-rank(M mod2)).
    """
    M=np.asarray(M,dtype=np.int64);m,n=M.shape;r,basis=binary_kernel(M)
    colp={}
    for j in range(n):insert(bitcolumn(M[:,j]),colp)
    require(len(colp)==r,'independent row/column binary ranks')
    for v in basis:
        vector=np.array([(v>>i)&1 for i in range(n)],dtype=np.int64)
        image=M@vector
        require(not np.any(image%2),'binary kernel divisible by two')
        insert(bitcolumn(image//2),colp)
    obstruction=len(colp)-r
    return 2*r+obstruction

def main():
    start=time.monotonic()
    rng=np.random.default_rng(17)
    for _ in range(20):
        control=rng.integers(-3,4,(3,4),dtype=np.int64)
        actual={tuple(control@np.array(v,dtype=np.int64)%4)for v in itertools.product(range(4),repeat=4)}
        require(len(actual)==2**log2_image_mod4(control),'independent exhaustive small-matrix cardinality control')
    # The only alternative order-twenty group is D10 x C2. Verify the
    # group facts behind the associator-independent commutativity lemma.
    def dm(a,b):
        return (a%5+(-1 if(a//5)&1 else 1)*(b%5))%5+5*(((a//5)&1)^((b//5)&1))+10*((a//10)^(b//10))
    inverse=[next(b for b in range(20)if dm(a,b)==0)for a in range(20)]
    H={0,5};normalizer=[a for a in range(20)if {dm(dm(a,h),inverse[a])for h in H}==H]
    require(normalizer==[0,5,10,15]and all(dm(10,a)==dm(a,10)for a in range(20)),'D20 normalizer and central quotient representative')
    cosets={tuple(sorted({dm(dm(h,a),k)for h,k in itertools.product(H,repeat=2)}))for a in range(20)}
    nonnormal=[D for D in cosets if len(D)==4]
    require(len(nonnormal)==4,'four dimension-two double cosets')
    for D in nonnormal:
        require(set(inverse[a]for a in D)==set(D),'inverse-stable nonnormal double coset')
        a=D[0];require(H&{dm(dm(a,h),inverse[a])for h in H}=={0},'trivial nonnormal stabilizer')
    data=json.loads((BASE/'tensors.json').read_text())
    families={r['id']:r for r in json.loads((BASE/'unresolved_families.json').read_text())['records']if r['family']=='D40'}
    integral_models=json.loads((GRADED/'integral_part_results.json').read_text())
    source_premises=[]
    for rid,row in families.items():
        R=data[rid];du=common.dual(R);units=[i for i in range(12)if sum(R[i][du[i]])==1]
        integral=[i for i,d in enumerate(row['dimensions_in_field'])if len(d)==1]
        twos=[i for i in integral if i not in units];lords=[i for i in range(12)if i not in integral]
        require(len(units)==len(twos)==len(lords)==4,'source D40 type')
        stabilizers=[[h for h in units if R[h][Y][Y]]for Y in twos]
        require(all(v==stabilizers[0]for v in stabilizers)and len(stabilizers[0])==2,'common two-dimensional stabilizer')
        g=next(h for h in stabilizers[0]if h)
        require(R[g][g][0]and all(R[g][i]==R[i][g]for i in range(12)),'central involution')
        require(all(not R[g][i][i]for i in lords),'free action on irrational simples')
        require(all(not R[i][j][k]for i,j in itertools.product(integral,repeat=2)for k in lords),'closed integral subring')
        E=[[[R[i][j][k]for k in integral]for j in integral]for i in integral]
        hits=[m for m in integral_models if common.based_iso(E,m['model_tensor'])is not None]
        require(hits,'integral pointed-Morita classification matches')
        if rid!='R12_1_449':
            require(any(E[i][j]!=E[j][i]for i,j in itertools.product(range(8),repeat=2)),'all eight integral subrings are noncommutative')
            require(all(m['group']=='F20'for m in hits),'six-model diagnostic agrees with the independent D20 exclusion')
        source_premises.append(dict(id=rid,g=g,integral_subring=integral,possible_pointed_groups=sorted({m['group']for m in hits})))
    co=json.loads((GRADED/'d8_cocycles.json').read_text());G=co['group_table'];n=len(G);c=co['subgroup_generator'];require(n==8 and c==2,'fixed grading subgroup')
    require(all(G[0][i]==G[i][0]==i for i in range(n)),'group unit')
    require(all(G[G[a][b]][d]==G[a][G[b][d]]for a,b,d in itertools.product(range(n),repeat=3)),'grading group associativity')
    r=1;s0=4
    require(G[r][r]==c and G[c][c]==0 and G[s0][s0]==0 and G[G[s0][r]][s0]==3,'actual D8 relations')
    # Independently verify the small split orthogonal group and its action.
    orthogonal=[]
    for a,b,d,e in itertools.product(range(5),repeat=4):
        if (a*e-b*d)%5 and all(((a*x+b*y)*(d*x+e*y)-x*y)%5==0 for x,y in itertools.product(range(5),repeat=2)):
            orthogonal.append(np.array([[a,b],[d,e]],dtype=np.int64))
    require(len(orthogonal)==8,'split orthogonal group has order eight')
    rot=np.array([[2,0],[0,3]],dtype=np.int64);invrot=np.array([[3,0],[0,2]],dtype=np.int64);I=np.eye(2,dtype=np.int64)
    reflections=[M for M in orthogonal if M[0,0]==M[1,1]==0]
    require(len(reflections)==4 and all(np.array_equal(M@M%5,I)and np.array_equal(M@rot@M%5,invrot)for M in reflections),'all odd classes reflect and square to one')
    require(len({tuple((np.linalg.matrix_power(rot,j)@reflections[0]%5).flat)for j in range(4)})==4,'changing the base lord covers all reflection choices')
    triples=list(itertools.product(range(1,n),repeat=3));ix={x:i for i,x in enumerate(triples)}
    pairs=list(itertools.product(range(1,n),repeat=2));pi={x:i for i,x in enumerate(pairs)}
    A=[]
    for a,b,d,e in itertools.product(range(1,n),repeat=4):
        row=[0]*len(triples)
        for value,key in [(1,(b,d,e)),(-1,(G[a][b],d,e)),(1,(a,G[b][d],e)),(-1,(a,b,G[d][e])),(1,(a,b,d))]:
            if key in ix:row[ix[key]]+=value
        A.append(row)
    row=[0]*len(triples);row[ix[c,c,c]]=1;A.append(row)
    A=np.asarray(A,dtype=np.int64)
    B=[]
    for a,b,d in triples:
        row=[0]*len(pairs)
        for value,key in [(1,(b,d)),(-1,(G[a][b],d)),(1,(a,G[b][d])),(-1,(a,b))]:
            if key in pi:row[pi[key]]+=value
        B.append(row)
    B=np.asarray(B,dtype=np.int64)
    require(not np.any(A@B),'integer bar differential squares to zero, including relative condition')
    kernel_log=2*len(triples)-log2_image_mod4(A);image_log=log2_image_mod4(B)
    quotient_log=kernel_log-image_log
    require(quotient_log==4,'relative mu4 cohomology has exactly sixteen classes')
    vectors=[]
    for w in co['representatives']:
        require(all(not w[a][b][d] for a,b,d in itertools.product(range(n),repeat=3)if 0 in(a,b,d)),'normalized cocycle')
        v=np.array([w[a][b][d]for a,b,d in triples],dtype=np.int64)
        require(not np.any((A@v)%4),'all relative cocycle equations')
        vectors.append(v)
    require(len(vectors)==16,'sixteen stored representatives')
    comparisons=0
    for i,j in itertools.combinations(range(16),2):
        require(log2_image_mod4(np.column_stack([B,(vectors[i]-vectors[j])%4]))>image_log,'distinct relative mu4 classes')
        comparisons+=1
    source=next(r for r in json.loads((GRADED/'feudal40_models_sparse.json').read_text())if r['parameters']['group']=='F20')
    R=source['tensor'];cert=source['certificate'];degree=[a//5 for a in range(20)]+list(range(4,8))
    require(all(degree[k]==G[degree[a]][degree[b]]for a,b,k in itertools.product(range(24),repeat=3)if R[a][b][k]),'D0 has the claimed faithful grading')
    ids=[156,263,309,383,467,470,501,514];targets={f'R12_1_{i}':data[f'R12_1_{i}']for i in ids};rows=[]
    for i,w in enumerate(co['representatives']):
        twist=dict(grading_group_table=G,grading=degree,cocycle=w,modulus=4)
        N,info=construct(R,cert,10,twist=twist)
        require(N is not None and info['rank']==12,'complete successful relative tensor construction')
        matches=[]
        for rid,T in targets.items():
            p=common.based_iso(T,N)
            if p is not None:matches.append(dict(id=rid,basis_map=p))
        require(len(matches)==1 and matches[0]['id']in('R12_1_156','R12_1_263'),'every twist belongs to one positive ring')
        rows.append(dict(index=i,tensor_sha256=common.sha(N),matches=matches))
    result=dict(status='PASS',source_premises=source_premises,independent_cohomology_method='binary lift obstruction and exact finite-module cardinalities',exhaustive_small_matrix_controls=20,mu4_relative_class_count=16,pairwise_distinctness_checks=comparisons,grading_twists_reconstructed=16,all_source_ids_tested=ids,possible_ids=sorted({r['matches'][0]['id']for r in rows}),records=rows,optimized_python=not __debug__,seconds=time.monotonic()-start)
    (OUT/('verification_optimized.json'if not __debug__ else'verification.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k not in('records','source_premises')},indent=2))

if __name__=='__main__':main()
