// Exercise complete-census queries and lossless record loading without a DOM.
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import {webcrypto} from "node:crypto";
import {fileURLToPath} from "node:url";
const dist = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../dist");
const requests = [];
const context = vm.createContext({URL, URLSearchParams, TextEncoder, TextDecoder, crypto: webcrypto,
  document: {body: {dataset: {}}}, location: {search: ""}, console,
  fetch: async url => {
    const relative = url.split("?")[0].replace(/^\.\//, "");
    const raw = fs.readFileSync(path.join(dist, relative));
    requests.push({path: relative, bytes: raw.length});
    return {ok: true, json: async () => JSON.parse(raw), arrayBuffer: async () => raw.buffer.slice(raw.byteOffset, raw.byteOffset+raw.byteLength)};
  }});
vm.runInContext(fs.readFileSync(path.join(dist, "vendor/fflate-0.8.2.js"), "utf8"), context);
vm.runInContext(fs.readFileSync(path.join(dist, "census.js"), "utf8"), context);
const api = context.RingCensus, manifest = await api.load();
assert.equal(manifest.total, 1434042);
const empty = api.readQuery(new URLSearchParams());
const first = await api.censusPage(manifest, empty, 0);
assert.equal(first.total, 1434042); assert.equal(first.records.length, 24);
assert.equal(first.records[0].id, "C3_1_1");
assert(requests.every(r => !/rank\d+\/\d+\.bin$/.test(r.path)), "Directory browsing must not request tensors");
const lastOffset = Math.floor((manifest.total-1)/24)*24;
const last = await api.censusPage(manifest, empty, lastOffset);
assert.equal(last.records.length, manifest.total-lastOffset);
assert.equal(last.records.at(-1).rank, 12);
const models = await api.censusPage(manifest, {...empty, status: "realized"}, 0);
assert.equal(models.total, 530, "Rank-two realizations are separate from the finite census");
const unresolved = await api.censusPage(manifest, {...empty, status: "unresolved"}, 0);
assert.equal(unresolved.total, 10);
assert.equal(new Set(unresolved.records.map(r => r.id)).size, 10);
const rankFour = await api.censusPage(manifest, {...empty, rank: 4}, 0);
assert.equal(rankFour.total, 889530);
const propertyQueries = [
  {p_integral: "yes"}, {p_integral: "no"}, {p_weakly_integral: "yes"},
  {p_simple: "yes", p_pointed: "no", m: 1}, {p_perfect: "yes", p_commutative: "no"},
  {rank: 12, status: "pseudo_unitarily_realized"}, {rank: 9, m: 2, status: "unresolved"}
];
for (const extra of propertyQueries) {
  const query = {...empty, ...extra};
  const page = await api.censusPage(manifest, query, 0);
  assert(page.records.length <= 24);
  assert(page.records.every(r => api.matches(r.flags, query)));
  assert.equal(page.total, manifest.bands.filter(b => (!query.rank || b.rank === query.rank) && (!query.m || b.multiplicity === query.m)).reduce((sum, b) => sum + api.matchingCount(b, query), 0));
}
const integral = await api.censusPage(manifest, {...empty, p_integral: "yes"}, 0);
const nonintegral = await api.censusPage(manifest, {...empty, p_integral: "no"}, 0);
assert.equal(integral.total + nonintegral.total, manifest.total, "Both sides of a property cover the full census");
for (const name of api.fields) {
  const yes = manifest.bands.reduce((n,b) => n + api.matchingCount(b, {["p_"+name]: "yes"}), 0);
  const no = manifest.bands.reduce((n,b) => n + api.matchingCount(b, {["p_"+name]: "no"}), 0);
  assert.equal(yes+no, manifest.total, name);
}
const beforeTensor = requests.length;
const record = await api.getRecord("C4_128_1");
assert.equal(record.fusion_tensor.length, 4); assert.equal(record.multiplicity, 128);
const tensorRequests = requests.slice(beforeTensor).filter(r => /rank\d+\/\d+\.bin$/.test(r.path));
assert.equal(tensorRequests.length, 1); assert(tensorRequests[0].bytes <= 32768);
assert.equal(record.tensor_sha256.length, 64);
await assert.rejects(() => api.getRecord("C4_129_1"));
await assert.rejects(() => api.getRecord("C4_128_9999999"));
await assert.rejects(() => api.getRecord("C13_1_1"));
assert.equal(api.parseID("C4_1_9007199254740993"), null);
for (const bad of ["?rank=0", "?rank=-3", "?m=1.1", "?page=NaN"])
  assert.throws(() => api.readQuery(new URLSearchParams(bad)));
const profiles = await api.profiles();
assert.equal(Object.keys(profiles.byID).length, 3462);
assert.equal(profiles.byCensus.size, 3460);
assert.equal(profiles.byID.R2_1_1.census_id, null);
const r623 = await api.getProfile("R12_1_623");
assert.equal(r623.record.status, "pseudo_unitarily_realized");
assert.equal(r623.record.categorification_scope.level_status.unitary, "unresolved");
const c623 = await api.getRecord(r623.census.census_id);
assert.equal(c623.profile.id, "R12_1_623");
assert.equal(c623.status, "pseudo_unitarily_realized");
const nonpseudo = await api.getProfile("R6_2_124");
assert.equal(nonpseudo.record.status, "realized");
assert(!api.matches(profiles.byID.R6_2_124.flags, {status: "pseudo_unitarily_realized"}));
assert(api.matches(profiles.byID.R6_2_124.flags, {status: "realized"}));
const fib = api.metadataRows(profiles, {...empty, q: "Fibonacci"});
assert(fib.length > 0);
const lowProof = await api.getProfile("F_{1,10}");
assert(lowProof.census.census_id.startsWith("C4_1_"));
const idSearch = api.metadataRows(profiles, {...empty, q: "R10_1_189"});
assert.equal(idSearch.length, 1);
assert(requests.every(r => !/^data\/(?:rank9_m2|rank12_m1|realized_rings|resolved_cases|unresolved_cases)\.json$/.test(r.path)), "New routes never fetch full legacy tensor catalogues");
console.log("Full census browser data PASS: complete counts, every property complement, boundaries, exact IDs, profile aliases, retained mathematical scope and <=32 KB tensor fetches.");
