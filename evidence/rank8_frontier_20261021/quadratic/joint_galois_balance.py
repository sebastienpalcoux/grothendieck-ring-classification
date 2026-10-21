"""Joint Galois multiplicities of commuting distinguished center matrices.

An integer linear combination can separate the finite union of all joint
eigenvalue tuples and their conjugates. Its integral characteristic
polynomial therefore forces equality of complete-tuple multiplicities.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter,defaultdict
from dataclasses import replace
from types import SimpleNamespace
import argparse,hashlib,json
from atomic_galois_balance import automorphisms,coordinates,st,need,control as actual_control
from quartic_complex_character_table import QuarticComplexTable
HERE=Path(__file__).resolve().parent


def data(T,column_labels,fixed):
    K=T.K;d=T.degree;maps,field=automorphisms(T)
    fp=T.characters.index(tuple(T.ds));Es=[E for E in range(len(T.characters))if E!=fp]
    vectors=[]
    for label in column_labels:
        if label[0]=='low':vectors.append((tuple(label[2]),))
        elif label[0]=='high_orbit':vectors.append(tuple(map(tuple,label[2])))
        elif label[0]=='fusion_coefficient':vectors.append(())
        else:raise ValueError('unsupported joint spectral column')
    fixed=tuple(map(tuple,fixed));distinct=sorted(set(fixed)|{v for vs in vectors for v in vs})
    values={}
    for v in distinct:
        dim=sum((K(n)*z for n,z in zip(v,T.ds)),K.zero);need(dim!=K.zero,'zero central dimension')
        values[v]=tuple(coordinates(T.beta[E]*sum((K(n)*z for n,z in zip(v,T.characters[E])),K.zero)/dim,d)for E in Es)
    transformed={};orbit_cache={}
    def conjugate(value,g):
        key=(value,g)
        if key not in transformed:
            M=maps[g];transformed[key]=tuple(sum((value[j]*M[j][k]for j in range(d)),Q(0))for k in range(d))
        return transformed[key]
    def orbit(value):
        if value not in orbit_cache:
            out=tuple(sorted({tuple(conjugate(x,g)for x in value)for g in range(d)}))
            for x in out:orbit_cache[x]=out
        return orbit_cache[value]
    by_column=[tuple(values[v]for v in vs)for vs in vectors]
    constants=Counter(values[v]for v in fixed)
    all_orbits=tuple(sorted({orbit(value)for value in values.values()}))
    report={'field':field,'characters':Es,'FP_character':fp,'restriction_vectors':len(distinct),
            'joint_candidate_eigenvalues':len(set(values.values())),
            'complete_joint_orbits':len(all_orbits),'orbit_sizes':[len(v)for v in all_orbits],
            'joint_assignments_sha256':st.digest([(v,values[v])for v in distinct])}
    return by_column,constants,orbit_cache,all_orbits,report


def rows_for_labels(T,column_labels,fixed):
    columns,constants,orbits,all_orbits,report=data(T,column_labels,fixed)
    occurrences=defaultdict(dict)
    for j,values in enumerate(columns):
        for value,n in Counter(values).items():occurrences[value][j]=n
    rows=[];rhs=[];labels=[];zero=0
    for values in all_orbits:
        first=values[0]
        for other in values[1:]:
            row=[0]*len(columns)
            for j,n in occurrences[first].items():row[j]+=n
            for j,n in occurrences[other].items():row[j]-=n
            b=constants[other]-constants[first]
            if not any(row)and not b:zero+=1;continue
            rows.append(tuple(row));rhs.append(b)
            labels.append(('joint_Galois_multiplicity',st.digest(first),st.digest(other)))
    report={**report,'rows':len(rows),'trivial_rows_omitted':zero,
            'rows_sha256':st.digest(rows),'rhs_sha256':st.digest(rhs)}
    return tuple(rows),tuple(rhs),tuple(labels),report


def append_joint_balance(system,C,T):
    fixed=[(1,)+(0,)*7];frame=system.metadata['frame_index']
    if frame is not None:fixed += [C.low[j][1]for j in C.frames[frame]]
    rows,rhs,labels,report=rows_for_labels(T,system.column_labels,fixed)
    columns=tuple(tuple(col)+tuple(row[j]for row in rows)for j,col in enumerate(system.columns))
    b=tuple(system.rhs)+rhs;row_labels=tuple(system.row_labels)+labels
    h=hashlib.sha256()
    for col in columns:h.update((repr(col)+'\n').encode())
    meta={**system.metadata,'kind':'commutative_integer_with_joint_Galois_balance',
          'pre_joint_metadata':system.metadata,'joint_Galois_balance':report,
          'rows':len(b),'columns_sha256':h.hexdigest(),'rhs_sha256':st.digest(b),
          'row_labels_sha256':st.digest(row_labels)}
    return replace(system,columns=columns,rhs=b,row_labels=row_labels,metadata=meta)


def filter_support(C,T):
    groups=C.meta['low_character_labels'];labels=[('low',groups[g],tuple(v))for g,v,z in C.low]
    labels += [('high_orbit',tuple(orbit),tuple((0,)+tuple(C.a['high'][j][0])for j in orbit))for orbit in C.orbits]
    columns,constants,orbits,all_orbits,field=data(T,labels,[(1,)+(0,)*7])
    members=defaultdict(set)
    for j,values in enumerate(columns):
        for value in values:members[value].add(j)
    active=set(range(len(columns)));rounds=[];obstruction=None
    while True:
        present=set(constants)|{v for j in active for v in columns[j]};removed=set();witnesses=[]
        for value in sorted(present):
            missing=next((v for v in orbits[value]if v not in present),None)
            if missing is None:continue
            witness={'joint_value':st.encode(value),'missing_joint_conjugate':st.encode(missing)}
            if constants[value]:obstruction={'kind':'fixed_joint_spectrum_missing_conjugate',**witness};break
            forced=sorted((members[value]&active)-removed)
            if forced:witnesses.append({**witness,'forced_zero_columns':forced});removed.update(forced)
        if obstruction or not removed:break
        rounds.append({'active_before':len(active),'witnesses':witnesses,'forced_zero_count':len(removed)})
        active-=removed
        for E in groups:
            if not any(j in active and label[1]==E for j,label in enumerate(labels[:len(C.low)])):
                obstruction={'kind':'empty_distinguished_domain','character':E};break
        if obstruction:break
    low=[j for j in range(len(C.low))if j in active];high=[j for j in range(len(C.orbits))if len(C.low)+j in active]
    report={'kind':'exact_joint_Galois_support_elimination','tensor_sha256':st.digest(C.R),
            'source_domain':C.meta,'field':field,'column_labels_sha256':st.digest(labels),
            'original_low':len(C.low),'original_high_orbits':len(C.orbits),
            'rounds':rounds,'retained_low_indices':low,'retained_high_orbit_indices':high,
            'retained_low':len(low),'retained_high_orbits':len(high),
            'outcome':'joint_support_obstruction'if obstruction else'joint_support_survives'}
    if obstruction:report['obstruction']=obstruction
    D=SimpleNamespace(R=C.R,a=C.a,low=[C.low[j]for j in low],orbits=[C.orbits[j]for j in high],
                      meta={**C.meta,'joint_support_filter_sha256':st.digest(report)})
    return D,report


def control():
    actual=actual_control();labels=actual['column_labels'];counts=actual['integer_multiplicities']
    from review_cm_real_sts import fib_group
    import sympy as s
    R=fib_group(True);a={'q':5,'dimensions':[[1,0]]*4+[[s.Rational(1,2),s.Rational(1,2)]]*4,'global_dimension':[10,2]}
    T=QuarticComplexTable(R,a);unit=(1,)+(0,)*7
    rows,rhs,_,report=rows_for_labels(T,labels,[unit])
    need(all(sum(n*x for n,x in zip(counts,row))==b for row,b in zip(rows,rhs)),'actual center violates joint Galois balance')
    # Explicitly check that every conjugate complete tuple has equal count.
    cols,fixed,orbits,all_orbits,_=data(T,labels,[unit]);multiplicity=Counter(fixed)
    for n,values in zip(counts,cols):
        for value in values:multiplicity[value]+=n
    need(sum(multiplicity.values())==64,'actual center rank differs')
    need(all(len({multiplicity[value]for value in orbit})==1 for orbit in all_orbits),'actual tuple orbit multiplicities differ')
    from atomic_spectrum import AtomicSpectrum,table_for
    C=AtomicSpectrum(R,4);D,support=filter_support(C,table_for(R,C.a))
    need(support['outcome']=='joint_support_survives','actual center eliminated')
    low={(C.meta['low_character_labels'][g],tuple(v))for g,v,z in D.low}
    high={frozenset((0,)+tuple(C.a['high'][j][0])for j in orbit)for orbit in D.orbits}
    for label in labels:
        if label[0]=='low':need((label[1],tuple(label[2]))in low,'actual low removed')
        else:need(frozenset(map(tuple,label[2]))in high,'actual high removed')
    return {'kind':'joint_Galois_balance_actual_center_control','model':'Fibonacci tensor Vec(C4)',
            'tensor_sha256':st.digest(R),'actual_center_rank':64,'all_joint_orbit_multiplicities_equal':True,
            'rows':report,'support_filter':support,
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [HERE/'atomic_galois_balance.py',HERE/'quartic_complex_character_table.py']}}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');a=p.parse_args()
    result=control();path=HERE/'joint_galois_balance_results.json'
    if a.write:path.write_text(json.dumps(st.encode(result),indent=2)+'\n')
    else:need(st.encode(result)==json.loads(path.read_text()),'joint Galois control differs')
    print('PASS joint Galois tuples and actual 64-simple center control',flush=True)


if __name__=='__main__':main()
