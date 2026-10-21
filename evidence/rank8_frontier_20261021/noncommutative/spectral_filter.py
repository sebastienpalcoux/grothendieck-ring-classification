"""Algebraic-integrality constraints for the known rows of the center S matrix."""
import character_modular as modular
from proofs import multiplication_matrix
c=modular.c;full=modular.full

def high_columns(R,a,cols):
    if a['factor'].degree()==4:return full.base.bq.high_columns(a,cols)[2]
    L=c.s.Matrix.hstack(*map(c.s.Matrix,cols));return full.base.grams.high_columns(a,L)[1]

def rejected(R,a,cols):
    K=a['K'];chs=modular.characters(R,a);out=[];cache={}
    for index,(v,z) in enumerate(high_columns(R,a,cols)):
        vv=(0,)+tuple(v);dimension=sum((K(x)*d for x,d in zip(vv,a['ds'])),K.zero)
        for E,(fc,mm,ch) in enumerate(zip(a['codegrees'],a['multiplicities'],chs)):
            eigenvalue=a['D']/fc/K(mm)*modular.value(ch,vv,K)/dimension;key=tuple(c.ec(eigenvalue))
            if key not in cache:cache[key]=multiplication_matrix(eigenvalue,K,a['factor']).charpoly().all_coeffs()
            poly=cache[key]
            if any(co.q!=1 for co in poly):
                out.append({'high_index':index,'column':list(v),'character':E,'eigenvalue':c.ec(eigenvalue),'characteristic_polynomial':list(map(str,poly))});break
    return out

def append_filter(R,a,cols,A,b,meta):
    bad=rejected(R,a,cols);A=list(A);b=list(b);nt=meta['trace_types']
    for rec in bad:
        row=[0]*len(A[0]);j=rec['high_index'];row[j*nt:(j+1)*nt]=[1]*nt;A.append(row);b.append(0)
    return A,b,dict(meta,spectral_rejections=bad)
