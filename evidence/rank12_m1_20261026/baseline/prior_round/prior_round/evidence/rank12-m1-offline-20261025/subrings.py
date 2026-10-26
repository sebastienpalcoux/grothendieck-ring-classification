"""Exclusion by actual closed based subrings, with explicit direct witnesses."""
from pathlib import Path
import collections,json,sys,time
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/work/rank11/arithmetic/legacy'))
sys.path.insert(0,str(ROOT/'sources/work/rank11'))
import arithmetic as ar, gng, noncomm_integral,common

def main():
    start=time.monotonic();data=json.loads((ROOT/'tensors.json').read_text())
    profiles=json.loads((ROOT/'profile.json').read_text())['records']
    classes=[];buckets=collections.defaultdict(list);out=[]
    for p in profiles:
        R=data[p['id']];proofs=[];sublist=[]
        for J in p['subrings']:
            if len(J)in(1,12):continue
            S=[[[R[i][j][k]for k in J]for j in J]for i in J];key=common.coarse(S)
            match=None;perm=None
            for ix in buckets[key]:
                perm=common.based_iso(S,classes[ix]['tensor'])
                if perm is not None:match=ix;break
            if match is None:
                match=len(classes);buckets[key].append(match);c=None
                for fn in [ar.near_group,ar.dnumber,gng.certificate,ar.integral_drinfeld,noncomm_integral.test,ar.cyclotomic]:
                    c=fn(S)
                    if c:break
                classes.append(dict(tensor=S,tensor_sha256=ar.sha(S),certificate=c))
                perm=list(range(len(J)))
            sublist.append(dict(subset=J,class_index=match,source_to_class_basis_map=perm))
            c=classes[match]['certificate']
            if c:
                proofs.append(dict(kind='excluded_subring',subset=J,class_index=match,source_to_class_basis_map=perm,scope='general_complex_fusion_category'))
        out.append(dict(id=p['id'],tensor_sha256=ar.sha(R),subrings=sublist,certificates=proofs[:1]))
    (ROOT/'subrings.json').write_text(json.dumps(dict(classes=classes,records=out,elapsed_seconds=time.monotonic()-start),indent=2)+'\n')
    print('DONE',len(out),'subring classes',len(classes),'excluded',sum(bool(r['certificates'])for r in out),'seconds',time.monotonic()-start)

if __name__=='__main__':main()
