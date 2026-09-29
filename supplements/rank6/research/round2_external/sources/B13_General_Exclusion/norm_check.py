from itertools import product
counts = [0] * 6
survivors = []
for m in range(1, 6):
    for w, x, y in product(range(-2, 3), range(-61, 62),
                           range(-27, 28)):
        if 5*w*w >= m*m:
            continue
        if (y-w) % 2 or (m-w) % 2 or (x-y-m+w) % 4:
            continue
        L = 149*(m*m + 5*w*w) - x*x - 5*y*y
        H = 298*m*w - 2*x*y
        if L <= 0 or L*L <= 5*H*H:
            continue
        counts[m] += 1
        numerator = L*L - 5*H*H
        if numerator % 256:
            raise ValueError("Nonintegral norm")
        n = numerator // 256
        if (149**2 * m**4) % n == 0:
            survivors.append((m, w, x, y, n))
print(counts[1:])
print(survivors)
