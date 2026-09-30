"""Compact, exact replay of the complete actual-mu48 branch reduction.

Discovery shards are input only when building a certificate.  The retained
certificate groups profile indices by independently checked integer Farkas
rays and explicitly lists every unresolved profile.  Replay reconstructs the
complete canonical induction-profile lists and all global actual-root systems;
no optimizer, discovery shard, numerical feasibility, or assertion is trusted.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import argparse, hashlib, json, sys, time
from pathlib import Path
from collections import defaultdict
import actual48 as Q
import moment48 as W
from exact import require
HERE=Path(__file__).resolve().parent
EP=[1,1,1,-1,1]


def enc(x):
    return json.loads(json.dumps(x))


def digest(x):
    return hashlib.sha256(json.dumps(x,separators=(',',':'),sort_keys=True).encode()).hexdigest()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integer(x):
    return type(x) is int


def sparse(ray,nrows,dense=False):
    if dense:
        require(len(ray)==nrows and all(integer(a) for a in ray),'invalid dense integer ray')
        ray=[[i,a] for i,a in enumerate(ray) if a]
    require(type(ray) is list,'ray is not a list')
    old=-1
    for item in ray:
        require(type(item) is list and len(item)==2,'invalid sparse ray entry')
        i,a=item
        require(integer(i) and old<i<nrows and integer(a) and a!=0,'invalid or duplicate sparse ray coordinate')
        old=i
    require(ray,'empty Farkas ray')
    return ray


def check_coefficients(rows,nv,ray):
    sparse(ray,len(rows))
    z=[0]*nv
    for i,a in ray:
        for j,b in rows[i].items():
            require(integer(j) and 0<=j<nv and integer(b),'invalid exact matrix entry')
            z[j]+=a*b
    require(all(a>=0 for a in z),'Farkas coefficient inequality fails')


def check_congruence(rows,nv,condition):
    m=condition['modulus'];ray=condition['rows']
    require(integer(m) and m>=2,'invalid congruence modulus')
    sparse(ray,len(rows))
    z=[0]*nv
    for i,a in ray:
        require(0<a<m,'noncanonical modular row coefficient')
        for j,b in rows[i].items():z[j]=(z[j]+a*b)%m
    require(not any(z),'modular coefficient divisibility fails')


def modular_value(condition,rhs):
    return sum(a*rhs[i] for i,a in condition['rows'])%condition['modulus']


def negative(ray,rhs):
    return sum(a*rhs[i] for i,a in ray)<0


def matrix(R,d,low,lab,ep):
    A,b,meta=Q.build(R,d,low,lab,ep)
    require(all(len(r)==meta['variables'] for r in A) and len(A)==len(b),'matrix dimensions disagree')
    require(all(integer(a) for r in A for a in r) and all(integer(a) for a in b),'nonintegral exact system')
    return [{j:a for j,a in enumerate(r) if a} for r in A],b,enc(meta)


def system_hash(rows,rhs,nv):
    return digest(dict(rows=[sorted(r.items()) for r in rows],rhs=rhs,variables=nv))


def load_sources(R,d,reconstruct=True):
    sources={}
    for low in range(len(d['lows'])):
        path=Q.P/f'research/round5/m8_1660/low{low}_profiles.json'
        c=json.loads(path.read_text())
        require(c['id']=='R6_8_1660' and c['selected_low']==low and c['outcome']=='complete_necessary_profile_enumeration','incomplete canonical profile source')
        require(len(c['branches'])==1,'ambiguous source branch')
        if reconstruct:
            expected=dict(c);expected.pop('seconds',None)
            fresh=Q.T.run(c['height'],20000000,low)
            require(enc(fresh)==expected,'complete canonical profile reconstruction differs')
        br=c['branches'][0]
        require(br['low']==low and br['columns']==enc(d['lows'][low]),'source low frame mismatch')
        require([a['labelling'] for a in br['cases']]==enc(list(d['tab'].assignments(d['lows'][low]))),'source character labels incomplete')
        V=br['high_vectors'];require(len({tuple(v) for v in V})==len(V),'duplicate source column')
        for case in br['cases']:
            require(all(len(p)==len(V) and all(integer(a) and a>=0 for a in p) for p in case['profiles']),'invalid source profile')
            ids=case['gram_filter']['survivor_indices']
            require(ids==sorted(set(ids)) and all(integer(i) and 0<=i<len(case['profiles']) for i in ids),'invalid canonical survivor indices')
        sources[low]=(path,br)
    return sources


def profile_matrix(rows,b,meta,br,d,low,use_moments):
    rows=list(rows)
    for v in br['high_vectors']:
        rows.append({j:1 for j,(w,a) in enumerate(meta['high_labels']) if w==v})
    md=None;extra=[]
    if use_moments:
        rr,extra,md=W.append_rows(d,d['lows'][low],meta['high_labels'],meta['variables'])
        rows+=rr
    return rows,extra,md


def code_binding(extra):
    paths={Path(__file__).resolve(),(Q.P/'data/census.json').resolve(),*(p.resolve() for p in extra)}
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name:
            path=Path(name).resolve()
            if path.is_relative_to(Q.P) and path.suffix=='.py':paths.add(path)
    return {str(p.relative_to(Q.P)):sha(p) for p in sorted(paths)}


def discovery_globals():
    found={}
    for low in (0,1):
        c=json.loads((HERE/f'low{low}_certificate.json').read_text())
        require(c['id']=='R6_8_1660' and c['complete'] is True and c['actual_twist_exponent_divides']==48,'incomplete global discovery')
        for rec in c['branches']:
            m=rec['meta'];key=(m['low'],tuple(m['labelling']),tuple(m['indicators']))
            require(key not in found and m['low']==low,'duplicate global branch')
            require(rec['outcome'] in ('exact_farkas','inconclusive'),'unrecognized global outcome')
            found[key]=rec
    return found


def ray_pool(low,lab,source,br,case,meta,rows,b,moment_rows,moment_rhs,md):
    """Validate all complete shard rays; their coverage assertions are not used."""
    pool=[];seen=set();nv=meta['variables'];nhigh=len(br['high_vectors'])
    for path in sorted(HERE.glob('profile_low*.json')):
        c=json.loads(path.read_text())
        if c.get('complete') is not True or c.get('low')!=low or c.get('labelling')!=lab:continue
        require(c['source']==str(source.relative_to(Q.P)) and c['source_sha256']==sha(source),'discovery profile source binding differs')
        require(c['id']=='R6_8_1660' and c['indicators']==EP and c['meta']==meta and c['total_profiles']==len(case['profiles']),'discovery branch metadata differs')
        require(integer(c['start']) and integer(c['stop']) and 0<=c['start']<=c['stop']<=len(case['profiles']),'invalid discovery shard range')
        require([r['index'] for r in c['profiles']]==list(range(c['start'],c['stop'])),'incomplete discovery shard')
        for rec in c['profiles']:require(rec['outcome'] in ('exact_farkas','inconclusive'),'invalid discovery profile outcome')
        for ray in c['rays']:
            check_coefficients(rows,nv,ray)
            key=tuple(map(tuple,ray))
            if key not in seen:seen.add(key);pool.append((ray,False))
    for path in sorted(HERE.glob('moment_low*.json')):
        c=json.loads(path.read_text())
        if c.get('complete') is not True or c.get('low')!=low or c.get('labelling')!=lab:continue
        require(c['id']=='R6_8_1660' and c['moment_metadata']==md,'moment discovery metadata differs')
        for source_rec in c['base']:
            p=Q.P/source_rec['path']
            require(p.exists() and sha(p)==source_rec['sha256'],'moment discovery base binding differs')
        for ray in c['rays']:
            check_coefficients(moment_rows,nv,ray)
            key=tuple(map(tuple,ray))
            if key not in seen:seen.add(key);pool.append((ray,True))
    return pool


def condition_pool(low,lab,source,case,meta,rows,md):
    pool=[];seen=set()
    for path in sorted(HERE.glob('mod*_low*.json')):
        c=json.loads(path.read_text())
        if c.get('complete') is not True or c.get('low')!=low or c.get('labelling')!=lab:continue
        require(c['id']=='R6_8_1660' and c['source_sha256']==sha(source) and c['moment_metadata']==md,'congruence discovery source or matrix differs')
        require(c['total']==len(case['gram_filter']['survivor_indices']),'congruence discovery scope differs')
        for cond in c['conditions']:
            check_congruence(rows,meta['variables'],cond)
            key=(cond['modulus'],tuple(map(tuple,cond['rows'])))
            if key not in seen:seen.add(key);pool.append(cond)
    return pool


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');ap.add_argument('--receipt',type=Path,default=HERE/'replay_O.json');ap.add_argument('--skip-profile-reconstruction',action='store_true',help='discovery-only convenience; never emits a passed receipt');args=ap.parse_args();start=time.monotonic()
    import scipy.optimize as opt
    def forbidden(*a,**k):raise RuntimeError('optimizer disabled in exact actual48 consolidation/replay')
    opt.linprog=opt.milp=forbidden
    require(args.build or not args.skip_profile_reconstruction,'canonical replay always reconstructs profile sources')
    R=next(r['N'] for r in json.loads((Q.P/'data/census.json').read_text()) if r['id']=='R6_8_1660')
    d=Q.prepare(R);sources=load_sources(R,d,not args.skip_profile_reconstruction)
    inputs=discovery_globals() if args.build else None
    expected=[(low,list(lab),list(ep)) for low,cols in enumerate(d['lows']) for lab in d['tab'].assignments(cols) for ep in Q.M.indicator_choices(R)]
    if args.build:
        require(set(inputs)=={(l,tuple(a),tuple(e)) for l,a,e in expected},'global discovery omits a necessary branch')
        cert=dict(id='R6_8_1660',scope='pseudo_unitary_necessary',actual_twist_exponent_divides=48,branches=[],complete=False)
    else:
        cert=json.loads(args.certificate.read_text())
        require(cert['id']=='R6_8_1660' and cert['scope']=='pseudo_unitary_necessary' and cert['actual_twist_exponent_divides']==48 and cert['complete'] is True,'wrong certificate scope or incomplete coverage')
        require(len(cert['branches'])==len(expected),'global branch count differs')
    identity_verified=False;summary=[]
    for ix,(low,lab,ep) in enumerate(expected):
        rows,b,meta=matrix(R,d,low,lab,ep);nv=meta['variables'];mh=system_hash(rows,b,nv)
        if args.build:
            raw=inputs[low,tuple(lab),tuple(ep)]
            require(raw['meta']==meta,'global discovery matrix metadata changed')
            # Check the original dense matrix digest as well as every exact ray.
            A=[[row.get(j,0) for j in range(nv)] for row in rows]
            require(raw['system_sha256']==hashlib.sha256(json.dumps([A,b],separators=(',',':')).encode()).hexdigest(),'global discovery matrix changed')
            rec=dict(low=low,labelling=lab,indicators=ep,system_sha256=mh)
            if raw['outcome']=='exact_farkas':
                ray=sparse(raw['ray'],len(rows),dense=True);check_coefficients(rows,nv,ray);require(negative(ray,b),'global Farkas rhs fails')
                rec.update(outcome='exact_farkas',ray=ray);cert['branches'].append(rec);summary.append(dict(low=low,labelling=lab,indicators=ep,outcome='exact_farkas'));continue
        else:
            rec=cert['branches'][ix]
            require((rec['low'],rec['labelling'],rec['indicators'])==(low,lab,ep) and rec['system_sha256']==mh,'branch identity or exact matrix differs')
            require(rec['outcome'] in ('exact_farkas','profile_frontier'),'invalid certificate branch outcome')
            if rec['outcome']=='exact_farkas':
                check_coefficients(rows,nv,rec['ray']);require(negative(rec['ray'],b),'global Farkas rhs fails');summary.append(dict(low=low,labelling=lab,indicators=ep,outcome='exact_farkas'));continue
        require(ep==EP,'a surviving indicator branch has no profile specialization')
        source,br=sources[low];case=next(c for c in br['cases'] if c['labelling']==lab);ids=case['gram_filter']['survivor_indices'];base_rows,_,_=profile_matrix(rows,b,meta,br,d,low,False)
        if args.build:
            allrows,extra,md=profile_matrix(rows,b,meta,br,d,low,True)
            pool=ray_pool(low,lab,source,br,case,meta,base_rows,b,allrows,extra,md)
            conditions=condition_pool(low,lab,source,case,meta,allrows,md)
            groups=defaultdict(list);modgroups=defaultdict(list);unresolved=[]
            for j in ids:
                rhs=b+case['profiles'][j]+extra
                hit=next((k for k,(ray,is_moment) in enumerate(pool) if negative(ray,rhs)),None)
                if hit is not None:groups[hit].append(j)
                else:
                    hit=next((k for k,c in enumerate(conditions) if modular_value(c,rhs)),None)
                    if hit is None:unresolved.append(j)
                    else:modgroups[hit].append(j)
            uses=any(any(i>=len(base_rows) for i,a in pool[k][0]) for k in groups) or any(any(i>=len(base_rows) for i,a in conditions[k]['rows']) for k in modgroups)
            selected_rows=allrows if uses else base_rows;selected_extra=extra if uses else []
            rec.update(outcome='profile_frontier',source=str(source.relative_to(Q.P)),source_sha256=sha(source),canonical_indices=ids,moments=uses,groups=[dict(ray=pool[k][0],profiles=v) for k,v in sorted(groups.items())],modular_groups=[dict(condition=conditions[k],profiles=v) for k,v in sorted(modgroups.items())],unresolved=unresolved,profile_matrix_sha256=system_hash(selected_rows,b+[0]*len(br['high_vectors'])+selected_extra,nv))
            if uses:rec['moment_metadata']=md
            cert['branches'].append(rec)
        else:
            require(rec['source']==str(source.relative_to(Q.P)) and rec['source_sha256']==sha(source) and rec['canonical_indices']==ids,'canonical profile coverage/source mismatch')
            require(type(rec['moments']) is bool,'invalid moment flag')
            selected_rows,selected_extra,md=profile_matrix(rows,b,meta,br,d,low,rec['moments'])
            require(rec['profile_matrix_sha256']==system_hash(selected_rows,b+[0]*len(br['high_vectors'])+selected_extra,nv),'profile matrix changed')
            if rec['moments']:require(rec['moment_metadata']==md,'moment source metadata changed')
        if rec['moments'] and not identity_verified:W.verify_identity_source();identity_verified=True
        covered=[]
        for group in rec['groups']:
            check_coefficients(selected_rows,nv,group['ray'])
            require(group['profiles']==sorted(set(group['profiles'])) and group['profiles'],'invalid Farkas profile group')
            for j in group['profiles']:
                require(integer(j) and j in ids,'Farkas group names a noncanonical profile')
                require(negative(group['ray'],b+case['profiles'][j]+selected_extra),'profile Farkas rhs fails')
            covered+=group['profiles']
        modular_excluded=0
        for group in rec['modular_groups']:
            check_congruence(selected_rows,nv,group['condition'])
            require(group['profiles']==sorted(set(group['profiles'])) and group['profiles'],'invalid modular profile group')
            for j in group['profiles']:
                require(integer(j) and j in ids,'modular group names a noncanonical profile')
                require(modular_value(group['condition'],b+case['profiles'][j]+selected_extra)!=0,'profile modular rhs vanishes')
            covered+=group['profiles'];modular_excluded+=len(group['profiles'])
        unresolved=rec['unresolved'];require(unresolved==sorted(set(unresolved)) and all(integer(j) for j in unresolved),'invalid unresolved profile list')
        require(len(covered)==len(set(covered)) and sorted(covered+unresolved)==ids,'profile partition overlaps or misses a canonical index')
        summary.append(dict(low=low,labelling=lab,indicators=ep,outcome='profile_frontier',profiles=len(ids),excluded=len(covered),unresolved=unresolved,rays=len(rec['groups']),modular_conditions=len(rec['modular_groups']),modular_excluded=modular_excluded,moments=rec['moments']))
        print('profile branch',low,lab,'excluded',len(covered),'remaining',len(unresolved),flush=True)
    extras=[p for p,br in sources.values()]
    if identity_verified:extras.append(W.SOURCE)
    binding=code_binding(extras)
    if args.build:
        cert['complete']=True;cert['files_sha256']=binding;cert['summary']=summary;args.certificate.write_text(json.dumps(cert,separators=(',',':'))+'\n')
    else:require(cert['files_sha256']==binding and cert['summary']==summary,'source closure or summary differs')
    all_excluded=all(r['outcome']=='exact_farkas' or not r['unresolved'] for r in cert['branches'])
    report=dict(passed=not args.skip_profile_reconstruction,optimizer_used=False,optimized_python=not __debug__,global_branches=len(expected),global_excluded=sum(s['outcome']=='exact_farkas' for s in summary),profile_branches=[s for s in summary if s['outcome']=='profile_frontier'],all_actual48_branches_excluded=all_excluded,categorical_construction_claimed=False,files_sha256=dict(binding,**{str(args.certificate.resolve().relative_to(Q.P)):sha(args.certificate)}),seconds=round(time.monotonic()-start,4))
    if not args.skip_profile_reconstruction:args.receipt.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=report['passed'],optimizer_used=False,global_branches=len(expected),global_excluded=report['global_excluded'],profile_counts=[dict(low=r['low'],labelling=r['labelling'],remaining=len(r['unresolved']),excluded=r['excluded'],rays=r['rays'],modular_conditions=r['modular_conditions']) for r in report['profile_branches']],seconds=report['seconds'])),flush=True)

if __name__=='__main__':main()
