"""Targeted exact receipt/witness verification and actual-center controls."""
from charged_quartic_pair import *

def controls():
 # Ising ordering: 1,sigma,psi.  The product with its reverse is Z(Ising).
 R=[[[1,0,0],[0,1,0],[0,0,1]],[[0,1,0],[1,0,1],[0,1,0]],[[0,0,1],[0,1,0],[1,0,0]]]
 rt=(F(0),F(1),F(0),F(0));S0=[[ONE,rt,ONE],[rt,Z,scale(rt,-1)],[ONE,scale(rt,-1),ONE]]
 labels=list(product(range(3),repeat=2));S=[[mul(S0[a][c],S0[b][d]) for c,d in labels] for a,b in labels]
 dims=S[0];g=labels.index((2,0));permutation=[labels.index((2-a if a!=1 else 1,b)) for a,b in labels]
 charge=[div(v,d)[0] for v,d in zip(S[g],dims)];pairs=list(cwr(range(9),2))
 X=s.Matrix(9,len(pairs),lambda k,p:R[labels[pairs[p][0]][0]][labels[pairs[p][1]][0]][labels[k][0]]*R[labels[pairs[p][0]][1]][labels[pairs[p][1]][1]][labels[k][1]])
 spectral=[]
 for i,j in pairs:
  spectral.append([div(mul(S[i][k],S[j][k]),dims[k]) for k in range(9)])
 Pmat=s.Matrix(9,9,lambda i,j:int(i==permutation[j]));gram=X.T*X;weighted=X.T*Pmat*X
 checks=0
 for p in range(len(pairs)):
  for q in range(p,len(pairs)):
   for ins,target in [(0,gram),(1,weighted)]:
    value=Z
    for k in range(9):value=add(value,scale(mul(spectral[p][k],spectral[q][k]),F(charge[k] if ins else 1,16)))
    need(value==scale(ONE,target[p,q]),'actual Z(Ising) fourth moment');checks+=1
 need(sum(i==j for i,j in enumerate(permutation))==3,'actual fermion fixed objects')
 # Double-semion modular S matrix and an order-two semion generator.
 labels2=list(product(range(2),repeat=2));S2=s.Matrix(4,4,lambda i,j:(-1)**sum(a*b for a,b in zip(labels2[i],labels2[j])))
 pp=list(cwr(range(4),2));X2=s.Matrix(4,len(pp),lambda k,p:int(labels2[k]==tuple(a^b for a,b in zip(labels2[pp[p][0]],labels2[pp[p][1]]))))
 gp=2;perm2=[labels2.index((a^1,b)) for a,b in labels2];J2=s.Matrix(4,4,lambda i,j:int(i==perm2[j]));count2=0
 for p,(i,j) in enumerate(pp):
  for q,(k,l) in enumerate(pp):
   for ins,target in [(0,X2.T*X2),(1,X2.T*J2*X2)]:
    val=sum(S2[i,z]*S2[j,z]*S2[k,z]*S2[l,z]*(S2[gp,z] if ins else 1) for z in range(4))/4
    need(val==target[p,q],'actual double-semion fourth moment');count2+=1
 need(all(S2[gp,perm2[i]]==-S2[gp,i] for i in range(4)),'semion flips monodromy')
 return {'Z_Ising_fourth_moment_identities':checks,'Z_Ising_fixed_fermion_simples':3,'double_semion_fourth_moment_identities':count2}

