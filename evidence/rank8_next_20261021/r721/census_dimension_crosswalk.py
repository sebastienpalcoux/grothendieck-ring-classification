"""Exhaustive exact FP-dimension crosswalk through rank8 multiplicity3.

Every positive dimension assignment with the requested multiset has sum
21+5sqrt(17). It must therefore be an eigenvector of sum_i N_i with this
eigenvalue. First test exact characteristic-polynomial divisibility by
x^2-42x+16 for every source tensor; then solve the quadratic eigenvector
exactly and verify all64 multiplicativity identities for any matches.
"""
from pathlib import Path
import gzip,json,hashlib,collections
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'supplements/rank8/data/rank8_m3_tables.txt.gz'
PREVIOUS=ROOT/'supplements/rank8/data/rank8_tables.txt.gz'
CENSUS=ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json'
OLD_IDS=ROOT/'supplements/rank8/data/decisions.json'
MANIFEST=ROOT/'evidence/rank8_m3_20261021/pipeline/source_manifest.json'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(data):return hashlib.sha256(data).hexdigest()
def read(path):
    raw=gzip.decompress(path.read_bytes());rows=[json.loads(line.translate(str.maketrans('{}','[]')))for line in raw.decode().splitlines()if line.strip()]
    return raw,rows
def fingerprint(R):return sha(json.dumps(R,separators=(',',':')).encode())
raw,rows=read(SOURCE);oldraw,old=read(PREVIOUS);manifest=json.loads(MANIFEST.read_text())
need(sha(SOURCE.read_bytes())==manifest['source_gzip_sha256'] and sha(raw)==manifest['source_raw_sha256'],'frozen cumulative source digest')
need(len(rows)==4500 and len(old)==973,'all cumulative source records')
oldhash=[fingerprint(R)for R in old];hashes=[fingerprint(R)for R in rows]
need(len(set(hashes))==4500,'no literal duplicates')
byhash={r['tensor_sha256']:r for r in json.loads(OLD_IDS.read_text())+json.loads(CENSUS.read_text())}
need(set(byhash)==set(hashes),'every cumulative record assigned exactly one historical ID')
need([h for h in hashes if h in set(oldhash)]==oldhash,'all previous multiplicity1/2 records preserved in order')
# Optional direct repository cross-checks; the accepted local sources suffice
# for a standalone replay after this evidence is copied elsewhere.
mirrors=[]
for rel,expected in [('results/rank8/tables.txt.gz',raw),('verification/rank8/previous_M2/tables.txt.gz',oldraw)]:
    p=ROOT.parent/'fusion-ring-census'/rel
    if p.exists():
        data=gzip.decompress(p.read_bytes());need(data==expected,'upstream census repository exact raw equality')
        mirrors.append(dict(path=str(p),gzip_sha256=sha(p.read_bytes()),raw_sha256=sha(data),raw_equal=True))
