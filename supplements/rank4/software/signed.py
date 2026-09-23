"""Exhaustive signed sphericalizations, with an exact Python reference search."""
import hashlib,itertools,subprocess,tempfile,os
from pathlib import Path
from exact import *
from rings import *

MASKS=(1,2,4,1,7,1,2,4,2,4)
SD_PERM_MAPS=tuple(sd_tuple(permute(sd_tensor(tuple(range(10))),p)) for p in PERMS)

def adjoint_signature(p):
    # Gauge signs cannot change an even residue modulo four. On odd
    # coefficients only parity is retained; the exact linked signs are
    # checked after orbit expansion. The mixed coefficient e uses parity.
    return tuple(v%2 if k==4 else (1 if v%2 else v%4) for k,v in enumerate(p))

def orbit_adjoint_signature(p):
    return min(adjoint_signature(tuple(p[k] for k in mapping)) for mapping in SD_PERM_MAPS)
def sd_equations(p):
    a,b,c,d,e,f,g,h,i,j=p
    return (a*d-b*b+b*g+c*h-d*d-e*e+1,a*e-b*c+b*h+c*i-d*e-e*f,
        b*e-c*d+d*h-e*g+e*i-f*h,a*f+b*i-c*c+c*j-e*e-f*f+1,
        b*f-c*e+d*i-e*h+e*j-f*i,d*f-e*e+g*i-h*h+h*j-i*i+1)
def ns_equations(p):
    a,b,c,d,e,f=p
    return (a*c-b*b+2*b*e-c*c-d*d+1,a*d-b*b+b*e+b*f-2*c*d,
            b*(c-d)+d*(e-f),-c*c+d*d-e*e+f*f-1)
def gauges(N):
    span={0};positive=[]
    for k in (1,2,0,4,3,5,6,7,8,9):
        if N[k]%2 and MASKS[k] not in span:
            positive.append(k);span|={v^MASKS[k] for v in list(span)}
    return positive

def gauge_images(N):
    return {tuple(v*(-1 if (mask&MASKS[k]).bit_count()%2 else 1) for k,v in enumerate(N)) for mask in range(8)}

def sd_parity_failure(N,p):
    """The three adjoint rows for each self-dual nonunit simple."""
    return any(not any(all((N[k]-nu*p[k])%4==0 for k in row) for nu in (-1,1))
               for row in ((0,3,5),(1,6,8),(2,7,9)))

def parity_domain_boxes(N,positive):
    """Disjoint nonempty residue boxes whose union satisfies adjoint parity."""
    boxes=set()
    for signs in itertools.product((-1,1),repeat=3):
        residues=[None]*10
        for nu,row in zip(signs,((0,3,5),(1,6,8),(2,7,9))):
            for k in row:residues[k]=(nu*N[k])%4
        domains=tuple(tuple(v for v in range(-n,n+1,2)
                            if (k not in positive or v>0) and (residues[k] is None or v%4==residues[k]))
                      for k,n in enumerate(N))
        if all(domains):boxes.add(domains)
    return sorted(boxes)

