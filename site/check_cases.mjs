#!/usr/bin/env node
/* Focused navigation tests without third-party DOM or browser dependencies. */
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import {fileURLToPath} from "node:url";

const dist=path.join(path.dirname(fileURLToPath(import.meta.url)),"dist");
const read=(name)=>fs.readFileSync(path.join(dist,name),"utf8");
const json=(name)=>JSON.parse(read(name));
const unresolved=json("data/unresolved_cases.json").cases;
const realized=json("data/realized_rings.json").records;
const resolved=json("data/resolved_cases.json").cases;
const atlas=json("data/atlas.json");
const statuses=json("data/classification_status.json").rows;
const origin="https://sebastienpalcoux.github.io/grothendieck-ring-classification/";

// Only the DOM operations used by the count/link renderers are implemented.
// Real layout, focus and browser navigation are verified in the deployed UI.
class TestNode {
  constructor(tag="", text="") {this.tagName=tag;this.nodeType=tag==="#text"?3:tag==="#fragment"?11:1;this.childNodes=[];this.parentNode=null;this.data=text;this.attributes={};this.dataset={};this.value="";this.listeners={};}
  get parentElement() {return this.parentNode?.nodeType===1?this.parentNode:null;}
  get children() {return this.childNodes.filter(n=>n.nodeType===1);}
  get textContent() {return this.nodeType===3?this.data:this.childNodes.map(n=>n.textContent).join("");}
  set textContent(value) {if(this.nodeType===3)this.data=String(value);else this.replaceChildren(String(value));}
  append(...nodes) {
    for(let node of nodes) {
      if(typeof node!=="object")node=new TestNode("#text",String(node));
      if(node.nodeType===11){this.append(...[...node.childNodes]);continue;}
      if(node.parentNode)node.parentNode.childNodes.splice(node.parentNode.childNodes.indexOf(node),1);
      node.parentNode=this;this.childNodes.push(node);
    }
  }
  replaceChildren(...nodes) {this.childNodes.forEach(n=>n.parentNode=null);this.childNodes=[];this.append(...nodes);}
  replaceWith(...nodes) {
    const parent=this.parentNode,index=parent.childNodes.indexOf(this),following=parent.childNodes.slice(index+1);
    parent.childNodes=parent.childNodes.slice(0,index);this.parentNode=null;
    following.forEach(n=>n.parentNode=null);parent.append(...nodes,...following);
  }
  setAttribute(key,value) {this.attributes[key]=String(value);}
  getAttribute(key) {return this.attributes[key];}
  addEventListener(type,callback) {(this.listeners[type] ||= []).push(callback);}
  emit(type) {for(const callback of this.listeners[type] || []) callback({target:this});}
  closest(tag) {for(let node=this;node;node=node.parentElement)if(node.tagName===tag)return node;return null;}
  querySelector(tag) {return descendants(this).find(n=>n.tagName===tag)||null;}
  querySelectorAll(tag) {return descendants(this).filter(n=>n.tagName===tag);}
}
function descendants(node) {return node.childNodes.flatMap(n=>[n,...descendants(n)]);}
function documentFixture() {
  const ids=new Map();
  return {
    ids,
    createElement:(tag)=>new TestNode(tag),
    createElementNS:(_,tag)=>new TestNode(tag),
    createTextNode:(text)=>new TestNode("#text",text),
    createDocumentFragment:()=>new TestNode("#fragment"),
    querySelector:(selector)=>{if(!ids.has(selector))ids.set(selector,new TestNode("div"));return ids.get(selector);},
    createTreeWalker:(node)=>{
      const texts=descendants(node).filter(n=>n.nodeType===3);let i=-1;
      return {nextNode(){i++;this.currentNode=texts[i];return this.currentNode||null;}};
    },
  };
}
function context(search="") {
  return {URL,URLSearchParams,Intl,console,Node:TestNode,NodeFilter:{SHOW_TEXT:4},document:documentFixture(),
          location:{href:origin+"unresolved.html"+search,search}};
}
const caseSource=read("cases.js");
const caseEnd="  init();\n})();";
assert.equal(caseSource.split(caseEnd).length,2,"Expected one case application entry point");
function casesFor(search) {
  const sandbox=context(search);vm.createContext(sandbox);
  vm.runInContext(caseSource.replace(caseEnd,
    "  globalThis.testCases={parseFilters,scopeText,matchesFilters,caseURL,downloadLink,safeURL,categoryClosure,categoryExclusionText,categoryDiagram,braidedStatusText,renderBraidedStatus,renderCategorification,renderSources};\n})();"),sandbox);
  sandbox.testCases.parseFilters();return sandbox.testCases;
}
const selections=[
  ["",6],["?rank=8&m=3",4],["?rank=8&max_m=3",4],["?rank=6",2],
  ["?rank=6&m=4",1],["?rank=6&m=8",1],["?rank=6&max_m=7",1],
  ["?rank=6&max_m=9",2],["?rank=7&m=5",0],["?rank=8&m=2",0],
];
for(const [query,count] of selections) {
  const api=casesFor(query),rows=unresolved.filter(api.matchesFilters);
  assert.equal(rows.length,count,`Wrong list scope: ${query}`);
  for(const ring of rows) {
    const href=new URL(api.caseURL(ring),origin),params=new URLSearchParams(query);
    assert.equal(href.searchParams.get("id"),ring.id);
    for(const key of ["rank","m","max_m"])assert.equal(href.searchParams.get(key),params.get(key));
  }
}
for(const query of ["?rank=-1","?rank=0","?m=1.5","?max_m=NaN","?rank=9007199254740992","?m=3&max_m=3"])
  assert.throws(()=>casesFor(query),undefined,`Invalid filter accepted: ${query}`);
