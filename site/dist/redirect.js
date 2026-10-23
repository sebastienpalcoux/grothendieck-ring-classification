"use strict";
// Preserve previously shared release links in the common case directory.
const target = new URL("./records.html", location.href);
target.search = location.search;
if (document.body.dataset.rank) target.searchParams.set("rank", document.body.dataset.rank);
location.replace(target.href);
