import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const site=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
class Element {
 constructor(tag){this.tag=tag;this.children=[];this.events={};this.value='';this.hidden=false;}
 append(...nodes){this.children.push(...nodes);}
 replaceChildren(...nodes){this.children=nodes;}
 addEventListener(name,callback){this.events[name]=callback;}
 querySelectorAll(tag){return this.children.flatMap(c=>typeof c==='object'?[...(c.tag===tag?[c]:[]),...c.querySelectorAll(tag)]:[]);}
 change(value){this.value=value;this.events.change();}
}
const ctx=vm.createContext({document:{createElement:tag=>new Element(tag)},URLSearchParams,location:{search:''}});
vm.runInContext(fs.readFileSync(path.join(site,'dist/properties.js'),'utf8'),ctx);
let changes=0;const root=new Element('div');
const filter=ctx.RingProperties.mount(root,'test',()=>changes++,new URLSearchParams('p_weakly_integral=yes&p_integral=no&q=ising'));
const selectors=root.querySelectorAll('select');assert.equal(selectors.length,8);
const ising={properties:{integral:false,weakly_integral:true,simple:false,perfect:false,pointed:false,commutative:true,self_dual:true,multiplicity_free:true}};
assert(filter.matches(ising));assert(!filter.matches({properties:{integral:true,weakly_integral:true}}));assert(!filter.matches({}));
selectors.find(s=>s.id==='test-simple').change('yes');assert(!filter.matches(ising));assert.equal(changes,1);
let query=filter.applyParams(new URLSearchParams('q=ising&rank=3'));assert.equal(query.get('q'),'ising');assert.equal(query.get('rank'),'3');assert.equal(query.get('p_integral'),'no');assert.equal(query.get('p_simple'),'yes');
root.querySelectorAll('button')[0].events.click();assert.equal(filter.size,0);assert(filter.matches(ising));assert.equal(filter.applyParams(query).get('p_integral'),null);
for(const name of ['records.html','unresolved.html','index.html']){const s=fs.readFileSync(path.join(site,'dist',name),'utf8');assert(s.includes('properties.js'));assert(s.includes('property-filters'));assert(s.includes('theory.html'));}
const theory=fs.readFileSync(path.join(site,'dist/theory.html'),'utf8');for(const anchor of ['rings','categories','grothendieck','dimensions','filters','examples','status','references'])assert(theory.includes(`id="${anchor}"`));
console.log('Shared structural filters PASS: exact flags, complements, conjunctions, reset, URL preservation and all three list integrations.');
