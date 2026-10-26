"""Certify every retained-pair cohomology restriction and frozen-case binding.

The obstruction certificates are independently verifiable vectors y over Z/8:
y*differential=0 and y*(-omega|H)!=0.  Thus a skipped restriction cannot be
trivialized over mu_8.  The independently audited exponent lemma upgrades this
to nontriviality over U(1) for the mu_4 cocycles used here.
"""
from setup import *
from gt_complete_models import s4_cocycles, trivializer
from twisted48_models import schur_cover


def differential(G,H):
    variables=[(a,b) for a,b in itertools.product(H,repeat=2) if a and b]
    triples=list(itertools.product([a for a in H if a],repeat=3))
    vi={ab:i for i,ab in enumerate(variables)}
    A=np.zeros((len(triples),len(variables)),dtype=np.int64)
    for i,(a,b,c) in enumerate(triples):
        for x,y,z in [(b,c,1),(a,G[b][c],1),(G[a][b],c,-1),(a,b,-1)]:
            if x and y:A[i,vi[x,y]]+=z
    return variables,triples,A%8


def row_diagonalization(A):
    """Elementary invertible row/column reduction over Z/8; retain left U."""
    B=A.copy()%8;m,n=B.shape;U=np.eye(m,dtype=np.int64)
    for k in range(min(m,n)):
        choices=[(int(B[i,j]&-B[i,j]),i,j)
                 for i in range(k,m) for j in range(k,n) if B[i,j]]
        if not choices:break
        d,i,j=min(choices)
        B[[k,i]]=B[[i,k]];U[[k,i]]=U[[i,k]]
        B[:,[k,j]]=B[:,[j,k]]
        inv=pow(int(B[k,k]//d),-1,8)
        B[k]=(B[k]*inv)%8;U[k]=(U[k]*inv)%8
        common.require(B[k,k]==d,'normalized pivot')
        for i in range(k+1,m):
            common.require(B[i,k]%d==0,'pivot divides column')
            q=B[i,k]//d
            B[i]=(B[i]-q*B[k])%8;U[i]=(U[i]-q*U[k])%8
        for j in range(k+1,n):
            common.require(B[k,j]%d==0,'pivot divides row')
            q=B[k,j]//d;B[:,j]=(B[:,j]-q*B[:,k])%8
    diagonal=np.array([B[i,i] if i<n else 0 for i in range(m)])
    D=np.zeros_like(B)
    for i in range(min(m,n)):D[i,i]=diagonal[i]
    common.require(np.array_equal(B,D),'diagonal form')
    return diagonal,U


def main():
    ps,S,vs=s4_cocycles();ps0,S0,beta=schur_cover()
    common.require(ps==ps0 and S==S0,'S4 coordinates')
    parity=[sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2 for p in ps]
    pi={p:i for i,p in enumerate(ps)}
    pairs=json.loads((OUT/'h8_pairs.json').read_text())+json.loads((OUT/'h4_pairs.json').read_text())
    frozen=json.loads((OUT/'gt_classification_frozen.json').read_text())
    def ckey(gi,hi,bits,ex,cl):return (gi,hi,tuple(bits),tuple(ex),cl)
    fcases={ckey(int(c['group_key']),c['parameters']['subgroup_index'],c['parameters']['transfer_bits'],c['parameters']['extra'],c['parameters']['schur_class']):c for c in frozen['cases']}
    common.require(len(fcases)==len(frozen['cases']),'unique parameter cases')
    certificates=[];used=set();counts={'admissible_restrictions':0,'inadmissible_restrictions':0,'frozen_categories':0}
    for gi in [28,29,30,48]:
        fam=[r for r in pairs if r['smallgroup'][1]==gi];G=fam[0]['table']
        pr=np.array([pi[tuple(x-1 for x in p)] for p in fam[0]['projection_permutations']])
        q=np.array(fam[0]['quotient_character']);B=np.array(beta)[pr[:,None],pr[None,:]];sg=np.array(parity)[pr]
        cache=[]
        for row in fam:
            variables,triples,A=differential(G,row['subgroup']);d,U=row_diagonalization(A)
            cache.append((variables,triples,A,d,U))
        extras=list(itertools.product(range(2),repeat=3)) if gi==48 else [(k,) for k in range(4)] if gi==30 else [()]
        for bits,V in vs:
            base=2*V[pr[:,None,None],pr[None,:,None],pr[None,None,:]]
            for ex in extras:
                W=base.copy()
                if gi==48:
                    W+=4*(ex[0]*q[:,None,None]*q[None,:,None]*q[None,None,:]+ex[1]*sg[:,None,None]*q[None,:,None]*q[None,None,:]+ex[2]*q[:,None,None]*B[None,:,:])
                elif gi==30:W+=2*ex[0]*q[:,None,None]*((q[None,:,None]+q[None,None,:])//4)
                W%=8
                for hi,row in enumerate(fam):
                    H=row['subgroup'];variables,triples,A,d,U=cache[hi]
                    rhs=np.array([-int(W[a,b,c])%8 for a,b,c in triples]);urhs=U@rhs%8
                    bad=next((i for i in range(len(d)) if urhs[i]%(int(d[i]) or 8)),None)
                    rec=dict(smallgroup=gi,subgroup_index=hi,transfer_bits=bits,extra=ex,omega_sha256=digest(W.tolist()))
                    p0=trivializer(G,H,W)
                    if bad is not None:
                        y=(U[bad]*(8//int(d[bad]) if d[bad] else 1))%8
                        common.require(np.all(y@A%8==0),'certificate annihilates differential')
                        residue=int(y@rhs%8);common.require(residue!=0,'certificate detects nonzero class')
                        common.require(p0 is None,'independent obstruction agrees with original solver')
                        rec.update(admissible=False,obstruction=y.tolist(),nonzero_pairing=residue)
                        counts['inadmissible_restrictions']+=1
                    else:
                        common.require(p0 is not None,'independent diagonal test agrees with solver')
                        pv=np.array([p0[a,b] for a,b in variables]);common.require(np.all((A@pv-rhs)%8==0),'positive trivializer')
                        rec.update(admissible=True,trivializer=pv.tolist(),frozen_cases=[])
                        counts['admissible_restrictions']+=1
                        for cl,P in enumerate(row['schur_cocycles']):
                            key=ckey(gi,hi,bits,ex,cl);common.require(key in fcases,'complete frozen case coverage');c=fcases[key];used.add(key)
                            psi=[[(p0[a,b]+4*P[i][j])%8 for j,b in enumerate(H)] for i,a in enumerate(H)]
                            common.require(c['subgroup']==H and c['psi']==psi,'exact relative cocycle binding')
                            common.require(c['omega_key']==str(gi)+':'+digest(W.tolist()),'exact associator binding')
                            common.require(frozen['groups'][str(gi)]==G,'group binding')
                            common.require(frozen['cocycles'][c['omega_key']]==W.tolist(),'actual associator table binding')
                            rec['frozen_cases'].append(c['case']);counts['frozen_categories']+=1
                    certificates.append(rec)
    common.require(used==set(fcases),'every frozen case and no extras')
    common.require(len(certificates)==432 and counts['frozen_categories']==92,'expected bounded coverage size')
    result=dict(status='PASS',modulus=8,counts=counts,total_restrictions=len(certificates),cases=certificates)
    (OUT/'restriction_certificates.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
