"""General R567 exclusion by a complete integer-center cubic obstruction.

The default read-only replay reconstructs every low/high domain, two
independent integer Gram enumerations, duality, and all 155 cubic values.
It performs no numerical optimization.
"""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json
import source,gram,cubic
HERE=Path(__file__).resolve().parent;FRONTIER=HERE.parent;need=source.need


def fibonacci_control():
    s=source.s;x=s.Symbol('x');K=s.QQ.alg_field_from_poly(s.Poly(x*x-x-1,x),alias='phi')
    phi=K.unit;D=K(2)+phi;f=K(3)-phi;dims=[K.one,phi];chi=[K.one,K.one-phi]
    total=K.zero
    for col,count in [((1,0),1),((1,1),1),((0,1),2)]:
        dim=sum((K(v)*d for v,d in zip(col,dims)),K.zero)
        total+=K(count)*source.modular.value(chi,col,K)**3/dim
    need(D/f**3*total==K.one,'actual Fibonacci-center positive control')
    return {'source':'Fibonacci center Fib x Fib^rev','distinguished_simple':'(X,X)','cubic_fusion_coefficient':1}


def run():
    d=source.data();R,a,b,characters,cols,Q,high,meta=d;K=b['K']
    need(json.loads(json.dumps(meta,default=int))==json.loads((HERE/'source.json').read_text()),'complete low/high/spectral source replay')
    enumeration=json.loads(json.dumps(gram.run(),default=int))
    need(enumeration==json.loads((HERE/'gram.json').read_text()),'complete double integer enumeration replay')
    need(enumeration['integer_Gram_count']==1071 and enumeration['duality_compatible_count']==155,'complete integer domain')
    need(enumeration['high_vectors']==[list(v)for v,z in high],'complete high ordering')
    need(b['multiplicities'][1]==1,'conjugate-FP character scalar')
    need(all(characters[1][i]==characters[1][a['du'][i]]for i in range(8)),'conjugate-FP distinguished object self-dual')
    coefficients,dual=cubic.linear_data(d)
    first=next(row for row in coefficients if row[0]==(1,1,1))
    triple,low,high_coefficients=first
    # Independently compare the S-normalized coefficients to the scalar
    # D/f^3 formula on every restriction, before using any multiplicities.
    allcols=list(cols)+[(0,)+tuple(v)for v,z in high]
    scalar=[]
    for col in allcols:
        dim=sum((K(x)*y for x,y in zip(col,b['ds'])),K.zero)
        scalar.append(b['D']/b['codegrees'][1]**3*source.modular.value(characters[1],col,K)**3/dim)
    need(low==sum(scalar[:5],K.zero)and high_coefficients==scalar[5:],'scalar and full-S cubic normalization agree')
    values=[];histogram=Counter()
    for index,m in enumerate(enumeration['solutions']):
        value=low+sum((K(n)*c for n,c in zip(m,high_coefficients)),K.zero)
        need(value in (K(source.s.Rational(1,3)),K(source.s.Rational(4,3))),'nonintegral cubic obstruction for each pattern')
        key=str(value.to_list()[0]);histogram[key]+=1
        values.append({'pattern_index':index,'cubic_coefficient':key,'obstruction':'nonintegral_rational'})
    need(dict(histogram)=={'1/3':84,'4/3':71},'complete cubic histogram')
    dependencies=[]
    for relative in ['r567_centerless_integer/source.py','r567_centerless_integer/source.json',
        'r567_centerless_integer/gram.py','r567_centerless_integer/gram.json','r567_centerless_integer/cubic.py',
        'review/INTEGRAL_CENTER_SUBCATEGORY.md','review/integral_center_subcategory.py','review/integral_center_subcategory.json',
        'structural_models/known_model_routes.py','structural_models/known_model_routes.json',
        'noncommutative_followup/additional_scope_gates.py','noncommutative_followup/additional_scope_gates.json']:
        p=FRONTIER/relative
        dependencies.append({'path':str(p.relative_to(HERE.parents[2])),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return {'target':'R8_3_567','kind':'general_exclusion_via_centerless_integer_Gram_and_cubic_Verlinde',
        'tensor_sha256':meta['tensor_sha256'],'unique_low_frame_index':2,
        'complete_integer_Gram_count':1071,'complete_duality_compatible_count':155,
        'distinguished_character_index':1,'distinguished_character_power_basis':[source.c.ec(x)for x in characters[1]],
        'formal_codegree_power_basis':source.c.ec(b['codegrees'][1]),
        'character_field_polynomial':meta['character_field_polynomial'],
        'cubic_checks':values,'coefficient_histogram':dict(sorted(histogram.items())),
        'actual_known_model_control':fibonacci_control(),'dependencies':dependencies,
        'scope':'general_complex_fusion_categories: certified Galois-pseudo-unitary reduction and no-integral-center theorem, followed by a complete necessary central integer-Gram and cubic Verlinde contradiction',
        'outcome':'general_exclusion'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args()
    actual=json.loads(json.dumps(run(),default=int));path=HERE/'verlinde_exclusion.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'complete exact R567 exclusion receipt')
    print('PASS R567:1071 complete integer Grams;155 dual-compatible;84 cubic values1/3 and71 values4/3; general exclusion.')
