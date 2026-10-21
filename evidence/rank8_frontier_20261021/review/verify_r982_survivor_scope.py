#!/usr/bin/env python3
"""Direct full-equation witnesses and all-indicator selected-pattern negatives."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,hashlib,itertools,json,math,sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=BASE.parents[1]
sys.path.insert(0,str(BASE/'commutative_integer'));sys.path.insert(0,str(BASE/'quadratic_atomic_integer'))
import r982 as source
from unit_pair_constraints import append_unit_pair_constraints
from fp_fusion_bounds import tighten_fusion_bounds

def need(ok,msg):
    if not ok:raise ValueError(msg)

def check_equations(S,values,integer):
    need(len(values)==len(S.columns),'full original witness size')
    need(all(0<=x<=u and(not integer or x.denominator==1)for x,u in zip(values,S.bounds)),'every original finite bound')
    total=[F(0)]*len(S.rhs)
    for x,col in zip(values,S.columns):
        if x:
            for i,a in enumerate(col):
                if a:total[i]+=x*a
    need(total==list(S.rhs),'every full original necessary equation')

def compute():
    folder=BASE/'commutative_integer';ring=source.st.load_ring('R8_3_982');R=ring['tensor'];C=source.cg.cone(R,4,'sts_frame');T=source.character_table(R,C.a)
    need(len(C.frames)==4,'complete four frame domain');profile=json.loads((folder/'R8_3_982_profile.json').read_text());rational=json.loads((folder/'R8_3_982_rational.json').read_text());records=[]
    eps=list(map(list,source.st.old.ht.indicator_choices(R)));need(len(eps)==8,'complete indicator domain')
    dual=[next(j for j in range(8)if R[i][j][0])for i in range(8)]
    for fi in range(4):
        D,filtermeta=source.filtered(C,fi);S=source.f.build(D,T,frame_index=fi);S=source.append_galois_balance(S,D,T);S=tighten_fusion_bounds(S,D,T)
        old=json.loads((folder/f'R8_3_982_frame{fi}.json').read_text());need(old['metadata']==S.metadata and old['profile']==filtermeta,'original full system binding')
        print('982 independent reconstructed frame',fi,len(S.rhs),len(S.columns),flush=True)
        rec={'frame_index':fi}
        if fi<2:
            S=append_unit_pair_constraints(S,D,T);saved=rational['records'][fi]
            need(S.metadata==saved['metadata'],'strengthened rational full system binding');values=list(map(F,saved['original_values']))
            check_equations(S,values,False);rec.update(outcome='exact_bounded_rational_survivor_only',rows=len(S.rhs),columns=len(S.columns));records.append(rec);continue
        values=list(map(F,old['original_integer_witness']));check_equations(S,values,True)
        p=profile['records'][fi];low=[tuple(v)for v in p['low_columns']];labels=p['character_labels'];lowmap=dict(zip(labels,low));fp=S.metadata['FP_character'];Es=[E for E in range(8)if E!=fp]
        need(low==[(1,)+(0,)*7]+[tuple(C.low[j][1])for j in C.frames[fi]],'fixed low restrictions')
        fusion={tuple(label[1:]):n for label,n in zip(S.column_labels,values)if label[0]=='fusion_coefficient'}
        dualE=S.metadata['dual_characters']
        for E,H in itertools.combinations_with_replacement(Es,2):
            need(sum(fusion[E,H,G]for G in Es)+int(H==dualE[E])==sum(lowmap[E][i]*lowmap[H][dual[i]]for i in range(8)),'all28 source-unit product identities')
        # Direct joint tuple multiset, with each duality member counted once.
        def tup(v):
            dim=sum((T.K(n)*d for n,d in zip(v,T.ds)),T.K.zero)
            return tuple(T.beta[E]*sum((T.K(n)*x for n,x in zip(v,T.characters[E])),T.K.zero)/dim for E in Es)
        counts=Counter(tup(v)for v in low)
        for label,n in zip(S.column_labels,values):
            if label[0]=='high_orbit' and n:
                for v in label[2]:counts[tup(v)]+=int(n)
        z=T.K([1,0]);need(T.K.mod.to_list()==list(map(int,source.s.Poly(source.s.cyclotomic_poly(24)).all_coeffs())),'full cyclotomic character field')
        for exponent in range(1,24):
            if math.gcd(exponent,24)!=1:continue
            def gal(a):
                out=T.K.zero
                for c in a.to_list():out=out*z**exponent+T.K(c)
                return out
            transformed=Counter()
            for t,n in counts.items():transformed[tuple(gal(a)for a in t)]+=n
            need(transformed==counts,'all full simultaneous Galois multiplicities')
        # Independently rebuild the fixed-mass phase domain from full vectors.
        orbit_lookup={tuple(sorted((0,)+tuple(C.a['high'][j][0])for j in orbit)):i for i,orbit in enumerate(C.orbits)}
        masses=[]
        for label,n in zip(S.column_labels,values):
            if label[0]=='high_orbit'and n:masses.append((orbit_lookup[tuple(sorted(label[2]))],int(n)))
        active=[];massrow={}
        for k,(oi,n)in enumerate(masses):
            for ti in range(C.nt):massrow[len(active)]=k;active.append(C.offset+oi*C.nt+ti)
        active.extend(range(C.high_end,C.nvars));columns=[C.column(j)for j in active];fixed=C.column(fi)
        phase=json.loads((folder/f'R8_3_982_frame{fi}_phases_h4.json').read_text());pm=phase['metadata']
        need(pm['source_phase_metadata']==C.meta and pm['masses']==[list(v)for v in masses]and pm['active_global_indices_sha256']==source.st.digest(active),'complete fixed-mass operator binding')
        need(phase['status']=='selected_integer_pattern_phase_incompatible'and[at['indicators']for at in phase['attempts']]==eps,'all eight selected-pattern indicator branches')
        rays={}
        for attempt in phase['attempts']:
            ray=tuple(attempt['certificate']['covector']);rhs=[x-fixed.get(i,0)for i,x in enumerate(C.rhs_for(attempt['indicators']))]+[n for oi,n in masses]
            need(len(ray)==len(rhs),'full phase covector size')
            if ray not in rays:
                vals=[sum(ray[i]*v for i,v in col.items())+(ray[C.nrows+massrow[j]]if j in massrow else 0)for j,col in enumerate(columns)]
                need(all(v>=0 for v in vals),'every complete fixed-pattern phase column inequality');rays[ray]=True
            need(sum(x*y for x,y in zip(ray,rhs))==attempt['certificate']['rhs_value']<0,'strict exact original RHS pairing')
        rec.update(outcome='exact_integer_joint_and_unit_product_survivor_but_selected_phase_pattern_excluded',rows=len(S.rhs),columns=len(S.columns),
            source_unit_pairs=28,joint_Galois_automorphisms=8,phase_indicator_branches=8,distinct_phase_rays=len(rays),phase_columns=len(active));records.append(rec)
    names=['r982.py','r982_joint_probe.py','r982_unit_pair_probe.py','r982_phases.py','r982_rational.py','R8_3_982_profile.json','R8_3_982_rational.json']+[f'R8_3_982_frame{j}.json'for j in range(4)]+[f'R8_3_982_frame{j}_phases_h4.json'for j in(2,3)]
    files=[Path(__file__),HERE/'commutative_integer_control_review.json']+[folder/n for n in names]
    return {'kind':'independent_R982_exact_survivor_and_selected_phase_scope_review','status':'exact_complete','records':records,
        'scope':'frames0/1 rational relaxation survivors; frames2/3 selected integer witnesses incompatible with phases; no source-ring exclusion',
        'files_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();actual=compute();path=HERE/'r982_survivor_scope_review.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'R982 target review differs')
    print('PASS982 four full witness domains;two selected integer patterns fail all eight phase branches;ring remains open')
