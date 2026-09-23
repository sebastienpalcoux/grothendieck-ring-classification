#!/usr/bin/env python3
"""Independently replay the complete compressed bounded-classification proof.

Every source tensor and input identity is rechecked. Arithmetic witnesses are
recomputed exactly and every required bounded search is rerun; generator statuses
and checkpoint files are never trusted. Census completeness is documented
by the pinned source repository; the supplied tensors are audited here.
"""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,csv,gzip,hashlib,itertools,json,multiprocessing,platform,sys,time,traceback
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'software'))
from exact import require
from census_data import iter_parameters,parameter_tensor,record_metadata,read_manifest
from rapid import check_dnumber


def init_worker(engine):
    global MODELS,SEARCH
    from signed import Search
    MODELS=json.loads((ROOT/'data/models.json').read_text());SEARCH=Search(engine)


def verify_task(value):
    row,tag,p=value
    from dispatch import check
    check(parameter_tensor(tag,p),row['certificate'],MODELS,SEARCH)
    return row['source_index']


def verify_identity(row,sid,tag,p):
    metadata=record_metadata(sid,tag,p)
    require(all(row.get(k)==v for k,v in metadata.items()),'input identification mismatch at '+str(sid))
    c=row.get('certificate');require(isinstance(c,dict),'unresolved certificate at '+str(sid))
    status='realized' if c['kind']=='model' else 'excluded'
    require(row.get('status')==status,'unproved status at '+str(sid))
    return metadata,status,c


GROUPS={
 'arithmetic_dnumbers':['dnumber'], 'subring_dimensions':['subring'],
 'nonselfdual_quadratic_moments':['Sm'], 'cyclotomicity':['cyclotomic'],
 'signed_dimension_characters':['signed','spherical','signed_characters','zero','duality','galois_fp','unsigned_gauge'],
 'normalized_norms':['norm','all_norms','det_prime'],
 'low_induction_and_moments':['induction','moment','gram_minor','gram_entry','rank_two_moment','diagonal_involution_moments','involution_propagation_42','involution_moment'],
 'quadratic_root_length':['root_length','near_group_root_length'],
 'dimension_field_containment':['field_prime','field_degree'], 'central_sign_moments':['sign_moments'],
 'spherical_global_moments':['spherical_global_moment','global_codegree_moment'],
 'signed_adjoint_parity':['signed_adjoint_parity'], 'literature_near_group':['literature_near_group'],
 'weak_integral_reduction':['weak_integral'], 'two_dimension_Galois_reduction':['two_dimensions'],
}


