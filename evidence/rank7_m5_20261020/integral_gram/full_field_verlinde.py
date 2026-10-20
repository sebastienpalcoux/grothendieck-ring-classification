"""Integral full-source-field two-moment and low-Verlinde discovery."""
import argparse
import json
import time
from fractions import Fraction as F

import explore as e
import verlinde as v
import q5_full_field as f
from full_source_phases import phase_records
from spectral_induction import Spectrum

q=e.q;m=e.m;HERE=e.HERE


def fifth_primary_refinement(columns,rhs,labels,orbits,records,rid):
    """Split genuine-zero rows by fifth-primary order and impose c,4c.

    Visible phases have fifth-primary part one or five.  True-zero
    multiplicity units four split into those two classes; unit-five
    variables cover fifth-primary orders >=25.  This is a necessary
    relaxation, not an assertion that every split is realizable.
    """
    weights=(2,1,1,2,-2,-2,0) if rid=='R7_5_3895' else (2,1,1,-2,-2,2,0)
    newcols=[];newlabels=[]
    for col,label in zip(columns,labels):
        orders=records[label['phase']]['orders']
        if orders:parts=[int(orders[0]%5==0)]
        elif label['multiplicity_unit']==4:parts=[0,1]
        else:
            q.require(label['multiplicity_unit']==5,'zero-phase semigroup unit')
            parts=[2]
        weight=label['multiplicity_unit']*sum(sum(a*b for a,b in zip(weights,(0,)+tuple(v)))**2 for v,g,z in orbits[label['orbit']])
        for part in parts:
            mass0=weight if part==0 else 0
            mass1=weight if part==1 else 0
            newcols.append(list(col)+[mass1-4*mass0,mass0])
            newlabels.append({**label,'fifth_primary':part})
    newcols += [list(col)+[0,0] for col in columns[len(labels):]]
    newrhs=list(rhs)+[32,24]
    slack=[0]*len(newrhs);slack[-1]=1;newcols.append(slack)
    return newcols,newrhs,newlabels


