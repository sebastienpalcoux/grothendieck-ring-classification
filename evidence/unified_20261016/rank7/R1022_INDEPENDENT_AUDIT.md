# Independent audit: R7_3_1022 via the inverse V4 algebra

Verdict: the categorical argument communicated by rank7_structural passes this independent audit, subject to inclusion of the cited published theorem and the already certified C3–V4 reduction. No unitarity or uniqueness theorem is required.

## Published input and its scope

Andrew Schopieray, *Categorification of integral group rings extended by one dimension*, J. London Math. Soc. 108 (2023), 1617–1641, DOI 10.1112/jlms.12789, Theorem 1.1, states that an elementary abelian 2-group supports a categorifiable near-group ring only at level zero, at levels one or two for C2, or at level four for C2×C2. In particular the ring R(V4,8) has no complex fusion categorification. This was checked directly in the published primary-source HTML, lines106–110, on16October2026. The theorem is not restricted to unitary categories.

## The algebraic commutation-cocycle obstruction

Let E have untwisted pointed part Vec_V4 and the free-orbit rules rho h=h rho, rho²=1+sum_h h rho. Choose coherent pointed multiplication and commutation maps; their scalar defect is a2-cocycle xi onV4. If its class is nontrivial, letA=sum_hh be the separable regular algebra. The endomorphism algebra of the induced A-bimodule A rho A is the twisted group algebra C^xi[V4], which isM2(C). Equivalently, the noninvertible double orbit has a single simple A-bimodule sigma whose underlying object has dimension8d, so its Morita-dual dimension is2d. The pointed double orbit gives four invertibles, the characters ofV4. Thus the entire dual has four invertibles and one noninvertible. Since d²=1+4d, its fusion rule is sigma²=sum_chi chi+8sigma. This contradicts the published theorem. Therefore[xi]=0.

This is the same calculation appearing in Izumi, arXiv:1609.07604, Proposition9.6, pp62–63, but it uses only a separable finite-group algebra, projective representations, rigidity, and FP dimensions. The algebraic proof above removes the C*-realization from that calculation.

## The inverse algebra really is V4-supported

The earlier certified reduction gives D with twelve invertibles A4 and three noninvertibles of dimension2t, and an algebra B on its normalV4 subgroup such that E=D_B^* has twelve invertibles A4 and twelve noninvertibles of dimensiont. Here t=2+sqrt5. The pointed category of E is untwisted Vec_A4, and its surviving based-ring rules are rho g=g rho and rho²=1+sum_{h inV4}h rho.

Use the distinguished simple rightB-module m=B. Its internal end in E has the multiplicity of an E-simple B-bimodule X given by

    dim Hom_{rightB}(B,X)=dim Hom_D(1,X).

Exactly four invertible B-bimodules have underlying support on the identityV4 coset. Each has underlying object B and contains1 once; every other simple has support avoiding1. Therefore the inverse internal-end algebra Q is precisely the sum of those four invertibles. They form the uniqueV4 in E_pt=A4. This argument works for either algebra2-cocycle onB.

## Twist cancellation and all three noninvertible orbits

Let beta be either algebra2-cocycle onQ. A noninvertible orbit represented by g rho has stabilizer inV4×V4 equal to the graph of Ad_g (up to the harmless convention of inverses). Its effective projective class is

    [xi|V4]+[beta]−Ad_g^*[beta].

Every automorphism ofV4 acts trivially on H²(V4,C*)=C2. Hence the beta terms cancel even when g lies outsideV4. The commutation-cocycle obstruction makes the remaining class zero. Each of the three orbits consequently has four one-dimensional stabilizer representations. Its four simple Q-bimodules each have underlying FP dimension4t and dual dimensiont. The inverse Morita dual therefore has twelve noninvertibles of dimensiont.

But the inverse Morita dual is D, whose certified dimensions are three noninvertibles of dimension2t. This contradiction excludes the hypothetical source categorification of R7_3_1022.

## Scope and checks

The rank8 V4 subcategory used above is identified solely by the fusion rules and the untwisted pointed associator proved in the earlier reduction. No equivalence to a known Haagerup–Izumi realization is assumed. The only external classification input is the unrestricted near-group theorem. Both the support calculation forQ and the cancellation under conjugation were checked independently; the latter is essential and must not be replaced by an unqualified assertion that all orbits have identical stabilizer maps.
