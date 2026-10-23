"""Exact three-character and central-restriction obstructions.

For each input the finite verifier checks the displayed characters directly
against all fusion coefficients. No numerical search or character-table
completeness assertion is needed.
"""
import json,sys,itertools
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'work/obstructions'))
from arithmetic import read

# Coordinate pairs [constant, coefficient of sqrt(2)] for the two real
# codegree-16 characters.  The codegree-8 character may use i*sqrt(2).
DATA={
 'R9_1_17':{'invertibles':[0,1,2,7],'two':8,'irrational':[3,4,5,6],
            'phi_signs':[-1,1,1,-1],
            'psi':[1,-1,-1,'u',0,0,'-u',1,0],'psi_u':'sqrt2'},
 'R9_1_83':{'invertibles':[0,4,5,6],'two':3,'irrational':[1,2,7,8],
            'phi_signs':[1,1,-1,-1],
            'psi':[1,0,0,0,-1,-1,1,'u','-u'],'psi_u':'sqrt2'},
 'R9_1_122':{'invertibles':[0,6,7,8],'two':5,'irrational':[1,2,3,4],
             'phi_signs':[1,1,-1,-1],
             'psi':[1,0,0,'u','-u',0,-1,1,-1],'psi_u':'i_sqrt2'},
 'R9_1_120':{'invertibles':[0,5,6,7],'two':8,'irrational':[1,2,3,4],
             'phi_signs':[1,-1,1,-1],'phi_u':'i_sqrt2'},
}

def need(x,msg):
 if not x:raise ValueError(msg)

def character(R,row,K):
 n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
 need(row[0]==K.one,'unit character')
 for i,j in itertools.product(range(n),repeat=2):
  need(row[i]*row[j]==sum((K(R[i][j][k])*row[k] for k in range(n)),K.zero),'character identity')
 return sum((row[i]*row[du[i]] for i in range(n)),K.zero)

def verify():
 out=[]
 K=s.QQ.algebraic_field(s.sqrt(2),s.I);u=K.from_sympy(s.sqrt(2));ii=K.from_sympy(s.I)
 L=s.QQ.algebraic_field(s.sqrt(6));d=L.from_sympy(2+s.sqrt(6));D=L(16)*(L.one+d)
 for r in read():
  name=r['id']
  if name not in DATA:continue
  a=DATA[name];R=r['tensor'];G=a['invertibles'];X=a['irrational'];y=a['two']
  dims=[L.zero]*9
  for i in G:dims[i]=L.one
  for i in X:dims[i]=d
  dims[y]=L(2)
  for i,j in itertools.product(range(9),repeat=2):
   need(dims[i]*dims[j]==sum((L(R[i][j][k])*dims[k] for k in range(9)),L.zero),'FP character')
  need(sum((x*x for x in dims),L.zero)==D,'global dimension')
  need(d*d==L(4)*d+L(2),'quadratic relation')
  phi=[K.zero]*9
  for i in G:phi[i]=K.one
  phi[y]=K(-2)
  q=u*(ii if a.get('phi_u')=='i_sqrt2' else K.one)
  for i,sgn in zip(X,a['phi_signs']):phi[i]=K(sgn)*q
  need(character(R,phi,K)==K(16),'formal codegree 16')
  need(D/L(16)==L.one+d,'central dimension 1+d')
  rec={'id':name,'tensor_sha256':r['tensor_sha256'],
       'scope':'general_complex_after_signed_Galois_pseudo_unitary_reduction',
       'dimensions':{'invertibles':G,'two_dimensional':y,'dimension_2_plus_sqrt6':X},
       'codegree16_character':[str(K.to_sympy(x)) for x in phi]}
  if name=='R9_1_120':
   witnesses=[]
   for x in X:
    pairs=[(j,k,R[x][j][k],R[j][x][k]) for j,k in itertools.product(range(9),repeat=2) if R[x][j][k]!=R[j][x][k]]
    need(pairs,'a dimension-d object is central')
    witnesses.append({'object':x,'noncommuting_object':pairs[0][0],'output':pairs[0][1],'left_coefficient':pairs[0][2],'right_coefficient':pairs[0][3]})
   rec.update(kind='central_restriction_obstruction',noncommutator_witnesses=witnesses)
  else:
   need(all(R[i][j]==R[j][i] for i in range(9) for j in range(9)),'commutative input')
   phiminus=phi[:]
   for i in X:phiminus[i]=-phi[i]
   need(character(R,phiminus,K)==K(16),'second codegree16 character')
   w=u*(ii if a['psi_u']=='i_sqrt2' else K.one)
   psi=[w if x=='u' else -w if x=='-u' else K(x) for x in a['psi']]
   need(character(R,psi,K)==K(8),'formal codegree8 character')
   need(D/L(8)==L(2)+L(2)*d,'central dimension 2+2d')
   # Exhaustive check of the only 16 possible pairs of codegree16
   # restrictions. Symmetry forces phi(Y)=-phi(X); the other two
   # symmetry identities, summed, force psi(X)+psi(Y)=0.
   checks=[]
   for x,z in itertools.product(X,repeat=2):
    compatible=phi[z]==-phi[x]
    if compatible:need(psi[x]+psi[z]!=K.zero,'three-character contradiction fails')
    checks.append({'X':x,'Y':z,'first_symmetry_holds':compatible,
                   'psi_sum':str(K.to_sympy(psi[x]+psi[z])) if compatible else None})
   rec.update(kind='three_character_restriction_obstruction',
              second_codegree16_character=[str(K.to_sympy(x)) for x in phiminus],
              codegree8_character=[str(K.to_sympy(x)) for x in psi],pair_checks=checks)
  out.append(rec)
 need(len(out)==4,'missing inputs')
 return out

if __name__=='__main__':
 out=verify();(HERE/'quadratic_certificates.json').write_text(json.dumps(out,indent=2)+'\n')
 print('PASS: all four quadratic-family rings satisfy the exact categorical obstructions.')
