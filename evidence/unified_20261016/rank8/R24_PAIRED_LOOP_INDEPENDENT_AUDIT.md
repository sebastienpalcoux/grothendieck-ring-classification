# Independent audit of the R24 paired-loop covariance

Status: PASS for the explicitly normalized paired-loop/right-bend step in
the current `R24_MINIMAL_DUAL_BRIDGE_DRAFT.md`. This audit is deliberately
restricted to that categorical step. The restricted coefficient/resolution
identities and the downstream normalizer argument have separate audits.

The audited version allows arbitrary decorated cubic eigenphases and does
not compare the two orders of incoming cubic rotation. The earlier claim
that these phases must coincide is not used or approved by this audit.

## Opposite Hom spaces and the contragredient action

Write F=Ad(g), A=r and B=r or gr. Use the canonical pivotal structure of
this tensor autoequivalence. All object-identification transposes below
are relative to that structure; they are not transposes relative to an
arbitrarily chosen self-duality on the palindrome gXg. In particular the
unit identification q_1=ev_g has defect one.

For H+=Hom(A tensor A,B) and H-=Hom(B,A tensor A), use the nondegenerate
composition pairing. Suppressing F's tensorator, the two operators induced
by fixed simple-object identifications q_A and q_B are

    T+(f)=q_B F(f)(q_A^-1 tensor q_A^-1),
    T-(h)=(q_A tensor q_A)F(h)q_B^-1.

The tensorator and its inverse cancel when these morphisms are composed.
Since F fixes scalar endomorphisms of the simple B, the composition pairing
obeys <T+ f,T- h>=<f,h>. Thus the matrix of T- in the composition-dual basis
is exactly (T+)^-t. This is a contragredient action, not the ordinary
pivotal transpose of the outgoing operator. Confusing these two operations
would be an error; the current proof explicitly distinguishes them.

## Pivotal form defects and the two signs

Let s_X denote the form defect of q_X, so in these normalized pivotal
identifications q_X^t=s_X q_X^-1. Transposing the displayed formula for
T+ reverses its compositions and gives

    R T+ = (s_B/s_A^2) T- R,

where R is the right pivotal bend between the opposite Hom spaces. This
identity is an ordinary linear transpose calculation. It introduces no
complex conjugation of an eigenvalue or coefficient.

For the normalized crossing c:g r -> r g, the object maps are

    q_r=(id_r tensor ev_g)(c tensor id_g),
    q_gr=id_g tensor q_r.

I compared these contractions against the oriented crossing and self-dual
form conventions on published EIP p506, including Definition 3.2, and
the loop diagrams on p507. In the first map the adjacent g evaluation and
coevaluation cancel; the residual two-crossing diagram is precisely the
defining mu diagram. Passing to q_gr reverses one further g self-dual
form. Its scalar is lambda_g. Hence

    s_r=mu,       s_gr=mu lambda_g.

This calculation uses the normalized crossing's pivotal rotation/inverse
relation and the antisymmetry of the g form. It does not use an adjoint
or a positive Hermitian form. With mu=1 and lambda_g=-1 it gives the plus
covariance on H and the minus covariance on J. The outgoing loop squares
are the same direct g-loop contractions as in EIP: K_H²=-I, K_J²=I.

## Consequences for the right-bend eigenbasis

The right theta pairings are nondegenerate by rigidity and composition
duality. Transposing their two vertices gives their symmetry, because the
incident self-duality signs of r and gr are all +1. The covariance above
says that K_H preserves its symmetric pairing while K_J negates its
symmetric pairing. Therefore K_H's +i and -i eigenspaces pair only with
each other, and K_J's +1 and -1 eigenspaces pair only with each other.
Nondegeneracy and dimension two force each eigenline to occur once.

Rescaling paired eigenvectors makes the right-bend matrix
E=[[0,1],[1,0]] in both channels. The incoming loop matrices are then
diag(-i,i) and diag(1,-1), respectively. The residual basis changes are
diag(u,u^-1) and diag(v,v^-1). These conclusions are bilinear statements
over C and do not imply or assume a C*-structure.

The right-bend step therefore supports the current minimal coefficient
argument. No equality of decorated cubic phases, no symmetric left-bend
pairing, and no incoming cubic-rotation order identity is claimed here.

## Additional independent check of the retained diagonal indices

I also checked the three retained contractions against the published EIP
p539 display and its source indices. Given the paired-slot table, its
first resolution at (k,l,k',l')=(0,0,0,0) is

    1=2 r0^2+2 xX-(2-sqrt(5)).

The third resolution at that tuple pairs the lower columns 00 and 11,
and is 1=2(xX+zZ). At (0,1,0,1), it pairs columns 01 and 10 and is
1=2(xX+yY). Both lower indices are complemented in the second term;
this is important for reproducing the two separate equations. The two
retained even diagonal D flips have i=k, so each decorated phase cancels
on its own as omega_i^3=1. Their use does not require the two decorated
phases to coincide.
