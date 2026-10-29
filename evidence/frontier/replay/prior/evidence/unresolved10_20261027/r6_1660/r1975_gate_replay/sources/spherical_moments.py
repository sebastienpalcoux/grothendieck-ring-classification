from exact import *
import sympy as s
def positive_sign_embedding(R,f,ds):
    """A signed-positive Galois character gives a positive spherical structure.
    The signs must be a tensor grading, not merely arbitrary basis signs.
    """
    for number,e in enumerate(embeddings(f)):
        signs=[e.sign(d) for d in ds]
        if not all(signs) or signs[0]!=1:continue
        if all(signs[i]*signs[j]==signs[k] for i in range(len(R)) for j in range(len(R)) for k in range(len(R)) if R[i][j][k]):
            return {'kind':'galois_fp_signs','embedding':number,'signs':signs}
    return None
def spherical_global_moment(a,f):
    """The same positive central-square measure for any spherical character.

    At each real embedding replace the unknown second indicators by the
    upper bound S=sum(abs(d_i)) over self-dual i. A violated necessary
    inequality at one embedding excludes the whole Galois orbit.
    """
    K,ds,D,pD=a.component(f);w=s.trace(a.C.inv()**2)
    for number,emb in enumerate(embeddings(f)):
        S=sum((K(emb.sign(ds[i]))*ds[i] for i in range(a.n) if a.du[i]==i),K.zero)
        h=K(w)*D*D
        gap=K(2)*(D-h)**2-(D*D-h)*(D*D+D*S-K(2)*h)
        if emb.sign(gap)>0:
            return {'kind':'spherical_global_moment','inverse_square_sum':str(w),
                    'embedding':number,'S':ec(S),'gap':ec(gap)}
    return None
