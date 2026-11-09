#include "../census/linear_box.hpp"
#include <array>
#include <iostream>
#include <random>
#include <set>
#include <stdexcept>
using W=census::Wide;using I=census::Integer;using Tuple=std::array<I,5>;
int main(){
 int tested=0;std::mt19937 random(20261102);
 for(int trial=0;trial<104;++trial){
  W equations[5][6]{};I M=2;Tuple seed{};
  for(auto&v:seed)v=random()%3;
  int rows=trial<4?trial:random()%6;
  for(int row=0;row<rows;++row){
   for(int col=0;col<5;++col){equations[row][col]=I(random()%5)-2;equations[row][5]+=equations[row][col]*seed[col];}
  }
  if(trial==1){for(auto&v:equations[0])v=0;equations[0][5]=1;}
  if(trial%7==0&&trial>3)equations[0][5]+=1;
  std::set<Tuple> expected,observed;Tuple x{};
  auto brute=[&](auto&&self,int depth)->void{
   if(depth<5){for(I v=0;v<=M;++v){x[depth]=v;self(self,depth+1);}return;}
   for(int row=0;row<5;++row){W sum=0;for(int col=0;col<5;++col)sum+=equations[row][col]*x[col];if(sum!=equations[row][5])return;}
   expected.insert(x);
  };brute(brute,0);
  W copy[5][6];for(int i=0;i<5;++i)for(int j=0;j<6;++j)copy[i][j]=equations[i][j];
  unsigned count=0;
  census::integer_box(copy,M,[&](const I* values){Tuple p{};for(int k=0;k<5;++k)p[k]=values[k];observed.insert(p);++count;});
  if(observed!=expected||count!=observed.size())throw std::logic_error("integer-box mismatch");
  ++tested;
 }
 std::cout<<"{\"all_checks_passed\":true,\"tests\":"<<tested<<",\"assignments_per_test\":243}\n";
}
