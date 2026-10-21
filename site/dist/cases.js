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
  const repoURL = (path) => `${repository}/blob/main/${path.split("/").map(encodeURIComponent).join("/")}`;
  function scalar(value) {
    if (typeof value === "string" && /^https?:\/\/\S+$/.test(value)) return link(value, value);
    if (typeof value === "string" && /^(evidence|data|supplements|verification|tools|manuscripts)\/[\w./+-]+$/.test(value)) return link(value, repoURL(value));
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
        if (value.every((v) => typeof v !== "string" || v.length < 60)) return el("p", "record-array", `[${value.map(compact).join(", ")}]`);
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
      row.append(el("dt", "", label(key)));
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
      location.assign(`./unresolved.html${query.size ? "?" + query : ""}`);
    });
    const render = () => {
      const query = $("#case-search").value.trim().toLowerCase();
      const found = scoped.filter((ring) => !query || JSON.stringify(ring).toLowerCase().includes(query));
      $("#case-results-title").textContent = `${found.length} ${found.length === 1 ? "case" : "cases"}${query ? ` matching “${$("#case-search").value.trim()}”` : ""}`;
      const root = $("#case-list"); root.replaceChildren();
      if (!found.length) {
        root.append(el("p", "case-empty", query ? "No case matches this search within the selected range." : "There are no currently unresolved cases in this recorded range."));
        root.append(link("View all unresolved cases →", "./unresolved.html")); return;
      }
      const rows = found.map((ring) => {
        const title = el("div", "case-row-title");
        title.append(link(ring.id, caseURL(ring), "case-id-link"), el("span", "case-row-status", "General categorifiability unresolved"));
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
    const node = section("invariants", "Ring invariants", "01 / EXACT RING DATA & DIMENSIONS");
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
    const node = section("characters", "Characters & codegrees", "02 / EXACT EXPRESSIONS & NUMERICAL VALUES");
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
    const node = section("fusion-data", "Fusion data", "03 / INTEGER STRUCTURE CONSTANTS");
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
    const node = section("research", unresolved ? "Research record" : "Models & constructions", "04 / RECORDED RESULTS & THEIR SCOPE");
    if (unresolved) {
      if (ring.summary) node.append(el("h3", "", "Latest case summary"), el("p", "case-prose", ring.summary));
      node.append(el("p", "case-prose", "General existence remains unresolved. The records below distinguish applicable criteria, searches with no conclusion, scoped obstructions and surviving necessary data. Historical stages retain their original dates and outcomes; the latest completed results take precedence where a later stage refines them."));
      node.append(el("p", "case-small-note", "The fusion tensor and derived invariants use this page’s supplied case basis. Research reports retain their cited source basis, which can differ. Consult the recorded source conventions and basis maps when comparing entries."));
      for (const report of ring.research || []) {
        const details = lazyDetails(report.title || label(report.source || "Research report"), () => {
          const content = el("div", "case-report-content");
          if (report.url || report.source) content.append(link("Read the source record ↗", report.url || repoURL(report.source)));
          if (report.source_sha256) content.append(el("p", "case-small-note", `Source SHA-256: ${report.source_sha256}`));
          content.append(structured(report.data)); return content;
        }, "case-report");
        node.append(details);
      }
      if (!(ring.research || []).length) node.append(el("p", "case-small-note", "No separate research report is included; consult the linked source records below."));
    } else {
      if (ring.model_reference) node.append(el("p", "case-model-reference", ring.model_reference));
      if (ring.model_reference_url) node.append(link("Read the model’s cited source ↗", ring.model_reference_url));
      for (const note of ring.construction_notes || []) node.append(el("p", "case-prose", note));
      if (ring.construction_proof_file) node.append(link("Construction and proof scope ↗", repoURL(ring.construction_proof_file)));
      if (ring.alternative_models?.length) node.append(lazyDetails(`${ring.alternative_models.length} alternative model records`, () => structured(ring.alternative_models)));
      node.append(el("p", "case-small-note", "The categorical model is reported by the cited source; categorical existence is not inferred from the ring tensor alone."));
    }
    return node;
  }
  function renderSources(ring) {
    const node = section("sources", "Sources & provenance", "05 / COMPLETE RECORDED EVIDENCE");
    if (ring.source) node.append(lazyDetails("Census source, basis and tensor provenance", () => structured(ring.source), "record-details", true));
    const other = Object.fromEntries(Object.entries(ring).filter(([key]) => !["id", "rank", "multiplicity", "status", "fusion_tensor", "tensor", "tensor_sha256", "basis", "unit_index", "source", "invariants", "research", "evidence", "download_url"].includes(key)));
    if (Object.keys(other).length) node.append(lazyDetails("Additional catalogue fields and basis maps", () => structured(other), "record-details", true));
    const evidence = ring.evidence || [];
    if (evidence.length) {
      node.append(el("h3", "", `${evidence.length} evidence links`));
      const list = el("ul", "case-evidence-list");
      for (const item of evidence) {
        const li = el("li"); li.append(link(item.label || item.path || item.url, item.url || repoURL(item.path)));
        if (item.path && item.label !== item.path) li.append(el("span", "case-source-path", item.path));
        list.append(li);
      }
      node.append(list);
    }
    node.append(link(`Read the rank-${ring.rank} manuscript ↗`, `./papers/rank${ring.rank}.pdf`));
    node.append(recordDownload(ring));
    return node;
  }
  function renderCase(ring, unresolved) {
    document.title = `${ring.id} · ${unresolved ? "Unresolved case" : ring.name} · Ring Atlas`;
    $("#case-title").textContent = ring.id;
    $("#case-kicker").textContent = `RANK ${ring.rank} · EXACT MULTIPLICITY ${ring.multiplicity} · ${unresolved ? "UNRESOLVED CASE" : "REALIZED RING"}`;
    $("#case-subtitle").textContent = unresolved ? "General categorifiability remains unresolved. Inspect the ring data, exact and numerical invariants, and the full recorded research history." : `${ring.name} · ${ring.existence} model reported in the catalogue.`;
    const back = $("#case-back");
    if (unresolved) {
      back.href = `./unresolved.html${filters.size ? "?" + filters : ""}`;
      back.textContent = filters.size ? `← ${scopeText()}: unresolved cases` : "← All unresolved cases";
    } else { back.href = `./index.html?rank=${ring.rank}&m=${ring.multiplicity}#rings`; back.textContent = "← Back to realized rings"; }
    $("#case-actions").append(downloadLink(ring), recordDownload(ring));
    const root = $("#case-detail"); root.replaceChildren();
    const notice = el("div", "case-notice");
    notice.append(el("p", "", "These records belong to the project’s current research claims. Independent human verification and Lean formalization are pending."), link("Research status and verification ↗", "./review.html")); root.append(notice);
    const nav = el("nav", "case-section-nav"); nav.setAttribute("aria-label", "Case sections");
    [["invariants", "Invariants"], ["characters", "Characters"], ["fusion-data", "Fusion data"], ["research", unresolved ? "Research record" : "Models"], ["sources", "Sources"]].forEach(([id, title]) => nav.append(link(title, `#${id}`, "")));
    root.append(nav, renderDimensions(ring), renderCharacters(ring), renderTensor(ring), renderResearch(ring, unresolved), renderSources(ring));
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
      const unresolved = await fetchJSON("./data/unresolved_cases.json");
      if (document.body.dataset.casePage === "list") { renderList(unresolved); return; }
      const id = params.get("id");
      if (!id || !/^(R\d+_\d+_\d+|F_\{\d+,\d+\})$/.test(id)) { renderError("Choose a valid case identifier from the directory, such as R8_3_65."); return; }
      const found = unresolved.cases.find((ring) => ring.id === id);
      if (found) { renderCase(found, true); return; }
      const realized = await fetchJSON("./data/realized_rings.json");
      const model = realized.records.find((ring) => ring.id === id);
      if (model) { renderCase(model, false); return; }
      renderError(`${id} is not a current unresolved case or a realized ring in this catalogue.`);
    } catch (error) { renderError(error.message || "The requested record could not be loaded."); }
  }
  init();
})();