const caseAPI=casesFor("");
for(const bad of ["javascript:alert(1)","data:text/html,test","file:///tmp/test"])assert.equal(caseAPI.safeURL(bad),null);
for(const ring of unresolved.concat(realized,resolved)) {
  const link=caseAPI.downloadLink(ring),url=new URL(link.href,origin);
  assert.equal(decodeURIComponent(url.pathname),`/grothendieck-ring-classification/downloads/fusion-tensors/${ring.id}.txt`);
  assert.equal(link.download,`${ring.id}.txt`);
}

// A Galois existence reduction must never become a structural assertion about
// the original category. Use separate graph inputs and inspect both rendered
// diagrams, including their accessible text.
const spherical={from:"general",to:"spherical",explanation:"Every category admits a spherical structure.",sources:[{label:"Sphericality proof",url:origin+"review.html"}]};
const galois={from:"general",to:"pseudo_unitary",mechanism:"Galois conjugation",explanation:"A pseudo-unitary Galois conjugate exists conditionally on a categorification.",sources:[{label:"Galois reduction",url:origin+"review.html"}]};
const baseReach=caseAPI.categoryClosure([]);
assert.equal(baseReach[4][0],true,"A unitary category is a general fusion category");
assert.equal(baseReach[0][1],false,"General pivotality is not asserted by the standard hierarchy");
const structureReach=caseAPI.categoryClosure([spherical]);
assert.equal(structureReach[0][1],true);
assert.equal(structureReach[0][2],true);
assert.equal(structureReach[1][2],true);
assert.equal(structureReach[0][3],false,"Automatic sphericality must not imply pseudo-unitarity");
const existenceReach=caseAPI.categoryClosure([spherical,galois]);
assert.equal(existenceReach[0][3],true);
assert.equal(existenceReach[0][4],false,"A pseudo-unitary Galois representative does not imply unitarity");
assert.equal(structureReach[0][3],false,"Computing existence closure must not change the same-category closure");
assert.equal(caseAPI.categoryExclusionText(undefined),"Scope not yet audited");
assert.equal(caseAPI.categoryExclusionText({strongest_excluded:null},true),"Unitary categorification also open");
assert.equal(caseAPI.categoryExclusionText({strongest_excluded:null}),"Without requiring a braiding, even unitary categorification remains open.");
assert.equal(caseAPI.categoryExclusionText({strongest_excluded:"pseudo_unitary"}),"No pseudo-unitary categorification");
assert.equal(caseAPI.categoryExclusionText({strongest_excluded:"pivotal"}),"No pivotal categorification");
const levelStatus={general:"unresolved",pivotal:"unresolved",spherical:"unresolved",pseudo_unitary:"unresolved",unitary:"unresolved"};
const scopeFixture={general_status:"unresolved",level_status:levelStatus,strongest_excluded:null,same_category_implications:[spherical],existence_implications:[galois],notes:[],audit_sources:[]};
const scopeView=caseAPI.renderCategorification({categorification_scope:scopeFixture});
const diagrams=descendants(scopeView).filter(node=>node.getAttribute("role")==="img");
assert.equal(diagrams.length,2,"Distinct structural and Galois-existence implications need distinct diagrams");
assert.match(diagrams[0].getAttribute("aria-label"),/Pseudo-unitary implies Spherical/);
assert.doesNotMatch(diagrams[0].getAttribute("aria-label"),/Spherical is equivalent to Pseudo-unitary/);
assert.match(diagrams[1].getAttribute("aria-label"),/Existence after possible Galois conjugation/);
assert.match(diagrams[1].getAttribute("aria-label"),/Spherical is equivalent to Pseudo-unitary/);
assert.match(scopeView.textContent,/does not make the original category pseudo-unitary or unitary/);
const noExtraView=caseAPI.renderCategorification({categorification_scope:{...scopeFixture,existence_implications:[]}});
assert.equal(descendants(noExtraView).filter(node=>node.getAttribute("role")==="img").length,1);
const missingAudit=caseAPI.renderCategorification({});
assert.equal(descendants(missingAudit).filter(node=>node.getAttribute("role")==="img").length,0);
assert.match(missingAudit.textContent,/Scope not yet audited/);
assert.doesNotMatch(missingAudit.textContent,/No exclusion established/);

