"""Necessary complete forgetful-product unit identities and coordinate bounds.

For fixed distinguished simples E,F, monoidality of forgetful F implies
F(E)F(F)=delta(E,F*)1+sum_G N_EF^G F(G)+nonnegative high contribution.
All unknown high restrictions have zero source-unit coefficient.  Thus the
unit coordinate is exact; every remaining coordinate gives a finite bound.
No integrality is imposed on any phase variable.
"""
from dataclasses import replace
from pathlib import Path
import itertools,json,sys,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import prepare as p
from features import require

def append(system,C,T):
 fi=system.metadata['frame_index'];require(fi is not None,'fixed low frame required')
 fp=system.metadata['FP_character'];dual=system.metadata['dual_characters']
 labels=[E for E in range(8) if E!=fp]
 vectors=[(1,)+(0,)*7]+[C.low[j][1] for j in C.frames[fi]]
 low=dict(zip(C.meta['frame_character_labels'][fi],vectors))
 lookup={tuple(label[1:]):j for j,label in enumerate(system.column_labels) if label[0]=='fusion_coefficient'}
 rows=[];rhs=[];rl=[];slacks=[]
 for E,F in itertools.combinations_with_replacement(labels,2):
  product=[sum(low[E][i]*low[F][j]*C.R[i][j][k] for i in range(8) for j in range(8)) for k in range(8)]
  for k in range(8):
   row=[0]*len(system.columns)
   for G in labels:row[lookup[E,F,G]]=low[G][k]
   b=product[k]-int(k==0 and F==dual[E])
   rows.append(row);rhs.append(b);rl.append(('full_forgetful_product',E,F,k))
   if k:slacks.append((len(rows)-1,E,F,k,b))
 cols=[tuple(c)+tuple(row[j] for row in rows) for j,c in enumerate(system.columns)]
 bounds=list(system.bounds);cl=list(system.column_labels);offset=len(system.rhs)
 for at,E,F,k,b in slacks:
  col=[0]*(offset+len(rows));col[offset+at]=1;cols.append(tuple(col));bounds.append(b);cl.append(('forgetful_product_slack',E,F,k))
 meta={**system.metadata,'full_product':{'equalities':28,'coordinate_inequalities':196,'scope':'pseudo_unitary_necessary_fixed_low_frame'}}
 return replace(system,columns=tuple(cols),rhs=tuple(system.rhs)+tuple(rhs),bounds=tuple(bounds),row_labels=tuple(system.row_labels)+tuple(rl),column_labels=tuple(cl),metadata=meta)

def make(fi):
 ring=p.old.st.load_ring('R8_3_982');C=p.old.cg.cone(ring['tensor'],4,'sts_frame');T=p.old.character_table(ring['tensor'],C.a)
 D,profile=p.old.filtered(C,fi);print('filtered',fi,flush=True)
 S=p.old.f.build(D,T,frame_index=fi);S=p.old.append_galois_balance(S,D,T);S=p.tighten_fusion_bounds(S,D,T)
 S=append(S,D,T);print('built',fi,len(S.rhs),len(S.columns),flush=True)
 box=p.old.box.propagate(S)
 (HERE/f'product_frame{fi}_box.json').write_text(json.dumps(box,separators=(',',':'))+'\n')
 print('box',fi,box['outcome'],box['fixed_variables'],box['tightenings'],flush=True)
 if box['outcome']=='integer_box_obstruction':return
 Q=p.old.equations.compact(p.old.box.reduced(S,box))
 out={'frame':fi,'tensor_sha256':ring['tensor_sha256'],'columns':Q.columns,'rhs':Q.rhs,'bounds':Q.bounds,'labels':Q.column_labels,'metadata':Q.metadata,'source_lower':box['lower_bounds'],'source_upper':box['upper_bounds']}
 (HERE/f'product_frame{fi}_system.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
 print('cached',fi,len(Q.rhs),len(Q.columns),flush=True)
 import linear
 result=linear.discover(Q)
 (HERE/f'product_frame{fi}_linear.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
 print('linear',fi,result['conclusion'],result.get('numerical_phase_I_objective'),flush=True)
if __name__=='__main__':make(int(sys.argv[1]))
