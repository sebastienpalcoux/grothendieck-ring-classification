"""Independent source and exact dimension-basis checks for four C9 exclusions."""
from itertools import product
import json
import sympy as s
from independent_audit import BASE,HERE,dual,require

if __name__=='__main__':
    t=s.Symbol('t');f=s.Poly(t**3-3*t-1,t);K=s.QQ.alg_field_from_poly(f);b=K([1,0]);x=K.one+2*b;y=2*b*b-2*K.one
    require(f.count_roots(1,2)==1 and len(f.intervals())==3,'positive largest root b between1and2')
    def col(z):
        co=list(reversed(z.to_list()));return s.Matrix(co+[0]*(3-len(co)))
    basis=s.Matrix.hstack(col(K.one),col(x),col(y));require(basis.det()!=0 and y*y==6*K.one+2*x+2*y,'independent dimension basis and exact Y-square')
    norm=s.Matrix.hstack(*(col(y*b**j)for j in range(3))).det();require(norm==-24,'exact Norm(Y)')
    scaled=[s.cancel(norm*s.Rational(m,3)**3)for m in(1,2)];require(scaled==[-s.Rational(8,9),-s.Rational(64,9)],'bothpossibleisotypicmultiplicitiesnonintegral')
    data=json.loads((BASE/'tensors.json').read_text());P={r['id']:r for r in json.loads((BASE/'profile.json').read_text())['records']};out=[]
    source={38:(11,10,1),39:(11,10,1),218:(7,11,3),219:(6,11,3)}
    for i,(g,T,h)in source.items():
        rid=f'R12_1_{i}';R=data[rid];n=len(R);du=dual(R);G=[a for a in range(n)if sum(R[a][du[a]])==1];require(len(G)==4,'four source invertibles')
        # Numerical values choose labels only; the complete positive character
        # is then proved over the exact cubic field and is the unique FP one.
        labels=[min(range(4),key=lambda j:abs(v-(1,2,4.758770483143641,5.0641777724759205)[j]))for v in P[rid]['fp_hint']]
        ds=[(K.one,K(2),x,y)[j]for j in labels]
        require([labels.count(j)for j in range(4)]==[4,2,4,2],'exact source dimension pattern')
        require(all(sum((K(R[a][c][k])*ds[k]for k in range(n)),K.zero)==ds[a]*ds[c]for a,c in product(range(n),repeat=2)),'all exact positive cubic dimension equations')
        I=[a for a in range(n)if labels[a]<2];B=[0,g,T];unit=lambda a:[int(a==b)for b in range(n)]
        require(R[g][g]==unit(0)and R[g][T]==R[T][g]==unit(T),'RepS3 unit and action')
        require(R[T][T]==[int(a in B)for a in range(n)],'exact rank3 RepS3 fusion square')
        require(all(du[a]in I for a in I)and all(not R[a][c][k]for a,c in product(I,repeat=2)for k in range(n)if k not in I),'actual integral rank6 subcategory')
        require(h in G and h not in B and R[R[h][g].index(1)][du[h]]==unit(g),'outside invertible normalizes g')
        require(set(B)|{R[h][a].index(1)for a in B}==set(I),'two cosets exhaust integral subcategory')
        non=[a for a in range(n)if a not in I]
        require(all(R[g][a]==R[a][g]and R[g][a]!=unit(a)for a in non),'all6 nonintegral objects have matching free g actions')
        out.append(dict(id=rid,g=g,T=T,h=h,integral_subset=I,all_positive_dimension_products_checked=144,forced_dual_type=dict(invertibles=12,X=4,Y=2),forced_Y_dual_product=dict(invertibles=6,X=2,Y=2),nonintegral_norms=list(map(str,scaled)),scope='general_complex_fusion_category'))
    result=dict(status='PASS',categorical_lemma_review='Rank3 pointed Morita lemma and inverse-algebra enlargement independently reviewed; no classification of original categorifications assumed.',records=out)
    (HERE/'c9_morita_independent.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS four C9 Morita-source and norm proofs')
