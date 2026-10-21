#!/usr/bin/env python3
"""Exact pointed counterexample to a proposed fermion dimension-character gate."""
from pathlib import Path
import argparse, hashlib, itertools, json

HERE=Path(__file__).resolve().parent
F3=[1,3,0,0,3,1,3,0,1,0,3,1,2,1,1,0,0,0,3,2,3,0,0,0,3,0,1]
TRIPLES=list(itertools.product(range(1,4),repeat=3))
TABLE=dict(zip(TRIPLES,F3))

def need(ok,msg):
    if not ok: raise ValueError(msg)

def beta(g,h):
    return ((g&1)*(h&1)+(g>>1)*(h>>1)+(g>>1)*(h&1))%2

def multiply(x,y):
    g,a=x;h,b=y
    return (g^h,(a+b+beta(g,h))%2)

def omega(x,y,z):
    """Exponent of i in the normalized associator."""
    g,a=x;h,b=y;k,c=z
    return (2*c*beta(g,h)+TABLE.get((g,h,k),0))%4

def half(x): return (2*x[1])%4

def compute():
    G=list(itertools.product(range(4),range(2)));one=(0,0);f=(0,1)
    for g,h,k,l in itertools.product(range(4),repeat=4):
        at=lambda a,b,c:TABLE.get((a,b,c),0)
        need((at(g,h,k)+at(g,h^k,l)+at(h,k,l)-at(g^h,k,l)-at(g,h,k^l)-2*beta(g,h)*beta(k,l))%4==0,'supercocycle')
    for x,y,z in itertools.product(G,repeat=3):
        need(multiply(multiply(x,y),z)==multiply(x,multiply(y,z)),'group associativity')
    need(all(multiply(x,x)==f for x in G if x[0]),'six quaternion elements have square f')
    need(multiply(f,f)==one,'central involution')
    need(all(multiply(x,f)==multiply(f,x)!=x for x in G),'central free action')
    for x,y,z,t in itertools.product(G,repeat=4):
        need((omega(y,z,t)+omega(x,multiply(y,z),t)+omega(x,y,z)-omega(multiply(x,y),z,t)-omega(x,y,multiply(z,t)))%4==0,'ordinary pentagon')
    need(all(omega(one,x,y)==omega(x,one,y)==omega(x,y,one)==0 for x,y in itertools.product(G,repeat=2)),'normalization')
    for x,y in itertools.product(G,repeat=2):
        # Half-braiding f tensor x -> x tensor f, with associator omega.
        need((half(multiply(x,y))-half(x)-half(y)+omega(f,x,y)-omega(x,f,y)+omega(x,y,f))%4==0,'central hexagon')
        need(omega(f,f,x)==omega(f,x,f)==omega(x,f,f)==0,'central square tensorator')
    need(half(f)==2 and all(2*half(x)%4==0 for x in G),'fermionic braiding and central square')
    x,y=(1,0),(2,0)
    need(multiply(x,y)==multiply(f,multiply(y,x)),'f is a commutator')
    # Every scalar character is multiplicative, hence kills a commutator.
    # Explicitly, these are the four characters of Q8/{1,f}=C2 x C2.
    chars=[]
    for u,v in itertools.product(range(2),repeat=2):
        ch={a:(-1)**(u*(a[0]&1)+v*(a[0]>>1))for a in G}
        need(all(ch[multiply(a,b)]==ch[a]*ch[b]for a,b in itertools.product(G,repeat=2)),'scalar character')
        need(ch[f]==1,'all scalar characters take f to plus one')
        chars.append([ch[a]for a in G])
    return {'kind':'unitary_pointed_fermion_without_negative_scalar_character',
        'group':'Q8','objects':[list(x)for x in G],'normalized_supercocycle_exponents_mod4':F3,
        'ordinary_pentagon_checks':8**4,'central_hexagon_checks':8**2,
        'fermion_underlying_object':list(f),'fermion_self_braiding':-1,
        'fermion_square_is_unit':True,'fermion_action_is_free':True,
        'quotient_simple_types':'four M-type simples; no Q-type simple',
        'all_scalar_characters':chars,'negative_fermion_scalar_characters':0,
        'scope':'counterexample to the proposed universal implication; no rank8 model claim',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=compute();path=HERE/'fermion_no_negative_character.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'receipt mismatch')
    print('PASS unitary Vec^omega(Q8): free central fermion, all-M quotient, no scalar character f=-1')
