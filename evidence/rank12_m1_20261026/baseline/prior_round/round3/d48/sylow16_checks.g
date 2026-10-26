LoadPackage("smallgrp");;
for gi in [10,12,13,14,19,30,34,36,37,38,39,43,48] do
 G:=SmallGroup(48,gi);;H:=SylowSubgroup(G,2);;N:=SylowSubgroup(G,3);;
 Print(gi," normalSylow3=",IsNormal(G,N)," Htype=",StructureDescription(H)," Hmultiplier=",AbelianInvariantsMultiplier(H),"\n");;
 if IsNormal(G,N) then
  z:=First(AsList(N),x->x<>One(G));;K:=Intersection(H,H^(z^-1));;
  if not Size(K)=8 or not ForAll(AsList(K),k->Comm(k,z)=One(G))then Error("normal-three intersection check");fi;
 fi;
od;
QUIT;