class CriterionUsage:
    def __init__(self):self.counts=Counter();self.first={};self.ring_counts=Counter();self.examples=defaultdict(list);self.compact=Counter();self.methods=defaultdict(Counter)
    def add(self,row):
        seen=set();m=row['multiplicity'];label=row['label']
        def walk(value):
            if isinstance(value,dict):
                k=value.get('kind')
                if isinstance(k,str):self.counts[k]+=1;self.first[k]=min(self.first.get(k,m),m);seen.add(k)
                for v in value.values():walk(v)
            elif isinstance(value,list):
                for v in value:walk(v)
        walk(row['certificate'])
        for k in seen:
            self.ring_counts[k]+=1
            if len(self.examples[k])<5:self.examples[k].append(label)
        enum=row['certificate'].get('enumeration')
        if enum and enum['method']=='global_signed_catalog_v3':
            method=enum['method'];self.methods[method]['records']+=1;self.methods[method]['retained_tables']+=enum['retained_tables'];self.methods[method]['eligible_orbits']+=enum['eligible_orbits']
            self.compact['retained']+=enum['retained_tables']
        elif enum:
            self.methods[enum['method']]['records']+=1;self.methods[enum['method']]['enumerated_associative_tuples']+=enum['total'];self.methods[enum['method']]['retained']+=enum['retained']
            self.compact['total_signed_candidates']+=enum['total'];self.compact['determinant_rejections']+=sum(enum['determinant_rejections']);self.compact['parity_rejections']+=enum['parity_rejections'];self.compact['retained']+=enum['retained']
    def report(self):
        grouped={k:min(self.first[x] for x in values if x in self.first) for k,values in GROUPS.items() if any(x in self.first for x in values)}
        return {'counts':dict(self.counts),'first_multiplicity':self.first,'ring_counts':dict(self.ring_counts),'example_labels':dict(self.examples),
            'group_definitions':GROUPS,'grouped_first_multiplicity':grouped,'largest_grouped_first_use':max(grouped.values(),default=None),
            'first_use_of_new_central_sign_obstruction':self.first.get('sign_moments'),'compact_signed_enumeration':dict(self.compact),'signed_enumeration_methods':{k:dict(v) for k,v in self.methods.items()},
            'interpretation':'First-use statistics refer to this ordering and grouping; they do not establish toolkit minimality or completeness at unbounded multiplicity. Counts for compact preliminary rejections are recorded separately. Under parity_domains_diophantine_v2, total counts only parity-admissible associative tuples; the complementary parameter domains are eliminated symbolically.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--engine',choices=['cpp','python'],default='cpp')
    p.add_argument('--workers',type=int,default=4);p.add_argument('--certificates',type=Path,default=ROOT/'certificates/classification.jsonl.gz')
    p.add_argument('--global-threads',type=int,default=4);p.add_argument('--global-workers',type=int,default=1);p.add_argument('--wait-for-certificates',type=float,default=0,metavar='SECONDS')
    args=p.parse_args();started=time.monotonic()
    from audit import audit_census_inputs
    census=audit_census_inputs(ROOT)
    global_proof=None
    if (ROOT/'data/signed_universal_128_manifest.json').exists():
        from global_signed import verify_global_catalog
        global_proof=verify_global_catalog(workers=args.global_workers,threads=args.global_threads)
    deadline=time.monotonic()+args.wait_for_certificates;last_notice=0
    while not args.certificates.exists():
        if time.monotonic()>=deadline:raise FileNotFoundError('Finish generation and atomic certificate merge before verification: '+str(args.certificates))
        if time.monotonic()-last_notice>=30:
            print('GLOBAL GATE PASSED; waiting for atomic classification file.',flush=True);last_notice=time.monotonic()
        time.sleep(min(2,max(0,deadline-time.monotonic())))
    manifest=read_manifest();models=json.loads((ROOT/'data/models.json').read_text());require(len(models)==15,'wrong model-table size')
    out=ROOT/'verification';out.mkdir(exist_ok=True);counts=Counter();types=Counter();by_m=defaultdict(Counter);usage=CriterionUsage();signed_total=0;checked=0;tasks=[]
    ledger_tmp=out/'ledger.csv.gz.tmp'
    with gzip.open(args.certificates,'rt') as proof,gzip.open(ledger_tmp,'wt',newline='') as ledger,multiprocessing.Pool(args.workers,initializer=init_worker,initargs=(args.engine,)) as pool:
        header=json.loads(next(proof));require(header.get('schema')==2,'wrong certificate schema')
        require(header.get('scope')=='rank4_multiplicity_at_most_128' and header.get('bound')==128 and header.get('records')==manifest['rings'],'wrong coverage scope')
        require(header.get('census_commit')==manifest['commit'] and header.get('parameters_sha256')==manifest['parameters_gz_sha256'],'wrong census identity')
        w=csv.DictWriter(ledger,fieldnames=['index','source_index','old_index','multiplicity','local_index','label','sha256','status','criterion']);w.writeheader()
        for parameter,line in itertools.zip_longest(iter_parameters(),proof):
            require(parameter is not None and line is not None,'certificate coverage length mismatch')
            sid,tag,pars=parameter;row=json.loads(line);meta,status,c=verify_identity(row,sid,tag,pars)
            if c['kind']=='dnumber':check_dnumber(parameter_tensor(tag,pars),c)
            else:tasks.append(pool.apply_async(verify_task,((row,tag,pars),)))
            counts[status]+=1;types[c['kind']]+=1;by_m[meta['multiplicity']][status]+=1;usage.add(row);checked+=1
            if c['kind']=='signed':
                enum=c.get('enumeration',{});signed_total+=enum.get('total',enum.get('retained_tables',len(c['tables'])))
            w.writerow({**meta,'status':status,'criterion':c['kind']})
            if checked%100000==0:print('CHECKED INPUTS',checked,'of',manifest['rings'],'elapsed',round(time.monotonic()-started,1),flush=True)
        for i,result in enumerate(tasks,1):
            result.get()
            if i%1000==0:print('CHECKED NON-DNUMBER WITNESSES',i,'of',len(tasks),flush=True)
    require(checked==manifest['rings'] and counts['realized']==15 and counts['excluded']==checked-15,'unexpected classification totals')
    ledger_tmp.replace(out/'ledger.csv.gz')
    import sympy,flint
    summary={'checked_rings':checked,'counts':dict(counts),'unresolved_count':0,'top_level_criteria':dict(types),
        'signed_records':types['signed'],'checked_signed_tables':signed_total,'signed_candidate_count_definition':'Sum of associative tuples explicitly enumerated by each certificate backend; v2 first removes parity-forbidden domains symbolically; v3 counts retained per-ring tables after the separately verified shared global catalog.','by_multiplicity':dict(by_m),
        'engine':args.engine,'workers':args.workers,'python':platform.python_version(),'sympy':sympy.__version__,'python_flint':flint.__version__,
        'elapsed_seconds':round(time.monotonic()-started,3),'certificate_sha256':hashlib.sha256(args.certificates.read_bytes()).hexdigest(),
        'census_audit':census,'global_signed_catalog':global_proof,'categorical_soundness':'Relies on the proved and cited criteria in the finite manuscript; not proof-assistant formalization.'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');(out/'criterion_usage.json').write_text(json.dumps(usage.report(),indent=2)+'\n')
    print('PASS: every census tensor, every certificate, and every required signed enumeration.',flush=True)
    print('PASS:',dict(counts),'0 unresolved;',signed_total,'signed candidates checked.',flush=True)
    print('Elapsed seconds:',round(time.monotonic()-started,2),flush=True)
if __name__=='__main__':
    try:main()
    except Exception:traceback.print_exc();sys.exit(1)