x=s.Symbol('x');poly=s.Poly(x*x-42*x+16,x);K=s.QQ.algebraic_field(s.sqrt(17));root=K.unit;theta=K(21)+5*root
alpha=(K(3)+root)/2
target=[K.one,alpha,alpha,alpha+1,alpha+1,2*alpha+1,2*alpha,2*alpha+2]
def key(v):return tuple(str(co)for co in v.to_list())
targetmult=collections.Counter(map(key,target))
counts=collections.Counter();ducounts=collections.Counter();screen=[];matches=[];screen_digest=hashlib.sha256()
for line,R in enumerate(rows,1):
    h=hashes[line-1];record=byhash[h]
    need(len(R)==8 and all(len(M)==8 and all(len(r)==8 for r in M)for M in R),'rank8 tensor shape')
    need(all(type(v)is int and v>=0 for M in R for r in M for v in r),'nonnegative integer tensor')
    maximum=max(v for M in R for r in M for v in r);need(maximum in(1,2,3),'multiplicitybounded3');counts[maximum]+=1
    du=[next(j for j in range(8)if R[i][j][0])for i in range(8)];ducounts[sum(i!=du[i]for i in range(8))//2]+=1
    M=s.Matrix(8,8,lambda j,k:sum(R[i][j][k]for i in range(8)))
    need(all(v>0 for v in M),'strictlypositive regularsum matrix')
    cp=M.charpoly(x).as_poly();rem=cp.rem(poly)
    screen_digest.update((h+':'+str(tuple(rem.all_coeffs()))+'\n').encode())
    if rem.as_expr()!=0:continue
    # Exact Gaussian solve of (M-thetaI)d=0 with d_unit=1.
    A=[[K(M[i,j])-(theta if i==j else K.zero)for j in range(8)]+[K.zero]for i in range(8)]
    A.append([K(int(j==0))for j in range(8)]+[K.one]);piv=[]
    for k in range(8):
        rr=len(piv);at=next((i for i in range(rr,len(A))if A[i][k]!=K.zero),None)
        if at is None:continue
        A[rr],A[at]=A[at],A[rr];v=A[rr][k];A[rr]=[z/v for z in A[rr]]
        for i in range(len(A)):
            if i!=rr:
                z=A[i][k];A[i]=[a-z*b for a,b in zip(A[i],A[rr])]
        piv.append(k)
    need(piv==list(range(8)) and all(v==K.zero for v in A[8]),'unique normalized theta eigenvector')
    dims=[A[i][-1]for i in range(8)];dimsmatch=collections.Counter(map(key,dims))==targetmult
    screen.append(dict(id=record['id'],tensor_sha256=h,source_line=line,characteristic_polynomial=list(map(int,cp.all_coeffs())),dimension_multiset_matches=dimsmatch,
                       normalized_eigenvector=[str(s.simplify(K.to_sympy(v)))for v in dims]))
    if not dimsmatch:continue
    need(all(sum((K(R[i][j][k])*dims[k]for k in range(8)),K.zero)==dims[i]*dims[j]for i in range(8)for j in range(8)),'all exact dimension homomorphism identities')
    need(all(bool(K.to_sympy(v)>0)for v in dims),'all dimensions strictlypositive')
    need(sum((v*v for v in dims),K.zero)==K(136)+32*root,'required globaldimension')
    if 'tensor'in record:need(record['tensor']==R,'ledger exact tensor orientation')
    matches.append(dict(id=record['id'],tensor_sha256=h,multiplicity=maximum,source_line=line,
                        dimensions=[str(s.simplify(K.to_sympy(v)))for v in dims],global_dimension='136+32*sqrt(17)',duality=du,tensor=R))
need(dict(counts)=={2:877,3:3527,1:96},'complete exactmultiplicityshards')
need(dict(ducounts)=={0:2621,1:1278,2:516,3:85},'complete dualityshards')
need(len(matches)==1 and matches[0]['id']=='R8_3_721','unique census identification')
result=dict(schema='rank8-cumulative-exact-dimension-crosswalk/v1',status='PASS',scope='Exhaustive exact dimension comparison across all4500 accepted rank8 fusion rings of multiplicityatmost3; categorification is not inferred by this script.',
    target_dimension_multiset=['1','a','a','a+1','a+1','2a+1','2a','2a+2'],parameter='a=(3+sqrt(17))/2',
    eigenvalue_obstruction='sumdimensions=21+5sqrt(17), minimal polynomialx^2-42x+16',
    scanned_cumulative_records=len(rows),previous_records=len(old),exact_multiplicity_counts=dict(counts),duality_pair_counts=dict(ducounts),
    rational_polynomial_remainder_audit_sha256=screen_digest.hexdigest(),spectral_filter_survivors=screen,
    matches=matches,upstream_repository_mirrors=mirrors,
    inputs={str(p.relative_to(ROOT)):dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes()))for p in[SOURCE,PREVIOUS,CENSUS,OLD_IDS,MANIFEST]})
print(json.dumps(result,indent=2))
