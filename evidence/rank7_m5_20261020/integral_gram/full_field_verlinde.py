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


def fifth_primary_refinement(columns,rhs,labels,orbits,records,rid,transport):
    """Split genuine-zero rows by fifth-primary order and impose c,4c.

    Visible phases have fifth-primary part one or five. True-zero units
    four split into those classes, with unit eight in the second class
    on actual transport-fixed/dual rows. Units five or ten cover
    fifth-primary orders >=25. This is a necessary
    relaxation, not an assertion that every split is realizable.
    """
    weights=(2,1,1,2,-2,-2,0) if rid=='R7_5_3895' else (2,1,1,-2,-2,2,0)
    newcols=[];newlabels=[]
    for col,label in zip(columns,labels):
        orders=records[label['phase']]['orders']
        if orders:parts=[int(orders[0]%5==0)]
        elif label['multiplicity_unit'] in (4,8,16):parts=[0,1]
        else:
            q.require(label['multiplicity_unit'] in (5,10),'zero-phase hidden fifth-power semigroup unit')
            parts=[2]
        weight=label['multiplicity_unit']*sum(sum(a*b for a,b in zip(weights,(0,)+tuple(v)))**2 for v,g,z in orbits[label['orbit']])
        representative=(0,)+tuple(orbits[label['orbit']][0][0]);tv=transport(representative)
        if all(x<=0 for x in tv):tv=tuple(-x for x in tv)
        dv=tuple(representative[i] for i in transport.dual)
        fixes=tv==representative or tv==dv
        for part in parts:
            scale=2 if not orders and part==1 and fixes else 1
            mass0=scale*weight if part==0 else 0
            mass1=scale*weight if part==1 else 0
            newcols.append([scale*x for x in col]+[mass1-4*mass0,mass0])
            newlabels.append({**label,'multiplicity_unit':scale*label['multiplicity_unit'],'fifth_primary':part})
    newcols += [list(col)+[0,0] for col in columns[len(labels):]]
    newrhs=list(rhs)+[32,24]
    slack=[0]*len(newrhs);slack[-1]=1;newcols.append(slack)
    return newcols,newrhs,newlabels


def all_word_congruences(columns,rhs,labels,congruences):
    """Use nonnegative residues, so the modular quotient is nonnegative."""
    for rec in congruences:
        modulus=rec['modulus'];constant=rec['constant']%modulus
        q.require(type(modulus)==int and modulus>0,'positive integer congruence modulus')
        coeff=[a%modulus for a in rec['coefficients']]
        for j,col in enumerate(columns):
            col.append(labels[j]['multiplicity_unit']*coeff[labels[j]['orbit']] if j<len(labels) else 0)
        rhs.append(-constant)
        slack=[0]*len(rhs);slack[-1]=-modulus;columns.append(slack)
    return columns,rhs,labels


