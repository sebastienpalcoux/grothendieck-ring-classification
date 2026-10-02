
function hi7DualTensor(){
 const n=8,T=Array.from({length:n},()=>Array.from({length:n},()=>Array(n).fill(0)));
 const add=(v,k,q=1)=>{if(k!==null)v[k]+=q};
 const b=x=>{x=(x%7+7)%7;return x===0?null:1+Math.min(x,7-x)};
 const c=x=>{x=(x%7+7)%7;return x===0?null:4+Math.min(x,7-x)};
 const fill=(i,j,v)=>{T[i][j]=v;T[j][i]=v.slice()};
 for(let i=0;i<n;i++){let v=Array(n).fill(0);v[i]=1;fill(0,i,v)}
 fill(1,1,Array(n).fill(1));
 for(let i=1;i<=3;i++){
  let v=Array(n).fill(1);v[0]=0;v[b(i)]=0;fill(1,b(i),v);
  v=Array(n).fill(1);v[0]=0;v[c(i)]=2;fill(1,c(i),v)
 }
 for(let i=1;i<=3;i++)for(let j=1;j<=3;j++){
  let v=Array(n).fill(1);v[0]=0;fill(b(i),c(j),v);
  v=Array(n).fill(1);v[0]=+(i===j);v[1]=+(i!==j);add(v,b(i+j),-1);add(v,b(i-j),-1);fill(b(i),b(j),v);
  v=Array(n).fill(1);v[0]=+(i===j);v[1]=1+(i===j);add(v,c(i+j));add(v,c(i-j));fill(c(i),c(j),v)
 }
 return T;
}

if (typeof module !== 'undefined') module.exports = {hi7DualTensor};
