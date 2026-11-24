"""Exact comparison of a real-rooted integer polynomial's largest root to 48+24√3."""


def negative(a, b):
    """Test a + b√3 < 0 using integers."""
    if a*b >= 0:
        return a+b < 0
    return a*a < 3*b*b if a > 0 else a*a > 3*b*b


def at_most_sharp_bound(coefficients):
    # Horner expansion at Y + 48 + 24√3. Coefficients ascend in Y.
    shifted = [(1, 0)]
    for c in coefficients[1:]:
        new = [(48*a+72*b, 24*a+48*b) for a,b in shifted] + [(0, 0)]
        for k,(a,b) in enumerate(shifted):
            x,y = new[k+1]
            new[k+1] = x+a, y+b
        x,y = new[0]
        new[0] = x+int(c), y
        shifted = new
    # A monic real-rooted polynomial has only nonpositive roots iff all
    # coefficients are nonnegative. Equality at the endpoint is included.
    return not any(negative(a,b) for a,b in shifted)
