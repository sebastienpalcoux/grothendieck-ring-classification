#!/usr/bin/env python3
"""Exact source-bound rejection of one historical rank-six modular witness.

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

INPUT_HASHES={'evidence/theoretical_20261016/rank6/r1660_modular_witness/witness.json': '947b560f526e3925156c78cd4fd6fbca645e50819b3163e74d6922025916b582', 'evidence/theoretical_20261016/rank6/r1660_modular_witness/system.json': '351faa175591faa11f153249ee85a01a35b31d6f5f7994f8db4f4fd45d3f7b3e', 'evidence/theoretical_20261016/rank6/r1660_modular_witness/inputs/low0_profiles.json': 'c74ce8eded70ee44ca896bfa6d5cbe42fb95804fea5f967018b6f7dbf42097cb', 'supplements/rank6/data/unresolved_tensors.json': 'cf1f3ac0d2b05062861f036932bdb140a5a5f0055dd054689b6e1fa67924d203', 'supplements/rank6/research/round5/m8_modrep/sl2_16.json': 'dd179136c6e534db88036a626ac50cd48a40e65b6a8c142c2d42ae25232cb978', 'supplements/rank6/research/round5/m8_modrep/sl2_3.json': 'd43af23f8ad2215828111c6933605262fe286ff5a39e1ddaf902bfde2628c6e5'}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo',type=Path)
    ap.add_argument('--output',type=Path); args=ap.parse_args()
    root=(args.repo or default_repo()).resolve()
    hashes=INPUT_HASHES
    data={}
    for path,digest in hashes.items():
        raw=(root/path).read_bytes(); need(hashlib.sha256(raw).hexdigest()==digest,'source hash: '+path)
        data[path]=json.loads(raw)
    prefix='supplements/rank6/'; old='evidence/theoretical_20261016/rank6/r1660_modular_witness/'
    witness=data[old+'witness.json']; system=data[old+'system.json']
    x=witness['solution']; reps=system['representations']; oldnv=system['meta']['variables']
    need(witness['system_sha256']==hashes[old+'system.json'],'historical system identity')
    need(len(x)==len(system['bounds'])==oldnv+len(reps)+48,'variable coverage')
    for val,(lo,hi)in zip(x,system['bounds']):
        need(type(val)is int and val>=lo and(hi is None or val<=hi),'historical integer bound')
    for row,rhs in zip(system['rows'],system['rhs']):
        need(sum(co*x[j]for j,co in row)==rhs,'historical necessary equation')
    need(len(system['rows'])==len(system['rhs'])==1536,'historical equation coverage')
    active=[(tuple(r['factors']),x[oldnv+j])for j,r in enumerate(reps)if x[oldnv+j]]
    need([[list(pair),mult]for pair,mult in active]==witness['active_irreps'],'active decomposition identity')
    low=data[old+'inputs/low0_profiles.json']['branches'][0]['columns']
    records=[(v,0,1)for v in low]+[([0]+v,t,x[j])for j,(v,t)in enumerate(system['meta']['high_labels'])if x[j]]
    need(sum(mult for v,t,mult in records)==37,'historical center rank')
    need(low[2]==[1,0,1,1,0,2],'low A restriction')
    Brow=[0,0,1,1,0,2]
    need([(v,mult)for v,t,mult in records if t==4]==[(Brow,2)],'complete phase-four doublet')
    localtables={m:data[prefix+f'research/round5/m8_modrep/sl2_{m}.json']for m in[16,3]}
    spect={}
    for pair,mult in active:
        a=localtables[16]['irreps'][pair[0]]; b=localtables[3]['irreps'][pair[1]]
        spec=[0]*48
        for i,p0 in enumerate(a['T_multiplicities']):
            for j,q0 in enumerate(b['T_multiplicities']):spec[(3*i+16*j)%48]+=p0*q0
        spect[pair]=spec
    need({pair:mult*spect[pair][4]for pair,mult in active if spect[pair][4]}=={(0,1):1,(61,5):1},'phase-four representation support')
    need(localtables[16]['irreps'][0]['degree']*localtables[3]['irreps'][1]['degree']==1,'hidden line degree')
    need(spect[61,5][0]==1 and all(v in[0,1]for v in spect[61,5]),'visible simple T spectrum')
    z=C([0,1]); q2=z**6+z**42; q3=z**4+z**44; q6=q2*q3
    def autom(a,k):return sum(co*z**((i*k)%48)for i,co in enumerate(a.a))
    def invK(a):
        rest=autom(a,5)*autom(a,7)*autom(a,11); norm=a*rest
        need(not any(norm.a[1:]) and bool(norm.a[0]),'nonrational or zero K norm')
        ans=rest/norm.a[0];need(a*ans==1,'K inverse');return ans
    d=3+2*q2+2*q3+q6; dims=[C(1),C(1),d,d,q2,q2*d]
    D=sum(v*v for v in dims);Di=(6-2*q3-q6)/48;need(D*Di==1,'dimension inverse')
    source=next(r for r in data[prefix+'data/unresolved_tensors.json']if r['id']=='R6_8_1660')
    N=source['N'];tensor_sha=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
    need(tensor_sha=='697ec27fe203356199bfcf674587be9c71455dbb681f2e086a076f726b03d267','source tensor')
    for i,j in itertools.product(range(6),repeat=2):
        need(dims[i]*dims[j]==sum(N[i][j][k]*dims[k]for k in range(6)),'dimension character')
    beta=sum(v*t for v,t in zip(dims,low[2]));ks=[k for k in[1,5,7,11]if D*autom(Di,k)==beta]
    need(len(ks)==1,'A character identification');ka=ks[0]
    L6=[-1,-1,-1,-1,-2,2]
    # e_W=w6/2; therefore |(S e_W)_E|^2=L6(v_E)^2/96.
    for i,dim in enumerate(dims):
        coordinate=sum((1 if autom(q6,k)==q6 else -1)*autom(dim*Di,k)for k in[1,5,7,11])/4
        need(coordinate==q6*Q(L6[i],48),'source coordinate weight')
    moments={};rB=None
    for v,t,mult in records:
        zz=sum(a*b for a,b in zip(dims,v));rr=beta*autom(zz,ka)*invK(zz)
        need(autom(rr,47)==rr,'nonreal spectral weight')
        weight=Q(sum(a*b for a,b in zip(L6,v))**2,96)
        mass,weighted=moments.get(t,(Q(0),C(0)))
        moments[t]=(mass+mult*weight,weighted+mult*weight*rr)
        if t==4:rB=rr
    need(rB==-1 and moments[4][0]>0,'B spectral weight and visible support')
    need(sum(mass for mass,weighted in moments.values())==1,'visible fixed-line norm')
    probabilities={}
    for m,ir,target in[(16,61,12),(3,5,1)]:
        table=localtables[m];rec=table['irreps'][ir]
        index={tuple(g):i for i,cl in enumerate(table['group']['classes'])for g in cl}
        chars=[C(list(reversed(a)))for a in rec['characters']]
        Sm=(0,m-1,1,0);Si=(0,1,m-1,0)
        values=[[chars[index[mul(mul(mul((1,j,0,1),Sm,m),(1,k,0,1),m),Si,m)]]for k in range(m)]for j in range(m)]
        probs={}
        for a,rank in enumerate(rec['T_multiplicities']):
            if not rank:continue
            need(rank==1,'local simple T spectrum')
            probs[a]=sum(values[j][k]*z**((-48//m*(target*j+a*k))%48)for j in range(m)for k in range(m))/(m*m)
        need(sum(probs.values())==1,'local probability norm');probabilities[m]=probs
    expected=C(0);terms=[]
    for a,pa in probabilities[16].items():
        for b,pb in probabilities[3].items():
            t=(3*a+16*b)%48;mass,weighted=moments[t]
            need(mass>0,'missing visible phase');qt=weighted/mass;pt=pa*pb
            expected+=pt*qt
            terms.append({'phase':t,'probability':pt.encode(),'spectral_expectation':qt.encode()})
    need(expected==2,'visible fusion expectation')
    coefficient=(expected+rB)/2;need(coefficient==C(Q(1,2)),'nonintegral coefficient')
    receipt={'status':'PASS','mathematical_verdict':'FIXED_WITNESS_EXCLUDED','ring':'R6_8_1660',
        'historical_necessary_system':'PASS, all 1536 equations and 1447 variable bounds',
        'source_files_sha256':hashes,'source_tensor_sha256':tensor_sha,'historical_rank':37,
        'A_forgetful_row':low[2],'B_forgetful_row':Brow,'B_twist_exponent_mod48':4,'B_multiplicity':2,
        'visible_irrep':[61,5],'hidden_irrep':[0,1],'visible_expectation':expected.encode(),
        'hidden_expectation':rB.encode(),'forced_fusion_coefficient':coefficient.encode(),
        'coefficient_encoding':'ascending rational coefficients in Q[z]/(z^16-z^8+1)',
        'phase_transition_table':terms,'categorification_claimed':False,'source_ring_excluded':False,
        'scope':'Only this historical rank37 restriction/twist/representation witness is excluded. Other profiles remain unresolved.'}
    text=json.dumps(receipt,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')

if __name__=='__main__':main()
