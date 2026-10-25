# Exact third-indicator bridge for the two C5+5 seeds

This is an unpublished audit derivation, not a change to a repository classification. It uses the actual near-group rotation operators and the exact part of their tube inventory; it does not identify a numerical S matrix with a candidate matrix.

Put `zeta=exp(2πi/5)`, `w=exp(2πi/3)`, and

\[
a=(5+3\sqrt5)/2,\qquad b=a+1,\qquad c=a+2.
\]

The two actual C5+5 seeds have bicharacter `⟨g,h⟩=zeta^(mgh)` and scalar parameter `c_seed`, respectively `(m,c_seed)=(1,-1)` and `(2,w)`. Their existence is the published near-group construction, not a consequence of any proposed center matrix.

## 1. Third indicator from the actual seed

[Izumi, arXiv:1512.04288v2](https://arxiv.org/pdf/1512.04288v2), Remark 3.11, pp22–23, identifies `ν3(ρ)` with the trace of `j1∘j2`. Section 9, printed p70, gives the anti-linear operators

\[
j_1(T_h)=a_m(h)T_{-h},\qquad
j_2(T_h)=\frac{\overline{c_{\rm seed}}}{\sqrt5}
 \sum_k\overline{\langle h,k\rangle}T_k,
\qquad a_m(h)=\zeta^{2mh^2}.
\]

The bars in the second formula were checked on a rendered copy of the primary PDF; they are lost by ordinary text extraction. Because both maps are anti-linear, their composition has trace

\[
\nu_3(\rho)
=\frac{c_{\rm seed}}{\sqrt5}
  \sum_{h\in C_5}\langle h,h\rangle^{-1}a_m(h)
=\frac{c_{\rm seed}}{\sqrt5}\sum_h\zeta^{mh^2}
=c_{\rm seed}\left(\frac m5\right).
\]

Therefore the two values are `−1` and `−w`, respectively. The exact script also checks that the five-by-five rotation matrix has cube equal to the identity in both cases. The apparent dimension typo in Example 13.8 is not used; `a²=5+5a` fixes the dimension.

## 2. Actual factor and known center objects

Use the actual tube inventory and twists in [Evans–Gannon, arXiv:1208.1500v1](https://arxiv.org/pdf/1208.1500v1), §4.3, equations (4.49)–(4.57), pp44–45. The five invertible center objects form a nondegenerate pointed category `P`, since their bicharacter has nonzero coefficient `2m` modulo5. Thus

\[
Z(\mathcal N)\simeq\mathcal P\boxtimes\mathcal B
\]

for an actual unitary modular category `B`. The center has40 simples, so `B` has8. Four factor simples are the known objects `1,B,C1,C2`, of dimensions `1,b,c,c` and twists `1,1,zeta^(-m),zeta^(-4m)`. The other four, denoted `D1,…,D4`, have dimension `a`; write their unknown actual twists as `t1,…,t4`. Their unknown S block and individual twists are not assumed.

The forgetful images of the center's b, c, and d types contain `ρ` once, whereas the invertible a types do not. Tensoring a factor object by the five objects of `P` produces a free orbit and multiplies twists by `zeta^(mg²)`. This determines the trace contribution of each orbit without any unknown S entries.

## 3. Induction gives the required exact twist moment

[Ng–Schauenburg, arXiv:math/0601012v3](https://arxiv.org/pdf/math/0601012v3), Theorem 4.1 and (4.2)–(4.3), printed p10, gives

\[
\nu_3(\rho)=\frac1{\operatorname{Dim}\mathcal N}
 \sum_{Z\in\operatorname{Irr}Z(\mathcal N)}
 [F(Z):\rho]\,\dim(Z)\,\theta_Z^3.
\]

Here `Dim N=5c`. Define

\[
G_3(m)=\sum_{g=0}^4\zeta^{3mg^2}
=\left(\frac{3m}5\right)\sqrt5,\qquad
L_3(m)=\zeta^{-3m}+\zeta^{-12m}.
\]

The ten unordered c-type pairs can be parametrized by `k=u+t,l=u−t`, with `u∈C5` and `t∈{1,2}` modulo sign. Consequently their twist-cube sum is `G3(m)L3(m)`. The exact induction formula becomes

\[
\nu_3(\rho)=\frac{G_3(m)}{5c}
 \left(b+cL_3(m)+a\sum_{i=1}^4t_i^3\right).
\]

Substituting the two exact rotation traces yields

\[
\boxed{\sum_{i=1}^4t_i^3=4\quad\text{for the first seed}},
\qquad
\boxed{\sum_{i=1}^4t_i^3=1+3w^2\quad\text{for the second seed}}.
\]

If the opposite ribbon convention is used consistently, all nonreal values are conjugated; the first equality and the second inequality with4 remain unchanged. Since the factor is unitary, each `|ti|=1`. The first equality therefore forces every `ti³=1` by equality in the triangle inequality. The second seed cannot have all four cube equal to1.

## 4. Exact arithmetic receipt and remaining joint proof inputs

`rank8_neargroup_seed_indicator.py` verifies all displayed algebraic identities over `Q[x]/Phi15(x)`, with `zeta=x³`, `w=x⁵`, and the positive real `sqrt5=1+2(x³+x^(-3))`. It reconstructs the actual anti-linear rotation matrices, checks50 rotation-cube entries in total, checks the unordered c-orbit sum directly, and checks both induction identities. It imports neither a census tensor nor either candidate modular matrix. The receipt is `rank8_neargroup_seed_indicator.json`.

This calculation supplies the seed-distinguishing input to the separate exact partial-fusion/associative-completion argument. By itself it does not classify the possible factor fusion rings. To complete that route, independently establish the partial fusion rules, the exhaustive list of associative completions, and the balancing constraints distinguishing those completions. Those parts are being audited by the rank-seven and rank-nine agents.
