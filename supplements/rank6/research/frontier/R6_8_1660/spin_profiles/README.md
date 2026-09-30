# Tensor involution and spin constraints

The manuscript proves the tensor involution exchanging X and gX, the resulting
even-fiber parity, and a homogeneous-packet Anderson--Moore--Vafa equation.
Combining its mod-3 specialization with the sixteenth-indicator field constraint
removes 57 of the preceding 1727 profiles: 18 by parity and 39 by the spin/field
condition. The remaining branch counts are 164, 753, 753, totaling **1670**.
The ring is still unresolved.

Run from the package root:

```bash
python -O research/frontier/R6_8_1660/spin_profiles/verify_spin_profiles.py
```

The standard-library verifier replays the preceding fermion certificate, checks
all mod-3 constants, and independently rechecks each rejected charge branch by
a second exact recursion. No optimizer or full center fusion reconstruction is
used. Surviving profiles need not admit spins or modular data.
