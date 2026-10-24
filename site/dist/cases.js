"use strict";
(() => {
  const $ = (selector) => document.querySelector(selector);
  const repository = "https://github.com/sebastienpalcoux/grothendieck-ring-classification";
  const params = new URLSearchParams(location.search);
  const filters = new URLSearchParams();
  const el = (tag, className = "", text = "") => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== "" && text !== undefined && text !== null) node.textContent = String(text);
    return node;
  };
  const label = (key) => String(key).replace(/_/g, " ").replace(/\bfp\b/gi, "FP").replace(/\bapprox\b/g, "(approximate)").replace(/^./, (c) => c.toUpperCase());
  const safeURL = (value) => {
    if (typeof value !== "string") return null;
    try {
      const url = new URL(value, location.href);
      return ["https:", "http:"].includes(url.protocol) ? url.href : null;
    } catch (_) { return null; }
  };
  const link = (text, href, className = "case-text-link") => {
    const node = el("a", className, text);
    const url = safeURL(href);
    if (url) node.href = url;
    return node;
  };
  const number = (value) => {
    if (value === null || value === undefined) return "Not recorded";
    if (typeof value === "object" && "re" in value && "im" in value) return `${number(value.re)} ${value.im < 0 ? "−" : "+"} ${number(Math.abs(value.im))}i`;
    if (typeof value !== "number") return String(value);
    return Number.isInteger(value) ? String(value) : String(Number(value.toPrecision(10)));
  };
  const compact = (value) => {
    if (value === null || value === undefined) return "Not recorded";
    if (typeof value === "boolean") return value ? "Yes" : "No";
    if (Array.isArray(value)) return value.length ? value.map(compact).join(", ") : "None recorded";
    if (typeof value === "object" && "re" in value && "im" in value) return number(value);
    return String(value);
  };
  const isPrimitive = (value) => value === null || typeof value !== "object" || ("re" in value && "im" in value);
  let evidenceSources = new Map();
  const sourcePath = (value) => typeof value === "string" && /^(evidence|data|supplements|verification|tools|manuscripts|site)\/[\w./+-]+$/.test(value);
  const repoURL = (path) => evidenceSources.get(path)?.url || `${repository}/blob/main/${path.split("/").map(encodeURIComponent).join("/")}`;
  function sourceLink(text, path, fallback) {
    const source = evidenceSources.get(path);
    const node = link(text, source?.packaged ? source.url : fallback || repoURL(path));
    if (source?.packaged) node.title = `${path}\n${source.restoration_note}\nRestored source SHA-256: ${source.sha256 || source.source_sha256}`;
    return node;
  }
  function restorationNote(source) {
    const note = el("p", "case-small-note", "Packaged source. After cloning the repository, run ");
    note.append(el("code", "", source.restoration_command || "python3 tools/restore_data.py"), document.createTextNode(" to restore the original path and verify its SHA-256. "));
    if (source.restoration_url) note.append(link("Restoration script ↗", source.restoration_url), document.createTextNode(" · "));
    if (source.manifest_url) note.append(link("Payload manifest ↗", source.manifest_url));
    return note;
  }
  function scalar(value) {
    if (typeof value === "string" && /^https?:\/\/\S+$/.test(value)) {
      const prefix = `${repository}/blob/main/`;
      if (value.startsWith(prefix)) {
        try {
          const path = decodeURIComponent(new URL(value).pathname.slice(new URL(prefix).pathname.length));
          if (evidenceSources.get(path)?.packaged) return sourceLink(value, path, value);
        } catch (_) { /* Preserve unrecognized source URLs verbatim. */ }
      }
      return link(value, value);
    }
    if (sourcePath(value)) return sourceLink(value, value);
    return el("span", "record-value", compact(value));
  }
  function lazyDetails(title, builder, className = "record-details", open = false) {
    const details = el("details", className);
    details.append(el("summary", "", title));
    let loaded = false;
    const populate = () => {
      if (!loaded && details.open) { loaded = true; details.append(builder()); }
    };
    details.addEventListener("toggle", populate);
    if (open) { details.open = true; populate(); }
    return details;
  }
  function structured(value) {
    if (isPrimitive(value)) return scalar(value);
    if (Array.isArray(value)) {
      if (!value.length) return el("p", "record-empty", "No entries recorded.");
      if (value.every(isPrimitive)) {
        if (value.every((v) => !sourcePath(v) && (typeof v !== "string" || v.length < 60))) return el("p", "record-array", `[${value.map(compact).join(", ")}]`);
        const list = el("ul", "record-list");
        value.forEach((item) => { const li = el("li"); li.append(scalar(item)); list.append(li); });
        return list;
      }
      const wrap = el("div", "record-group");
      value.forEach((item, i) => {
        const title = item && typeof item === "object" ? item.title || item.name || item.stage || item.id || item.criterion || item.mode : null;
        wrap.append(lazyDetails(`${i + 1}. ${title ? label(title) : "Record"}`, () => structured(item)));
      });
      return wrap;
    }
    const list = el("dl", "record-fields");
    for (const [key, item] of Object.entries(value)) {
      const row = el("div", "record-field");
      const term = el("dt");
      term.append(sourcePath(key) ? sourceLink(key, key) : document.createTextNode(label(key)));
      row.append(term);
      const dd = el("dd");
      if (isPrimitive(item) || (Array.isArray(item) && item.every(isPrimitive) && item.length <= 20)) dd.append(structured(item));
      else dd.append(lazyDetails(Array.isArray(item) ? `${item.length} entries` : "View recorded values", () => structured(item)));
      row.append(dd); list.append(row);
    }
    return list;
  }
  function fact(name, value, className = "") {
    const item = el("div", `case-fact ${className}`);
    item.append(el("dt", "", name), el("dd", "", value));
    return item;
  }
  function section(id, title, kicker) {
    const node = el("section", "case-section"); node.id = id;
    if (kicker) node.append(el("p", "eyebrow", kicker));
    node.append(el("h2", "", title));
    return node;
  }
  function dataTable(headers, rows, caption) {
    const wrap = el("div", "case-table-scroll"); wrap.tabIndex = 0;
    wrap.setAttribute("role", "region"); wrap.setAttribute("aria-label", caption);
    const table = el("table", "case-table");
    table.append(el("caption", "sr-only", caption));
    const head = el("thead"), header = el("tr");
    headers.forEach((name) => { const cell = el("th", "", name); cell.scope = "col"; header.append(cell); });
    head.append(header); table.append(head);
    const body = el("tbody");
    rows.forEach((row) => {
      const tr = el("tr");
      row.forEach((value, i) => {
        const cell = el(i ? "td" : "th");
        if (!i) cell.scope = "row";
        cell.append(value instanceof Node ? value : document.createTextNode(String(value)));
        tr.append(cell);
      }); body.append(tr);
    });
    table.append(body); wrap.append(table); return wrap;
  }
  function downloadLink(ring, className = "case-button") {
    const anchor = link("Download fusion tensor · Python .txt ↓", ring.download_url || `./downloads/fusion-tensors/${encodeURIComponent(ring.id)}.txt`, className);
    anchor.download = `${ring.id}.txt`;
    return anchor;
  }
  function recordDownload(ring) {
    const button = el("button", "case-secondary-button", "Download complete record · JSON ↓"); button.type = "button";
    button.addEventListener("click", () => {
      const url = URL.createObjectURL(new Blob([JSON.stringify(ring, null, 2) + "\n"], {type:"application/json"}));
      const anchor = el("a"); anchor.href = url; anchor.download = `${ring.id}.json`;
      document.body.append(anchor); anchor.click(); anchor.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    }); return button;
  }
  function parseFilters() {
    for (const key of ["rank", "m", "max_m"]) {
      const value = params.get(key);
      if (value === null || value === "") continue;
      if (!/^[1-9]\d*$/.test(value) || !Number.isSafeInteger(Number(value))) throw new Error(`The ${key === "rank" ? "rank" : "multiplicity"} filter must be a positive integer.`);
      filters.set(key, value);
    }
    for (const [key,value] of params) if (/^p_(integral|weakly_integral|simple|perfect|pointed|commutative|self_dual|multiplicity_free)$/.test(key) && ["yes","no"].includes(value)) filters.set(key,value);
    if (filters.has("m") && filters.has("max_m")) throw new Error("Choose either exact multiplicity or a maximum multiplicity, not both.");
  }
  function scopeText() {
    const pieces = [filters.has("rank") ? `Rank ${filters.get("rank")}` : "All ranks"];
    if (filters.has("m")) pieces.push(`exact multiplicity ${filters.get("m")}`);
    else if (filters.has("max_m")) pieces.push(`multiplicity ≤ ${filters.get("max_m")}`);
    else pieces.push("all recorded multiplicities");
    return pieces.join(" · ");
  }
  function matchesFilters(ring) {
    return (!filters.has("rank") || ring.rank === Number(filters.get("rank"))) &&
      (!filters.has("m") || ring.multiplicity === Number(filters.get("m"))) &&
      (!filters.has("max_m") || ring.multiplicity <= Number(filters.get("max_m")));
  }
  function caseURL(ring) {
    const query = new URLSearchParams(filters); query.set("id", ring.id);
    return `./case.html?${query}`;
  }
  const categoryLevels = ["general", "pivotal", "spherical", "pseudo_unitary", "unitary"];
  const categoryLabels = {general:"General", pivotal:"Pivotal", spherical:"Spherical", pseudo_unitary:"Pseudo-unitary", unitary:"Unitary"};
  function categoryExclusionText(scope, short = false) {
    if (!scope) return "Scope not yet audited";
    if (scope.strongest_excluded) return `No ${categoryLabels[scope.strongest_excluded].toLowerCase()} categorification`;
    if (scope.level_status?.unitary === "realized") return "Unitary categorification realized";
    return short ? "Unitary categorification also open" : "Without requiring a braiding, even unitary categorification remains open.";
  }
  function braidedStatusText(braided, short = false) {
    if (braided?.status === "excluded") return "No braided categorification";
    if (braided?.status === "unresolved") {
      if (short && braided.conditional_exclusions?.length) {
        const strongest = categoryLevels.find((level) => braided.conditional_exclusions.some((item) => item.assumption === level));
        const condition = strongest ? categoryLabels[strongest].toLowerCase() : String(braided.conditional_exclusions[0].assumption);
        return `Braided open · ${condition} braided excluded`;
      }
      return "Braided categorification unresolved";
    }
    return "Braided scope not yet audited";
  }
  function categoryClosure(implications) {
    const reachable = categoryLevels.map((_, i) => categoryLevels.map((_, j) => j <= i));
    for (const implication of implications) {
      const from = categoryLevels.indexOf(implication.from), to = categoryLevels.indexOf(implication.to);
      if (from < 0 || to < 0) throw new Error("Unrecognized categorification level in the recorded implications.");
      reachable[from][to] = true;
    }
    for (let k = 0; k < categoryLevels.length; k++)
      for (let i = 0; i < categoryLevels.length; i++)
        for (let j = 0; j < categoryLevels.length; j++)
          reachable[i][j] ||= reachable[i][k] && reachable[k][j];
    return reachable;
  }
  function categoryDiagram(implications, kind) {
    const reachable = categoryClosure(implications);
    const node = el("div", "category-chain"); node.setAttribute("role", "img");
    const description = [];
    categoryLevels.forEach((level, i) => {
      if (i) {
        const both = reachable[i - 1][i];
        const arrow = el("span", `category-arrow${both ? " category-equivalence" : ""}`, both ? "⇔" : "⇐");
        arrow.setAttribute("aria-hidden", "true"); node.append(arrow);
        description.push(both ? `${categoryLabels[categoryLevels[i - 1]]} is equivalent to ${categoryLabels[level]}` : `${categoryLabels[level]} implies ${categoryLabels[categoryLevels[i - 1]]}`);
      }
      const box = el("span", "category-level", categoryLabels[level]); box.setAttribute("aria-hidden", "true"); node.append(box);
    });
    node.setAttribute("aria-label", `${kind}. ${description.join(". ")}.`);
    return node;
  }
  function categorySources(sources) {
    const links = el("div", "category-source-links");
    for (const source of sources || []) {
      const href = source.url || (source.path ? repoURL(source.path) : null);
      if (!href) continue;
      const item = sourceLink(source.label || "Supporting argument ↗", source.path, href);
      if (source.locator) item.title = [item.title, source.locator].filter(Boolean).join("\n");
      links.append(item);
    }
    return links;
  }
  function renderBraidedStatus(braided) {
    const panel = el("div", `category-braided${braided?.status === "excluded" ? " category-braided-excluded" : ""}`);
    panel.append(el("h3", "", "Braided categorification"), el("p", "category-braided-status", braidedStatusText(braided)));
    if (braided?.explanation) panel.append(el("p", "case-prose", braided.explanation));
    if (braided?.sources?.length) panel.append(categorySources(braided.sources));
    if (braided?.morita?.status === "excluded") {
      panel.append(el("h4", "", "No braided Morita representative"), el("p", "case-prose", braided.morita.explanation), categorySources(braided.morita.sources));
    }
    if (braided?.status === "unresolved") {
      for (const restriction of braided.conditional_exclusions || []) {
        const condition = categoryLabels[restriction.assumption]?.toLowerCase() || String(restriction.assumption);
        const item = el("div", "category-braided-condition");
        item.append(el("h4", "", `No ${condition} braided categorification`));
        if (restriction.explanation) item.append(el("p", "case-prose", restriction.explanation));
        if (restriction.sources?.length) item.append(categorySources(restriction.sources));
        panel.append(item);
      }
    }
    panel.append(el("p", "case-small-note", "Braiding is an additional structure, separate from the hierarchy below. A braided obstruction does not exclude general categorification."));
    return panel;
  }
  function renderCategorification(ring) {
    const scope = ring.categorification_scope;
    const node = section("categorification", "Categorification status", "STRUCTURE / OBSTRUCTIONS & IMPLICATIONS");
    node.append(el("p", `category-status${scope?.strongest_excluded ? " category-status-excluded" : ""}`, categoryExclusionText(scope)));
    node.append(renderBraidedStatus(scope?.braided));
    if (!scope) return node;
    if (scope.general_status === "excluded") {
      node.append(el("p", "case-prose", "General complex categorification is excluded. This also excludes pivotal, spherical, pseudo-unitary and unitary categorification."));
      for (const note of scope.notes || []) node.append(el("p", "case-prose", note));
      node.append(categorySources(scope.audit_sources));
      return node;
    }
    const same = scope.same_category_implications || [], existence = scope.existence_implications || [];
    const realized = scope.level_status?.unitary === "realized";
    node.append(el("p", "case-prose", realized ? "A unitary model establishes general, pivotal, spherical, pseudo-unitary and unitary categorifiability. The diagrams below retain the universal implications proved for this fusion ring; they do not assert that every categorification is unitary." : "General categorifiability remains unresolved. The diagram records which additional structures a hypothetical categorification must admit."));
    if (realized && scope.model_sources?.length) node.append(categorySources(scope.model_sources));
    node.append(el("h3", "", "Structures on the same category"), categoryDiagram(same, "Structures admitted by the same category"));
    node.append(el("p", "case-small-note", "Read arrows as implications. A double arrow includes a reverse implication established for this ring. Pivotal and spherical mean that a structure can be chosen; this does not assert that every chosen pivotal structure is spherical. An absent reverse arrow means no such implication is established here."));
    const sameClosure = categoryClosure(same), existenceClosure = categoryClosure([...same, ...existence]);
    const addsExistence = categoryLevels.some((_, i) => categoryLevels.some((_, j) => existenceClosure[i][j] && !sameClosure[i][j]));
    if (addsExistence) {
      const title = existence.every((item) => /galois/i.test(item.mechanism || "")) ? "Existence after possible Galois conjugation" : "Existence of a categorification";
      node.append(el("h3", "", title), categoryDiagram([...same, ...existence], title));
      node.append(el("p", "case-small-note", "This row compares existence for the same fusion ring, allowing the stated change of category. A pseudo-unitary Galois conjugate does not make the original category pseudo-unitary or unitary."));
    }
    const argumentsList = el("div", "category-arguments");
    for (const [items, kind] of [[same, "Same category"], [existence, "Existence reduction"]]) {
      for (const implication of items) {
        const argument = el("article", "category-argument");
        argument.append(el("p", "category-argument-kind", kind), el("h4", "", implication.label || `${categoryLabels[implication.from]} ⇒ ${categoryLabels[implication.to]}`));
        if (implication.mechanism) argument.append(el("p", "case-small-note", implication.mechanism));
        if (implication.explanation) argument.append(el("p", "case-prose", implication.explanation));
        argument.append(categorySources(implication.sources)); argumentsList.append(argument);
      }
    }
    if (argumentsList.children.length) {
      const details = el("details", "record-details category-proof-details");
      details.append(el("summary", "", "Why these implications hold · arguments and references"), argumentsList);
      node.append(details);
    }
    else node.append(el("p", "case-prose", "No additional reverse implication is established in the current case audit."));
    for (const note of scope.notes || []) node.append(el("p", "case-small-note", note));
    if (scope.record_scope_note) node.append(el("p", "case-small-note", scope.record_scope_note));
    if (scope.audit_sources?.length) node.append(lazyDetails("Sources for the categorification-status audit", () => categorySources(scope.audit_sources)));
    return node;
  }
  function renderList(payload) {
    const all = [...payload.cases].sort((a, b) => a.rank - b.rank || a.multiplicity - b.multiplicity || a.id.localeCompare(b.id, "en", {numeric:true}));
    const scoped = all.filter(matchesFilters);
    $("#case-scope").textContent = `${scopeText()} · ${scoped.length} unresolved ${scoped.length === 1 ? "case" : "cases"}`;
    document.title = `${scoped.length} unresolved cases · ${scopeText()} · Ring Atlas`;
    const rankSelect = $("#case-rank");
    [...new Set([...all.map((r) => r.rank), ...(filters.has("rank") ? [Number(filters.get("rank"))] : [])])].sort((a,b) => a-b).forEach((rank) => {
      const option = el("option", "", `Rank ${rank}`); option.value = rank; rankSelect.append(option);
    });
    rankSelect.value = filters.get("rank") || "";
    $("#case-m-mode").value = filters.has("max_m") ? "max_m" : "m";
    $("#case-m").value = filters.get("m") || filters.get("max_m") || "";
    $("#case-filters").addEventListener("submit", (event) => {
      event.preventDefault(); const query = new URLSearchParams();
      if (rankSelect.value) query.set("rank", rankSelect.value);
      if ($("#case-m").value) query.set($("#case-m-mode").value, $("#case-m").value);
      for (const [key,value] of new URLSearchParams(location.search)) if (key.startsWith("p_")) query.set(key,value);
      location.assign(`./unresolved.html${query.size ? "?" + query : ""}`);
    });
    const propertyFilter = RingProperties.mount($("#case-property-filters"), "case-property", () => {const url=new URL(location.href);propertyFilter.applyParams(url.searchParams);history.replaceState(null,"",url);render();});
    const render = () => {
      const query = $("#case-search").value.trim().toLowerCase();
      const found = scoped.filter((ring) => propertyFilter.matches(ring) && (!query || JSON.stringify(ring).toLowerCase().includes(query)));
      $("#case-scope").textContent = `${scopeText()} · ${scoped.length} unresolved in range · ${found.length} matching filters`;
      $("#case-results-title").textContent = `${found.length} ${found.length === 1 ? "case" : "cases"}${query ? ` matching “${$("#case-search").value.trim()}”` : ""}`;
      const root = $("#case-list"); root.replaceChildren();
      if (!found.length) {
        root.append(el("p", "case-empty", query ? "No case matches this search within the selected range." : "No unresolved case matches the selected range and ring properties."));
        root.append(link("View all unresolved cases →", "./unresolved.html")); return;
      }
      const rows = found.map((ring) => {
        const title = el("div", "case-row-title");
        title.append(link(ring.id, caseURL(ring), "case-id-link"), el("span", "case-row-status", "General categorifiability unresolved"), el("span", "case-row-category-status", categoryExclusionText(ring.categorification_scope, true)), el("span", "case-row-braided-status", braidedStatusText(ring.categorification_scope?.braided, true)));
        const download = link("Python .txt ↓", ring.download_url || `./downloads/fusion-tensors/${encodeURIComponent(ring.id)}.txt`);
        download.download = `${ring.id}.txt`; download.setAttribute("aria-label", `Download fusion tensor for ${ring.id} as a Python list`);
        return [title, ring.rank, ring.multiplicity, ring.invariants.commutative ? "Commutative" : "Noncommutative", number(ring.invariants.global_fp_dimension_approx), download];
      });
      root.append(dataTable(["Case / open full record", "Rank", "Exact m", "Multiplication", "FP dimension ≈", "Fusion data"], rows, "Unresolved fusion rings in the selected range"));
      root.append(el("p", "case-small-note", "The global Frobenius–Perron dimensions shown here are numerical approximations. Open a case for exact algebraic presentations, all recorded invariants and research evidence."));
    };
    $("#case-search").addEventListener("input", render); render();
  }
  function renderDimensions(ring) {
    const inv = ring.invariants;
    const node = section("invariants", "Ring invariants", "02 / EXACT RING DATA & DIMENSIONS");
    const facts = el("dl", "case-facts");
    facts.append(fact("Commutative", inv.commutative ? "Yes" : "No"), fact("Unit", ring.basis[ring.unit_index || 0]),
      fact("Invertible basis objects", inv.invertible_indices.map((i) => ring.basis[i]).join(", ")),
      fact("Global FP dimension ≈", number(inv.global_fp_dimension_approx)));
    node.append(facts);
    const rows = ring.basis.map((name, i) => [name, ring.basis[inv.dual_indices[i]], inv.invertible_indices.includes(i) ? "Yes" : "No", number(inv.frobenius_perron_dimensions_approx[i])]);
    node.append(dataTable(["Basis object", "Dual", "Invertible", "FP dimension ≈"], rows, "Basis objects, duality and Frobenius–Perron dimensions"));
    node.append(el("p", "case-small-note", inv.dimensions_method || "Dimensions marked ≈ are numerical approximations."));
    if (inv.formal_codegree_polynomial) {
      node.append(el("h3", "", "Exact formal-codegree polynomial"), el("pre", "case-formula", inv.formal_codegree_polynomial), el("p", "case-small-note", "The polynomial includes multiplicities."));
    } else if (inv.central_casimir_polynomial) {
      node.append(el("h3", "", "Exact central Casimir polynomial"), el("pre", "case-formula", inv.central_casimir_polynomial), el("p", "case-small-note", "For a noncommutative block of degree d, the Casimir eigenvalue is d times its formal codegree. This is not itself the formal-codegree polynomial."));
    }
    if (inv.frobenius_perron_dimensions_exact) {
      const exactRows = inv.frobenius_perron_dimensions_exact.map((dimension, i) => [ring.basis[i], dimension.minimal_polynomial, compact(dimension.largest_real_root_interval)]);
      if (inv.global_fp_dimension_exact) exactRows.push(["Global dimension", inv.global_fp_dimension_exact.minimal_polynomial, compact(inv.global_fp_dimension_exact.largest_real_root_interval)]);
      node.append(lazyDetails("Exact FP dimensions: minimal polynomials and rational isolating intervals", () => {
        const content = el("div"); content.append(el("p", "case-small-note", inv.exact_dimension_method), dataTable(["Dimension", "Minimal polynomial", "Isolating interval endpoints"], exactRows, "Exact Frobenius–Perron dimension data")); return content;
      }));
    }
    if (inv.all_closed_based_subrings) node.append(lazyDetails("Based subrings, adjoint subring and invertible multiplication", () => {
      const content = el("div");
      content.append(el("p", "case-small-note", inv.closed_based_subrings_method));
      content.append(dataTable(["Closed based subring", "Basis objects"], inv.all_closed_based_subrings.map((indices, i) => [i + 1, indices.map((index) => ring.basis[index]).join(", ")]), "All closed based subrings"));
      content.append(el("h4", "", "Adjoint subring"), el("p", "record-array", inv.adjoint_subring_indices.map((index) => ring.basis[index]).join(", ")));
      if (inv.invertible_multiplication_table) content.append(el("h4", "", "Invertible multiplication table"), dataTable(["×", ...inv.invertible_table_labels.map((index) => ring.basis[index])], inv.invertible_multiplication_table.map((row, i) => [ring.basis[inv.invertible_table_labels[i]], ...row.map((index) => ring.basis[index])]), "Group multiplication on the invertible basis objects"));
      return content;
    }));
    if (inv.fusion_matrix_characteristic_polynomials) node.append(lazyDetails("Fusion-matrix polynomials, traces and determinants", () => dataTable(["Matrix", "Characteristic polynomial", "Trace", "Determinant"], inv.fusion_matrix_characteristic_polynomials.map((polynomial, i) => [`N${i}`, polynomial, inv.fusion_matrix_traces[i], inv.fusion_matrix_determinants[i]]), "Exact fusion-matrix invariants")));
    node.append(lazyDetails("All recorded invariant fields", () => structured(inv)));
    return node;
  }
  function renderCharacters(ring) {
    const inv = ring.invariants;
    const node = section("characters", "Characters & codegrees", "03 / EXACT EXPRESSIONS & NUMERICAL VALUES");
    const exact = inv.exact_character_presentation;
    if (exact) {
      node.append(el("h3", "", "Exact character presentation"), el("p", "case-prose", exact.instruction || ""));
      node.append(el("p", "case-small-note", exact.exact_generator || "θ = Σᵢ wᵢ χ(Xᵢ)"));
      const grid = el("dl", "case-facts"); grid.append(fact("Generator weights wᵢ", compact(exact.generator_weights))); node.append(grid);
      node.append(el("h4", "", "Primitive polynomial P(θ) = 0"), el("pre", "case-formula", exact.primitive_polynomial));
      node.append(lazyDetails("Exact basis values χ(Xᵢ) and formal codegree", () => {
        const content = el("div");
        exact.basis_values.forEach((expression, i) => { content.append(el("h4", "", `χ(${ring.basis[i]})`), el("pre", "case-formula", expression)); });
        content.append(el("h4", "", "Formal codegree"), el("pre", "case-formula", exact.codegree_value)); return content;
      }));
    }
    const characters = inv.irreducible_characters_approx;
    if (Array.isArray(characters) && characters.length) {
      node.append(el("h3", "", "Numerical irreducible characters"));
      const hasExact = characters.some((row) => row.formal_codegree_minimal_polynomial || row.formal_codegree_exact);
      const rows = characters.map((row, i) => [`χ${i + 1}`, row.degree || 1, ...row.values_approx.map(number), number(row.formal_codegree_approx), ...(hasExact ? [row.formal_codegree_exact || (row.formal_codegree_minimal_polynomial ? `${row.formal_codegree_minimal_polynomial} = 0` : "Not recorded")] : [])]);
      node.append(dataTable(["Character", "Degree", ...ring.basis.map((x) => `${x} ≈`), "Codegree ≈", ...(hasExact ? ["Exact f or polynomial"] : [])], rows, "Approximate irreducible character values and formal codegrees"));
    } else node.append(el("p", "case-prose", "A validated numerical character table is not recorded for this case."));
    if (inv.character_method) node.append(el("p", "case-small-note", inv.character_method));
    return node;
  }
  function renderTensor(ring) {
    const node = section("fusion-data", "Fusion data", "04 / INTEGER STRUCTURE CONSTANTS");
    node.append(el("p", "case-prose", "N[i][j][k] is the coefficient of Xₖ in Xᵢ · Xⱼ. The first basis object X0 is the tensor unit. The .txt file is a single Python list of lists of lists of integers, without an assignment or additional text."));
    node.append(downloadLink(ring), el("p", "case-small-note", "The download uses exactly the basis shown on this page. Basis permutations, when recorded, are included under sources and provenance."));
    const selectors = el("div", "case-matrix-controls"); selectors.setAttribute("role", "group"); selectors.setAttribute("aria-label", "Choose a fusion matrix");
    const matrix = el("div", "case-matrix"), status = el("p", "case-small-note"); status.setAttribute("aria-live", "polite");
    const select = (index) => {
      selectors.querySelectorAll("button").forEach((button, i) => { button.setAttribute("aria-pressed", String(index === i)); });
      status.textContent = `N${index}: left multiplication by ${ring.basis[index]}. Rows are Xⱼ; columns are Xₖ.`;
      matrix.replaceChildren(dataTable(["j \\ k", ...ring.basis], ring.fusion_tensor[index].map((row, j) => [ring.basis[j], ...row]), `Fusion matrix N${index}`));
    };
    ring.basis.forEach((name, i) => { const button = el("button", "case-matrix-button", `N${i}`); button.type = "button"; button.title = `Left multiplication by ${name}`; button.addEventListener("click", () => select(i)); selectors.append(button); });
    node.append(selectors, status, matrix); select(ring.rank > 1 ? 1 : 0);
    node.append(lazyDetails("View the complete Python tensor", () => el("pre", "case-tensor-literal", JSON.stringify(ring.fusion_tensor, null, 2))));
    node.append(el("h3", "", "Tensor identity"), el("p", "case-small-note", "SHA-256 of the tensor encoded as compact JSON (integer entries; no whitespace). This identifies the tensor, not the bytes of the formatted .txt download:"), el("code", "case-checksum", ring.tensor_sha256));
    return node;
  }
  function renderResearch(ring, unresolved) {
    const hasHistory = Boolean(ring.research?.length);
    const node = section("research", unresolved ? "Research record" : hasHistory ? "Model & research history" : "Models & constructions", "01 / RESULTS & RESEARCH");
    if (!unresolved) {
      if (ring.model_reference) node.append(el("p", "case-model-reference", ring.model_reference));
      if (ring.model_reference_url) node.append(link("Read the model’s cited source ↗", ring.model_reference_url));
      for (const note of ring.construction_notes || []) node.append(el("p", "case-prose", note));
      if (ring.construction_proof_file) node.append(link("Construction and proof scope ↗", repoURL(ring.construction_proof_file)));
      if (ring.alternative_models?.length) node.append(lazyDetails(`${ring.alternative_models.length} alternative model records`, () => structured(ring.alternative_models)));
      node.append(el("p", "case-small-note", "The categorical model is reported by the cited source; categorical existence is not inferred from the ring tensor alone."));
    }
    if (unresolved || hasHistory) {
      if (ring.summary) node.append(el("h3", "", "Latest case summary"), el("p", "case-prose", ring.summary));
      node.append(el("p", "case-prose", ring.status === "excluded" ? "This case is now excluded from general categorification. Earlier research records retain their historical scope; the accepted exclusion above supersedes their former unresolved status." : ring.status === "unitarily_realized" ? "This case is now realized by a unitary category. Earlier records preserve the research history, including necessary conditions and attempts made before the model was identified. The accepted construction supersedes their former unresolved status." : "General existence remains unresolved. The records below distinguish applicable criteria, searches with no conclusion, scoped obstructions and surviving necessary data. Historical stages retain their original dates and outcomes; the latest completed results take precedence where a later stage refines them."));
      node.append(el("p", "case-small-note", "The fusion tensor and derived invariants use this page’s supplied case basis. Research reports retain their cited source basis, which can differ. Consult the recorded source conventions and basis maps when comparing entries."));
      const reports = ring.research || [];
      const reportDetails = (report) => lazyDetails(report.title || label(report.source || "Research report"), () => {
          const content = el("div", "case-report-content");
          if (report.url || report.source) content.append(sourceLink(report.packaged ? "Open packaged source files ↗" : "Read the source record ↗", report.source, report.url));
          if (report.packaged) content.append(el("p", "case-source-path", report.source), restorationNote(report));
          if (report.source_sha256) content.append(el("p", "case-small-note", `Source SHA-256: ${report.source_sha256}`));
          content.append(structured(report.data)); return content;
        }, "case-report");
      if (reports.length) node.append(reportDetails(reports[0]));
      const current = reports.slice(1).filter((report) => !/^(historical|earlier)/i.test(report.title || ""));
      const historical = reports.slice(1).filter((report) => /^(historical|earlier)/i.test(report.title || ""));
      for (const [title, entries] of [["Supporting research reports", current], ["Earlier research stages", historical]]) {
        if (entries.length) node.append(lazyDetails(`${title} · ${entries.length}`, () => {
          const group = el("div", "case-report-group");
          entries.forEach((report) => group.append(reportDetails(report)));
          return group;
        }, "record-details"));
      }
      if (!(ring.research || []).length) node.append(el("p", "case-small-note", "No separate research report is included; consult the linked source records below."));
    }
    return node;
  }
  function evidenceCatalogue(ring) {
    const node = el("div", "evidence-catalogue");
    const searchLabel = el("label", "evidence-search-label", "Find a file in the complete evidence catalogue");
    const search = el("input", "evidence-search");
    search.type = "search"; search.placeholder = "Search titles, paths or ring identifiers…";
    searchLabel.append(search); node.append(searchLabel);
    const results = el("p", "case-small-note"); results.setAttribute("aria-live", "polite");
    const groups = el("div", "evidence-groups"); node.append(results, groups);
    const reports = new Set((ring.research || []).map((report) => report.source));
    const suffix = ring.id.split("_").at(-1);
    const specific = new RegExp(`(?:^|[/_.-])(?:${ring.id}|r${suffix}|${suffix})(?=$|[/_.-])`, "i");
    const category = (item) => {
      const path = item.path || "";
      if (reports.has(path) || specific.test(path)) return "Case-specific files and cited reports";
      if (new RegExp(`^(?:evidence/rank${ring.rank}[_/]|supplements/rank${ring.rank}/|manuscripts/rank${ring.rank}/)`).test(path)) return `Shared rank-${ring.rank} archive`;
      if (/^(?:data|site)\//.test(path)) return "Data, conventions and provenance";
      return "Other project archives";
    };
    const appendFiles = (entries) => {
      const container = el("div");
      const list = el("ul", "case-evidence-list"); container.append(list);
      let shown = 0;
      const more = el("button", "evidence-more", "Show more files"); more.type = "button";
      const appendNext = () => {
        const end = Math.min(shown + 40, entries.length);
        for (const item of entries.slice(shown, end)) {
          const li = el("li");
          const name = item.label && item.label !== item.path ? item.label : (item.path || item.url || "Source").split("/").at(-1);
          li.append(sourceLink(name, item.path, item.url));
          if (item.path) li.append(el("span", "case-source-path", item.path));
          if (item.packaged) li.append(el("p", "case-small-note", `Packaged source · original file SHA-256: ${item.sha256}`));
          list.append(li);
        }
        shown = end; more.hidden = shown === entries.length;
        more.textContent = `Show more files · ${entries.length - shown} remaining`;
      };
      more.addEventListener("click", appendNext); container.append(more); appendNext();
      return container;
    };
    const render = () => {
      const query = search.value.trim().toLowerCase();
      const entries = (ring.evidence || []).filter((item) => `${item.label || ""} ${item.path || ""} ${item.url || ""}`.toLowerCase().includes(query));
      results.textContent = `${entries.length.toLocaleString("en-US")} of ${(ring.evidence || []).length.toLocaleString("en-US")} recorded files. Shared and other project archives retain the full source history.`;
      groups.replaceChildren();
      for (const title of ["Case-specific files and cited reports", `Shared rank-${ring.rank} archive`, "Data, conventions and provenance", "Other project archives"]) {
        const matches = entries.filter((item) => category(item) === title);
        if (matches.length) groups.append(lazyDetails(`${title} · ${matches.length}`, () => appendFiles(matches), "record-details evidence-group", Boolean(query)));
      }
      if (!entries.length) groups.append(el("p", "case-empty", "No file matches this search."));
    };
    search.addEventListener("input", render); render();
    const packaged = (ring.evidence || []).find((item) => item.packaged);
    if (packaged) node.append(lazyDetails("Reading packaged sources and verifying checksums", () => restorationNote(packaged)));
    return node;
  }
  function renderSources(ring) {
    const node = section("sources", "Sources & provenance", "05 / COMPLETE RECORDED EVIDENCE");
    const actions = el("div", "case-source-actions");
    actions.append(link(ring.report_url ? (ring.report_label || "Research manuscript") + " ↗" : `Rank-${ring.rank} manuscript ↗`, ring.report_url || `./papers/rank${ring.rank}.pdf`), recordDownload(ring));
    node.append(actions);
    if (ring.source) node.append(lazyDetails("Census source, basis and tensor provenance", () => structured(ring.source)));
    const other = Object.fromEntries(Object.entries(ring).filter(([key]) => !["id", "rank", "multiplicity", "status", "fusion_tensor", "tensor", "tensor_sha256", "basis", "unit_index", "source", "invariants", "research", "evidence", "download_url", "categorification_scope"].includes(key)));
    if (Object.keys(other).length) node.append(lazyDetails("Additional catalogue fields and basis maps", () => structured(other)));
    const evidence = ring.evidence || [];
    if (evidence.length) {
      node.append(lazyDetails(`Complete evidence catalogue · ${evidence.length.toLocaleString("en-US")} files`, () => evidenceCatalogue(ring), "record-details evidence-library"));
    }
    return node;
  }
  function renderCase(ring, unresolved) {
    evidenceSources = new Map((ring.research || []).filter((item) => item.source).map((item) => [item.source, item]));
    for (const item of ring.evidence || []) if (item.path) evidenceSources.set(item.path, item);
    const excluded = ring.status === "excluded";
    document.title = `${ring.id} · ${excluded ? "Excluded case" : unresolved ? "Unresolved case" : ring.name} · Ring Atlas`;
    $("#case-title").textContent = ring.id;
    $("#case-kicker").textContent = `RANK ${ring.rank} · EXACT MULTIPLICITY ${ring.multiplicity} · ${excluded ? "GENERAL CATEGORIFICATION EXCLUDED" : unresolved ? "UNRESOLVED CASE" : "REALIZED RING"}`;
    $("#case-subtitle").textContent = excluded ? "Resolved by a general exclusion. The fusion data, invariants and proof remain available at this permanent case address." : unresolved ? "General categorifiability remains unresolved. Inspect the ring data, exact and numerical invariants, and the full recorded research history." : ring.status === "unitarily_realized" ? `${ring.name || ring.id} · Unitary model identified. The fusion data, invariants and full research history remain available at this permanent case address.` : `${ring.name} · ${ring.existence} model reported in the catalogue.`;
    const back = $("#case-back");
    if (excluded) {
      back.href = `./records.html?rank=${ring.rank}&m=${ring.multiplicity}`;
      back.textContent = "← Back to case records";
    } else if (unresolved) {
      back.href = `./unresolved.html${filters.size ? "?" + filters : ""}`;
      back.textContent = filters.size ? `← ${scopeText()}: unresolved cases` : "← All unresolved cases";
    } else { back.href = `./index.html?rank=${ring.rank}&m=${ring.multiplicity}#rings`; back.textContent = "← Back to realized rings"; }
    $("#case-actions").replaceChildren(downloadLink(ring), recordDownload(ring));
    const root = $("#case-detail"); root.replaceChildren();
    const notice = el("div", "case-notice");
    notice.append(el("p", "", "These records belong to the project’s current research claims. Independent human verification and Lean formalization are pending."), link("Research status and verification ↗", "./review.html")); root.append(notice);
    const nav = el("nav", "case-section-nav"); nav.setAttribute("aria-label", "Case sections");
    if (unresolved || ring.categorification_scope) nav.append(link("Categorification status", "#categorification", ""));
    [["research", unresolved ? "Research record" : ring.research?.length ? "Model & research" : "Models"], ["invariants", "Invariants"], ["characters", "Characters"], ["fusion-data", "Fusion data"], ["sources", "Sources"]].forEach(([id, title]) => nav.append(link(title, `#${id}`, "")));
    if (ring.properties) {
      const labels = [["simple","simple"],["perfect","perfect"],["pointed","pointed"],["self_dual","self-dual"],["multiplicity_free","multiplicity-free"]];
      const properties = el("p","case-small-note","Exact ring properties: " + (ring.properties.integral ? "integral" : ring.properties.weakly_integral ? "weakly integral, nonintegral" : "not weakly integral") + ", " + (ring.properties.commutative ? "commutative" : "noncommutative") + (labels.some(([key])=>ring.properties[key]) ? ", " : "") + labels.filter(([key])=>ring.properties[key]).map(([,label])=>label).join(", ") + ". ");
      properties.append(link("Definitions and filter conventions →","./theory.html#filters"));root.append(properties);
    }
    root.append(nav);
    if (unresolved || ring.categorification_scope) root.append(renderCategorification(ring));
    root.append(renderResearch(ring, unresolved), renderDimensions(ring), renderCharacters(ring), renderTensor(ring), renderSources(ring));
  }
  function renderError(message) {
    const target = $("#case-list") || $("#case-detail");
    target.replaceChildren(el("p", "case-empty", message), link("Open the unresolved case directory →", "./unresolved.html"), link("Return to the research atlas →", "./index.html#atlas"));
    if ($("#case-scope")) $("#case-scope").textContent = "The requested case list could not be displayed.";
    if ($("#case-subtitle")) $("#case-subtitle").textContent = "The requested case record could not be displayed.";
  }
  async function fetchJSON(path) {
    const response = await fetch(path);
    if (!response.ok) throw new Error("The case records could not be loaded. Please reload the page or use the data links below.");
    return response.json();
  }
  async function init() {
    try {
      parseFilters();
      const catalogue = await RingCatalogue.load();
      const unresolved = {cases: catalogue.cases.filter(r => r.status === "unresolved")};
      if (document.body.dataset.casePage === "list") { renderList(unresolved); return; }
      const id = params.get("id");
      if (!id || !/^(R\d+_\d+_\d+|F_\{\d+,\d+\})$/.test(id)) { renderError("Choose a valid case identifier from the directory, such as R8_3_982."); return; }
      const ring = catalogue.cases.find(record => record.id === id);
      if (ring) { renderCase(ring, ["unresolved", "excluded"].includes(ring.status)); return; }
      renderError(`${id} has no individual case record in this catalogue.`);
    } catch (error) { renderError(error.message || "The requested record could not be loaded."); }
  }
  init();
})();

