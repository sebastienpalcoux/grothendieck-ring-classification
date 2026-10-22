#!/usr/bin/env python3
"""Exact tensor support and joint commutant for the forced center packet."""
from pathlib import Path
import hashlib,json,sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parent))
import verify_semionic_packet as p
s=p.s

def main():
    path=Path(__file__).with_name('semionic_packet.json')
    old=json.loads(path.read_text());out=[];x=s.Symbol('x')
    nine=(x-7414)*(x-3159)*(x-446)*(x*x-359748*x+226527876)*(x*x-388*x+37652)*(x*x-260*x+18196)
    p.need(s.gcd(nine,s.diff(nine,x))==1 and nine.subs(x,-486)!=0,'nine distinct separated joint eigenvalues')
    for row in old['results']:
        n=row['center_rank'];I=s.eye(n);Ns=[s.Matrix(N)for N in row['packet_fusion_matrices']]
        b=p.build_at(row['pattern'],row['pair_histogram']);N2=s.Matrix(b['N2']);K3=s.Matrix(b['K3']);K4=s.Matrix(b['K4'])
        ops=Ns+[N2,K3,K4]
        p.need(all(A*A.T==A.T*A for A in ops),'every operator is normal')
        p.need(all(A*B==B*A for A in ops for B in ops),'all forced operators commute')
        residual=n-s.Matrix.vstack(*Ns,N2,K3-I,K4+I).rank()
        p.need(residual==n-9,'common scalar residual space has dimension n-9')
        L=sum((3**i*A for i,A in enumerate(ops)),s.zeros(n))
        p.need(s.expand(L.charpoly(x).as_expr()-(x+486)**(n-9)*nine)==0,'exact separated characteristic polynomial')
        closure=[]
        target=x**(n-8)*(x-1)**2*(x+1)*(x+5)*(x*x-270*x+225)*(x*x+2*x+5)
        for N in Ns:
            p.need(s.expand(N.charpoly(x).as_expr()-target)==0,'packet fusion characteristic polynomial')
            reach=I+N+N.T+(N+N.T)**2
            p.need(all(reach[0,j]>0 for j in range(n)),'every center simple reached within two tensor factors of Z and its dual')
            closure.append(n)
        out.append({'pattern':row['pattern'],'pair_histogram':row['pair_histogram'],'center_rank':n,'packet_generators_two_step_support_sizes':closure,'common_residual_dimension':residual,'joint_simple_eigenspaces':9,'joint_commutant_complex_dimension':9+(n-9)**2,'status':'PASS'})
    p.need(len(out)==25,'all 25 accepted domains replayed')
    result={'schema':'r1154-packet-closure/v1','status':'PASS','scope':'Necessary packet fusion matrices generate all center labels in two tensor steps. Their forced operators retain a common unresolved scalar space; no subcategory, grading contradiction, categorification or exclusion follows.','separating_operator':'NZ0+3NZ1+9NZ2+27NZ3+81N2+243K3+729K4','separating_characteristic_polynomial':'(x+486)^(n-9)*'+str(nine),'results':out,'packet_receipt_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name('packet_closure.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','branches':len(out),'ranks':sorted({r['center_rank']for r in out}),'commutant_dimensions':sorted({r['joint_commutant_complex_dimension']for r in out})}))
if __name__=='__main__':main()
