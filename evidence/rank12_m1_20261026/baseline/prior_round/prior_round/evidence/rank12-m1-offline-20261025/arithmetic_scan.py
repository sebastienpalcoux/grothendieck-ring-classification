"""Short exact rank-independent tests; necessary-condition passes are not models."""
from pathlib import Path
import collections,json,sys,time
import sympy as s
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/work/rank11/arithmetic/legacy'))
import arithmetic as old
import exact,gng,noncomm_integral

def main():
    start=time.monotonic();rows=json.loads((ROOT/'tensors.json').read_text())
    out=[]
    for rid,R in rows.items():
        cs=[]
        for fn in [old.near_group,old.dnumber,gng.certificate]:
            c=fn(R)
            if c:cs.append(c)
        # To keep this first pass short, expensive overlapping tests are
        # unnecessary after an exact general-complex obstruction is obtained.
        if not cs:
            for fn in [old.integral_drinfeld,noncomm_integral.test,old.cyclotomic]:
                c=fn(R)
                if c:
                    c.setdefault('scope','general_complex_fusion_category');cs.append(c)
                    break
        if not cs and old.comm(R):
            p=old.casimir(R).charpoly(old.t).as_poly()
            for q,e in p.factor_list()[1]:
                degree=q.degree();norm=abs(int(q.TC()))
                if all(v<degree for v in s.factorint(norm).values()) and (degree!=len(R)or e!=1 or p!=q):
                    cs.append(dict(kind='primitive_codegree',factor=list(map(int,q.all_coeffs())),degree=degree,norm=norm,scope='general_complex_fusion_category',reference='Schopieray 2005.13760, Corollary 4.3 and Theorem 4.4'))
                    break
        out.append(dict(id=rid,tensor_sha256=old.sha(R),certificates=cs))
        if len(out)%25==0:
            (ROOT/'arithmetic.json').write_text(json.dumps(out,indent=2)+'\n')
            print(len(out),'excluded',sum(bool(x['certificates'])for x in out),round(time.monotonic()-start,2),flush=True)
    (ROOT/'arithmetic.json').write_text(json.dumps(out,indent=2)+'\n')
    print('DONE',len(out),'excluded',sum(bool(x['certificates'])for x in out),dict(collections.Counter(c['kind']for r in out for c in r['certificates'])),'seconds',time.monotonic()-start)

if __name__=='__main__':main()
