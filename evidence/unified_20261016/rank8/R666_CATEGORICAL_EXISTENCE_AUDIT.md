# Independent categorical-existence audit for R8_2_666

Audit by the rank6-center agent, 2026-10-16. Scope: the actual categorical existence of the ambient rank-28 modular category used by `C4_CENTRALIZER_PROOF.md`; the separate exact tensor replay belongs to that proof and its verifier.

## Primary source check

I independently opened and read Grossman–Izumi, *Infinite families of potential modular data related to quadratic categories*, arXiv:1906.07397v2, section 3.2.3.1, PDF page 21. The paragraph on the smallest example identifies the two choices with G=C4×C4 and Gamma=C16×C2, r=±3, as the Drinfeld-center modular data of the two complex-conjugate near-group C4 categories with multiplicity 4. It explains that the identification uses Izumi (2001), Theorem 6.8, equations (6.18)–(6.21), and the explicit structure constants in Example A.2.

This is an assertion about existing categories, distinct from the following conjecture for the larger odd-factor family. The title and the potential-data scope of other parts of the paper do not make this smallest example conjectural.

Source: https://arxiv.org/pdf/1906.07397

I independently checked Bonderson–Rowell–Wang, *On Realizing Modular Data*, arXiv:1910.07061, section 2.4.1, PDF page 4. The authors explicitly attribute categorical existence of the hyperbolic choices to Grossman–Izumi using Izumi (2001). They then select precisely the parameters used in the proposed model:

- G=C4×C4, theta_G(x,y)=(y,x), q_G(x,y)=i^(-xy).
- Gamma=C16×C2, theta_Gamma(x,y)=(3x+8y,x+y), q_Gamma(x,y)=zeta_32^(3x²)i^(y²).

The compatible elliptic form mentioned nearby is not needed. The present model uses only the verified hyperbolic form.

Source: https://arxiv.org/pdf/1910.07061

## The subcategory is categorically defined

Starting from the actual unitary Drinfeld center C, take its full pointed fusion subcategory P and its Müger centralizer B=P-prime. A centralizer in a unitary braided fusion category is again a unitary braided fusion category. Thus B exists before any recognition of its fusion tensor. BRW section 2.4.2 also explicitly lists the same eight labels as the proposed proof.

The pointed metric group is K=C4 with q(k)=i^(-k²). Its radical is {0,2}, whose twists are both 1; hence the Müger center of B is Tannakian of order two. In particular the argument does not require B itself to be modular. Verlinde is applied in the existing ambient modular category C and then restricted to the centralizer, which is legitimate.

## Conclusion

The categorical-existence premise of the R666 construction passes this independent audit. It is not an inference that every admissible modular datum is realizable. It uses a specific published identification with a known unitary near-group center. Given the separate exact full-tensor comparison in `verify_c4_centralizer.py`, this supplies an actual unitary braided categorification of R8_2_666.
