LoadPackage("smallgrp");;
out:=OutputTextFile("rank12-m1-round3-20261026/d48/subgroup_twist_candidates.json",false);;PrintTo(out,"[\n");;first:=true;;
for gi in [29,30,48] do
 G:=SmallGroup(48,gi);;els:=ShallowCopy(AsList(G));;Remove(els,Position(els,One(G)));;Add(els,One(G),1);;
 for hc in ConjugacyClassesSubgroups(G) do
 H:=Representative(hc);;if Size(H)<>8 or NormalClosure(G,H)<>G or AbelianInvariantsMultiplier(H)<>[2] then continue;fi;
 ep:=EpimorphismSchurCover(H);;cov:=Source(ep);;ker:=Kernel(ep);;hs:=ShallowCopy(AsList(H));;Remove(hs,Position(hs,One(H)));;Add(hs,One(H),1);;
 lifts:=List(hs,h->PreImagesRepresentative(ep,h));;lifts[1]:=One(cov);;
 psi:=List(hs,a->List(hs,b->0));;
 for a in [1..Length(hs)] do for b in [1..Length(hs)] do
  if lifts[a]*lifts[b]<>lifts[Position(hs,hs[a]*hs[b])] then psi[a][b]:=1;fi;
 od;od;
 objects:=[];;dims:=[];;
 for dc in DoubleCosets(G,H,H) do
  z:=Representative(dc);;kg:=Intersection(H,H^(z^-1));;ks:=ShallowCopy(AsList(kg));;Remove(ks,Position(ks,One(G)));;Add(ks,One(G),1);;
  alpha:=List(ks,a->List(ks,b->(psi[Position(hs,a)][Position(hs,b)]-psi[Position(hs,z^-1*a*z)][Position(hs,z^-1*b*z)])mod 2));;
  table:=[];;nn:=Length(ks);;
  for a in [0..2*nn-1] do
   row:=[];;for b in [0..2*nn-1] do
    Add(row,2*(Position(ks,ks[QuoInt(a,2)+1]*ks[QuoInt(b,2)+1])-1)+(a mod 2+b mod 2+alpha[QuoInt(a,2)+1][QuoInt(b,2)+1])mod 2+1);
   od;Add(table,row);
  od;
  perms:=List([1..2*nn],b->PermList(List([1..2*nn],a->table[a][b])));;extgrp:=Group(perms);;cc:=ConjugacyClasses(extgrp);;cp:=List(perms,p->PositionProperty(cc,c->p in c));;
  for chi in Irr(extgrp) do
   if chi[cp[2]]<>-chi[1] then continue;fi;
   Add(dims,Index(H,kg)*chi[1]);;
   Add(objects,rec(z:=Position(els,z)-1,stab:=List(ks,k->Position(els,k)-1),char:=List([1..nn],a->CoeffsCyc(chi[cp[2*a-1]],96))));
  od;
 od;
 Sort(dims);;Print(gi," H ",StructureDescription(H)," dimensions ",dims,"\n");
 if dims<>[1,1,1,1,1,1,1,1,2,2,4,4] then continue;fi;
 if not first then PrintTo(out,",\n");fi;first:=false;;
 PrintTo(out,"{\"smallgroup\":[48,",gi,"],\"table\":",List(els,a->List(els,b->Position(els,a*b)-1)),",\"subgroup\":",List(hs,a->Position(els,a)-1),",\"psi\":",psi,",\"objects\":[");;
 for oi in [1..Length(objects)] do
  o:=objects[oi];;if oi>1 then PrintTo(out,",");fi;
  PrintTo(out,"{\"z\":",o.z,",\"stab\":",o.stab,",\"char\":",o.char,"}");;
 od;PrintTo(out,"]}");;
 od;
od;
PrintTo(out,"\n]\n");;CloseStream(out);;QUIT;
