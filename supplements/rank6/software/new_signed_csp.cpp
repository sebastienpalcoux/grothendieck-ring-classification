// Complete finite-domain quadratic equation solver. No numerical pruning.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <deque>
#include <iostream>
#include <limits>
#include <vector>
using namespace std;
struct Term { long long c; int i,j; };
struct Eq { vector<Term> terms; vector<int> vars; };
int nv,ne; vector<vector<long long>> values; vector<Eq> eqs;
vector<vector<int>> links; unsigned long long nodes=0,sols=0;
chrono::steady_clock::time_point begun; double budget;
bool complete=true;
int card(uint64_t d){return __builtin_popcountll(d);}
long long fixed(int i,const vector<uint64_t>&ds){return values[i][__builtin_ctzll(ds[i])];}
vector<long long> domain(int i,const vector<uint64_t>&ds){
 vector<long long> out; for(int k=0;k<(int)values[i].size();++k)if(ds[i]&(1ULL<<k))out.push_back(values[i][k]);return out;
}
bool propagate(vector<uint64_t>&ds){
 deque<int> queue;vector<bool> waiting(ne,true);for(int e=0;e<ne;++e)queue.push_back(e);
 while(!queue.empty()){
  int at=queue.front();queue.pop_front();waiting[at]=false;const Eq&e=eqs[at];
  vector<int> free;for(int i:e.vars)if(card(ds[i])>1)free.push_back(i);
  if(free.size()<=2){
   long long c=0,a=0,b=0,aa=0,ab=0,bb=0;
   int x=free.empty()?-2:free[0],y=free.size()<2?-3:free[1];
   for(auto t:e.terms){
    long long co=t.c;int degreeX=0,degreeY=0;
    for(int k:{t.i,t.j}){if(k<0)continue;if(k==x)++degreeX;else if(k==y)++degreeY;else co*=fixed(k,ds);}
    if(degreeX==2)aa+=co;else if(degreeY==2)bb+=co;else if(degreeX&&degreeY)ab+=co;
    else if(degreeX)a+=co;else if(degreeY)b+=co;else c+=co;
   }
   if(free.empty()){if(c)return false;continue;}
   uint64_t goodX=0,goodY=0;
   for(int ix=0;ix<(int)values[x].size();++ix)if(ds[x]&(1ULL<<ix)){
    long long vx=values[x][ix];
    if(y<0){if(c+a*vx+aa*vx*vx==0)goodX|=1ULL<<ix;continue;}
    for(int iy=0;iy<(int)values[y].size();++iy)if(ds[y]&(1ULL<<iy)){
     long long vy=values[y][iy];if(c+a*vx+b*vy+aa*vx*vx+ab*vx*vy+bb*vy*vy==0){goodX|=1ULL<<ix;goodY|=1ULL<<iy;}
    }
   }
   if(!goodX||(y>=0&&!goodY))return false;
   for(auto pair:vector<pair<int,uint64_t>>{{x,goodX},{y,goodY}}){
    int k=pair.first;if(k<0||ds[k]==pair.second)continue;ds[k]=pair.second;
    for(int q:links[k])if(!waiting[q]){waiting[q]=true;queue.push_back(q);}
   }
  }else{
   long long low=0,high=0;
   for(auto t:e.terms){
    long long lo=1,hi=1;
    if(t.i>=0){auto vi=domain(t.i,ds);lo=*min_element(vi.begin(),vi.end());hi=*max_element(vi.begin(),vi.end());}
    if(t.j>=0){
     long long nlo=numeric_limits<long long>::max(),nhi=numeric_limits<long long>::min();
     auto vi=domain(t.i,ds),vj=domain(t.j,ds);
     if(t.i==t.j){for(long long v:vi){nlo=min(nlo,v*v);nhi=max(nhi,v*v);}}
     else for(long long v:vi)for(long long w:vj){nlo=min(nlo,v*w);nhi=max(nhi,v*w);}
     lo=nlo;hi=nhi;
    }
    if(t.c<0)swap(lo,hi);low+=t.c*lo;high+=t.c*hi;
   }
   if(low>0||high<0)return false;
  }
 }
 return true;
}
void dfs(vector<uint64_t> ds){
 if(!complete)return;
 if(nodes==numeric_limits<unsigned long long>::max()){complete=false;return;}++nodes;
 if((nodes&1023)==0&&chrono::duration<double>(chrono::steady_clock::now()-begun).count()>budget){complete=false;return;}
 if(!propagate(ds))return;
 int chosen=-1,best=100000;double bestScore=-1;
 for(int i=0;i<nv;++i)if(card(ds[i])>1){
  int count=card(ds[i]);double score=0;
  for(int e:links[i]){int left=0;for(int k:eqs[e].vars)left+=(card(ds[k])>1);score+=1.0/(left*left);}
  score/=(count-1);
  if(score>bestScore||(score==bestScore&&count<best)){chosen=i;best=count;bestScore=score;}
 }
 if(chosen<0){
  if(sols==numeric_limits<unsigned long long>::max()){complete=false;return;}++sols;
  for(int i=0;i<nv;++i)cout<<fixed(i,ds)<<' ';cout<<'\n';return;
 }
 uint64_t original=ds[chosen];for(int k=0;k<(int)values[chosen].size();++k)if(original&(1ULL<<k)){ds[chosen]=1ULL<<k;dfs(ds);if(!complete)return;}
}
int main(){
 cin>>nv>>ne>>budget;values.resize(nv);links.resize(nv);vector<uint64_t>ds(nv);
 for(int i=0;i<nv;++i){int n;cin>>n;if(n<1||n>63)return 4;for(int j=0;j<n;++j){long long v;cin>>v;values[i].push_back(v);}ds[i]=(1ULL<<n)-1;}
 eqs.resize(ne);for(int e=0;e<ne;++e){int nt;cin>>nt;for(int j=0;j<nt;++j){Term t;cin>>t.c>>t.i>>t.j;eqs[e].terms.push_back(t);if(t.i>=0)eqs[e].vars.push_back(t.i);if(t.j>=0)eqs[e].vars.push_back(t.j);}auto&v=eqs[e].vars;sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());for(int i:v)links[i].push_back(e);}
 if(!cin)return 5;begun=chrono::steady_clock::now();dfs(ds);
 cerr<<"complete "<<complete<<" nodes "<<nodes<<" solutions "<<sols<<'\n';return complete?0:3;
}
