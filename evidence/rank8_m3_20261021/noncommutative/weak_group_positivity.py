"""Promote a unitary obstruction only through a proved weak-group gate."""
from pathlib import Path
import argparse,json,sys
import sympy as s
from scalar_sieve import ScalarCharacters
from exact import require,ec
import unitary_primary3
HERE=Path(__file__).resolve().parent

def integral_value(x):
    values=ec(x)
    if len(values)>1:return None
    z=s.Rational(values[0]) if values else s.S.Zero
    return int(z) if z.q==1 else None

def gate(R):
    a=ScalarCharacters(R);f,K,ds,D,pD,emb=a.fp();d=integral_value(D)
    if d is None or d<=0:return None
    if d<84:return {'kind':'dimension_below_84','dimension':d}
    if len(s.factorint(d))<=2:return {'kind':'two_prime_dimension','dimension':d}
    neutral=[i for i,x in enumerate(ds) if integral_value(x) is not None]
    if len(neutral)==len(R):return None
    N=set(neutral);degree=[int(i not in N) for i in range(len(R))]
    if any((degree[i]+degree[j]-degree[k])%2 for i in range(len(R)) for j in range(len(R)) for k in range(len(R)) if R[i][j][k]):return None
    D0=sum((ds[i]*ds[a.du[i]] for i in neutral),K.zero);d0=integral_value(D0)
    if d0 is None or 2*d0!=d or d0>=84:return None
    return {'kind':'faithful_C2_extension_of_dimension_below_84','dimension':d,'neutral_dimension':d0,'neutral_basis':neutral,'degrees':degree}

def verify(R,c):
    require(c.get('kind')=='weak_group_unitarity_lift','wrong gate certificate')
    g=gate(R);require(g is not None and g==c['gate'],'weak-group-theoretical reduction failed')
    unitary_primary3.verify(R,c['unitary_certificate'])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    census={r['id']:r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text())};path=HERE/'lifted_results.json'
    if not args.write:
        for row in json.loads(path.read_text()):verify(census[row['id']]['tensor'],row['certificate'])
        print('PASS: exact weak-group unitarity lifts');return
    rows=json.loads((HERE/'unitary_primary3_results.json').read_text());out=[]
    for r in rows:
        if not r.get('certificate'):continue
        R=census[r['id']]['tensor'];g=gate(R)
        if g is None:continue
        c={'kind':'weak_group_unitarity_lift','gate':g,'unitary_certificate':r['certificate']};verify(R,c)
        out.append({'id':r['id'],'tensor_sha256':census[r['id']]['tensor_sha256'],'scope':'general_complex_fusion_category','outcome':'excluded','certificate':c})
    path.write_text(json.dumps(out,separators=(',',':'))+'\n');print('PASS',len(out),[r['id'] for r in out])
if __name__=='__main__':main()
