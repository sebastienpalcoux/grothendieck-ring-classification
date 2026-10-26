"""Short zero/one spectrum scans, with independent exact witness checking."""
from pathlib import Path
import json,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/evidence/rank11_m1_20261023/work/rank11/structural'))
from verify_baseline import spectrum

def main():
    data=json.loads((ROOT/'tensors.json').read_text());excluded=set()
    for f in ['arithmetic.json','subrings.json']:
        q=json.loads((ROOT/f).read_text());rs=q['records']if isinstance(q,dict)else q
        excluded.update(r['id']for r in rs if r['certificates'])
    allresults={}
    for kind in ['zero_spectrum','one_spectrum']:
        # Skip a second search after an exact arbitrary-complex obstruction.
        rows=[(rid,R)for rid,R in data.items()if rid not in excluded]
        with (ROOT/(kind+'.input')).open('w')as f:
            f.write(str(len(rows))+'\n')
            for rid,R in rows:f.write('12 '+' '.join(str(x)for A in R for B in A for x in B)+'\n')
        subprocess.run(['g++','-std=c++17','-O3',str(ROOT/(kind+'.cpp')),'-o',str(ROOT/kind)],check=True)
        start=time.monotonic();complete=True
        with (ROOT/(kind+'.input')).open()as inp,(ROOT/(kind+'.output')).open('w')as out:
            try:subprocess.run([str(ROOT/kind)],stdin=inp,stdout=out,check=True,timeout=45)
            except subprocess.TimeoutExpired:complete=False
        records=[];found=[]
        for line in (ROOT/(kind+'.output')).read_text().splitlines():
            v=list(map(int,line.split()));i,has=v[:2];rid,R=rows[i]
            if has:
                c=dict(kind=kind,indices=v[2:],scope='general_complex_fusion_category')
                spectrum(R,c);found.append(rid);excluded.add(rid)
            else:c=None
            records.append(dict(id=rid,certificate=c))
        allresults[kind]=dict(complete=complete,attempted=len(rows),completed=len(records),excluded=found,records=records,elapsed_seconds=time.monotonic()-start)
        (ROOT/'spectra.json').write_text(json.dumps(allresults,indent=2)+'\n')
        print(kind,'complete',complete,'processed',len(records),'of',len(rows),'excluded',len(found),'seconds',time.monotonic()-start,flush=True)

if __name__=='__main__':main()
