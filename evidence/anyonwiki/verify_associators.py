"""Replay published associators over exact cyclotomic fields, without solving equations."""
import itertools,json,re,hashlib
from pathlib import Path
import sympy as s
from sympy import QQ
from sympy.polys.matrices import DomainMatrix
def sha(R):return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
def signatures(R):
 n=len(R);du=[next(j for j in range(n) if R[i][j][0])for i in range(n)]
 return [(i==0,du[i]==i,tuple(sorted(v for row in R[i] for v in row)),tuple(sorted(R[i][i])),sum(R[i][j][j]for j in range(n)))for i in range(n)]
def iso(A,B):
 n=len(A);sa,sb=signatures(A),signatures(B)
 if sorted(sa)!=sorted(sb):return None
 opts=[[j for j in range(n) if sa[i]==sb[j]]for i in range(n)]
 order=sorted(range(n),key=lambda i:len(opts[i]));p=[None]*n
 def rec(t):
  if t==n:return list(p)
  i=order[t]
  for j in opts[i]:
   if j in p:continue
   p[i]=j;inds=[x for x in range(n)if p[x]is not None]
   if all(A[a][b][c]==B[p[a]][p[b]][p[c]] for a in inds for b in inds for c in inds):
    answer=rec(t+1)
    if answer is not None:return answer
   p[i]=None
  return None
 return rec(0)



HERE=Path(__file__).resolve().parent
SOURCES=HERE/'symbolic'

def check(code,conductor):
    path=SOURCES/('cat_'+code+'.jl')
    raw=path.read_text();x=s.Symbol('x')
    K=QQ.alg_field_from_poly(s.Poly(s.cyclotomic_poly(conductor,x),x))
    F={}
    for labels,coeffs in re.findall(r'\[([\d, ]+)\]\s*=>\s*QQFieldElem\[([^\]]+)\]',raw):
        key=tuple(int(z.strip())-1 for z in labels.split(','))
        value=K([QQ(z.strip().replace('//','/')) for z in reversed(coeffs.split(','))])
        assert key not in F
        F[key]=value
    n=7;R=[[[0]*n for j in range(n)]for i in range(n)]
    for a,b,c,d,e,f in F:
        if a==0:
            assert e==b and f==d and F[a,b,c,d,e,f]==K.one
            R[b][c][d]=1
    support=[[tuple(k for k in range(n)if R[i][j][k])for j in range(n)]for i in range(n)]
    expected=set();blocks=0
    for a,b,c,d in itertools.product(range(n),repeat=4):
        left=[e for e in support[a][b]if R[e][c][d]]
        right=[f for f in support[b][c]if R[a][f][d]]
        assert len(left)==len(right)
        if not left:continue
        for e,f in itertools.product(left,right):expected.add((a,b,c,d,e,f))
        matrix=DomainMatrix([[F[a,b,c,d,e,f]for f in right]for e in left],(len(left),len(right)),K)
        assert matrix.det()!=K.zero,('singular',a,b,c,d)
        blocks+=1
    assert set(F)==expected,('inadmissible or missing symbols',len(F),len(expected))
    for a,b,c,d,e,f in expected:
        if 0 in (a,b,c):assert F[a,b,c,d,e,f]==K.one
    du=[next(j for j in range(n)if R[i][j][0])for i in range(n)]
    assert all(F[i,du[i],i,i,0,0]!=K.zero for i in range(n))
    equations=0
    for a,b,c,d in itertools.product(range(n),repeat=4):
        for e in support[a][b]:
            for p in support[e][c]:
                for q in support[p][d]:
                    for l in support[c][d]:
                        for k in support[b][l]:
                            if not R[a][k][q]:continue
                            lhs=K.zero
                            for h in support[b][c]:
                                if not R[a][h][p] or not R[h][d][k]:continue
                                lhs+=F[a,b,c,p,e,h]*F[a,h,d,q,p,k]*F[b,c,d,k,h,l]
                            rhs=K.zero
                            if R[e][l][q]:rhs=F[e,c,d,q,p,l]*F[a,b,l,q,e,k]
                            assert lhs==rhs,('pentagon',a,b,c,d,e,p,q,l,k)
                            equations+=1
    crosswalk=json.loads((HERE/'crosswalk.json').read_text())['matches']
    wiki_id='FR_'+'_'.join(code.split('_')[:4])
    match=next(z for z in crosswalk if z['match']['wiki_id']==wiki_id)
    perm=iso(match['match']['tensor'],R);assert perm is not None
    result=dict(category_code=[int(t)for t in code.split('_')],census_id=match['census_id'],
                conductor=conductor,field_polynomial=s.Poly(s.cyclotomic_poly(conductor,x),x).all_coeffs(),
                f_symbols=len(F),invertible_blocks=blocks,pentagon_equations=equations,
                unit_constraints=True,rigidity_nonzero_constraints=True,
                symbolic_file_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),wiki_to_associator_basis=perm,
                tensor=R,tensor_sha256=sha(R))
    result['field_polynomial']=list(map(int,result['field_polynomial']))
    return result

if __name__=='__main__':
    results=[]
    for code,conductor in [('7_1_2_3_1_0_1',8),('7_1_2_12_1_0_1',28),('7_1_4_3_1_0_1',16)]:
        r=check(code,conductor);results.append(r)
        print({k:v for k,v in r.items()if k not in ('tensor','field_polynomial')},flush=True)
    (HERE/'associator_report.json').write_text(json.dumps({'status':'PASS','exact':True,'results':results},indent=2)+'\n')
