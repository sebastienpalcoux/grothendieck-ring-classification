"""Lift an exact pseudo-unitary trace exclusion through every signed quotient."""
from pathlib import Path
import argparse,json,sys,time
import biquadratic_traces as bq
from scalar_sieve import ScalarCharacters,character_obstructions
from exact import require
import proofs
from oriented_signed import enumerate_all,from_values,validate_general

def sphere(R):
    a=ScalarCharacters(R);fp=a.fp()[0];branches=character_obstructions(R,a.cf)
    for (f,m),branch in zip(a.components,branches):
        if branch['obstruction'] is not None:continue
        K,ds,D,pD=a.component(f)
        branch['obstruction']={'kind':'galois_fp'} if f==fp else proofs.positive_sign_embedding(R,f,ds)
    return branches

def discover(R,pseudo,timeout=120):
    require(pseudo is not None,'missing pseudo-unitary certificate')
    bq.verify(R,pseudo)
    original=ScalarCharacters(R);original_sphere=sphere(R)
    if any(c['obstruction'] is None for c in original_sphere):
        return None,{'scope':'pseudo_unitary_only','unresolved_spherical_characters':sum(c['obstruction'] is None for c in original_sphere)}
    values,problem,stats=enumerate_all(R,timeout);branches=[]
    for value in values:
        T=from_values(R,problem,value);validate_general(T)
        branch={'values':list(value)};parity=proofs.signed_adjoint_parity(R,T);gauge=proofs.gauge_original(T,R)
        if parity is not None:branch['obstruction']=parity
        elif gauge is not None:branch['obstruction']={'kind':'gauge_original','signs':gauge}
        else:
            signed=ScalarCharacters(T)
            chars=character_obstructions(T,original.cf+signed.cf)
            if any(c['obstruction'] is None for c in chars):
                return None,{'scope':'pseudo_unitary_only','signed_count':len(values),'unresolved_signed_values':list(value),'characters':chars}
            branch['characters']=chars
        branches.append(branch)
    cert={'kind':'rank8_biquadratic_lift','scope':'general_complex_fusion_category',
          'pseudo':pseudo,'sphere':original_sphere,'branches':branches}
    return cert,{'signed_count':len(values),'spherical_components':len(original_sphere)}

def verify(R,c):
    require(c.get('kind')=='rank8_biquadratic_lift','wrong biquadratic lifting kind')
    expected,_=discover(R,c['pseudo'],timeout=1200)
    require(expected is not None and expected==c,'complete biquadratic lift did not replay')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ring',required=True);ap.add_argument('--height',type=int,default=6);ap.add_argument('--verify',action='store_true');args=ap.parse_args()
    root=Path(__file__).parent;row=next(r for r in json.loads((root.parent/'pipeline/census_m3.json').read_text()) if r['id']==args.ring)
    path=root/f'biquadratic_{args.ring}.json'
    if args.verify:verify(row['tensor'],json.loads(path.read_text())['certificate']);print(args.ring,'PASS');return
    start=time.monotonic();pseudo,report=bq.discover(row['tensor'],args.height)
    c,lift_report=discover(row['tensor'],pseudo) if pseudo else (None,None)
    out={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'scope':'general_complex_fusion_category' if c else 'attempt',
         'outcome':'excluded' if c else 'no_conclusion','certificate':c,'report':report,'lift_report':lift_report,'seconds':round(time.monotonic()-start,6)}
    path.write_text(json.dumps(out,separators=(',',':'))+'\n');print(args.ring,out['outcome'],flush=True)
if __name__=='__main__':main()
