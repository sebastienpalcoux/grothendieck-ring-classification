"""Cyclic-16 weights when the two conductor-eight Fourier modes vanish."""
from fractions import Fraction
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'generic_quartic'))
from sixteen import S, conjugates, examples


def weight(x, y):
    """Enclose (y-1)/(2(y-x)) using the given rational root intervals."""
    numerator = (y[0] - S, y[1] - S)
    denominator = (2 * (y[0] - x[1]), 2 * (y[1] - x[0]))
    assert denominator[0] * denominator[1] > 0
    corners = [Fraction(a, b) for a in numerator for b in denominator]
    return min(corners), max(corners)


def main(generate=False):
    # No auxiliary data need to be generated for these direct comparisons.
    ratios = examples(100)
    positive = 0
    for row in ratios:
        x = conjugates(*row[:4])
        assert all(x[0][1] < z[0] for z in x[1:])
        q = [weight(x[i], x[(i+2) % 4]) for i in range(4)]
        if any(hi < 0 for lo, hi in q):
            continue
        assert all(lo > 0 for lo, hi in q)
        positive += 1
        assert any(hi < q[0][0] for lo, hi in q[1:])
    assert (len(ratios), positive) == (86, 20)
    print('Conductor 16: 86 ratios, 20 positive weight vectors, none with q_0 least.')


if __name__ == '__main__':
    main('--generate' in sys.argv)
