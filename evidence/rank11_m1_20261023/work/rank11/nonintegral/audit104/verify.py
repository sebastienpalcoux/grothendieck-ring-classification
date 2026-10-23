"""Independent R104 group-theoretical reconstruction by actual bimodules.

No gt32 or other model-construction code is imported.  Build free bimodules
A tensor (z tensor A), impose scalar stabilizer quotients, take the balanced
relative tensor quotient, and solve the graded bimodule intertwining equations.
All matrices are monomial with sixteenth-root phases, so every linear system
reduces to an exact weighted graph over Z/16.  The one nondegenerate projective
V4 block is retained as its free module, two copies of its unique simple.
"""
from pathlib import Path
from collections import defaultdict, deque
from itertools import product
import gzip, hashlib, json, time

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
MOD = 16


def need(value, message):
    if not value:
        raise ValueError(message)


def components(size, edges, allow_zero=False):
    """Relations e_j = zeta**p e_i; return components, weights, roots.

    A contradictory phase circuit forces its whole component to zero.  This
    option is used for intertwiner coordinates, not for the module bases.
    """
    graph = [[] for _ in range(size)]
    for i, j, phase in edges:
        phase %= MOD
        graph[i].append((j, phase))
        graph[j].append((i, -phase % MOD))
    classes = [-1] * size
    weights = [0] * size
    roots = []
    good = []
    for root in range(size):
        if classes[root] >= 0:
            continue
        c = len(roots)
        roots.append(root)
        good.append(True)
        classes[root] = c
        queue = deque([root])
        while queue:
            i = queue.popleft()
            for j, phase in graph[i]:
                value = (weights[i] + phase) % MOD
                if classes[j] < 0:
                    classes[j] = c
                    weights[j] = value
                    queue.append(j)
                else:
                    need(classes[j] == c, 'graph component identity')
                    if weights[j] != value:
                        good[c] = False
        need(allow_zero or good[c], 'nonzero quotient phase consistency')
    return classes, weights, roots, good


