# Actual near-group centralizer: partial fusion without numerical S identification

This is the first input to the new R8_2_820/R8_2_869 audit bridge. It uses Evans–Gannon §4.3 (actual tube algebra), not the candidate formula or numerical identification of §4.4.

Let N be either actual C5+5 unitary near-group category with pairing parameter m=1 or2. Put a=(5+3√5)/2, b=a+1, c=a+2, and D=45b. EG equations (4.49)–(4.51) give five actual invertible center objects a_g, with nondegenerate restricted pairing ζ5^(-2mgh). They form a nondegenerate pointed category P. Hence the actual unitary center decomposes as P⊠B, where B=P′ is unitary modular. The actual tube decomposition has40 simple summands, so B has8 simples. This rank calculation does not use candidate Γ labels or assume any D object is self-dual.

The actual known non-D-D blocks in EG (4.57) identify four of these objects as a_0,b_0,c_{1,-1},c_{2,-2}; call them 1,B,C1,C2. They are self-dual by uniqueness of the half-braidings for their underlying objects (or the actual duals a_g→a_-g, b_g→b_-g, c_kl→c_-k,-l). The remaining four objects are of actual d type, all of dimension a. Equivalently, tensoring by a_g shifts a d object's monodromy character by the nondegenerate C5 pairing, so the20 actual d objects split into five monodromy classes of four each. Denote the four trivial-monodromy objects D1,…,D4, allowing an arbitrary duality involution among them.

Let M be the **actual** unnormalized S matrix of B. Its known columns 0,B,C1,C2 follow from EG (4.57); in the basis (1,B,C1,C2,D1,…,D4), they have

- dimension column d=(1,b,c,c,a,a,a,a);
- B column s_B=(b,1,c,c,-a,-a,-a,-a);
- C_k column s_k=(c,c,c(ζ5^(2mk)+ζ5^(-2mk)),c(ζ5^(4mk)+ζ5^(-4mk)),0,0,0,0), for k=1,2.

These columns are real. The D-D block is left entirely unknown. Normalization is M M* = D I: EG's center denominator is Dim(N)=5c, and the pointed-factor decomposition multiplies normalized S by √5, giving B's denominator √D=(5c)/√5. The elementary identity c²=9b checks D.

For any self-dual known object X, ordinary fusion is

\[
(N_X)_{jk}=D^{-1}\sum_l \frac{M_{Xl}}{d_l}M_{jl}\overline{M_{kl}}.
\]

For X=C_k, M_{C_k,D_l}=0, so this sum uses only the four known columns. For X=B, the eigenvalue on every D column is −1. Eliminate their entire unknown contribution by unitarity to obtain

\[
N_B=-I+D^{-1}\left((b+1)dd^t+(1+b^{-1})s_Bs_B^t+2s_1s_1^t+2s_2s_2^t\right).
\]

This proves N_B,N_C1,N_C2 exactly without using any D-D entry, any individual D twist, any candidate group Γ, or any unproved D self-duality. `rank8-ng-partial-fusion.py` evaluates precisely these formulas over the exact field and confirms the same integer matrices for m=1 and2. It sets every D-D matrix entry to `None` before the calculation, so accidental use of that block would fail. Its receipt is `rank8-ng-partial-fusion.json`. In particular,

\[
BD_i=B+C_1+C_2+\sum_{j\ne i}D_j,
\qquad
C_kD_i=B+C_1+C_2+\sum_jD_j.
\]

The known-known products and all other entries of these three matrices are included in the receipt. Commutativity supplies their transpose products. For two D objects with unknown involution i↦i*, Frobenius reciprocity now fixes

\[
D_iD_j=\delta_{j,i^*}1+(1-\delta_{j,i^*})B+C_1+C_2+
\sum_k n_{ij}^kD_k.
\]

Since a²=5+5a, comparison of exact dimensions yields

\[
\sum_k n_{ij}^k=2+\delta_{j,i^*}.
\]

Thus every remaining coefficient lies in0..3. In lowered notation F_ijk=n_ij^(k*), commutativity and Frobenius reciprocity make F completely symmetric, and duality gives F_i*j*k*=F_ijk. These are exactly the complete domains used by the independent `rank8-neargroup-associativity-classify.py` enumeration. The only involution types on four objects are identity, one transposition and two transpositions; none is silently omitted.

## Independent review of the completion and distinction code

I separately read the complete `rank8-neargroup-associativity-classify.py` driver. It merges precisely the duality orbits of all20 unordered D triples, enforces all10 pair sums with their exact repeated-variable coefficients, and enumerates each nonnegative integral solution. The residual upper bounds and capacity pruning are necessary conditions only; they cannot remove a valid assignment. It reconstructs every8×8×8 ordinary coefficient, checks all multiplication-matrix commutators and all8^4 associativity identities, and checks full duality/Frobenius relations. Its integer operations are far below int64 limits. The resulting two classes are self-dual, identified with the existing two exact candidate tensors **as rings only**. Neither candidate's categorical existence is used here.

I also reviewed `rank8-neargroup-twist-distinction.py` and the mathematical distinction: after that completion theorem, every actual factor S column is one of the eight exact ring characters; the four D columns are exactly those with formal codegree D/a²=9. Hence their possible reorderings are finite. For820, balancing the D_i² rule makes each actual D twist a cube root of unity. For869, S symmetry fixes its unique distinguished D character and forces three actual D diagonal entries divided by a to be real cubic irrationals; balancing would make these rational if every D twist were a cube root. The actual seed third indicators therefore distinguish the two rings, as proved in `rank8_neargroup_seed_indicator.md` and the rank-seven agent's joint bridge note.

This is a replacement argument closing the numerical-identification gap. The old manuscript's reliance on the cited finite numerical S comparison is not itself upgraded by these calculations; the new proof and its source-bound finite classification should be incorporated explicitly before describing the old proof as repaired.
