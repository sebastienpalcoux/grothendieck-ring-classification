#!/usr/bin/env python3
"""All proper based subrings: exact FPdim index, without commutativity.

The Perron character is constructed over the field of the Perron eigenvalue
of the strictly positive matrix sum_i N_i.  Every entry is certified positive
using rational root isolation; all multiplication identities are checked.
"""
from pathlib import Path
import argparse, collections, json, sys, time
import sympy as s
from run import ROOT, HERE, rows, require, old, exact
sys.path.insert(0,str(HERE.parent))
import common

def solve_field(B, v, K):
    n=len(v); A=[list(B[i])+[v[i]] for i in range(n)]
    for j in range(n):
        q=next((i for i in range(j,n) if A[i][j]),None)
        require(q is not None,'singular Perron cofactor')
        A[j],A[q]=A[q],A[j]; a=A[j][j]
        A[j]=[x/a for x in A[j]]
        for i in range(n):
            if i==j or not A[i][j]:continue
            a=A[i][j]; A[i]=[x-a*y for x,y in zip(A[i],A[j])]
    return [A[i][-1] for i in range(n)]

def fp_character(R):
    n=len(R); A=sum(map(s.Matrix,R),s.zeros(n)); t=exact.t
    require(all(x>0 for x in A),'positive separating sum')
    factors=A.charpoly(t).as_poly().factor_list()[1]
    real=[(f,m,e) for f,m in factors for e in exact.embeddings(f)]
    f,m,emb=max(real,key=lambda x:x[2].hi)
    require(m==1,'Perron multiplicity')
    K=exact.field(f); u=K(s.Poly(t,t).rem(f).all_coeffs())
    B=[[K(A[i,j])-(u if i==j else K.zero) for j in range(1,n)] for i in range(1,n)]
    v=[-K(A[i,0]) for i in range(1,n)]
    d=[K.one]+solve_field(B,v,K)
    require(all(emb.sign(x)>0 for x in d),'positive Perron dimensions')
    require(all(sum((K(R[i][j][k])*d[k] for k in range(n)),K.zero)==d[i]*d[j]
                for i in range(n) for j in range(n)),'exact dimension homomorphism')
    D=sum((x*x for x in d),K.zero)
    return f,K,u,d,D,emb

def polynomial_of(q,f,K,u):
    d=f.degree()
    M=s.Matrix.hstack(*(exact.vector(q*u**i,d) for i in range(d)))
    return M.charpoly(exact.t).as_poly()

def check_certificate(R,c):
    f,K,u,ds,D,emb=fp_character(R)
    require(c['field_polynomial']==exact.pc(f),'FP defining polynomial')
    J=c['subset']; require(J in common.subrings(R) and 1<len(J)<len(R),'proper subring')
    S=sum((ds[j]**2 for j in J),K.zero)
    p=polynomial_of(D/S,f,K,u)
    require(exact.pc(p)==c['quotient_polynomial'] and any(x.q!=1 for x in p.all_coeffs()),'nonintegral index')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--verify-only',action='store_true');args=ap.parse_args()
    allrows=rows(); out=HERE/'subring_indices.json'
    if args.verify_only:
        ledger=json.loads(out.read_text());require(len(ledger['records'])==len(allrows),'complete inventory')
        for r,w in zip(allrows,ledger['records']):
            require(r['id']==w['id'] and r['tensor_sha256']==w['tensor_sha256'],'identity')
            for c in w['certificates']:check_certificate(r['tensor'],c)
        print('PASS all FP-index certificates');return
    ledger={'records':[]};start=time.monotonic()
    for r in allrows:
        R=r['tensor'];Js=[J for J in common.subrings(R) if 1<len(J)<len(R)]
        rec={k:v for k,v in r.items() if k!='tensor'}|{'proper_subrings_checked':len(Js),'certificates':[]}
        if Js:
            f,K,u,ds,D,emb=fp_character(R)
            rec['field_polynomial']=exact.pc(f)
            rec['FP_dimensions_in_field']=[exact.ec(x) for x in ds]
            rec['positive_root_interval']=[str(emb.lo),str(emb.hi)]
            rec['indices']=[]
            for J in Js:
                S=sum((ds[j]**2 for j in J),K.zero); p=polynomial_of(D/S,f,K,u)
                rec['indices'].append({'subset':J,'polynomial':exact.pc(p),'algebraic_integer':all(x.q==1 for x in p.all_coeffs())})
                if any(x.q!=1 for x in p.all_coeffs()):
                    rec['certificates'].append({'kind':'subring_dimension','subset':J,
                        'field_polynomial':exact.pc(f),'quotient_polynomial':exact.pc(p),
                        'scope':'general_complex_fusion_category','reference':'EGNO Tensor Categories Theorem 7.17.6; LPR Theorem 2.13'})
        ledger['records'].append(rec)
        out.write_text(json.dumps(ledger,indent=2)+'\n')
        if rec['certificates'] or len(ledger['records'])%20==0:
            print(r['id'],len(Js),len(rec['certificates']),round(time.monotonic()-start,2),flush=True)
    ledger['elapsed_seconds']=time.monotonic()-start
    ledger['excluded']=sum(bool(r['certificates']) for r in ledger['records'])
    out.write_text(json.dumps(ledger,indent=2)+'\n')
    print('DONE',ledger['excluded'],'excluded',ledger['elapsed_seconds'],flush=True)
if __name__=='__main__':main()
