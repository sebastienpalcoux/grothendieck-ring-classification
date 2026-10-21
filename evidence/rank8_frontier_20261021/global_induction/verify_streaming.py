"""Exact coefficient and full-oracle comparison with the published operator."""
import argparse,json
from fractions import Fraction as Q
import streaming as new
import global_duality as frozen

def validate():
    records=[]
    for n in (334,1453,920,986):
        source=new.load_ring(f'R8_3_{n}');R=source['tensor'];a=new.old.setup(R)
        full=len(a['high'])
        if n in (920,986):
            du=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
            vectors={tuple(v) for v,z in a['high'][:64]};vectors|={tuple(v[du[k]-1] for k in range(1,8)) for v in list(vectors)}
            a=dict(a,high=[h for h in a['high'] if tuple(h[0]) in vectors])
        cone=new.Cone(R,4,a);A,b,ir,meta=frozen.contracted_build(R,a,4)
        new.require(meta['variables']==cone.nvars and len(A)==cone.nrows,'operator sizes differ')
        ep=new.old.ht.indicator_choices(R)[0];A,b=new.old.integers(A,b,ir,a['global_dimension'],ep);rhs=cone.rhs_for(ep)
        ratios=[Q(x,y) if y else None for x,y in zip(rhs,b)]
        for j in range(cone.nvars):
            col=cone.column(j)
            for i in range(cone.nrows):
                x=col.get(i,0);y=A[i].get(j,0)
                new.require(bool(x)==bool(y),'coefficient support differs')
                if y:
                    ratio=Q(x,y)
                    if ratios[i] is None:ratios[i]=ratio
                    new.require(ratios[i]==ratio,'streamed coefficient differs from published matrix')
        new.require(all((Q(x)==ratio*y if ratio is not None else x==y==0) for x,y,ratio in zip(rhs,b,ratios)),'streaming right side differs')
        for seed in range(3):
            y=[((i*17+seed*29)%31)-15 for i in range(cone.nrows)]
            scores=[sum(y[i]*x for i,x in cone.column(j).items()) for j in range(cone.nvars)]
            report=cone.oracle(y,limit=cone.nvars)
            new.require(report['minimum']==min(0,min(scores)) and report['negative_columns']==sum(x<0 for x in scores),'factored oracle differs from complete direct scan')
            new.require(set(report['violating_columns'])=={j for j,x in enumerate(scores) if x<0},'oracle omitted a violating column')
        records.append({'id':source['id'],'tensor_sha256':source['tensor_sha256'],'full_high_domain':full,'compared_high_domain':len(a['high']),'rows':cone.nrows,'columns':cone.nvars,'domain_sha256':cone.meta['domain_sha256'],'full_coefficient_comparison':True,'complete_oracle_controls':3})
        print(source['id'],'PASS',cone.nrows,cone.nvars,flush=True)
    return {'result':'PASS','records':records}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();out=validate();path=new.HERE/'streaming_validation.json'
    if args.write:path.write_text(json.dumps(out,separators=(',',':'))+'\n')
    else:new.require(json.loads(path.read_text())==out,'streaming validation receipt differs')
if __name__=='__main__':main()
