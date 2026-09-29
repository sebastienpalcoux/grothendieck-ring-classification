# Half-E6 control for the nonreal cubic indicator

Primary source: T. J. Hagge and S.-M. Hong, *Some non-braided fusion
categories of rank 3*, arXiv:0704.0208v2, Section 8 and Appendix A:
https://arxiv.org/pdf/0704.0208

Their objects satisfy y^2=1, yx=xy=x, x^2=1+y+2x.
Appendix A gives the mixed associator a^x_{y,x,y}=-1 and the
trivalent rotation block

    B = exp(7*pi*i/12)/sqrt(2) * [[1,i],[1,-i]].

Section 8 identifies this block with bending the trivalent vertex and
establishes the strict pivotal structure. Consequently its trace is

    Tr(B)=exp(pi*i/3)=-zeta_3^2.

The complex-conjugate realization has trace -zeta_3. Reversing the
rotation convention interchanges these two values. In either convention
Re(nu_3(x))=1/2. Direct multiplication gives B^3=I. The coefficient may
be written ((1-sqrt(3))+i*(1+sqrt(3)))/4 for exact checks.

Thus the anticommuting stabilizer condition need not make the third
indicator real. The local M3 argument must retain its separate
cyclotomic rationality step. The half-E6 example attains the proposed
general bound Re(nu_3(Y)) <= dim Hom(1,Y^3)/4 when that dimension is two.
