# Independent direct audit of conjugation-pairing exclusion for R1768

29 October 2026. **The new categorical lemma is valid.** Combined with the
previously accepted complete positive indicator restriction, it contradicts
R1768 categorifiability. This audit verifies the new lemma and its tensor
application directly; the inherited indicator and general-complex reduction
premises remain separately identified below.

## 1. Direct pivotal proof, with no Morita or Frobenius-functor premise

Let C be a pivotal fusion category over C. By pivotal strictification we may
assume the tensor product, the duality tensor constraints, and the pivotal
isomorphism are strict. In particular **=Id and (UV)*=V*U* literally.
This is Ng--Schauenburg, *Higher Frobenius-Schur Indicators for Pivotal
Categories*, Theorem 2.2, arXiv:math/0503167.

Let Y be a selfdual simple, and choose an isomorphism f:Y->Y*. Its pivotal
transpose is f*, and f*=epsilon f, with epsilon=nu_2(Y) in {1,-1}.
For an arbitrary object X put V=X tensor Y tensor X*. Then

    V* = X tensor Y* tensor X*,
    q = id_X tensor f tensor id_X* : V -> V*.

The map q is an isomorphism, and reversing the three tensor factors under
duality gives exactly

    q* = id_X tensor f* tensor id_X* = epsilon q.

There is no scalar, FP-dimension factor, choice of a selfduality on X, or
braiding in this calculation. Thus V has a nondegenerate epsilon-symmetric
selfduality. Pivotal equivalence transports this statement back from the
strict model. Neither pseudo-unitarity nor a Frobenius-monoidal forgetful
functor is needed for the lemma itself.

If a selfdual simple Z with nu_2(Z)=delta occurs in V with multiplicity m,
choose its selfduality p:Z->Z*. On the Z-isotypic block, q is p tensor M for
an invertible m by m complex matrix M. The transpose relation reads

    delta M^t = epsilon M.

If epsilon=-delta, M is alternating and m must be even. Consequently

    [Z : X tensor Y tensor X*] odd  =>  nu_2(Z)=nu_2(Y)

for selfdual simple Y,Z. This is a necessary condition on every pivotal
fusion category, not a functorial preservation assertion about numerical
indicators of general objects.

## 2. Independent R1768 arithmetic

I read the frozen source tensor independently of the candidate checker.
All eight source simples are selfdual. Direct integer multiplication gives

    X2 g X2* = g+2X2+2X3+2X4+2X5+X6+X7,

with g=X1. The published positive indicator vector is

    (1,-1,1,1,1,1,1,1).

Taking Y=g and Z=X6 (or X7), the product has odd multiplicity one but
opposite indicator signs, contradicting the lemma. The exact vector was
computed as sum_t N[2][1][t] N[t][2][k], yielding
(0,1,2,2,2,2,1,1).

## 3. Dependency caution

The source ring alone does not force all six nonpointed indicators positive.
I independently computed the complete parity graph whose vertices are the
selfdual simples and whose edges record odd multiplicity in some Xi Y Xi*.
It has precisely two connected components:

    {0,2,3,5},     {1,4,6,7}.

The first has sign +1 because it contains the unit. The second could have
sign -1 from this graph alone. Therefore a proof must retain the earlier
complete theorem forcing +1 on X4,X6,X7; it cannot silently derive those
signs from this new ring calculation. The accepted forty-branch saturated
Galois/indicator analysis is the stated source of that premise.

Similarly, general complex exclusion uses the established reduction from
arbitrary complex categorification to a positive pivotal representative.
The direct new lemma handles that representative. It does not assert that
an arbitrary original fusion category is already pseudo-unitary.

## 4. Other current cases

For comparison, the same complete finite triple-product test gives no parity
contradiction for the accepted indicator vectors of R1154, R1660, R941, or
R928. This was checked directly from their frozen source tensors. It does
not decide those cases.

## Primary reference checked

Ng, Schauenburg, *Higher Frobenius-Schur Indicators for Pivotal Categories*,
Theorem 2.2 (strictification of both duality and pivotal structure),
https://arxiv.org/abs/math/0503167 . The map q and the multiplicity-parity
argument above are proved explicitly, rather than inferred from that
reference or from earlier Morita-pairing claims.
