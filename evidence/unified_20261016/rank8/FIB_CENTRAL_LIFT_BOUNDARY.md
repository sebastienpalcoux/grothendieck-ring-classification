# A central Fibonacci lift is not a Deligne factorization

A general implication from regular Fibonacci bimodule components, trivial BrPic(Fib), or even an actual central lift of Fib to a Deligne splitting is false.

The unitary adjoint E8 category is an explicit counterexample. Its rank-four ring has generators tau and x with

    tau^2=1+tau,  x^2=1+x+tau x,

and basis 1,tau,x,tau x. The Fibonacci left and right actions coincide; their two rank-two components are regular Fib bimodules. Yet the category is not Fib times a rank-two fusion category. Such a splitting would give the rank-two factor either pointed or Fibonacci fusion rules, whereas the remaining simple dimensions in Ad(E8) are d and phi d with d the positive root of d^2=1+(1+phi)d, different from 1 and phi.

There is nonetheless an actual central lift of Fib. Mitchell Rowett, Monoidal Ladder Categories, printed pages82--83, Proposition6.11 (citing Edie-Michell's Lemma3.1.3), gives

    Z(Ad(E8)+)=Ad(D16) times Fib^rev,
    Z(Ad(E8)-)=Ad(D16)^rev times Fib,

and explicitly states the corresponding central functors Fib^rev→Ad(E8)+ and Fib→Ad(E8)-. The source is https://tqft.net/web/research/students/MitchellRowett/thesis.pdf . The existing census model is supplements/rank4/data/models.json, model Ad_E8, label F_{3,19}; its four multiplication matrices verify the presentation above.

This counterexample does not disprove a forced-central-lift statement under additional assumptions. It does disprove using such a lift as an ordinary quotient or Deligne factorization in an unbraided ambient fusion category. Müger factorization requires a braided ambient category. Quotienting a central Tannakian Rep(C2) is a separate operation and requires proving that precise central symmetric structure.
