"""Exact commutative sector of unrestricted signed quotients of rank-six rings.

The source ring may be noncommutative. Commutativity is imposed only on
this sector, by equality of oriented coefficient variables; all coefficient
domains are intersected, with no Frobenius--Schur normalization. The source
formal codegrees come from its two linear characters and its M_2 block,
whose formal codegree is HALF the regular Casimir eigenvalue.

A successful certificate excludes this sector only. It must be combined
with a separate exhaustive argument for the noncommutative sector.
"""
import hashlib,itertools,json,re,subprocess,tempfile,time
from pathlib import Path
from exact import require,pc,ec,poly
from rings import dual,Characters
from oriented_signed import problem,validate_general
from signed import from_values
from oriented_extension import linear_data
from proofs import norm_failure,field_failure,check_norm,check_field

def make_problem(R):
 p=problem(R,normalized=False);mapping=p['mapping'];nvar=len(p['domains']);parent=list(range(nvar));zero=set()
 def find(i):
  if parent[i]!=i:parent[i]=find(parent[i])
  return parent[i]
 def union(a,b):parent[find(a)]=find(b)
 for i,j,k in itertools.product(range(1,len(R)),repeat=3):
  a=mapping.get((i,j,k));b=mapping.get((j,i,k))
  if a is None and b is None:continue
  if a is None:zero.add(b)
  elif b is None:zero.add(a)
  else:union(a,b)
 groups={}
 for i in range(nvar):groups.setdefault(find(i),[]).append(i)
 pos={v:j for j,v in enumerate(p['order'])};source=p['source'];records=[]
 for group in groups.values():
  rep=min(group,key=pos.get);domain=set(p['domains'][group[0]])
  for i in group[1:]:domain &= set(p['domains'][i])
  if any(i in zero for i in group):domain &= {0}
  domain=sorted(domain);records.append({'variables':group,'representative':rep,'domain':domain})
  for i in group:
   allowed=','.join(map(str,domain)) if i==rep else 'v['+str(rep)+']'
   source,count=re.subn(r'for\(int x:vector<int>\{[^}]*\}\)\{v\['+str(i)+r'\]=x;', 'for(int x:vector<int>{'+allowed+'}){v['+str(i)+']=x;',source)
   require(count==1,'native loop matching')
 return p,source,records

def enumerate_sector(R,seconds=120):
    validate_general(R,nonnegative=True)
    require(len(R)==6 and any(R[i][j]!=R[j][i] for i in range(6) for j in range(6)),
            'expected a noncommutative rank-six input')
    p,source,groups=make_problem(R)
    with tempfile.TemporaryDirectory() as td:
        src=Path(td)/'enum.cpp';exe=Path(td)/'enum';src.write_text(source)
        subprocess.run(['g++','-std=c++17','-O3',str(src),'-o',str(exe)],check=True,capture_output=True)
        run=subprocess.run([str(exe)],capture_output=True,text=True,check=True,timeout=seconds)
    m=re.fullmatch(r'nodes (\d+) solutions (\d+)\s*',run.stderr)
    require(m is not None,'commutative sector completion marker missing')
    vals=sorted(tuple(map(int,line.split())) for line in run.stdout.splitlines())
    require(len(vals)==len(set(vals))==int(m[2]),'commutative sector solution count')
    for v in vals:
        require(len(v)==len(p['domains']) and all(x in dom for x,dom in zip(v,p['domains'])),
                'oriented coefficient domain violated')
    return vals,p,{'nodes':int(m[1]),'solutions':int(m[2]),'complete':True,
                   'indicator_normalization':False,'variable_groups':groups,
                   'native_source_sha256':hashlib.sha256(source.encode()).hexdigest()}


def sign_orbits(R,vals,p):
    n=len(R);du=dual(R);allvalues=set(vals)
    signs=[(1,)+tail for tail in itertools.product((-1,1),repeat=n-1)
           if all(((1,)+tail)[i]==((1,)+tail)[du[i]] for i in range(n))]
    factors=[tuple(e[a]*e[b]*e[c] for orb in p['active'] for a,b,c in [orb[0]]) for e in signs]
    groups={}
    for v in vals:
        orbit={tuple(x*y for x,y in zip(v,f)) for f in factors}
        require(orbit<=allvalues,'commutative signed gauge orbit is incomplete')
        groups.setdefault(min(orbit),set()).add(v)
    return groups


