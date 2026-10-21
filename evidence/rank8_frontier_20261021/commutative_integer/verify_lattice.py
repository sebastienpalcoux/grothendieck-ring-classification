"""Independent exhaustive validation of the exact modular lattice eliminator."""
from pathlib import Path
import argparse,itertools,json,random
from features import System,require
from lattice import modular,verify_result,hermite
from bounds import propagate,reduced,lift
from features import check_integer
from flint import fmpz_mat
from equations import compact,lift_separator
HERE=Path(__file__).resolve().parent

def run():
    records=[]
    for p in (2,3):
        outcomes={}
        for m,n in[(1,0),(1,1),(2,1),(2,2),(3,2),(3,3)]:
            for seed in range(50):
                rng=random.Random(1000*p+100*m+10*n+seed)
                columns=tuple(tuple(rng.randrange(-5,6)for _ in range(m))for _ in range(n));b=tuple(rng.randrange(-5,6)for _ in range(m))
                S=System(columns,b,(10,)*n,(),(),{})
                expected=any(all(sum(columns[j][i]*x[j]for j in range(n))%p==b[i]%p for i in range(m))for x in itertools.product(range(p),repeat=n))
                got=modular(S,p)
                require((got['outcome']=='consistent_mod_prime')==expected,'bit-plane elimination disagrees with complete Cartesian enumeration')
                verify_result(S,got);outcomes[got['outcome']]=outcomes.get(got['outcome'],0)+1
        records.append({'prime':p,'systems':300,'outcomes':outcomes})
    hnf_cases=0
    for m,n in[(1,1),(3,1),(3,3),(5,7)]:
        for seed in range(20):
            rng=random.Random(100*m+10*n+seed);cols=tuple(tuple(rng.randrange(-6,7)for _ in range(m))for _ in range(n));b=tuple(rng.randrange(-6,7)for _ in range(m));S=System(cols,b,(100,)*n,(),(),{})
            out=hermite(S,batch=2)
            def nonzero(M):return[tuple(map(int,row))for row in M.tolist()if any(row)]
            expected=nonzero(fmpz_mat(cols).hnf())==nonzero(fmpz_mat(list(cols)+[b]).hnf())
            require((out['outcome']=='integer_lattice_member')==expected,'incremental HNF differs from complete HNF');hnf_cases+=1
    box_cases=0
    for seed in range(300):
        rng=random.Random(seed);m=1+seed%4;n=1+(seed//4)%4;cols=tuple(tuple(rng.randrange(-4,5)for _ in range(m))for _ in range(n));u=tuple(rng.randrange(1,4)for _ in range(n));b=tuple(rng.randrange(-8,9)for _ in range(m));S=System(cols,b,u,(),tuple(range(n)),{})
        feasible=[x for x in itertools.product(*(range(v+1)for v in u))if all(sum(x[j]*cols[j][i]for j in range(n))==b[i]for i in range(m))]
        out=propagate(S)
        if out['outcome']=='integer_box_obstruction':require(not feasible,'false interval/gcd obstruction')
        else:
            R=reduced(S,out)
            for x in feasible:require(all(l<=v<=h for l,v,h in zip(out['lower_bounds'],x,out['upper_bounds'])),'true integer solution removed')
            for y in itertools.product(*(range(v+1)for v in R.bounds)):
                if all(sum(y[j]*R.columns[j][i]for j in range(len(y)))==R.rhs[i]for i in range(m)):check_integer(S,lift(S,out,y))
        box_cases+=1
    compression_cases=0
    for seed in range(100):
        rng=random.Random(seed);m=1+seed%4;n=1+seed%3;cols=tuple(tuple(rng.randrange(-4,5)for _ in range(m))for j in range(n));b=tuple(rng.randrange(-6,7)for _ in range(m));S=System(cols,b,(3,)*n,(),tuple(range(n)),{});T=compact(S)
        for x in itertools.product(range(4),repeat=n):
            before=all(sum(x[j]*cols[j][i]for j in range(n))==b[i]for i in range(m));after=all(sum(x[j]*T.columns[j][i]for j in range(n))==T.rhs[i]for i in range(len(T.rhs)))
            require(before==after,'row compression changed integer solutions')
        outcome=hermite(T)
        if outcome['outcome']=='integer_lattice_obstruction':lift_separator(S,T,outcome['certificate'])
        compression_cases+=1
    return {'result':'PASS','kind':'exhaustive_integer_lattice_and_bound_validation','proportional_compression_comparisons':compression_cases,'modular_records':records,'HNF_direct_comparisons':hnf_cases,'complete_finite_box_comparisons':box_cases,'independent_methods':['complete finite-field vector enumeration','one-shot exact HNF of A and [A|b]','complete bounded integer vector enumeration']}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');a=ap.parse_args();out=run();path=HERE/'lattice_validation.json'
    if a.write:path.write_text(json.dumps(out,indent=2)+'\n')
    else:require(out==json.loads(path.read_text()),'modular validation differs')
    print('PASS 600 modular +80 direct HNF +300 finite-box +100 compression controls',flush=True)
if __name__=='__main__':main()
