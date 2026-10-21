"""Exact integer Gram, distinguished-S and cubic Verlinde necessary systems.

No numerical solver is used here. Low variables select distinguished
restrictions, high variables count complete duality orbits, and cubic
auxiliary variables are actual nonnegative integral fusion coefficients.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
import hashlib,itertools,json,math,sys
import sympy as s
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'global_induction'))
import streaming as st
from exact import require

@dataclass
class System:
    columns: tuple
    rhs: tuple
    bounds: tuple
    row_labels: tuple
    column_labels: tuple
    metadata: dict

def power_coordinates(value,degree):
    v=list(reversed(value.to_list()));require(len(v)<=degree,'field degree mismatch')
    return tuple(Q(str(x))for x in v)+tuple(Q(0)for _ in range(degree-len(v)))

def build(C,T,frame_index=None):
    R=C.R;require(all(R[i][j]==R[j][i]for i in range(8)for j in range(8)),'commutative integer adapter only')
    K=T.K;degree=T.degree;characters=T.characters
    fp=next(E for E,ch in enumerate(characters)if tuple(ch)==tuple(T.ds))
    require(sum(tuple(ch)==tuple(T.ds)for ch in characters)==1,'FP character not unique')
    du=[next(j for j in range(8)if R[i][j][0])for i in range(8)]
    dualE=[]
    for ch in characters:
        matches=[E for E,row in enumerate(characters)if tuple(row)==tuple(ch[j]for j in du)]
        require(len(matches)==1,'dual character not unique');dualE.append(matches[0])
    require(dualE[fp]==fp,'FP character not self-dual')
    labels=[E for E in range(8)if E!=fp]
    triples=[(E,F,G)for E,F in itertools.combinations_with_replacement(labels,2)for G in labels]
    symmetric_keys=[tuple(sorted((E,F,dualE[G])))for E,F,G in triples]
    unique_keys=tuple(sorted(set(symmetric_keys)))
    intern={Q(0):Q(0)}
    def share(x):x=Q(x);return intern.setdefault(x,x)
    cache={};chi_cache={}
    def chi(v):
        v=tuple(v)
        if v not in chi_cache:chi_cache[v]=tuple(sum((K(n)*a for n,a in zip(v,ch)),K.zero)for ch in characters)
        return chi_cache[v]
    def cubic(v):
        v=tuple(v)
        if v not in cache:
            cv=chi(v);dim=sum((K(n)*d for n,d in zip(v,T.ds)),K.zero);require(dim!=K.zero,'zero central dimension')
            normalized=tuple(T.beta[E]*cv[E]for E in range(8))
            denominator=K.one/(T.D**2*dim)
            pairs={pair:normalized[pair[0]]*normalized[pair[1]]for pair in set(k[:2]for k in unique_keys)}
            values={k:tuple(share(x)for x in power_coordinates(pairs[k[:2]]*normalized[k[2]]*denominator,degree))for k in unique_keys}
            cache[v]=tuple(x for k in symmetric_keys for x in values[k])
        return cache[v]
    unit=(1,)+(0,)*7
    if frame_index is None:
        require('low_character_labels'in C.meta,'atomic character labels required')
        groups=C.meta['low_character_labels'];lows=[(groups[g],tuple(v))for g,v,z in C.low]
        fixed=[unit]
    else:
        require(0<=frame_index<len(C.frames),'invalid complete frame index')
        lows=[];fixed=[unit]+[C.low[j][1]for j in C.frames[frame_index]]
        require(C.meta['frame_character_labels'][frame_index][0]==fp,'fixed unit character mismatch')
    B=s.Matrix(C.a['B']);H=B-sum((s.Matrix(v)*s.Matrix(v).T for v in fixed),s.zeros(8))
    rows=[];rhs=[];prefix=[];column_labels=[];bounds=[]
    def add(label,b):rows.append(label);rhs.append(Q(b));return len(rows)-1
    simplex={E:add(('low_onehot',E),1)for E in labels}if lows else{}
    gram={(i,j):add(('gram',i,j),H[i,j])for i in range(8)for j in range(i,8)}
    # Full distinguished S symmetry; no phase projection is involved.
    sr={(E,F,k):add(('S_symmetry',E,F,k),0)for E,F in itertools.combinations(labels,2)for k in range(degree)}if lows else{}
    low_lookup={x:i for i,x in enumerate(lows)};duality_rows={};duality_entries={}
    if lows:
        for i,(E,v)in enumerate(lows):
            other=(dualE[E],tuple(v[du[j]]for j in range(8)))
            require(other in low_lookup,'low domain not closed under distinguished duality')
            j=low_lookup[other]
            if i<j:
                row=add(('low_duality',i,j),0);duality_rows[i,j]=row;duality_entries[i]=(row,Q(1));duality_entries[j]=(row,Q(-1))
    for at,(G,v)in enumerate(lows):
        p={simplex[G]:Q(1)}
        p.update({row:Q(v[i]*v[j])for (i,j),row in gram.items()if v[i]*v[j]})
        cv=chi(v)
        for E,F in itertools.combinations(labels,2):
            value=(T.beta[E]*cv[E]if G==F else K.zero)-(T.beta[F]*cv[F]if G==E else K.zero)
            for k,x in enumerate(power_coordinates(value,degree)):
                if x:p[sr[E,F,k]]=share(x)
        if at in duality_entries:
            row,value=duality_entries[at];p[row]=value
        prefix.append(p);column_labels.append(('low',G,v));bounds.append(1)
    cubic_columns=[cubic(v)for E,v in lows]
    # Per-orbit counts are integers. Old compressed phase variables are not
    # imported and are never given an extra integrality assumption here.
    for orbit in C.orbits:
        vs=[(0,)+tuple(C.a['high'][j][0])for j in orbit]
        g={(i,j):sum(v[i]*v[j]for v in vs)for i in range(8)for j in range(i,8)}
        upper=min(int(H[i,i]//g[i,i])for i in range(8)if g[i,i])
        if upper<=0:continue
        prefix.append({gram[i,j]:Q(value)for(i,j),value in g.items()if value})
        column_labels.append(('high_orbit',tuple(orbit),tuple(vs)));bounds.append(upper)
        features=[cubic(v)for v in vs]
        cubic_columns.append(tuple(share(sum(row,Q(0)))for row in zip(*features)))
    fixed_cubic=tuple(sum(values,Q(0))for values in zip(*(cubic(v)for v in fixed)))
    cubic_start=len(rows)
    for triple in triples:
        for k in range(degree):add(('cubic',*triple,k),-fixed_cubic[len(rows)-cubic_start])
    nr=len(rows);base_count=len(prefix);scales=[1]*nr
    for i,b in enumerate(rhs):scales[i]=b.denominator
    for p,features in zip(prefix,cubic_columns):
        for i,x in p.items():scales[i]=math.lcm(scales[i],x.denominator)
        for j,x in enumerate(features):scales[cubic_start+j]=math.lcm(scales[cubic_start+j],x.denominator)
    intcache={0:0}
    def integer(x,row):
        z=Q(x)*scales[row];require(z.denominator==1,'nonintegral row scaling');v=int(z);return intcache.setdefault(v,v)
    columns=[]
    for p,features in zip(prefix,cubic_columns):
        col=[0]*cubic_start
        for row,x in p.items():col[row]=integer(x,row)
        col.extend(integer(x,cubic_start+j)for j,x in enumerate(features));columns.append(tuple(col))
    for ti,triple in enumerate(triples):
        row=cubic_start+ti*degree;col=[0]*nr;col[row]=-scales[row];columns.append(tuple(col));column_labels.append(('fusion_coefficient',*triple))
        upper=fixed_cubic[ti*degree]+sum(max(Q(0),features[ti*degree])*bound for features,bound in zip(cubic_columns,bounds[:base_count]))
        bounds.append(max(0,math.floor(upper)))
    b=tuple(integer(x,i)for i,x in enumerate(rhs));columns=tuple(columns)
    h=hashlib.sha256()
    for col in columns:h.update((repr(col)+'\n').encode())
    metadata={'kind':'commutative_integer_Gram_S_cubic','tensor_sha256':st.digest(R),'FP_character':fp,'dual_characters':dualE,
              'frame_index':frame_index,'field_degree':degree,'field_polynomial':list(map(str,K.mod.to_list())),
              'rows':nr,'variables':len(columns),'low_variables':len(lows),'high_variables':base_count-len(lows),'fusion_variables':len(triples),
              'columns_sha256':h.hexdigest(),'rhs_sha256':st.digest(b),'bounds_sha256':st.digest(bounds),'row_labels_sha256':st.digest(rows),'column_labels_sha256':st.digest(column_labels)}
    return System(columns,b,tuple(bounds),tuple(rows),tuple(column_labels),metadata)

def check_integer(system,values):
    require(len(values)==len(system.columns),'integer witness length differs')
    require(all(isinstance(v,int)and 0<=v<=bound for v,bound in zip(values,system.bounds)),'integer witness outside finite nonnegative bounds')
    total=[0]*len(system.rhs)
    for value,col in zip(values,system.columns):
        if value:
            for i,x in enumerate(col):total[i]+=value*x
    require(tuple(total)==system.rhs,'integer witness fails exact equality')
    return True

def verify_modular(system,certificate):
    p=certificate['prime'];y=certificate['covector'];require(s.isprime(p)and len(y)==len(system.rhs),'invalid modular witness')
    require(all(sum(a*b for a,b in zip(y,col))%p==0 for col in system.columns),'modular covector does not annihilate every column')
    value=sum(a*b for a,b in zip(y,system.rhs))%p;require(value!=0 and value==certificate['rhs_residue'],'modular rhs is not separated')
    return True
