"use strict";
// One catalogue for every rank; source-bound research payloads remain intact.
globalThis.RingCatalogue = (() => {
  const sources = ["rank9_rank10_m1.json", "rank11_m1.json", "rank9_m2.json", "rank12_m1.json"];
  const dataVersion = "42a5e602260421acfddb";
  let pending;
  async function fetchJSON(name) {
    const response = await fetch(`./data/${name}?v=${dataVersion}`);
    if (!response.ok) throw new Error("The ring catalogue could not be loaded. Please reload the page.");
    return response.json();
  }
  function load() {
    return pending ||= Promise.all([
      fetchJSON("realized_rings.json"), fetchJSON("unresolved_cases.json"), fetchJSON("resolved_cases.json"),
      ...sources.map(fetchJSON), fetchJSON("ring_property_flags.json"),
    ]).then(([realized, unresolved, resolved, ...updates]) => {
      const properties = updates.pop();
      const attach = ring => {const entry = properties.records[ring.id]; if (!entry || entry.tensor_sha256 !== ring.tensor_sha256) throw new Error("Ring properties do not match the tensor: " + ring.id); return {...ring, properties: entry.properties};};
      const models = [...realized.records, ...updates.flatMap(p => p.cases.filter(r => ["unitarily_realized", "pseudo_unitarily_realized", "realized"].includes(r.status)))];
      const cases = new Map(models.map(r => [r.id, {...r, status: r.status || (r.existence === "unitary" ? "unitarily_realized" : "realized")} ]));
      for (const ring of [...unresolved.cases, ...resolved.cases, ...updates.flatMap(p => p.cases)]) cases.set(ring.id, ring);
      const ordered = [...cases.values()].sort((a, b) => a.rank - b.rank || a.multiplicity - b.multiplicity || a.id.localeCompare(b.id, "en", {numeric: true}));
      models.sort((a,b)=>a.rank-b.rank || a.multiplicity-b.multiplicity || a.id.localeCompare(b.id,"en",{numeric:true}));
      return {models: models.map(attach), cases: ordered.map(attach), summaries: updates.map(p => p.summary)};
    });
  }
  function mergeAtlas(state, catalogue) {
    const put = (rows, value) => {
      const index = rows.findIndex(r => r.rank === value.rank && r.multiplicity === value.multiplicity);
      if (index < 0) rows.push(value); else rows[index] = value;
    };
    for (const summary of catalogue.summaries) {
      const multiplicity = summary.multiplicity || 1;
      for (const [key, c] of Object.entries(summary.counts)) {
        const rank = Number(key), n = (c.excluded || 0) + (c.unitarily_realized || 0) + (c.unresolved || 0) + (c.pseudo_unitarily_realized || 0);
        put(state.data.rows, {rank, multiplicity, rings: n, source: summary.source_url, verification: summary.ledger_url});
        put(state.data.grothendieck_rows, {rank, multiplicity, rings: (c.unitarily_realized || 0) + (c.pseudo_unitarily_realized || 0), is_lower_bound: Boolean(c.unresolved)});
        put(state.data.classification_rows, {rank, multiplicity, rings: n, excluded_general: c.excluded || 0, realized_unitary: c.unitarily_realized || 0,
          realized_other_or_unspecified: c.pseudo_unitarily_realized || 0, realized_pseudo_unitary_unitarity_unproved: c.pseudo_unitarily_realized || 0, realized_spherical_nonpseudounitary: 0, unresolved_general: c.unresolved || 0, unassessed: 0,
          classification_coverage: c.unresolved ? "partial_classification" : "complete_classification"});
        const bands = state.data.classification_rows.filter(r => r.rank === rank).sort((a,b)=>a.multiplicity-b.multiplicity);
        let through = 0;
        for (const band of bands) {if (band.multiplicity !== through+1 || band.unresolved_general) break; through++;}
        const entry = {rank, through, analyzed_through: Math.max(...bands.map(r=>r.multiplicity)), kind: bands.some(r=>r.unresolved_general)?"partial":"complete",
          rings: bands.reduce((n,r)=>n+r.rings,0), positive: bands.reduce((n,r)=>n+r.realized_unitary+(r.realized_other_or_unspecified||0)+(r.realized_spherical_nonpseudounitary||0),0), unresolved: bands.reduce((n,r)=>n+r.unresolved_general,0),
          note: "Exact multiplicity bands have individual source-bound decisions and downloadable tensors. Necessary conditions alone are not realizations."};
        const index = state.data.scope.findIndex(r=>r.rank===rank);
        if (index<0) state.data.scope.push(entry); else state.data.scope[index]=entry;
      }
      if (summary.current_documents) state.data.current_publication_documents = summary.current_documents;
    }
    state.models = catalogue.models;
    state.data.catalogue_records = catalogue.cases;
    state.data.latest_catalogue_publication = [...catalogue.summaries].sort((a,b)=>a.date.localeCompare(b.date)).at(-1);
    if (state.data.theoretical_retry?.date >= state.data.latest_catalogue_publication.date)
      state.data.latest_catalogue_publication = state.data.theoretical_retry;
    state.data.publication_date = [state.data.snapshot, ...catalogue.summaries.map(s => s.date)].sort().at(-1);
    state.data.catalogue_papers = catalogue.summaries.map(s => {
      const ranks = Object.keys(s.counts).map(Number).sort((a,b)=>a-b), c=s.totals, m=s.multiplicity || 1;
      const stem = `rank${ranks.join("-rank")}`;
      return {rank:ranks[0],ranks,multiplicity:m,title:s.report_title || `${ranks.length>1?"Ranks":"Rank"} ${ranks.join(" and ")} multiplicity-one fusion rings`,
        subtitle:`${s.input_count} analyzed; ${c.excluded || 0} exclusions, ${c.unitarily_realized || 0} unitary models${c.pseudo_unitarily_realized ? `, ${c.pseudo_unitarily_realized} additional pseudo-unitary model (unitarity unproved)` : ""}, ${c.unresolved || 0} unresolved`,
        type:"CLASSIFICATION",slug:s.report_url.split("/").at(-1).replace(/\.pdf$/,""),sourceRef:"main",sourcePath:s.report_source || `publications/${stem}/paper/${stem}.tex`};
    }).sort((a,b)=>a.rank-b.rank || a.multiplicity-b.multiplicity);
  }
  const node = (tag, text = "", className = "") => {
    const result = document.createElement(tag); result.textContent = text;
    if (className) result.className = className;
    return result;
  };
  const anchor = (text, href) => {const result = node("a", text); result.href = href; return result;};
  async function directory() {
    if (document.body?.dataset.censusDirectory === "full") return;
    const root = document.querySelector("#record-list");
    if (!root) return;
    try {
      const catalogue = await load(), params = new URLSearchParams(location.search);
      const search = document.querySelector("#record-search"), status = document.querySelector("#record-status"), rank = document.querySelector("#record-rank"), multiplicity = document.querySelector("#record-m");
      const previous = document.querySelector("#record-previous"), next = document.querySelector("#record-next");
      const ranks = [...new Set(catalogue.cases.map(r => r.rank))];
      for (const value of ranks) {const option = node("option", `Rank ${value}`); option.value = String(value); rank.append(option);}
      rank.value = ranks.includes(Number(params.get("rank"))) ? params.get("rank") : "";
      status.value = ["excluded", "realized", "unitarily_realized", "pseudo_unitarily_realized", "unresolved"].includes(params.get("status")) ? params.get("status") : "";
      const m = Number(params.get("m")); multiplicity.value = Number.isSafeInteger(m) && m > 0 ? String(m) : "";
      search.value = (params.get("q") || "").slice(0, 500);
      const pageSize = 24; let page = 0;
      const propertyFilter = RingProperties.mount(document.querySelector("#record-property-filters"), "record-property", () => {page = 0; render();}, params);
      const render = () => {
        const query = search.value.trim().toLowerCase(), url = new URL(location.href);
        const exactM = Number(multiplicity.value), validM = Number.isSafeInteger(exactM) && exactM > 0;
        for (const [key, value] of [["rank", rank.value], ["m", validM ? String(exactM) : ""], ["status", status.value], ["q", search.value.trim()]]) {
          if (value) url.searchParams.set(key, value); else url.searchParams.delete(key);
        }
        propertyFilter.applyParams(url.searchParams);
        history.replaceState(null, "", url);
        const rows = catalogue.cases.filter(r => propertyFilter.matches(r) && (!rank.value || r.rank === Number(rank.value)) && (!validM || r.multiplicity === exactM) &&
          (!status.value || (status.value === "realized" ? ["realized", "unitarily_realized", "pseudo_unitarily_realized"].includes(r.status) : r.status === status.value)) &&
          (!query || `${r.id} ${r.name || ""} ${r.summary || ""} ${(r.research || []).map(x => JSON.stringify(x.data)).join(" ")}`.toLowerCase().includes(query)));
        const lastPage = Math.max(0, Math.ceil(rows.length / pageSize) - 1); page = Math.min(page, lastPage);
        const visible = rows.slice(page * pageSize, (page + 1) * pageSize);
        document.querySelector("#record-count").textContent = rows.length ? `${rows.length} matching records · showing ${page * pageSize + 1}–${page * pageSize + visible.length}` : "No matching records";
        previous.disabled = page === 0; next.disabled = page === lastPage; root.replaceChildren();
        for (const ring of visible) {
          const detail = node("details", "", "record-details"), heading = node("summary");
          const label = {excluded: "Excluded over ℂ", unitarily_realized: "Unitary model", pseudo_unitarily_realized: "Pseudo-unitary model · unitarity unproved", realized: "Categorical model", unresolved: "Unresolved"}[ring.status];
          heading.append(node("strong", ring.id), ` · ${label}`); detail.append(heading, node("p", ring.summary || ring.name));
          const links = node("div", "", "case-actions"), download = anchor("Fusion tensor .txt ↓", ring.download_url || `./downloads/fusion-tensors/${encodeURIComponent(ring.id)}.txt`);
          download.download = `${ring.id}.txt`;
          links.append(anchor("Open complete record →", `./case.html?id=${encodeURIComponent(ring.id)}`), download); detail.append(links); root.append(detail);
        }
      };
      for (const control of [search, status, rank, multiplicity]) control.addEventListener("input", () => {page = 0; render();});
      previous.addEventListener("click", () => {if (page > 0) {page--; render();}});
      next.addEventListener("click", () => {if (!next.disabled) {page++; render();}});
      render();
    } catch (error) {root.textContent = error.message;}
  }
  if (document.querySelector("#record-list")) directory();
  return {load, mergeAtlas};
})();
