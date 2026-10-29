"""Oriented sphericalization with the nonzero monomial necessary condition.

In the signed quotient of a sphericalization, every simple basis element has
nonzero categorical dimension. Hence every product of simple basis elements
is nonzero. We impose its degree-two instance before enumerating signed rings.
All multiplicity-two trace coordinates retain the full {-2,0,2} domain.
"""
from pathlib import Path
import sys,json,time,itertools
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
sys.path.insert(0,str(BASE/'work'))
from signed_pb import *

TARGETS=[686,690,726,728,736,1187,1241,1377,1424]

def pair_constraints(R,P):
    pairs=[]
    n=len(R)
    for i,j in itertools.product(range(1,n),repeat=2):
        # A fixed unit-output term or an odd multiplicity never vanishes.
        if R[i][j][0] or any(c%2 for c in R[i][j]):
            continue
        coords=sorted({P.mapping[i,j,k] for k in range(1,n) if R[i][j][k]})
        assert coords
        P.s.add(z3.Or(*(z3.Not(P.states[v][0]) for v in coords)))
        pairs.append({'objects':[i,j],'coordinates':coords})
    return pairs

def discover(R,spherical_report,max_seconds=240):
    start=time.time();src=chars(R);P=FiniteProblem(R,timeout=60000)
    pairs=pair_constraints(R,P)
    branches=[]
    while time.time()-start<max_seconds:
        result=P.check()
        if result==z3.unsat:
            return {'outcome':'excluded','complete':True,'criterion':'signed_nonzero_products',
                    'variables':len(P.states),'equations':len(P.eqs),
                    'gauge_coordinates':P.gauge,'nonzero_pair_constraints':pairs,
                    'branches':branches,'seconds':time.time()-start,
                    'backend':'exact_pseudo_boolean_associativity'}
        if result!=z3.sat:
            return {'outcome':'no_conclusion','complete':False,'reason':str(result),
                    'branches':branches,'seconds':time.time()-start}
        values=P.values();T=tensor(R,P.mapping,values);g=original_gauge(R,T)
        if g is not None:
            assert spherical_report['spherical_excluded']
            why={'kind':'original_gauge','signs':g,'spherical_report':spherical_report}
        else:
            why=dnumber(T)
            if why is None:
                a=chars(T);cb=[]
                for f,m in a.components:
                    cb.append({'factor':pc(f),'obstruction':char_obstruction(a,f,list(src.cf)+list(a.cf))})
                if any(b['obstruction'] is None for b in cb):
                    return {'outcome':'no_conclusion','complete':False,
                            'reason':'signed character survives','branches':branches,
                            'surviving_values':values,'surviving_characters':cb,
                            'seconds':time.time()-start}
                why={'kind':'all_signed_scalar_characters_excluded','characters':cb}
        branches.append({'values':values,'obstruction':why,
                         'gauge_orbit_size':P.block_gauge_orbit(values)})
    return {'outcome':'no_conclusion','complete':False,'reason':'discovery allowance',
            'branches':branches,'seconds':time.time()-start}

def run(rid,seconds=240):
    rows={r['id']:r for r in read()}
    pre={r['id']:r['report']for r in load('sphere_original.json')}
    r=discover(rows[rid]['tensor'],pre[rid],seconds)
    r.update(id=rid,tensor_sha256=rows[rid]['tensor_sha256'])
    (HERE/(rid+'.json')).write_text(json.dumps(r,indent=2)+'\n')
    return {'id':rid,'outcome':r['outcome'],'branches':len(r['branches']),
            'seconds':round(r['seconds'],3),'reason':r.get('reason')}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--ring');ap.add_argument('--seconds',type=int,default=240)
    args=ap.parse_args()
    targets=[args.ring] if args.ring else [f'R9_2_{i}'for i in TARGETS]
    for rid in targets:print(json.dumps(run(rid,args.seconds)),flush=True)
