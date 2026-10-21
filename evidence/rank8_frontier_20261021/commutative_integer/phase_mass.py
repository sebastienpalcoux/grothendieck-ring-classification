"""Exact specialization of a frozen phase cone to fixed restriction counts.

Low source-column indices are fixed with coefficient one. Each high
restriction-duality orbit has a prescribed nonnegative integer count; its
relative-phase variables remain nonnegative rationals.
"""
from pathlib import Path
from fractions import Fraction as Q
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'global_induction'))
import column_generation as cg
st=cg.st;require=cg.require

class MassCone:
    def __init__(self,C,fixed_indices,masses):
        masses=tuple(masses);require(all(isinstance(oi,int)and isinstance(n,int)for oi,n in masses),'high masses must be exact integers')
        self.C=C;self.R=C.R;self.fixed_indices=tuple(fixed_indices);self.masses=masses
        require(len(set(self.fixed_indices))==len(self.fixed_indices)and all(0<=j<C.offset for j in self.fixed_indices),'invalid fixed low columns')
        require(len({i for i,n in self.masses})==len(self.masses)and all(0<=i<len(C.orbits)and n>0 for i,n in self.masses),'invalid fixed high counts')
        self.fixed={}
        for j in self.fixed_indices:
            for i,a in C.column(j).items():self.fixed[i]=self.fixed.get(i,0)+a
        self.active=[];self.mass_for_local={}
        for row,(oi,n)in enumerate(self.masses):
            for ti in range(C.nt):
                self.mass_for_local[len(self.active)]=row;self.active.append(C.offset+oi*C.nt+ti)
        self.active.extend(range(C.high_end,C.nvars));self.nvars=len(self.active);self.nrows=C.nrows+len(self.masses)
        self.metadata={'kind':'fixed_integer_restriction_phase_system','source_phase_metadata':C.meta,
                       'fixed_low_indices':list(self.fixed_indices),'rows':self.nrows,'variables':self.nvars,
                       'nonzero_high_orbits':len(self.masses),'masses':[list(v)for v in self.masses],
                       'active_global_indices_sha256':st.digest(self.active)}
    def column(self,j):
        require(0<=j<self.nvars,'invalid fixed-mass column index');col=dict(self.C.column(self.active[j]))
        if j in self.mass_for_local:col[self.C.nrows+self.mass_for_local[j]]=1
        return col
    def rhs_for(self,ep):return[v-self.fixed.get(i,0)for i,v in enumerate(self.C.rhs_for(ep))]+[n for oi,n in self.masses]
    def check_feasible(self,c,ep):
        indices=c['indices'];weights=list(map(Q,c['weights']));require(len(indices)==len(weights)and all(v>=0 for v in weights),'invalid fixed-mass primal')
        total=[Q(0)]*self.nrows
        for j,x in zip(indices,weights):
            for i,a in self.column(j).items():total[i]+=a*x
        require(total==self.rhs_for(ep),'fixed mass phase equations fail')
        self.C.check_feasible(list(self.fixed_indices)+[self.active[j]for j in indices],['1']*len(self.fixed_indices)+list(map(str,weights)),ep)
        return True
    def check_ray(self,c,ep):
        y=c['covector'];require(len(y)==self.nrows and all(isinstance(a,int)for a in y),'invalid fixed-mass separator')
        key=tuple(y)
        if not hasattr(self,'_checked_rays'):self._checked_rays=set()
        if key not in self._checked_rays:
            require(all(sum(y[i]*a for i,a in self.column(j).items())>=0 for j in range(self.nvars)),'fixed-mass separator fails a column')
            self._checked_rays.add(key)
        require(sum(a*v for a,v in zip(y,self.rhs_for(ep)))==c['rhs_value']<0,'fixed-mass separator sign differs');return True


def discover(D,save=None,seconds=120):
    out={'status':'running','metadata':D.metadata,'attempts':[]};rows=cg.active_rows(D,range(D.nvars))
    if save:save(out)
    for ep in map(list,st.old.ht.indicator_choices(D.R)):
        b=D.rhs_for(ep)
        reused=False
        for previous in out['attempts']:
            if previous.get('outcome')!='exact_selected_pattern_obstruction':continue
            y=previous['certificate']['covector'];value=sum(a*v for a,v in zip(y,b))
            if value<0:
                cert={'covector':y,'rhs_value':value};D.check_ray(cert,ep)
                out['attempts'].append({'indicators':ep,'outcome':'exact_selected_pattern_obstruction','certificate':cert,'reused_ray':True});reused=True;break
        if reused:
            if save:save(out)
            continue
        answer,diag=cg.phase_one(rows,b,D.nvars,seconds);attempt={'indicators':ep,'lp':diag};out['attempts'].append(attempt)
        if save:save(out)
        print('fixed-mass phase',ep,diag,flush=True)
        if not answer.success:out['status']='numerical_search_incomplete';break
        primal=cg.exact_feasible(D,list(range(D.nvars)),b,answer.x[:D.nvars])if answer.fun<1e-7 else None
        if primal is not None:
            D.check_feasible(primal,ep);attempt.update(outcome='exact_phase_feasible',certificate=primal);out['status']='exact_integer_and_phase_compatible';break
        y=cg.reuse_dual(rows,b,D.nvars,answer)
        if y is None:y=st.old.farkas(rows,b,D.nvars,True)
        if y is None:out['status']='exact_reconstruction_incomplete';break
        cert={'covector':y,'rhs_value':sum(a*v for a,v in zip(y,b))};D.check_ray(cert,ep);attempt.update(outcome='exact_selected_pattern_obstruction',certificate=cert)
        if save:save(out)
    else:out['status']='selected_integer_pattern_phase_incompatible'
    if save:save(out)
    return out


def verify(D,out):
    require(out['metadata']==D.metadata,'fixed-mass domain differs')
    require(out['status']in('exact_integer_and_phase_compatible','selected_integer_pattern_phase_incompatible'),'fixed-mass search incomplete')
    choices=list(map(list,st.old.ht.indicator_choices(D.R)))
    for a in out['attempts']:
        require(a['indicators']in choices,'inadmissible indicators')
        if a['outcome']=='exact_phase_feasible':D.check_feasible(a['certificate'],a['indicators'])
        else:D.check_ray(a['certificate'],a['indicators'])
    if out['status']=='selected_integer_pattern_phase_incompatible':require([a['indicators']for a in out['attempts']]==choices,'incomplete indicator coverage')
    else:require(any(a['outcome']=='exact_phase_feasible'for a in out['attempts']),'missing compatible primal')
    return True
