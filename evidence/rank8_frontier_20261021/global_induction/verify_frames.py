"""Exact frame-column and oracle checks; default is read-only."""
import argparse,json
from fractions import Fraction as Q
import frame_cone as f
import streaming as st
import global_duality as frozen

def validate():
    records=[]
    for n in (334,1453,1739):
        source=st.load_ring(f'R8_3_{n}');R=source['tensor'];a=st.old.setup(R)
        # All low frames, and a duality-closed high subdomain, are sufficient
        # to test contraction while keeping the explicit reference small.
        du=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
        vectors={tuple(v) for v,z in a['high'][:16]};vectors|={tuple(v[du[k]-1] for k in range(1,8)) for v in list(vectors)}
        a=dict(a,high=[h for h in a['high'] if tuple(h[0]) in vectors])
        C=f.FrameCone(R,4,a);A,b,ir,meta=frozen.contracted_build(R,a,4)
        ep=st.old.ht.indicator_choices(R)[0];A,b=st.old.integers(A,b,ir,a['global_dimension'],ep)
        # Obtain the positive row scaling independently from each atom.
        ratios=[Q(x,y) if y else None for x,y in zip(C.rhs_for(ep),b)]
        for j,col in enumerate(C.atom_columns):
            for i,row in enumerate(A):
                x=col.get(i,0);y=row.get(j,0);st.require(bool(x)==bool(y),'atomic support differs')
                if y:
                    ratio=Q(x,y)
                    if ratios[i] is None:ratios[i]=ratio
                    st.require(ratios[i]==ratio,'atomic row scaling differs')
        sample=list(range(min(30,len(C.frames))))+list(range(0,len(C.frames),max(1,len(C.frames)//101)))
        for j in sorted(set(sample)):
            col=C.column(j)
            for i,row in enumerate(A):
                expected=sum(row.get(k,0) for k in C.frames[j])
                st.require(Q(col.get(i,0))==(ratios[i] or 1)*expected,'frame does not equal published atom sum')
        for seed in range(3):
            y=[((i*17+seed*29)%31)-15 for i in range(C.nrows)]
            atomic=[sum(y[i]*v for i,v in col.items()) for col in C.atom_columns]
            low=[sum(atomic[k] for k in frame) for frame in C.frames]
            high=[sum(y[i]*v for i,v in C.column(j).items()) for j in range(C.offset,C.nvars)]
            scores=low+high;report=C.oracle(y,limit=C.nvars)
            st.require(report['minimum']==min(0,min(scores)),'frame oracle minimum differs')
            st.require(set(report['violating_columns'])=={j for j,v in enumerate(scores) if v<0},'frame oracle is incomplete')
        records.append({'id':source['id'],'tensor_sha256':source['tensor_sha256'],'frames':len(C.frames),'frame_domain_sha256':C.meta['frame_domain_sha256'],'published_column_sum_checks':len(set(sample)),'complete_oracle_controls':3})
        print(source['id'],'PASS',len(C.frames),flush=True)
    return {'result':'PASS','records':records}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();result=validate();dest=st.HERE/'frame_validation.json'
    if args.write:dest.write_text(json.dumps(result,separators=(',',':'))+'\n')
    else:st.require(json.loads(dest.read_text())==result,'frame validation receipt differs')
if __name__=='__main__':main()