// Braiding is orthogonal to the five-level chain. Its exclusion must not change
// the general problem, structural statuses, or either implication diagram.
assert.equal(caseAPI.braidedStatusText(undefined),"Braided scope not yet audited");
assert.equal(caseAPI.braidedStatusText({status:"excluded"}),"No braided categorification");
assert.equal(caseAPI.braidedStatusText({status:"unresolved"}),"Braided categorification unresolved");
const braidedExcluded={status:"excluded",explanation:"The fusion product is noncommutative.",sources:[{label:"Braiding audit",url:origin+"review.html"}]};
const excludedFixture={categorification_scope:{...scopeFixture,braided:braidedExcluded}};
const beforeExclusion=JSON.stringify(excludedFixture);
const excludedView=caseAPI.renderCategorification(excludedFixture);
assert.equal(JSON.stringify(excludedFixture),beforeExclusion,"Rendering a braided exclusion must not alter any recorded statuses");
assert.equal(caseAPI.categoryExclusionText(excludedFixture.categorification_scope),caseAPI.categoryExclusionText(scopeFixture));
assert.match(excludedView.textContent,/No braided categorification/);
assert.match(excludedView.textContent,/General categorifiability remains unresolved/);
assert.match(excludedView.textContent,/A braided obstruction does not exclude general categorification/);
const excludedDiagrams=descendants(excludedView).filter(node=>node.getAttribute("role")==="img");
assert.deepEqual(excludedDiagrams.map(node=>node.getAttribute("aria-label")),diagrams.map(node=>node.getAttribute("aria-label")));
assert.equal(baseReach.length,5,"Braiding is not a sixth structure level");
for(const diagram of excludedDiagrams) assert.doesNotMatch(diagram.textContent,/braid/i);
assert.throws(()=>caseAPI.categoryClosure([{from:"general",to:"braided"}]),/Unrecognized categorification level/);

const braidedUnresolved={status:"unresolved",explanation:"Commutativity alone does not construct a braiding.",sources:[],conditional_exclusions:[{assumption:"spherical",explanation:"Only spherical braided categorification is excluded by this argument.",sources:[{label:"Conditional obstruction",url:origin+"review.html"}]}]};
assert.equal(caseAPI.braidedStatusText(braidedUnresolved,true),"Braided open · spherical braided excluded");
const multipleConditions={...braidedUnresolved,conditional_exclusions:[{assumption:"unitary"},{assumption:"spherical"},{assumption:"pivotal"}]};
assert.equal(caseAPI.braidedStatusText(multipleConditions,true),"Braided open · pivotal braided excluded",
  "The list summary highlights the strongest conditional exclusion, independent of input order");
assert.equal(caseAPI.braidedStatusText(multipleConditions),"Braided categorification unresolved",
  "The case heading must not turn a conditional exclusion into an unconditional one");