def commutative_signed_sector_certificate(R,seconds=120):
    vals,p,stats=enumerate_sector(R,seconds);orbits=sign_orbits(R,vals,p);du=dual(R)
    _,_,q,fe,original_cf=linear_data(R)
    branches=[]
    for v,orbit in sorted(orbits.items()):
        T=from_values(R,p,v);validate_general(T)
        require(all(T[i][j]==T[j][i] for i in range(len(R)) for j in range(len(R))),
                'commutativity constraint not enforced')
        a=Characters(T);required=[(poly(pc(g)),m) for g,m in list(original_cf)+list(a.cf)]
        branch={'values':list(v),'orbit_size':len(orbit),'generator':a.k,'characters':[]}
        for f,m in a.components:
            K,ds,delta,pD=a.component(f)
            zero=next((i for i,d in enumerate(ds) if not d),None)
            unequal=next((i for i,d in enumerate(ds) if d!=ds[du[i]]),None)
            if zero is not None:why={'kind':'zero','object':zero}
            elif unequal is not None:why={'kind':'duality','object':unequal}
            else:why=norm_failure(pD,required) or field_failure(f,required)
            if why is None:return None
            branch['characters'].append({'factor':pc(f),'global_dimension_polynomial':pc(pD),
                                          'obstruction':why})
        branches.append(branch)
    return {'kind':'commutative_signed_sector','version':1,
            'scope':'commutative_sector_of_unrestricted_sphericalization_quotient',
            'original_linear_formal_codegree_polynomial':pc(q),
            'original_matrix_block_formal_codegree':str(fe),
            'enumeration':stats,'all_values':list(map(list,vals)),'branches':branches}


def verify(R,c):
    require(c.get('kind')=='commutative_signed_sector' and c.get('version')==1,
            'incorrect commutative sector certificate kind/version')
    require(c.get('scope')=='commutative_sector_of_unrestricted_sphericalization_quotient',
            'incorrect commutative sector scope')
    vals,p,stats=enumerate_sector(R);orbits=sign_orbits(R,vals,p)
    require(c['enumeration']==stats and c['all_values']==list(map(list,vals)),
            'incomplete unrestricted commutative sector enumeration')
    _,_,q,fe,original_cf=linear_data(R)
    require(c['original_linear_formal_codegree_polynomial']==pc(q) and
            c['original_matrix_block_formal_codegree']==str(fe),'source formal codegree normalization')
    require([b['values'] for b in c['branches']]==[list(v) for v in sorted(orbits)],
            'missing signed gauge orbit')
    rejections=0
    for (v,orbit),branch in zip(sorted(orbits.items()),c['branches']):
        require(branch['orbit_size']==len(orbit),'signed gauge orbit size')
        T=from_values(R,p,v);validate_general(T)
        require(all(T[i][j]==T[j][i] for i in range(len(R)) for j in range(len(R))),
                'noncommutative table in commutative sector')
        a=Characters(T,branch['generator']);required=[(poly(pc(g)),m) for g,m in list(original_cf)+list(a.cf)]
        require(len(branch['characters'])==len(a.components),'missing signed character component')
        for (f,m),cc in zip(a.components,branch['characters']):
            K,ds,delta,pD=a.component(f)
            require(cc['factor']==pc(f) and cc['global_dimension_polynomial']==pc(pD),
                    'incorrect signed character polynomial')
            why=cc['obstruction'];kind=why['kind']
            if kind=='zero':require(not ds[why['object']],'claimed zero dimension is nonzero')
            elif kind=='duality':require(ds[why['object']]!=ds[a.du[why['object']]],'dual dimensions agree')
            elif kind=='norm':check_norm(pD,required,why)
            elif kind.startswith('field_'):check_field(f,required,why)
            else:require(False,'unsupported commutative sector character obstruction')
            rejections+=1
    return {'commutative_signed_sector_excluded':True,'signed_tables':len(vals),
            'sign_orbits':len(orbits),'character_rejections':rejections,
            'indicator_normalization':False,'matrix_block_formal_codegree':str(fe)}


certificate=commutative_signed_sector_certificate
