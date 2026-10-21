"""Complete R941 monodromy-charge allocations and joint Galois spectra."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import argparse,hashlib,itertools,json
import joint_spectrum as joint
HERE=Path(__file__).resolve().parent;FRONTIER=HERE.parent;need=joint.need


def compute():
    jp=HERE/'joint_spectrum.json';source=json.loads(jp.read_text());rec=next(r for r in source['records']if r['id']=='R8_3_941')
    values=[tuple(tuple(map(F,z))for z in t)for t in rec['low_high_joint_eigenvalue_tuples']]
    cp=FRONTIER/'quartic_integer_center/r941_charges.json';charges=json.loads(cp.read_text())
    need(charges['complete_charge_allocation_count']==len(charges['solutions'])==93,'complete93 charge allocations')
    patterns=json.loads((FRONTIER/'quartic_integer_center/gram_cubic.json').read_text())['patterns']
    signs=[1,1,1,1,-1];translated=[40,41,42,43,57];cases=[]
    for at,case in enumerate(charges['solutions']):
        counts=Counter();p=case['plus_pairs'];m=case['minus_individuals'];pattern=patterns[case['pattern_index']]
        need(len(p)==len(m)==40 and all(2*x+y==pattern[j]for j,(x,y)in enumerate(zip(p,m))),'charge split matches integer Gram pattern')
        for j,sign in enumerate(signs):counts[(sign,values[j])]+=1
        for j in range(40):counts[(1,values[j+5])]+=2*p[j];counts[(-1,values[j+5])]+=m[j]
        for j,sign in zip(translated,signs):need(pattern[j]==1,'fixed low-translate count');counts[(sign,values[j+5])]+=1
        need(all(pattern[j]==0 for j in range(40,65)if j not in translated),'complete charge support')
        failure=None
        for sign,t in sorted(counts):
            for e2,e3 in itertools.product((-1,1),repeat=2):
                ct=tuple((z[0],z[1]*e2,z[2]*e3,z[3]*e2*e3)for z in t)
                if counts[sign,t]!=counts[sign,ct]:
                    failure={'monodromy_charge':sign,'tuple':[list(map(str,z))for z in t],'signs':[e2,e3],
                             'multiplicity':counts[sign,t],'conjugate_multiplicity':counts[sign,ct]};break
            if failure is not None:break
        cases.append({'allocation_index':at,'pattern_index':case['pattern_index'],'passes':failure is None,'first_exact_failure':failure})
    return {'id':'R8_3_941','kind':'joint_Galois_multiplicities_including_central_involution',
        'dependencies_sha256':{str(p.relative_to(FRONTIER)):hashlib.sha256(p.read_bytes()).hexdigest()for p in[jp,cp]},
        'complete_allocation_count':93,'cases':cases,'surviving_allocation_indices':[r['allocation_index']for r in cases if r['passes']],
        'surviving_pattern_indices':sorted({r['pattern_index']for r in cases if r['passes']}),
        'scope':'necessary joint spectra of the five distinguished fusion matrices and N_G; rational charge coordinate fixed under every field automorphism'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args();out=compute();path=HERE/'charged_joint_spectrum.json'
    if args.write:path.write_text(json.dumps(out,indent=2)+'\n')
    else:need(out==json.loads(path.read_text()),'charged joint spectral receipt')
    print('PASS R941 charged joint Galois: allocations',len(out['surviving_allocation_indices']),'patterns',len(out['surviving_pattern_indices']),flush=True)
