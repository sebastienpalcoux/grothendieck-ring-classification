#!/usr/bin/env python3
"""Unrestricted parity-domain review of the R721/R1154 Galois-PU gates.

Uses the frozen ordered associativity equations, but removes every
positive-indicator/modulo-four domain restriction. No commutativity
is imposed. Every resulting tensor is checked in all 512 positions.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,re,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent;OLD=HERE.parent.parent/'rank8_m3_20261021'
sys.path.insert(0,str(OLD/'noncommutative'))
import scalar_sieve as old

def need(ok,message):
    if not ok:raise ValueError(message)

def unrestricted(R):
    from oriented_signed import problem
    p=problem(R);du=old.dual(R)
    domains=[list(range(-R[a][b][du[c]],R[a][b][du[c]]+1,2)) for orb in p['active'] for a,b,c in [orb[0]]]
    pattern=r'case (\d+):for\(int x:vector<int>\{([^}]*)\}\)\{v\[(\d+)\]=x;'
    def replacement(m):
        level,var=int(m[1]),int(m[3]);need(p['order'][level]==var,'enumeration variable order')
        need([int(x) for x in m[2].split(',') if x]==p['domains'][var],'old domain source mismatch')
        need(max(map(abs,domains[var]))==max(map(abs,p['domains'][var])),'native range bound changed')
        return 'case '+str(level)+':for(int x:vector<int>{'+','.join(map(str,domains[var]))+'}){v['+str(var)+']=x;'
    cpp,count=re.subn(pattern,replacement,p['source']);need(count==len(domains),'all domains expanded')
    with tempfile.TemporaryDirectory() as directory:
        source=Path(directory)/'enum.cpp';exe=Path(directory)/'enum';source.write_text(cpp)
        subprocess.run(['g++','-O3','-std=c++17',str(source),'-o',str(exe)],check=True,capture_output=True)
        result=subprocess.run([str(exe)],check=True,capture_output=True,text=True,timeout=240)
    vals=sorted(tuple(map(int,line.split())) for line in result.stdout.splitlines())
    need(len(vals)==len(set(vals)),'duplicate signed tensor')
    p['domains']=domains
    return vals,p,result.stderr.strip()

def compute(source):
    R=source['tensor'];need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==source['tensor_sha256'],'source hash')
    vals,p,statistics=unrestricted(R);print(source['id'],'unrestricted enumeration complete',statistics,flush=True)
    a=old.ScalarCharacters(R);du=a.du
    ordinary=old.character_obstructions(R,a.cf);fp=old.pc(a.fp()[0])
    need([r['factor'] for r in ordinary if r['obstruction'] is None]==[fp],'FP orbit is not unique ordinary survivor')
    # Full sign-gauge classes, reducing only repeated algebraic computations.
    signs=[(1,)+tail for tail in itertools.product((-1,1),repeat=7) if all(((1,)+tail)[i]==((1,)+tail)[du[i]] for i in range(8))]
    masks=[tuple(g[x]*g[y]*g[z] for orb in p['active'] for x,y,z in [orb[0]]) for g in signs]
    groups={}
    for v in vals:
        T=old.from_values(R,p,v);old.validate_general(T)
        representative=min(tuple(x*y for x,y in zip(v,mask)) for mask in masks)
        groups.setdefault(representative,[]).append(v)
    reports=[]
    for representative,members in sorted(groups.items()):
        T=old.from_values(R,p,representative);gauge=old.proofs.gauge_original(T,R)
        if gauge is not None:
            need(all(T[i][j][k]==gauge[i]*gauge[j]*gauge[k]*R[i][j][k] for i in range(8) for j in range(8) for k in range(8)),'full gauge identity')
            report={'kind':'spherical_section','gauge_signs':gauge}
        else:
            signed=old.ScalarCharacters(T);characters=old.character_obstructions(T,a.cf+signed.cf)
            need(all(c['obstruction'] and c['obstruction']['kind'] in ('zero','duality','norm') for c in characters),'unrestricted nongauge scalar survivor')
            report={'kind':'nongauge_excluded','matrix_formal_codegree':str(signed.matrix_codegree),'characters':characters}
        reports.append({'representative':list(representative),'members':len(members),**report})
    return {'id':source['id'],'tensor_sha256':source['tensor_sha256'],'signed_variables':len(p['domains']),'normalized_indicator_domains_used':False,'commutativity_assumed':False,'complete_signed_count':len(vals),'native_statistics':statistics,'signed_values_sha256':hashlib.sha256(json.dumps(vals,separators=(',',':')).encode()).hexdigest(),'gauge_classes':reports,'ordinary_characters':ordinary,'fp_character_factor':fp,'conclusion':'every categorification is spherical and has a pseudo-unitary Galois conjugate; no existence or exclusion conclusion'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args()
    census=json.loads((OLD/'pipeline/census_m3.json').read_text());out=[compute(next(s for s in census if s['id']==rid)) for rid in ('R8_3_721','R8_3_1154')]
    path=HERE/'nc_gate_unrestricted.json'
    if args.write:path.write_text(json.dumps(out,indent=2)+'\n')
    else:need(json.loads(path.read_text())==out,'unrestricted reviewer receipt changed')
    print('PASS: complete unrestricted signed Galois-PU gates')
