"""General categorical trace-ideal and signed-saturation obstruction.

For each rational/quadratic original formal codegree f, induction forces
Delta/f integral in the signed dimension field K containing Q(f). Relative
trace therefore forces Tr_K(Delta) into Tr_Q(f)(f O_Q(f)). Their least common
multiple bounds the signed Casimir trace without isolating K or assuming
pivotality. Exact saturation can then reduce categorification to PU Galois.
"""
import argparse
import itertools
import json
import math
from pathlib import Path
import sympy as s
from exact import require,pc
from rings import dual,validate,casimir
from signed import from_values,gauge_original
from new_ramified_signed import magnitude_branches,enumerate_magnitude,original_characters

ROOT=Path(__file__).resolve().parents[1]


def arithmetic(R):
    n=len(R)
    if n!=6 or dual(R)!=list(range(n)) or any(R[i][j]!=R[j][i] for i in range(n) for j in range(n)):
        return None
    validate(R)
    C=casimir(R);T=int(s.trace(C));data=[]
    for f,m in C.charpoly().as_poly().factor_list()[1]:
        if f.degree()==1:
            value=-s.Rational(f.TC(),f.LC())
            require(value.q==1 and value>0,'invalid rational formal codegree')
            data.append({'polynomial':pc(f),'multiplicity':int(m),'field_degree':1,
                         'trace_generators':[int(value)],'trace_ideal_generator':int(value)})
        elif f.degree()==2:
            A=-int(f.all_coeffs()[1]);B=int(f.TC());disc=A*A-4*B
            require(disc>0,'formal codegree field not real')
            q=math.prod(int(p) for p,e in s.factorint(disc).items() if e%2)
            b=math.isqrt(disc//q)
            require(q>1 and b*b*q==disc,'invalid quadratic discriminant')
            if q%4==1:
                require((A+b*q)%2==0,'nonintegral trace from quadratic integral basis')
                traces=[A,(A+b*q)//2];basis=['1','(1+sqrt(q))/2']
            else:
                traces=[A,b*q];basis=['1','sqrt(q)']
            step=math.gcd(*traces)
            require(step>0,'zero trace ideal')
            data.append({'polynomial':pc(f),'multiplicity':int(m),'field_degree':2,
                         'quadratic_radicand':q,'root_numerator':[A,b],'root_denominator':2,
                         'integral_basis':basis,'trace_generators':traces,'trace_ideal_generator':step})
        # Higher-degree factors are deliberately unused. Omitting necessary
        # divisibilities only weakens this criterion.
    if not data:return None
    L=math.lcm(*(v['trace_ideal_generator'] for v in data))
    deficits=[]
    for i in range(1,n):
        for j in range(i,n):
            for k in range(j,n):
                v=R[i][j][k]
                if v>=2:
                    w=len(set(itertools.permutations((i,j,k))))
                    deficits.append(w*(v*v-(v-2)**2))
    return {'rank':n,'original_Casimir_trace':T,'codegree_trace_ideals':data,
            'dimension_trace_multiple':L,'deficit_budget':T-L,
            'minimum_positive_magnitude_deficit':min(deficits) if deficits else None}


def reduction(R,seconds=60):
    data=arithmetic(R)
    if data is None or data['deficit_budget']<0:return None
    minimum=data['minimum_positive_magnitude_deficit']
    if minimum is None or data['deficit_budget']>=minimum:return None
    original=original_characters(R)
    if original is None:return None
    p,domains=magnitude_branches(R,data)
    require(len(domains)==1,'trace saturation did not leave exactly one magnitude pattern')
    magnitudes=domains[0]
    values,stats=enumerate_magnitude(R,p,magnitudes,seconds)
    cases=[]
    for v in values:
        gauge=gauge_original(from_values(R,p,v),R)
        if gauge is None:return None
        cases.append({'values':list(v),'gauge_original':gauge})
    return {'kind':'trace_ideal_signed_reduction','scope':'general_complex_fusion_categories',
            'arithmetic':data,'indicator_restrictions':False,'sign_gauges':p['gauges'],
            'magnitudes':magnitudes,'statistics':stats,'signed_tables':cases,
            'original_characters':original,
            'claim':'Every categorification has a pseudo-unitary Galois conjugate.'}


def verify_reduction(R,c):
    require(c.get('kind')=='trace_ideal_signed_reduction','wrong trace-ideal reduction kind')
    recomputed=reduction(R,seconds=120)
    require(recomputed is not None and recomputed==c,'incorrect complete trace-ideal saturation reduction')
    return True


def certificate(R,pseudo=None,seconds=60):
    data=arithmetic(R)
    if data is None:return None
    if data['deficit_budget']<0:
        return {'kind':'formal_codegree_trace_ideal','scope':'general_complex_fusion_categories','arithmetic':data}
    if pseudo is None:return None
    red=reduction(R,seconds)
    if red is None:return None
    from oriented_extension import pseudo_check
    pseudo_check(R,pseudo)
    return {'kind':'trace_ideal_signed_pseudo_exclusion','scope':'general_complex_fusion_categories',
            'reduction':red,'pseudo':pseudo}


def verify(R,c):
    require(c.get('scope')=='general_complex_fusion_categories','wrong trace-ideal scope')
    if c.get('kind')=='formal_codegree_trace_ideal':
        a=arithmetic(R)
        require(a is not None and a==c['arithmetic'],'incorrect formal-codegree trace ideals')
        require(a['deficit_budget']<0,'no Casimir trace contradiction')
        return True
    require(c.get('kind')=='trace_ideal_signed_pseudo_exclusion','wrong trace-ideal certificate kind')
    verify_reduction(R,c['reduction'])
    from oriented_extension import pseudo_check
    pseudo_check(R,c['pseudo'])
    return True


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--all',action='store_true')
    ap.add_argument('--verbose',action='store_true')
    ap.add_argument('--output',default=str(ROOT/'research/round2_external/trace_ideal_scan.json'))
    args=ap.parse_args()
    if args.all:rows=json.load(open(ROOT/'data/census.json'))
    else:rows=json.load(open(ROOT/'verification/round2/campaign_manifest.json'))['inputs']
    results=[]
    for row in rows:
        a=arithmetic(row['N'])
        if a is not None:
            c=certificate(row['N']) if a['deficit_budget']<0 else None
            results.append({'id':row['id'],'arithmetic':a,'certificate':c})
            if c and args.verbose:print(row['id'],'excluded',a['dimension_trace_multiple'],a['original_Casimir_trace'],flush=True)
    Path(args.output).write_text(json.dumps({'checked':len(rows),'results':results},indent=2)+'\n')
    print(json.dumps({'checked':len(rows),'applicable':len(results),'excluded':sum(z['certificate'] is not None for z in results),'output':args.output}))

if __name__=='__main__':main()
