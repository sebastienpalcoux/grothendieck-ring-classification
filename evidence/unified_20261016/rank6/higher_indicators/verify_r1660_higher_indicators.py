#!/usr/bin/env python3
"""Exact source-bound rank-six necessary third-indicator refinement.

Standard library only. The frozen, independently certified finite-group
character tables are inputs; all torus, compression and new matrix-coefficient
traces used here are regenerated. No categorical existence is claimed.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import argparse, hashlib, itertools, json, math
from functools import lru_cache

def need(ok, message):
    if not ok:
        raise ValueError(message)

class C:
    """Q[z]/(z^16-z^8+1), ascending coefficients, z = zeta_48."""
    __slots__ = ('a',)
    def __init__(self, value=0):
        if isinstance(value, C): self.a=value.a; return
        a=list(value) if isinstance(value,(list,tuple)) else [value]
        a=[Q(v) for v in a]+[Q(0)]*max(0,16-len(a))
        for k in range(len(a)-1,15,-1):
            a[k-8]+=a[k]; a[k-16]-=a[k]
        self.a=tuple(a[:16])
    def __add__(self, other):
        other=C(other); return C([x+y for x,y in zip(self.a,other.a)])
    __radd__=__add__
    def __neg__(self): return C([-x for x in self.a])
    def __sub__(self, other): return self+-C(other)
    def __rsub__(self, other): return C(other)+-self
    def __mul__(self, other):
        other=C(other); a=[Q(0)]*31
        for i,x in enumerate(self.a):
            if x:
                for j,y in enumerate(other.a):
                    if y: a[i+j]+=x*y
        return C(a)
    __rmul__=__mul__
    def __truediv__(self, other): return C([x/Q(other) for x in self.a])
    def __pow__(self, n):
        need(n>=0,'negative cyclotomic power'); out=C(1); base=self
        while n:
            if n%2: out=out*base
            base=base*base; n//=2
        return out
    def __eq__(self, other): return self.a==C(other).a
    def integer(self):
        need(not any(self.a[1:]) and self.a[0].denominator==1,'not an integer')
        return int(self.a[0])
    def encode(self):
        a=list(self.a)
        while a and not a[-1]: a.pop()
        return [str(x) for x in a]

def default_repo():
    for parent in [Path.cwd(),*Path(__file__).resolve().parents]:
        for candidate in [parent,parent/'repo']:
            if (candidate/'supplements/rank6/data/unresolved_tensors.json').is_file():
                return candidate
    raise ValueError('Repository root not found; pass --repo')

def mul(g,h,m):
    a,b,c,d=g; e,f,u,v=h
    return ((a*e+b*u)%m,(a*f+b*v)%m,(c*e+d*u)%m,(c*f+d*v)%m)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo',type=Path)
    ap.add_argument('--output',type=Path); args=ap.parse_args()
    root=(args.repo or default_repo()).resolve()
    prefix='supplements/rank6/'
    hashes={
      prefix+'data/unresolved_tensors.json':'cf1f3ac0d2b05062861f036932bdb140a5a5f0055dd054689b6e1fa67924d203',
      prefix+'research/round5/m8_modrep/sl2_16.json':'dd179136c6e534db88036a626ac50cd48a40e65b6a8c142c2d42ae25232cb978',
      prefix+'research/round5/m8_modrep/sl2_3.json':'d43af23f8ad2215828111c6933605262fe286ff5a39e1ddaf902bfde2628c6e5'}
    data={}
    for path,digest in hashes.items():
        raw=(root/path).read_bytes(); need(hashlib.sha256(raw).hexdigest()==digest,'source hash: '+path)
        data[path]=json.loads(raw)
    source=next(r for r in data[prefix+'data/unresolved_tensors.json'] if r['id']=='R6_8_1660')
    N=source['N']; need(source['dual']==list(range(6)),'source duality')
    tensor_sha=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
    need(tensor_sha=='697ec27fe203356199bfcf674587be9c71455dbb681f2e086a076f726b03d267','source tensor hash')
    z=C([0,1]); q2=z**6+z**42; q3=z**4+z**44; q6=q2*q3; omega=z**16
    need(q2*q2==2 and q3*q3==3 and q6*q6==6 and omega**2+omega+1==0,'field normalization')
    d=3+2*q2+2*q3+q6; dims=[C(1),C(1),d,d,q2,q2*d]
    D=sum(x*x for x in dims); Di=(6-2*q3-q6)/48
    need(D*Di==1,'global dimension inverse')
    for i,j in itertools.product(range(6),repeat=2):
        need(dims[i]*dims[j]==sum(N[i][j][k]*dims[k] for k in range(6)),'FP dimension character')
    weights3=[-1,-1,1,1,-1,-1]; weights6=[-1,-1,-1,-1,-2,2]
    # Check the exact rational coordinates by Galois Fourier projection.
    def autom(x,k): return sum(a*z**((i*k)%48) for i,a in enumerate(x.a))
    units=[k for k in range(48) if math.gcd(k,48)==1]
    @lru_cache(None)
    def signs(k):
        return [1,1 if autom(q2,k)==q2 else -1,
                1 if autom(q3,k)==q3 else -1,
                1 if autom(q6,k)==q6 else -1]
    for i,v in enumerate(dims):
        e3=sum(signs(k)[2]*autom(v*Di,k) for k in units)/16
        e6=sum(signs(k)[3]*autom(v*Di,k) for k in units)/16
        need(e3==Q(weights3[i],24)*q3 and e6==Q(weights6[i],48)*q6,'indicator weights')
    def power(i,n):
        out=[1,0,0,0,0,0]
        for _ in range(n): out=[sum(out[j]*N[j][i][k] for j in range(6)) for k in range(6)]
        return out
    hom3=[power(i,3)[0] for i in range(6)]
    need(hom3==[1,0,3,3,0,8],'third invariant dimensions')
    hom57={str(n):[power(i,n)[0] for i in [2,5]] for n in [5,7]}
    need(hom57=={'5':[402,2272],'7':[55401,626784]},'higher invariant dimensions')
    local=[]
    for m in [16,3]:
        table=data[prefix+f'research/round5/m8_modrep/sl2_{m}.json']; group=table['group']
        index={tuple(g):i for i,cl in enumerate(group['classes']) for g in cl}
        need(len(index)==group['order'],'class partition')
        S=(0,m-1,1,0); ts=[(1,j,0,1) for j in range(m)]
        c1=Counter(index[mul(t,S,m)] for t in ts)
        c2=Counter(index[mul(mul(mul(t,S,m),u,m),S,m)] for t in ts for u in ts)
        records=[]
        for ix,rec in enumerate(table['irreps']):
            ch=[C(list(reversed(coeff))) for coeff in rec['characters']]
            def avg(counts,den): return sum(ch[k]*v for k,v in counts.items())/den
            n=rec['T_multiplicities'][0]
            torus={a:avg(Counter(index[(a,a*j%m,0,pow(a,-1,m))] for j in range(m)),m)
                   for a in sorted({k%m for k in units})}
            need(torus[1]==n,'fixed-space rank')
            trace=avg(c1,m); trace2=avg(c2,m*m)
            if n==1: need(trace2==trace*trace,'rank-one compression')
            moments={n0:avg(Counter(index[((1-j*n0)%m,j,(-n0)%m,1)] for j in range(m)),m)
                     for n0 in [1,3,5,7]}
            records.append({'index':ix,'rank':n,'sign':rec['central_sign'],'torus':torus,
                            'trace':trace,'det':(trace*trace-trace2)/2,'moments':moments})
        local.append(records)
    # Exhaust every tensor-product irrep. A compression polynomial must divide
    # one of the two exact low-block polynomials. No choice of low columns enters.
    low_roots=[[C(1),C(1),C(Q(-1,2)),C(0),-q3/6,-q6/12],
               [C(1),C(Q(-1,2)),C(0),C(0),-q3/6,-q6/12]]
    eligible={2:[],3:[]}; total_pairs=0
    for left,right in itertools.product(*local):
        total_pairs+=1; n=left['rank']*right['rank']
        if not n or left['sign']*right['sign']!=1: continue
        weights=[(sum(signs(k)[a]*left['torus'][k%16]*right['torus'][k%3] for k in units)/16).integer() for a in range(4)]
        if sum(weights)!=n or any(w<0 or w>v for w,v in zip(weights,[3,1,1,1])): continue
        need(right['rank']==1 and left['rank'] in [1,2],'unexpected fixed rank')
        trace=left['trace']*right['trace']
        if n==1:
            passes=any(trace in roots for roots in low_roots)
        else:
            det=left['det']*right['trace']**2
            passes=any(trace==a+b and det==a*b for roots in low_roots for a,b in itertools.combinations(roots,2))
        if not passes: continue
        for sector,target in [(2,-q3/6),(3,-q6/12)]:
            if weights[sector]:
                if n==1 and trace!=target: continue
                need(n==1 and weights[sector]==1,'nonunique saturated fixed space')
                eligible[sector].append((left['index'],right['index']))
    need(total_pairs==532,'irreducible table size')
    need(eligible[2]==[(33,4),(36,5)] and eligible[3]==[(54,4),(61,5)],'eligible saturated irreps')
    allowed_traces={tuple((a+b*omega+c*omega**2).a):(a,b,c)
                    for a in range(4) for b in range(4-a) for c in [3-a-b]}
    cases=[]; surviving=[]
    for p3,p6 in itertools.product(eligible[2],eligible[3]):
        moments={}
        for n in [1,3,5,7]:
            def coefficient(pair): return local[0][pair[0]]['moments'][n]*local[1][pair[1]]['moments'][n]
            a=2*q3*coefficient(p3); b=2*q6*coefficient(p6)
            x=(3+2*a+b)/2; t=2+a+b
            moments[str(n)]={'X':x.encode(),'T':t.encode()}
            if n==1: need(x==0 and t==0,'first indicator normalization')
            if n==3: x3=x; t3=t
            if n==5: need(x==2 and t==2,'fifth indicators')
            if n==7: need(x==3 and t==4,'seventh indicators')
        compatible=tuple(x3.a) in allowed_traces
        if compatible:
            need(t3==2 and x3 in [2+omega,2+omega**2],'surviving third indicators')
            surviving.append([list(p3),list(p6)])
        else: need(x3 in [-3*omega,-3*omega**2],'excluded mixed choice')
        cases.append({'chi3_pair':p3,'chi6_pair':p6,'cyclic_dimension_three_compatible':compatible,
                      'third_rotation_multiplicities':allowed_traces.get(tuple(x3.a)),
                      'moments_ascending_zeta48_coefficients':moments})
    need(surviving==[[[33,4],[54,4]],[[36,5],[61,5]]],'surviving pair count')
    receipt={'status':'PASS','mathematical_verdict':'REFINED_NECESSARY_CONDITION',
             'ring':'R6_8_1660','source_files_sha256':hashes,'source_tensor_sha256':tensor_sha,
             'coefficient_field':'Q[z]/(z^16-z^8+1); ascending coefficient arrays',
             'irreducible_pairs_exhausted':total_pairs,'eligible_chi3_pairs':eligible[2],
             'eligible_chi6_pairs':eligible[3],'third_invariant_dimensions':hom3,
             'higher_invariant_dimensions_X_T':hom57,'cases':cases,'surviving_pairs':surviving,
             'forced_third_indicator_T':2,'categorification_claimed':False,
             'scope':'Two mixed saturated-irrep choices are excluded. Two conjugate necessary profiles remain; the earlier rank-37 witness uses the second. No category is constructed or excluded.'}
    text=json.dumps(receipt,indent=2)+'\n'
    if args.output: args.output.write_text(text)
    print(text,end='')
if __name__=='__main__': main()
