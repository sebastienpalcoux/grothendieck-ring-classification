#!/usr/bin/env python3
"""Exact source hypotheses for the general dimension-90 structural theorem.

Categorical inputs are explicitly cited in D90_STRUCTURAL_PROOF.md. The
executable verifies fusion axioms, a positive integral dimension character,
the adjoint closure, the sign action, the forced de-equivariantization type,
and the elementary arithmetic in the dimension-45 group-theoretical argument.
Default replay is read-only. Only --write regenerates the deterministic receipt.
"""
from collections import Counter
from pathlib import Path
import argparse,hashlib,itertools,json,math
HERE=Path(__file__).resolve().parent
KIND='dimension90_solvable_rigidity'
SCOPE='general_complex_fusion_category'
REFERENCES=[
 {'author':'Jingcheng Dong','title':'Classification of certain weakly integral fusion categories','url':'https://arxiv.org/pdf/2103.04553v3','locator':'Corollary4.16, printed p17','input':'Every complex fusion category of FP dimension90 is solvable.'},
 {'author':'Etingof-Nikshych-Ostrik','title':'Weakly group-theoretical and solvable fusion categories','url':'https://arxiv.org/pdf/0809.3031v2','locator':'Proposition4.4, printed p13','input':'A solvable category has a final cyclic-prime extension or equivariantization step.'},
 {'author':'Jordan-Larson','title':'On the classification of certain fusion categories','url':'https://arxiv.org/pdf/0812.1603v2','locator':'Theorem1.1, printed p2','input':'An integral category of dimension p*q^2 is group-theoretical unless p=2 or odd p divides q+1.'},
 {'author':'Gelaki-Naidu','title':'Some properties of group-theoretical categories','url':'https://arxiv.org/pdf/0709.4326v1','locator':'Section5.1 and Theorem5.1, printed pp7-8','input':'Simple objects are double-coset/projective-stabilizer pairs, with the displayed stabilizer cocycle.'},
]
def require(test,message):
 if not test:raise ValueError(message)
def digest(value):return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()
def axioms(R):
 n=len(R);require(n==8 and all(len(A)==n and all(len(row)==n for row in A)for A in R),'rank-eight tensor shape')
 require(all(type(v)is int and v>=0 for A in R for row in A for v in row),'nonnegative integral coefficients')
 require(all(R[0][i]==R[i][0]==[int(i==j)for j in range(n)]for i in range(n)),'based unit')
 du=[]
 for i in range(n):
  hits=[j for j in range(n)if R[i][j][0]];require(len(hits)==1,'unique dual');du.append(hits[0])
 require(all(R[i][j][0]==int(j==du[i])for i,j in itertools.product(range(n),repeat=2)),'duality multiplicity')
 require(all(R[i][j][k]==R[du[j]][du[i]][du[k]]==R[du[i]][k][j]for i,j,k in itertools.product(range(n),repeat=3)),'Frobenius reciprocity')
 require(all(sum(R[i][j][a]*R[a][k][b]for a in range(n))==sum(R[j][k][a]*R[i][a][b]for a in range(n))for i,j,k,b in itertools.product(range(n),repeat=4)),'associativity')
 return du
def closure(R,seed):
 basis=set(seed)|{0};history=[sorted(basis)]
 while True:
  enlarged=basis|{k for i in basis for j in basis for k,v in enumerate(R[i][j])if v}
  if enlarged==basis:return sorted(basis),history
  basis=enlarged;history.append(sorted(basis))
