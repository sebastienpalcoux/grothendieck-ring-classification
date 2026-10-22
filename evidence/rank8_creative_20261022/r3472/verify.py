#!/usr/bin/env python3
"""Replay conditional R3472 rank-two Morita restrictions using exact integers."""
import argparse, ast, hashlib, json
from pathlib import Path
from product_equations import dualities, equations
from exact_integer import solve
from second_branch_count import count

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SPECTRA=ROOT/'evidence/rank8_research_20261022/r1768_r3472/r3472_rank_two_dual_spectra.json'
ACTIONS=ROOT/'evidence/rank8_next_20261021/quadratic/action_classes.json'
TENSOR=ROOT/'site/dist/downloads/fusion-tensors/R8_3_3472.txt'

def need(ok,why):
    if not ok:raise ValueError(why)

def main(write=False):
    spectra=json.loads(SPECTRA.read_text())['spectra']
    records=[]
    for index in (0,3,5):
      row=spectra[index]
      for dims,dual in dualities(row['invertible_count'],row['nonintegral_dimensions']):
        A,b,variables=equations(dims,dual,row['invertible_count'])
        result=solve(A,b)
        need(result['complete'] and not result['solutions'],'Exhaustion did not exclude the product system')
        records.append({'spectrum_index':index,'duality':dual,'dimensions':[list(d) for d in dims],
                        'variables':len(variables),'equations':len(A),
                        'complete_search_nodes':result['nodes'],'outcome':'no nonnegative integer solution'})
    need(len(records)==6,'Duality coverage changed')
    remaining=[i for i,r in enumerate(spectra) if not r['excluded_by_orbit_test'] and i not in (0,3,5)]
    need(remaining==[1,2,4,6,7,8,10],'First-branch count changed')

    # Exact positive control: the input fusion ring itself satisfies the equations.
    R=ast.literal_eval(TENSOR.read_text());dual=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    actions=json.loads(ACTIONS.read_text())['R8_3_3472']['complete_action_classes']
    rank_two=[r['actions'] for r in actions if r['module_rank']==2]
    need(sorted(r[1] for r in rank_two)==sorted([[[1,5],[5,11]],[[5,7],[7,7]]]),'Input action classes changed')
    act=next(r for r in rank_two if r[1]==[[5,7],[7,7]])
    dims=[]
    for m in act:
        need((m[0][0]+m[1][1])%2==0 and m[0][1]%7==0,'Nonintegral source dimension coordinates')
        dims.append(((m[0][0]+m[1][1])//2,5*m[0][1]//7))
    A,b,v=equations(dims,dual,1)
    x=[R[i][j][dual[k]] for i,j,k in v]
    need(all(sum(c*y for c,y in zip(row,x))==target for row,target in zip(A,b)),
         'Original ring failed the exact positive control')

    # Cauchy: 70^2 <= (35-h)*175 gives h<=7. Then Lagrange integrality.
    hs=[h for h in range(1,8) if 1400%h==0 and 9800%(h*h)==0]
    need(hs==[1,2,5,7],'Integral-subcategory domain changed')
    counts=[count(h) for h in hs]
    need([r['nonintegral_multisets'] for r in counts]==[272348,124228,3900,2],'Arithmetic count changed')
    # h=7 equality forces (u,t)=(2k,5k), hence sum k^2=7.
    partitions=[(a,b) for a in range(8) for b in range(2) if a+4*b==7]
    need(partitions==[(3,1),(7,0)],'Order-seven equality profiles changed')
    need(sum(r['nonintegral_multisets'] for r in counts)==400478,'Second-branch total changed')
    out={'case_id':'R8_3_3472','status':'PASS',
      'scope':'conditional necessary restrictions if the specified based module lifts to an indecomposable module category',
      'first_branch_generator':[[5,7],[7,7]],'second_branch_generator':[[1,5],[5,11]],
      'first_branch_previous_spectra':10,'first_branch_product_excluded_spectra':3,
      'first_branch_retained_indices':remaining,'first_branch_exact_product_checks':records,
      'second_branch_integral_subcategory_dimensions':hs,'second_branch_arithmetic_counts':counts,
      'second_branch_arithmetic_total':400478,'second_branch_orbit_excluded':1,
      'second_branch_arithmetic_after_orbit':400477,
      'positive_control':'Original R3472 fusion tensor satisfies all constructed Frobenius/unit/dimension equations',
      'general_categorification_status':'unresolved','new_model_constructed':False,
      'inputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (SPECTRA,ACTIONS,TENSOR)}}
    path=HERE/'verification.json'
    if write:path.write_text(json.dumps(out,indent=2)+'\n')
    else:need(json.loads(path.read_text())==out,'Saved verification receipt changed')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true')
    main(parser.parse_args().write)
