# Bounded model search for R6_9_3748

No model was found in this search. This is a discovery result, not an obstruction to categorification.

The tensor contains the rank-three PSU(2)5 ring with basis `1,a,b`, where `a²=1+b`, `ab=a+b`, and `b²=1+a+b`. Its other three basis elements are `X,Xa,Xb`, with `X²=1+(2+2a+b)X`. Thus the positive dimension used in the screen is obtained from

`a=2 cos(pi/7)`, `b=a²−1`, `h=2+2a+b`, `x=(h+sqrt(h²+4))/2`, and `D=(1+a²+b²)(1+x²)`.

The numerical value is approximately `600.7027860000444`. The exact global-dimension polynomial is recorded in the JSON output; its constant term is `5274997=7^4*13^3`.

`weyl_screen_m9.py` adapts the inherited WZW vacuum Weyl-product screen. It checks A1–A12, B2–B12, C2–C12, D4–D12, E6–E8, F4 and G2, at levels 1–48. It searches for a rational ratio of the ambient global dimension to `D` or `D²`, with value in `[1/100,100]` and denominator at most 100, at 65 decimal digits and tolerance `10^-50`. The process completed within its 55-second deadline. There were no matches.

This finite numerical screen does not cover arbitrary products, module categories, roots of unity, condensations, or extension sequences. A missing rational match gives no categorical nonexistence statement. The retained exact based-ring model constructors also supply no match: all 64 registered constructor records have maximum coefficient at most 7, whereas this tensor has maximum 9. Extending a parameterized based-ring formula beyond its cited categorical parameter values does not establish a model.
