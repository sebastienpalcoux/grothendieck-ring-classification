"""Bounded exact-method attempts on the recovered candidate cohort.

The cohort is a scheduling list only. All criterion hypotheses and outcomes
are calculated from source tensors; no search limit is a mathematical result.
"""
import argparse,concurrent.futures,json,time
from types import SimpleNamespace
from pathlib import Path
import advanced_campaign as campaign
COHORT=[65,436,439,455,567,721,731,901,903,921,925,926,928,941,982,985,986,1055,1154,1203,1350,1463,1615,1617,1660,1661,1739,1768,1795,2842,2885,3258,3344,3413,3472]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--jobs',type=int,default=2);ap.add_argument('--budget',type=int,default=90);ap.add_argument('--memory-mb',type=int,default=1500);ap.add_argument('--commutative-only',action='store_true');args=ap.parse_args()
    rows=json.loads((campaign.HERE.parent/'pipeline/census_m3.json').read_text());rows=[r for r in rows if int(r['id'].split('_')[-1]) in COHORT and (not args.commutative_only or r['commutative'])]
    work=[(row,mode) for mode in ('dimension_order','character','tensor_rotation','modular') for row in rows];results=[];start=time.monotonic()
    def one(job):
        row,mode=job;settings=SimpleNamespace(tag='candidate_'+mode,mode=mode,height=6,signed_timeout=60,budget=args.budget,memory_mb=args.memory_mb,overwrite=False)
        return campaign.task(row,settings)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for result in pool.map(one,work):
            results.append(result);print(result['id'],result.get('mode'),result['status'],flush=True)
            output={'cohort_ids':[r['id'] for r in rows],'budget_seconds_per_attempt':args.budget,'completed':len(results),'planned':len(work),'seconds':round(time.monotonic()-start,3),'attempts':results}
            campaign.save(campaign.HERE/'candidate_attempts.json',output)
if __name__=='__main__':main()
