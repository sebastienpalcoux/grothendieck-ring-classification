#!/usr/bin/env python3
"""Exact necessary Morita reduction for R8_1_9; does not decide categorifiability."""
import argparse,hashlib,sys
import itertools,json,gzip
from pathlib import Path
def flat(r):return tuple(v for m in r for row in m for v in row)
def group(kind):return [[(a+b)%4 if kind=='C4' else a^b for b in range(4)] for a in range(4)]
def automorphisms(g):return [(0,*p) for p in itertools.permutations(range(1,4)) if all((0,*p)[g[a][b]]==g[(0,*p)[a]][(0,*p)[b]] for a in range(4) for b in range(4))]
def construct(g,tau,g0,m):
 R=[[[0]*8 for j in range(8)] for i in range(8)]
 for a in range(4):
  for b in range(4):
   R[a][b][g[a][b]]=1;R[a][4+b][4+g[a][b]]=1;R[4+a][b][4+g[a][tau[b]]]=1
   q=g[a][tau[b]];R[4+a][4+b][g[q][g0]]=1
   for k in range(4):R[4+a][4+b][4+g[q][k]]=m[k]
 return R
def permute(R,p):
 out=[[[0]*8 for j in range(8)] for i in range(8)]
 for i,j,k in itertools.product(range(8),repeat=3):out[p[i]][p[j]][p[k]]=R[i][j][k]
 return flat(out)
def canonical(R,g):
 return min(permute(R,list(s)+[4+g[s[i]][h] for i in range(4)]) for s in automorphisms(g) for h in range(4))
def axioms(R):
 du=[]
 for i in range(8):
  ks=[j for j in range(8) if R[i][j][0]]
  if len(ks)!=1 or R[i][ks[0]][0]!=1:return None
  du.append(ks[0])
 if any(du[du[i]]!=i for i in range(8)):return None
 if any(R[i][j][k]!=R[du[i]][k][j] or R[i][j][k]!=R[k][du[j]][i] for i,j,k in itertools.product(range(8),repeat=3)):return None
 # Group relations and mixed triples checked by construction; check all anyway.
 for i,j,k,l in itertools.product(range(8),repeat=4):
  if sum(R[i][j][s]*R[s][k][l] for s in range(8))!=sum(R[j][k][s]*R[i][s][l] for s in range(8)):return None
 return du

def require(condition,message):
    if not condition:raise RuntimeError(message)