assert.equal(caseAPI.braidedStatusText({...multipleConditions,status:"excluded"},true),"No braided categorification");
const commutativeView=caseAPI.renderCategorification({invariants:{commutative:true},categorification_scope:{...scopeFixture,braided:braidedUnresolved}});
assert.match(commutativeView.textContent,/Braided categorification unresolved/);
assert.match(commutativeView.textContent,/No spherical braided categorification/);
assert.doesNotMatch(commutativeView.textContent,/No braided categorification/);
assert.doesNotMatch(commutativeView.textContent,/Braided categorification (exists|realized|established)/);
const unconditionallyExcluded=caseAPI.renderBraidedStatus({...braidedUnresolved,status:"excluded"});
assert.doesNotMatch(unconditionallyExcluded.textContent,/No spherical braided categorification/,
  "Conditional restrictions are only displayed for unresolved braiding");
for(const ring of unresolved) {
  assert.ok(ring.categorification_scope,`Missing published categorification scope: ${ring.id}`);
  assert.ok(ring.categorification_scope.braided,`Missing published braided audit: ${ring.id}`);
  const before=JSON.stringify(ring.categorification_scope);
  const view=caseAPI.renderCategorification(ring);
  assert.equal(JSON.stringify(ring.categorification_scope),before,`Rendering altered recorded statuses: ${ring.id}`);
  assert.match(view.textContent,/General categorifiability remains unresolved/);
  assert.ok(view.textContent.includes(caseAPI.braidedStatusText(ring.categorification_scope.braided)),`Missing braided status: ${ring.id}`);
  const ringDiagrams=descendants(view).filter(node=>node.getAttribute("role")==="img");
  assert.ok(ringDiagrams.length,`Missing implication diagram: ${ring.id}`);
  for(const diagram of ringDiagrams)assert.doesNotMatch(diagram.textContent,/braid/i,`Braiding entered the structure hierarchy: ${ring.id}`);
}

for(const ring of resolved) {
  const view=caseAPI.renderCategorification(ring);
  assert.doesNotMatch(view.textContent,/General categorifiability remains unresolved/);
  if(ring.status==="excluded") {
    assert.match(view.textContent,/No general categorification/);
    assert.equal(descendants(view).filter(node=>node.getAttribute("role")==="img").length,0,"Excluded cases do not need hypothetical-structure diagrams");
  } else {
    assert.equal(ring.id,"R8_3_982");
    assert.equal(ring.status,"unitarily_realized");
    assert.match(view.textContent,/Unitary categorification realized/);
    assert.match(view.textContent,/do not assert that every categorification is unitary/);
    assert.doesNotMatch(view.textContent,/No general categorification/);
    assert.ok(descendants(view).some(node=>node.getAttribute("role")==="img"),"The realized case retains its proved universal implications");
  }
}

const appSource=read("app.js"),appEnd="\nstart();";
assert.equal(appSource.split(appEnd).length,2,"Expected one atlas application entry point");
const sandbox=context();vm.createContext(sandbox);
vm.runInContext(appSource.replace(appEnd,
  "\nglobalThis.testApp={state,element,unresolvedUrl,linkUnresolvedText,tensorDownload,renderDetail,renderScope,renderTheoreticalUpdate,renderRingProfile,renderPapers,renderFilters};"),sandbox);
const app=sandbox.testApp,doc=sandbox.document;
app.state.data=atlas;
app.state.models=realized;
app.state.positiveMap=new Map(atlas.grothendieck_rows.map(r=>[`${r.rank}:${r.multiplicity}`,r]));
app.state.statusMap=new Map(statuses.map(r=>[`${r.rank}:${r.multiplicity}`,r]));
const links=(node)=>descendants(node).filter(n=>n.tagName==="a");
const assertLink=(node,text,query)=>{
  const found=links(node).find(a=>a.textContent===text);
  assert.ok(found,`Missing linked count: ${text}`);
  assert.equal(found.href,`./unresolved.html${query}`,`Wrong count destination: ${text}`);
};
const sample=app.element("p","","8 unresolved / 8 unresolved ");
const prelinked=app.element("a","","8 unresolved");prelinked.href="./unresolved.html";sample.append(prelinked);
app.linkUnresolvedText(sample,"8 unresolved",{rank:8,m:3});
assert.equal(sample.textContent,"8 unresolved / 8 unresolved 8 unresolved");
assert.equal(links(sample).length,3);
assert.equal(links(prelinked).length,0,"An existing link must not be nested");
for(const record of statuses.filter(r=>r.unresolved_general)) {
  app.state.selected=atlas.rows.find(r=>r.rank===record.rank&&r.multiplicity===record.multiplicity);
  app.renderDetail();
  assertLink(doc.querySelector("#cell-detail"),String(record.unresolved_general),`?rank=${record.rank}&m=${record.multiplicity}`);
}
app.renderScope();
for(const record of atlas.scope.filter(r=>r.unresolved))
  assertLink(doc.querySelector("#scope-cards"),`${record.unresolved} unresolved`,`?rank=${record.rank}&max_m=${record.analyzed_through}`);
