"""Exact zero/proportional equality compression, preserving integer solutions."""
from dataclasses import replace
import hashlib,math
from features import require,st

def compact(system):
    m=len(system.rhs);n=len(system.columns);rows=[[]for _ in range(m)]
    for j,col in enumerate(system.columns):
        for i,a in enumerate(col):
            if a:rows[i].append((j,a))
    lookup={};unique=[];rhs=[];representatives=[];mapping=[]
    for i,(row,b)in enumerate(zip(rows,system.rhs)):
        if not row and not b:mapping.append(None);continue
        g=abs(b)
        for j,a in row:g=math.gcd(g,abs(a))
        require(g>0,'zero row content')
        scale=g if (row[0][1]if row else b)>0 else -g
        key=(tuple((j,a//scale)for j,a in row),b//scale)
        if key not in lookup:
            lookup[key]=len(unique);unique.append(key[0]);rhs.append(key[1]);representatives.append((i,scale))
        mapping.append((lookup[key],scale))
    columns=[[0]*len(unique)for _ in range(n)]
    for i,row in enumerate(unique):
        for j,a in row:columns[j][i]=a
    columns=tuple(map(tuple,columns));h=hashlib.sha256()
    for col in columns:h.update((repr(col)+'\n').encode())
    metadata={'kind':'exact_proportional_equation_compression','source_metadata':system.metadata,
              'original_rows':m,'rows':len(rhs),'variables':n,'columns_sha256':h.hexdigest(),'rhs_sha256':st.digest(rhs),
              'row_mapping_sha256':st.digest(mapping),'representatives':[list(v)for v in representatives]}
    return replace(system,columns=columns,rhs=tuple(rhs),row_labels=tuple(('scaled_original_row',i,d)for i,d in representatives),metadata=metadata)


def lift_separator(original,compressed,certificate):
    from fractions import Fraction as Q
    from lattice import verify_separator
    reps=compressed.metadata['representatives'];values=[Q(0)]*len(original.rhs)
    for y,(i,scale)in zip(certificate['covector'],reps):values[i]+=Q(y,scale)
    d=math.lcm(*(v.denominator for v in values));y=[int(v*d)for v in values]
    if certificate['kind']=='rational_annihilator':
        out={'kind':'rational_annihilator','covector':y,'rhs_value':sum(a*b for a,b in zip(y,original.rhs))}
    else:
        modulus=certificate['modulus']*d;out={'kind':'integral_modular_annihilator','covector':y,'modulus':modulus,'rhs_residue':sum(a*b for a,b in zip(y,original.rhs))%modulus}
    verify_separator(original,out);return out