def python_sd(N,positive):
    """Eliminate h,g,j when b!=0; handle every zero-denominator case."""
    D=[tuple(v for v in range(-n,n+1,2) if k not in positive or v>0) for k,n in enumerate(N)]
    sets=list(map(set,D));A,B,C,DD,E,F,G,H,I,J=D;out=[]
    def emit(p):
        if not any(sd_equations(p)):out.append(p)
    for a,b,c,d,e,f in itertools.product(A,B,C,DD,E,F):
        if b:
            for i in I:
                hh=e*(d+f-a)+b*c-c*i
                if hh%b:continue
                h=hh//b
                if h not in sets[7]:continue
                gg=b*b+d*d+e*e-a*d-c*h-1
                if gg%b:continue
                g=gg//b
                if g not in sets[6]:continue
                jj=c*c+e*e+f*f-a*f-b*i-1
                if c:
                    if jj%c:continue
                    j=jj//c
                    if j in sets[9]:emit((a,b,c,d,e,f,g,h,i,j))
                elif jj==0:
                    for j in J:emit((a,b,c,d,e,f,g,h,i,j))
        elif c:
            hh=d*d+e*e-a*d-1;ii=e*(d+f-a);jj=c*c+e*e+f*f-a*f-1
            if hh%c or ii%c or jj%c:continue
            h,i,j=hh//c,ii//c,jj//c
            if h not in sets[7] or i not in sets[8] or j not in sets[9]:continue
            gg=h*(d-f)+e*i-c*d
            if e:
                if gg%e:continue
                g=gg//e
                if g in sets[6]:emit((a,b,c,d,e,f,g,h,i,j))
            elif gg==0:
                for g in G:emit((a,b,c,d,e,f,g,h,i,j))
        else:
            if a*d-d*d-e*e+1 or e*(a-d-f) or a*f-e*e-f*f+1:continue
            for h,i in itertools.product(H,I):
                gg=h*(d-f)+e*i;jj=e*h+i*(f-d)
                if e:
                    if gg%e or jj%e:continue
                    g,j=gg//e,jj//e
                    if g in sets[6] and j in sets[9]:emit((a,b,c,d,e,f,g,h,i,j))
                elif gg==0 and jj==0:
                    for g,j in itertools.product(G,J):emit((a,b,c,d,e,f,g,h,i,j))
    return sorted(out)

