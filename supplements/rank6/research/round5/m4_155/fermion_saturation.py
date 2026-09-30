"""Unit-column saturation after every compatible canonical fermion action.

Copy permutations inside each restriction/charge class normalize an involution
to its number of two-cycles. Positive-charge classes have no fermion-fixed
objects. This yields a complete finite necessary action domain.
"""
import argparse,itertools,json,sys
from pathlib import Path
from algebra_saturation import check_pair
import sympy as s
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from exact import require

def actions(R,W,eps):
    groups={}
    for i,v in enumerate(W):groups.setdefault((tuple(v),eps[i]),[]).append(i)
    mul=lambda v:tuple(sum(v[j]*R[3][j][k] for j in range(6)) for k in range(6))
    variable=[key for key in sorted(groups) if key[1]==-1 and mul(key[0])==key[0]]
    for choices in itertools.product(*(range(len(groups[key])//2+1) for key in variable)):
        prescribed=dict(zip(variable,choices));perm=list(range(len(W)))
        for(v,e),ids in groups.items():
            other=groups[mul(v),e];require(len(ids)==len(other),'fermion orbit counts disagree')
            if mul(v)!=v:
                for i,j in zip(ids,other):perm[i]=j
            else:
                require(e==-1 or len(ids)%2==0,'fermion has forced positive-charge fixed point')
                pairs=len(ids)//2 if e==1 else prescribed[v,e]
                for j in range(pairs):a,b=ids[2*j:2*j+2];perm[a]=b;perm[b]=a
        require(all(perm[perm[i]]==i for i in range(len(W))),'not an involution')
        yield perm

def calculate():
    src=json.loads((Path(__file__).parent/'packet_frontier.json').read_text());R=next(x['N'] for x in json.loads((P/'data/census.json').read_text()) if x['id']=='R6_4_155');out=[]
    for split in src['splittings']:
        for survivor in split['survivors']:
            require(split['quadratic_sign']==-1,'unexpected surviving pointed quadratic form')
            W=next(c for c in src['cases'] if c['profile']==split['profile'])['survivors'][split['orientation']]['W'];unit=W.index([1,0,0,0,0,0]);n=len(W);cases=[]
            for j,perm in enumerate(actions(R,W,survivor['charges'])):
                F=s.zeros(n)
                for i,a in enumerate(perm):F[a,i]=1
                result=check_pair(s.Matrix(survivor['Na']),s.Matrix(survivor['Nb']),unit,[F]);result.pop('saturated_basis',None);result.pop('positive_cone',None);case=dict(action=j,permutation=perm,**result);cases.append(case)
                print(split['profile'],j,result['passed'],result['reason'],result.get('algebra_dimension'),flush=True)
            out.append(dict(profile=split['profile'],orientation=split['orientation'],actions=cases,surviving_actions=[x['action'] for x in cases if x['passed']]))
    return dict(id='R6_4_155',scope='complete_canonical_fermion_action_domain_on_six_retained_profiles',optimizer_used=False,complete=True,cases=out)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--verify',action='store_true');args=ap.parse_args();p=Path(__file__).with_suffix('.json');result=calculate()
    if args.verify:require(result==json.loads(p.read_text()),'fermion saturation certificate differs')
    else:p.write_text(json.dumps(result,indent=2)+'\n')