def fourth_cyclic_constraints(columns,rhs,labels,orbits,records,low,ds,D,N,sign):
    """Impose the complete C4 character on Hom(1,X_i^4), for i=1,...,6."""
    objects=[]
    for i in range(1,7):
        power=[int(k==0) for k in range(7)]
        for _ in range(4):power=[sum(power[j]*N[j][i][k] for j in range(7)) for k in range(7)]
        m4=power[0];t2=sum(N[i][i][k]*sign[k] for k in range(7))
        q.require((m4+t2)%2==0 and m4>=abs(t2),'valid order-two restriction of cyclic character')
        A=(m4+t2)//2;B=(m4-t2)//2;start=len(rhs)
        known=tuple(sum(v[i]*sum(v[k]*ds[k][j] for k in range(7)) for v in [(1,0,0,0,0,0,0)]+low) for j in range(2))
        target=[-A*D[0]-known[0],-A*D[1]-known[1],0,0,-B*D[0],-B*D[1],0,0,A,B]
        for j,col in enumerate(columns):
            coeff=[F(0)]*10
            if j<len(labels):
                label=labels[j];mu=[F(x,8) for x in records[label['phase']]['fourth_scaled8']]
                for v,g,z in orbits[label['orbit']]:
                    for block in range(0,8,2):
                        product=q.base.mul(z,mu[block:block+2],5)
                        coeff[block]+=label['multiplicity_unit']*v[i-1]*product[0]
                        coeff[block+1]+=label['multiplicity_unit']*v[i-1]*product[1]
            col.extend(coeff)
        rhs.extend(target)
        indices=[]
        for kind in range(4):
            col=[F(0)]*len(rhs)
            if kind==0:col[start]=-2*D[0];col[start+1]=-2*D[1]
            if kind==2:col[start+4]=-2*D[0];col[start+5]=-2*D[1]
            col[start+8+kind//2]=1
            indices.append(len(columns));columns.append(col)
        objects.append({'source_object':i,'hom_four':m4,'nu2_square':t2,'A':A,'B':B,'variables':indices})
    return columns,rhs,labels,objects


def run(rid,first=False,time_limit=60,active_branch=None,chi8_branch=None,reuse=None,fp5=False,word_file=None,norm_files=(),all_words=None,fourth=False,cases=None,export_only=False):
    import numpy as np
    from scipy.optimize import milp,Bounds,LinearConstraint
    from scipy.sparse import csc_matrix
    N=next(r['tensor'] for r in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==rid)
    d,D,B,zs,T,signs=q.source_data(N,rid);table=m.ExactQuadraticCharacterTable(N,d,5)
    if fourth:
        from full_source_phases import phase_records_fourth
        records=phase_records_fourth()
    else:records=phase_records(field='F8')
    pool=[];results=[]
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
        allword_data=json.loads(open(all_words).read()) if all_words else None
        if allword_data:
            q.require(allword_data['id']==rid and allword_data['source_sha256']==q.tensor_hash(N),'all-word source identity')
            q.require(allword_data['domain_sha256']==V['domain_sha256'],'all-word complete domain identity')
        if word_file:
            W=json.loads(open(word_file).read())
            q.require(W['domain_sha256']==V['domain_sha256'],'word coefficient domain matches exactly')
            q.require(W['source_sha256']==q.tensor_hash(N),'word coefficient source matches exactly')
            words=W['words'];known+=list(map(F,W['known']))
            vcols=[a+list(map(F,b)) for a,b in zip(vcols,W['orbits'])]
        print(json.dumps({'event':'domain','id':rid,'low':dom['low_index'],'orbits':len(orbits),'phases':len(records)}),flush=True)
        for ci,case in enumerate(dom['cases']):
            if -1 in case['sign']:continue
            if cases is not None and ci not in cases:continue
            columns,rhs,labels=f.build_system(table,low,case['label'],orbits,dom['bound'],D,zs,case['sign'],T,records,rid,chi8_branch=chi8_branch)
            if fp5:columns,rhs,labels=fifth_primary_refinement(columns,rhs,labels,orbits,records,rid,T)
            norm_records=[json.loads(open(path).read()) for path in norm_files]
            cuts=[]
            if norm_records:
                import integer_norm_cuts as nc
                cutdom={'id':rid,'low':low,'orbits':orbits}
                cuts=[nc.coefficient_cut(table,cutdom,case['label'],N,T.dual,V,record) for record in norm_records]
                columns,rhs,labels=nc.append_cuts(columns,rhs,labels,cuts)
            if allword_data:columns,rhs,labels=all_word_congruences(columns,rhs,labels,allword_data['constraints'])
            cyclic=[]
            if fourth:columns,rhs,labels,cyclic=fourth_cyclic_constraints(columns,rhs,labels,orbits,records,low,d,D,N,case['sign'])
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
                cyclic=[{**obj,'variables':[j-len(fixed) for j in obj['variables']]} for obj in cyclic]
            if fourth:
                name=rid+'_c4_system_'+str(dom['low_index'])+'_'+str(ci)
                if chi8_branch is not None:name+='_chi8_'+str(chi8_branch)
                if active_branch is not None:name+='_branch'+str(active_branch)
                system={'id':rid,'source_sha256':q.tensor_hash(N),'domain_sha256':V['domain_sha256'],'low_index':dom['low_index'],'case':ci,'label':case['label'],'indicator_sign':case['sign'],'chi8_branch':chi8_branch,'columns':cols,'rhs':rhs,'phase_labels':labels,'fixed_support':fixed_support,'auxiliary_count':extra0,'low_verlinde_count':len(V['triples']),'words':words,'cyclic_characters':cyclic,'phase_records':records,'low':low,'orbits':orbits,'norm_cut_records':norm_records,'norm_cut_coefficients':cuts,'all_word_congruences':allword_data,'fifth_primary_refinement':fp5}
                (HERE/(name+'.json')).write_text(json.dumps(system)+'\n')
                if export_only:
                    print(json.dumps({'event':'exact_system_export','file':name+'.json','columns':len(cols),'equations':len(rhs)}),flush=True)
                    if first:break
                    continue
            sep=q.separate(cols,rhs,pool)
            result={'index':dom['low_index'],'case':ci,'phase_variables':len(labels),'exact_separator':sep}
            if reuse and sep is None:
                old_result=next((r for r in json.loads(open(reuse).read())['results'] if r['case']==ci and r.get('exact_feasible')),None)
                if old_result is not None:
                    physical=lambda r:(r['orbit'],r['phase'],r.get('fifth_primary'))
                    saved={}
                    for item in old_result['support']:
                        k=physical(item);saved[k]=saved.get(k,0)+item['count']*item['multiplicity_unit']
                    for item in fixed_support:
                        k=physical(item);saved[k]=saved.get(k,0)-item['count']*item['multiplicity_unit']
                    index={physical(r):j for j,r in enumerate(labels)}
                    if all(n==0 or k in index for k,n in saved.items()) and all(n>=0 for n in saved.values()) and all(saved.get(physical(r),0)%r['multiplicity_unit']==0 for r in labels):
                        phase_counts=[saved.get(physical(r),0)//r['multiplicity_unit'] for r in labels]
                        hom=old_result['verlinde_coefficients']+old_result.get('word_multiplicities',[])
                        if len(hom)==len(V['triples'])+len(words):
                            counts=phase_counts+[0]*extra0+hom
                            remainder=[F(b)-sum(c[i]*x for c,x in zip(cols,counts)) for i,b in enumerate(rhs)]
                            valid=True
                            for j in range(len(labels),len(labels)+extra0):
                                nz=[i for i,a in enumerate(cols[j]) if a]
                                if len(nz)!=1:valid=False;break
                                i=nz[0];n=remainder[i]/cols[j][i]
                                if n.denominator!=1 or n<0:valid=False;break
                                counts[j]=int(n);remainder[i]=0
                            if valid and not any(remainder):
                                result.update({'status':0,'exact_feasible':True,'support':fixed_support+[{**lab,'count':n} for lab,n in zip(labels,phase_counts) if n],'verlinde_coefficients':old_result['verlinde_coefficients'],'word_multiplicities':old_result.get('word_multiplicities',[]),'reused_witness_exactly_checked':True})
            if sep is None and not result.get('exact_feasible'):
                ub=[min([rhs[i]//col[i] for i in range(21) if col[i]>0] or [np.inf]) for col in cols]
                start=time.monotonic()
                res=milp(np.r_[np.ones(len(labels)),np.zeros(len(cols)-len(labels))],integrality=np.ones(len(cols)),bounds=Bounds(np.zeros(len(cols)),ub),constraints=LinearConstraint(csc_matrix(np.array(cols,dtype=float).T),rhs,rhs),options={'time_limit':time_limit})
                result.update({'status':int(res.status),'seconds':time.monotonic()-start})
                if res.x is not None:
                    counts=[round(float(x)) for x in res.x]
                    result['exact_feasible']=all(x>=0 for x in counts) and all(sum(c[i]*x for c,x in zip(cols,counts))==b for i,b in enumerate(rhs))
                    result['support']=fixed_support+[{**labels[i],'count':n} for i,n in enumerate(counts[:len(labels)]) if n]
                    result['auxiliary_counts']=counts[len(labels):len(labels)+extra0]
                    result['verlinde_coefficients']=counts[len(labels)+extra0:len(labels)+extra0+len(V['triples'])]
                    result['word_multiplicities']=counts[len(labels)+extra0+len(V['triples']):]
            print(json.dumps(result),flush=True);results.append(result)
            output={'id':rid,'phase_records':records,'source_sha256':q.tensor_hash(N),'low':low,'orbits':orbits,'words':words,'chi8_branch':chi8_branch,'fifth_primary_refinement':fp5,'fourth_cyclic_character':fourth,'cyclic_characters':cyclic,'fixed_row_zero_units':([8,16,10] if fourth else [4,8,10]) if fp5 else None,'norm_cut_records':norm_records,'norm_cut_coefficients':cuts,'all_word_congruences':allword_data,'results':results,'separators':pool}
            suffix='' if active_branch is None else '_branch'+str(active_branch)
            if chi8_branch is not None:suffix+='_chi8_'+str(chi8_branch)
            if fp5:suffix+='_fp5'
            if words:suffix+='_words'
            if norm_records:suffix+='_norm'
            if allword_data:suffix+='_allwords'
            if fourth:suffix+='_c4'
            (HERE/(rid+'_full_field_verlinde'+suffix+'.json')).write_text(json.dumps(output,indent=2)+'\n')
            if first:break


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('ring',choices=q.CONFIG);p.add_argument('--first',action='store_true');p.add_argument('--time-limit',type=int,default=60);p.add_argument('--active-branch',type=int);p.add_argument('--chi8-branch',type=int,choices=[0,2]);p.add_argument('--reuse');p.add_argument('--fp5',action='store_true');p.add_argument('--word-file');p.add_argument('--norm-cut',action='append',default=[]);p.add_argument('--all-words');p.add_argument('--fourth',action='store_true');p.add_argument('--cases');p.add_argument('--export-only',action='store_true');a=p.parse_args();run(a.ring,a.first,a.time_limit,a.active_branch,a.chi8_branch,a.reuse,a.fp5,a.word_file,a.norm_cut,a.all_words,a.fourth,None if a.cases is None else set(map(int,a.cases.split(','))),a.export_only)
