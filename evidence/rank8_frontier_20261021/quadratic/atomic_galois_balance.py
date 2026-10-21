"""Exact Galois multiplicity rows for distinguished central fusion spectra.

These rows count actual central simples. They never impose integrality on
relative-twist trace variables. A successful balance test is only necessary.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter,defaultdict
from dataclasses import replace
import argparse,hashlib,json,sys
import sympy as s
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'global_induction'))
import streaming as st
from exact import discover_roots,check_roots,evaluate
from quartic_complex_character_table import QuarticComplexTable,simple_data as quartic_data
from sextic_character_table import SexticTable,simple_data as sextic_data
from rank_two_and_models import need


def coordinates(value,degree):
    out=tuple(Q(str(x))for x in reversed(value.to_list()))
    need(len(out)<=degree,'field degree mismatch')
    return out+(Q(0),)*(degree-len(out))


def automorphisms(T):
    K=T.K;d=T.degree;x=s.Symbol('x')
    p=s.Poly.from_list([s.Rational(str(c))for c in K.mod.to_list()],x)
    need(p.degree()==d and p.is_irreducible,'not a degree-d number field')
    images=discover_roots(p,K)
    need(images is not None and len(set(images))==d,'character field is not Galois')
    check_roots(p,K,images)
    basis=[K([1,0])**j for j in range(d)]
    maps=[]
    for image in images:
        matrix=tuple(coordinates(image**j,d)for j in range(d))
        for a in basis:
            for b in basis:
                need(evaluate((a*b).to_list(),image,K)==
                     evaluate(a.to_list(),image,K)*evaluate(b.to_list(),image,K),
                     'generator image does not preserve multiplication')
        maps.append(matrix)
    def act(v,M):return tuple(sum((v[j]*M[j][k]for j in range(d)),Q(0))for k in range(d))
    image_keys={coordinates(v,d)for v in images}
    need(all({act(coordinates(v,d),M)for v in images}==image_keys for M in maps),
         'automorphisms do not permute the complete generator-root set')
    return maps,{'degree':d,'field_polynomial':list(map(str,p.all_coeffs())),
                 'generator_images':[list(map(str,coordinates(v,d)))for v in images],
                 'complete_automorphism_count':len(images),
                 'basis_product_checks':d**3}


def rows_for_labels(T,column_labels,fixed):
    """Return integer rows, RHS, row labels, and exact coverage metadata."""
    K=T.K;d=T.degree;maps,field=automorphisms(T)
    fp=T.characters.index(tuple(T.ds));fixed=tuple(map(tuple,fixed))
    vectors=[]
    for label in column_labels:
        if label[0]=='low':vectors.append((tuple(label[2]),))
        elif label[0]=='high_orbit':vectors.append(tuple(map(tuple,label[2])))
        elif label[0]=='fusion_coefficient':vectors.append(())
        else:raise ValueError('unsupported integer column label')
    distinct=sorted(set(fixed)|{v for vs in vectors for v in vs})
    chars={v:tuple(sum((K(n)*x for n,x in zip(v,ch)),K.zero)for ch in T.characters)for v in distinct}
    dims={v:sum((K(n)*x for n,x in zip(v,T.ds)),K.zero)for v in distinct}
    need(all(value!=K.zero for value in dims.values()),'zero proposed central dimension')
    orbits={};rows=[];rhs=[];labels=[];reports=[];trivial=0
    def orbit(v):
        if v not in orbits:
            values={tuple(sum((v[j]*M[j][k]for j in range(d)),Q(0))for k in range(d))for M in maps}
            orbit_key=tuple(sorted(values))
            for value in values:orbits[value]=orbit_key
        return orbits[v]
    for E in range(len(T.characters)):
        if E==fp:continue
        lambdas={v:coordinates(T.beta[E]*chars[v][E]/dims[v],d)for v in distinct}
        occurrences=defaultdict(dict)
        for j,vs in enumerate(vectors):
            for value,count in Counter(lambdas[v]for v in vs).items():occurrences[value][j]=count
        constants=Counter(lambdas[v]for v in fixed)
        allorbits=sorted({orbit(value)for value in lambdas.values()})
        for values in allorbits:
            reference=values[0]
            for partner in values[1:]:
                row=[0]*len(column_labels)
                for j,count in occurrences[reference].items():row[j]+=count
                for j,count in occurrences[partner].items():row[j]-=count
                b=constants[partner]-constants[reference]
                if not any(row)and not b:trivial+=1;continue
                rows.append(tuple(row));rhs.append(b)
                labels.append(('Galois_spectral_multiplicity',E,tuple(map(str,reference)),tuple(map(str,partner))))
        reports.append({'character':E,'candidate_eigenvalue_count':len(set(lambdas.values())),
                        'complete_Galois_orbit_count':len(allorbits),
                        'orbit_sizes':[len(v)for v in allorbits],
                        'eigenvalue_assignment_sha256':st.digest([(v,lambdas[v])for v in distinct])})
    return tuple(rows),tuple(rhs),tuple(labels),{
        'field':field,'characters_checked':len(reports),'FP_character':fp,
        'restriction_vectors':len(distinct),'nontrivial_rows':len(rows),
        'identically_zero_rows_omitted':trivial,'character_reports':reports,
        'rows_sha256':st.digest(rows),'rhs_sha256':st.digest(rhs)}


def append_galois_balance(system,C,T):
    frame=system.metadata['frame_index']
    fixed=[(1,)+(0,)*7]
    if frame is not None:fixed += [C.low[j][1]for j in C.frames[frame]]
    rows,rhs,labels,report=rows_for_labels(T,system.column_labels,fixed)
    columns=tuple(tuple(col)+tuple(row[j]for row in rows)for j,col in enumerate(system.columns))
    b=tuple(system.rhs)+rhs;row_labels=tuple(system.row_labels)+labels
    h=hashlib.sha256()
    for col in columns:h.update((repr(col)+'\n').encode())
    meta={**system.metadata,'kind':'commutative_integer_Gram_S_cubic_Galois',
          'base_metadata':system.metadata,'Galois_balance':report,
          'rows':len(b),'columns_sha256':h.hexdigest(),'rhs_sha256':st.digest(b),
          'row_labels_sha256':st.digest(row_labels)}
    return replace(system,columns=columns,rhs=b,row_labels=row_labels,metadata=meta)


def control():
    R=[[[0]*8 for _ in range(8)]for _ in range(8)]
    for i in range(8):
        for j in range(8):
            a,g=divmod(i,4);b,h=divmod(j,4)
            for c in([0,1]if a==b==1 else[a+b]):R[i][j][4*c+(g+h)%4]+=1
    a={'q':5,'dimensions':[[1,0]]*4+[[s.Rational(1,2),s.Rational(1,2)]]*4,
       'global_dimension':[10,2]}
    T=QuarticComplexTable(R,a);K=T.K;fp=T.characters.index(tuple(T.ds));unit=(1,)+(0,)*7
    def column(g,u,v):
        ans=[0]*8;ans[g]=u;ans[g+4]=v;return tuple(ans)
    labels=[];counts=[]
    for E in range(8):
        if E==fp:continue
        v=unit if T.beta[E]==K.one else column(0,1,1)
        need(T.beta[E]==sum((K(n)*d for n,d in zip(v,T.ds)),K.zero),'known distinguished dimension')
        labels.append(('low',E,v));counts.append(1)
    labels.append(('high_orbit',(0,),(column(0,0,1),)));counts.append(8)
    for g in [1,2]:
        for u,v,n in [(1,0,4),(0,1,8),(1,1,4)]:
            vs=(column(g,u,v),column(4-g,u,v))if g==1 else(column(g,u,v),)
            labels.append(('high_orbit',tuple(range(len(vs))),vs));counts.append(n)
    rows,rhs,row_labels,report=rows_for_labels(T,labels,[unit])
    need(all(sum(c*x for c,x in zip(row,counts))==b for row,b in zip(rows,rhs)),
         'actual Fibonacci times Vec(C4) center violates Galois balance')
    actual=[unit]
    for label,n in zip(labels,counts):
        vs=(label[2],)if label[0]=='low'else label[2]
        actual.extend(v for v in vs for _ in range(n))
    need(len(actual)==64,'known center rank differs')
    polynomials=[];nonreal=False
    for E,ch in enumerate(T.characters):
        poly=[K.one]
        for v in actual:
            dim=sum((K(n)*d for n,d in zip(v,T.ds)),K.zero)
            eigen=T.beta[E]*sum((K(n)*z for n,z in zip(v,ch)),K.zero)/dim
            nonreal |= T.conjugate(eigen)!=eigen
            out=[K.zero]*(len(poly)+1)
            for j,c in enumerate(poly):out[j]+=c;out[j+1]-=c*eigen
            poly=out
        co=[coordinates(c,4)for c in poly]
        need(all(v[1:]==(Q(0),)*3 and v[0].denominator==1 for v in co),
             'actual center fusion characteristic polynomial not integral')
        polynomials.append([int(v[0])for v in co])
    need(nonreal,'positive control lacks nonreal modular eigenvalues')
    return {'model':'Fibonacci tensor Vec(C4)','tensor_sha256':st.digest(R),
            'actual_center_rank':64,'nonreal_modular_eigenvalues':True,
            'Galois_balance':report,'integer_multiplicities':counts,
            'column_labels':st.encode(labels),'all_eight_integer_characteristic_polynomials':polynomials}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    records=[]
    for index,cls,data in[(65,QuarticComplexTable,quartic_data),(3472,SexticTable,sextic_data)]:
        source=st.load_ring(f'R8_3_{index}');T=cls(source['tensor'],data(index));_,meta=automorphisms(T)
        records.append({'id':source['id'],'tensor_sha256':source['tensor_sha256'],'automorphisms':meta})
    files=[HERE/'quartic_complex_character_table.py',HERE/'sextic_character_table.py']
    result={'kind':'exact_atomic_Galois_spectral_balance_adapter','result':'PASS',
            'source_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest()for f in files},
            'records':records,'positive_control':control(),
            'scope':'necessary multiplicities of integer fusion-matrix spectra; no categorification claim'}
    path=HERE/'atomic_galois_balance_results.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'Galois balance control receipt changed')
    print('PASS exact Galois automorphisms and actual complex-character positive center control',flush=True)


if __name__=='__main__':main()
