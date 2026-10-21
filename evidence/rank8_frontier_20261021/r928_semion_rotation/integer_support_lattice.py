"""Exact integer lattice after necessary nonnegative support restrictions."""
from pathlib import Path
import argparse,hashlib,json
from flint import nmod_mat
import pair_rotation as pair
import integer_counts as counts
HERE=Path(__file__).resolve().parent;need=pair.need


def bounds(A,b):
    out=[None]*len(A[0]);witness=[None]*len(A[0])
    for i,(row,rhs)in enumerate(zip(A,b)):
        if rhs<0 or any(x<0 for x in row):continue
        for j,x in enumerate(row):
            if x>0:
                q=rhs//x
                if out[j]is None or q<out[j]:out[j]=q;witness[j]=i
    need(all(v is not None for v in out),'finite exact upper bounds')
    return out,witness


def check_ray(A,b,active,cert):
    p=cert['prime'];y=cert['row']
    need(p in counts.PRIMES and len(y)==len(A)and all(type(v)is int and 0<=v<p for v in y),'modular certificate domain')
    need(all(sum(v*A[i][j]for i,v in enumerate(y))%p==0 for j in active),'all possible nonzero integer variables annihilated')
    residue=sum(v*x for v,x in zip(y,b))%p
    need(residue!=0 and residue==cert['rhs_residue'],'nonzero modular RHS contradiction')


def run(write):
    loaded=pair.setup();prior=json.loads((HERE/'integer_counts.json').read_text());path=HERE/'integer_support_lattice.json'
    saved=None if write else json.loads(path.read_text());cases=[]
    for previous in prior['cases']:
        index=previous['metadata']['pattern_index'];A,b,meta=pair.build(loaded,index)
        need(meta==previous['metadata'],'source full pair equations')
        ub,rows=bounds(A,b);need(ub==previous['result']['finite_exact_upper_bounds'],'exact bounds independently rebuilt')
        active=[j for j,v in enumerate(ub)if v]
        if write:
            if previous['result']['status']=='exact_nonnegative_integer_witness':
                witness=previous['result']['witness'];counts.check_integer(A,b,witness)
                result={'status':'exact_nonnegative_integer_witness','witness':witness}
            else:
                result={'status':'integer_feasibility_unresolved','tested_modular_primes':list(counts.PRIMES)}
                for p in counts.PRIMES:
                    Z,n=nmod_mat([[row[j]%p for j in active]for row in A],p).transpose().nullspace()
                    for k in range(n):
                        y=[int(Z[i,k])for i in range(len(A))];r=sum(v*x for v,x in zip(y,b))%p
                        if r:
                            cert={'prime':p,'row':y,'rhs_residue':r};check_ray(A,b,active,cert)
                            result={'status':'exact_supported_integer_lattice_obstruction','certificate':cert};break
                    if result['status']!='integer_feasibility_unresolved':break
        else:
            old=saved['cases'][len(cases)];need(old['metadata']==meta and old['active_variables']==active and old['bound_witness_rows']==rows,'complete exact supported lattice domain')
            result=old['result']
            if result['status']=='exact_nonnegative_integer_witness':counts.check_integer(A,b,result['witness'])
            elif result['status']=='exact_supported_integer_lattice_obstruction':check_ray(A,b,active,result['certificate'])
            else:
                need(result['status']=='integer_feasibility_unresolved','honest incomplete integer outcome')
                for prime in counts.PRIMES:
                    Z,nullity=nmod_mat([[row[j]%prime for j in active]for row in A],prime).transpose().nullspace()
                    need(all(sum(int(Z[i,k])*b[i]for i in range(len(A)))%prime==0 for k in range(nullity)),'all recorded supported modular tests pass')
        cases.append({'metadata':meta,'active_variables':active,'bound_witness_rows':rows,'result':result})
        print('R928 supported integer lattice',index,result['status'],flush=True)
    out={'id':'R8_3_928','dependencies_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in[HERE/'integer_counts.py',HERE/'integer_counts.json',HERE/'pair_rotation.py',HERE/'pair_rotation.json']},
         'cases':cases,'surviving_indices':[x['metadata']['pattern_index']for x in cases if x['result']['status']!='exact_supported_integer_lattice_obstruction'],
         'scope':'integer relative-trace type multiplicities; support-zero consequences use nonnegativity; exact modular exclusions and exact integer feasible necessary data only'}
    if write:path.write_text(json.dumps(out,indent=2)+'\n')
    else:need(out==saved,'full supported integer lattice receipt')
    print('PASS R928 supported integer lattice campaign; survivors=',out['surviving_indices'],flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');run(p.parse_args().write)
