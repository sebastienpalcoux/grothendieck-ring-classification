"""C4 pointed-associator support refinement of the complete R65 CM-STS cone.

All existing stages are imported read-only.  The allowed root trace types are
deduced from equality in the indicator trace triangle inequality, not a bound
on twist orders.  k=1 represents both odd associator classes; k=2 is separate.
"""
from pathlib import Path
import argparse, json, sys, time
from fractions import Fraction as Q

HERE = Path(__file__).resolve().parent
FRONTIER = HERE.parents[1] / 'rank8_frontier_20261021'
sys.path[:0] = [str(FRONTIER/'global_induction'), str(FRONTIER/'quadratic')]
import streaming as st
import column_generation as cg
from atomic_cm_real_sts import AtomicCMRealSTS
from exact import require


class PointedPhaseCone(AtomicCMRealSTS):
    def __init__(self, R, k, fourier=False):
        require(k in (0, 1, 2), 'unsupported associator parity branch')
        super().__init__(R, 4)
        self.k = k
        self.fourier = fourier
        expected = ([[0, 0, 0, 0]] if k == 1 else [[0, 0, 0, -1]] if k == 2
                    else [[1,1,1,1],[-1,1,-1,1],[0,-1,0,1]])
        gtypes = {i for i, tt in enumerate(self.types)
                  if tt in [[(Q(x), Q(0)) for x in vals] for vals in expected]}
        htypes = {i for i, tt in enumerate(self.types)
                  if tt in [[(Q(x), Q(0)) for x in vals]
                            for vals in ([[0,-1,0,1]] if k == 1
                                         else [[1,1,1,1],[-1,1,-1,1]])]}
        require(gtypes and htypes, 'required all-order trace types absent')
        self.allowed_types = []
        for orbit in self.orbits:
            permitted = set(range(self.nt))
            for j in orbit:
                v = self.a['high'][j][0]
                require(sum(bool(v[i-1]) for i in (1,2,7)) <= 1,
                        'distinct pointed objects share a high column')
                if v[0] or v[1]: permitted &= gtypes
                if v[6]: permitted &= htypes
                if fourier and (v[0] or v[1]):
                    # Fourier inversion at the four roots of theta^4=i^k
                    # gives each fibre mass D/4=2+11d. Since its rational
                    # coefficient is sum(m_g^2), each constituent has m_g=1;
                    # positivity gives noninvertible coefficient at most 11.
                    if v[0]+v[1] != 1 or sum(v[i-1] for i in (3,4,5,6)) > 11:
                        permitted.clear()
            self.allowed_types.append(permitted)
        require(all(not any(v[i] for i in (1,2,7)) for _,v,_ in self.low),
                'I(1) and nontrivial pointed induction overlap')
        self.allowed = (set(range(self.offset)) |
                        set(range(self.high_end, self.nvars)) |
                        {self.offset+o*self.nt+t
                         for o, ts in enumerate(self.allowed_types) for t in ts})
        self.meta = {**self.meta, 'pointed_associator_classes': [1,3] if k == 1 else [k],
                     'allowed_columns': len(self.allowed),
                     'pointed_phase_domain_sha256': st.digest(sorted(self.allowed)),
                     'pointed_fourier_integrality': fourier,
                     'generator_trace_type_indices': sorted(gtypes),
                     'involution_trace_type_indices': sorted(htypes)}

    def high_scores(self, y):
        for index, value in super().high_scores(y):
            if index in self.allowed: yield index, value

    def initial_columns(self):
        return self.allowed

    def check_feasible(self, indices, weights, indicators):
        require(all(i in self.allowed for i in indices), 'forbidden pointed twist support')
        return super().check_feasible(indices, weights, indicators)


def run(k, seconds, fourier=False):
    start = time.monotonic()
    source = st.load_ring('R8_3_65')
    C = PointedPhaseCone(source['tensor'], k, fourier)
    out = {'id': source['id'], 'tensor_sha256': source['tensor_sha256'],
           'scope': 'necessary_pseudo_unitary_pointed_phase_relaxation',
           'metadata': C.meta, 'branches': []}
    dest = HERE/f'pointed_phase_k{k}{"_fourier" if fourier else ""}.json'
    def save():
        out['seconds'] = round(time.monotonic()-start,3)
        dest.write_text(json.dumps(st.encode(out), separators=(',',':'))+'\n')
    active = C.initial_columns()
    print('DOMAIN', k, C.nrows, C.nvars, len(active), flush=True)
    choices = [ep for ep in st.old.ht.indicator_choices(source['tensor'])
               if ep[6] == (-1 if k == 1 else 1)]
    for ep in choices:
        attempt = {'indicators': list(ep)}
        out['branches'].append(attempt)
        def progress(iterations):
            attempt['iterations'] = iterations
            print('BRANCH', k, list(ep), iterations[-1]['outcome'], flush=True)
            save()
        certificate, feasible, active, iterations = cg.solve_case(
            C, ep, active, 256, seconds, progress)
        if feasible is not None:
            C.check_feasible(feasible['indices'], feasible['weights'], ep)
            attempt.update(status='exact_feasible', certificate=feasible)
        elif certificate is not None:
            require(C.check_farkas(certificate['y'],ep)==certificate['bTy'], 'recheck')
            attempt.update(status='exact_infeasible', certificate=certificate)
        else: attempt['status'] = 'inconclusive'
        save()
    out['status'] = ('all_branches_exact_infeasible' if all(
        b['status']=='exact_infeasible' for b in out['branches']) else
        'necessary_relaxation_survives' if any(
        b['status']=='exact_feasible' for b in out['branches']) else 'inconclusive')
    save()
    return out


def verify(path):
    data=json.loads(Path(path).read_text()); k=data['metadata']['pointed_associator_classes'][0]
    source=st.load_ring('R8_3_65'); require(source['tensor_sha256']==data['tensor_sha256'],'tensor mismatch')
    C=PointedPhaseCone(source['tensor'],k,data['metadata'].get('pointed_fourier_integrality',False))
    if 'pointed_fourier_integrality' not in data['metadata']:
        data['metadata']['pointed_fourier_integrality']=False
    require(st.encode(C.meta)==data['metadata'],'domain mismatch')
    expected=[list(ep) for ep in st.old.ht.indicator_choices(source['tensor'])
              if ep[6] == (-1 if k == 1 else 1)]
    require([b['indicators'] for b in data['branches']]==expected,
            'pointed second-indicator branch coverage incomplete')
    for branch in data['branches']:
        cert=branch.get('certificate')
        if branch['status']=='exact_feasible':
            C.check_feasible(cert['indices'],cert['weights'],branch['indicators'])
        elif branch['status']=='exact_infeasible':
            require(C.check_farkas(cert['y'],branch['indicators'])==cert['bTy'],'ray mismatch')
            # Independently use explicit sparse columns, not the factored oracle.
            dots=[sum(cert['y'][r]*v for r,v in C.column(i).items())
                  for i in sorted(C.allowed)]
            require(min(dots)>=0,'explicit full matrix Farkas verification failed')
        else: require(branch['status']=='inconclusive','unsupported status')
    if data['status']=='all_branches_exact_infeasible':
        require(all(b['status']=='exact_infeasible' for b in data['branches']),
                'incomplete exclusion promoted')
    print('PASS',path)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--k',type=int,choices=(0,1,2));p.add_argument('--seconds',type=int,default=60);p.add_argument('--verify');p.add_argument('--fourier',action='store_true')
    args=p.parse_args()
    if args.verify:verify(args.verify)
    else: print(run(args.k,args.seconds,args.fourier)['status'],flush=True)
