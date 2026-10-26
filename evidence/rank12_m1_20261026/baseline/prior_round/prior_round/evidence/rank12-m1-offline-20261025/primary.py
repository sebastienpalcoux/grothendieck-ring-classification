"""Short reduced primary-3 tests, with a proved general-to-unitary gate."""
from pathlib import Path
from fractions import Fraction as F
import itertools,json,math,time
import numpy as np
ROOT=Path(__file__).resolve().parent

def upper_bound(cs,sq):
    scale=10**8;value=F(0)
    for c,q in zip(cs,sq):
        a=math.isqrt(q*scale*scale);b=a if a*a==q*scale*scale else a+1
        value+=F(c*(b if c>=0 else a),q*scale)
    return value

def main():
    start=time.monotonic();data=json.loads((ROOT/'tensors.json').read_text())
    rem=set(json.loads((ROOT/'remaining_after_basic.json').read_text()));rows=[]
    for p in json.loads((ROOT/'profile.json').read_text())['records']:
        if p['id']not in rem:continue
        sq=p['squared_dimensions']
        if sq is None:continue
        D=sum(sq);x=D;primes=[]
        for a in range(2,math.isqrt(x)+1):
            if x%a==0:
                primes.append(a)
                while x%a==0:x//=a
        if x>1:primes.append(x)
        if len(primes)>2:continue
        N=np.array(data[p['id']],dtype=np.int64);cert=None
        for size in [2,3]:
            for U in itertools.combinations(range(12),size):
                A=N[:,U,:][:,:,U];B=np.einsum('iab,icd,ief,i->acebdf',A,A,A,1/np.sqrt(sq)).reshape(size**3,size**3)
                w,V=np.linalg.eigh(B)
                if w[0]>=-1e-7:continue
                v=np.rint(V[:,0]*1000).astype(np.int64)
                cs=[int(v@np.kron(np.kron(a,a),a)@v)for a in A]
                upper=upper_bound(cs,sq)
                if upper<0:
                    cert=dict(kind='primary3_with_solvable_unitarity_gate',subset=list(U),vector=v.tolist(),coefficients=cs,squared_dimensions=sq,global_dimension=D,primes=primes,rigorous_quadratic_upper_bound=str(upper),scope='general_complex_fusion_category',gate='ENO 0809.3031 Theorem1.6; Galindo-Hong-Rowell 1105.5048 Theorem5.20')
                    break
            if cert:break
        rows.append(dict(id=p['id'],tensor_sha256=p['tensor_sha256'],certificate=cert))
    (ROOT/'primary.json').write_text(json.dumps(dict(records=rows,elapsed_seconds=time.monotonic()-start,scope='Reduced primary-3; absence of a witness is no conclusion'),indent=2)+'\n')
    print('eligible',len(rows),'excluded',sum(r['certificate']is not None for r in rows),'seconds',time.monotonic()-start)

if __name__=='__main__':main()
