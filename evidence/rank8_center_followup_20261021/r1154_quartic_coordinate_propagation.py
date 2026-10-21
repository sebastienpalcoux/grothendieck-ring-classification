"""Exact coordinate-only necessary propagation after the R1154 quartic bound.

Does not enumerate coupled assignments or use a solver. No repository writes.
Run r1154_quartic_necessary_filters.py first and save its stdout beside this file.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--root',type=Path,default=HERE.parents[1]/'grothendieck-ring-classification')
ap.add_argument('--base',type=Path,default=HERE/'r1154_quartic_necessary_filters.json')
args=ap.parse_args();root=args.root.resolve()
def need(ok,message):
    if not ok:raise RuntimeError(message)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
r=json.loads(args.base.read_text())
need(r['verifier_sha256']==digest(HERE/'r1154_quartic_necessary_filters.py'),'upstream verifier hash')
for name,expected in r['source_sha256'].items():need(digest(root/name)==expected,'upstream source hash: '+name)
d=json.loads((root/'evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json').read_text())
need(d['tensor_sha256']==r['tensor_sha256'],'tensor binding')
need(r['coordinate_exclusions']==892 and len(r['survivor_indices'])==r['remaining_patterns']==346,'upstream cardinalities')
initial=set(r['survivor_indices']);need(len(initial)==346,'unique initial indices')
need(all(all(type(x) is int and x>=0 for x in col) for col in d['high_columns']),'nonnegative integer restriction matrix')
failures=[];remaining=[];reason_counts={};groups=[];covered=[];maximum_iterations=0;maximum_domain_size=0
for g in r['groups']:
    alpha=F(g['alpha']);qs=[F(row[0]) for row in g['minimum_norm_rows_by_high_type']]
    groupfail=[];grouppass=[]
    for ix in g['indices']:
        if ix not in initial:continue
        covered.append(ix);counts=d['completions'][ix]
        choices=[[] if not n else [F(v)-q for v in range(L,U+1) if (F(v)-q)**2<=alpha] for n,q,(L,U) in zip(counts,qs,g['integer_pair11_ranges'])]
        maximum_domain_size=max(maximum_domain_size,max(map(len,choices)))
        why=None;bound={};iterations=0
        while True:
            iterations+=1
            if any(n and not cs for n,cs in zip(counts,choices)):
                why='empty_coordinate_domain';break
            mn=[min(t*t for t in cs) if cs else F(0) for cs in choices]
            lb=sum(n*v for n,v in zip(counts,mn))
            if lb>alpha:
                why='squared_norm_lower_bound';bound={'lower_bound':str(lb),'alpha':str(alpha)};break
            ub=sum(n*max(t*t for t in cs) for n,cs in zip(counts,choices) if n)
            if ub<alpha:
                why='squared_norm_upper_bound';bound={'upper_bound':str(ub),'alpha':str(alpha)};break
            lows=[sum(n*col[j]*min(cs) for n,col,cs in zip(counts,d['high_columns'],choices) if n) for j in range(7)]
            highs=[sum(n*col[j]*max(cs) for n,col,cs in zip(counts,d['high_columns'],choices) if n) for j in range(7)]
            bad=[j for j,(l,u) in enumerate(zip(lows,highs)) if l>0 or u<0]
            if bad:
                j=bad[0];why='linear_residual_interval';bound={'restriction_coordinate':j+1,'lower_bound':str(lows[j]),'upper_bound':str(highs[j])};break
            changed=False;new=[]
            for i,(n,cs) in enumerate(zip(counts,choices)):
                if not n:new.append([]);continue
                col=d['high_columns'][i]
                # Fix one individual row of type i, leaving n_i-1 copies free.
                # Every discarded value violates a necessary bound, so removal
                # for all interchangeable copies preserves every true solution.
                ok=[t for t in cs if lb-mn[i]+t*t<=alpha and all(l-col[j]*min(cs)+col[j]*t<=0<=u-col[j]*max(cs)+col[j]*t for j,(l,u) in enumerate(zip(lows,highs)))]
                changed|=(ok!=cs);new.append(ok)
            choices=new
            if not changed:break
        maximum_iterations=max(maximum_iterations,iterations)
        if why:
            failures.append({'index':ix,'group':g['group'],'reason':why,'iterations':iterations,'terminal_bound':bound,'terminal_coordinate_domains':[[str(t) for t in cs] for cs in choices]})
            groupfail.append(ix);reason_counts[why]=reason_counts.get(why,0)+1
        else:remaining.append(ix);grouppass.append(ix)
    groups.append({'group':g['group'],'alpha':g['alpha'],'initial_patterns':len(groupfail)+len(grouppass),'excluded':len(groupfail),'surviving':len(grouppass)})
need(sorted(covered)==sorted(initial),'complete initial domain coverage')
need(sorted([r['index'] for r in failures]+remaining)==sorted(initial),'disjoint exhaustive outcome partition')
result={
 'scope':'exact necessary coordinate propagation on remaining R1154 Gram patterns; no ring exclusion or categorification claim',
 'id':r['id'],'tensor_sha256':r['tensor_sha256'],'initial_cubic_patterns':1238,
 'initial_coordinate_exclusions':892,'initial_patterns':346,'additional_exclusions':len(failures),'total_excluded_patterns':892+len(failures),'remaining_patterns':len(remaining),
 'method':{'initial_coordinate_domain':'t=n-q with L<=n<=U and t^2<=alpha','norm_bound':'sum of individual minimum squares <= alpha <= sum of individual maximum squares','linear_bound':'Each coordinate of M t must admit zero between sums of minimum and maximum contributions. M has nonnegative entries.','pruning':'Fix one candidate value in one individual row. Remove it when its squared norm plus others minimum squares exceeds alpha, or any linear-coordinate interval excludes zero. Apply identical pruning to all copies of that high type and iterate.','not_checked':'Joint assignments satisfying all linear equations and the exact squared norm simultaneously'},
 'maximum_coordinate_domain_size':maximum_domain_size,'maximum_iterations':maximum_iterations,'failure_reasons':reason_counts,'groups':groups,'failures':failures,'survivor_indices':remaining,
 'base_receipt_sha256':digest(args.base),'base_verifier_sha256':r['verifier_sha256'],'source_sha256':r['source_sha256'],'verifier_sha256':digest(Path(__file__))
}
print(json.dumps(result,indent=2))
