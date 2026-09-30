"""Exact finite-level realization of saturated cyclic spans in quartic data.

This checks an explicit equivariant quotient of Ind_B^{SL2(Z/f)} chi.
All universal conductor moment and spectral identities therefore hold on the
checked cyclic span; no categorical realization is asserted. An equivariant
isometric section exists by complete reducibility and polar decomposition,
so this quotient verification also transfers Hermitian moment identities.
"""
import argparse,itertools,json,math,sys,time
from pathlib import Path
from collections import deque
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
from exact import require,evaluate
from dimension_block_support import saturated_characters
from round5_modular_checks import centers
from round5_quartic_pair import digest


def model(f,chi,C):
    units=[a for a in range(f) if math.gcd(a,f)==1]
    require(all(chi[a*b%f]==chi[a]*chi[b] for a in units for b in units),'invalid torus character')
    reps=[];canonical={}
    for v in itertools.product(range(f),repeat=2):
        if math.gcd(*v,f)!=1 or v in canonical:continue
        j=len(reps);reps.append(v)
        for a in units:
            av=(a*v[0]%f,a*v[1]%f);require(av not in canonical,'nonfree projective normalization');canonical[av]=(j,chi[a])
    def operator(g):
        a,b,c,d=g
        return [canonical[((a*x+b*y)%f,(c*x+d*y)%f)] for x,y in reps]
    return dict(representatives=reps,S=operator((0,-1,1,0)),T=operator((1,1,0,1)),start=canonical[1,0])


def span_rank(vectors,C):
    basis=[]
    for v in vectors:
        v=list(v)
        for j,b in basis:
            if v[j]:a=v[j];v=[x-a*y for x,y in zip(v,b)]
        j=next((j for j,x in enumerate(v) if x),None)
        if j is not None:a=v[j];basis.append((j,[x/a for x in v]))
    return len(basis)


def check(data,ds,S,ee):
    C=data['C'];F=data['F'];pack=saturated_characters(data);require(pack['E']==C,'larger character field not implemented');r=len(S);D=data['DD'];theta=[C.unit**a for a in ee]
    auto=lambda x,a:evaluate(x.to_list(),C.unit**a,C)
    inds=[]
    for a in pack['reps']:
        row=[auto(d/D,a) for d in ds];matches=[j for j,actual in enumerate(S) if actual==row];require(len(matches)==1,'dimension-character row not unique');inds.append(matches[0])
    def act(op,v):
        if op=='T':return [x*z for x,z in zip(v,theta)]
        return [sum((a*b for a,b in zip(row,v) if a and b),C.zero) for row in S]
    reports=[]
    for ch in pack['characters']:
        f=ch['conductor'];require(F==f,'this audit targets full conductor saturation');weights=ch['weights'];w=[C.zero]*r;wb=[C.zero]*r
        for j,z in zip(inds,weights):w[j]=z;wb[j]=auto(z,F-1)
        require(act('T',w)==w,'starting vector not unipotent fixed')
        Sw=act('S',w);compressed=[v if e==0 else C.zero for v,e in zip(Sw,ee)]
        require(compressed==[ch['fourier']*v for v in wb],'saturated opposite-character compression identity')
        character={a:weights[next(j for j,b in enumerate(pack['reps']) if tuple(auto(x,a) for x in data['dims'])==tuple(auto(x,b) for x in data['dims']))] for a in range(F) if math.gcd(a,F)==1}
        attempts=[]
        for conjugate in [False]:
            chi={a:auto(v,F-1) if conjugate else v for a,v in character.items()};m=model(f,chi,C);start,scale=m['start'];v=[None]*len(m['representatives']);v[start]=[x/scale for x in w];q=deque([start]);edges=0;failed=False
            while q and not failed:
                j=q.popleft()
                for op in ['S','T']:
                    i,z=m[op][j];actual=act(op,v[j]);target=[x/z for x in actual];edges+=1
                    if v[i] is None:v[i]=target;q.append(i)
                    elif v[i]!=target:failed=True;break
            attempts.append(dict(conjugate_character=conjugate,passed=not failed,edges=edges))
            if not failed:
                require(all(x is not None for x in v),'projective orbit disconnected');require(edges==2*len(v),'incomplete generator edges');rank=span_rank(v,C)
                reports.append(dict(conductor=f,character_phases=ch['phases'],dimension_character_indices=inds,compression_verified=True,induced_dimension=len(v),cyclic_dimension=rank,checked_generator_edges=edges,conjugate_character=conjugate,intertwiner_sha256=digest([[[str(c) for c in x.to_list()] for x in row] for row in v]),attempts=attempts,all_universal_moment_and_spectral_identities_follow=True));break
        else:raise ValueError('no finite induced-module intertwiner: further analysis required')
    return reports


def reconstruct():
    result=[]
    for rid in ['R6_4_22','R6_4_91']:
        R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']==rid);cert=json.load(open(ROOT/f'research/round5/quartic_pair/{rid}_center_reconstruction.json'))['certificate'];variants=[]
        for data,label,W,ds,S,ee in centers(rid,cert,R):
            reports=check(data,ds,S,ee);variants.append(dict(label=label,checks=reports));print(rid,label,[(x['conductor'],x['induced_dimension'],x['cyclic_dimension']) for x in reports],flush=True)
        result.append(dict(id=rid,source_sha256=digest(cert),variants=variants))
    return dict(passed=True,optimizer_used=False,categorification_claimed=False,results=result)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--verify',action='store_true');a=ap.parse_args()
    import scipy.optimize
    def denied(*_,**__):raise RuntimeError('numerical optimizer disabled')
    scipy.optimize.linprog=scipy.optimize.milp=denied
    start=time.monotonic();cert=reconstruct()
    if a.verify:require(cert==json.loads(a.output.read_text()),'conductor intertwiner record differs')
    else:a.output.write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps(dict(passed=True,optimizer_used=False,seconds=time.monotonic()-start)),flush=True)
