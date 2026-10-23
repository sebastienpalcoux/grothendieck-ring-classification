"use strict";
// An additive release: historical datasets remain unchanged and inspectable.
globalThis.Rank910 = (() => {
  let pending;
  const load = () => pending ||= fetch("./data/rank9_rank10_m1.json").then(response => {
    if (!response.ok) throw new Error("The rank-nine/ten release could not be loaded.");
    return response.json();
  });
  const node = (tag, text = "", className = "") => {
    const result = document.createElement(tag); result.textContent = text;
    if (className) result.className = className;
    return result;
  };
  const anchor = (text, href) => { const result = node("a", text); result.href = href; return result; };
  const statusLabel = status => ({excluded: "Excluded over ℂ", unitarily_realized: "Unitary model", unresolved: "Unresolved"})[status];
  function mergeAtlas(state, payload) {
    const summary = payload.summary;
    for (const rank of [9, 10]) {
      const c = summary.counts[String(rank)];
      const n = (c.excluded || 0) + (c.unitarily_realized || 0) + (c.unresolved || 0);
      state.data.rows.push({rank, multiplicity: 1, rings: n, source: summary.source_url, verification: summary.ledger_url});
      state.data.grothendieck_rows.push({rank, multiplicity: 1, rings: c.unitarily_realized || 0, is_lower_bound: Boolean(c.unresolved)});
      state.data.classification_rows.push({rank, multiplicity: 1, rings: n, excluded_general: c.excluded || 0, realized_unitary: c.unitarily_realized || 0,
        realized_other_or_unspecified: 0, realized_spherical_nonpseudounitary: 0, unresolved_general: c.unresolved || 0, unassessed: 0,
        classification_coverage: c.unresolved ? "partial_classification" : "complete_classification"});
      state.data.scope.push({rank, through: c.unresolved ? 0 : 1, analyzed_through: 1, kind: c.unresolved ? "partial" : "complete",
        rings: n, positive: c.unitarily_realized || 0, unresolved: c.unresolved || 0,
        note: "Multiplicity one only. Every supplied tensor has a case record, decision scope and downloadable fusion data."});
    }
    state.models.push(...payload.cases.filter(r => r.status === "unitarily_realized"));
    state.data.rank9_rank10_m1_update = summary;
  }
  function currentPanel(payload) {
    const root = document.querySelector("#rank9-10-current");
    if (!root) return;
    const s = payload.summary; const c = s.totals;
    const content = node("div");
    const result = node("p", `${s.input_count} supplied fusion rings: ${c.excluded || 0} excluded over ℂ, ${c.unitarily_realized || 0} unitary models, `);
    result.append(c.unresolved ? anchor(`${c.unresolved} unresolved`, "./rank9-10.html?status=unresolved") : "0 unresolved", ".");
    content.append(node("p", "23 OCTOBER 2026 · MULTIPLICITY ONE", "eyebrow"), node("h2", "Ranks nine and ten"),
      result);
    root.replaceChildren(content);
    const actions = node("div", "", "update-actions");
    actions.append(anchor("Browse all 336 case records →", "./rank9-10.html"), anchor("Read the report ↗", s.report_url), anchor("Proofs and verification ↗", s.source_url));
    if (s.archive) actions.append(anchor("Download verification package ↓", s.archive.url));
    content.append(actions);
  }
  async function directory() {
    const root = document.querySelector("#rank9-10-list");
    if (!root) return;
    try {
      const payload = await load(); currentPanel(payload);
      const search = document.querySelector("#rank9-10-search"), status = document.querySelector("#rank9-10-status"), rank = document.querySelector("#rank9-10-rank");
      const previous = document.querySelector("#rank9-10-previous"), next = document.querySelector("#rank9-10-next");
      const params = new URLSearchParams(location.search);
      status.value = ["excluded", "unitarily_realized", "unresolved"].includes(params.get("status")) ? params.get("status") : "";
      rank.value = ["9", "10"].includes(params.get("rank")) ? params.get("rank") : "";
      search.value = (params.get("q") || "").slice(0, 500);
      const pageSize = 24; let page = 0;
      const render = () => {
        const query = search.value.trim().toLowerCase();
        const url = new URL(location.href);
        for (const [key, value] of [["status", status.value], ["rank", rank.value], ["q", search.value.trim()]]) {
          if (value) url.searchParams.set(key, value); else url.searchParams.delete(key);
        }
        history.replaceState(null, "", url);
        const rows = payload.cases.filter(r => (!rank.value || r.rank === Number(rank.value)) && (!status.value || r.status === status.value) &&
          (!query || `${r.id} ${r.name} ${r.summary} ${r.research.map(x => JSON.stringify(x.data)).join(" ")}`.toLowerCase().includes(query)));
        const lastPage = Math.max(0, Math.ceil(rows.length / pageSize) - 1);
        page = Math.min(page, lastPage);
        const visible = rows.slice(page * pageSize, (page + 1) * pageSize);
        document.querySelector("#rank9-10-count").textContent = rows.length ? `${rows.length} matching records · showing ${page * pageSize + 1}–${page * pageSize + visible.length}` : "No matching records";
        previous.disabled = page === 0; next.disabled = page === lastPage;
        root.replaceChildren();
        for (const ring of visible) {
          const detail = node("details", "", "record-details"); const heading = node("summary");
          heading.append(node("strong", ring.id), ` · ${statusLabel(ring.status)}${ring.investigation_deferred ? " · investigation deferred" : ""}`);
          detail.append(heading, node("p", ring.summary));
          const links = node("div", "", "case-actions"); const download = anchor("Fusion tensor .txt ↓", ring.download_url); download.download = `${ring.id}.txt`;
          links.append(anchor("Open complete record →", `./case.html?id=${encodeURIComponent(ring.id)}`), download); detail.append(links); root.append(detail);
        }
      };
      for (const control of [search, status, rank]) control.addEventListener("input", () => { page = 0; render(); });
      previous.addEventListener("click", () => { if (page > 0) { page--; render(); } });
      next.addEventListener("click", () => { if (!next.disabled) { page++; render(); } });
      render();
    } catch (error) { root.textContent = error.message; }
  }
  if (document.querySelector("#rank9-10-list")) directory();
  return {load, mergeAtlas, currentPanel};
})();
