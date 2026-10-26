from pathlib import Path
import json,sys,time
import sympy as s
from fp import fp_character,exact,require
from state import current
from field_checks import pu_gate
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/work/rank11'))
sys.path.insert(0,str(ROOT/'sources/work/rank11/arithmetic/legacy'))
import arithmetic as ar
import compression

def main():
    start=time.monotonic();data=json.loads((ROOT/'tensors.json').read_text());ex,mo=current();rows=[]
    for p in json.loads((ROOT/'profile.json').read_text())['records']:
        rid=p['id']
        if rid in ex or rid in mo:continue
        R=data[rid];cs=[];rep,c=compression.discover(R)
        if c:cs.append(dict(c,scope='general_complex_fusion_category'))
        gate=pu_gate(R,p)
        if gate:
            f,K,u,ds,D,emb=fp_character(R);B=ar.casimir(R);w=s.trace(B.inv()**2)
            gap=K(2*w)-K.one-K.one/D
            if emb.sign(gap)>0:cs.append(dict(kind='PU_codegree_reciprocal_square',gate=gate,inverse_square_sum=str(w),gap=exact.ec(gap),scope='general_complex_fusion_category'))
            if ar.comm(R):
                S=sum((ds[i]for i in range(len(R))if p['dual'][i]==i),K.zero);h=K(w)*D*D
                gap=K(2)*(D-h)**2-(D*D-h)*(D*D+D*S-K(2)*h)
                if emb.sign(gap)>0:cs.append(dict(kind='PU_global_two_moment',gate=gate,inverse_square_sum=str(w),S=exact.ec(S),gap=exact.ec(gap),scope='general_complex_fusion_category'))
        rows.append(dict(id=rid,tensor_sha256=ar.sha(R),certificates=cs,compression_check=rep))
    (ROOT/'more_criteria.json').write_text(json.dumps(dict(records=rows,elapsed_seconds=time.monotonic()-start),indent=2)+'\n')
    print('checked',len(rows),'excluded',sum(bool(r['certificates'])for r in rows),'seconds',time.monotonic()-start)
if __name__=='__main__':main()
