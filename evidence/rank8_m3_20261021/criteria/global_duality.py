"""Exact duality contraction of the global central-induction relaxation.

This module is isolated at replay: base certificates retain their original
uncontracted systems. Dual restriction/trace types have equal multiplicity
in a ribbon center and therefore may share one nonnegative variable.
"""
from pathlib import Path
import argparse,hashlib,json,os,sys,time,traceback
import global_induction as engine
from exact import require
ORIGINAL_BUILD=engine._build
_installed=False
_configuration=None

def duality_map(R,a,metadata):
    du=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    require(all(du[du[i]]==i for i in range(8)),'basis duality not involutive')
    high=a['high'];lookup={tuple(v):i for i,(v,z) in enumerate(high)}
    require(len(lookup)==len(high),'duplicate high restriction vector')
    pairs=[]
    for i,(v,z) in enumerate(high):
        vd=tuple(v[du[j]-1] for j in range(1,8));j=lookup.get(vd)
        require(j is not None,'complete high set not dual closed')
        require(tuple(high[j][1])==tuple(z),'dual restriction dimensions differ')
        pairs.append(j)
    require(all(pairs[pairs[i]]==i for i in range(len(high))),'high duality not involutive')
    offset=sum(map(len,a['columns']));trace_count=metadata['trace_types'];high_end=offset+len(high)*trace_count
    mapping=list(range(offset));groups={};nextvar=offset
    for i in range(len(high)):
        orbit=min(i,pairs[i])
        for ti in range(trace_count):
            key=(orbit,ti)
            if key not in groups:groups[key]=nextvar;nextvar+=1
            mapping.append(groups[key])
    for j in range(high_end,metadata['variables']):mapping.append(nextvar);nextvar+=1
    require(len(mapping)==metadata['variables'] and set(mapping)==set(range(nextvar)),'contraction loses a variable class')
    return mapping,pairs,nextvar

def contracted_build(R,a,height):
    rows,rhs,indicators,metadata=ORIGINAL_BUILD(R,a,height)
    mapping,pairs,nextvar=duality_map(R,a,metadata)
    for at,row in enumerate(rows):
        out={}
        for j,value in row.items():
            k=mapping[j];out[k]=out.get(k,0)+value
        rows[at]={j:value for j,value in out.items() if value}
    metadata=dict(metadata,variables=nextvar,uncontracted_variables=metadata['variables'],high_duality_orbits=len(set(min(i,pairs[i]) for i in range(len(pairs)))),duality_mapping_sha256=hashlib.sha256(json.dumps(mapping,separators=(',',':')).encode()).hexdigest(),duality_contracted=True)
    return rows,rhs,indicators,metadata

def install(radicands=None):
    global _installed,_configuration
    configuration=tuple(radicands) if radicands is not None else None
    if _installed:
        require(configuration==_configuration,'field adapter reused with different radicands')
        return
    if radicands is not None:
        import general_global_convex
        general_global_convex.install(*radicands)
    engine._build=contracted_build;engine._system_cache.clear();engine.install();_installed=True;_configuration=configuration

def verify(R,c):
    require(c['kind']=='global_duality_induction_lift','wrong duality-convex certificate')
    install(c.get('radicands'));engine.verify(R,{'kind':'global_convex_induction_lift','general':c['general']})

def run(row,height,dest,radicands=None):
    start=time.monotonic();out={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'mode':'global_duality_convex','status':'running'}
    if radicands is not None:out['radicands']=list(radicands)
    dest.parent.mkdir(parents=True,exist_ok=True)
    def save():
        out['seconds']=round(time.monotonic()-start,3);temporary=dest.with_suffix('.tmp');temporary.write_text(json.dumps(out,separators=(',',':'))+'\n');temporary.replace(dest)
    def progress(c):out.update(status='partial_indicator_certificate',partial_certificate=c);save()
    seeds=[]
    if dest.exists():
        old=json.loads(dest.read_text())
        if old.get('tensor_sha256')==row['tensor_sha256']:seeds=[old[k] for k in ('partial_certificate','pseudo_certificate') if k in old]
    try:
        install(radicands)
        # Every old ray is merely a proposal: engine.certificate checks it against
        # every exact contracted coefficient before it can become a seed.
        a=engine.setup(row['tensor']);metadata=engine.build(row['tensor'],a,height)[3]
        out['report']=metadata;out['status']='system_constructed';save()
        for path in (engine.HERE/'advanced').glob('global*/'+row['id']+'.json'):
            old=json.loads(path.read_text())
            if old.get('tensor_sha256')!=row['tensor_sha256']:continue
            for key in ('partial_certificate','pseudo_certificate'):
                if key in old and old[key].get('height')==height:
                    seeds.append(dict(old[key],metadata=metadata))
        pseudo,report=engine.certificate(row['tensor'],height,progress,seeds);out['report']=report
        if pseudo:
            out.pop('partial_certificate',None);out.update(status='pseudo_certificate_pending_replay',pseudo_certificate=pseudo);save()
            import character_induction
            general=character_induction.lift_general(row['tensor'],pseudo,120)
            if general:
                c={'kind':'global_duality_induction_lift','general':general}
                if radicands is not None:c['radicands']=list(radicands)
                verify(row['tensor'],c);out.update(status='excluded',scope='general_complex_fusion_category',certificate=c)
            else:engine.verify_pseudo(row['tensor'],pseudo);out['status']='pseudo_unitary_only'
        else:out['status']='no_conclusion'
    except MemoryError as exc:out.update(status='resource_bound',error=repr(exc),memory_limit_mb=int(os.environ.get('RANK8_GLOBAL_MEMORY_MB','0')))
    except Exception as exc:out.update(status='error',error=repr(exc),traceback=traceback.format_exc())
    save();print(row['id'],out['status'],out['seconds'],flush=True)
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ring',required=True);ap.add_argument('--height',type=int,default=4);ap.add_argument('--tag',default='global_duality');ap.add_argument('--q',type=int);ap.add_argument('--r',type=int);args=ap.parse_args()
    row=next(r for r in json.loads((engine.HERE.parent/'pipeline/census_m3.json').read_text()) if r['id']==args.ring)
    require((args.q is None)==(args.r is None),'both radicands required')
    return run(row,args.height,engine.HERE/'advanced'/args.tag/(args.ring+'.json'),[args.q,args.r] if args.q else None)
if __name__=='__main__':main()
