"""General signed-spectrum saturation for noncommutative rank-six rings.

Noncommutativity modulo two forces every oriented signed quotient to have
Wedderburn type C + C + M_2(C). Original central induction isolates its
quadratic dimension field. Exact finite codegree enumeration bounds the
Casimir deficit; saturated cases admit a complete sign-only enumeration.
No indicator normalization, commutative quotient, or pivotality is assumed.
"""
from fractions import Fraction as Q
import itertools, math, re, subprocess, tempfile
from pathlib import Path
import sympy as s
from exact import require, pc
from rings import dual, validate
from weighted_induction import data
from induction import low_failure
from oriented_signed import problem, validate_general
from signed import from_values, gauge_original


def hypotheses(R,allow_even_commutators=False):
    if len(R)!=6:return None
    witness=next(((i,j,k) for i,j,k in itertools.product(range(6),repeat=3)
                  if (R[i][j][k]-R[j][i][k])%2),None)
    if witness is None and not allow_even_commutators:return None
    if all(R[i][j]==R[j][i] for i in range(6) for j in range(6)):return None
    a=data(R)
    if a['factor'].degree()!=2 or a['q']%4!=1:return None
    validate_general(R,nonnegative=True)
    A,B=a['global_dimension'];h=int(a['codegrees'][-1].to_list()[0])
    return a,{'noncommutative_mod2_witness':list(witness) if witness else None,
        'requires_commutative_sector_exclusion':witness is None,
        'quadratic_radicand':a['q'],'FP_dimension':[str(A),str(B)],
        'matrix_block_codegree':h,'Casimir_trace':int(s.trace(a['Casimir'])),
        'linear_character_polynomial':pc(a['factor']),
        'original_formal_codegree_multiplicities':[1,1,2]}


def integral(a,b):
    """a+b sqrt(q) in O_q for squarefree q=1 mod 4."""
    return (2*b).denominator==1 and (a-b).denominator==1


def arithmetic(R,allow_even_commutators=False):
    z=hypotheses(R,allow_even_commutators=allow_even_commutators)
    if z is None:return None
    a,hyp=z;q=a['q'];A,B=a['global_dimension'];T=hyp['Casimir_trace']
    c=hyp['matrix_block_codegree'];norm=A*A-q*B*B
    if T>10000:raise TimeoutError('noncommutative spectrum trace budget')
    out=[]
    # Delta=(tr+b2 sqrt(q))/2 and Tr(Delta)+8h <= T.
    # All positive signed formal codegrees are >1. The reciprocal identity
    # forces h>2 and therefore tr <= T-24.
    for tr in range(c,T-23,c):
        bound=math.isqrt((tr*tr-1)//q)
        for b2 in range(-bound,bound+1):
            u,v=Q(tr,2),Q(b2,2)
            if not integral(u,v) or not integral(u/c,v/c):continue
            if not integral((u*A-q*v*B)/norm,(v*A-u*B)/norm):continue
            if not integral((u*A+q*v*B)/norm,(v*A+u*B)/norm):continue
            no=u*u-q*v*v
            if (Q(tr*tr)/no).denominator!=1 or no<=tr:continue
            h=2/(1-Q(tr)/no)
            if h.denominator!=1 or h<=2 or tr+8*h>T:continue
            if not integral(u/h,v/h):continue
            out.append({'dimension_numerator':[tr,b2],'dimension_denominator':2,
                'dimension_norm':str(no),'matrix_block_codegree':int(h),
                'signed_Casimir_trace':int(tr+8*h)})
    lower=min((z['signed_Casimir_trace'] for z in out),default=None)
    return {'kind':'noncommutative_signed_spectrum','hypotheses':hyp,
        'spectra':out,'signed_Casimir_lower_bound':lower,
        'deficit_budget':None if lower is None else T-lower,'excluded':not out}


def saturated_signs(R,seconds=120):
    p=problem(R,normalized=False);source=p['source'];magnitudes=[]
    for i,dom in enumerate(p['domains']):
        bound=max(map(abs,dom));magnitudes.append(bound)
        d=[v for v in dom if abs(v)==bound]
        source,count=re.subn(r'for\(int x:vector<int>\{[^}]+\}\)\{v\['+str(i)+r'\]=x;',
            'for(int x:vector<int>{'+','.join(map(str,d))+'}){v['+str(i)+']=x;',source)
        require(count==1,'oriented sign-only loop reconstruction')
    with tempfile.TemporaryDirectory() as td:
        cpp=Path(td)/'enum.cpp';exe=Path(td)/'enum';cpp.write_text(source)
        subprocess.run(['g++','-std=c++17','-O3',str(cpp),'-o',str(exe)],check=True,capture_output=True)
        run=subprocess.run([str(exe)],capture_output=True,text=True,check=True,timeout=seconds)
    m=re.fullmatch(r'nodes (\d+) solutions (\d+)\s*',run.stderr)
    require(m is not None,'oriented enumeration completion missing')
    vals=sorted(tuple(map(int,x.split())) for x in run.stdout.splitlines())
    require(len(vals)==int(m[2])==len(set(vals)),'oriented sign-only solution count')
    cases=[]
    for v in vals:
        require(len(v)==len(magnitudes) and all(abs(x)==b for x,b in zip(v,magnitudes)),
                'oriented sign-only domain mismatch')
        T=from_values(R,p,v);validate_general(T)
        g=gauge_original(T,R)
        if g is None:return None
        cases.append({'values':list(v),'gauge_original':g})
    return {'magnitudes':magnitudes,'indicator_restrictions':False,
        'statistics':{'nodes':int(m[1]),'solutions':int(m[2]),'complete':True},
        'signed_tables':cases}


def certificate(R,commutative_sector=None):
    a=arithmetic(R,allow_even_commutators=True)
    if a is None:return None
    extra={}
    if a['hypotheses']['requires_commutative_sector_exclusion']:
        import round3_commutative_sector
        if commutative_sector is None:
            commutative_sector=round3_commutative_sector.certificate(R)
            if commutative_sector is None:return None
        round3_commutative_sector.verify(R,commutative_sector)
        extra={'commutative_sector':commutative_sector}
    else:require(commutative_sector is None,'unnecessary commutative sector certificate')
    if a['excluded']:
        return {'kind':'noncommutative_signed_exclusion','scope':'general_complex_fusion_categories',
                'arithmetic':a,**extra}
    if a['deficit_budget']!=0:return None
    signs=saturated_signs(R)
    if signs is None:return None
    z=data(R);branches=[]
    for cols in z['lows']:
        why=low_failure(cols,z['Gram'],z['ds'],z['D'],z['K'],z['embedding'],z['du'])
        if why is None:return None
        branches.append({'columns':[list(c) for c in cols],'ordinary':why})
    return {'kind':'noncommutative_signed_exclusion','scope':'general_complex_fusion_categories',
        'arithmetic':a,'reduction':signs,**extra,
        'pseudo':{'kind':'weighted_ordinary_induction','column_counts':list(map(len,z['columns'])),
                  'low_count':len(z['lows']),'branches':branches}}


def verify(R,c):
    require(c.get('kind')=='noncommutative_signed_exclusion','wrong noncommutative certificate kind')
    require(c.get('scope')=='general_complex_fusion_categories','wrong noncommutative scope')
    if c.get('arithmetic',{}).get('hypotheses',{}).get('requires_commutative_sector_exclusion'):
        require(isinstance(c.get('commutative_sector'),dict),'missing commutative sector exclusion')
    z=certificate(R,c.get('commutative_sector'))
    require(z is not None and z==c,'noncommutative certificate differs from exact reconstruction')
    return True
