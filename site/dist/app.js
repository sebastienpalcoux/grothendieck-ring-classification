/* Static atlas. Census, classification and model records have separate provenance. */
"use strict";

const $ = (selector) => document.querySelector(selector);
const fmt = new Intl.NumberFormat("en-US");
const state = { data: null, models: [], rank: "all", range: "20", mode: "grothendieck", selected: null, allModels: false, profile: null, profileTab: "tensor" };
const paperEntries = [
  {rank:2, title:"A short classification of complex rank-two Grothendieck rings", subtitle:"Self-contained, unrestricted classification", type:"MANUSCRIPT", slug:"rank2"},
  {rank:3, title:"Galois-averaged indicators and sphericality in rank three", subtitle:"Direct five-ring classification and sphericality", type:"MANUSCRIPT", slug:"rank3"},
  {rank:4, title:"Rank-four Grothendieck rings through multiplicity 128", subtitle:"Complete general categorification", type:"CLASSIFICATION", slug:"rank4"},
  {rank:5, title:"Rank-five Grothendieck rings through multiplicity twenty", subtitle:"Complete general classification through m = 20", type:"CLASSIFICATION", slug:"rank5"},
  {rank:6, title:"Rank-six fusion rings: categorification criteria and models through multiplicity eight", subtitle:"Categorification through multiplicity eight", type:"CLASSIFICATION", slug:"rank6"},
];
function paperSourcePath(rank,extension="pdf") {
  if (rank<=3) return `manuscripts/rank${rank}.${extension}`;
  if (rank===7) return `manuscripts/rank7/papers/manuscript.${extension}`;
  if (rank===8) return `manuscripts/rank8/paper/rank8.${extension}`;
  return `manuscripts/rank${rank}/papers/${rank===4?"finite":"manuscript"}.${extension}`;
}
function getStatus(rank,multiplicity) {
  return state.statusMap?.get(`${rank}:${multiplicity}`);
}

