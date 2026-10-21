#include <iostream>
using namespace std;
int main(){
long long count=0;
for(long long x0 : {1LL,3LL,5LL}) {
for(long long x1 : {1LL,3LL,5LL}) {
for(long long x2 : {1LL,3LL,5LL}) {
for(long long x3 : {-4LL,-2LL,0LL,2LL,4LL}) {
for(long long x4 : {-4LL,-2LL,0LL,2LL,4LL}) {
for(long long x5 : {-4LL,-2LL,0LL,2LL,4LL}) {
for(long long x6 : {-4LL,-2LL,0LL,2LL,4LL}) {
for(long long x7 : {-4LL,-2LL,0LL,2LL,4LL}) {
if (((x0*x0) - x0*x3 - x1*x5 + (x4*x4) - x4*x7 + (x6*x6) - 1)!=0) continue;
for(long long x8 : {-4LL,-2LL,0LL,2LL,4LL}) {
for(long long x9 : {-5LL,-3LL,-1LL,1LL,3LL,5LL}) {
if ((x0*x1 - x0*x5 - x1*x9 + x2*x6 + x4*x6 - x6*x7)!=0) continue;
if ((x0*x2 - x1*x6 - x2*x9 + x4*x9 - x5*x6 + x6*x8)!=0) continue;
if ((x0*x6 - x1*x4 - x2*x5 - x3*x6 + x4*x5 + x6*x9)!=0) continue;
if ((x0*x9 - (x1*x1) + x1*x8 - (x2*x2) + x2*x7 - (x6*x6) + 1)!=0) continue;
if ((x2*x4 + x3*x9 - (x5*x5) + x5*x8 - (x6*x6) - (x9*x9) + 1)!=0) continue;
++count; cout << x0 << "," << x1 << "," << x2 << "," << x3 << "," << x4 << "," << x5 << "," << x6 << "," << x7 << "," << x8 << "," << x9 << "\n";
}
}
}
}
}
}
}
}
}
}
cerr << count << " solutions\n"; return 0;
}