class Search:
    def __init__(self,engine='cpp',use_global=True):
        require(engine in ('cpp','python'),'unknown search engine')
        self.engine=engine;self.tmp=tempfile.TemporaryDirectory();self.exe=Path(self.tmp.name)/'enum'
        self.source_hashes={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                            for name in ('enumerate_signed.cpp','enumerate_signed_diophantine.cpp','enumerate_nonselfdual.cpp')}
        self.global_catalog=None;self._global_prime_indices={};self._global_orbit_images={};self._global_signature_indices=None
        if use_global and (Path(__file__).resolve().parents[1]/'data/signed_universal_128_manifest.json').exists():
            from global_signed import load_catalog
            rows,manifest=load_catalog()
            self.global_catalog=(tuple((tuple(p),int(det)) for p,det in rows),manifest)
        if engine=='cpp':
            source=Path(__file__).with_name('enumerate_signed.cpp')
            subprocess.run(['g++','-O2','-std=c++17',str(source),'-o',str(self.exe)],check=True)
            self.ns_exe=Path(self.tmp.name)/'enum_ns'
            subprocess.run(['g++','-O2','-std=c++17',str(source.with_name('enumerate_nonselfdual.cpp')),'-o',str(self.ns_exe)],check=True)
            self.diophantine_exe=Path(self.tmp.name)/'enum_diophantine'
            subprocess.run(['g++','-O2','-std=c++17',str(source.with_name('enumerate_signed_diophantine.cpp')),'-o',str(self.diophantine_exe)],check=True)
    def selfdual(self,N):
        pos=gauges(N)
        if self.engine=='python':out=python_sd(N,pos)
        else:
            # C++ loop variables are bounded by N. All products fit safely
            # below signed 64-bit limits with this deliberately low guard.
            # The linear i-elimination uses intermediates of degree at most four.
            require(max(N)<=1000,'C++ guard: use the Python engine')
            line=' '.join(map(str,[0]+list(N)+[int(k in pos) for k in range(10)]))+'\n'
            text=subprocess.check_output([str(self.exe)],input=line,text=True)
            out=sorted(tuple(map(int,line.split()[2:])) for line in text.splitlines() if line.startswith('T '))
        require(len(out)==len(set(out)),'duplicate enumeration result')
        for p in out:
            require(all(abs(v)<=N[k] and (v-N[k])%2==0 for k,v in enumerate(p)),'signed bound failure')
            require(all(p[k]>0 for k in pos) and not any(sd_equations(p)),'signed equation/gauge failure')
        return out

    def filtered_selfdual(self,N,primes,method='parity_domains_diophantine_v2'):
        """Exhaustively replay two necessary tests, retaining only survivors.

        The rejected tuples are never materialized by the C++ backend.  This
        is certificate compression only: both generation and verification
        exhaust the same signed box and check a rejection for every tuple.
        The Python backend supplies an independent reference partition.
        """
        primes=list(primes)
        require(method in ('exhaustive_determinant_parity_v1','parity_domains_diophantine_v2'),'unknown signed replay method')
        restricted=method=='parity_domains_diophantine_v2'
        require(primes==sorted(set(primes)) and all(s.isprime(q) for q in primes),'invalid filter primes')
        pos=gauges(N)
        boxes=parity_domain_boxes(N,pos) if restricted else None
        if self.engine=='python':
            tables=python_sd(N,pos);out=[];counts=[0]*len(primes);parity=0
            if restricted:tables=[p for p in tables if not sd_parity_failure(N,p)]
            for p in tables:
                det=casimir_determinant(sd_tensor(p))
                bad=next((k for k,q in enumerate(primes) if det%q),None)
                if bad is not None:counts[bad]+=1
                elif sd_parity_failure(N,p):parity+=1
                else:out.append(p)
            total=len(tables);det_rejected=sum(counts)
        else:
            require(max(N)<=1000 and all(q<2**63 for q in primes),'C++ exact-integer guard')
            mode=2 if restricted else 1
            line=' '.join(map(str,[0]+list(N)+[int(k in pos) for k in range(10)]+[mode,len(primes)]+primes))+'\n'
            result=subprocess.check_output([str(self.diophantine_exe if restricted else self.exe)],input=line,text=True)
            out=sorted(tuple(map(int,line.split()[2:])) for line in result.splitlines() if line.startswith('T '))
            summaries=[line.split() for line in result.splitlines() if line.startswith('C ')]
            require(len(summaries)==1,'missing signed search summary')
            values=list(map(int,summaries[0][4:]));total,det_rejected,parity,retained,*counts=values
            require(retained==len(out),'signed retained count mismatch')
            if restricted:
                native_boxes=[int(line.split()[2]) for line in result.splitlines() if line.startswith('B ')]
                require(native_boxes==[len(boxes)],'parity residue box mismatch')
        require(len(out)==len(set(out)),'duplicate retained signed tuple')
        require(len(counts)==len(primes) and sum(counts)==det_rejected,'invalid prime partition')
        require(total==det_rejected+parity+len(out),'invalid signed partition')
        for p in out:
            require(all(abs(v)<=N[k] and (v-N[k])%2==0 for k,v in enumerate(p)),'signed bound failure')
            require(all(p[k]>0 for k in pos) and not any(sd_equations(p)),'signed equation/gauge failure')
            require(not sd_parity_failure(N,p),'retained parity failure')
            det=casimir_determinant(sd_tensor(p))
            require(all(det%q==0 for q in primes),'retained determinant failure')
        source='enumerate_signed_diophantine.cpp' if restricted else 'enumerate_signed.cpp'
        summary={'method':method,'total':total,
                 'primes':primes,'determinant_rejections':counts,'parity_rejections':parity,
                 'retained':len(out),
                 'source_sha256':self.source_hashes[source]}
        if restricted:
            require(parity==0,'parity-compatible search has rejected parity tuple')
            summary.update(domain='signed_bounds_and_adjoint_parity',parity_boxes=len(boxes),
                           parity_admissible_total=total)
        return out,summary

    def nonselfdual(self,N):
        if self.engine=='python':return nonselfdual_tables(N)
        require(max(N)<=1000,'C++ non-self-dual coefficient guard')
        line=' '.join(map(str,N))+'\n'
        result=subprocess.check_output([str(self.ns_exe)],input=line,text=True)
        out=[tuple(map(int,line.split()[1:])) for line in result.splitlines() if line.startswith('T ')]
        count=[int(line.split()[1]) for line in result.splitlines() if line.startswith('C ')]
        require(count==[len(out)] and out==sorted(set(out)),'invalid non-self-dual output')
        for p in out:
            require(all(abs(v)<=N[k] and (v-N[k])%2==0 for k,v in enumerate(p)),'non-self-dual bounds')
            require(p==ns_gauge(p) and not any(ns_equations(p)),'non-self-dual equations or gauge')
        return out

    def global_selfdual(self,N,primes):
        """Query the globally certified signed orbit census.

        The global verifier replays the complete canonical enumeration and
        its universal arithmetic exclusions once. This query expands every
        surviving orbit, then checks the original bounds, gauge and parity
        conditions exactly. Determinants are invariant under these actions.
        """
        require(self.global_catalog is not None,'global signed catalog unavailable')
        rows,manifest=self.global_catalog
        require(max(N)<=manifest['bound'],'signed query exceeds global census bound')
        primes=list(primes)
        require(primes==sorted(set(primes)) and all(s.isprime(q) for q in primes),'invalid global query primes')
        if self._global_signature_indices is None:
            self._global_signature_indices={}
            for index,(p,det) in enumerate(rows):
                signature=orbit_adjoint_signature(p)
                self._global_signature_indices.setdefault(signature,[]).append(index)
        signature=orbit_adjoint_signature(N)
        signature_indices=self._global_signature_indices.get(signature,())
        if primes:
            q=max(primes)
            cache_key=(q,signature)
            if cache_key not in self._global_prime_indices:
                self._global_prime_indices[cache_key]=tuple(k for k in signature_indices if rows[k][1]%q==0)
            eligible=self._global_prime_indices[cache_key]
        else:eligible=signature_indices
        pos=gauges(N);out=set();eligible_count=0
        for index in eligible:
            p,det=rows[index]
            if any(det%q for q in primes):continue
            eligible_count+=1
            if max(map(abs,p))>max(N):continue
            if index not in self._global_orbit_images:
                images=set()
                for mapping in SD_PERM_MAPS:
                    images.update(gauge_images(tuple(p[k] for k in mapping)))
                if len(self._global_orbit_images)>=8192:
                    del self._global_orbit_images[next(iter(self._global_orbit_images))]
                self._global_orbit_images[index]=tuple(sorted(images))
            for candidate in self._global_orbit_images[index]:
                if any(abs(v)>N[k] or (v-N[k])%2 for k,v in enumerate(candidate)):continue
                if any(candidate[k]<=0 for k in pos):continue
                if sd_parity_failure(N,candidate):continue
                out.add(candidate)
        out=sorted(out)
        for p in out:
            require(not any(sd_equations(p)),'global catalog contains a nonassociative table')
            det=casimir_determinant(sd_tensor(p))
            require(all(det%q==0 for q in primes),'global determinant data inconsistent')
        summary={'method':'global_signed_catalog_v3','bound':manifest['bound'],
                 'catalog_sha256':manifest['catalog_sha256'],
                 'generator_source_sha256':manifest['generator_source_sha256'],
                 'filter_source_sha256':manifest['filter_source_sha256'],
                 'catalog_orbits':len(rows),'eligible_orbits':eligible_count,
                 'orbit_filter':'adjoint_residue_signature_and_required_primes',
                 'primes':primes,'retained_tables':len(out)}
        return out,summary

