"""Experimental extension of the audited Scott scan by exact star-quiver reflections."""
import r155_braid_scott as base
from reflection_test import reflection_test

scott_admissible=base.admissible
def admissible(exponents,counts):
    if not scott_admissible(exponents,counts):return False
    return reflection_test(tuple(tuple(row) for row in exponents),tuple(tuple(row) for row in counts))[0]
base.admissible=admissible
if __name__=='__main__':base.main()
