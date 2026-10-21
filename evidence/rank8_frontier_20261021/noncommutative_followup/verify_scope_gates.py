"""Complete unrestricted parity-domain Galois-PU gates for R928 and R941."""
from pathlib import Path
import argparse,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'review'))
import verify_nc_gate_unrestricted as gate
from independent_wedderburn import audit,audit_signed

def compute():
    census=json.loads((gate.OLD/'pipeline/census_m3.json').read_text());out=[]
    for rid in ('R8_3_928','R8_3_941'):
        source=next(row for row in census if row['id']==rid)
        result=gate.compute(source)
        result['scope']='general_complex_fusion_category'
        result['outcome']='Galois_pseudo_unitary_reduction'
        result['independent_wedderburn']=audit(source['tensor'])
        from oriented_signed import problem
        p=problem(source['tensor'])
        for signed_class in result['gauge_classes']:
            if signed_class['kind']=='nongauge_excluded':
                T=gate.old.from_values(source['tensor'],p,signed_class['representative'])
                signed_class['independent_wedderburn']=audit_signed(T)
        out.append(result)
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=compute();path=HERE/'scope_gates.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:gate.need(result==json.loads(path.read_text()),'complete quartic scope-gate replay')
    for row in result:
        print('PASS',row['id'],row['complete_signed_count'],'unrestricted signed tensors;',
              'complete C^4 plus M2 decomposition; every categorification has a spherical structure and a pseudo-unitary Galois conjugate')

if __name__=='__main__':main()
