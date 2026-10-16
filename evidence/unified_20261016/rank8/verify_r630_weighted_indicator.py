#!/usr/bin/env python3
"""Source-bound exact arithmetic for the conductor-40 third-indicator obstruction.
The only finite search is the separately audited structural sphericality gate;
no center enumeration, numerical optimization, or twist search is used.
"""
import argparse,gzip,hashlib,importlib.util,json
from pathlib import Path

ARCHIVE_SHA='35a8d69e9af8c873b3003890218a35b38b792abb89c19066f6705bf9c1c1d1ed'
def need(b,msg):
    if not b:raise RuntimeError(msg)
def flat(R):return tuple(c for M in R for row in M for c in row)
def mul(a,b):return(a[0]*b[0]+10*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def verify(repo):
    source=repo/'supplements/rank8/data/rank8_tables.txt.gz'
    need(hashlib.sha256(source.read_bytes()).hexdigest()==ARCHIVE_SHA,'immutable census archive')
    rs=[]
    for line in gzip.open(source,'rt'):
        if not line.strip():continue
        R=json.loads(line.replace('{','[').replace('}',']'))
        if max(flat(R))==2:rs.append(R)
    rs.sort(key=flat);R=rs[629]
    gatepath=repo/'evidence/unified_20261016/rank8/verify_hi6_pair_galois_pu.py'
    spec=importlib.util.spec_from_file_location('hi6_spherical_gate',gatepath)
    gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    structural=gate.verify(R,630)
    a=[1,1,2,3,3,2,4,4];b=[0,0,1,1,1,1,1,1]
    d=list(zip(a,b));D=tuple(sum(mul(x,x)[j]for x in d)for j in range(2))
    need(D==(120,36),'global dimension')
    need(all(mul(d[i],d[j])==tuple(sum(R[i][j][k]*d[k][c]for k in range(8))for c in range(2))for i in range(8)for j in range(8)),'FP homomorphism')
    fs=structural['formal_codegrees']
    need(fs==[(120,0,36,0),(120,0,-36,0)]+[(k,0,0,0)for k in[4,6,6,12,12,12]],'two irrational codegrees, all other codegrees rational')
    need(mul(D,(120,-36))==(1440,0),'global norm')
    need(mul((19,6),(120,-36))==D,'unique Galois-unit dimension')
    # 1/D-1/Dbar = -72 sqrt(10)/1440 = -sqrt(10)/20;
    # its square is 1/40, the primitive quadratic conductor.
    need(72*20==1440 and 10*40==20**2,'exact conductor-40 compression equality')
    ell=[3*x-10*y for x,y in d]
    need(ell==[3,3,-4,-1,-1,-4,2,2],'source weights')
    need(3*D[0]-10*D[1]==0,'weights annihilate rational multiples of D')
    need(40%3==1 and 40%3!=0,'Kronecker character chi_40(3)=+1')
    cube=[sum(R[i][i][k]*R[k][i][0]for k in range(8))for i in range(8)]
    need(cube==[1,0,0,1,1,1,0,0],'source cubic invariant multiplicities')
    terms=[(i,ell[i])for i in range(1,8)if cube[i]]
    need(terms==[(3,-1),(4,-1),(5,-4)],'only three nonunit third-indicator terms')
    need(all(cube[i]==1 for i,c in terms),'three one-dimensional rotation spaces')
    weights=sorted(abs(c)for i,c in terms)
    need(weights[-1]>sum(weights[:-1]),'strict triangle contradiction')
    return {'status':'PASS','criterion':'quadratic_conductor_Galois_indicator','scope':'general_complex_via_audited_HI6_spherical_Galois_gate','id':'R8_2_630','source_sha256':ARCHIVE_SHA,'tensor_sha256':structural['tensor_sha256'],'general_scope_dependency':'HI6_PAIR_GALOIS_PU.md','gate_verifier_sha256':hashlib.sha256(gatepath.read_bytes()).hexdigest(),'signed_spherical_gate_branches':structural['signed_branches'],'FP_dimensions':d,'global_dimension':D,'formal_codegrees':fs,'conductor':40,'Galois_power':3,'integer_weights':ell,'cubic_invariant_dimensions':cube,'nonunit_weighted_terms':terms,'triangle_largest_side':weights[-1],'triangle_other_sides_sum':sum(weights[:-1]),'center_enumeration_used':False,'optimizer_used':False,'proof':'R630_WEIGHTED_GALOIS_INDICATOR_PROOF.md'}
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();r=verify(a.repo);t=json.dumps(r,indent=2)+'\n'
    if a.output:a.output.write_text(t)
    print(t)
if __name__=='__main__':main()