def main():
 names=['quartic_pair','charged_quartic_pair','involution_pair_gram','higher_moments','integer_pair_completion'];receipts={}
 for name in names:
  obj=read(HERE/(name+'.json'));need(obj['verifier_sha256']==digest(HERE/(name+'.py')),'producer binding '+name)
  for path,sha in obj['source_sha256'].items():need(digest(ROOT/path)==sha,'source binding '+path)
  receipts[name]=obj
 source=read(P/'source.json')['records'];domain=read(P/'gram_cubic.json')['patterns'];charges=read(P/'r941_charges.json')['solutions'];summary=[]
 for rr,rec in enumerate(source):
  semion=rec['id'].endswith('928');V=s.Matrix.hstack(*(s.Matrix((0,)+tuple(v)) for v in rec['canonical_high_vectors'][:40]))
  first=receipts['quartic_pair']['records'][rr];need(first['domain']==343 and first['survivors']==list(range(343)),'complete quartic domain')
  charged=receipts['charged_quartic_pair']['records'][rr];need(len(charged['cases'])==(15 if semion else 93),'complete charged domain')
  by={c['allocation']:c for c in charged['cases']};integer=receipts['integer_pair_completion']['records'][rr]['cases'];unique_counts=[]
  for wit in integer:
   a=wit['allocation'];case=by[a];sec=case['sectors'][0];neg=case['sectors'][1];T=matrix(sec['T']);G=matrix(sec['G'])
   ns=[n//2 for n in domain[case['pattern']][:40]] if semion else charges[a]['plus_pairs']
   if not semion:
    T/=2;G/=2
    invcases=receipts['involution_pair_gram']['records'][rr]['cases']
    invcase=next(z for z in invcases if z['allocation']==a)
    need(invcase['sectors'][0]['antisymmetric_rank']==0 and matrix(invcase['sectors'][0]['antisymmetric_Gram'])==s.zeros(7),'fermion orbit constancy')
   need(wit['outcome']=='exact_integer_witness','integer witness present')
   rebuiltT=s.zeros(*T.shape);rebuiltG=s.zeros(*G.shape);counts=[0]*40
   for row in wit['witness']:
    k=row['type'];n=row['multiplicity'];x=s.Matrix(1,7,row['pair_fusion_coefficients'])
    need(n>0 and all(t>=0 and s.Rational(t).q==1 for t in x),'nonnegative integer witness')
    counts[k]+=n;rebuiltT+=n*V[:,k]*x;rebuiltG+=n*x.T*x
   need(counts==ns and rebuiltT==T and rebuiltG==G,'full exact pair witness')
   need(neg['Hrank']==0,'negative sector rigidity');Xm=matrix(neg['Xtypes'])
   nm=[n//2 for n in domain[case['pattern']][:40]] if semion else charges[a]['minus_individuals']
   need(all(z.q==1 and z>=0 for k,n in enumerate(nm) if n for z in Xm[k,:]),'negative coefficients integral')
   need(V*s.diag(*nm)*Xm==matrix(neg['T']) and Xm.T*s.diag(*nm)*Xm==matrix(neg['G']),'forced negative witness')
   if not semion:
    active=[k for k,n in enumerate(ns) if n];options=[]
    # Independently enumerate the rank-one ellipsoid domain, without the
    # producer's candidates() routine or its stored list of possible rows.
    H=matrix(sec['H'])/2;X0=matrix(sec['Xtypes']);need(H.rank()==1 and H[0,0]>0,'rank-one uniqueness domain')
    for k in active:
     rows=[];x=X0[k,:];bound=int(s.ceiling(x[0]))+math.isqrt(int(s.ceiling(H[0,0])))+2
     for n in range(bound+1):
      delta=n-x[0]
      if delta*delta>H[0,0]:continue
      row=x+(delta/H[0,0])*H[0,:]
      if all(v.q==1 and v>=0 for v in row):rows.append([int(v) for v in row])
     need(rows==wit['rows_by_type'][str(k)],'independent complete row domain')
     options.append(list(cwr(range(len(rows)),ns[k])))
    tested=0;valid=0
    for choices in product(*options):
     tested+=1;TT=s.zeros(*T.shape);GG=s.zeros(*G.shape)
     for k,ixs in zip(active,choices):
      for j in ixs:
       x=s.Matrix(1,7,wit['rows_by_type'][str(k)][j]);TT+=V[:,k]*x;GG+=x.T*x
     valid+=int(TT==T and GG==G)
    need(tested==16 and valid==1,'unique fermion orbit completion');unique_counts.append(tested)
  moments=receipts['higher_moments']['records'][rr];need(moments['maximum_degree']==10,'degree bound')
  need(all(c['tested']==2002 and 'failure' not in c for c in moments['cases']),'complete bounded unit moments')
  need(len(integer)==(10 if semion else 14),'current survivor count')
  summary.append({'id':rec['id'],'exact_pair_completions':len(integer),'negative_sector_residual_rank':0,'unit_moments_per_case':2002,'unique_fermion_completions':len(unique_counts)})
 result={'kind':'targeted_exact_pair_receipt_review','controls':controls(),'records':summary,'source_sha256':{str((HERE/(n+'.json')).relative_to(ROOT)):digest(HERE/(n+'.json')) for n in names},'verifier_sha256':digest(Path(__file__)),'scope':'Exact arithmetic and control review; categorical applicability is stated separately in PROOF.md.'}
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