def run(repo):
    ALL={}
    for kind in ['C4','V4']:
     g=group(kind)
     for tau in automorphisms(g):
      if any(tau[tau[a]]!=a for a in range(4)):continue
      for g0 in range(4):
       for m in itertools.product(range(5),repeat=4):
        if sum(m)!=4:continue
        # inexpensive coefficient constraints
        if tau[g0]!=g0 or any(m[g[k][tau[a]]]!=m[g[k][a]] for k in range(4) for a in range(4)):continue
        R=construct(g,tau,g0,m);du=axioms(R)
        if du is None:continue
        key=(kind,canonical(R,g))
        if key not in ALL:ALL[key]={'group':kind,'tau':tau,'g0':g0,'m':m,'dual':du,'tensor':R}
    raw=[json.loads(l.replace('{','[').replace('}',']')) for l in gzip.open(repo/'supplements/rank8/data/rank8_tables.txt.gz','rt')]
    by={n:sorted([R for R in raw if max(flat(R))==n],key=flat) for n in [1,2]}
    for n,rs in by.items():
     for idx,R in enumerate(rs,1):
      inv=[a for a in range(8) if sum(R[a][next(j for j in range(8) if R[a][j][0])])==1]
      if len(inv)!=4:continue
      non=[a for a in range(8) if a not in inv]
      # Require free invertible action and each pair of noninvertibles 1 pointed plus4 nonpointed coeffs.
      if any(sum(R[i][j][k] for k in inv)!=1 or sum(R[i][j][k] for k in non)!=4 for i in non for j in non):continue
      p=[0]+[x for x in inv if x]+non
      S=[[[R[i][j][k] for k in p] for j in p] for i in p]
      g=[[S[i][j].index(1) for j in range(4)] for i in range(4)]
      for kind in ['C4','V4']:
       G=group(kind)
       maps=[(0,*q) for q in itertools.permutations(range(1,4)) if all((0,*q)[g[a][b]]==G[(0,*q)[a]][(0,*q)[b]] for a in range(4) for b in range(4))]
       if not maps:continue
       s=maps[0];rho=4;P=[s[i] for i in range(4)]+[None]*4
       for i in range(4):P[S[i][rho].index(1)]=4+s[i]
       if any(x is None for x in P):continue
       f=permute(S,P);T=[[[f[i*64+j*8+k] for k in range(8)] for j in range(8)] for i in range(8)]
       key=(kind,canonical(T,G))
       if key not in ALL:raise RuntimeError(('census missing',n,idx))
       ALL[key]['source_id']=f'R8_{n}_{idx}'
    records=list(ALL.values())
    for c in records:
     G=group(c['group']); beta=[]
     for b in range(1,4):
      if G[b][b]!=0 or c['tau'][b]!=b or c['g0'] not in [0,b]:continue
      cosets=[];seen=set()
      for h in range(4):
       if h not in seen:
        pair=[h,G[h][b]];cosets.append(pair);seen.update(pair)
      if any(sum(c['m'][h] for h in p)!=2 for p in cosets):continue
      if any(c['tau'][h] not in [h,G[h][b]] for h in range(4)):continue
      beta.append(b)
     c['possible_dual_character_beta']=beta

    ledger={c['id']:c for c in json.loads((repo/'supplements/rank8/data/decisions.json').read_text())}
    source=by[1][8]
    digest=hashlib.sha256(json.dumps(source,separators=(',',':')).encode()).hexdigest()
    expected='1718ab13b6969ed751b621f7303b9e2bb29bb8280f692315499b130a420538f6'
    require(digest==expected==ledger['R8_1_9']['tensor_sha256'],'source hash')
    du=axioms(source)
    require(du==[0,2,1,4,3,5,6,7],'source duality')
    require(all(source[i][j]==source[j][i] for i in range(8) for j in range(8)),'source commutativity')
    pointed=[0,1,7,2]
    require(all(source[pointed[a]][pointed[b]][pointed[(a+b)%4]]==1 for a in range(4) for b in range(4)),'pointed C4')
    cubes={}
    for x in [5,6]:
        cube=[sum(source[x][x][j]*source[j][x][k] for j in range(8)) for k in range(8)]
        require(all(cube[g]==1 for g in pointed),'odd pointed cube multiplicities')
        cubes[str(x)]=cube
    # Exact Z[d]/(d²-4d-1) positive dimension character.
    dims=[(1,0) if i in pointed else (0,1) for i in range(8)]
    for i,j in itertools.product(range(8),repeat=2):
        a,b=dims[i];c,d=dims[j]
        lhs=(a*c+b*d,a*d+b*c+4*b*d)
        rhs=tuple(sum(source[i][j][k]*dims[k][q] for k in range(8)) for q in range(2))
        require(lhs==rhs,'dimension character')
    orbits=[[0,7],[1,2],[3,4],[5,6]]
    action=[[[sum(source[i][o[0]][x] for x in target) for o in orbits] for target in orbits] for i in range(8)]
    reps=[0,1,3,5]
    basis=[action[i] for i in reps]
    I,P,R,PR=basis
    def mul(A,B):return [[sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
    def add(*terms):return [[sum(n*A[i][j] for n,A in terms) for j in range(4)] for i in range(4)]
    require(mul(P,P)==I and mul(P,R)==PR==mul(R,P),'module product')
    require(mul(R,R)==add((1,I),(2,R),(2,PR)),'2D2 quotient')
    require(all([M[a][0] for a in range(4)]==[int(a==j) for a in range(4)] for j,M in enumerate(basis)),'cyclic unit column')
    require(action[0]==action[7] and action[1]==action[2] and action[3]==action[4] and action[5]==action[6],'module fibres')
    for o in orbits:
        x=o[0]
        actual={source[source[h][x].index(1)][k].index(1) for h in [0,7] for k in [0,7]}
        stab=sum(source[source[h][x].index(1)][k][x] for h in [0,7] for k in [0,7])
        require(actual==set(o) and stab==2,'bimodule support orbit')
    require(len(records)==22,'complete abstract census size')
    good=[c for c in records if c['possible_dual_character_beta']]
    expected9={'R8_2_25','R8_1_9','R8_1_15','R8_1_12','R8_2_477','R8_2_478','R8_1_69','R8_1_53','R8_1_49'}
    require({c.get('source_id') for c in good}==expected9,'module-compatible list')
    excluded={'R8_2_25','R8_2_478','R8_1_49'}
    require(all(ledger[x]['status']=='excluded' for x in excluded),'existing exclusion boundary')
    for c in good:
        name=c['source_id'];r=c['tensor'];dual=c['dual']
        _,sm,si=name.split('_')
        source_tensor=by[int(sm)][int(si)-1]
        c['source_sha256']=hashlib.sha256(json.dumps(source_tensor,separators=(',',':')).encode()).hexdigest()
        require(c['source_sha256']==ledger[name]['tensor_sha256'],'candidate source digest')
        if name in ['R8_1_15','R8_1_69']:
            require(all(dual[x]==x for x in range(4,8)),'selfdual noninvertibles')
            for x in range(4,8):
                unit_cube=sum(r[x][x][j]*r[j][x][0] for j in range(8))
                require(unit_cube%2==1,'forced positive noninvertible indicator')
            c['noninvertible_total_indicator_coefficient']=4
        elif name in ['R8_1_12','R8_1_53']:
            require(all(dual[x]!=x for x in range(4,8)),'complex noninvertibles')
            c['noninvertible_total_indicator_coefficient']=0
        elif name=='R8_1_9':
            require(sum(dual[x]==x for x in range(4,8))==2,'R9 indicator coefficient')
            c['noninvertible_total_indicator_coefficient']=2
        elif name=='R8_2_477':
            require(all(dual[x]==x for x in range(4,8)),'R477 indicator signs')
            signs=[z for z in itertools.product([-1,1],repeat=4) if sum(z)==2]
            require(len(signs)==4 and all(z.count(1)==3 for z in signs),'three-positive one-negative')
            c['required_noninvertible_sign_counts']={'positive':3,'negative':1}
    survivors=[c['source_id'] for c in good if c['source_id'] not in excluded and c.get('noninvertible_total_indicator_coefficient',2)==2]
    require(set(survivors)=={'R8_1_9','R8_2_477'},'final two alternatives')
    # Standard pointed dual cocycle for the untwisted C4 subgroup extension.
    G=list(itertools.product(range(2),repeat=2))
    plus=lambda a,b:tuple(x^y for x,y in zip(a,b))
    omega=lambda a,b,c:(-1)**(a[1]*b[0]*c[0])
    for a,b,c,d in itertools.product(G,repeat=4):
        require(omega(b,c,d)*omega(a,plus(b,c),d)*omega(a,b,c)==omega(plus(a,b),c,d)*omega(a,b,plus(c,d)),'pointed dual cocycle')
    pointed_signs=[omega(g,g,g) for g in G if g!=(0,0)]
    require(sorted(pointed_signs)==[-1,1,1],'one-anomaly pointed class')
    return {'status':'PASS','scope':'necessary_conditions_only_no_status_change','source_id':'R8_1_9','source_sha256':digest,'cubes':cubes,'module_basis':basis,'abstract_quadratic_tensors':len(records),'module_compatible_tensors':[{k:v for k,v in c.items() if k!='tensor'} for c in good],'final_dual_alternatives':sorted(survivors),'pointed_dual_nonidentity_indicators':pointed_signs,'categorical_scope':'The proved odd-isotypic, separable-Morita and center-indicator arguments are explained in R9_MORITA_FRONTIER.md; this checker verifies their finite source hypotheses.'}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.repo.resolve()),sort_keys=True,indent=2))
if __name__=='__main__':main()
