"""Independent full-S matrix review of the R721 twist/balancing refinement.

Uses SymPy's domain-matrix elimination, not the discovery elimination code.
Reconstructs unnormalized S rows and uses STS directly with the center global
dimension D^2. Reads only the fixed tensor/character and action inputs.
"""
from pathlib import Path
from hashlib import sha256
from itertools import combinations_with_replacement, product
import argparse
import json
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]
OLD=ROOT/'evidence/rank8_frontier_20261021/noncommutative'
sys.path.insert(0,str(OLD))
import central_support as c
import character_modular as md
import rotation_search as base
from sympy.polys.matrices import DomainMatrix

def check(ok,message):
    if not ok:raise ValueError(message)

def eliminate(rows,K):
    reduced,piv=DomainMatrix(rows,(len(rows),len(rows[0])),K).rref()
    return reduced.to_list(),piv

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    base.install()
    tensor_path=c.OLD.parent/'pipeline/census_m3.json'
    source=next(r for r in json.loads(tensor_path.read_text()) if r['id']=='R8_3_721')
    check(source['tensor_sha256']=='76e26a815651476dfda5c2aa654f0d1327bdc890e08086cb6dbfe39ef9a1cdc5','source')
    R=source['tensor'];a=c.w.data(R);K=a['K'];D=a['D']
    lows=a['lows'][10];chars=md.characters(R,a)
    high=md.full.base.grams.high_columns(a,c.s.Matrix.hstack(*map(c.s.Matrix,lows)))[1]
    columns=list(lows)+[(0,)+tuple(v) for v,z in high]
    dims=[md.value(chars[0],v,K) for v in columns]
    low_cases_path=OLD/'verlinde_low_721.json'
    low_cases=json.loads(low_cases_path.read_text())['cases']
    case_results=[]
    for case in low_cases:
        perm=case['permutation'];inverse=[perm.index(j) for j in range(5)]
        S=[[D/a['codegrees'][e]/K(a['multiplicities'][e])*md.value(chars[e],v,K)
            for v in columns] for e in inverse]
        check(all(S[i][j]==S[j][i] for i in range(5) for j in range(5)),'symmetric low S')
        active=[t for t,n in enumerate(case['multiplicities']) if n]
        rows=[]
        for i,j in combinations_with_replacement(range(5),2):
            rows.append([S[i][5+t]*S[j][5+t] for t in active]+
                [D*S[i][j]-sum((S[i][k]*S[j][k] for k in range(5)),K.zero)])
        red,piv=eliminate(rows,K)
        inconsistent=len(active) in piv
        sums={} if inconsistent else {t:red[k][-1] for k,t in enumerate(active)}
        if perm==[0,1,2,3,4]:
            check(inconsistent or sums[3]==K(-7),'first assignment obstruction')
        else:
            check(not inconsistent and tuple(piv)==tuple(range(4)),'unique twist sums')
            check(sums[3]==K.one,'singleton B twist')
            if 8 in active:check(sums[8]==K.zero,'unsplit C singleton zero')
            if 0 in active:check(sums[0]==K(-4),'A sum')
            if 4 in active:check(sums[4]==K.zero,'C sum')
        case_results.append({'rank':5+sum(case['multiplicities']),
             'permutation':perm,'inconsistent':inconsistent,
             'sums':{str(t):c.ec(v) for t,v in sums.items()}})
    action_path=ROOT/'evidence/rank8_center_followup_20261021/r721_center_extension_receipt.json'
    action=json.loads(action_path.read_text())['case_results'][7]
    check(action['center_rank']==22 and action['permutation']==[0,1,3,2,4],'action input')
    types=[t for t,n in enumerate(action['counts']) for _ in range(n)]
    fullcols=list(lows)+[columns[t+5] for t in types]
    ds=[md.value(chars[0],v,K) for v in fullcols]
    perm=action['permutation'];inverse=[perm.index(j) for j in range(5)]
    S=[[D/a['codegrees'][e]/K(a['multiplicities'][e])*md.value(chars[e],v,K)
        for v in fullcols] for e in inverse]
    outcomes=[]
    for witness in action['witnesses']:
        equations=[]
        for i,N in enumerate(witness['matrices'],1):
            for j in range(22):
                equations.append([K(N[k][j])*ds[k]-(S[i][j] if j==k else K.zero)
                                  for k in range(22)]+[K.zero])
        for j in range(22):
            if j<5 or types[j-5] in (0,3):
                equations.append([K(int(j==k)) for k in range(22)]+
                    [K(-1 if j>=5 and types[j-5]==0 else 1)])
        red,piv=eliminate(equations,K)
        check(22 not in piv,'consistent action balancing')
        zero=[p for row,p in zip(red,piv) if row[-1]==K.zero
              and all(x==K.zero for j,x in enumerate(row[:-1]) if j!=p)]
        expected=sorted(set(action['C_labels'])-{action['C_labels'][v]
                   for edge in witness['C_matching'] for v in edge})
        check(zero==expected,'precisely unmatched vertices forced zero')
        outcomes.append({'matching_size':witness['matching_size'],'zero_twists':zero})
    check(len(outcomes)==46 and sum(not r['zero_twists'] for r in outcomes)==9,'complete action domain')
    # Ordinary second indicators via induction; test all five signs, with
    # the nonselfdual pair fixed to zero directly from the tensor duality.
    dual=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    check(dual==[0,2,1,3,4,5,6,7],'source duality')
    known=[sum((ds[k]*K(fullcols[k][j]) for k in range(10)),K.zero) for j in range(8)]
    C=next(k+5 for k,t in enumerate(types) if t==4)
    B=next(k+5 for k,t in enumerate(types) if t==5)
    indicator_results=[]
    for signs in product((-1,1),repeat=5):
        eps=[1,0,0]+list(signs)
        rows=[[ds[C]*K(fullcols[C][j]),ds[B]*K(fullcols[B][j]),D*K(eps[j])-known[j]]
              for j in range(8)]
        red,piv=eliminate(rows,K)
        if 2 not in piv:
            check(tuple(piv)==(0,1),'unique squared sums')
            indicator_results.append({'indicators':eps,'C2':c.ec(red[0][-1]),'D2':c.ec(red[1][-1])})
    check(len(indicator_results)==1 and indicator_results[0]['C2']==[],'second indicator uniqueness')
    discovery_path=ROOT/'evidence/rank8_next_20261021/r721/twist_balancing_receipt.json'
    discovery=json.loads(discovery_path.read_text())
    check(indicator_results[0]['indicators']==discovery['fs2_solution']['indicators'] and
          indicator_results[0]['D2']==discovery['fs2_solution']['D_square_twist_sum'],'discovery agreement')
    paths=[tensor_path,low_cases_path,action_path,discovery_path]
    out={'schema':'r721-independent-twist-review/v1','passed':True,
         'scope':'Necessary center constraints; no source-ring categorifiability decision',
         'sts_cases':case_results,'actions':outcomes,'fs2':indicator_results,
         'source_sha256':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in paths},
         'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(out,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