doc.querySelector("#research-update").append(new TestNode("a"));
app.renderTheoreticalUpdate();
const rank8Open=unresolved.filter(r=>r.rank===8).length;
assertLink(doc.querySelector("#research-update-title"),`${rank8Open} open cases`,"?rank=8&max_m=3");
assertLink(doc.querySelector("#theoretical-update-heading"),`${unresolved.length} open cases`,"");
for(const selector of ["#research-update-summary","#theoretical-update-scope"])
  assertLink(doc.querySelector(selector),`${rank8Open} extensively investigated exotic candidates`,"?rank=8&m=3");
assertLink(doc.querySelector("#research-update-summary"),"2 rank-six","?rank=6");
assertLink(doc.querySelector("#research-update-summary"),`${rank8Open} rank-eight`,"?rank=8");
for(const ring of realized) {
  const link=app.tensorDownload(ring),url=new URL(link.href,origin);
  assert.equal(decodeURIComponent(url.pathname),`/grothendieck-ring-classification/downloads/fusion-tensors/${ring.id}.txt`);
  assert.equal(link.download,`${ring.id}.txt`);
}
console.log("Case navigation checked: filters, count links, 228 tensor routes, distinct structural/Galois-existence implications, and separate braided status.");

// A census-only extension must never enter categorification data or imply
// zero models/exclusions. Use a synthetic future rank rather than a new claim.
const fusionContext=context();
fusionContext.fetch=async()=>({ok:true,json:async()=>({release_date:"test",ranks:{
  "20":{bound:1,complete:true,verified:true,classes:7,counts:{"1":7},tables:"results/rank20/tables.txt.gz"}
}})});
vm.createContext(fusionContext);
vm.runInContext(appSource.replace(appEnd,"\nglobalThis.fusionTest={state,loadFusionCounts,ranges,normalizeCountSelection,renderDetail};"),fusionContext);
const fusion=fusionContext.fusionTest;
fusion.state.data=structuredClone(atlas);
fusion.state.models=structuredClone(realized);
fusion.state.positiveMap=new Map(atlas.grothendieck_rows.map(r=>[`${r.rank}:${r.multiplicity}`,r]));
fusion.state.statusMap=new Map(statuses.map(r=>[`${r.rank}:${r.multiplicity}`,r]));
const categoryBefore=JSON.stringify([fusion.state.data,fusion.state.models]);
await fusion.loadFusionCounts();
assert.equal(JSON.stringify([fusion.state.data,fusion.state.models]),categoryBefore,"Census refresh must preserve all categorification data");
fusion.state.mode="fusion";fusion.state.rank=20;
assert.ok(fusion.ranges(fusion.state.data).ranks.includes(20));
fusion.state.selected=fusion.state.censusMap.get("20:1");
fusion.renderDetail();
const fusionDetail=fusionContext.document.querySelector("#cell-detail").textContent;
assert.match(fusionDetail,/7censused fusion rings/);
assert.match(fusionDetail,/Categorification not assessed/);
assert.doesNotMatch(fusionDetail,/reported realized Grothendieck/);
fusion.state.mode="grothendieck";fusion.normalizeCountSelection();
assert.ok(!fusion.ranges(fusion.state.data).ranks.includes(20));
assert.equal(fusion.state.rank,"all");assert.equal(fusion.state.selected,null);
const offlineContext=context();offlineContext.fetch=async()=>{throw new Error("offline")};
vm.createContext(offlineContext);
vm.runInContext(appSource.replace(appEnd,"\nglobalThis.offlineTest={state,loadFusionCounts};"),offlineContext);
offlineContext.offlineTest.state.data=structuredClone(atlas);
await offlineContext.offlineTest.loadFusionCounts();
assert.equal(offlineContext.offlineTest.state.fusionRows,undefined);
assert.match(offlineContext.document.querySelector("#fusion-census-status").textContent,/bundled fusion-count snapshot/);
console.log("Fusion-only census refresh checked: extra ranks, no categorical claims, mode isolation and offline fallback.");