function element(tag, classes, content) {
  const el = document.createElement(tag);
  if (classes) el.className = classes;
  if (content !== undefined) el.textContent = content;
  return el;
}
function rankRows(data) {
  const map = new Map();
  for (const row of state.mode==="grothendieck"?data.grothendieck_rows:data.rows)
    map.set(`${row.rank}:${row.multiplicity}`, row);
  return map;
}
function ranges(data) {
  const ranks = [...new Set(data.scope.map((r) => r.rank))].sort((a,b)=>a-b);
  const max = Math.max(...data.rows.map((r) => r.multiplicity));
  return {ranks,max};
}
function renderFilters() {
  const container = $("#rank-filters");
  container.replaceChildren();
  for (const rank of ["all", ...ranges(state.data).ranks]) {
    const btn = element("button", `rank-btn ${state.rank === rank ? "active" : ""}`, rank === "all" ? "ALL" : String(rank));
    btn.type = "button";
    btn.setAttribute("aria-pressed", String(state.rank === rank));
    btn.setAttribute("aria-label", rank === "all" ? "All ranks" : `Rank ${rank}`);
    btn.addEventListener("click", () => {
      state.rank = rank;
      if (rank !== "all" && state.selected?.rank !== rank) {
        const preferred=state.data.grothendieck_rows.find((row)=>row.rank===rank &&
          (state.range==="all" || row.multiplicity<=Number(state.range)));
        const first=state.data.rows.find((row)=>row.rank===rank &&
          (state.range==="all" || row.multiplicity<=Number(state.range)));
        state.selected=state.censusMap.get(`${rank}:${preferred?.multiplicity??first?.multiplicity}`)||null;
      }
      renderFilters();
      renderTable();
      renderDetail();renderCatalogue();
    });
    container.append(btn);
  }
}
function buildCountRow(m,visibleRanks,rows,maxima) {
  const tr = element("tr");
  tr.dataset.multiplicity=String(m);
  tr.append(element("td", "", String(m).padStart(2,"0")));
  for (const rank of visibleRanks) {
    const td = element("td");
    const row = rows.get(`${rank}:${m}`);
    if (row) {
      const status=getStatus(rank,m);
      const coverage=status?.classification_coverage||"";
      const button = element("button", `count-cell ${coverage} ${state.selected?.rank===rank && state.selected?.multiplicity===m ? "selected":""}`, `${state.mode==="grothendieck" && row.is_lower_bound?"≥ ":""}${fmt.format(row.rings)}`);
      button.type = "button";
      const coverageText={"complete_classification":"complete classification","partial_classification":"partial classification","census_only":"census only"}[coverage];
      button.title = `Rank ${rank}, multiplicity ${m}: ${row.is_lower_bound && state.mode==="grothendieck"?"at least ":""}${fmt.format(row.rings)} ${state.mode==="grothendieck"?"confirmed realized Grothendieck":"censused fusion"} rings${coverageText ? `, ${coverageText}` : ""}`;
      button.setAttribute("aria-label", button.title);
      button.setAttribute("aria-pressed", String(state.selected?.rank===rank && state.selected?.multiplicity===m));
      const intensity = Math.log1p(row.rings) / Math.log1p(maxima[rank]);
      button.style.setProperty("--fill", `${Math.round(8 + intensity*24)}%`);
      button.addEventListener("click", () => {
        state.selected = state.censusMap.get(`${rank}:${m}`) || row;
        const locationUrl=new URL(window.location.href);
        locationUrl.searchParams.set("rank",String(rank));
        locationUrl.searchParams.set("m",String(m));
        history.replaceState(null,"",locationUrl);
        $("#count-table .count-cell.selected")?.classList.remove("selected");
        $("#count-table [aria-pressed='true']")?.setAttribute("aria-pressed","false");
        button.classList.add("selected");
        button.setAttribute("aria-pressed","true");
        state.allModels=false;
        $("#catalogue-scope").setAttribute("aria-pressed","false");
        $("#catalogue-scope").textContent="Show all realized rings";
        $("#catalogue-search").value="";
        renderDetail();renderCatalogue();
      });
      td.append(button);
    } else td.append(element("span", "missing", "—"));
    tr.append(td);
  }
  return tr;
}
function virtualSpacer(height,columnCount) {
  const tr=element("tr","virtual-spacer");const td=element("td");
  td.colSpan=columnCount;td.style.height=`${height}px`;
  td.setAttribute("aria-hidden","true");tr.append(td);return tr;
}
function renderTableWindow() {
  const v=state.virtual;
  if (!v) return;
  const scroll=$("#table-scroll");
  const virtual=v.bands.length>80;
  const start=virtual?Math.max(0,Math.floor(scroll.scrollTop/40)-8):0;
  const end=virtual?Math.min(v.bands.length,start+Math.ceil((scroll.clientHeight||570)/40)+18):v.bands.length;
  if (v.start===start && v.end===end) return;
  v.start=start;v.end=end;
  const fragment=document.createDocumentFragment();
  if (start) fragment.append(virtualSpacer(start*40,v.visibleRanks.length+1));
  for (let i=start;i<end;i++) fragment.append(buildCountRow(v.bands[i],v.visibleRanks,v.rows,v.maxima));
  if (end<v.bands.length) fragment.append(virtualSpacer((v.bands.length-end)*40,v.visibleRanks.length+1));
  $("#count-table tbody").replaceChildren(fragment);
}
function renderTable() {
  const {ranks,max} = ranges(state.data);
  const visibleRanks = state.rank === "all" ? ranks : [state.rank];
  const limit = state.range === "all" ? max : Math.min(Number(state.range),max);
  const rows = rankRows(state.data);
  const sourceRows=state.mode==="grothendieck"?state.data.grothendieck_rows:state.data.rows;
  const table = $("#count-table");
  const head = table.tHead;
  head.replaceChildren();
  const header = element("tr");
  header.append(element("th", "", "m"));
  for (const rank of visibleRanks) header.append(element("th", "", `RANK ${rank}`));
  head.append(header);
  const maxima = Object.fromEntries(visibleRanks.map((rank) => [rank, Math.max(1,...sourceRows.filter((r) => r.rank === rank && r.multiplicity <= limit).map((r) => r.rings))]));
  const bands=[...new Set(sourceRows.filter((r)=>r.multiplicity<=limit && visibleRanks.includes(r.rank) && r.rings>0).map((r)=>r.multiplicity))].sort((a,b)=>a-b);
  state.virtual={bands,visibleRanks,rows,maxima,start:-1,end:-1};
  table.setAttribute("aria-rowcount",String(bands.length+1));
  renderTableWindow();
  const records=sourceRows.filter((r)=>r.multiplicity<=limit && visibleRanks.includes(r.rank)).length;
  $("#table-scroll").setAttribute("aria-label",state.mode==="grothendieck"?"Grothendieck ring count table":"Fusion ring count table");
  $("#table-footer").firstElementChild.textContent = `${fmt.format(records)} recorded cells · zero-only rows omitted · exact multiplicity m · — = ${state.mode==="grothendieck"?"no realized model":"no census record"}`;
}
function appendDetailRow(container,label,value) {
  const tone=label==="Excluded"?"excluded":label==="Unresolved"?"open":label==="Realized"?"realized":"";
  const p=element("div",`detail-row ${tone}`);
  p.append(element("span","",label), element("strong","",value));
  container.append(p);
}
function appendDetailLink(container,label,value,text) {
  const p=element("div","detail-row");
  p.append(element("span","",label));
  const a=element("a","detail-value-link",text);
  a.href=value; a.target="_blank"; a.rel="noopener";
  p.append(a);
  container.append(p);
}
function renderTrend(panel,row) {
  const observations=(state.mode==="grothendieck"?state.data.grothendieck_rows:state.data.rows)
    .filter((item)=>item.rank===row.rank && Math.abs(item.multiplicity-row.multiplicity)<=5)
    .sort((a,b)=>a.multiplicity-b.multiplicity);
  if (observations.length<3) return;
  const block=element("div","trend-block");
  block.append(element("div","detail-kicker","NEARBY MULTIPLICITIES"));
  const ns="http://www.w3.org/2000/svg";
  const chart=document.createElementNS(ns,"svg");
  chart.setAttribute("viewBox","0 0 242 74");
  chart.setAttribute("role","img");
  chart.setAttribute("aria-label",`Rank ${row.rank}, multiplicities ${observations[0].multiplicity} to ${observations.at(-1).multiplicity}, counts ${observations.map((o)=>o.rings).join(", ")}`);
  const min=Math.min(...observations.map((o)=>o.rings));
  const max=Math.max(...observations.map((o)=>o.rings));
  const scale=(value)=>59-(value-min)/Math.max(1,max-min)*46;
  const points=observations.map((o,index)=>[8+index*226/(observations.length-1),scale(o.rings)]);
  const line=document.createElementNS(ns,"polyline");
  line.setAttribute("points",points.map((p)=>p.join(",")).join(" "));
  line.setAttribute("fill","none");
  line.setAttribute("stroke","#eac589");
  line.setAttribute("stroke-width","2");
  chart.append(line);
  points.forEach(([x,y],index)=>{
    if (observations[index].multiplicity!==row.multiplicity) return;
    const circle=document.createElementNS(ns,"circle");
    circle.setAttribute("cx",String(x));circle.setAttribute("cy",String(y));
    circle.setAttribute("r","4");circle.setAttribute("fill","#a8d6c5");
    chart.append(circle);
  });
  block.append(chart);
  const labels=element("div","trend-labels");
  labels.append(element("span","",`m = ${observations[0].multiplicity}`),element("span","",`m = ${observations.at(-1).multiplicity}`));
  block.append(labels);
  panel.append(block);
}
function renderDetail() {
  const panel=$("#cell-detail");
  panel.replaceChildren();
  const row=state.selected;
  if (!row) {
    panel.append(element("div","detail-kicker","SELECT A CELL"));
    panel.append(element("div","detail-number","r × m"));
    panel.append(element("p","detail-label","Inspect a rank and multiplicity."));
    panel.append(element("div","detail-rule"));
    panel.append(element("p","detail-note","Choose any number in the census to see its exact count, source, and classification scope."));
    return;
  }
  panel.append(element("div","detail-kicker",`RANK ${row.rank} / MULTIPLICITY ${row.multiplicity}`));
  const realized=state.positiveMap.get(`${row.rank}:${row.multiplicity}`)?.rings||0;
  const lowerBound=state.positiveMap.get(`${row.rank}:${row.multiplicity}`)?.is_lower_bound;
  panel.append(element("div","detail-number",`${lowerBound?"≥ ":""}${fmt.format(realized)}`));
  panel.append(element("p","detail-label",`${lowerBound?"confirmed ":""}${realized===1?"realized Grothendieck ring":"realized Grothendieck rings"}`));
  panel.append(element("div","detail-rule"));
  appendDetailRow(panel,"Fusion rings in census",fmt.format(row.rings));
  const status=getStatus(row.rank,row.multiplicity);
  const scope=state.data.scope.find((entry)=>entry.rank===row.rank);
  if (status) {
    const coverage={"complete_classification":"Complete","partial_classification":"Partial","census_only":"Census only"}[status.classification_coverage]||"Unspecified";
    appendDetailRow(panel,"Classification",coverage);
    if (status.classification_coverage!=="census_only") {
      appendDetailRow(panel,"Realized",fmt.format(realized));
      appendDetailRow(panel,"Excluded",fmt.format(status.excluded_general));
      if (status.unresolved_general) appendDetailRow(panel,"Unresolved",fmt.format(status.unresolved_general));
      if (status.realized_spherical_nonpseudounitary)
        appendDetailRow(panel,"Spherical, not pseudo-unitary",fmt.format(status.realized_spherical_nonpseudounitary));
    } else appendDetailRow(panel,"Unassessed",fmt.format(status.unassessed));
  } else if (scope?.kind==="complete" && scope.through===null) appendDetailRow(panel,"Classification","Unrestricted rank");
  else if (scope?.kind==="provisional") appendDetailRow(panel,"Classification","Revision in progress");
  else appendDetailRow(panel,"Classification","No ledger in this release");
  if (typeof row.source==="string" && /^https?:\/\//.test(row.source))
    appendDetailLink(panel,"Source",row.source,"Exact count table ↗");
  else appendDetailRow(panel,"Source",String(row.source||"Census repository"));
  if (row.verification) {
    if (/^https?:\/\//.test(String(row.verification)))
      appendDetailLink(panel,"Check",row.verification,"Audit record ↗");
    else appendDetailRow(panel,"Check",String(row.verification));
  }
  let note=lowerBound?"This positive count is a lower bound; unresolved fusion rings may also admit models.":"The realized ring count is exact for this classified band; the census includes all fusion rings.";
  if (status?.classification_coverage==="partial_classification")
    note="This realized count is a lower bound; “unresolved” means general categorification remains undecided in this release.";
  else if (status?.classification_coverage==="census_only")
    note="The census is complete for this band, but the classification ledger has not assessed its rings.";
  else if (status?.classification_coverage==="complete_classification")
    note="Each ring in this band is realized or excluded by the stated criteria.";
  panel.append(element("p","detail-note",note));
  if (realized) renderTrend(panel,row);
  if (realized) {
    const browse=element("a","detail-link",`Browse ${fmt.format(realized)} explicit ${realized===1?"ring":"rings"} ↓`);
    browse.href="#rings";panel.append(browse);
  }
  const link=element("a","detail-link","Open census source ↗");
  link.href=state.data.source_repository;
  link.target="_blank";link.rel="noopener";
  panel.append(link);
}
function renderScope() {
  const grid=$("#scope-cards");
  grid.replaceChildren();
  for (const record of state.data.scope) {
    const card=element("article","scope-card");
    card.append(element("div","scope-index",`RANK ${record.rank} / COMPLEX`));
    card.append(element("div","scope-rank",`r = ${record.rank}`));
    card.append(element("div","scope-limit",record.through===null?"UNRESTRICTED RANK":record.through>0?`COMPLETE THROUGH m ≤ ${record.through}`:"NO COMPLETE INITIAL BAND"));
    let summary;
    if (record.rings!==null && record.positive!==null)
      summary=`${record.unresolved?"≥ ":""}${fmt.format(record.positive)} realized among ${fmt.format(record.rings)} analyzed fusion rings through m ≤ ${record.analyzed_through}. ${record.unresolved?`${fmt.format(record.unresolved)} unresolved.`:""}`;
    else summary=`${fmt.format(record.positive)} realized Grothendieck rings. ${record.note||"Unrestricted classification."}`;
    card.append(element("p","scope-description",summary));
    if (record.rings!==null && record.note) card.append(element("p","scope-extra",record.note));
    grid.append(card);
  }
}
function renderPapers() {
  const release = state.data.rank6_release;
  if (release) {
    const date = new Date(release.date+"T12:00:00Z");
    const dateOptions = {day:"numeric",month:"long",year:"numeric",timeZone:"UTC"};
    $("#edition-date").textContent = date.toLocaleDateString("en-GB", {...dateOptions,month:"short"}).toUpperCase();
    $("#snapshot-date").textContent = `Research snapshot · ${date.toLocaleDateString("en-GB", dateOptions)}`;
    const frontierRows = $("#rank6-frontier-rows");
    frontierRows.replaceChildren();
    for (const record of release.research_cases || []) {
      const row = element("tr");
      const name = element("th", "", record.id);
      name.scope = "row";
      row.append(name, element("td", "", record.public_summary));
      frontierRows.append(row);
    }
    $("#rank6-frontier").hidden = !frontierRows.children.length;
    const summary = $("#rank6-release");
    summary.replaceChildren(element("strong", "", `Rank six, multiplicity at most ${release.analyzed_through}. `));
    summary.append(document.createTextNode(`${fmt.format(release.excluded)} excluded, ${release.realized} realized, ${release.unresolved} unresolved. ${release.research_summary || ""} `));
    const archive=element("a", "", "Download manuscript and certificates");
    archive.href=`./${release.archive.path}`;archive.download="";summary.append(archive);
  }
  const grid=$("#paper-grid");
  grid.replaceChildren();
  const entries=[...paperEntries];
  const r6=state.data.scope.find((x)=>x.rank===6);
  if (r6) entries.find((entry)=>entry.rank===6).subtitle=r6.unresolved
    ? `Complete to ${r6.through}; ${r6.unresolved} cases remain through ${r6.analyzed_through}`
    : `Complete through multiplicity ${r6.analyzed_through}`;
  const r7=state.data.scope.find((x)=>x.rank===7);
  const r8=state.data.scope.find((x)=>x.rank===8);
  if (r7)
    entries.push({rank:7,title:"Rank-seven Grothendieck rings: certified exclusions and models through multiplicity four",
      subtitle:`${fmt.format(r7.rings)} analyzed; ${r7.positive} models and ${r7.unresolved} general open cases`,type:"CLASSIFICATION",slug:"rank7"});
  if (r8)
    entries.push({rank:8,title:"Rank-eight Grothendieck rings through multiplicity two: criteria, models, and the unresolved frontier",
      subtitle:`${fmt.format(r8.rings)} analyzed; ${r8.positive} models and ${r8.unresolved} general open cases`,type:"CLASSIFICATION",slug:"rank8"});
  for (const paper of entries) {
    const card=element("article","paper-card");
    const content=element("div");
    const meta=element("div","paper-meta");
    meta.append(element("span","",`0${paper.rank-1} / RANK ${paper.rank}`),element("span","",paper.type));
    content.append(meta,element("h3",paper.title.length>55?"long-title":"",paper.title),element("p","",paper.subtitle));
    card.append(content);
    const actions=element("div","paper-actions");
    const manuscript=element("a","","Read manuscript ↗");
    // A local PDF is included in the deployed snapshot when available.
    manuscript.href=`./papers/${paper.slug}.pdf`;
    manuscript.dataset.localPaper=paper.slug;
    const source=element("a","","Source & verification ↗");
    source.href=`${state.data.classification_repository}/blob/${state.data.classification_commit || "main"}/${paperSourcePath(paper.rank,"tex")}`;
    source.target="_blank";source.rel="noopener";
    actions.append(manuscript);
    if (paper.rank===4) {
      const companion=element("a","","Companion ↗");
      companion.href="./papers/rank4_companion.pdf";
      const guide=element("a","","Verification guide ↗");
      guide.href="./papers/rank4_guide.pdf";
      actions.append(companion,guide);
    }
    if (paper.rank===5 || paper.rank===6) {
      const guide=element("a","","Verification guide ↗");
      guide.href=`./papers/rank${paper.rank}_guide.pdf`;
      actions.append(guide);
    }
    actions.append(source);
    card.append(actions);
    grid.append(card);
  }
}
function formatApprox(value) {
  if (typeof value==="number") return `≈ ${Number(value).toLocaleString("en-US",{maximumSignificantDigits:10})}`;
  if (value && typeof value==="object" && "re" in value)
    return `≈ ${value.re} ${value.im<0?"−":"+"} ${Math.abs(value.im)}i`;
  return "Unavailable";
}
function link(textLabel,url) {
  const a=element("a","profile-link",textLabel);
  a.href=url;a.target="_blank";a.rel="noopener noreferrer";
  return a;
}
function renderCatalogue() {
  const grid=$("#ring-cards");
  if (!grid) return;
  grid.replaceChildren();
  const chosen=state.selected;
  const all=state.allModels;
  let records=state.models.filter((r)=>all ? (state.rank==="all" || r.rank===state.rank)
                                         : chosen && r.rank===chosen.rank && r.multiplicity===chosen.multiplicity);
  const query=$("#catalogue-search").value.trim().toLowerCase();
  if (query) records=records.filter((r)=>`${r.id} ${r.name} ${r.model_reference}`.toLowerCase().includes(query));
  $("#catalogue-context").textContent=all
    ? `${records.length} realized rings ${state.rank==="all"?"across the analyzed ranks":`at rank ${state.rank}`}`
    : chosen?`Rank ${chosen.rank} · exact multiplicity ${chosen.multiplicity} · ${records.length} explicit models`:"Choose a cell above";
  if (!records.length) {
    grid.append(element("p","catalogue-empty",query?"No model matches that search.":"No realized Grothendieck rings in this band. The classification panel still records its excluded or unresolved fusion rings."));
    return;
  }
  for (const ring of records) {
    const card=element("article","ring-card");
    const meta=element("div","ring-card-meta",`RANK ${ring.rank}   /   m = ${ring.multiplicity}   /   ${ring.id}`);
    card.append(meta,element("h3","",ring.name));
    const facts=element("div","ring-card-facts");
    facts.append(element("span","",ring.existence),element("span","",ring.invariants.commutative?"commutative":"noncommutative"),
                 element("span","",`FPdim ${formatApprox(ring.invariants.global_fp_dimension_approx)}`));
    card.append(facts);
    const open=element("button","open-ring","Explore ring ↗");
    open.type="button";open.addEventListener("click",()=>openRing(ring));
    card.append(open);grid.append(card);
  }
}
function profileFact(label,value) {
  const span=element("span","profile-fact");
  span.append(element("small","",label),element("strong","",value));
  return span;
}
function matrixTable(headers,rows) {
  const wrap=element("div","profile-table-scroll");
  const table=element("table","profile-table");
  const tr=element("tr");
  tr.append(element("th","", ""));
  headers.forEach((head)=>tr.append(element("th","",head)));
  const thead=element("thead");thead.append(tr);table.append(thead);
  const tbody=element("tbody");
  rows.forEach((row,j)=>{
    const line=element("tr");line.append(element("th","",`X${j}`));
    row.forEach((value)=>line.append(element("td","",String(value))));
    tbody.append(line);
  });
  table.append(tbody);wrap.append(table);return wrap;
}
function renderRingProfile() {
  const ring=state.profile;
  if (!ring) return;
  $("#ring-kicker").textContent=`RANK ${ring.rank} · MULTIPLICITY ${ring.multiplicity} · ${ring.id}`;
  $("#ring-title").textContent=ring.name;
  const facts=$("#ring-facts");facts.replaceChildren();
  facts.append(profileFact("Model",ring.existence),profileFact("Commutativity",ring.invariants.commutative?"yes":"no"),
               profileFact("Global FP dimension",formatApprox(ring.invariants.global_fp_dimension_approx)));
  document.querySelectorAll("[data-profile-tab]").forEach((button)=>{
    const selected=button.dataset.profileTab===state.profileTab;
    button.setAttribute("aria-selected",String(selected));button.tabIndex=selected?0:-1;
  });
  const panel=$("#ring-profile");panel.replaceChildren();
  const inv=ring.invariants;
  if (state.profileTab==="tensor") {
    panel.append(element("p","profile-note","Nᵢ[j,k] is the coefficient of Xₖ in Xᵢ · Xⱼ. The full integral tensor is downloadable below."));
    const buttons=element("div","matrix-selector");
    for (let i=0;i<ring.rank;i++) {
      const btn=element("button",`matrix-btn ${state.matrixIndex===i?"active":""}`,`N${i}`);
      btn.type="button";btn.setAttribute("aria-pressed",String(state.matrixIndex===i));
      btn.addEventListener("click",()=>{state.matrixIndex=i;renderRingProfile()});buttons.append(btn);
    }
    panel.append(buttons,matrixTable(ring.basis,ring.fusion_tensor[state.matrixIndex]));
    const dl=element("button","download-tensor","Download full ring record JSON ↓");
    dl.type="button";
    dl.addEventListener("click",()=>{
      const blob=new Blob([JSON.stringify(ring,null,2)],{type:"application/json"});
      const url=URL.createObjectURL(blob);const anchor=element("a");anchor.href=url;anchor.download=`${ring.id}.json`;anchor.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
    });
    panel.append(dl,element("p","profile-note",`SHA-256 of canonical JSON tensor: ${ring.tensor_sha256}`));
  } else if (state.profileTab==="characters") {
    const overview=element("div","invariant-grid");
    overview.append(profileFact("Dual indices",inv.dual_indices.map((i)=>`X${i}`).join(", ")),
      profileFact("Invertible basis objects",inv.invertible_indices.map((i)=>`X${i}`).join(", ")),
      profileFact("FP dimensions",inv.frobenius_perron_dimensions_approx.map(formatApprox).join(" · ")));
    panel.append(overview,element("p","profile-note",inv.dimensions_method));
    if (inv.formal_codegree_polynomial)
      panel.append(profileFact("Exact formal-codegree polynomial (with multiplicity)",inv.formal_codegree_polynomial));
    else if (inv.central_casimir_polynomial)
      panel.append(profileFact("Exact central Casimir polynomial",inv.central_casimir_polynomial),
        element("p","profile-note","In a noncommutative block of degree d, its Casimir eigenvalue is d times the formal codegree. This polynomial is not itself the formal-codegree polynomial."));
    if (inv.exact_character_presentation) {
      const exact=inv.exact_character_presentation;
      const details=element("details","exact-presentation");
      details.append(element("summary","","Exact character expressions in an algebraic root θ"));
      details.append(element("p","profile-note",exact.instruction));
      details.append(profileFact("θ = Σ wᵢ χ(Xᵢ), weights",exact.generator_weights.join(", ")));
      details.append(profileFact("P(θ) = 0",exact.primitive_polynomial));
      exact.basis_values.forEach((expr,i)=>details.append(profileFact(`χ(X${i})`,expr)));
      details.append(profileFact("Formal codegree",exact.codegree_value));
      panel.append(details);
    }
    if (Array.isArray(inv.irreducible_characters_approx)) {
      const wrap=element("div","profile-table-scroll");const table=element("table","profile-table char-table");
      const hasExactCodegrees=inv.irreducible_characters_approx.some((row)=>row.formal_codegree_minimal_polynomial);
      const head=element("tr");["χ","degree",...ring.basis,"formal codegree ≈",...(hasExactCodegrees?["exact f or p(u) = 0"]:[])].forEach((x)=>head.append(element("th","",x)));
      const th=element("thead");th.append(head);table.append(th);
      const body=element("tbody");
      inv.irreducible_characters_approx.forEach((row,index)=>{
        const tr=element("tr");tr.append(element("th","",`χ${index+1}`),element("td","",String(row.degree||1)));
        row.values_approx.forEach((x)=>tr.append(element("td","",formatApprox(x))));
        tr.append(element("td","",formatApprox(row.formal_codegree_approx)));
        if (hasExactCodegrees) tr.append(element("td","",row.formal_codegree_exact||
          `${row.formal_codegree_minimal_polynomial} = 0`));
        body.append(tr);
      });
      table.append(body);wrap.append(table);panel.append(wrap);
    } else panel.append(element("p","profile-note","A validated character table for this algebra is currently unavailable."));
    panel.append(element("p","profile-note",inv.character_method));
  } else {
    panel.append(profileFact("Existence",ring.existence));
    panel.append(element("p","profile-citation",ring.model_reference));
    panel.append(link("Inspect this exact model record ↗",`${state.data.classification_repository}/blob/${state.data.classification_commit || "main"}/${ring.source_file}`));
    if (ring.model_reference_url)
      panel.append(link("Open the model's cited source ↗",ring.model_reference_url));
    panel.append(element("p","profile-note",`Source entry: ${ring.source_location}. Catalogue tensors were checked for unit, duality and associativity; existence is cited from the model source, not inferred from ring axioms.`));
    if (ring.basis_permutation_model_to_census)
      panel.append(profileFact("Model basis → census basis",ring.basis_permutation_model_to_census.join(", ")));
    if (ring.basis_permutation_census_to_model)
      panel.append(profileFact("Census basis → model basis",ring.basis_permutation_census_to_model.join(", ")));
    for (const alternative of ring.alternative_models||[]) {
      const block=element("div","alternative-model");
      block.append(element("strong","",`Alternative: ${alternative.name}`),
        element("p","profile-note",alternative.reference));
      if (alternative.basis_permutation_model_to_census)
        block.append(profileFact("Model basis → census basis",alternative.basis_permutation_model_to_census.join(", ")));
      if (alternative.basis_permutation_census_to_model)
        block.append(profileFact("Census basis → model basis",alternative.basis_permutation_census_to_model.join(", ")));
      if (alternative.source_url) block.append(link("Open alternative source ↗",alternative.source_url));
      panel.append(block);
    }
    panel.append(link(`Rank-${ring.rank} manuscript ↗`,`./papers/rank${ring.rank}.pdf`));
  }
}
function openRing(ring) {
  state.selected=state.censusMap.get(`${ring.rank}:${ring.multiplicity}`)||state.selected;
  renderTable();renderDetail();
  state.profile=ring;state.profileTab="tensor";state.matrixIndex=1;
  renderRingProfile();
  const url=new URL(location.href);url.searchParams.set("ring",ring.id);
  url.searchParams.set("rank",String(ring.rank));url.searchParams.set("m",String(ring.multiplicity));
  history.replaceState(null,"",url);
  const dialog=$("#ring-dialog");if (!dialog.open) dialog.showModal();
}
function initCatalogue() {
  $("#catalogue-scope").addEventListener("click",()=>{
    state.allModels=!state.allModels;
    $("#catalogue-scope").setAttribute("aria-pressed",String(state.allModels));
    $("#catalogue-scope").textContent=state.allModels?"Show selected band":"Show all realized rings";
    renderCatalogue();
  });
  $("#catalogue-search").addEventListener("input",renderCatalogue);
  $("#close-ring").addEventListener("click",()=>$("#ring-dialog").close());
  $("#ring-dialog").addEventListener("close",()=>{
    state.profile=null;const url=new URL(location.href);url.searchParams.delete("ring");history.replaceState(null,"",url);
  });
  const tabs=[...document.querySelectorAll("[data-profile-tab]")];
  tabs.forEach((button,index)=>{
    button.addEventListener("click",()=>{state.profileTab=button.dataset.profileTab;renderRingProfile()});
    button.addEventListener("keydown",(event)=>{
      if (!["ArrowLeft","ArrowRight","Home","End"].includes(event.key)) return;
      event.preventDefault();
      const target=event.key==="Home"?0:event.key==="End"?tabs.length-1:
        (index+(event.key==="ArrowRight"?1:-1)+tabs.length)%tabs.length;
      state.profileTab=tabs[target].dataset.profileTab;renderRingProfile();tabs[target].focus();
    });
  });
}
async function verifyLocalPapers() {
  // Avoid broken PDF links when a revision is still in progress.
  await Promise.all([...document.querySelectorAll("[data-local-paper]")].map(async (a)=>{
    try {
      const response=await fetch(a.href,{method:"HEAD"});
      if (!response.ok || !/pdf/i.test(response.headers.get("content-type")||"")) throw new Error("missing");
    } catch {
      a.href=`${state.data.classification_repository}/blob/${state.data.classification_commit || "main"}/${paperSourcePath(Number(a.dataset.localPaper.slice(4)))}`;
      a.textContent="View paper files ↗";
      a.target="_blank";a.rel="noopener";
    }
  }));
}
function initControls() {
  let pendingScroll=false;
  $("#table-scroll").addEventListener("scroll",()=>{
    if (pendingScroll)return;
    pendingScroll=true;
    requestAnimationFrame(()=>{pendingScroll=false;renderTableWindow()});
  },{passive:true});
  for (const mode of ["grothendieck","fusion"]) {
    $(`#view-${mode}`).addEventListener("click",()=>{
      state.mode=mode;
      for (const key of ["grothendieck","fusion"])
        $(`#view-${key}`).setAttribute("aria-pressed",String(key===mode));
      renderTable();renderDetail();
    });
  }
  $("#range-select").addEventListener("change",(event)=>{
    state.range=event.target.value;
    renderTable();
  });
  $("#jump-input").addEventListener("keydown",(event)=>{
    if (event.key!=="Enter") return;
    const m=Number(event.target.value);
    if (!Number.isInteger(m) || m<1) return;
    const max=ranges(state.data).max;
    if (m>max) {event.target.setCustomValidity(`Largest recorded multiplicity: ${max}`);event.target.reportValidity();return}
    event.target.setCustomValidity("");
    if (state.range!=="all" && m>Number(state.range)) {
      state.range="all";
      $("#range-select").value="all";
      renderTable();
    }
    if (state.rank!=="all") {
      const row=state.censusMap.get(`${state.rank}:${m}`);
      if (row) {state.selected=row;renderDetail();renderCatalogue()}
    }
    const index=state.virtual.bands.indexOf(m);
    if(index>=0) {
      $("#table-scroll").scrollTop=Math.max(0,index*40-80);
      renderTableWindow();
      const target=document.querySelector(`#count-table tbody tr[data-multiplicity="${m}"]`);
      target?.animate([{background:"#eac589"},{background:"transparent"}],{duration:1600});
    }
  });
}
async function start() {
  try {
    const [response,statusResponse,modelsResponse]=await Promise.all([fetch("./data/atlas.json"),fetch("./data/classification_status.json"),fetch("./data/realized_rings.json")]);
    if (!response.ok || !statusResponse.ok || !modelsResponse.ok) throw new Error(`Data HTTP ${response.status}/${statusResponse.status}/${modelsResponse.status}`);
    state.data=await response.json();
    state.data.classification_rows=(await statusResponse.json()).rows;
    state.models=(await modelsResponse.json()).records;
    if (!Array.isArray(state.data.rows) || !state.data.rows.length) throw new Error("No counts");
    state.data.rows=state.data.rows.map((r)=>({...r,rank:Number(r.rank),multiplicity:Number(r.multiplicity),rings:Number(r.rings)}));
    state.data.grothendieck_rows=(state.data.grothendieck_rows||[]).map((r)=>({...r,rank:Number(r.rank),multiplicity:Number(r.multiplicity),rings:Number(r.rings)}));
    state.censusMap=new Map(state.data.rows.map((r)=>[`${r.rank}:${r.multiplicity}`,r]));
    state.positiveMap=new Map(state.data.grothendieck_rows.map((r)=>[`${r.rank}:${r.multiplicity}`,r]));
    state.statusMap=new Map((state.data.classification_rows||[]).map((r)=>[`${r.rank}:${r.multiplicity}`,r]));
    if (state.data.census_commit) $("#source-commit").textContent=`Pinned at commit ${state.data.census_commit.slice(0,12)}.`;
    const params=new URLSearchParams(window.location.search);
    const requestedRing=params.get("ring");
    const linkedModel=requestedRing?state.models.find((r)=>r.id===requestedRing):null;
    const requestedRank=Number(params.get("rank"))||linkedModel?.rank||0;
    const requestedM=Number(params.get("m"))||linkedModel?.multiplicity||0;
    state.selected=state.censusMap.get(`${requestedRank}:${requestedM}`)
      || state.data.rows.find((r)=>r.rank===4 && r.multiplicity===1)
      || state.data.rows[0];
    if (requestedRank && state.data.scope.some((x)=>x.rank===requestedRank))state.rank=requestedRank;
    if (state.selected && requestedM>Number(state.range)) {state.range="all";$("#range-select").value="all"}
    renderFilters();renderTable();renderDetail();renderScope();renderPapers();initControls();initCatalogue();renderCatalogue();
    if (requestedRank && requestedM) {
      const index=state.virtual.bands.indexOf(requestedM);
      if(index>=0) {$("#table-scroll").scrollTop=Math.max(0,index*40-80);renderTableWindow()}
    }
    if (linkedModel) openRing(linkedModel);
    await verifyLocalPapers();
  } catch (err) {
    $("#cell-detail").textContent="The count snapshot could not be loaded. Please refresh this page.";
    $("#table-scroll").textContent=`Census data unavailable (${err.message}).`;
  }
}
start();
