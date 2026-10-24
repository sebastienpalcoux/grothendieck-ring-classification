# Independent central-indicator checks for R1154 and R1768

These checks give **no new exclusion**. Their purpose is to test a
potentially stronger categorical constraint on the already forced full
packet/Weil fusion data, rather than run another relaxation of unknown
source twists.

The categorical inputs are Ng–Schauenburg, *Frobenius–Schur indicators
and exponents of spherical categories*,
[arXiv:math/0601012](https://arxiv.org/pdf/math/0601012), Theorems 4.1 and
7.5. Write `D=Dim(C)` for a source category and use its positive spherical
normalization. The global dimension of its center is `D^2`. Put
`v_n=(d_Z theta_Z^n)_Z`. With the row-input convention for a fusion matrix
`N_X`, Frobenius reciprocity rewrites Theorem 7.5 as

```
              nu_n(X) = D^-2 v_(-n)^t N_X v_n.
```

The adjoint-indicator identity also gives `M v_n=D nu_n`, where `M` is
the source-by-center restriction matrix. At n=2 the source vector is
real, and the modular formula is consequently a real quadratic form.

## R1154: all100 packet identities pass

For each of the four packet objects, the previous exact reconstruction
has `4N_Z=J+K`, with `J=M^t N_g M`. Every nonzero entry of `K` is on the
four known twist-one low simples and the four semionic packet simples.
Their twist squares are respectively +1 and -1. Direct exact calculation
on all25 remaining histograms gives

```
                v_(-2)^t K v_2=0.
```

Write the source second-indicator vector as
`nu=(1,0,0,-1,a,b,c,d)`. The based permutation of the source invertible
is `(0 3)(1 7)(2 6)(4 5)`, hence

```
  4 nu_2(Z) = nu^t N_g nu = -2+2ab.
```

Each packet object is nonselfdual, so `nu_2(Z)=0` and `a=b`. The previous
exact source rotation constraints already force `b=c=d=1` and exclude
the remaining negative value of `a`. This is therefore an independent
consistency proof of an existing sign, not a new reduction.

## R1768: the18-object branch passes

Set `s=sqrt(37)`, `u=6+s`, `a=u^2`, `d=12u`, `q=su`, and `D=12su`.
The forced center contains `1`, `alpha` of dimension `a`, and18 simples
`Z_k` of dimension `d`, one at each nonsquare primitive37 twist. All
other simples have dimensions `t_Y q`.

The source indicators are `(1,-1,1,1,1,1,1,1)`. Thus the center twist
square Gauss sum is `D(6u)`. Since2 is a nonsquare modulo37,

```
 sum_(k nonsquare) zeta^(2k)=(-1+s)/2,
 sum_Y t_Y^2 theta_Y^2=-2.
```

Let `B_kl=s s_(Zk,Zl)` be the previously forced Weil block. Parameterize
`k=2b^2,l=2c^2`, so `B_kl=-(zeta^(4bc)+zeta^(-4bc))`. Completing the
finite square gives

```
 sum_k zeta^(2k) B_kl = 1-s zeta^(-l/2).
```

The verifier checks each of these18 identities in `Q[zeta_37]`, using
the quadratic Gauss sum for `s`. Consequently the projections of `v_2`
onto the normalized S columns for `1,alpha,Z_l` are respectively

```
          6u,   -6u,   -12u zeta^(-l/2).
```

The relevant fusion eigenvalues for `Z_k` are `d,-d/a,B_kl,0` on
`1,alpha,Z_l,Y`. The row sum of `B` is one. Its second indicator is
therefore

```
 nu_2(Z_k) = [36u^2 d(1-1/a)+144u^2]/D^2 = 1.
```

For `alpha` the eigenvalues are `a,1/a,-1,1`; completeness of the
orthonormal S columns yields

```
 nu_2(alpha)=1+[36u^2(a+1/a-2)-2*18*144u^2]/D^2=1.
```

These are valid indicators for the forced selfdual objects. No
contradiction occurs. This calculation concerns only the18-object
branch; it does not silently discard the72-object branch.

Run `python verify_indicator_checks.py`. The saved receipt is
`indicator_checks.json`; the script does not alter the published sources.
