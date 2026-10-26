LoadPackage("smallgrp");;
opts:=function(K)
 local ep,cov,iso,ker,kels,cc,rows,chi,fp,old,pos,all;
 ep:=EpimorphismSchurCover(K);;cov:=Source(ep);;ker:=Kernel(ep);;iso:=IsomorphismPcGroup(cov);;cov:=Image(iso);;ker:=Image(iso,ker);;
 kels:=AsList(ker);;cc:=ConjugacyClasses(cov);;pos:=List(kels,a->PositionProperty(cc,c->a in c));;rows:=[];;all:=[];;
 for chi in Irr(cov) do
  fp:=List(pos,i->chi[i]/chi[1]);;old:=Position(rows,fp);;
  if old=fail then Add(rows,fp);Add(all,[chi[1]]);else Add(all[old],chi[1]);fi;
 od;return Set(List(all,SortedList));
end;;
for gi in [1..52] do
 G:=SmallGroup(48,gi);;
 for hc in ConjugacyClassesSubgroups(G) do
  H:=Representative(hc);;if NormalClosure(G,H)<>G then continue;fi;
  ds:=List(Irr(H),c->c[1]);;if not ForAll(ds,d->d in [1,2,4]) or Number(ds,d->d=1)>8 or Number(ds,d->d=2)>2 or Number(ds,d->d=4)>2 then continue;fi;
  states:=[[Number(ds,d->d=1),Number(ds,d->d=2),Number(ds,d->d=4)]];;
  for dc in DoubleCosets(G,H,H) do
   z:=Representative(dc);;if z in H then continue;fi;
   K:=Intersection(H,H^(z^-1));;odims:=opts(K);;choices:=[];;
   for dd in odims do
    dd:=List(dd,x->x*Index(H,K));;
    if ForAll(dd,d->d in [1,2,4]) then Add(choices,[Number(dd,d->d=1),Number(dd,d->d=2),Number(dd,d->d=4)]);fi;
   od;
   news:=[];;for st in states do for ch in choices do
    x:=st+ch;;if x[1]<=8 and x[2]<=2 and x[3]<=2 then AddSet(news,x);fi;
   od;od;states:=news;;
  od;
  if [8,2,2] in states then Print("POSSIBLE ",gi," ",StructureDescription(G)," H ",StructureDescription(H)," order ",Size(H)," N ",Size(Normalizer(G,H))," DC ",List(DoubleCosets(G,H,H),dc->StructureDescription(Intersection(H,H^(Representative(dc)^-1)))),"\n");fi;
 od;
od;
QUIT;
