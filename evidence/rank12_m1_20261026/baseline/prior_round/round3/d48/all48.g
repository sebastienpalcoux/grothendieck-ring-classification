LoadPackage("smallgrp");;
out:=OutputTextFile("rank12-m1-round3-20261026/d48/all48_candidates.json",false);;
PrintTo(out,"[\n");;first:=true;;count:=0;;tested:=0;;
for gi in [1..NrSmallGroups(48)] do
 G:=SmallGroup(48,gi);;els:=ShallowCopy(AsList(G));;Remove(els,Position(els,One(G)));;Add(els,One(G),1);;
 for hc in ConjugacyClassesSubgroups(G) do
 H:=Representative(hc);;tested:=tested+1;;dims:=[];;dbs:=DoubleCosets(G,H,H);;
 for dc in dbs do
  g:=Representative(dc);;K:=Intersection(H,H^g);;degrees:=List(Irr(K),x->x[1]);;
  Append(dims,List(degrees,d->Index(H,K)*d));;
 od;
 Sort(dims);;
 if dims<>[1,1,1,1,1,1,1,1,2,2,4,4] then continue;fi;
 table:=List(els,a->List(els,b->Position(els,a*b)-1));;hs:=List(AsList(H),a->Position(els,a)-1);;Sort(hs);;
 if not first then PrintTo(out,",\n");fi;first:=false;;
 PrintTo(out,"{\"smallgroup\":[48,",gi,"],\"table\":",table,",\"subgroup\":",hs,"}");;
 count:=count+1;;Print("candidate ",gi," subgroup ",Size(H),"\n");
 od;
od;
PrintTo(out,"\n]\n");;CloseStream(out);;
Print("TESTED ",tested," CANDIDATES ",count,"\n");
QUIT;
