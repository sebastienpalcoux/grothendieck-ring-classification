import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const site = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const propertySource = fs.readFileSync(path.join(site, 'dist/properties.js'), 'utf8');
const constructionSource = fs.readFileSync(path.join(site, 'dist/constructions.js'), 'utf8');

// A small DOM fixture exercises the actual shipped scripts without dependencies.
class Element {
  constructor(tag) {
    Object.assign(this, {tag, children: [], events: {}, value: '', hidden: false,
      disabled: false, dataset: {}, textContent: '', className: '', parent: null});
  }
  append(...nodes) {
    for (const node of nodes) {
      if (node && typeof node === 'object') {
        if (node.parent) node.parent.children = node.parent.children.filter(child => child !== node);
        node.parent = this;
      }
      this.children.push(node);
    }
  }
  replaceChildren(...nodes) {
    for (const node of this.children) if (node && typeof node === 'object') node.parent = null;
    this.children = [];
    this.append(...nodes);
  }
  addEventListener(name, callback) { this.events[name] = callback; }
  querySelectorAll(selector) {
    const matches = node => selector.startsWith('.')
      ? node.className.split(/\s+/).includes(selector.slice(1)) : node.tag === selector;
    return this.children.flatMap(node => node && typeof node === 'object'
      ? [...(matches(node) ? [node] : []), ...node.querySelectorAll(selector)] : []);
  }
  get options() { return this.children; }
  focus() { this.focused = true; }
  scrollIntoView() { this.scrolled = true; }
  input(value) { this.value = value; this.events.input(); }
  change(value) { this.value = value; this.events.change(); }
}

function fixture(url = 'https://example.org/atlas/constructions.html', brokenProperties = false) {
  const selectors = new Map();
  for (const id of ['construction-search', 'construction-rank', 'construction-m',
    'construction-property-filters', 'construction-count', 'construction-empty', 'construction-reset']) {
    selectors.set('#' + id, new Element('div'));
  }
  selectors.get('#construction-rank').append(...['', '6', '8', '10'].map(value =>
    Object.assign(new Element('option'), {value})));
  const rows = [
    ['R8_2_11', 8, 2, 'inversion orbifold', false],
    ['R6_4_3', 6, 4, 'fermion quotient', true],
    ['R8_2_1', 8, 2, 'cyclic orbifold', true],
    ['R8_3_2', 8, 3, 'tensor extension', false],
    ['R10_1_2', 10, 1, 'tensor product', true],
    ['R8_12_1', 8, 12, 'higher multiplicity extension', true],
  ];
  const entries = rows.map(([id, rank, m, search, integral]) => Object.assign(new Element('article'), {
    id, className: 'construction-entry',
    dataset: {id, rank: String(rank), multiplicity: String(m), search,
      properties: JSON.stringify({integral, weakly_integral: true, simple: false})},
  }));
  const list = new Element('div');
  list.append(...entries);
  selectors.set('.construction-list', list);
  selectors.set('.construction-toolbar', new Element('form'));
  const location = {};
  function navigate(value) {
    const parsed = new URL(value);
    Object.assign(location, {href: parsed.href, search: parsed.search, hash: parsed.hash});
  }
  navigate(url);
  const events = {}, errors = [];
  const context = vm.createContext({
    document: {querySelector: key => selectors.get(key), createElement: tag => new Element(tag)},
    location, history: {replaceState: (_state, _title, value) => navigate(value.href)},
    URL, URLSearchParams, requestAnimationFrame: callback => callback(),
    window: {addEventListener: (name, callback) => { events[name] = callback; }},
    console: {error: (...args) => errors.push(args)},
  });
  vm.runInContext(propertySource, context);
  if (brokenProperties) context.RingProperties.mount = () => { throw new Error('Simulated dependency failure'); };
  vm.runInContext(constructionSource, context);
  const get = id => selectors.get('#' + id);
  return {entries, list, get, location, events, errors, navigate,
    visible: () => list.children.filter(entry => !entry.hidden).map(entry => entry.id),
    property: name => get('construction-property-filters').querySelectorAll('select')
      .find(select => select.id === 'construction-property-' + name)};
}