def run(rid,first=False,time_limit=60,active_branch=None,chi8_branch=None,reuse=None,fp5=False,word_file=None,norm_files=()):
    import numpy as np
    from scipy.optimize import milp,Bounds,LinearConstraint
    from scipy.sparse import csc_matrix
    N=next(r['tensor'] for r in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==rid)
    d,D,B,zs,T,signs=q.source_data(N,rid);table=m.ExactQuadraticCharacterTable(N,d,5)
    records=phase_records(field='F8');pool=[];results=[]
    for dom in e.domains(rid):
        if rid=='R7_5_5039' and dom['low_index']==1:continue
        if rid=='R7_5_3895' and dom['low_index']==6:continue
        low=[tuple(z) for z in dom['low']]
        orbits=[[(tuple(a),tuple(b),tuple(c)) for a,b,c in orb] for orb in dom['orbits']]
        spectrum=Spectrum(table,[(1,0,0,0,0,0,0)]+low,[(a,c) for orb in orbits for a,b,c in orb])
        q.require(not spectrum.missing_low,'eligible low spectrum')
        forbidden=set(map(tuple,spectrum.forbidden))
        orbits=[orb for orb in orbits if all(a not in forbidden for a,b,c in orb)]
        V=v.coefficients(table,{'id':rid,'low_index':dom['low_index'],'low':low,'orbits':orbits})
        known=list(map(F,V['known']));vcols=[list(map(F,c)) for c in V['orbits']]
        words=[]
        if word_file:
            W=json.loads(open(word_file).read())
            q.require(W['domain_sha256']==V['domain_sha256'],'word coefficient domain matches exactly')
            q.require(W['source_sha256']==q.tensor_hash(N),'word coefficient source matches exactly')
            words=W['words'];known+=list(map(F,W['known']))
            vcols=[a+list(map(F,b)) for a,b in zip(vcols,W['orbits'])]
        print(json.dumps({'event':'domain','id':rid,'low':dom['low_index'],'orbits':len(orbits),'phases':len(records)}),flush=True)
        for ci,case in enumerate(dom['cases']):
            if -1 in case['sign']:continue
            columns,rhs,labels=f.build_system(table,low,case['label'],orbits,dom['bound'],D,zs,case['sign'],T,records,rid,chi8_branch=chi8_branch)
            if fp5:columns,rhs,labels=fifth_primary_refinement(columns,rhs,labels,orbits,records,rid)
            norm_records=[json.loads(open(path).read()) for path in norm_files]
            cuts=[]
            if norm_records:
                import integer_norm_cuts as nc
                cutdom={'id':rid,'low':low,'orbits':orbits}
                cuts=[nc.coefficient_cut(table,cutdom,case['label'],N,T.dual,V,record) for record in norm_records]
                columns,rhs,labels=nc.append_cuts(columns,rhs,labels,cuts)
            extra0=len(columns)-len(labels);old=len(rhs)
            cols=[]
            for j,col in enumerate(columns):
                tail=([labels[j]['multiplicity_unit']*x for x in vcols[labels[j]['orbit']]] if j<len(labels) else [F(0)]*len(known))
                cols.append(list(map(F,col))+tail)
            rhs=list(map(F,rhs))+[-x for x in known]
            for ti in range(len(V['triples'])+len(words)):
                col=[F(0)]*len(rhs);col[old+2*ti]=-1;cols.append(col)
            cols,rhs=m.integral_system(cols,rhs)
            fixed_support=[]
            if active_branch is not None:
                q.require(rid=='R7_5_3895','active branch currently implemented only for3895')
                old_system=json.loads((HERE/(rid+'_system_8_'+str(ci)+'.json')).read_text())
                allocation=json.loads((HERE/(rid+'_active_8.json')).read_text())['branches'][active_branch]
                old_orbits=dom['orbits'];desired={}
                for j,count in allocation:
                    original=old_system['phase_selection'][j]
                    key=tuple(tuple(row[0]) for row in old_orbits[original//10])
                    desired[key]=count*old_system['multipliers'][original]
                fixed={}
                for j,lab in enumerate(labels):
                    orb=orbits[lab['orbit']]
                    if not any(row[0][3]!=row[0][4] for row in orb):continue
                    key=tuple(tuple(row[0]) for row in orb);target=desired.get(key,0)
                    q.require(target%lab['multiplicity_unit']==0,'fixed active multiplicity divisible byphaseunit')
                    fixed[j]=target//lab['multiplicity_unit']
                    if fixed[j]:fixed_support.append({**lab,'count':fixed[j]})
                rhs=[b-sum(cols[j][i]*n for j,n in fixed.items()) for i,b in enumerate(rhs)]
                cols=[c for j,c in enumerate(cols) if j not in fixed]
                labels=[lab for j,lab in enumerate(labels) if j not in fixed]
            sep=q.separate(cols,rhs,pool)
            result={'index':dom['low_index'],'case':ci,'phase_variables':len(labels),'exact_separator':sep}
            if reuse and sep is None:
                old_result=next((r for r in json.loads(open(reuse).read())['results'] if r['case']==ci and r.get('exact_feasible')),None)
                if old_result is not None:
                    saved={(r['orbit'],r['phase'],r['multiplicity_unit']):r['count'] for r in old_result['support']}
                    index={(r['orbit'],r['phase'],r['multiplicity_unit']):j for j,r in enumerate(labels)}
                    if set(saved)<=set(index) and extra0==0:
                        counts=[saved.get((r['orbit'],r['phase'],r['multiplicity_unit']),0) for r in labels]+old_result['verlinde_coefficients']
                        if all(sum(c[i]*x for c,x in zip(cols,counts))==b for i,b in enumerate(rhs)):
                            result.update({'status':0,'exact_feasible':True,'support':old_result['support'],'verlinde_coefficients':old_result['verlinde_coefficients'],'reused_witness_exactly_checked':True})
            if sep is None and not result.get('exact_feasible'):
                ub=[min([rhs[i]//col[i] for i in range(21) if col[i]>0] or [np.inf]) for col in cols]
                start=time.monotonic()
                res=milp(np.r_[np.ones(len(labels)),np.zeros(len(cols)-len(labels))],integrality=np.ones(len(cols)),bounds=Bounds(np.zeros(len(cols)),ub),constraints=LinearConstraint(csc_matrix(np.array(cols,dtype=float).T),rhs,rhs),options={'time_limit':time_limit})
                result.update({'status':int(res.status),'seconds':time.monotonic()-start})
                if res.x is not None:
                    counts=[round(float(x)) for x in res.x]
                    result['exact_feasible']=all(x>=0 for x in counts) and all(sum(c[i]*x for c,x in zip(cols,counts))==b for i,b in enumerate(rhs))
                    result['support']=fixed_support+[{**labels[i],'count':n} for i,n in enumerate(counts[:len(labels)]) if n]
                    result['verlinde_coefficients']=counts[len(labels)+extra0:len(labels)+extra0+len(V['triples'])]
                    result['word_multiplicities']=counts[len(labels)+extra0+len(V['triples']):]
            print(json.dumps(result),flush=True);results.append(result)
            output={'id':rid,'phase_records':records,'source_sha256':q.tensor_hash(N),'low':low,'orbits':orbits,'words':words,'chi8_branch':chi8_branch,'fifth_primary_refinement':fp5,'norm_cut_records':norm_records,'norm_cut_coefficients':cuts,'results':results,'separators':pool}
            suffix='' if active_branch is None else '_branch'+str(active_branch)
            if chi8_branch is not None:suffix+='_chi8_'+str(chi8_branch)
            if fp5:suffix+='_fp5'
            if words:suffix+='_words'
            if norm_records:suffix+='_norm'
            (HERE/(rid+'_full_field_verlinde'+suffix+'.json')).write_text(json.dumps(output,indent=2)+'\n')
            if first:break


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('ring',choices=q.CONFIG);p.add_argument('--first',action='store_true');p.add_argument('--time-limit',type=int,default=60);p.add_argument('--active-branch',type=int);p.add_argument('--chi8-branch',type=int,choices=[0,2]);p.add_argument('--reuse');p.add_argument('--fp5',action='store_true');p.add_argument('--word-file');p.add_argument('--norm-cut',action='append',default=[]);a=p.parse_args();run(a.ring,a.first,a.time_limit,a.active_branch,a.chi8_branch,a.reuse,a.fp5,a.word_file,a.norm_cut)
