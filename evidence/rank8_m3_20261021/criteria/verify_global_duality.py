"""Read-only exact contraction validation; --write records regenerated checks."""
import argparse,hashlib,json
from pathlib import Path
import global_duality as adapter
from exact import require

HERE=Path(__file__).resolve().parent

def run():
    census={r['id']:r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text())}
    records=[]
    for index in (334,475,1453):
        row=census[f'R8_3_{index}'];R=row['tensor'];a=adapter.engine.setup(R)
        original,rhs,indicators,meta=adapter.ORIGINAL_BUILD(R,a,4)
        mapping,pairs,n=adapter.duality_map(R,a,meta)
        actual,b,ir,after=adapter.contracted_build(R,a,4)
        require(b==rhs and ir==indicators,'right sides or indicator rows changed')
        low=sum(map(len,a['columns']));types=meta['trace_types'];end=low+len(pairs)*types
        inverse={}
        for i,j in enumerate(mapping):inverse.setdefault(j,[]).append(i)
        require(len(inverse)==n,'missing contracted column')
        for j,old in inverse.items():
            if old[0]<low or old[0]>=end:require(len(old)==1,'non-high variable was contracted')
            else:
                i,t=divmod(old[0]-low,types)
                expected=sorted(set((low+i*types+t,low+pairs[i]*types+t)))
                require(old==expected,'contraction differs from same-trace dual orbit')
        # Independently evaluate the contracted system on five complete vectors.
        # This checks every original nonzero coefficient, not a selected submatrix.
        for seed in range(5):
            x=[(j*(2*seed+3)+seed)%17 for j in range(n)]
            for old,new in zip(original,actual):
                require(sum(value*x[mapping[j]] for j,value in old.items())==sum(value*x[j] for j,value in new.items()),'substitution identity failed')
        for j,old in inverse.items():
            for r in range(len(original)):
                require(sum(original[r].get(k,0) for k in old)==actual[r].get(j,0),'contracted coefficient differs')
        model=json.loads((HERE/'advanced/global_duality_validation'/f'R8_3_{index}.json').read_text())
        require(model['tensor_sha256']==row['tensor_sha256'],'control tensor mismatch')
        require(model['status']==('excluded' if index==1453 else 'no_conclusion'),'unexpected model/negative control')
        records.append({'id':row['id'],'tensor_sha256':row['tensor_sha256'],'original_variables':meta['variables'],'contracted_variables':n,'rows':len(original),'high_columns':len(pairs),'duality_orbits':after['high_duality_orbits'],'mapping_sha256':after['duality_mapping_sha256'],'control_status':model['status']})
    return {'result':'PASS','checks':'complete duality partition and every contracted coefficient; five exact substitution vectors; two positive controls and one negative control','records':records}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();result=run();dest=HERE/'global_duality_validation.json'
    if args.write:dest.write_text(json.dumps(result,separators=(',',':'))+'\n')
    else:require(json.loads(dest.read_text())==result,'duality validation receipt differs')
    print(json.dumps(result,separators=(',',':')))
if __name__=='__main__':main()