const normal = fixture();
assert.deepEqual(normal.visible(), ['R6_4_3', 'R8_2_1', 'R8_2_11', 'R8_3_2', 'R8_12_1', 'R10_1_2'],
  'Rank, multiplicity and identifiers must be sorted numerically');
assert.equal(normal.get('construction-count').textContent, 'Showing 6 of 6 examples');
assert(normal.get('construction-reset').disabled);
normal.get('construction-search').input('FERMION');
assert.deepEqual(normal.visible(), ['R6_4_3']);
assert.equal(new URL(normal.location.href).searchParams.get('q'), 'FERMION');
normal.get('construction-rank').input('8');
assert.deepEqual(normal.visible(), []);
assert.equal(normal.get('construction-count').textContent, 'Showing 0 of 6 examples');
assert.equal(normal.get('construction-empty').hidden, false);
normal.get('construction-reset').events.click();
assert.equal(normal.visible().length, 6);
assert.equal(normal.location.search, '');
assert(normal.get('construction-search').focused);
normal.get('construction-m').input('2');
assert.deepEqual(normal.visible(), ['R8_2_1', 'R8_2_11']);
normal.property('integral').change('yes');
assert.deepEqual(normal.visible(), ['R8_2_1']);
assert.equal(new URL(normal.location.href).searchParams.get('p_integral'), 'yes');
normal.get('construction-reset').events.click();
assert.equal(normal.property('integral').value, '');
assert.equal(normal.location.search, '');
assert.equal(normal.visible().length, 6);

const shared = fixture('https://example.org/atlas/constructions.html?rank=8&m=2&q=orbifold&p_integral=no&p_simple=no');
assert.deepEqual(shared.visible(), ['R8_2_11'], 'URL filters combine on initial load');
assert.equal(shared.property('integral').value, 'no');
assert.equal(shared.property('simple').value, 'no');
shared.navigate('https://example.org/atlas/constructions.html?rank=10&p_integral=yes');
shared.events.popstate();
assert.deepEqual(shared.visible(), ['R10_1_2'], 'Browser navigation restores controls and filters');
assert.equal(shared.get('construction-rank').value, '10');

const linked = fixture('https://example.org/atlas/constructions.html?rank=6&p_integral=yes#R8_2_11');
assert.equal(linked.visible().length, 6, 'A linked entry clears conflicting filters');
assert.equal(linked.location.search, '');
assert.equal(linked.location.hash, '#R8_2_11');
assert(linked.entries.find(entry => entry.id === 'R8_2_11').scrolled);
linked.get('construction-rank').input('6');
assert.equal(linked.location.hash, '', 'Changing filters removes a now-unrelated entry fragment');
linked.navigate(linked.location.href + '#R10_1_2');
linked.events.hashchange();
assert.equal(linked.visible().length, 6);
assert(linked.entries.find(entry => entry.id === 'R10_1_2').scrolled);

const fallback = fixture('https://example.org/atlas/constructions.html?rank=6', true);
assert.equal(fallback.visible().length, 6, 'Failed enhancement must leave every static entry readable');
assert.equal(fallback.get('construction-empty').hidden, true);
assert.equal(fallback.get('construction-property-filters').hidden, true);
assert.equal(fallback.get('construction-count').textContent,
  '6 examples. All entries are displayed; filtering is unavailable.');
for (const control of ['construction-search', 'construction-rank', 'construction-m', 'construction-reset']) {
  assert(fallback.get(control).disabled, 'Unavailable filter controls must be disabled');
}
assert.equal(fallback.errors.length, 1);
assert.equal(normal.errors.length + shared.errors.length + linked.errors.length, 0);

console.log('Construction catalogue PASS: numeric ordering, search/rank/multiplicity/property filters, shared URLs, reset, empty results, fragment reveal, navigation and readable static fallback.');
