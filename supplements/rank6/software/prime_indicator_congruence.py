"""Exact large-prime indicator congruences conditional on a proved exponent.

If p does not divide the twist exponent N, the p-th indicator lies in both
Q(zeta_p) and Q(zeta_N), hence is an integer. Rational cyclic-character
multiplicities give nu_p(X)=[X^p:1] modulo p. Pseudo-unitarity bounds its
absolute value by FPdim(X). A prime larger than twice an integer FP bound
therefore determines the indicator uniquely, if such a value exists.
"""
import argparse,hashlib,json,math,sys,time
from pathlib import Path
import sympy as s
from exact import require
from rings import Characters,validate
ROOT=Path(__file__).resolve().parents[1]

def modular_unit_coefficient(N,p):
    """Coefficient of the unit in the p-th power, via exact modular squaring."""
    n=len(N);M=[[int(a)%p for a in row]for row in N];v=[1]+[0]*(n-1);power=p
    while power:
        if power&1:v=[sum(v[j]*M[j][k] for j in range(n))%p for k in range(n)]
        power//=2
        if power:M=[[sum(M[i][j]*M[j][k] for j in range(n))%p for k in range(n)]for i in range(n)]
    return v[0]

def large_prime_targets(R,N,samples=3):
    validate(R);require(type(N)is int and N>0 and samples>=1,'invalid exponent or sample count')
    n=len(R);bounds=[max(map(sum,M))for M in R];cutoff=2*max(bounds)
    residues=[a for a in range(N)if math.gcd(a,N)==1];primes={a:[]for a in residues};p=cutoff
    while any(len(v)<samples for v in primes.values()):
        p=int(s.nextprime(p));a=p%N
        if a in primes and len(primes[a])<samples:primes[a].append(p)
    _,K,ds,D,poly,embedding=Characters(R).fp();rows=[];failures=[]
    for a in residues:
        values=[];observations=[]
        for p in primes[a]:
            row=[]
            for i,M in enumerate(R):
                h=modular_unit_coefficient(M,p);candidates=[x for x in (h,h-p)if -bounds[i]<=x<=bounds[i]]
                require(len(candidates)<=1,'prime cutoff failed to give uniqueness')
                value=candidates[0]if candidates else None
                if value is None:failures.append(dict(residue=a,prime=p,object=i,reason='no_bounded_integer',unit_coefficient_mod_prime=h,bound=bounds[i]))
                elif embedding.sign(ds[i]-K(abs(value)))<0:failures.append(dict(residue=a,prime=p,object=i,reason='exceeds_exact_FP_dimension',value=value))
                row.append(value)
            observations.append(dict(prime=p,values=row));values.append(row)
        if any(row!=values[0]for row in values[1:]):failures.append(dict(residue=a,reason='same_residue_disagrees',observations=observations))
        rows.append(dict(residue=a,values=values[0],observations=observations))
    return dict(exponent=N,scope='conditional_on_proved_center_twist_exponent_and_pseudo_unitarity',samples_per_residue=samples,row_sum_bounds=bounds,prime_cutoff_strict=cutoff,residue_count=len(residues),targets=rows,failures=failures,passed=not failures,optimizer_used=False)

def campaign():
    census=json.loads((ROOT/'data/census.json').read_text());out=[]
    for ident,N in [('R6_4_22',20),('R6_4_91',16),('R6_4_629',15),('R6_8_1660',48)]:
        R=next(r['N']for r in census if r['id']==ident);result=dict(id=ident,**large_prime_targets(R,N));out.append(result);print({'id':ident,'passed':result['passed'],'failures':result['failures'],'targets':[(r['residue'],r['values'])for r in result['targets']]},flush=True)
    cyclic=[[[int(k==(i+j)%3) for k in range(3)]for j in range(3)]for i in range(3)]
    control=large_prime_targets(cyclic,3,2);require(control['passed'] and all(t['values']==[1,0,0]for t in control['targets']),'Vec(C3) positive control failed')
    wrong=large_prime_targets(cyclic,2,2);require(not wrong['passed'] and any(f['reason']=='same_residue_disagrees'for f in wrong['failures']),'false exponent control was not rejected')
    fibonacci=[[[1,0],[0,1]],[[0,1],[1,1]]];fib=large_prime_targets(fibonacci,5,2)
    require(fib['passed'] and all(t['values']==[1,int(t['residue'] in(2,3))]for t in fib['targets']),'Fibonacci positive control failed')
    checks=0
    for R in (cyclic,fibonacci):
        for M in R:
            for p in (5,7,11,13):
                v=[1]+[0]*(len(R)-1)
                for _ in range(p):v=[sum(v[j]*M[j][k]for j in range(len(R)))for k in range(len(R))]
                require(modular_unit_coefficient(M,p)==v[0]%p,'binary modular power control failed');checks+=1
    return dict(kind='large_prime_indicator_congruence_campaign',version=1,optimizer_used=False,controls=dict(cyclic_C3=control,fibonacci=fib,false_exponent=wrong,binary_power_checks=checks),cases=out)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--verify',action='store_true');ap.add_argument('--output',type=Path,default=ROOT/'research/round5/unification/prime_indicator_congruences.json');args=ap.parse_args();st=time.monotonic()
    if args.verify:
        import scipy.optimize as op
        def denied(*a,**k):raise RuntimeError('optimizer forbidden in prime-indicator replay')
        op.linprog=op.milp=denied
    result=campaign()
    if args.verify:
        require(result==json.loads(args.output.read_text()),'prime indicator replay differs')
        files=[Path(__file__),ROOT/'software/exact.py',ROOT/'software/rings.py',ROOT/'data/census.json',args.output]
        receipt=dict(passed=True,optimizer_used=False,optimized_python=not __debug__,elapsed_seconds=round(time.monotonic()-st,3),files={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()for f in files})
        args.output.with_name(args.output.stem+'_replay_O.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt,flush=True)
    else:args.output.write_text(json.dumps(result,indent=2)+'\n')
