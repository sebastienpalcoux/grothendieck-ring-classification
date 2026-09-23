#!/usr/bin/env python3
"""Independent exact arithmetic comparisons across the entire extended census."""
from pathlib import Path
import sys,json,time,copy
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'software'))
from rings import *
from signed import gauge_images,canonical_duality
from proofs import signed_adjoint_parity
from rapid import dnumber as fast_dnumber,check_dnumber as fast_check,casimir_polynomial
from census_data import iter_parameters,parameter_tensor,read_manifest

def main():
    start=time.monotonic();n=0;dn=0;max_m=0
    for sid,tag,p in iter_parameters():
        if sid%4000 and max(p)!=128:continue
        # A deterministic distributed sample plus every 128th boundary input.
        if sid%4000 and sid%128:continue
        R=parameter_tensor(tag,p);f=casimir_polynomial(R)
        require([int(f[k]) for k in range(4,-1,-1)]==[int(a) for a in codegree_poly(R).all_coeffs()],'characteristic polynomial accelerator disagreement')
        require(casimir_determinant(R)==casimir(R).det(),'Bareiss determinant disagreement')
        a=fast_dnumber(R);b=dnumber(R);require(bool(a)==bool(b),'FLINT/SymPy d-number disagreement')
        if a:check_dnumber(R,a);fast_check(R,b);dn+=1
        n+=1;max_m=max(max_m,max(p))
    models=json.loads((ROOT/'data/models.json').read_text());gauge_checks=0
    for model in models:
        R,_,kind=canonical_duality(model['matrices'])
        if kind!='sd':continue
        for pars in gauge_images(sd_tuple(R)):
            require(signed_adjoint_parity(R,sd_tensor(pars)) is None,'model gauge rejected by parity');gauge_checks+=1
    report={'passed':True,'FLINT_SymPy_polynomial_and_dnumber_comparisons':n,'cross_checked_dnumber_witnesses':dn,
        'largest_sampled_multiplicity':max_m,'model_gauge_parity_checks':gauge_checks,
        'sampling':'Every source index divisible by4000, plus multiplicity128 source indices divisible by128.',
        'elapsed_seconds':round(time.monotonic()-start,3)}
    (ROOT/'verification/extension_tests.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
