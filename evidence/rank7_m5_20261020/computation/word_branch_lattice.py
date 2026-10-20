"""Add word-integrality equations to the finite frame-eight branch lattices."""
import hashlib,json,sys,time
from fractions import Fraction as F
from pathlib import Path
from inactive_lattice import hermite_basis,prepare,check_counts,require
from word_coefficients import coefficients,modular,q
HERE=Path(__file__).resolve().parent;INPUT=HERE.parent/'integral_gram'


def main():
    rid='R7_5_3895';N=next(r['tensor'] for r in json.loads((HERE/'source_frontier.json').read_text()) if r['id']==rid)
    ds,D,B,zs,T,signs=q.source_data(N,rid);table=modular.ExactQuadraticCharacterTable(N,ds,5)
    dom=next(d for d in json.loads((INPUT/(rid+'_domains.json')).read_text()) if d['low_index']==8)
    words=[[1]*4,[1]*5];V=coefficients(table,dom,words);known=list(map(F,V['known']));orbcols=[list(map(F,row)) for row in V['orbits']]
    (HERE/(rid+'_frame8_word_coefficients.json')).write_text(json.dumps(V,indent=2)+'\n')
    print(json.dumps({'event':'coefficients','orbits':len(orbcols),'known':list(map(str,known))}),flush=True)
    systems={};originals={}
    for case in (0,2,4,6):
        old=json.loads((INPUT/f'{rid}_system_8_{case}.json').read_text());originals[case]=old;cols=[];width=len(old['rhs'])
        for j,col in enumerate(old['columns']):
            if j<len(old['phase_selection']):
                phase_index=old['phase_selection'][j];tail=[old['multipliers'][phase_index]*x for x in orbcols[phase_index//10]]
            else:tail=[F(0)]*len(known)
            cols.append(list(map(F,col))+tail)
        rhs=list(map(F,old['rhs']))+[-x for x in known]
        for wi in range(len(words)):
            col=[F(0)]*len(rhs);col[width+2*wi]=-1;cols.append(col)
        cols,rhs=modular.integral_system(cols,rhs);systems[case]={'columns':cols,'rhs':rhs}
    branches=json.loads((INPUT/f'{rid}_active_8.json').read_text())['branches']
    pruning=json.loads((HERE/f'{rid}_branch_lattice_8.json').read_text())['branches']
    output={'id':rid,'low_index':8,'words':words,'results':[],'status':'partial'}
    for ix in (0,19,160,165):
        start=time.monotonic();counts=dict(branches[ix]);prior=next(r for r in pruning if r['index']==ix)
        kept=prior['kept_columns']+list(range(len(originals[0]['columns']),len(systems[0]['columns'])))
        columns=[systems[0]['columns'][j] for j in kept];basis=hermite_basis(columns)
        cases=[]
        for case,system in systems.items():
            require([system['columns'][j] for j in kept]==columns,'shared augmented inactive columns')
            rhs=[b-sum(system['columns'][j][i]*c for j,c in counts.items()) for i,b in enumerate(system['rhs'])]
            prepared=prepare(columns,rhs,[],basis=basis);okay,why=check_counts(prepared,[],return_failure=True)
            cases.append({'case':case,'lattice_pass':okay,'failure':why,'prepared':prepared})
        item={'branch':ix,'kept_columns':kept,'active_counts':branches[ix],'cases':cases,'seconds':time.monotonic()-start};output['results'].append(item)
        (HERE/f'{rid}_word_branch_lattice.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
        print(json.dumps({'branch':ix,'rank':len(basis),'columns':len(columns),'cases_passing':[x['case'] for x in cases if x['lattice_pass']],'seconds':item['seconds']}),flush=True)
    output['status']='complete';(HERE/f'{rid}_word_branch_lattice.json').write_text(json.dumps(output,separators=(',',':'))+'\n')

if __name__=='__main__':main()
