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
const atlas=json("data/atlas.json");
const statuses=json("data/classification_status.json").rows;
const origin="https://sebastienpalcoux.github.io/grothendieck-ring-classification/";

// Only the DOM operations used by the count/link renderers are implemented.
// Real layout, focus and browser navigation are verified in the deployed UI.
class TestNode {
  constructor(tag="", text="") {this.tagName=tag;this.nodeType=tag==="#text"?3:tag==="#fragment"?11:1;this.childNodes=[];this.parentNode=null;this.data=text;this.attributes={};this.dataset={};}
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
  addEventListener() {}
  closest(tag) {for(let node=this;node;node=node.parentElement)if(node.tagName===tag)return node;return null;}
  querySelector(tag) {return descendants(this).find(n=>n.tagName===tag)||null;}
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
    "  globalThis.testCases={parseFilters,scopeText,matchesFilters,caseURL,downloadLink,safeURL};\n})();"),sandbox);
  sandbox.testCases.parseFilters();return sandbox.testCases;
}
const selections=[
  ["",10],["?rank=8&m=3",8],["?rank=8&max_m=3",8],["?rank=6",2],
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
for(const ring of unresolved.concat(realized)) {
  const link=caseAPI.downloadLink(ring),url=new URL(link.href,origin);
  assert.equal(decodeURIComponent(url.pathname),`/grothendieck-ring-classification/downloads/fusion-tensors/${ring.id}.txt`);
  assert.equal(link.download,`${ring.id}.txt`);
}

const appSource=read("app.js"),appEnd="\nstart();";
assert.equal(appSource.split(appEnd).length,2,"Expected one atlas application entry point");
const sandbox=context();vm.createContext(sandbox);
vm.runInContext(appSource.replace(appEnd,
  "\nglobalThis.testApp={state,element,unresolvedUrl,linkUnresolvedText,tensorDownload,renderDetail,renderScope,renderTheoreticalUpdate};"),sandbox);
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
assertLink(doc.querySelector("#research-update-title"),"8 open cases","?rank=8&max_m=3");
assertLink(doc.querySelector("#theoretical-update-heading"),"10 open cases","");
for(const selector of ["#research-update-summary","#theoretical-update-scope"])
  assertLink(doc.querySelector(selector),"8 extensively investigated exotic candidates","?rank=8&m=3");
assertLink(doc.querySelector("#research-update-summary"),"2 rank-six","?rank=6");
assertLink(doc.querySelector("#research-update-summary"),"8 rank-eight","?rank=8");
for(const ring of realized) {
  const link=app.tensorDownload(ring),url=new URL(link.href,origin);
  assert.equal(decodeURIComponent(url.pathname),`/grothendieck-ring-classification/downloads/fusion-tensors/${ring.id}.txt`);
  assert.equal(link.download,`${ring.id}.txt`);
}
console.log("Case navigation checked: exact/cumulative/empty/invalid filters, scoped count links and 228 tensor download routes.");