// Every case keeps its complete archive accessible without rendering a wall
// of file links. Exercise real disclosure/search/pagination event handlers.
const hasClass=(node,name)=>String(node.className || "").split(" ").includes(name);
let evidenceFilesChecked=0;
for(const ring of [...unresolved,...resolved,...realized]) {
  const sources=caseAPI.renderSources(ring);
  assert.equal(descendants(sources).filter(n=>hasClass(n,"case-evidence-list")).length,0,ring.id+": archive should be folded initially");
  const library=descendants(sources).find(n=>hasClass(n,"evidence-library"));
  if(!ring.evidence?.length){assert.equal(library,undefined);continue;}
  library.open=true;library.emit("toggle");
  const groups=descendants(library).filter(n=>hasClass(n,"evidence-group"));
  assert(groups.length>0 && groups.length<=4);
  for(const group of groups) {
    group.open=true;group.emit("toggle");
    const more=descendants(group).find(n=>hasClass(n,"evidence-more"));
    let batches=0;
    while(!more.hidden){assert(++batches<1000,"Pagination must finish");more.emit("click");}
  }
  const files=descendants(library).filter(n=>hasClass(n,"case-evidence-list")).flatMap(list=>list.children);
  assert.equal(files.length,ring.evidence.length,ring.id+": evidence count changed");
  const paths=files.map(li=>descendants(li).find(n=>hasClass(n,"case-source-path"))?.textContent || "").sort();
  assert.deepEqual(paths,ring.evidence.map(item=>item.path || "").sort(),ring.id+": missing or duplicated evidence path");
  const input=descendants(library).find(n=>hasClass(n,"evidence-search"));
  const needle=ring.evidence[0].path || ring.evidence[0].label || "";
  input.value=needle;input.emit("input");
  const result=descendants(library).find(n=>n.getAttribute("aria-live")==="polite");
  const count=ring.evidence.filter(item=>`${item.label || ""} ${item.path || ""} ${item.url || ""}`.toLowerCase().includes(needle.toLowerCase())).length;
  assert(result.textContent.startsWith(count.toLocaleString("en-US")+" of "));
  input.value="no-evidence-file-matches-this-query";input.emit("input");
  assert(descendants(library).some(n=>n.textContent==="No file matches this search."));
  evidenceFilesChecked+=files.length;
}
console.log(`Evidence catalogue checked: ${evidenceFilesChecked} preserved file records; folded defaults, complete pagination and search across all case pages.`);

