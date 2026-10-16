#!/usr/bin/env python3
"""Source-bound exact arithmetic for the unified Fibonacci character-parity proof."""
import argparse,gzip,hashlib,itertools,json,math
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)
def flat(R):return tuple(c for a in R for b in a for c in b)
B=list(itertools.product(range(2),repeat=3));pos={x:i for i,x in enumerate(B)}
def model(epsilon):
    def product(x,y):
        terms={tuple(a+b for a,b in zip(x,y)):1};out=[0]*8
        while terms:
            (g,t,z),c=terms.popitem()
            if g>=2:news=[(g%2,t,z)]
            elif t>=2:news=[(g,t-1,z),(g,t-2,z)]
            elif z>=2:news=[(g+epsilon,t,z-2),(g,t+1,z-1),(g+1,t+1,z-1)]
            else:out[pos[g,t,z]]+=c;continue
            for q in news:terms[q]=terms.get(q,0)+c
        return out
    return [[product(x,y) for y in B] for x in B]
# Q(phi,d), basis 1,phi,d,phi*d; phi^2=phi+1, d^2=1+2*phi*d.
ZERO=(0,0,0,0);ONE=(1,0,0,0);PHI=(0,1,0,0);D=(0,0,1,0)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(n,a):return tuple(n*x for x in a)
def sub(a,b):return add(a,scale(-1,b))
def mul(a,b):
    out=[0]*4
    for i,j in itertools.product(range(4),repeat=2):
        terms={(i%2+j%2,i//2+j//2):a[i]*b[j]}
        while terms:
            (p,q),c=terms.popitem()
            if not c:continue
            if q>=2:news=[(p,q-2,c),(p+1,q-1,2*c)]
            elif p>=2:news=[(p-1,q,c),(p-2,q,c)]
            else:out[p+2*q]+=c;continue
            for u,v,w in news:terms[u,v]=terms.get((u,v),0)+w
    return tuple(out)
def power(a,n):
    z=ONE
    for _ in range(n):z=mul(z,a)
    return z
# The pair notation adjoins omega^2=(-1)^epsilon. For epsilon=0 one
# specializes omega to 1; for epsilon=1 to i. Both identities are exact.
def ext_add(a,b):return add(a[0],b[0]),add(a[1],b[1])
def ext_scale(n,a):return scale(n,a[0]),scale(n,a[1])
def ext_mul(a,b,s):return add(mul(a[0],b[0]),scale(s,mul(a[1],b[1]))),add(mul(a[0],b[1]),mul(a[1],b[0]))
def ext_power(a,n,s):
    z=(ONE,ZERO)
    for _ in range(n):z=ext_mul(z,a,s)
    return z

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3]);ap.add_argument('--output',type=Path);a=ap.parse_args()
    source=a.repo/'supplements/rank8/data/rank8_tables.txt.gz'
    need(hashlib.sha256(source.read_bytes()).hexdigest()=='35a8d69e9af8c873b3003890218a35b38b792abb89c19066f6705bf9c1c1d1ed','source archive hash')
    rs=[json.loads(line.replace('{','[').replace('}',']')) for line in gzip.open(source,'rt')]
    rs=sorted((r for r in rs if max(flat(r))==2),key=flat)
    # Norm(phi+2)=5 is not a rational square; hence the four coordinates are independent.
    need(mul(add(PHI,scale(2,ONE)),sub(scale(3,ONE),PHI))==scale(5,ONE),'quadratic norm')
    need(math.isqrt(5)**2!=5,'nonsquare norm')
    delta=scale(2,mul(add(PHI,scale(2,ONE)),add(ONE,mul(D,D))))
    z=sub(mul(sub(PHI,ONE),D),PHI)
    tp=sub(ONE,PHI)
    need(mul(z,z)==add(ONE,scale(2,mul(tp,z))),'third character relation')
    f_pair=scale(4,add(PHI,scale(2,ONE)))
    f_psi=scale(2,mul(add(tp,scale(2,ONE)),add(ONE,mul(z,z))))
    beta_pair=add(ONE,mul(PHI,D))
    beta_psi=add(add(ONE,PHI),mul(add(scale(2,ONE),scale(3,PHI)),D))
    need(beta_pair==(1,0,0,1) and beta_psi==(1,1,2,3),'dimension coordinates')
    need(mul(f_pair,beta_pair)==delta,'paired central dimension')
    need(mul(f_psi,beta_psi)==delta,'third central dimension')
    cases=[]
    for idx,eps,perm,sha in [(190,1,[0,1,5,3,7,2,6,4],'ef368ba29ddc183f215145eb6a50ead0655e91afff2d3e844f918c6d2a91d867'),(489,0,[0,3,7,4,1,6,2,5],'23cae0639e4ce7e54428705a66098747319e26d5f29ad8dff05914a6d43caef1')]:
        R=rs[idx-1];M=model(eps);s=(-1)**eps
        tensor_hash=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
        need(tensor_hash==sha,'case tensor hash')
        need(all(M[i][j][k]==R[perm[i]][perm[j]][perm[k]] for i,j,k in itertools.product(range(8),repeat=3)),'512-entry tensor identification')
        dual=[next(j for j in range(8) if M[i][j][0]) for i in range(8)]
        need(dual==[pos[(gi+eps*xi)%2,ti,xi] for gi,ti,xi in B],'full involution')
        chars=[]
        for sign in (1,-1):
            vals=[]
            for gi,ti,xi in B:
                p=(scale((-1)**gi,power(PHI,ti)),ZERO)
                vals.append(ext_mul(p,ext_power((ZERO,scale(sign,ONE)),xi,s),s))
            chars.append(vals)
        chars.append([(mul(power(tp,ti),power(z,xi)),ZERO) for gi,ti,xi in B])
        for h,vals in enumerate(chars):
            for i,j in itertools.product(range(8),repeat=2):
                rhs=(ZERO,ZERO)
                for k in range(8):rhs=ext_add(rhs,ext_scale(M[i][j][k],vals[k]))
                need(ext_mul(vals[i],vals[j],s)==rhs,'character multiplicativity')
            f=(ZERO,ZERO)
            for i in range(8):f=ext_add(f,ext_mul(vals[i],vals[dual[i]],s))
            need(f==((f_pair if h<2 else f_psi),ZERO),'formal codegree with duality')
        # The only two possible paired central restrictions have equal psi value.
        y=pos[0,1,1];gy=pos[1,1,1]
        need(chars[2][y]==chars[2][gy],'psi equality on both paired restrictions')
        # Any dimension-compatible third restriction has pair totals (1,1,2,3).
        # Unit multiplicity one fixes g coefficient zero. All remaining choices
        # are checked exactly, though the proof simply uses 2*v_y=3.
        count=0
        for v_tau,v_x,v_y in itertools.product(range(2),range(3),range(4)):
            v=[0]*8;v[pos[0,0,0]]=1;v[pos[0,1,0]]=v_tau;v[pos[1,1,0]]=1-v_tau
            v[pos[0,0,1]]=v_x;v[pos[1,0,1]]=2-v_x;v[y]=v_y;v[gy]=3-v_y
            diff=(ZERO,ZERO)
            for j in range(8):diff=ext_add(diff,ext_scale(v[j],ext_add(chars[0][j],ext_scale(-1,chars[1][j]))))
            expected=(ZERO,scale(2,add(scale(2*v_x-2,ONE),scale(2*v_y-3,PHI))))
            need(diff==expected and diff!=(ZERO,ZERO),'exact character-parity contradiction')
            count+=1
        cases.append({'id':f'R8_2_{idx}','epsilon':eps,'model_to_census':perm,'tensor_sha256':tensor_hash,'tensor_entries_matched':512,'character_homomorphisms_checked':3,'dimension_compatible_third_restrictions':count,'reciprocity_compatible_third_restrictions':0,'result':'no complex fusion-category categorification'})
    report={'status':'PASS','classification_changes':2,'method':'theoretical character reciprocity and odd multiplicity','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'categorical_source':'Ostrik, arXiv:1309.4822, Example 2.9 and Theorem 2.13 with its preceding character-level definition','general_scope_dependency':'FIB_PAIR_THEORETICAL_GALOIS_PU.md','dimension_basis':['1','phi','d','phi*d'],'paired_central_dimension':list(beta_pair),'third_central_dimension':list(beta_psi),'cases':cases}
    text=json.dumps(report,indent=2)+'\n'
    if a.output:a.output.write_text(text)
    print(text,end='')
if __name__=='__main__':main()
