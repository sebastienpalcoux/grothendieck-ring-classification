"""Exact-only replay controls for the optional bounded phase-I proposal."""
from pathlib import Path
from fractions import Fraction as Q
import argparse,json
from features import System,require
from linear import verify
HERE=Path(__file__).resolve().parent
CASES=[((1,),2,1,True),((-1,),-2,1,True),((2,),1,1,False),((1,),1,1,False),((0,),1,1,True)]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rediscover',action='store_true');ap.add_argument('--write',action='store_true');args=ap.parse_args();path=HERE/'linear_validation.json'
    require(not args.write or args.rediscover,'writing requires explicit rediscovery')
    saved=None if args.rediscover else json.loads(path.read_text());records=[]
    for i,(col,b,u,negative)in enumerate(CASES):
        S=System((col,),(b,),(u,),(),(),{})
        if args.rediscover:
            from linear import discover
            proposal=discover(S)
            require((proposal['conclusion']=='exact_bounded_linear_obstruction')==negative,'phase-I control gave wrong exact conclusion')
            cert=proposal['certificate']if negative else {'rational_primal':[str(Q(b,col[0]))]}
        else:cert=saved['records'][i]['certificate']
        if negative:verify(S,cert)
        else:
            x=list(map(Q,cert['rational_primal']));require(len(x)==1 and 0<=x[0]<=u and x[0]*col[0]==b,'rational control witness fails')
        records.append({'column':list(col),'rhs':b,'upper_bound':u,'negative':negative,'certificate':cert})
    out={'kind':'exact_bounded_phase_I_validation','result':'PASS','records':records,
         'scope':'three exact bounded separators, one integral feasible control, and one integer-infeasible but rationally feasible control'}
    if args.write:path.write_text(json.dumps(out,indent=2)+'\n')
    elif not args.rediscover:require(saved==out,'bounded phase-I control differs')
    print('PASS exact-only bounded phase-I controls',flush=True)
if __name__=='__main__':main()