def theorem_certificate(R):
 n=8;du=axioms(R);unit=[1]+[0]*7
 invertibles=[i for i in range(n)if R[i][du[i]]==unit]
 require(len(invertibles)==2 and invertibles[0]==0,'exactly two invertibles')
 g=invertibles[1];require(R[g][g]==unit,'sign involution')
 noninvertibles=[i for i in range(n)if i not in invertibles];candidates=[]
 for sixes in itertools.combinations(noninvertibles,2):
  ds=[1 if i in invertibles else 6 if i in sixes else 2 for i in range(n)]
  if all(sum(R[i][j][k]*ds[k]for k in range(n))==ds[i]*ds[j]for i,j in itertools.product(range(n),repeat=2)):candidates.append(ds)
 require(len(candidates)==1,'unique positive integral type(1^2,2^4,6^2) character');ds=candidates[0]
 require(Counter(ds)=={1:2,2:4,6:2} and sum(d*d for d in ds)==90,'dimension90 type')
 left=[];right=[]
 for i in range(n):
  require(sum(R[g][i])==sum(R[i][g])==1,'invertible action permutation')
  left.append(R[g][i].index(1));right.append(R[i][g].index(1))
 require(all(left[i]==right[i]==i for i in noninvertibles),'sign fixes every noninvertible')
 seed={k for i in range(n)for k,v in enumerate(R[i][du[i]])if v};adjoint,history=closure(R,seed)
 require(adjoint==list(range(n)),'nontrivial universal grading remains possible')
 subrings=[]
 for mask in range(1<<7):
  B=[0]+[i for i in range(1,n)if mask>>(i-1)&1];closed,_=closure(R,B)
  if closed==B and all(du[i]in B for i in B):subrings.append(dict(basis=B,dimension=sum(ds[i]**2 for i in B)))
 # In a C2-equivariantization, a fixed simple has two sign-exchanged lifts.
 # All six sign-fixed noninvertibles must therefore come from free orbits.
 forced=[1]
 for i in noninvertibles:
  require(ds[i]%2==0,'free-orbit dimension must halve integrally');forced.extend([ds[i]//2]*2)
 forced.sort();require(Counter(forced)=={1:9,3:4}and sum(d*d for d in forced)==45,'forced dimension45 type')
 sylow={str(p):[m for m in range(1,46)if (45//power)%m==0 and m%p==1]for p,power in [(3,9),(5,5)]}
 require(sylow=={'3':[1],'5':[1]},'Sylow arithmetic for order45')
 require(45==5*3**2 and 5!=2 and (3+1)%5!=0,'Jordan-Larson exceptional case')
 noncyclic_H=[dict(order=h,index=45//h,schur_multiplier_exponent=3,restriction_coprime_to3=math.gcd(45//h,3)==1)for h in (9,45)]
 require(all(r['restriction_coprime_to3']for r in noncyclic_H),'restriction/corestriction coprimality')
 return dict(kind=KIND,scope=SCOPE,tensor_sha256=digest(R),dimension_character=ds,dimension_character_products_checked=64,global_dimension=90,duality=du,invertibles=invertibles,sign_involution=g,left_sign_action=left,right_sign_action=right,adjoint_seed=sorted(seed),adjoint_closure_steps=history,adjoint_basis=adjoint,all_closed_subrings=subrings,forced_deequivariantization_dimensions=forced,forced_deequivariantization_global_dimension=45,dimension45_group_arithmetic=dict(sylow_counts=sylow,abelian_group_invariant_factors=[[45],[3,15]],noncyclic_stabilizers=noncyclic_H,Jordan_Larson_parameters=dict(p=5,q=3,p_divides_q_plus_one=False)),contradiction='The forced dimension45 category has four3-dimensional simples, whereas all integral categories of dimension45 are pointed by the cited group-theoretical/cohomology argument.')
def verify(R,c):
 require(c==theorem_certificate(R),'dimension90 structural certificate differs')
def records():
 rows={r['id']:r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text())};out=[]
 for ident in ('R8_3_2904','R8_3_3082'):
  row=rows[ident];require(digest(row['tensor'])==row['tensor_sha256'],'source tensor SHA');c=theorem_certificate(row['tensor']);verify(row['tensor'],c)
  out.append(dict(id=ident,tensor_sha256=row['tensor_sha256'],excluded=True,scope=SCOPE,certificate=c))
 return dict(schema='rank8-dimension90-structural-v1',proof='evidence/rank8_m3_20261021/models/D90_STRUCTURAL_PROOF.md',references=REFERENCES,records=out)
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args();actual=records();target=HERE/'d90_structural.json'
 if args.write:target.write_text(json.dumps(actual,indent=2)+'\n')
 else:require(actual==json.loads(target.read_text()),'dimension90 structural receipt differs')
 print('PASS: two general dimension90 exclusions; exact fusion axioms,64 dimension identities,adjoint closure,sign action,and dimension45 arithmetic per source.')
if __name__=='__main__':main()
