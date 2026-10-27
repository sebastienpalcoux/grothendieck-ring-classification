"""Prove Galois pseudo-unitarity by exhaustive signed dimension spectra.

The global dimension of the original category is the signed scalar codegree
sum_i d_i d_{i*}, half of its sphericalization's global dimension. If every
admissible scalar character gives a Galois conjugate of the source FP global
dimension, some Galois conjugate of any categorification is pseudo-unitary.
"""
from nonzero_products import *

GATE_TARGETS=[137,1607,1976,114,128,1487,1635,1636,1959,
              500,515,516,920,1235,1372,1373,1569,1886,1975,1983]

def unique_required(source,a):
    # The scalar component API expects each irreducible codegree polynomial
    # once; multiplicities do not enter field/norm/lattice necessary tests.
    out=[]
    for p,m in list(source.cf)+list(a.cf):
        if not any(p==q for q,_ in out):out.append((p,m))
    return out

def discover_gate(R,max_seconds=240):
    start=time.time();src=chars(R);f,K,ds,D,fp_minpoly,e=src.fp()
    P=FiniteProblem(R,timeout=60000);pairs=pair_constraints(R,P);branches=[]
    while time.time()-start<max_seconds:
        result=P.check()
        if result==z3.unsat:
            return {'outcome':'galois_pseudo_unitarity','complete':True,
                    'criterion':'signed_global_dimension_spectrum',
                    'fp_global_minimal_polynomial':pc(fp_minpoly),
                    'variables':len(P.states),'equations':len(P.eqs),
                    'gauge_coordinates':P.gauge,'nonzero_pair_constraints':pairs,
                    'branches':branches,'seconds':time.time()-start}
        if result!=z3.sat:return {'outcome':'no_conclusion','complete':False,'reason':str(result),'branches':branches,'seconds':time.time()-start}
        values=P.values();T=tensor(R,P.mapping,values);why=dnumber(T)
        if why is None:
            a=chars(T);cb=[]
            for g,m in a.components:
                c=char_obstruction(a,g,unique_required(src,a));gate=None
                if c is None:
                    _,_,_,pD=a.component(g)
                    if pD==fp_minpoly:gate={'kind':'global_dimension_Galois_FP','polynomial':pc(pD)}
                cb.append({'factor':pc(g),'obstruction':c,'gate':gate})
            if any(b['obstruction'] is None and b['gate'] is None for b in cb):
                return {'outcome':'no_conclusion','complete':False,'reason':'signed global dimension outside FP orbit',
                        'branches':branches,'surviving_values':values,'surviving_characters':cb,'seconds':time.time()-start}
            why={'kind':'signed_scalar_characters_gated','characters':cb}
        branches.append({'values':values,'obstruction':why,'gauge_orbit_size':P.block_gauge_orbit(values)})
    return {'outcome':'no_conclusion','complete':False,'reason':'discovery allowance','branches':branches,'seconds':time.time()-start}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--ring');ap.add_argument('--seconds',type=int,default=240);ap.add_argument('--remaining',action='store_true')
    args=ap.parse_args();raw={r['id']:r for r in read()}
    for rid in ([args.ring]if args.ring else[f'R9_2_{i}'for i in GATE_TARGETS]):
        if args.remaining and(HERE/('gate_'+rid+'.json')).exists():continue
        r=discover_gate(raw[rid]['tensor'],args.seconds);r.update(id=rid,tensor_sha256=raw[rid]['tensor_sha256'])
        (HERE/('gate_'+rid+'.json')).write_text(json.dumps(r,indent=2)+'\n')
        print(rid,r['outcome'],len(r['branches']),round(r['seconds'],3),r.get('reason'),flush=True)