class Audit:
    def __init__(self, record):
        self.r = record
        self.G = record['group_table']
        self.H = record['subgroup']
        self.W = record['omega']
        need(record['modulus'] == 8, 'omega input modulus')
        self.inv = [row.index(0) for row in self.G]
        self.psi = {(a, b): 2 * record['psi'][i][j]
                    for i, a in enumerate(self.H)
                    for j, b in enumerate(self.H)}
        self.checks = defaultdict(int)

    def mul(self, *args):
        v = 0
        for a in args:
            v = self.G[v][a]
        return v

    def w(self, a, b, c):
        return 2 * self.W[a][b][c]

    def foundations(self):
        G, H = self.G, self.H
        n = len(G)
        need(n == 32 and len(H) == 4 and H[0] == 0, 'group and subgroup sizes')
        need(all(sorted(row) == list(range(n)) for row in G), 'group rows')
        need(all(G[0][x] == G[x][0] == x for x in range(n)), 'group unit')
        for a, b, c in product(range(n), repeat=3):
            need(G[G[a][b]][c] == G[a][G[b][c]], 'group associativity')
        need(all(G[a][b] in H for a, b in product(H, repeat=2)), 'subgroup closure')
        need(all(G[a][a] == 0 for a in H), 'Klein four subgroup')
        for a, b in product(range(n), repeat=2):
            need(self.w(0,a,b) == self.w(a,0,b) == self.w(a,b,0) == 0,
                 'normalized associator')
        for a, b, c, d in product(range(n), repeat=4):
            need((self.w(b,c,d) - self.w(G[a][b],c,d)
                  + self.w(a,G[b][c],d) - self.w(a,b,G[c][d])
                  + self.w(a,b,c)) % MOD == 0, 'all cocycle equations')
            self.checks['cocycle_equations'] += 1
        for a, b, c in product(H, repeat=3):
            need((self.psi[a,b] + self.psi[G[a][b],c]
                  - self.w(a,b,c) - self.psi[b,c] - self.psi[a,G[b][c]])
                 % MOD == 0, 'algebra associativity')
        need(all(self.psi[0,a] == self.psi[a,0] == 0 for a in H), 'algebra unit')

    def check_module(self, M):
        G, H = self.G, self.H
        grades, L, R = M['grades'], M['L'], M['R']
        n = len(grades)
        for a in H:
            need(sorted(t for t,p in L[a]) == list(range(n)), 'invertible left action')
            need(sorted(t for t,p in R[a]) == list(range(n)), 'invertible right action')
        for i, x in enumerate(grades):
            need(L[0][i] == R[0][i] == (i,0), 'module units')
            for a in H:
                need(grades[L[a][i][0]] == G[a][x], 'left degree')
                need(grades[R[a][i][0]] == G[x][a], 'right degree')
            for a, b in product(H, repeat=2):
                j,p = L[b][i]; k,q = L[a][j]; t,r = L[G[a][b]][i]
                need(k == t and (p+q-r-self.psi[a,b]+self.w(a,b,x))%MOD == 0,
                     'left associativity')
                j,p = R[a][i]; k,q = R[b][j]; t,r = R[G[a][b]][i]
                need(k == t and (p+q-r-self.psi[a,b]-self.w(x,a,b))%MOD == 0,
                     'right associativity')
                j,p = L[a][i]; k,q = R[b][j]
                j2,p2 = R[b][i]; k2,q2 = L[a][j2]
                need(k == k2 and (p+q-p2-q2-self.w(a,x,b))%MOD == 0,
                     'bimodule compatibility')
                self.checks['bimodule_axiom_triples'] += 1

    def free(self, z):
        H = self.H
        pairs = list(product(H, repeat=2))
        ix = {p:i for i,p in enumerate(pairs)}
        grades = [self.mul(h,z,k) for h,k in pairs]
        L, R = {}, {}
        for a in H:
            L[a] = [(ix[self.mul(a,h),k],
                     (self.psi[a,h]-self.w(a,h,self.mul(z,k)))%MOD)
                    for h,k in pairs]
            R[a] = [(ix[h,self.mul(k,a)],
                     (self.w(h,self.mul(z,k),a)+self.w(z,k,a)+self.psi[k,a])%MOD)
                    for h,k in pairs]
        M = dict(grades=grades,L=L,R=R,pairs=pairs,ix=ix)
        self.check_module(M)
        return M

    def descend(self, M, edges):
        classes, weights, roots, good = components(len(M['grades']), edges)
        out = dict(grades=[M['grades'][i] for i in roots], L={}, R={})
        need(all(M['grades'][i] == out['grades'][classes[i]]
                 for i in range(len(classes))), 'homogeneous quotient relations')
        for side in ['L', 'R']:
            for a in self.H:
                op = M[side][a]
                out[side][a] = [(classes[op[i][0]],(op[i][1]+weights[op[i][0]])%MOD)
                                for i in roots]
                for i,(j,p) in enumerate(op):
                    need(out[side][a][classes[i]] ==
                         (classes[j],(p+weights[j]-weights[i])%MOD),
                         'action descends on every quotient relation')
        self.check_module(out)
        return out

    def simple_copies(self, label):
        z = label['z']
        F = self.free(z)
        stab = [a for a in self.H if self.mul(self.inv[z],a,z) in self.H]
        need(stab == label['stabilizer'], 'actual stabilizer')
        polys = {int(a):{int(e):c for e,c in p.items()}
                 for a,p in label['character_polynomial'].items()}
        if polys[0] == {0:2}:
            need(len(stab) == 4 and all(polys[a] == {} for a in stab if a),
                 'unique nondegenerate projective V4 character')
            # A four-dimensional stabilizer algebra has a unique degree-two
            # irrep exactly when it is noncommutative. Test its operators
            # directly on the base homogeneous fiber.
            T = {}
            for a in stab:
                b = self.mul(self.inv[z],a,z)
                T[a] = self.compose(F['L'][a], F['R'][self.inv[b]])
            base = F['ix'][0,0]
            need(any(self.compose(T[a],T[b])[base] != self.compose(T[b],T[a])[base]
                     for a,b in product(stab,repeat=2)),
                 'noncommutative twisted V4 algebra on its base fiber')
            F['copies'] = 2
            return F
        need(all(len(polys[a]) == 1 and list(polys[a].values()) == [1] for a in stab),
             'one-dimensional stabilizer character')
        mu = {a:(int(label['scalar_projective'][str(a)])+next(iter(polys[a])))%MOD
              for a in stab}
        edges = []
        for a in stab:
            b = self.mul(self.inv[z],a,z)
            generator = F['ix'][a,self.inv[b]]
            # D_a is the bimodule endomorphism determined by sending the
            # free generator to L_a R_(b^-1) of that generator. Extend by
            # D_a(e_(h,k))=L_h R_k D_a(e_(0,0)).
            D = []
            for h,k in F['pairs']:
                j,p = F['R'][k][generator]
                t,q = F['L'][h][j]
                D.append((t,(p+q)%MOD))
            for h in self.H:
                need(self.compose(D,F['L'][h]) == self.compose(F['L'][h],D)
                     and self.compose(D,F['R'][h]) == self.compose(F['R'][h],D),
                     'free bimodule endomorphism')
            for i,(j,p) in enumerate(D):
                edges.append((i,j,mu[a]-p))
        M = self.descend(F,edges)
        need(len(set(M['grades'])) == len(M['grades']), 'scalar homogeneous fibers')
        need(len(M['grades']) == len(self.H)**2//len(stab), 'simple orbit size')
        M['copies'] = 1
        return M

    @staticmethod
    def compose(A,B):
        return [(A[j][0],(p+A[j][1])%MOD) for j,p in B]

    def tensor(self,M,N):
        pairs = list(product(range(len(M['grades'])),range(len(N['grades']))))
        ix = {p:i for i,p in enumerate(pairs)}
        grades = [self.mul(M['grades'][i],N['grades'][j]) for i,j in pairs]
        edges = []
        L, R = {}, {}
        for h in self.H:
            L[h], R[h] = [], []
            for i,j in pairs:
                x,y = M['grades'][i],N['grades'][j]
                ii,p = M['R'][h][i]; jj,q = N['L'][h][j]
                # (R_h m_x) tensor n_y = omega(x,h,y) m_x tensor L_h n_y.
                edges.append((ix[i,jj],ix[ii,j],self.w(x,h,y)+q-p))
                ii,p = M['L'][h][i]
                L[h].append((ix[ii,j],(p-self.w(h,x,y))%MOD))
                jj,q = N['R'][h][j]
                R[h].append((ix[i,jj],(q+self.w(x,y,h))%MOD))
        Q = self.descend(dict(grades=grades,L=L,R=R),edges)
        need(len(Q['grades'])*len(self.H) == len(pairs), 'relative tensor dimension')
        return Q

    def hom(self,M,N):
        pairs = [(i,j) for i,x in enumerate(M['grades'])
                 for j,y in enumerate(N['grades']) if x == y]
        ix = {p:i for i,p in enumerate(pairs)}
        edges = []
        for side in ['L','R']:
            for h in self.H:
                for i,j in pairs:
                    ii,p = M[side][h][i]; jj,q = N[side][h][j]
                    edges.append((ix[i,j],ix[ii,jj],q-p))
        self.checks['graded_intertwiner_systems'] += 1
        return sum(components(len(pairs),edges,allow_zero=True)[3])

    def run(self):
        self.foundations()
        labels = self.r['labels']
        need(len(labels) == 11, 'all eleven labels')
        modules = [self.simple_copies(l) for l in labels]
        seen = set()
        for z in sorted({l['z'] for l in labels}):
            orbit = {self.mul(a,z,b) for a,b in product(self.H,repeat=2)}
            need(not seen.intersection(orbit), 'distinct double cosets')
            seen.update(orbit)
            need(sum(len(m['grades']) for l,m in zip(labels,modules) if l['z']==z)
                 == len(self.H)**2, 'complete decomposition of each free bimodule')
        need(seen == set(range(len(self.G))), 'all double cosets covered')
        for i,j in product(range(11),repeat=2):
            need(self.hom(modules[i],modules[j]) ==
                 (modules[i]['copies']**2 if i==j else 0), 'distinct simple blocks')
        dims = [len(m['grades'])//(len(self.H)*m['copies']) for m in modules]
        need(sum(d*d for d in dims) == len(self.G), 'complete simple inventory')
        T = [[[0]*11 for _ in range(11)] for _ in range(11)]
        for i,j in product(range(11),repeat=2):
            Q = self.tensor(modules[i],modules[j])
            for k in range(11):
                h = self.hom(Q,modules[k])
                copies = modules[i]['copies']*modules[j]['copies']*modules[k]['copies']
                need(h%copies == 0, 'free isotypic multiplicities divide exactly')
                T[i][j][k] = h//copies
        need(T == self.r['model_tensor'], 'independent balanced tensor equals candidate')
        src = list(gzip.open(ROOT/'repositories/fusion-ring-census/results/rank11/tables.txt.gz','rt'))[103]
        R = json.loads(src.replace('{','[').replace('}',']'))
        sha = hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
        need(sha == self.r['tensor_sha256'], 'full source tensor identity')
        p = self.r['basis_map_source_to_model']
        need(sorted(p) == list(range(11)) and p[0] == 0, 'based input bijection')
        need(all(R[i][j][k] == T[p[i]][p[j]][p[k]]
                 for i,j,k in product(range(11),repeat=3)), 'all 1331 source coefficients')
        for i,j,k,l in product(range(11),repeat=4):
            need(sum(T[i][j][a]*T[a][k][l] for a in range(11)) ==
                 sum(T[j][k][a]*T[i][a][l] for a in range(11)), 'fusion associativity')
        return dict(status='PASS',id='R11_1_104',tensor_sha256=sha,
                    method='free bimodules, balanced tensor quotients, graded intertwiner equations',
                    dimensions=dims,model_tensor=T,basis_map_source_to_model=p,
                    action_copies=[m['copies'] for m in modules],checks=dict(self.checks),
                    coefficients=1331,associativity_equations=14641,
                    external_dependencies=[])


if __name__ == '__main__':
    start = time.monotonic()
    r = json.load(open(ROOT/'work/rank11/known_models/jordan_gt_model.json'))
    result = Audit(r).run()
    result['seconds'] = time.monotonic()-start
    (P/'replay.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='model_tensor'},indent=2),flush=True)
