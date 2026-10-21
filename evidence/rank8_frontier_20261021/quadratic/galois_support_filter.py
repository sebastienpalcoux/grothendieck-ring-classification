"""Exact missing-conjugate support elimination before cubic assembly.

If an eigenvalue occurs with positive multiplicity in an integer matrix,
every Galois conjugate occurs. A missing conjugate forces the entire
nonnegative column containing that eigenvalue to zero. Iterate to closure.
"""
from pathlib import Path
from types import SimpleNamespace
from fractions import Fraction as Q
import argparse,hashlib,json
from atomic_galois_balance import automorphisms,coordinates,st,need,control as known_center
from atomic_spectrum import AtomicSpectrum,table_for
HERE=Path(__file__).resolve().parent


def filter_support(C,T):
    K=T.K;d=T.degree;maps,field=automorphisms(T)
    fp=T.characters.index(tuple(T.ds));labels=C.meta['low_character_labels']
    lows=[(labels[g],tuple(v))for g,v,z in C.low]
    vectors=[(v,)for E,v in lows]
    vectors += [tuple((0,)+tuple(C.a['high'][j][0])for j in orbit)for orbit in C.orbits]
    unit=(1,)+(0,)*7;distinct=sorted({unit}|{v for vs in vectors for v in vs})
    dims={v:sum((K(n)*x for n,x in zip(v,T.ds)),K.zero)for v in distinct}
    need(all(z!=K.zero for z in dims.values()),'zero candidate dimension')
    values={};members={};fixed={};orbit_cache={}
    def orbit(key):
        if key not in orbit_cache:
            out=tuple(sorted({tuple(sum((key[j]*M[j][k]for j in range(d)),Q(0))for k in range(d))for M in maps}))
            for v in out:orbit_cache[v]=out
        return orbit_cache[key]
    for E,ch in enumerate(T.characters):
        if E==fp:continue
        ev={v:coordinates(T.beta[E]*sum((K(n)*x for n,x in zip(v,ch)),K.zero)/dims[v],d)for v in distinct}
        values[E]=[tuple(ev[v]for v in vs)for vs in vectors]
        fixed[E]=ev[unit];lookup={}
        for j,vs in enumerate(values[E]):
            for value in vs:lookup.setdefault(value,set()).add(j)
        members[E]=lookup
        for value in ev.values():orbit(value)
    active=set(range(len(vectors)));rounds=[];obstruction=None
    while True:
        present={E:{fixed[E]}|{v for j in active for v in values[E][j]}for E in values}
        removed=set();witnesses=[]
        for E in values:
            for value in sorted(present[E]):
                missing=next((v for v in orbit(value)if v not in present[E]),None)
                if missing is None:continue
                witness={'character':E,'eigenvalue':list(map(str,value)),
                         'missing_conjugate':list(map(str,missing))}
                if fixed[E]==value:
                    obstruction={'kind':'fixed_unit_spectrum_missing_conjugate',**witness};break
                forced=sorted((members[E].get(value,set())&active)-removed)
                if forced:
                    witnesses.append({**witness,'forced_zero_columns':forced});removed.update(forced)
            if obstruction:break
        if obstruction:break
        if not removed:break
        rounds.append({'active_columns_before':len(active),
                       'present_eigenvalues_sha256':st.digest({E:sorted(v)for E,v in present.items()}),
                       'witnesses':witnesses,'forced_zero_count':len(removed)})
        active-=removed
        for E in labels:
            if not any(j in active and G==E for j,(G,v)in enumerate(lows)):
                obstruction={'kind':'empty_distinguished_character_domain','character':E};break
        if obstruction:break
    keep_low=[j for j in range(len(lows))if j in active]
    keep_high=[j for j in range(len(C.orbits))if j+len(lows)in active]
    report={'kind':'exact_missing_Galois_conjugate_support_elimination',
            'tensor_sha256':st.digest(C.R),'original_atomic_domain':C.meta,'field':field,
            'original_low_columns':len(lows),'original_high_orbits':len(C.orbits),
            'complete_candidate_column_sha256':st.digest([lows,C.orbits,vectors]),
            'rounds':rounds,'retained_low_indices':keep_low,'retained_high_orbit_indices':keep_high,
            'retained_low_columns':len(keep_low),'retained_high_orbits':len(keep_high),
            'outcome':'necessary_support_obstruction'if obstruction else'necessary_support_survives'}
    if obstruction:report['obstruction']=obstruction
    # Deliberately expose only the data API used by the integer constructor:
    # this filtered object must not be mistaken for a valid old phase cone.
    out=SimpleNamespace(R=C.R,a=C.a,low=[C.low[j]for j in keep_low],
                        orbits=[C.orbits[j]for j in keep_high],meta={**C.meta,'Galois_support_filter_sha256':st.digest(report)})
    return out,report


def control():
    import sympy as s
    R=[[[0]*8 for _ in range(8)]for _ in range(8)]
    for i in range(8):
        for j in range(8):
            a,g=divmod(i,4);b,h=divmod(j,4)
            for c in([0,1]if a==b==1 else[a+b]):R[i][j][4*c+(g+h)%4]+=1
    C=AtomicSpectrum(R,4);T=table_for(R,C.a);filtered,report=filter_support(C,T)
    need(report['outcome']=='necessary_support_survives','known actual center support excluded')
    actual=known_center()['column_labels'];groups=C.meta['low_character_labels']
    retained_low={(groups[g],tuple(v))for g,v,z in filtered.low}
    retained_high={frozenset((0,)+tuple(C.a['high'][j][0])for j in orbit)for orbit in filtered.orbits}
    for label in actual:
        if label[0]=='low':need((label[1],tuple(label[2]))in retained_low,'known distinguished restriction removed')
        else:need(frozenset(map(tuple,label[2]))in retained_high,'known high restriction orbit removed')
    return {'model':'Fibonacci tensor Vec(C4)','all_actual_center_supports_retained':True,'report':report}


def target(index):
    source=st.load_ring(f'R8_3_{index}');C=AtomicSpectrum(source['tensor'],4)
    old=json.loads((HERE.parent/'global_induction/atomic_spectrum_results'/f'R8_3_{index}_h4.json').read_text())
    need(C.meta==old['metadata']and old['tensor_sha256']==source['tensor_sha256'],'original complete atomic domain differs')
    T=table_for(source['tensor'],C.a);_,report=filter_support(C,T)
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ring',type=int,choices=[65,3472]);p.add_argument('--write',action='store_true');args=p.parse_args()
    result=target(args.ring)if args.ring else control()
    suffix=str(args.ring)if args.ring else'control';path=HERE/f'galois_support_{suffix}_results.json'
    if args.write:path.write_text(json.dumps(st.encode(result),indent=2)+'\n')
    else:need(st.encode(result)==json.loads(path.read_text()),'Galois support replay differs')
    report=result if args.ring else result['report']
    print('PASS Galois support',suffix,report['outcome'],report['retained_low_columns'],report['retained_high_orbits'],flush=True)


if __name__=='__main__':main()
