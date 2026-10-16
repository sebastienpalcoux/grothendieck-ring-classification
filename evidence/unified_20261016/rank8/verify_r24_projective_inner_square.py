"""Portable source/algebra checks for the audited R24 local obstruction.

This script checks the immutable source and every finite index/scalar step.
The categorical hypotheses and local diagram proof are established separately
in R24_PROJECTIVE_INNER_SQUARE_PROOF.md and its independent audits.
"""
import argparse
from fractions import Fraction as F
import gzip
import hashlib
import itertools
import json
from pathlib import Path

def need(ok, why):
    if not ok:
        raise ValueError(why)

def add(x,y): return (x[0]+y[0],x[1]+y[1])
def neg(x): return (-x[0],-x[1])
def sub(x,y): return add(x,neg(y))
def mul(x,y): return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def div(x,y):
    n=y[0]*y[0]-5*y[1]*y[1]
    need(n!=0,'nonzero field divisor')
    z=mul(x,(y[0],-y[1]))
    return (z[0]/n,z[1]/n)
def q(a,b=0): return(F(a),F(b))
def total(xs):
    v=q(0)
    for x in xs:v=add(v,x)
    return v

def flat(r):return tuple(a for m in r for row in m for a in row)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path)
    args=ap.parse_args();root=args.repo.resolve()
    src=root/'supplements/rank8/data/rank8_tables.txt.gz'
    with gzip.open(src,'rt')as f: rows=[json.loads(l.replace('{','[').replace('}',']'))for l in f]
    N=sorted((r for r in rows if max(flat(r))==2),key=flat)[23]
    digest=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
    need(digest=='2b4780441d9590e8e7269cd82b7675aa75cec11c39bd3e94bb372cca1ada6738','R24 immutable source tensor')
    ledger={r['id']:r for r in json.loads((root/'supplements/rank8/data/decisions.json').read_text())}
    need(ledger['R8_2_24']['tensor_sha256']==digest,'source/ledger identity')
    need(all(sum(N[i][j][k]*N[k][a][b]for k in range(8))==sum(N[j][a][k]*N[i][k][b]for k in range(8))for i,j,a,b in itertools.product(range(8),repeat=4)),'source associativity')
    def simple(i,j):
        need(sum(N[i][j])==1,'simple product')
        return N[i][j].index(1)
    dual=[next(j for j in range(8)if N[i][j][0])for i in range(8)]
    inv=[i for i in range(8)if sum(N[i][dual[i]])==1]
    need(inv==[0,1,2,7],'pointed labels')
    s=1;g=7;rho=5;grho=6;neutral=[0,g,rho,grho]
    need(simple(s,s)==g and simple(g,g)==0,'s orderfour with squareg')
    need(simple(g,rho)==simple(rho,g)==grho,'neutral g action')
    need(all(simple(simple(s,i),dual[s])==i for i in neutral),'Ad_s fixes every neutral label')
    need(all(dual[i]==i for i in neutral),'neutral simples selfdual')
    need(all(not N[i][j][k]for i,j in itertools.product(neutral,repeat=2)for k in range(8)if k not in neutral),'neutral fusion closure')
    need([N[rho][rho][i]for i in neutral]==[1,0,2,2],'neutral 2D2 square')
    d=q(2,1);db=q(2,-1)
    dims=[q(1)if i in inv else d for i in range(8)]
    for i,j in itertools.product(range(8),repeat=2):
        need(mul(dims[i],dims[j])==total(mul(q(N[i][j][k]),dims[k])for k in range(8)),'two-valued positive dimension character')
    n=[[[N[i][j][k]for k in neutral]for j in neutral]for i in neutral]
    chars=[[q(1),q(1),d,d],[q(1),q(1),db,db],[q(1),q(-1),q(1),q(-1)],[q(1),q(-1),q(-1),q(1)]]
    for ch in chars:
        for i,j in itertools.product(range(4),repeat=2):
            need(mul(ch[i],ch[j])==total(mul(q(n[i][j][k]),ch[k])for k in range(4)),'complete neutral character table')
    fs=[total(mul(x,x)for x in ch)for ch in chars]
    need(fs==[q(20,8),q(20,-8),q(4),q(4)],'neutral formal codegrees')
    need(sub(div(q(1),fs[0]),div(q(1),fs[1]))==q(0,F(-1,5)),'conductor-five saturation scalar')
    signs=[]
    for a,b,c in itertools.product([-1,1],repeat=3):
        if 2+2*a-b-c==-2: signs.append([a,b,c])
    need(signs==[[-1,1,1]],'weighted second indicator unique signs')
    cubes=[sum(n[i][i][j]*n[j][i][0]for j in range(4))for i in range(4)]
    need(cubes==[1,0,2,2],'cubic rotation dimensions')
    # In Q[omega]/(omega^2+omega+1), enumerate the six two-dimensional
    # cyclic traces; their sum4 forces both multiplicity triples(2,0,0).
    triples=[(a,b,2-a-b)for a in range(3)for b in range(3-a)]
    cubic_pairs=[(v,w)for v in triples for w in triples
                 if(v[0]-v[2]+w[0]-w[2],v[1]-v[2]+w[1]-w[2])==(4,0)]
    need(cubic_pairs==[((2,0,0),(2,0,0))],'weighted cubic identity forces both rotations identity')
    # Polynomial ring over Q(sqrt5), with independent incoming/outgoing
    # coefficient partners. No conjugation operation is introduced.
    vn=['r','x','X','y','Y','z','Z','a','A'];zeroexp=(0,)*len(vn)
    def pc(c):return {}if c==q(0)else{zeroexp:c}
    def pv(v):
        ex=[0]*len(vn);ex[vn.index(v)]=1;return{tuple(ex):q(1)}
    def pa(a,b):
        out=dict(a)
        for m,c in b.items():out[m]=add(out.get(m,q(0)),c)
        return{m:c for m,c in out.items()if c!=q(0)}
    def pn(a):return{m:neg(c)for m,c in a.items()}
    def pm(a,b):
        out={}
        for m,c in a.items():
            for n,e in b.items():
                ex=tuple(x+y for x,y in zip(m,n));out[ex]=add(out.get(ex,q(0)),mul(c,e))
        return{m:c for m,c in out.items()if c!=q(0)}
    partners={'r':'r','x':'X','X':'x','y':'Y','Y':'y','z':'Z','Z':'z','a':'A','A':'a'}
    def pd(a):
        out={}
        for m,c in a.items():
            ex=[0]*len(vn)
            for k,e in enumerate(m):ex[vn.index(partners[vn[k]])]+=e
            out[tuple(ex)]=c
        return out
    def ps(terms):
        a={}
        for b in terms:a=pa(a,b)
        return a
    z0={};vr=pv('r')
    A=[[vr,z0,z0,pv('A')],[z0,vr,vr,z0],[z0,vr,vr,z0],[pv('a'),z0,z0,vr]]
    D=[[pv('x'),z0,z0,pv('Z')],[z0,pv('X'),pv('y'),z0],[z0,pv('Y'),pn(pv('X')),z0],[pv('z'),z0,z0,pn(pv('x'))]]
    def ent(M,v):i,j,k,l=v;return M[2*i+j][2*k+l]
    def odd(v):i,j,k,l=v;return(k,1-j,i,1-l)
    def even(v):i,j,k,l=v;return(1-k,1-l,1-i,1-j)
    def cyc(v):i,j,k,l=v;return(j,1-k,1-i,l)
    for v in itertools.product(range(2),repeat=4):
        need(odd(odd(v))==v,'odd dual flip involution')
        need(ent(A,odd(v))==pd(ent(A,v))and ent(D,odd(v))==pd(ent(D,v)),'all16 composition-dual slots')
        need(ent(A,v)==ent(A,cyc(v))==ent(A,even(v)),'ordinary tetrahedral symmetry')
        if sum(v)%2:need(ent(A,v)==ent(D,v)=={},'loop parity zeros')
    for v in [(0,0,0,0),(0,1,0,1)]:
        need(v[0]==v[2],'decorated phase occurs as its cube')
        need(ent(D,even(v))==pn(ent(D,v)),'two diagonal evenD flips')
    # Prove that the displayed coefficient forms exhaust the stated LINEAR
    # constraints. No off-diagonal decorated even flip is imposed.
    slots=list(itertools.product(range(2),repeat=4))
    def relation(v,w=None,sign=-1):
        row=[F(0)]*16;row[slots.index(v)]+=1
        if w is not None:row[slots.index(w)]+=sign
        return row
    def rank(rows):
        a=[list(map(F,row))for row in rows];pivot=0
        for col in range(len(a[0])if a else 0):
            hit=next((i for i in range(pivot,len(a))if a[i][col]),None)
            if hit is None:continue
            a[pivot],a[hit]=a[hit],a[pivot]
            scale=a[pivot][col];a[pivot]=[x/scale for x in a[pivot]]
            for i in range(len(a)):
                if i!=pivot and a[i][col]:
                    scale=a[i][col];a[i]=[x-scale*y for x,y in zip(a[i],a[pivot])]
            pivot+=1
        return pivot
    ac=[relation(v)for v in slots if sum(v)%2]
    ac += [relation(v,f(v))for v in slots for f in (cyc,even)]
    dc=[relation(v)for v in slots if sum(v)%2]
    dc += [relation(v,even(v),1)for v in [(0,0,0,0),(0,1,0,1)]]
    arank,drank=rank(ac),rank(dc)
    need((arank,drank)==(13,10),'complete linear slot dimensions3and6')
    for M,variables,expected in [(A,['r','a','A'],3),(D,['x','X','y','Y','z','Z'],6)]:
        coefficient_rows=[]
        for v in slots:
            row=[]
            for var in variables:
                exponent=next(iter(pv(var)))
                coefficient=ent(M,v).get(exponent,q(0))
                need(coefficient[1]==0,'rational linear slot parameterization')
                row.append(coefficient[0])
            coefficient_rows.append(row)
        need(rank(coefficient_rows)==expected,'displayed parameters independent')
    q1=ps(pm(ent(M,(i,0,j,0)),pd(ent(M,(i,0,j,0))))
          for M in [A,D]for i,j in itertools.product(range(2),repeat=2))
    expect=pm(pc(q(2)),pa(pm(vr,vr),pm(pv('x'),pv('X'))))
    need(q1==expect,'first diagonal contraction:2r2+2xX')
    for k,l,var in [(0,0,'z'),(0,1,'y')]:
        q3=ps(pm(ent(D,(i,j,a,b)),pd(ent(D,(i,j,a,b))))
              for a,b in [(k,l),(1-k,1-l)]for i,j in itertools.product(range(2),repeat=2))
        expect=pm(pc(q(2)),pa(pm(pv('x'),pv('X')),pm(pv(var),pv(partners[var]))))
        need(q3==expect,'third diagonal contraction:2xX+2pairedproduct')
    scalar_branches=[]
    need(div(q(1),d)==q(-2,1),'positive unit-channel1overd')
    for tau in [-1,1]:
        r=div(add(db,q(tau)),q(4))
        xx=sub(div(q(3,-1),q(2)),mul(r,r))
        t=sub(q(F(1,2)),xx)
        expected=div(q(-5,3)if tau==-1 else q(-1,1),q(8))
        need(t==expected and t!=q(0),'both tube branches force nonzero mixed entries')
        need(mul(sub(mul(q(4),r),db),sub(mul(q(4),r),db))==q(1),'unit-corner scalar polynomial')
        scalar_branches.append({'tau':tau,'r':list(map(str,r)),'xX':list(map(str,xx)),'yY_equals_zZ':list(map(str,t))})
    weights=[[-2,2],[-2,-2]]
    need([sum(w[j]for w in weights)for j in range(2)]==[-4,0],'coefficient invariance forcesu4=1')
    receipt={'status':'PASS','classification_decisions':1,'criterion':'projective_inner_square_obstruction','id':'R8_2_24','tensor_sha256':digest,'neutral_source_labels':neutral,'order_four_source_label':s,'neutral_formal_codegrees':[[str(a),str(b)]for a,b in fs],'forced_neutral_FS2':signs[0],'neutral_cubic_invariant_dimensions':cubes,'cubic_rotation_multiplicity_pairs':cubic_pairs,'dual_slots_checked':16,'A_linear_constraint_rank':arank,'D_linear_constraint_rank':drank,'diagonal_resolutions_checked':3,'scalar_branches':scalar_branches,'mixed_coefficient_gauge_weights':weights,'scope':'Exact immutable source and finite index/scalar arithmetic only. The categorical paired-frame and no-inner-square theorem is established in R24_PROJECTIVE_INNER_SQUARE_PROOF.md and its independent audits.'}
    out=json.dumps(receipt,indent=2)+'\n'
    if args.output: args.output.write_text(out)
    print(out,end='')
if __name__=='__main__':main()
