"use strict";
// Complete census directory. Tensor and band requests are bounded; old research
// identifiers remain separate aliases with coefficient-verified basis maps.
globalThis.RingCensus = (() => {
  const dataVersion = "9d4ee69795aff28d7b90";
  const base = "./data/full-census/";
  const fields = ["integral", "weakly_integral", "simple", "perfect", "pointed", "commutative", "self_dual", "multiplicity_free"];
  const codes = {excluded: 1, unitarily_realized: 2, pseudo_unitarily_realized: 3, unresolved: 4, realized: 5};
  const labels = {excluded: "Excluded over ℂ", unitarily_realized: "Unitary model", pseudo_unitarily_realized: "Pseudo-unitary model · unitarity unproved", unresolved: "Unresolved", realized: "Categorical model"};
  const profileBit = 1 << 11;
  const caches = new Map();
  let manifestPromise, profilesPromise;
  const text = (tag, value = "", className = "") => {
    const el = document.createElement(tag); el.textContent = value;
    if (className) el.className = className;
    return el;
  };
  const anchor = (label, href, className = "case-text-link") => {
    const el = text("a", label, className); el.href = href; return el;
  };
  const properties = bits => Object.fromEntries(fields.map((key, i) => [key, Boolean(bits & (1 << i))]));
  const status = bits => Object.keys(codes).find(key => codes[key] === ((bits >> 8) & 7));
  const cid = (band, index) => `C${band.rank}_${band.multiplicity}_${index}`;
  const numericOrder = (a, b) => a.rank - b.rank || a.multiplicity - b.multiplicity || a.id.localeCompare(b.id, "en", {numeric: true});

  async function digest(bytes) {
    if (!globalThis.crypto?.subtle) throw new Error("This browser cannot verify the census files. Open this HTTPS address in a current browser.");
    return [...new Uint8Array(await crypto.subtle.digest("SHA-256", bytes))].map(x => x.toString(16).padStart(2, "0")).join("");
  }
  function cached(key, loader, limit = 8) {
    if (caches.has(key)) {
      const value = caches.get(key); caches.delete(key); caches.set(key, value); return value;
    }
    const promise = loader().catch(error => {caches.delete(key); throw error;});
    caches.set(key, promise);
    while (caches.size > limit) caches.delete(caches.keys().next().value);
    return promise;
  }
  async function verified(entry) {
    return cached(entry.path + ":" + entry.sha256, async () => {
      const response = await fetch(base + entry.path + "?v=" + entry.sha256.slice(0, 20));
      if (!response.ok) throw new Error("A census file could not be loaded. Please retry or use the source dataset link.");
      const bytes = await response.arrayBuffer();
      if (bytes.byteLength !== entry.bytes || await digest(bytes) !== entry.sha256)
        throw new Error("The census file does not match this snapshot. Reload the page before continuing.");
      if (entry.encoding === "gzip") {
        if (!globalThis.fflate?.gunzipSync) throw new Error("The census decompressor could not be loaded. Please reload.");
        const decoded = fflate.gunzipSync(new Uint8Array(bytes));
        if (decoded.byteLength !== entry.uncompressed_bytes) throw new Error("Invalid decoded census file length.");
        return decoded.buffer.slice(decoded.byteOffset, decoded.byteOffset + decoded.byteLength);
      }
      return bytes;
    });
  }
  async function load() {
    if (!manifestPromise) manifestPromise = (async () => {
      const response = await fetch(base + "manifest.json?v=" + dataVersion);
      if (!response.ok) throw new Error("The complete census index could not be loaded. Please retry.");
      const manifest = await response.json();
      if (manifest.schema !== "ring-atlas/full-census/v1" || manifest.version !== dataVersion || manifest.total !== 1434042)
        throw new Error("The census index and this page are from different snapshots. Please reload.");
      return manifest;
    })().catch(error => {manifestPromise = null; throw error;});
    return manifestPromise;
  }
  async function profiles() {
    if (!profilesPromise) profilesPromise = (async () => {
      const manifest = await load();
      const payload = JSON.parse(new TextDecoder().decode(await verified(manifest.profiles)));
      return {byID: payload, byCensus: new Map(Object.entries(payload).filter(([, p]) => p.census_id).map(([id, p]) => [p.census_id, {id, ...p}]))};
    })().catch(error => {profilesPromise = null; throw error;});
    return profilesPromise;
  }
  function parseID(value) {
    const match = /^C([3-9]|1[0-2])_([1-9]\d*)_([1-9]\d*)$/i.exec(value || "");
    if (!match || match.slice(1).some(x => !Number.isSafeInteger(Number(x)))) return null;
    return {rank: Number(match[1]), multiplicity: Number(match[2]), index: Number(match[3])};
  }
  function matches(bits, query) {
    const found = status(bits);
    if (query.status === "realized" ? !["realized", "unitarily_realized", "pseudo_unitarily_realized"].includes(found)
      : query.status && query.status !== found) return false;
    return fields.every((key, index) => !query["p_" + key] || Boolean(bits & (1 << index)) === (query["p_" + key] === "yes"));
  }
  function selectedBands(manifest, query) {
    return manifest.bands.filter(b => (!query.rank || b.rank === query.rank) && (!query.m || b.multiplicity === query.m));
  }
  function matchingCount(band, query) {
    return band.histogram.reduce((total, [bits, count]) => total + (matches(bits, query) ? count : 0), 0);
  }
  async function bandRows(band) {
    const raw = await verified(band);
    if (raw.byteLength !== band.count * 6) throw new Error("Invalid band index length.");
    const view = new DataView(raw);
    return {line: index => view.getUint32(index * 6, true), bits: index => view.getUint16(index * 6 + 4, true)};
  }
  async function censusPage(manifest, query, offset, limit = 24) {
    const bands = selectedBands(manifest, query);
    const total = bands.reduce((sum, b) => sum + matchingCount(b, query), 0);
    const records = [], needed = [];
    if (offset >= total || limit <= 0) return {total, records};
    let skip = offset, remaining = limit;
    for (const band of bands) {
      const count = matchingCount(band, query);
      if (skip >= count) {skip -= count; continue;}
      const take = Math.min(remaining, count-skip);
      needed.push({band, skip, take}); remaining -= take; skip = 0;
      if (!remaining) break;
    }
    const indexes = await Promise.all(needed.map(async part => ({...part, rows: await bandRows(part.band)})));
    for (const part of indexes) {
      const {band, rows} = part;
      let skip = part.skip, remaining = part.take;
      for (let i = 0; i < band.count; i++) {
        const bits = rows.bits(i);
        if (!matches(bits, query)) continue;
        if (skip) {skip--; continue;}
        records.push({id: cid(band, i + 1), rank: band.rank, multiplicity: band.multiplicity,
          source_line: rows.line(i), flags: bits, status: status(bits), properties: properties(bits)});
        if (--remaining === 0) break;
      }
    }
    return {total, records};
  }
  async function getRecord(id) {
    const parsed = parseID(id);
    if (!parsed) throw new Error("Choose a valid census identifier, such as C4_128_1.");
    const manifest = await load();
    const band = manifest.bands.find(b => b.rank === parsed.rank && b.multiplicity === parsed.multiplicity);
    if (!band || parsed.index > band.count) throw new Error("This identifier is outside the published census bounds.");
    const rows = await bandRows(band), line = rows.line(parsed.index - 1), bits = rows.bits(parsed.index - 1);
    const rank = manifest.ranks.find(r => r.rank === parsed.rank);
    const chunkNumber = Math.floor((line - 1) / rank.chunk_size);
    const chunkHashes = new Uint8Array(await verified(rank.chunk_index));
    if (chunkHashes.byteLength !== rank.chunk_count * 36) throw new Error("Invalid tensor hash index.");
    const chunkHash = [...chunkHashes.slice(chunkNumber*36, chunkNumber*36+32)].map(x => x.toString(16).padStart(2, "0")).join("");
    const compressedBytes = new DataView(chunkHashes.buffer, chunkHashes.byteOffset).getUint32(chunkNumber*36+32, true);
    const chunk = {path: `rank${rank.rank}/${chunkNumber}.bin`, sha256: chunkHash,
      bytes: compressedBytes, encoding: rank.tensor_encoding,
      uncompressed_bytes: Math.min(rank.chunk_size, rank.count-chunkNumber*rank.chunk_size)*rank.tensor_stride};
    const view = new DataView(await verified(chunk));
    const start = ((line - 1) % rank.chunk_size) * rank.tensor_stride;
    if (start + rank.tensor_stride > view.byteLength) throw new Error("Invalid tensor chunk offset.");
    const n = parsed.rank;
    const tensor = Array.from({length: n}, (_, i) => Array.from({length: n}, (_, j) => Array.from({length: n}, (_, k) => view.getUint16(start + 2*((i*n+j)*n+k), true))));
    if (Math.max(...tensor.flat(2)) !== parsed.multiplicity || tensor.some((plane, i) => plane.some((row, j) => tensor[0][i][j] !== Number(i === j) || tensor[i][0][j] !== Number(i === j))))
      throw new Error("The tensor does not match its census band or unit convention.");
    const canonicalID = cid(band, parsed.index), directory = await profiles();
    return {id: canonicalID, rank: n, multiplicity: parsed.multiplicity, status: status(bits),
      properties: properties(bits), fusion_tensor: tensor, basis: Array.from({length: n}, (_, i) => "X" + i),
      tensor_sha256: await digest(new TextEncoder().encode(JSON.stringify(tensor))), census_record: true,
      source_line: line,
      source: Object.fromEntries(["rank", "bound", "tables_path", "tables_gz_sha256", "tables_uncompressed_sha256", "completeness"].map(key => [key, rank[key]])),
      snapshot: Object.fromEntries(["date", "census_repository", "census_commit", "classification_commit", "classification_summary"].map(key => [key, manifest[key]])),
      profile: directory.byCensus.get(canonicalID) || null};
  }
  async function getProfile(id) {
    const directory = await profiles(), entry = directory.byID[id];
    if (!entry) throw new Error("This research profile is not recorded. Search the full census directory by its C identifier.");
    const payload = JSON.parse(new TextDecoder().decode(await verified(entry)));
    if (payload.record.id !== id || payload.census?.census_id !== entry.census_id && entry.census_id !== null)
      throw new Error("The profile does not match its identifier.");
    if (await digest(new TextEncoder().encode(JSON.stringify(payload.record.fusion_tensor))) !== payload.record.tensor_sha256)
      throw new Error("The profile tensor does not match its recorded SHA-256.");
    return payload;
  }
  function download(tensor, name) {
    const url = URL.createObjectURL(new Blob([JSON.stringify(tensor) + "\n"], {type: "text/plain;charset=utf-8"}));
    const a = anchor("", url); a.download = name + ".txt"; document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  function readQuery(params) {
    const integer = key => {
      const value = params.get(key);
      if (value === null || value === "") return null;
      if (!/^[1-9]\d*$/.test(value) || !Number.isSafeInteger(Number(value))) throw new Error("Rank, multiplicity and page must be positive whole numbers.");
      return Number(value);
    };
    const query = {rank: integer("rank"), m: integer("m"), page: integer("page") || 1,
      scope: params.get("scope") === "profiles" ? "profiles" : "census",
      status: Object.hasOwn(codes, params.get("status")) ? params.get("status") : "", q: (params.get("q") || "").trim().slice(0, 200)};
    for (const field of fields) {
      const value = params.get("p_" + field);
      if (["yes", "no"].includes(value)) query["p_" + field] = value;
    }
    return query;
  }
  function metadataRows(directory, query) {
    const search = query.q.toLocaleLowerCase("en");
    return Object.entries(directory.byID).map(([id, r]) => ({id, ...r}))
      .filter(r => (!query.rank || r.rank === query.rank) && (!query.m || r.multiplicity === query.m) && matches(r.flags, query)
        && (!search || `${r.id} ${r.census_id || ""} ${r.name} ${r.search}`.toLocaleLowerCase("en").includes(search)))
      .sort(numericOrder);
  }
  async function directory() {
    const root = document.querySelector("#record-list");
    if (!root || document.body.dataset.censusDirectory !== "full") return;
    const controls = Object.fromEntries(["search", "rank", "m", "status", "scope", "previous", "next", "page", "count", "note", "reset", "form"].map(key => [key, document.querySelector("#record-" + key)]));
    let generation = 0, timer;
    try {
      const [manifest, profileDirectory] = await Promise.all([load(), profiles()]);
      let query = readQuery(new URLSearchParams(location.search));
      for (const r of [2, ...manifest.ranks.map(r => r.rank)]) {
        const option = text("option", r === 2 ? "Rank 2 · separate realizations" : "Rank " + r); option.value = String(r); controls.rank.append(option);
      }
      const syncControls = () => {
        controls.search.value = query.q; controls.rank.value = query.rank ? String(query.rank) : "";
        controls.m.value = query.m ? String(query.m) : ""; controls.status.value = query.status; controls.scope.value = query.scope;
      };
      syncControls();
      const propertyFilter = RingProperties.mount(document.querySelector("#record-property-filters"), "record-property", () => update(), new URLSearchParams(location.search));
      function collect() {
        const params = propertyFilter.applyParams(new URLSearchParams());
        for (const [key, value] of [["q", controls.search.value], ["rank", controls.rank.value], ["m", controls.m.value], ["status", controls.status.value], ["scope", controls.scope.value]])
          if (value) params.set(key, value);
        return readQuery(params);
      }
      function saveURL() {
        const url = new URL(location.href); url.search = "";
        for (const key of ["rank", "m", "status", "q"]) if (query[key]) url.searchParams.set(key, String(query[key]));
        if (query.scope === "profiles") url.searchParams.set("scope", "profiles");
        if (query.page > 1) url.searchParams.set("page", String(query.page));
        for (const field of fields) if (query["p_" + field]) url.searchParams.set("p_" + field, query["p_" + field]);
        history.replaceState(null, "", url);
      }
      function showError(error) {
        controls.count.textContent = "The requested records could not be displayed.";
        root.replaceChildren(text("p", error.message || String(error), "case-empty"));
        controls.previous.disabled = controls.next.disabled = true;
        root.setAttribute("aria-busy", "false");
      }
      async function render() {
        const request = ++generation;
        controls.previous.disabled = controls.next.disabled = true;
        root.setAttribute("aria-busy", "true"); controls.count.textContent = "Loading matching records…";
        try {
          if (query.rank !== 2 && !selectedBands(manifest, query).length) {
            const covered = query.rank && manifest.ranks.find(r => r.rank === query.rank);
            throw new Error(covered ? `Rank ${covered.rank} is released through multiplicity ${covered.bound}. This requested band is outside the published coverage; it does not mean there are zero rings.` : "This rank or multiplicity is outside the published census coverage; it does not mean there are zero rings.");
          }
          const exactCensusID = parseID(query.q);
          const searchProfiles = Boolean(query.q && !exactCensusID);
          const separateRankTwo = query.rank === 2;
          let result;
          if (query.scope === "profiles" || separateRankTwo || searchProfiles) {
            const candidates = metadataRows(profileDirectory, query);
            const rows = candidates;
            if (exactCensusID) {
              const id = `C${exactCensusID.rank}_${exactCensusID.multiplicity}_${exactCensusID.index}`;
              result = {total: rows.filter(r => r.census_id === id).length, records: rows.filter(r => r.census_id === id)};
            } else result = {total: rows.length, records: rows.slice((query.page-1)*24, query.page*24)};
          } else if (exactCensusID) {
            const band = manifest.bands.find(b => b.rank === exactCensusID.rank && b.multiplicity === exactCensusID.multiplicity);
            let record;
            if (band && exactCensusID.index <= band.count && (!query.rank || query.rank === band.rank) && (!query.m || query.m === band.multiplicity)) {
              const rows = await bandRows(band), bits = rows.bits(exactCensusID.index-1);
              if (matches(bits, query)) record = {id: cid(band, exactCensusID.index), rank: band.rank, multiplicity: band.multiplicity, flags: bits, status: status(bits)};
            }
            result = {total: record ? 1 : 0, records: record ? [record] : []};
          } else result = await censusPage(manifest, query, (query.page-1)*24);
          if (request !== generation) return;
          const pages = Math.max(1, Math.ceil(result.total/24));
          if (query.page > pages) {query.page = pages; return render();}
          saveURL();
          const profileView = query.scope === "profiles" || separateRankTwo || searchProfiles;
          controls.rank.querySelector('option[value=""]').textContent = profileView ? "All profile ranks · 2–12" : "All census ranks · 3–12";
          const population = profileView ? "matching detailed profiles" : "matching census rings";
          const start = result.total ? (query.page-1)*24+1 : 0;
          controls.count.textContent = `${result.total.toLocaleString("en-US")} ${population}${result.total ? ` · showing ${start.toLocaleString("en-US")}–${(start+result.records.length-1).toLocaleString("en-US")}` : ""}`;
          controls.note.textContent = separateRankTwo ? "These two rank-two realizations are outside the 1,434,042-ring census, which covers ranks 3–12. Rank two also has an unrestricted symbolic classification."
            : searchProfiles ? "Text searches cover documented models, criteria and research identifiers, including the separate rank-two profiles. Enter an exact C identifier to find any census ring."
            : query.scope === "profiles" ? "Detailed profiles add constructions, proofs and research history. The full census view includes every released ring, including exclusions without a detailed profile."
            : "Complete released census at the stated bounds. All eight property filters cover every ring. Detailed profiles provide additional mathematical explanations where available.";
          root.replaceChildren();
          for (const row of result.records) {
            const censusID = row.id.startsWith("C") ? row.id : row.census_id;
            const profile = row.id.startsWith("C") ? profileDirectory.byCensus.get(row.id) : row;
            const item = text("article", "", "census-card");
            const heading = text("h2", "", "census-card-title");
            heading.append(anchor(row.id, `./case.html?id=${encodeURIComponent(row.id)}`), text("span", labels[row.status], "census-status"));
            item.append(heading, text("p", `Rank ${row.rank} · exact multiplicity ${row.multiplicity}`, "case-small-note"));
            if (profile && profile.name !== profile.id) item.append(text("p", profile.name, "census-model"));
            if (profileView && censusID) item.append(text("p", "Census record: " + censusID, "case-small-note"));
            const actions = text("div", "", "case-actions");
            actions.append(anchor("Open record →", `./case.html?id=${encodeURIComponent(row.id)}`));
            if (!profileView && profile) actions.append(anchor("Detailed profile " + profile.id + " →", `./case.html?id=${encodeURIComponent(profile.id)}`));
            if (profileView && censusID) actions.append(anchor("View census basis →", `./case.html?id=${censusID}`));
            if (censusID) {
              const button = text("button", "Fusion tensor .txt ↓", "case-secondary-button"); button.type = "button";
              button.addEventListener("click", async () => {
                button.disabled = true;
                try {const ring = await getRecord(censusID); download(ring.fusion_tensor, censusID);}
                catch (error) {button.textContent = "Download failed — retry"; button.title = error.message;}
                finally {button.disabled = false;}
              }); actions.append(button);
            }
            item.append(actions); root.append(item);
          }
          if (!result.records.length) root.append(text("p", "No records match these filters. Clear the filters to browse the complete released census.", "case-empty"));
          controls.page.value = String(query.page); controls.page.max = String(pages);
          document.querySelector("#record-pages").textContent = "of " + pages.toLocaleString("en-US");
          controls.previous.disabled = query.page <= 1; controls.next.disabled = query.page >= pages;
          controls.page.disabled = !result.total;
        } catch (error) {if (request === generation) showError(error);}
        finally {if (request === generation) root.setAttribute("aria-busy", "false");}
      }
      function update() {
        clearTimeout(timer);
        try {query = collect(); query.page = 1; void render();}
        catch (error) {generation++; showError(error);}
      }
      controls.form.addEventListener("submit", event => {event.preventDefault(); update();});
      for (const control of [controls.rank, controls.status, controls.scope]) control.addEventListener("change", update);
      for (const control of [controls.search, controls.m]) control.addEventListener("input", () => {clearTimeout(timer); timer = setTimeout(update, 220);});
      const showPage = async value => {
        query.page = value; await render();
        controls.count.scrollIntoView({block: "start", behavior: "auto"});
      };
      controls.previous.addEventListener("click", () => {if (query.page > 1) void showPage(query.page-1);});
      controls.next.addEventListener("click", () => {void showPage(query.page+1);});
      const selectPage = () => {
        const value = Number(controls.page.value);
        if (Number.isSafeInteger(value) && value > 0) {void showPage(value);}
        else controls.page.value = String(query.page);
      };
      controls.page.addEventListener("change", selectPage);
      controls.page.addEventListener("keydown", event => {if (event.key === "Enter") {event.preventDefault(); selectPage();}});
      controls.reset.addEventListener("click", () => {location.href = "./records.html";});
      await render();
    } catch (error) {
      root.replaceChildren(text("p", error.message || String(error), "case-empty"));
      controls.count.textContent = "The census could not be displayed. The source datasets remain available below.";
    }
  }
  return {load, profiles, getRecord, getProfile, download, directory, fields, labels,
    properties, status, matches, selectedBands, matchingCount, censusPage, readQuery, parseID, metadataRows};
})();
if (typeof document !== "undefined" && document.body?.dataset.censusDirectory === "full") void RingCensus.directory();
