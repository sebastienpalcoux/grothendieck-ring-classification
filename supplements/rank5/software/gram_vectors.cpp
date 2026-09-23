// Exact rank-four Gram-vector enumeration for the inherited spherical checks.
// Called only after Python verifies that every accumulation fits signed 128 bits.
// No floating-point arithmetic is used.
#include <array>
#include <iostream>
using I = long long;
using W = __int128_t;

I isqrt(I x) {
    I lo = 0, hi = (I(1) << 30);
    while (lo < hi) {
        const I mid = lo + (hi - lo + 1) / 2;
        if (W(mid) * mid <= x) lo = mid; else hi = mid - 1;
    }
    return lo;
}

int main() {
    I Q[4][4], adj[4][4], determinant;
    for (auto &row : Q) for (auto &x : row)
        if (!(std::cin >> x) || x <= -(I(1) << 60) || x >= (I(1) << 60)) return 2;
    for (auto &row : adj) for (auto &x : row)
        if (!(std::cin >> x) || x <= -(I(1) << 60) || x >= (I(1) << 60)) return 2;
    if (!(std::cin >> determinant) || determinant <= 0 || determinant >= (I(1) << 60)) return 2;
    I bound[4];
    for (int i = 0; i < 4; ++i) {
        if (Q[i][i] < 0) return 2;
        bound[i] = isqrt(Q[i][i]);
    }
    std::array<I, 4> v;
    for (v[0] = 0; v[0] <= bound[0]; ++v[0])
    for (v[1] = 0; v[1] <= bound[1]; ++v[1])
    for (v[2] = 0; v[2] <= bound[2]; ++v[2])
    for (v[3] = 0; v[3] <= bound[3]; ++v[3]) {
        if (!(v[0] || v[1] || v[2] || v[3])) continue;
        bool admissible = true;
        for (int i = 0; i < 4; ++i) for (int j = i; j < 4; ++j)
            if (W(v[i]) * v[j] > Q[i][j]) admissible = false;
        if (!admissible) continue;
        W quadratic = 0;
        for (int i = 0; i < 4; ++i) for (int j = 0; j < 4; ++j)
            quadratic += W(v[i]) * adj[i][j] * v[j];
        if (quadratic > determinant) continue;
        for (I x : v) std::cout << x << ' ';
        std::cout << '\n';
    }
}
