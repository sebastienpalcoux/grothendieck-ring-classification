# A check against two tempting false semion arguments

Neither a central semion nor the combination of its free pointed action and
X^*=sX forces an exclusion for a nonbraided fusion category. Here is an
explicit counterexample, written entirely as cocycle scalars.

Let C=Vec_{Z/4}^{omega}, with residues a,b,c in {0,1,2,3} and

omega(a,b,c)=i^{a floor((b+c)/4)}.

The standard carry identity proves the 3-cocycle equation. Let s be the
underlying degree-two object and define its half-braiding with degree x by

c_{s,x}=zeta_8^{3x}.

The half-braiding equation in this convention is

c_{s,x+y mod4}/(c_{s,x}c_{s,y})
 = omega(x,s,y)/(omega(s,x,y)omega(x,y,s)).

The two omega factors with first input x cancel, and both sides are
(-1)^{floor((x+y)/4)}. Thus this is an actual central object. Its central
square has half-braiding

c_{s,x}^2 omega(s,s,x)omega(x,s,s)/omega(s,x,s)
 = zeta_8^{6x} i^x=1.

So it has order two in Z(C). Its self-braiding is zeta_8^6=-i, and the
pointed associator omega(s,s,s)=-1. Consequently it generates a central
reverse-semion subcategory. Tensoring by s is free on all four simples of C.
For the degree-one simple X, X^* has degree three, hence X^*=sX.

Yet C cannot be a Deligne product of a semion category and a rank-two fusion
category: C is pointed with group C4, whereas such a pointed product would
have group C2 x C2. This directly rules out the proposed general splitting
argument. This counterexample has nontrivial universal grading C4, so it
makes no assertion about the additional U(C)=1 and cubic-vertex conditions
specific to R12_1_623.
