"""Scoped exact construction filters for the forced R941 fermionic quotient."""
from pathlib import Path
import argparse,hashlib,itertools,json
import sympy as s
import source,r941_fermionic
HERE=Path(__file__).resolve().parent;need=source.need

def run():
    branch=json.loads(json.dumps(r941_fermionic.run(),default=int))
    need(branch==json.loads((HERE/'r941_fermionic.json').read_text()),'exact quotient source replay')
    Q=branch['bosonic_branch']['quotient_tensor'];subrings=[]
    for mask in range(8):
        J=[0]+[i for i in range(1,4)if mask&(1<<(i-1))]
        if all(not Q[i][j][k]for i in J for j in J for k in range(4)if k not in J):subrings.append(J)
    need(subrings==[[0],[0,1,2,3]],'complete quotient fusion-subring domain')
    x=s.symbols('x');D=72+48*s.sqrt(2)+40*s.sqrt(3)+28*s.sqrt(6)
    poly=s.Poly(s.minpoly(D,x),x);need(poly.degree()==4 and poly.is_irreducible,'quartic quotient dimension')
    families=[]
    for n,radical in[(6,15),(8,6)]:
        d=(n+s.sqrt(n*n+4*n))/2;nearD=s.expand(n+d*d)
        need(s.Poly(s.minpoly(nearD,x),x).degree()==2,'specified near-group source quadratic dimension')
        need(s.Poly(s.minpoly(nearD**2,x),x).degree()==2,'specified center quadratic dimension')
        families.append({'type':f'near_group_order_{n}_multiplicity_{n}','source_global_dimension':str(nearD),
            'center_global_dimension':str(s.expand(nearD**2)),'dimension_field':f'Q(sqrt({radical}))',
            'outcome':'every_rational_rescaling_of_these_center_dimensions_differs_from_quartic_target'})
    return {'id':branch['id'],'tensor_sha256':branch['tensor_sha256'],
        'quotient_receipt_sha256':hashlib.sha256((HERE/'r941_fermionic.json').read_bytes()).hexdigest(),
        'quotient_rank':4,'quotient_simple_types':['m','m','m','m'],
        'all_unit_containing_subsets_tested':8,'all_quotient_fusion_subrings':subrings,
        'direct_tensor_products_of_two_rank_two_supercategories':'excluded_by_all_m_type_and_absence_of_rank_two_subring',
        'quotient_global_dimension_polynomial':list(map(int,poly.all_coeffs())),
        'specified_near_group_center_families':families,
        'primary_sources':[{'url':'https://arxiv.org/abs/1709.01941','locator':'Section4.1.3, with free fermion action giving m-type orbit simples'},
            {'url':'https://arxiv.org/abs/2208.02757','locator':'Section3 and AppendixE; rank-two computations cover stated low multiplicities, completeness beyond them is conjectural'},
            {'url':'https://arxiv.org/abs/2305.09108','locator':'Introduction theorem(a),(b): centers of types C6+6 and C2xC4+8, pointed-factor removal and bosonic condensation'}],
        'scope':'specified direct super tensor-product and published near-group-center constructions only',
        'limitation':'No classification of general rank-four superfusion categories, arbitrary superalgebra condensations, or mixed construction chains is asserted.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    actual=json.loads(json.dumps(run(),default=int));path=HERE/'r941_super_constructions.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'scoped super construction receipt differs')
    print('PASS941: all rank2-by-rank2 super products and specified published near-group-center dimension routes excluded; general superfusion problem open.')
