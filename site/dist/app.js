/* Static atlas. Census, classification and model records have separate provenance. */
"use strict";

const $ = (selector) => document.querySelector(selector);
const fmt = new Intl.NumberFormat("en-US");
const state = { data: null, models: [], rank: "all", range: "20", mode: "grothendieck", selected: null, allModels: false, profile: null, profileTab: "tensor" };
const paperEntries = [
  {rank:2, title:"A short classification of complex rank-two Grothendieck rings", subtitle:"Self-contained, unrestricted classification", type:"MANUSCRIPT", slug:"rank2"},
  {rank:3, title:"Galois-averaged indicators and sphericality in rank three", subtitle:"Direct five-ring classification and sphericality", type:"MANUSCRIPT", slug:"rank3"},
  {rank:4, title:"Grothendieck rings of general fusion categories of rank four", subtitle:"Unrestricted classification · 15 rings · automatic sphericality", type:"CLASSIFICATION", slug:"rank4"},
  {rank:5, title:"Rank-five Grothendieck rings through multiplicity twenty", subtitle:"Complete general classification through m = 20", type:"CLASSIFICATION", slug:"rank5"},
  {rank:6, title:"Rank-six fusion rings: categorification criteria and models through multiplicity nine", subtitle:"Categorification through multiplicity nine", type:"CLASSIFICATION", slug:"rank6"},
];
function paperSourcePath(rank,extension="pdf") {
  const cataloguePaper=state.data?.catalogue_papers?.find(p=>p.ranks.includes(rank));
  if (cataloguePaper) return cataloguePaper.sourcePath.replace(/\.tex$/,`.${extension}`);
  if (rank<=3) return `manuscripts/rank${rank}.${extension}`;
  if (rank===7) return `manuscripts/rank7/papers/manuscript.${extension}`;
  if (rank===8) return `manuscripts/rank8/paper/rank8.${extension}`;
  return `manuscripts/rank${rank}/papers/${rank===4?"companion":"manuscript"}.${extension}`;
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
function unresolvedUrl(filters={}) {
  const query=new URLSearchParams(Object.entries(filters).filter(([,value])=>value!==undefined));
  return `./unresolved.html${query.size?`?${query}`:""}`;
}
function linkUnresolvedText(container,text,filters={}) {
  // Link the recorded count without changing the surrounding research wording.
  const walker=document.createTreeWalker(container,NodeFilter.SHOW_TEXT);
  const matches=[];
  while (walker.nextNode()) {
    const node=walker.currentNode;
    if (!node.parentElement.closest("a") && node.textContent.includes(text)) matches.push(node);
  }
  for (const node of matches) {
    const parts=node.textContent.split(text), fragment=document.createDocumentFragment();
    parts.forEach((part,index)=>{
      if (index) {
        const anchor=element("a","unresolved-count-link",text);
        anchor.href=unresolvedUrl(filters);fragment.append(anchor);
      }
      fragment.append(document.createTextNode(part));
    });
    node.replaceWith(fragment);
  }
}
function tensorDownload(ring,classes="download-tensor") {
  const anchor=element("a",classes,"Download fusion tensor (.txt) ↓");
  anchor.href=`./downloads/fusion-tensors/${encodeURIComponent(ring.id)}.txt`;
  anchor.download=`${ring.id}.txt`;
  anchor.setAttribute("aria-label",`Download ${ring.id} fusion tensor as a Python list (.txt)`);
  return anchor;
}
function censusRows(data=state.data) {
  return state.fusionRows || data.rows;
}
function visibleCountRows(data=state.data) {
  return state.mode==="grothendieck" ? data.grothendieck_rows : censusRows(data);
}
async function loadFusionCounts() {
  if (state.fusionRequest) return state.fusionRequest;
  state.fusionRequest=(async()=>{
    const root="https://github.com/sebastienpalcoux/fusion-ring-census";
    const notice=$("#fusion-census-status");
    try {
      const response=await fetch("https://raw.githubusercontent.com/sebastienpalcoux/fusion-ring-census/main/results/census.json");
      if (!response.ok) throw new Error("Census HTTP "+response.status);
      const manifest=await response.json();
      if (!manifest.ranks || typeof manifest.ranks!=="object") throw new Error("Invalid census manifest");
      const merged=new Map(state.data.rows.map(row=>[`${row.rank}:${row.multiplicity}`,row]));
      for (const [key,item] of Object.entries(manifest.ranks)) {
        const rank=Number(key),counts=Object.entries(item.counts||{});
        if (!Number.isInteger(rank) || rank<2 || !item.complete || !item.verified ||
            !Number.isInteger(item.bound) || item.bound<1 || counts.length!==item.bound ||
            counts.some(([m,n])=>!Number.isInteger(Number(m)) || Number(m)<1 || Number(m)>item.bound || !Number.isSafeInteger(n) || n<0) ||
            counts.reduce((sum,[,n])=>sum+n,0)!==item.classes) throw new Error("Uncertified census band");
        for (const [m,rings] of counts) merged.set(`${rank}:${Number(m)}`,{
          rank,multiplicity:Number(m),rings,source:`${root}/blob/main/results/counts.csv`,
          verification:`${root}/tree/main/verification/rank${rank}`,
          tensor_download:`${root}/raw/refs/heads/main/${item.tables}`
        });
      }
      state.fusionRows=[...merged.values()];
      state.censusMap=new Map(state.fusionRows.map(row=>[`${row.rank}:${row.multiplicity}`,row]));
      if (notice) {notice.textContent=`Current fusion-ring census · release ${manifest.release_date}. Categorification uses the separate classification ledger.`;notice.hidden=false;}
    } catch (error) {
      if (notice) {notice.textContent="The live census could not be loaded; the bundled fusion-count snapshot is shown.";notice.hidden=false;}
    }
  })();
  return state.fusionRequest;
}
function normalizeCountSelection() {
  const ranks=ranges(state.data).ranks;
  if (state.rank!=="all" && !ranks.includes(state.rank)) state.rank="all";
  if (state.selected && !ranks.includes(state.selected.rank)) state.selected=null;
}
function rankRows(data) {
  const map = new Map();
  for (const row of visibleCountRows(data))
    map.set(`${row.rank}:${row.multiplicity}`, row);
  return map;
}
function ranges(data) {
  const ranks = [...new Set(state.mode==="grothendieck" ? data.scope.map(r=>r.rank) : censusRows(data).map(r=>r.rank))].sort((a,b)=>a-b);
  const max = Math.max(...visibleCountRows(data).map(r=>r.multiplicity));
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
        const preferred=visibleCountRows().find((row)=>row.rank===rank &&
          (state.range==="all" || row.multiplicity<=Number(state.range)));
        const first=censusRows().find((row)=>row.rank===rank &&
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
      button.title = `Rank ${rank}, multiplicity ${m}: ${row.is_lower_bound && state.mode==="grothendieck"?"at least ":""}${fmt.format(row.rings)} ${state.mode==="grothendieck"?"reported realized Grothendieck":"censused fusion"} rings${coverageText ? `, ${coverageText}` : ""}`;
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
  const sourceRows=visibleCountRows();
  const table = $("#count-table");
  const head = table.tHead;
  head.replaceChildren();
  const header = element("tr");
  header.append(element("th", "", "m"));
  for (const rank of visibleRanks) header.append(element("th", "", `RANK ${rank}`));
  for (const heading of header.children) heading.scope = "col";
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
  const observations=visibleCountRows()
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
  const status=getStatus(row.rank,row.multiplicity);
  const scope=state.data.scope.find((entry)=>entry.rank===row.rank);
  const assessed=Boolean((status && status.classification_coverage!=="census_only") ||
    state.positiveMap.has(`${row.rank}:${row.multiplicity}`) || scope?.kind==="unrestricted");
  const realized=state.positiveMap.get(`${row.rank}:${row.multiplicity}`)?.rings||0;
  const lowerBound=state.positiveMap.get(`${row.rank}:${row.multiplicity}`)?.is_lower_bound;
  panel.append(element("div","detail-number",state.mode==="fusion"?fmt.format(row.rings):`${lowerBound?"≥ ":""}${fmt.format(realized)}`));
  panel.append(element("p","detail-label",state.mode==="fusion"?"censused fusion rings":`reported ${realized===1?"realized Grothendieck ring":"realized Grothendieck rings"}`));
  panel.append(element("div","detail-rule"));
  appendDetailRow(panel,"Fusion rings in census",fmt.format(row.rings));
  if (status) {
    const coverage={"complete_classification":"Complete","partial_classification":"Partial","census_only":"Census only"}[status.classification_coverage]||"Unspecified";
    appendDetailRow(panel,"Classification",coverage);
    if (status.classification_coverage!=="census_only") {
      appendDetailRow(panel,"Realized",fmt.format(realized));
      appendDetailRow(panel,"Excluded",fmt.format(status.excluded_general));
      if (status.unresolved_general) {
        const openRow=element("div","detail-row open");
        const openLink=element("a","unresolved-count-link",fmt.format(status.unresolved_general));
        openLink.href=unresolvedUrl({rank:row.rank,m:row.multiplicity});
        openLink.setAttribute("aria-label",`Browse ${status.unresolved_general} unresolved cases at rank ${row.rank}, multiplicity ${row.multiplicity}`);
        openRow.append(element("span","","Unresolved"),openLink);panel.append(openRow);
      }
      if (status.realized_pseudo_unitary_unitarity_unproved)
        appendDetailRow(panel,"Pseudo-unitary · unitarity unproved",fmt.format(status.realized_pseudo_unitary_unitarity_unproved));
      if (status.realized_spherical_nonpseudounitary)
        appendDetailRow(panel,"Spherical, not pseudo-unitary",fmt.format(status.realized_spherical_nonpseudounitary));
    } else appendDetailRow(panel,"Unassessed",fmt.format(status.unassessed));
  } else if (scope?.kind==="unrestricted") appendDetailRow(panel,"Classification","Unrestricted rank");
  else if (scope?.kind==="provisional") appendDetailRow(panel,"Classification","Revision in progress");
  else appendDetailRow(panel,"Classification","Categorification not assessed");
  if (row.tensor_download) appendDetailLink(panel,"Data",row.tensor_download,"Download census tensors (.gz) ↓");
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
  if (!assessed) note="Categorification has not been assessed for this census band. No model or exclusion count is asserted.";
  panel.append(element("p","detail-note",note));
  if (realized) renderTrend(panel,row);
  if (realized) {
    const browse=element("a","detail-link",`Browse ${fmt.format(realized)} explicit ${realized===1?"ring":"rings"} ↓`);
    browse.href="#rings";panel.append(browse);
  }
  const records=element("a","detail-link","Browse recorded cases →");
  records.href=`./records.html?rank=${row.rank}&m=${row.multiplicity}`;
  panel.append(records);
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
    const description=element("p","scope-description",summary);
    if (record.unresolved) linkUnresolvedText(description,`${fmt.format(record.unresolved)} unresolved`,{rank:record.rank,max_m:record.analyzed_through});
    card.append(description);
    if (record.rings!==null && record.note) card.append(element("p","scope-extra",record.note));
    grid.append(card);
  }
}
function renderTheoreticalUpdate() {
  const update = state.data.theoretical_update;
  const notice = $("#research-update");
  const details = $("#theoretical-update");
  notice.hidden = details.hidden = !update;
  if (!update) return;
  const m3 = state.data.rank8_m3_update;
  const currentRemaining = {};
  if (state.data.remaining_ids?.length) {
    for (const id of state.data.remaining_ids) {
      const rank = id.match(/^R(\d+)_/)?.[1];
      if (rank) currentRemaining[rank] = (currentRemaining[rank] || 0) + 1;
    }
  } else {
    for (const row of state.data.scope) if (row.unresolved) currentRemaining[row.rank] = row.unresolved;
  }
  const totalOpen = Object.values(currentRemaining).reduce((a,b)=>a+b,0);
  const rankNames = {"6":"rank-six", "7":"rank-seven", "8":"rank-eight", "9":"rank-nine", "10":"rank-ten"};
  const openText = Object.entries(currentRemaining).filter(([,n])=>n).map(([rank,n])=>`${n} ${rankNames[rank] || `rank-${rank}`}`).join(", ");
  const scopeText = `General existence remains open for ${openText} rings. ` +
    (m3 ? `The rank-eight multiplicity-three band has ${fmt.format(m3.excluded)} general exclusions, ${m3.unitarily_realized} unitary models and ${m3.unresolved} unresolved cases. ` : "") +
    "R8_3_1768 is excluded by pivotal conjugation parity and the complete necessary indicator system. The other current restrictions do not provide another category or general exclusion.";
  $("#research-update-title").textContent = `Current classification · ${totalOpen} open cases`;
  $("#theoretical-update-heading").textContent = `Current proofs · ${totalOpen} open cases`;
  $("#research-update-summary").textContent = scopeText;
  $("#theoretical-update-scope").textContent = scopeText + " The current proof notes distinguish the inherited categorical premises, exact certificates, and remaining gaps.";
  for (const selector of ["#research-update-title", "#theoretical-update-heading"]) linkUnresolvedText($(selector), `${totalOpen} open cases`);
  for (const container of [$("#research-update-summary"),$("#theoretical-update-scope")]) {
    if (m3?.unresolved) linkUnresolvedText(container,`${m3.unresolved} unresolved cases`,{rank:8,m:3});
    for (const [rank,count] of Object.entries(currentRemaining)) if (count) linkUnresolvedText(container,`${count} ${rankNames[rank] || `rank-${rank}`}`,{rank});
  }
  const base = `${state.data.classification_repository}/blob/main/evidence/frontier/README.md`;
  $("#latest-research-source").href = base;
  $("#latest-research-source").textContent = "Current proofs and remaining cases ↗";
  const actions = $("#theoretical-update-actions");
  actions.replaceChildren();
  const archive = element("a", "", "Current proofs and exact checks · ZIP ↓");
  archive.href = "./downloads/Fusion-Ring-Frontier-Proofs-and-Checks.zip"; archive.download = "";
  const remaining = element("a", "", "Current open tensors · Python ↓");
  remaining.href = "./downloads/current_remaining_cases.py"; remaining.download = "";
  const source = element("a", "", "Proof notes and commands ↗"); source.href = base;
  const review = element("a", "", "Research status & verification ↗"); review.href = "./review.html";
  actions.append(archive, remaining, source, review);
  const rows = $("#theoretical-update-rows");
  rows.replaceChildren();
  const ids = [...new Set(["R8_3_1768", ...(state.data.remaining_ids || [])])].sort((a,b)=>a.localeCompare(b, "en", {numeric:true}));
  for (const id of ids) {
    const row = element("tr"); const name = element("th", "", id); name.scope = "row";
    const proof = element("a", "", id === "R8_3_1768" ? "General exclusion: pivotal conjugation parity →" : "Current restrictions and remaining gap →");
    proof.href = `./case.html?id=${encodeURIComponent(id)}`;
    const cell = element("td"); cell.append(proof); row.append(name, cell); rows.append(row);
  }
  const checksum = $("#theoretical-update-checksum"); checksum.replaceChildren();
  const manifest = element("a", "", "Current source and download checksums ↓"); manifest.href = "./data/current_publication_revision.json"; manifest.download = "";
  checksum.append(manifest);
  notice.querySelector("a").addEventListener("click", () => { details.open = true; });
}

function renderPapers() {
  const release = state.data.rank6_release;
  if (release) {
    const date = new Date((state.data.publication_date || state.data.snapshot)+"T12:00:00Z");
    const dateOptions = {day:"numeric",month:"long",year:"numeric",timeZone:"UTC"};
    $("#edition-date").textContent = date.toLocaleDateString("en-GB", {...dateOptions,month:"short"}).toUpperCase();
    $("#snapshot-date").textContent = `Research snapshot · ${date.toLocaleDateString("en-GB", dateOptions)}`;
    const frontierRows = $("#rank6-frontier-rows");
    frontierRows.replaceChildren();
    for (const record of release.research_cases || []) {
      const row = element("tr");
      const name = element("th");
      const caseLink=element("a","unresolved-count-link",record.id);
      caseLink.href=`./case.html?id=${encodeURIComponent(record.id)}`;name.append(caseLink);
      name.scope = "row";
      const currentProfile = state.data.catalogue_records?.find(r => r.id === record.id);
      row.append(name, element("td", "", currentProfile?.summary || record.public_summary));
      frontierRows.append(row);
    }
    $("#rank6-frontier").hidden = !frontierRows.children.length;
    const summary = $("#rank6-release");
    summary.replaceChildren(element("strong", "", `Rank six, multiplicity at most ${release.analyzed_through}. `));
    summary.append(document.createTextNode(`${fmt.format(release.excluded)} excluded, ${release.realized} realized, ${release.unresolved} unresolved. ${release.research_summary || ""} `));
    if (release.unresolved) linkUnresolvedText(summary,`${release.unresolved} unresolved`,{rank:6,max_m:release.analyzed_through});
    if (state.data.theoretical_update) {
      const archive=element("a", "", "Historical proof and verification archive");
      archive.href=state.data.theoretical_update.archive.url || `./${state.data.theoretical_update.archive.path}`;archive.download="";summary.append(archive);
    }
    const manifest=state.data.current_publication_documents || state.data.current_documents;
    if (manifest) {
      const checksums=element("a", "", "Manuscript checksums");
      checksums.href=`./${manifest.path}`;checksums.download="";
      summary.append(document.createTextNode(" · "),checksums);
    }
    const verification=element("a", "", "Verification instructions");
    verification.href=`${state.data.classification_repository}/blob/${state.data.classification_commit || "main"}/docs/VERIFY.md`;
    summary.append(document.createTextNode(" · "),verification);
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
    entries.push({rank:7,title:r7.unresolved ? `Rank-seven Grothendieck rings: exclusions and models through multiplicity ${r7.analyzed_through}` : `Rank-seven Grothendieck rings: complete classification through multiplicity ${r7.analyzed_through}`,
      subtitle:`${fmt.format(r7.rings)} analyzed; ${r7.positive} models${r7.unresolved ? ` and ${r7.unresolved} general open ${r7.unresolved===1?"case":"cases"}` : "; complete classification"}`,type:"CLASSIFICATION",slug:"rank7"});
  if (r8)
    entries.push({rank:8,title:r8.unresolved ? `Rank-eight Grothendieck rings through multiplicity ${r8.analyzed_through}: criteria, models, and unresolved candidates` : `Rank-eight Grothendieck rings: complete classification through multiplicity ${r8.analyzed_through}`,
      subtitle:`${fmt.format(r8.rings)} analyzed; ${r8.positive} models${r8.unresolved ? ` and ${r8.unresolved} general open ${r8.unresolved===1?"case":"cases"}` : "; complete classification"}`,type:"CLASSIFICATION",slug:"rank8"});
  entries.push(...(state.data.catalogue_papers || []));
  for (const [index,paper] of entries.entries()) {
    const card=element("article","paper-card");
    const content=element("div");
    const meta=element("div","paper-meta");
    meta.append(element("span","",`${String(index+1).padStart(2,"0")} / ${(paper.ranks?.length || 1)>1?"RANKS":"RANK"} ${(paper.ranks || [paper.rank]).join("–")}`),element("span","",paper.type));
    content.append(meta,element("h3",paper.title.length>55?"long-title":"",paper.title),element("p","",paper.subtitle));
    const paperScope=state.data.scope.find(r=>r.rank===paper.rank);
    if (paperScope?.unresolved) linkUnresolvedText(content,paper.rank===6?`${paperScope.unresolved} cases remain`:`${paperScope.unresolved} general open ${paperScope.unresolved===1?"case":"cases"}`,{rank:paper.rank,max_m:paperScope.analyzed_through});
    card.append(content);
    const actions=element("div","paper-actions");
    const manuscript=element("a","","Read manuscript ↗");
    // A local PDF is included in the deployed snapshot when available.
    manuscript.href=`./papers/${paper.slug}.pdf`;
    manuscript.dataset.localPaper=paper.slug;
    const source=element("a","","Source & checks ↗");
    source.href=`${state.data.classification_repository}/blob/${paper.sourceRef || state.data.classification_commit || "main"}/${paper.sourcePath || paperSourcePath(paper.rank,"tex")}`;
    source.target="_blank";source.rel="noopener";
    actions.append(manuscript);
    if (paper.rank===4) {
      const companion=element("a","","Finite census paper ↗");
      companion.href="./papers/rank4_finite.pdf";
      const guide=element("a","","Verification guide ↗");
      guide.href="./papers/rank4_guide.pdf";
      actions.append(companion,guide);
      const pivotal=element("a","","Pivotal case · Dong–Palcoux–Plessis ↗");
      pivotal.href="https://arxiv.org/abs/2609.33272";
      pivotal.target="_blank";pivotal.rel="noopener";
      actions.append(pivotal);
    }
    if (paper.rank===5 || paper.rank===6) {
      const guide=element("a","","Verification guide ↗");
      guide.href=`./papers/rank${paper.rank}_guide.pdf`;
      actions.append(guide);
    }
    const release=state.data.upper_rank_releases?.[String(paper.rank)];
    if (release) {
      if (state.data.theoretical_update) {
        const current=element("a","","Historical proof archive ↓");
        current.href=state.data.theoretical_update.archive.url || `./${state.data.theoretical_update.archive.path}`;current.download="";
        actions.append(current);
      }
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
  records=records.filter(r=>state.propertyFilter?.matches(r) ?? true);
  const query=$("#catalogue-search").value.trim().toLowerCase();
  if (query) records=records.filter((r)=>`${r.id} ${r.name} ${r.model_reference}`.toLowerCase().includes(query));
  $("#extended-haagerup-note").hidden=all || chosen?.rank!==6 || chosen?.multiplicity!==7
    || !records.some((r)=>r.id==="R6_7_2274");
  $("#catalogue-context").textContent=all
    ? `${records.length} realized rings ${state.rank==="all"?"across the analyzed ranks":`at rank ${state.rank}`}`
    : chosen?`Rank ${chosen.rank} · exact multiplicity ${chosen.multiplicity} · ${records.length} explicit model${records.length===1?"":"s"}`:"Choose a cell above";
  if (!records.length) {
    grid.append(element("p","catalogue-empty",(query || state.propertyFilter?.size)?"No recorded model matches the selected filters.":"No realized Grothendieck rings in this band. The classification panel still records its excluded or unresolved fusion rings."));
    return;
  }
  for (const ring of records) {
    const card=element("article","ring-card");
    const meta=element("div","ring-card-meta",`RANK ${ring.rank}   /   m = ${ring.multiplicity}   /   ${ring.id}`);
    card.append(meta,element("h3","",ring.name));
    const facts=element("div","ring-card-facts");
    if (ring.properties) {
      facts.append(element("span","",ring.properties.integral ? "integral" : ring.properties.weakly_integral ? "weakly integral · nonintegral" : "not weakly integral"));
      for (const key of ["simple","perfect","pointed"]) if (ring.properties[key]) facts.append(element("span","",key));
    }
    facts.append(element("span","",ring.existence),element("span","",ring.invariants.commutative?"commutative":"noncommutative"),
                 element("span","",`FPdim ${formatApprox(ring.invariants.global_fp_dimension_approx)}`));
    card.append(facts);
    const open=element("button","open-ring","Explore ring ↗");
    open.type="button";open.addEventListener("click",()=>openRing(ring));
    const actions=element("div","ring-card-actions");
    actions.append(open,tensorDownload(ring,"ring-tensor-download"));
    card.append(actions);grid.append(card);
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
    if (selected) $("#ring-profile").setAttribute("aria-labelledby",button.id);
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
    const downloads=element("div","tensor-download-actions");
    downloads.append(tensorDownload(ring),dl);
    panel.append(downloads,element("p","profile-note","The .txt file is a Python list of lists of lists of integers: N[i][j][k] is the coefficient of Xₖ in Xᵢ · Xⱼ. Indices follow the displayed basis, with unit X₀."),element("p","profile-note",`SHA-256 of canonical JSON tensor: ${ring.tensor_sha256}`));
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
    if (ring.case_url) panel.append(link("Complete case record and research →",ring.case_url));
    panel.append(link("Inspect this exact model record ↗",ring.source_url || `${state.data.classification_repository}/blob/${state.data.classification_commit || "main"}/${ring.source_file}`));
    if (ring.model_reference_url)
      panel.append(link("Open the model's cited source ↗",ring.model_reference_url));
    for (const note of ring.construction_notes||[])
      panel.append(element("p","profile-note",note));
    if (ring.construction_proof_file)
      panel.append(link("Read the construction and its proof scope ↗",`${state.data.classification_repository}/blob/${state.data.classification_commit || "main"}/${ring.construction_proof_file}`));
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
    panel.append(link(ring.report_url ? (ring.report_label || "Rank-nine/ten research report") + " ↗" : `Rank-${ring.rank} manuscript ↗`,ring.report_url || `./papers/rank${ring.rank}.pdf`));
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
  state.propertyFilter=RingProperties.mount($("#model-property-filters"), "model-property", () => {const url=new URL(location.href);state.propertyFilter.applyParams(url.searchParams);history.replaceState(null,"",url);renderCatalogue();});
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
      const fallback=a.dataset.readingSource || paperSourcePath(Number(a.dataset.localPaper.slice(4)));
      a.href=`${state.data.classification_repository}/blob/${state.data.classification_commit || "main"}/${fallback}`;
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
    $(`#view-${mode}`).addEventListener("click",async()=>{
      state.mode=mode;
      const url=new URL(location.href);url.searchParams.set("view",mode);history.replaceState(null,"",url);
      for (const key of ["grothendieck","fusion"])
        $(`#view-${key}`).setAttribute("aria-pressed",String(key===mode));
      if (mode==="fusion") await loadFusionCounts();
      normalizeCountSelection();renderFilters();renderTable();renderDetail();renderCatalogue();
    });
  }
  $("#range-select").addEventListener("change",(event)=>{
    state.range=event.target.value;
    renderTable();
  });
  const jumpToMultiplicity=(event)=>{
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
  };
  $("#jump-input").addEventListener("keydown",event=>{if(event.key==="Enter")jumpToMultiplicity(event)});
  $("#jump-input").addEventListener("change",jumpToMultiplicity);
}
async function start() {
  try {
    const [response,statusResponse,modelsResponse]=await Promise.all([fetch("./data/atlas.json",{cache:"no-cache"}),fetch("./data/classification_status.json",{cache:"no-cache"}),fetch("./data/realized_rings.json",{cache:"no-cache"})]);
    if (!response.ok || !statusResponse.ok || !modelsResponse.ok) throw new Error(`Data HTTP ${response.status}/${statusResponse.status}/${modelsResponse.status}`);
    state.data=await response.json();
    state.data.classification_rows=(await statusResponse.json()).rows;
    state.models=(await modelsResponse.json()).records;
    const catalogue = await RingCatalogue.load();
    RingCatalogue.mergeAtlas(state, catalogue);
    if (!Array.isArray(state.data.rows) || !state.data.rows.length) throw new Error("No counts");
    state.data.rows=state.data.rows.map((r)=>({...r,rank:Number(r.rank),multiplicity:Number(r.multiplicity),rings:Number(r.rings)}));
    state.data.grothendieck_rows=(state.data.grothendieck_rows||[]).map((r)=>({...r,rank:Number(r.rank),multiplicity:Number(r.multiplicity),rings:Number(r.rings)}));
    state.censusMap=new Map(state.data.rows.map((r)=>[`${r.rank}:${r.multiplicity}`,r]));
    state.positiveMap=new Map(state.data.grothendieck_rows.map((r)=>[`${r.rank}:${r.multiplicity}`,r]));
    state.statusMap=new Map((state.data.classification_rows||[]).map((r)=>[`${r.rank}:${r.multiplicity}`,r]));
    const censusPins = [
      ["Historical census base", state.data.census_commit],
      ["Rank-seven M5 extension", state.data.census_extensions?.rank7_m5?.census_commit],
      ["Rank-eight M3 extension", state.data.census_extensions?.rank8_m3?.census_commit],
    ];
    const sourceCommit = $("#source-commit");
    sourceCommit.replaceChildren();
    for (const [label, commit] of censusPins.filter(([, commit]) => commit)) {
      const link = element("a", "", commit.slice(0, 12));
      link.href = `${state.data.source_repository}/tree/${commit}`;
      link.target = "_blank"; link.rel = "noopener";
      sourceCommit.append(`${label}: `, link, ". ");
    }
    const params=new URLSearchParams(window.location.search);
    if (params.get("view")==="fusion") {state.mode="fusion";await loadFusionCounts();}
    for (const key of ["grothendieck","fusion"]) $(`#view-${key}`).setAttribute("aria-pressed",String(key===state.mode));
    const requestedRing=params.get("ring");
    const linkedModel=requestedRing?state.models.find((r)=>r.id===requestedRing):null;
    const requestedRank=Number(params.get("rank"))||linkedModel?.rank||0;
    const requestedM=Number(params.get("m"))||linkedModel?.multiplicity||0;
    state.selected=state.censusMap.get(`${requestedRank}:${requestedM}`)
      || state.data.rows.find((r)=>r.rank===4 && r.multiplicity===1)
      || state.data.rows[0];
    if (requestedRank && ranges(state.data).ranks.includes(requestedRank))state.rank=requestedRank;
    if (state.selected && requestedM>Number(state.range)) {state.range="all";$("#range-select").value="all"}
    renderFilters();renderTable();renderDetail();renderScope();renderTheoreticalUpdate();renderPapers();initControls();initCatalogue();renderCatalogue();
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
