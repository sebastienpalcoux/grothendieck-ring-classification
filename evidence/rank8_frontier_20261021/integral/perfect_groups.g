if LoadPackage("smallgrp")=fail then Error("SmallGroups unavailable");fi;
SetInfoLevel(InfoWarning,0);
perfect:=[];;
for i in [1..NumberSmallGroups(360)] do
 g:=SmallGroup(360,i);;
 if IsPerfectGroup(g) then Add(perfect,i);fi;
od;
if perfect<>[118] then Error("perfect360 mismatch");fi;
if IdGroup(AlternatingGroup(6))<>[360,118] then Error("A6 identifier mismatch");fi;
Print("{\"order360_groups\":",NumberSmallGroups(360),",\"perfect360_indices\":",perfect,",\"perfect_divisor_counts\":[");
first:=true;;
for n in DivisorsInt(360) do
 if n>1 then
  if not first then Print(",");fi;first:=false;
  Print("[",n,",",NumberPerfectGroups(n),"]");
 fi;
od;
Print("]}\n");
QUIT;