def ns_gauge(p):
    a,b,c,d,e,f=p
    return min((u*a,v*b,u*c,u*d,v*e,v*f) for u,v in itertools.product((-1,1),repeat=2))
def nonselfdual_tables(N):
    # Eliminate a from the first or second equation whenever possible.
    out=set();A,B,C,D,E,F=[range(-n,n+1,2) for n in N]
    aset=set(A)
    for b,c,d,e,f in itertools.product(B,C,D,E,F):
        if b*(c-d)+d*(e-f) or -c*c+d*d-e*e+f*f-1:continue
        if c:
            rhs=b*b-2*b*e+c*c+d*d-1
            if rhs%c:continue
            aa=[rhs//c]
        elif d:
            rhs=b*b-b*e-b*f+2*c*d
            if rhs%d:continue
            aa=[rhs//d]
        else:aa=A
        for a in aa:
            p=(a,b,c,d,e,f)
            if a in aset and not any(ns_equations(p)):out.add(ns_gauge(p))
    return sorted(out)

def canonical_duality(R):
    if dual(R)==[0,1,2,3]:return R,list(range(4)),'sd'
    for p in PERMS:
        T=permute(R,p)
        if dual(T)==[0,1,3,2]:return T,list(p),'ns'
    raise VerificationError('unrecognized rank-four duality')
