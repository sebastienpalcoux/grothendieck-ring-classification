/* Static atlas. All counts are loaded from the repository-derived JSON snapshot. */
"use strict";

const $ = (selector) => document.querySelector(selector);
const fmt = new Intl.NumberFormat("en-US");
const state = { data: null, rank: "all", range: "20", selected: null };
const paperEntries = [
  {rank:2, title:"A short classification of complex rank-two Grothendieck rings", subtitle:"Self-contained, unrestricted classification", type:"MANUSCRIPT", slug:"rank2"},
  {rank:3, title:"Galois-averaged indicators and sphericality in rank three", subtitle:"Direct five-ring classification and sphericality", type:"MANUSCRIPT", slug:"rank3"},
  {rank:4, title:"Rank-four Grothendieck rings through multiplicity 128", subtitle:"Complete general categorification", type:"CLASSIFICATION", slug:"rank4"},
  {rank:5, title:"Rank-five Grothendieck rings through multiplicity twenty: two general residuals at eighteen", subtitle:"Exact strata 19 and 20 excluded", type:"CLASSIFICATION", slug:"rank5"},
  {rank:6, title:"Rank-six fusion rings: categorification criteria and models through multiplicity eight", subtitle:"Complete to 2; partial general analysis through 8", type:"CLASSIFICATION", slug:"rank6"},
];
function paperSourcePath(rank,extension="pdf") {
  if (rank<=3) return `manuscripts/rank${rank}.${extension}`;
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
  for (const row of data.rows) map.set(`${row.rank}:${row.multiplicity}`, row);
  return map;
}
function ranges(data) {
  const ranks = [...new Set(data.rows.map((r) => r.rank))].sort((a,b)=>a-b);
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
      renderFilters();
      renderTable();
    });
    container.append(btn);
  }
}
function renderTable() {
  const {ranks,max} = ranges(state.data);
  const visibleRanks = state.rank === "all" ? ranks : [state.rank];
  const limit = state.range === "all" ? max : Math.min(Number(state.range),max);
  const rows = rankRows(state.data);
  const table = $("#count-table");
  const head = table.tHead;
  const body = table.tBodies[0];
  head.replaceChildren();
  body.replaceChildren();
  const header = element("tr");
  header.append(element("th", "", "m"));
  for (const rank of visibleRanks) header.append(element("th", "", `RANK ${rank}`));
  head.append(header);
  const maxima = Object.fromEntries(visibleRanks.map((rank) => [rank, Math.max(1,...state.data.rows.filter((r) => r.rank === rank && r.multiplicity <= limit).map((r) => r.rings))]));
  const fragment = document.createDocumentFragment();
  let records = 0;
  for (let m=1; m<=limit; m++) {
    const tr = element("tr");
    tr.append(element("td", "", String(m).padStart(2,"0")));
    for (const rank of visibleRanks) {
      const td = element("td");
      const row = rows.get(`${rank}:${m}`);
      if (row) {
        records++;
        const status=getStatus(rank,m);
        const coverage=status?.classification_coverage||"";
        const button = element("button", `count-cell ${coverage} ${state.selected?.rank===rank && state.selected?.multiplicity===m ? "selected":""}`, fmt.format(row.rings));
        button.type = "button";
        const coverageText={"complete_classification":"complete classification","partial_classification":"partial classification","census_only":"census only"}[coverage];
        button.title = `Rank ${rank}, multiplicity ${m}: ${fmt.format(row.rings)} rings${coverageText ? `, ${coverageText}` : ""}`;
        button.setAttribute("aria-label", button.title);
        button.setAttribute("aria-pressed", String(state.selected?.rank===rank && state.selected?.multiplicity===m));
        const intensity = Math.log1p(row.rings) / Math.log1p(maxima[rank]);
        button.style.setProperty("--fill", `${Math.round(8 + intensity*24)}%`);
        button.addEventListener("click", () => {
          state.selected = row;
          const locationUrl=new URL(window.location.href);
          locationUrl.searchParams.set("rank",String(rank));
          locationUrl.searchParams.set("m",String(m));
          history.replaceState(null,"",locationUrl);
          $("#count-table .count-cell.selected")?.classList.remove("selected");
          $("#count-table [aria-pressed='true']")?.setAttribute("aria-pressed","false");
          button.classList.add("selected");
          button.setAttribute("aria-pressed","true");
          renderDetail();
        });
        td.append(button);
      } else {
        const dash = element("span", "missing", "—");
        dash.title = "No complete census published for this rank and multiplicity";
        td.append(dash);
      }
      tr.append(td);
    }
    fragment.append(tr);
  }
  body.append(fragment);
  $("#table-footer").firstElementChild.textContent = `${fmt.format(records)} recorded cells · exact multiplicity m · — = unavailable`;
}
function appendDetailRow(container,label,value) {
  const p=element("div","detail-row");
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
  const observations=state.data.rows
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
  panel.append(element("div","detail-number",fmt.format(row.rings)));
  panel.append(element("p","detail-label",row.rings===1?"isomorphism class of based rings":"isomorphism classes of based rings"));
  panel.append(element("div","detail-rule"));
  appendDetailRow(panel,"Census","Complete");
  const status=getStatus(row.rank,row.multiplicity);
  const scope=state.data.scope.find((entry)=>entry.rank===row.rank);
  if (status) {
    const coverage={"complete_classification":"Complete","partial_classification":"Partial","census_only":"Census only"}[status.classification_coverage]||"Unspecified";
    appendDetailRow(panel,"Classification",coverage);
    const realized=status.realized_unitary+status.realized_other_or_unspecified+status.realized_spherical_nonpseudounitary;
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
  let note="This cell counts based-ring isomorphism classes at one exact multiplicity.";
  if (status?.classification_coverage==="partial_classification")
    note="“Unresolved” means general categorification remains undecided in this release.";
  else if (status?.classification_coverage==="census_only")
    note="The census is complete for this band, but the classification ledger has not assessed its rings.";
  else if (status?.classification_coverage==="complete_classification")
    note="Each ring in this band is realized or excluded by the stated criteria.";
  panel.append(element("p","detail-note",note));
  renderTrend(panel,row);
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
    card.append(element("div","scope-limit",record.kind==="provisional"?"PROOF IN REVISION":record.through===null?"UNRESTRICTED RANK":`COMPLETE THROUGH m ≤ ${record.through}`));
    let summary;
    if (record.rings!==null && record.positive!==null)
      summary=`${fmt.format(record.positive)} categorifiable among ${fmt.format(record.rings)} counted rings.`;
    else summary=record.note || "Classification of the unrestricted rank.";
    card.append(element("p","scope-description",summary));
    if (record.rings!==null && record.note) card.append(element("p","scope-extra",record.note));
    grid.append(card);
  }
}
function renderPapers() {
  const grid=$("#paper-grid");
  grid.replaceChildren();
  for (const paper of paperEntries) {
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
    source.href=`${state.data.classification_repository}/blob/main/${paperSourcePath(paper.rank,"tex")}`;
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
async function verifyLocalPapers() {
  // Avoid broken PDF links when a revision is still in progress.
  await Promise.all([...document.querySelectorAll("[data-local-paper]")].map(async (a)=>{
    try {
      const response=await fetch(a.href,{method:"HEAD"});
      if (!response.ok || !/pdf/i.test(response.headers.get("content-type")||"")) throw new Error("missing");
    } catch {
      a.href=`${state.data.classification_repository}/blob/main/${paperSourcePath(Number(a.dataset.localPaper.slice(4)))}`;
      a.textContent="View paper files ↗";
      a.target="_blank";a.rel="noopener";
    }
  }));
}
function initControls() {
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
    const target=$("#count-table tbody").children[m-1];
    target?.scrollIntoView({behavior:"smooth",block:"center"});
    target?.animate([{background:"#eac589"},{background:"transparent"}],{duration:1600});
  });
}
async function start() {
  try {
    const response=await fetch("./data/atlas.json");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.data=await response.json();
    if (!Array.isArray(state.data.rows) || !state.data.rows.length) throw new Error("No counts");
    state.data.rows=state.data.rows.map((r)=>({...r,rank:Number(r.rank),multiplicity:Number(r.multiplicity),rings:Number(r.rings)}));
    state.statusMap=new Map((state.data.classification_rows||[]).map((r)=>[`${r.rank}:${r.multiplicity}`,r]));
    if (state.data.census_commit) $("#source-commit").textContent=`Pinned at commit ${state.data.census_commit.slice(0,12)}.`;
    const params=new URLSearchParams(window.location.search);
    const requestedRank=Number(params.get("rank")), requestedM=Number(params.get("m"));
    state.selected=state.data.rows.find((r)=>r.rank===requestedRank && r.multiplicity===requestedM)
      || state.data.rows.find((r)=>r.rank===6 && r.multiplicity===3)
      || state.data.rows[0];
    if (state.selected && requestedM>Number(state.range)) {state.range="all";$("#range-select").value="all"}
    renderFilters();renderTable();renderDetail();renderScope();renderPapers();initControls();
    if (requestedRank && requestedM) {
      const target=$("#count-table tbody").children[requestedM-1];
      target?.scrollIntoView({block:"center"});
    }
    await verifyLocalPapers();
  } catch (err) {
    $("#cell-detail").textContent="The count snapshot could not be loaded. Please refresh this page.";
    $("#table-scroll").textContent=`Census data unavailable (${err.message}).`;
  }
}
start();
