"""Exact order-two pointed-induction/Fourier refinements of R1768 and R1795.

All frozen source and cone files are read-only.  The local low-column
accelerator evaluates precisely the frozen rational-row-reduced equations
using integers; the complete base metadata must match the frozen domain.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse, hashlib, itertools, json, math, sys, time
HERE=Path(__file__).resolve().parent
STAGE=HERE.parents[1]/'rank8_frontier_20261021'
sys.path.insert(0,str(STAGE/'global_induction'))
import streaming as st
import column_generation as cg
from atomic_real_sts import AtomicRealSTS
from exact import require, vector
s=st.old.s


def fast_restriction(ds,beta,K,B):
    """Same finite rectangle/RREF equations as induction.restriction_columns."""
    tail=len(ds)-1;degree=K.mod.degree()
    A=s.Matrix.hstack(*(vector(d,degree) for d in ds[1:]))
    rr,piv=A.row_join(vector(beta-K.one,degree)).rref()
    if tail in piv:return []
    free=[j for j in range(tail) if j not in piv]
    bounds=[min(int(B[0,i]),math.isqrt(int(B[i,i]))) for i in range(1,len(ds))]
    equations=[]
    for row,j in enumerate(piv):
        den=math.lcm(*(int(rr[row,k].q) for k in free+[tail]))
        equations.append((j,den,int(rr[row,tail]*den),[int(rr[row,k]*den) for k in free]))
    out=[]
    for chosen in itertools.product(*(range(bounds[j]+1) for j in free)):
        v=[0]*tail
        for j,a in zip(free,chosen):v[j]=a
        for j,den,rhs,co in equations:
            numerator=rhs-sum(a*b for a,b in zip(co,chosen))
            if numerator%den or not 0<=numerator<=bounds[j]*den:break
            v[j]=numerator//den
        else:out.append((1,)+tuple(v))
    return sorted(out)


def setup(index):
    # Frozen quadratic_data resolves this global helper at call time.
    st.old.ht.restriction_columns=fast_restriction
    source=st.load_ring(f'R8_3_{index}')
    C=AtomicRealSTS(source['tensor'],4)
    old=json.loads((STAGE/'global_induction/complete_results'/f'R8_3_{index}_atomic_real_sts_h4.json').read_text())
    require(C.meta==old['metadata'],'accelerated base domain differs from frozen full cone')
    require(source['tensor_sha256']==old['tensor_sha256'],'frozen source differs')
    R=source['tensor'];n=len(R)
    require(R[1][1]==[int(i==0) for i in range(n)],'pointed generator is not order two')
    require(all(R[1][i][i]==0 and sum(R[1][i])==1 for i in range(n)),
            'pointed generator does not act freely')
    ds=C.a['dimensions']
    for i in range(n):
        for j in range(n):
            require(tuple(C.a['mul'](ds[i],ds[j]))==tuple(sum(R[i][j][a]*ds[a][k]
                    for a in range(n)) for k in range(2)),'FP dimension character check')
    print('BASE',index,C.nrows,C.nvars,flush=True)
    return source,C,old


def fibre_filter(C):
    """Complete dimension/pointed-Gram packing relaxation for both fibres.

    A constituent with multiplicity m contributes (m^2,m*z_0,m*z_1).
    Unbounded nonnegative integer packings are enumerated in the finite
    box q<=Bgg, mass<=D/2.  Both fibres must fit and their q values sum Bgg.
    """
    g=1;budget=int(C.a['B'][g,g]);target=tuple(Q(x)/2 for x in C.D)
    require(C.a['B'][0,g]==0,'unit and g inductions overlap')
    require(all(Q(x)>=0 for d in C.a['dimensions'] for x in d),'dimension basis not coordinatewise nonnegative')
    den=math.lcm(*(x.denominator for x in target),
                 *(Q(x).denominator for v,z in C.a['high'] for x in z))
    target=tuple(int(x*den) for x in target)
    items={j:(int(v[0])**2,*(int(Q(x)*den)*int(v[0]) for x in z))
           for j,(v,z) in enumerate(C.a['high']) if v[0]}
    accepted=set(items);rounds=[]
    while True:
        types=sorted({items[j] for j in accepted})
        reached=[set() for _ in range(budget+1)];reached[0].add((0,0))
        for q in range(1,budget+1):
            for c,a,b in types:
                if c>q:continue
                for x,y in reached[q-c]:
                    if x+a<=target[0] and y+b<=target[1]:reached[q].add((x+a,y+b))
        qs=[q for q in range(budget+1) if target in reached[q]]
        good=[q for q in qs if budget-q in qs]
        keep={j for j in accepted if any(q>=items[j][0] and
              (target[0]-items[j][1],target[1]-items[j][2]) in reached[q-items[j][0]]
              for q in good)}
        rounds.append({'input_columns':len(accepted),'mass_types':len(types),
                       'fibre_Gram_values':qs,'complementary_Gram_values':good,
                       'reachable_counts':[len(x) for x in reached],
                       'rejected_high_indices':sorted(accepted-keep)})
        if keep==accepted:break
        accepted=keep
    report={'pointed_index':g,'total_pointed_Gram':budget,
            'dimension_coordinate_scale':den,'fibre_mass':target,
            'original_pointed_high_columns':len(items),
            'retained_pointed_high_columns':len(accepted),'rounds':rounds,
            'retained_high_indices':sorted(accepted),'packing_scope':'necessary integer relaxation; nonpointed Gram cross constraints omitted'}
    return accepted,report


class PointedCone(AtomicRealSTS):
    def __init__(self,base,epsilon):
        self.__dict__.update(base.__dict__)
        require(epsilon in (-1,1),'invalid pointed second indicator')
        self.epsilon=epsilon
        accepted,report=fibre_filter(self)
        expected=([[0,-1,0,1]] if epsilon==-1 else [[1,1,1,1],[-1,1,-1,1]])
        pt={i for i,t in enumerate(self.types) if t in
            [[(Q(x),Q(0)) for x in values] for values in expected]}
        require(pt,'pointed phase trace absent')
        require(all(v[1]==0 for _,v,_ in self.low),'low restriction contains g')
        self.allowed=set(range(self.offset))|set(range(self.high_end,self.nvars))
        for orbit,members in enumerate(self.orbits):
            ts=set(range(self.nt))
            for j in members:
                if self.a['high'][j][0][0]:
                    ts &= pt
                    if j not in accepted:ts.clear()
            self.allowed.update(self.offset+orbit*self.nt+t for t in ts)
        self.meta={**base.meta,'pointed_second_indicator':epsilon,
                   'allowed_columns':len(self.allowed),'allowed_domain_sha256':st.digest(sorted(self.allowed)),
                   'Fourier_fibre_filter':report}

    def high_scores(self,y):
        for index,value in super().high_scores(y):
            if index in self.allowed:yield index,value

    def check_feasible(self,indices,weights,ep):
        require(all(i in self.allowed for i in indices),'forbidden fibre/phase column')
        return super().check_feasible(indices,weights,ep)

    def initial_columns(self):
        zero=next(i for i,t in enumerate(self.types) if not any(x for v in t for x in v))
        selected=set(range(self.offset))|set(range(self.high_end,self.nvars))
        for orbit in range(len(self.orbits)):
            candidates=[self.offset+orbit*self.nt+t for t in range(self.nt)
                        if self.offset+orbit*self.nt+t in self.allowed]
            z=self.offset+orbit*self.nt+zero
            if candidates:selected.update([z] if z in candidates else candidates)
        return selected


def run(index,seconds):
    start=time.monotonic();source,base,old=setup(index)
    out={'id':source['id'],'tensor_sha256':source['tensor_sha256'],
         'scope':'necessary_pseudo_unitary_C2_Fourier_fibre_relaxation',
         'base_metadata':base.meta,'parities':[]}
    path=HERE/f'R8_3_{index}.json'
    def save():out['seconds']=round(time.monotonic()-start,3);path.write_text(json.dumps(st.encode(out),separators=(',',':'))+'\n')
    for epsilon in (-1,1):
        C=PointedCone(base,epsilon);record={'metadata':C.meta,'branches':[]};out['parities'].append(record)
        f=C.meta['Fourier_fibre_filter']
        print('FILTER',index,epsilon,'columns',len(C.allowed),'pointed',
              f['original_pointed_high_columns'],'->',f['retained_pointed_high_columns'],flush=True);save()
        active=C.initial_columns()
        old_rays=[b['y'] for b in old.get('partial_pseudo_certificate',{}).get('cases',[])]
        # Prior exact rays remain valid on subsets.  Try the old surviving
        # branch first to avoid reproducing already settled indicator signs.
        choices=[list(ep) for ep in st.old.ht.indicator_choices(C.R) if ep[0]==epsilon]
        witness_ep=old['certificate']['indicators']
        if witness_ep in choices:choices.remove(witness_ep);choices.insert(0,witness_ep)
        for ep in choices:
            attempt={'indicators':ep};record['branches'].append(attempt)
            prior=next((y for y in old_rays if sum(a*b for a,b in zip(y,C.rhs_for(ep)))<0),None)
            if prior is not None:
                value=C.check_farkas(prior,ep);attempt.update(status='exact_infeasible',certificate={'y':prior,'bTy':value},reused_frozen_ray=True);save();continue
            def progress(iterations):attempt['iterations']=iterations;save();print('ROUND',index,ep,iterations[-1]['outcome'],flush=True)
            cert,feasible,active,iterations=cg.solve_case(C,ep,active,512,seconds,progress)
            if cert:
                attempt.update(status='exact_infeasible',certificate=cert);old_rays.append(cert['y'])
            elif feasible:
                attempt.update(status='exact_feasible',certificate=feasible);record['status']='necessary_relaxation_survives';save();break
            else:attempt['status']='inconclusive';record['status']='inconclusive';save();break
            save()
        else:record['status']='all_indicator_branches_exact_infeasible'
        save()
    out['status']='all_parities_exact_infeasible' if all(r['status']=='all_indicator_branches_exact_infeasible' for r in out['parities']) else 'no_complete_exclusion'
    save();return out


def verify_result(index):
    source,base,old=setup(index)
    out=json.loads((HERE/f'R8_3_{index}.json').read_text())
    require(source['tensor_sha256']==out['tensor_sha256'],'source mismatch')
    require(base.meta==out['base_metadata'],'base metadata mismatch')
    require([r['metadata']['pointed_second_indicator'] for r in out['parities']]==[-1,1],
            'missing pointed parity')
    eligible=list(map(list,st.old.ht.indicator_choices(source['tensor'])))
    for record in out['parities']:
        epsilon=record['metadata']['pointed_second_indicator'];C=PointedCone(base,epsilon)
        require(st.encode(C.meta)==record['metadata'],'new fibre domain mismatch')
        seen=[];checked_rays=set()
        for branch in record['branches']:
            ep=branch['indicators'];require(ep in eligible and ep[0]==epsilon and ep not in seen,
                                         'ineligible/repeated second-indicator branch');seen.append(ep)
            cert=branch.get('certificate')
            if branch['status']=='exact_feasible':
                C.check_feasible(cert['indices'],cert['weights'],ep)
            elif branch['status']=='exact_infeasible':
                key=tuple(cert['y'])
                if key not in checked_rays:
                    require(C.oracle(cert['y'],1)['negative_columns']==0,'separator column sign failed')
                    checked_rays.add(key)
                value=sum(a*b for a,b in zip(cert['y'],C.rhs_for(ep)))
                require(value==cert['bTy'] and value<0,'separator right-hand-side replay differs')
            else:require(branch['status']=='inconclusive','unsupported branch status')
        status=record['status']
        if status=='necessary_relaxation_survives':
            require(any(b['status']=='exact_feasible' for b in record['branches']),'missing feasible witness')
        elif status=='all_indicator_branches_exact_infeasible':
            require(sorted(seen)==sorted(ep for ep in eligible if ep[0]==epsilon) and
                    all(b['status']=='exact_infeasible' for b in record['branches']),
                    'incomplete parity exclusion')
        else:require(status=='inconclusive','unsupported parity status')
    expected='all_parities_exact_infeasible' if all(r['status']=='all_indicator_branches_exact_infeasible'
                for r in out['parities']) else 'no_complete_exclusion'
    require(out['status']==expected,'terminal status promoted')
    print('PASS exact C2 Fourier replay',source['id'],out['status'],flush=True)
    return {'id':source['id'],'tensor_sha256':source['tensor_sha256'],
            'status':out['status'],'parities':[{
                'pointed_second_indicator':r['metadata']['pointed_second_indicator'],
                'status':r['status'],'allowed_columns':r['metadata']['allowed_columns'],
                'verified_indicator_branches':len(r['branches']),
                'admissible_indicator_branches':sum(ep[0]==r['metadata']['pointed_second_indicator']
                                                   for ep in eligible)} for r in out['parities']]}


def write_receipt(index,report):
    root=HERE.parents[2]
    paths=[HERE/'c2_fibres.py',HERE/f'R8_3_{index}.json']
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name:
            path=Path(name).resolve()
            if root in path.parents and path.suffix=='.py':paths.append(path)
    report['sources']={str(path.relative_to(root)):hashlib.sha256(path.read_bytes()).hexdigest()
                       for path in sorted(set(paths))}
    (HERE/f'verification_R8_3_{index}.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--ring',type=int,choices=(1768,1795),required=True);p.add_argument('--seconds',type=int,default=60);p.add_argument('--verify',action='store_true');p.add_argument('--write-receipt',action='store_true');a=p.parse_args()
    if a.verify:
        report=verify_result(a.ring)
        if a.write_receipt:write_receipt(a.ring,report)
    else:print(run(a.ring,a.seconds)['status'],flush=True)
