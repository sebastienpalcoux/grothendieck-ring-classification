"""All based rings of dimension type1^4,2² admitting a swap of the2D simples.

Products with invertibles are permutation actions. Frobenius reciprocity fixes
every invertible coefficient; only the indicated tiny compositions of0,1,2
remain. This is an exact proof of a finite ring lemma, not an F-symbol search.
"""
from setup import *

def main():
    records=[];summaries=[]
    for name,G in [('C4',[[(a+b)%4 for b in range(4)]for a in range(4)]),('V4',[[a^b for b in range(4)]for a in range(4)])]:
        chars=[(0,)+v for v in itertools.product(range(2),repeat=3) if all(((0,)+v)[G[a][b]]==(((0,)+v)[a]+((0,)+v)[b])%2 for a,b in itertools.product(range(4),repeat=2))]
        autos=[(0,)+p for p in itertools.permutations(range(1,4)) if all(((0,)+p)[G[a][b]]==G[((0,)+p)[a]][((0,)+p)[b]] for a,b in itertools.product(range(4),repeat=2))]
        tried=valid=swappable=0
        for L,R,d in itertools.product(chars,chars,range(2)):
            star=[next(b for b in range(4) if G[a][b]==0)for a in range(4)]+[4+d,5-d]
            N=np.zeros((6,6,6),dtype=np.int64)
            for a,b in itertools.product(range(4),repeat=2):N[a,b,G[a][b]]=1
            for a,t in itertools.product(range(4),range(2)):
                N[a,4+t,4+(t^L[a])]=1;N[4+t,a,4+(t^R[a])]=1
            choices=[]
            for i,j in itertools.product(range(4,6),repeat=2):
                for g in range(4):N[i,j,g]=N[g,star[j],i]
                rem=4-int(sum(N[i,j,:4]))
                if rem<0 or rem%2:break
                choices.append([(a,rem//2-a)for a in range(rem//2+1)])
            if len(choices)!=4:continue
            for vals in itertools.product(*choices):
                tried+=1
                for (i,j),v in zip(itertools.product(range(4,6),repeat=2),vals):N[i,j,4:]=v
                if not all(N[i,j,k]==N[star[i],k,j]==N[k,star[j],i] for i,j,k in itertools.product(range(6),repeat=3)):continue
                if not all(N[star[j],star[i],star[k]]==N[i,j,k]for i,j,k in itertools.product(range(6),repeat=3)):continue
                if not np.array_equal(np.einsum('ijm,mkl->ijkl',N,N),np.einsum('jkm,iml->ijkl',N,N)):continue
                valid+=1;swaps=[]
                for a in autos:
                    p=list(a)+[5,4]
                    if all(p[p[i]]==i for i in range(6)) and np.array_equal(N,N[np.ix_(p,p,p)]):swaps.append(p)
                if not swaps:continue
                swappable+=1
                expected=np.zeros((6,6,6),dtype=np.int64)
                for a,b in itertools.product(range(4),repeat=2):expected[a,b,G[a][b]]=1
                for a,t in itertools.product(range(4),range(4,6)):expected[a,t,t]=expected[t,a,t]=1
                expected[4,4,5]=expected[5,5,4]=2;expected[4,5,:4]=expected[5,4,:4]=1
                common.require(np.array_equal(N,expected),'every swappable ring is R3,G')
                records.append(dict(group=name,tensor=N.tolist(),dual=star,swapping_automorphisms=swaps))
        summaries.append(dict(group=name,dimension_compatible_tables=tried,based_ring_tables=valid,swappable_tables=swappable))
    result=dict(status='PASS',summaries=summaries,records=records,categorical_consequence='Jordan-Larson Theorem1.4 permits R3,G of grouporder4 only forG=V4')
    (OUT/'rank6_swap_rings.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(summaries))

if __name__=='__main__':main()
