"""Refresh all subgroup cocycles for the two remaining Sylow-16 pairs."""
from setup import *
sys.path.insert(0,str(ROUND3))
from subgroup_twist_fusion import fusion
import sympy as sp


def main():
    cases=json.loads((OUT/'h16_all_cases.json').read_text())
    common.require(len(cases)==12,'all 4+8 Schur classes')
    F=sp.QQ.cyclotomic_field(96);zeta=F.unit
    def cv(v):return sum((F(c)*zeta**j for j,c in enumerate(v) if c),F.zero)
    def conj(v):return sum((F(c)*zeta**(-j) for j,c in enumerate(v) if c),F.zero)
    results=[]
    for ci,r in enumerate(cases):
        G,H,P=r['table'],r['subgroup'],r['psi'];hi={a:i for i,a in enumerate(H)}
        common.require(len(H)==16 and G[0]==list(range(48)),'group coordinates')
        common.require(all(G[G[a][b]][c]==G[a][G[b][c]] for a,b,c in itertools.product(range(48),repeat=3)),'group associativity')
        common.require(all((P[hi[b]][hi[c]]+P[hi[a]][hi[G[b][c]]]-P[hi[G[a][b]]][hi[c]]-P[hi[a]][hi[b]])%2==0 for a,b,c in itertools.product(H,repeat=3)),'actual subgroup cocycle')
        byz={};dims=[]
        for ob in r['objects']:
            K=ob['stab'];dim=cv(ob['char'][0]);common.require(dim in [F(1),F(2)],'fiber dimension1or2')
            dims.append(16//len(K)*int(dim.to_list()[0]));byz.setdefault(ob['z'],[]).append(ob)
        for z,obs in byz.items():
            K=obs[0]['stab']
            common.require(sum(int(cv(o['char'][0]).to_list()[0])**2 for o in obs)==len(K),'complete projective degree sum')
            for i,o in enumerate(obs):
                for j,p in enumerate(obs):
                    common.require(sum((cv(a)*conj(b) for a,b in zip(o['char'],p['char'])),F.zero)==F(len(K)*int(i==j)),'projective character orthogonality')
        dims.sort();out=dict(case=ci,smallgroup=r['smallgroup'],subgroup=H,psi_sha256=digest(P),dimensions=dims)
        if dims==[1]*8+[2]*2+[4]*2:
            M=fusion(r);mult=max(x for a in M for b in a for x in b);matches=[]
            for rid in IDS+['R12_1_30','R12_1_417','R12_1_414','R12_1_531']:
                p=common.based_iso(DATA[rid],M)
                if p is not None:matches.append(dict(id=rid,source_to_model=p))
            common.require(mult>1 or bool(matches),'target tensor accounted for')
            out.update(multiplicity=mult,matches=matches,model_tensor=M)
        results.append(out);print(ci,r['smallgroup'],dims,out.get('multiplicity'),out.get('matches'),flush=True)
    result=dict(status='PASS',cases=results)
    (OUT/'h16_audit.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
    print('PASS',len(results),flush=True)


if __name__=='__main__':main()
