LoadPackage("smallgrp");;
out:=OutputTextFile("rank12-m1-round4-20261026/d48/h4_pairs.json",false);;PrintTo(out,"[\n");;first:=true;;
for gi in [30,48] do
 G:=SmallGroup(48,gi);;els:=ShallowCopy(AsList(G));;Remove(els,Position(els,One(G)));;Add(els,One(G),1);;
 N:=First(NormalSubgroups(G),n->Size(n)=2 and IsomorphismGroups(FactorGroup(G,n),SymmetricGroup(4))<>fail);;
 nat:=NaturalHomomorphismByNormalSubgroup(G,N);;iso:=IsomorphismGroups(Image(nat),SymmetricGroup(4));;projs:=List(els,g->List(ListPerm(Image(iso,Image(nat,g))^-1,4),x->x));;
 ccG:=ConjugacyClasses(G);;poss:=List(els,g->PositionProperty(ccG,c->g in c));;
 if gi=30 then
  ch:=First(Irr(G),c->c[1]=1 and ForAny(c,x->x=E(4)));;q:=List(poss,i->Position([1,E(4),-1,-E(4)],ch[i])-1);;
 elif gi=48 then
  sg:=List(els,g->SignPerm(Image(iso,Image(nat,g))));;
  ch:=First(Irr(G),c->c[1]=1 and ForAny(c,x->x=-1) and List(poss,i->c[i])<>sg);;q:=List(poss,i->Position([1,-1],ch[i])-1);;
 else q:=[];fi;
 for hc in ConjugacyClassesSubgroups(G) do
  H:=Representative(hc);;if Size(H)<>4 or NormalClosure(G,H)<>G or Size(Normalizer(G,H))<>8 then continue;fi;
  if SortedList(List(DoubleCosets(G,H,H),dc->Size(Intersection(H,H^(Representative(dc)^-1)))))<>[1,1,2,4,4]then continue;fi;
  if not StructureDescription(H) in ["C4","C2 x C2"]then continue;fi;
  hs:=ShallowCopy(AsList(H));;Remove(hs,Position(hs,One(H)));;Add(hs,One(H),1);;
  ep:=EpimorphismSchurCover(H);;cov:=Source(ep);;ker:=Kernel(ep);;lifts:=List(hs,h->PreImagesRepresentative(ep,h));;lifts[1]:=One(cov);;
  isc:=IsomorphismPcGroup(cov);;lifts:=List(lifts,l->Image(isc,l));;ker:=Image(isc,ker);;kc:=ConjugacyClasses(ker);;psis:=[];;
  for chi in Irr(ker) do
   psi:=List(hs,a->List(hs,b->0));;
   for a in [1..Length(hs)]do for b in [1..Length(hs)]do
    coc:=lifts[a]*lifts[b]*lifts[Position(hs,hs[a]*hs[b])]^-1;;
    psi[a][b]:=Position([1,-1],chi[PositionProperty(kc,c->coc in c)])-1;
   od;od;Add(psis,psi);
  od;
  if not first then PrintTo(out,",\n");fi;first:=false;;
  PrintTo(out,"{\"smallgroup\":[48,",gi,"],\"table\":",List(els,a->List(els,b->Position(els,a*b)-1)),",\"projection_permutations\":",projs,",\"quotient_character\":",q,",\"subgroup\":",List(hs,a->Position(els,a)-1),",\"schur_cocycles\":",psis,"}");;
 od;
od;PrintTo(out,"\n]\n");;CloseStream(out);;QUIT;
