"""Read-only exact validation of isolated generic field/data adapters."""
import argparse,json
import generic_data as gd
import streaming as st
from exact import require

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    import general_biquadratic as frozen
    records=[]
    for q,r,primes in ((2,3,[2,3]),(3,5,[2,3,5]),(3,7,[2,3,7]),(3,13,[2,3,13])):
        f=gd.Field(q,r,primes);frozen.configure(q,r);frozen.PRIMES=primes
        for h in (4,6):
            a=f.traces(h);b=frozen.trace_types(h);require(a==b,'isolated trace domain differs');records.append({'radicands':[q,r],'height':h,'bound':a[1],'types':len(a[0]),'domain_sha256':st.digest(a)})
        for h in range(3,7):
            rs=list(map(int,gd.s.divisors(h)[:-1]));require(f.rotations(h,rs)==frozen.trace_types(h,gd.s.divisors(h),rs)[0],'isolated rotation domain differs')
        # Reconfigure the frozen module, then prove the object stayed bound.
        before=f.traces(4);frozen.configure(17,19);require(f.traces(4)==before,'field object depends on global radicands')
    source=st.load_ring('R8_3_901');a=gd.setup(source['tensor'],3,5)
    import general_global_convex as legacy
    legacy.install(3,5);b=st.old.setup(source['tensor'])
    fields=['dimensions','global_dimension','columns','high','field']
    for name in fields:require(a[name]==b[name],'isolated source data differs: '+name)
    require(a['B']==b['B'] and a['codegrees']==b['codegrees'],'isolated spectral data differs')
    records.append({'id':source['id'],'tensor_sha256':source['tensor_sha256'],'data_sha256':st.digest([a[name] for name in fields]),'low_counts':list(map(len,a['columns'])),'high_count':len(a['high'])})
    out={'result':'PASS','records':records,'scope':'exact formula/data equivalence; no categorification claim'};dest=st.HERE/'generic_validation.json'
    if args.write:dest.write_text(json.dumps(out,separators=(',',':'))+'\n')
    else:require(json.loads(dest.read_text())==out,'generic validation receipt differs')
    print('PASS isolated generic fields and complete R901 data',flush=True)
if __name__=='__main__':main()
