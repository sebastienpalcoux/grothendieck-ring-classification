#!/usr/bin/env python3
"""Independent exact checks for both signed-search accelerators."""
from pathlib import Path
from collections import Counter
import argparse,copy,gzip,itertools,json,random,subprocess,sys,tempfile,time
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'software'))
from proofs import *


def records():
    final=ROOT/'certificates/classification.jsonl.gz'
    if final.exists():
        from census_data import iter_parameters
        with gzip.open(final,'rt') as stream:
            next(stream)
            for (sid,tag,p),line in zip(iter_parameters(),stream):
                row=json.loads(line)
                if row['certificate']['kind']=='signed':
                    require(sid==row['source_index'],'signed test input identity')
                    row['parameters']=list(p);row['tag']=tag;yield row
    else:
        for line in (ROOT/'certificates/stage_signed.jsonl').open():
            row=json.loads(line)
            if row['certificate'] and row['certificate']['kind']=='signed':yield row


def main():
    start=time.monotonic();fast,slow=Search('cpp'),Search('python')
    comparisons=0;global_comparisons=0;fixture=None;methods=Counter()
    for row in records():
        c=row['certificate']
        methods[c.get('enumeration',{}).get('method','nonselfdual_explicit')]+=1
        if c['duality_type']!='sd':continue
        if 'parameters' in row:R=sd_tensor(row['parameters'])
        else:
            from census_data import iter_parameters,parameter_tensor
            # This fallback is used only if a future record schema omits parameters.
            tag,p=next((tag,p) for sid,tag,p in iter_parameters() if sid==row['source_index'])
            R=parameter_tensor(tag,p)
        A=permute(R,c['basis']);N=sd_tuple(A)
        if max(N)>6:continue
        primes=sorted({int(q) for f,m in codegree_factors(A) for q in s.factorint(abs(int(f.TC())))})
        a,b=fast.filtered_selfdual(N,primes),slow.filtered_selfdual(N,primes)
        require(a==b,'compressed search disagrees with independent Python enumeration')
        if fast.global_catalog is not None:
            from rapid import dnumber as rapid_dnumber,cyclotomic_failure as rapid_cyclotomic
            expected=[p for p in a[0] if rapid_dnumber(sd_tensor(p)) is None
                      and rapid_cyclotomic(sd_tensor(p)) is None]
            require(fast.global_selfdual(N,primes)[0]==expected,'global orbit expansion differs from local enumeration')
            global_comparisons+=1
        original=slow.selfdual(N)
        require(original==fast.selfdual(N),'unfiltered self-dual backend disagreement')
        for p in original:
            require(sd_parity_failure(N,p)==(signed_adjoint_parity(A,sd_tensor(p)) is not None),'parity slot formula mismatch')
        comparisons+=1
        if fixture is None and c['tables']:fixture=(R,c)
    require(comparisons>0,'no bounded signed fixtures found')
    extra_bounds=((0,0,0,1,0,1,1,0,0,1),(1,)*10,(2,)*10,
                  (2,0,0,1,0,1,2,2,2,2),(0,0,0,1,0,1,0,0,0,0))
    for N in extra_bounds:
        require(fast.filtered_selfdual(N,[] )==slow.filtered_selfdual(N,[]),
                'degenerate parity-domain enumeration disagreement')

    ns_checks=0
    for N in itertools.product(range(3),repeat=6):
        require(fast.nonselfdual(N)==nonselfdual_tables(N),'non-self-dual backend disagreement')
        ns_checks+=1

    rng=random.Random(71284)
    tuples=[tuple(rng.randint(-bound,bound) for _ in range(10)) for bound in (128,1000) for _ in range(100)]
    with tempfile.TemporaryDirectory() as tmp:
        cpp=Path(tmp)/'determinant.cpp';exe=Path(tmp)/'determinant'
        source=ROOT/'software/enumerate_signed.cpp'
        cpp.write_text('#define main signed_main\n#include "'+str(source)+'"\n#undef main\n'
          'int main(){P p;while(std::cin>>p[0]){for(int i=1;i<10;i++)std::cin>>p[i];'
          'auto d=casimir_det(p);std::cout<<(long long)(d/1000000000000000000LL)<<" "'
          '<<(long long)(d%1000000000000000000LL)<<"\\n";}}\n')
        subprocess.run(['g++','-O2','-std=c++17',str(cpp),'-o',str(exe)],check=True)
        result=subprocess.check_output([str(exe)],input=''.join(' '.join(map(str,p))+'\n' for p in tuples),text=True)
    require(len(result.splitlines())==len(tuples),'missing determinant output')
    for p,line in zip(tuples,result.splitlines()):
        a,b=map(int,line.split())
        require(a*10**18+b==casimir_determinant(sd_tensor(p)),'C++ Casimir determinant disagreement')

    R,certificate=fixture;rejected=[]
    count_key='retained_tables' if certificate['enumeration']['method']=='global_signed_catalog_v3' else 'total'
    source_key='generator_source_sha256' if certificate['enumeration']['method']=='global_signed_catalog_v3' else 'source_sha256'
    edits=[('invalid basis',lambda c:c.update(basis=[0,1,1,3])),
           ('altered enumeration count',lambda c:c['enumeration'].update({count_key:c['enumeration'][count_key]+1})),
           ('missing retained tuple',lambda c:c['tables'].pop()),
           ('wrong source digest',lambda c:c['enumeration'].update({source_key:'0'*64}))]
    for name,edit in edits:
        c=copy.deepcopy(certificate);edit(c)
        try:check_signed(R,c,fast)
        except (VerificationError,ValueError,IndexError,KeyError):rejected.append(name)
        else:raise VerificationError('corrupted compact certificate accepted: '+name)
    report={'passed':True,'selfdual_python_cpp_cases_through_6':comparisons,
            'certificate_methods':dict(methods),
            'extra_degenerate_signed_boxes':len(extra_bounds),'global_orbit_query_comparisons':global_comparisons,
            'nonselfdual_python_cpp_bound_boxes':ns_checks,
            'cpp_python_casimir_determinants':len(tuples),
            'rejected_corruptions':rejected,'elapsed_seconds':round(time.monotonic()-start,3)}
    target=ROOT/'verification/signed_scaling_tests.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':main()