// Every rank uses the same catalogue, case renderer, filters and pagination.
const added=json("data/rank9_rank10_m1.json"),eleven=json("data/rank11_m1.json"),nineM2=json("data/rank9_m2.json"),twelve=json("data/rank12_m1.json");
const payloads={"realized_rings.json":{records:realized},"unresolved_cases.json":{cases:unresolved},"resolved_cases.json":{cases:resolved},"rank9_rank10_m1.json":added,"rank11_m1.json":eleven,"rank9_m2.json":nineM2,"rank12_m1.json":twelve,"ring_property_flags.json":json("data/ring_property_flags.json")};
const fetchCatalogue=async url=>({ok:true,json:async()=>structuredClone(payloads[url.split("/").at(-1).split("?")[0]])});
const catalogueContext=context();catalogueContext.document.querySelector=()=>null;catalogueContext.fetch=fetchCatalogue;
vm.createContext(catalogueContext);vm.runInContext(read("catalogue.js"),catalogueContext);
const catalogue=await catalogueContext.RingCatalogue.load();
assert.equal(catalogue.models.length,532);
assert.equal(catalogue.cases.length,3462);
assert.equal(new Set(catalogue.cases.map(r=>r.id)).size,3462);
assert.equal(catalogue.cases.filter(r=>r.status==="unresolved").length,7);
for (const id of ["R9_2_1607","R9_2_1975","R9_2_1976"]) {
  const ring=catalogue.cases.find(r=>r.id===id);
  assert.equal(ring.status,"excluded");
  assert.equal(ring.categorification_scope.strongest_excluded,"general");
}
for (const id of [114,115,152,153,179]) {
  const ring=catalogue.cases.find(r=>r.id===`R10_1_${id}`);
  assert.equal(ring.status,"excluded");
  assert.equal(ring.categorification_scope.strongest_excluded,"general");
}
const cyclicFrontier=catalogue.cases.find(r=>r.id==="R10_1_189");
assert.equal(cyclicFrontier.status,"unitarily_realized");
assert.equal(cyclicFrontier.existence,"unitary");
assert(Object.values(cyclicFrontier.categorification_scope.level_status).every(s=>s==="realized"));
assert.equal(cyclicFrontier.categorification_scope.braided.status,"excluded");
assert.equal(cyclicFrontier.investigation_deferred,false);
const r623=catalogue.cases.find(r=>r.id==="R12_1_623");
assert(catalogue.models.some(r=>r.id==="R12_1_623"));
assert.equal(r623.status,"pseudo_unitarily_realized");
assert.equal(r623.categorification_scope.level_status.general,"realized");
assert.equal(r623.categorification_scope.level_status.pseudo_unitary,"realized");
assert.equal(r623.categorification_scope.level_status.unitary,"unresolved");
const pseudoView=caseAPI.renderCategorification(r623);
assert.match(pseudoView.textContent,/Unitarity remains unproved/);
assert.doesNotMatch(pseudoView.textContent,/General categorifiability remains unresolved/);
const state={data:structuredClone(atlas),models:structuredClone(realized)};state.data.classification_rows=structuredClone(statuses);
catalogueContext.RingCatalogue.mergeAtlas(state,catalogue);
for (const original of realized) {const {properties,...record}=state.models.find(r=>r.id===original.id);assert.equal(JSON.stringify(record),JSON.stringify(original));}
assert.equal(state.data.rows.length,atlas.rows.length+5);
assert.equal(state.data.scope.length,atlas.scope.length+4);
assert.equal(new Set(state.models.map(r=>r.id)).size,532);
for(const [rank,total,models,open] of [[9,142,40,1],[10,194,58,0],[11,182,27,0],[12,632,152,0]]) {
  assert.equal(state.data.rows.find(r=>r.rank===rank).rings,total);
  assert.equal(state.data.grothendieck_rows.find(r=>r.rank===rank).rings,models);
  assert.equal(state.data.scope.find(r=>r.rank===rank).unresolved,open);
}
const releaseContext=context();releaseContext.Blob=Blob;vm.createContext(releaseContext);
vm.runInContext(caseSource.replace(caseEnd,"  globalThis.renderReleaseCase=renderCase;\n})();"),releaseContext);
for(const ring of catalogue.cases) {
  releaseContext.renderReleaseCase(ring,["unresolved","excluded"].includes(ring.status));
  assert.equal(releaseContext.document.querySelector("#case-title").textContent,ring.id);
  const back=releaseContext.document.querySelector("#case-back").href;
  assert(!/rank11|rank9-10/.test(back),"Every case returns to a common atlas view");
  if(ring.status==="excluded")assert.equal(back,`./records.html?rank=${ring.rank}&m=${ring.multiplicity}`);
  if(ring.status==="unitarily_realized")assert.equal(back,`./index.html?rank=${ring.rank}&m=${ring.multiplicity}#rings`);
}
doc.querySelectorAll=()=>[];
for(const ring of catalogue.models.filter(row=>row.rank>=9)) {
  app.state.profile=ring;app.state.matrixIndex=1;
  for(const tab of ["tensor","characters","source"]) {
    app.state.profileTab=tab;app.renderRingProfile();assert(doc.querySelector("#ring-profile").textContent.length>0);
  }
  assert(links(doc.querySelector("#ring-profile")).some(item=>item.href===ring.report_url));
}
for(const query of ["","?rank=2&m=1","?rank=10&status=unresolved","?rank=11","?rank=11&status=realized","?rank=11&status=excluded","?rank=11&status=unresolved","?rank=9&m=2&status=unresolved","?rank=99&status=invalid","?q=R10_1_189","?rank=12","?rank=12&status=realized","?rank=12&status=pseudo_unitarily_realized"]) {
  const directory=context(query);directory.location.href=origin+"records.html"+query;directory.fetch=fetchCatalogue;
  directory.history={replaceState:(_,__,url)=>{directory.location.href=String(url);directory.location.search=url.search;}};
  vm.createContext(directory);vm.runInContext(read("properties.js"),directory);vm.runInContext(read("catalogue.js"),directory);
  await new Promise(resolve=>setImmediate(resolve));
  const get=id=>directory.document.querySelector("#record-"+id),params=new URLSearchParams(query);
  const expected=catalogue.cases.filter(r=>(!params.get("rank")||params.get("rank")==="99"||r.rank===Number(params.get("rank")))&&
    (!params.get("m")||r.multiplicity===Number(params.get("m")))&&(!params.get("status")||params.get("status")==="invalid"||
    (params.get("status")==="realized"?["realized","unitarily_realized","pseudo_unitarily_realized"].includes(r.status):r.status===params.get("status")))&&
    (!params.get("q")||r.id===params.get("q")));
  const seen=[];
  for(let pages=0;pages<Math.ceil(expected.length/24)+1;pages++) {
    const shown=get("list").children;assert(shown.length<=24,"Directory pages stay compact");
    seen.push(...shown.map(row=>descendants(row).find(n=>n.tagName==="strong").textContent));
    if(get("next").disabled)break;get("next").emit("click");
  }
  assert.deepEqual(seen,Array.from(expected,r=>r.id),`All ordered records must be reachable: ${query}`);
  get("rank").value="11";get("rank").emit("input");assert(get("previous").disabled,"Filtering resets pagination");
}
for(const name of ["index.html","case.html","unresolved.html","records.html"]) {
  const html=read(name);assert.match(html,/src="\.\/catalogue\.js/);assert.doesNotMatch(html,/rank11-current|rank9-10-current|href="\.\/rank11\.html"/);
}
for(const name of ["rank11.html","rank9-10.html"])assert.match(read(name),/src="\.\/redirect\.js/);
console.log("Unified catalogue checked: 3462 ordered case pages, 532 models, 7 open cases; shared rank/status/multiplicity filters and complete pagination through rank 12.");

app.state.data=state.data;app.state.models=state.models;
app.state.censusMap=new Map(state.data.rows.map(r=>[`${r.rank}:${r.multiplicity}`,r]));
app.state.positiveMap=new Map(state.data.grothendieck_rows.map(r=>[`${r.rank}:${r.multiplicity}`,r]));
app.state.statusMap=new Map(state.data.classification_rows.map(r=>[`${r.rank}:${r.multiplicity}`,r]));
app.renderFilters();assert.equal(doc.querySelector("#rank-filters").children.length,12);
assert.equal(doc.querySelector("#rank-filters").children.at(-1).textContent,"12");
app.renderPapers();const papers=doc.querySelector("#paper-grid").children;
assert.equal(papers.length,11);assert.match(papers.at(-1).textContent,/11 \/ RANK 12/);
assert(links(papers.at(-1)).some(a=>a.href.endsWith("/blob/main/publications/rank12/paper/rank12.tex")));
assert([...papers].some(p=>links(p).some(a=>a.href.endsWith("/blob/main/publications/rank9-rank10/paper/rank9-rank10.tex"))));
assert([...papers].some(p=>links(p).some(a=>a.href.endsWith("/blob/main/publications/rank9-m2/paper/rank9-m2.tex"))));
for(const rank of [2,9,10,11,12]) {
  app.state.selected=state.data.rows.find(r=>r.rank===rank&&r.multiplicity===1);app.renderDetail();
  assert(links(doc.querySelector("#cell-detail")).some(a=>a.href===`./records.html?rank=${rank}&m=1`));
}
for(const [name,rank] of [["rank11.html","11"],["rank9-10.html",""]]) {
  const redirect=context("?status=excluded&q=test");redirect.document.body={dataset:{rank}};
  redirect.location.href=origin+name+redirect.location.search;let destination;
  redirect.location.replace=url=>{destination=new URL(url);};vm.createContext(redirect);vm.runInContext(read("redirect.js"),redirect);
  assert.equal(destination.pathname,"/grothendieck-ring-classification/records.html");
  assert.equal(destination.searchParams.get("q"),"test");assert.equal(destination.searchParams.get("status"),"excluded");
  if(rank)assert.equal(destination.searchParams.get("rank"),rank);
}
console.log("Standard rank controls, ordered manuscript shelf and current mathematical PDFs, common count-to-case links and legacy URL redirects checked.");
