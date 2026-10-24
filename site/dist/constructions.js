"use strict";
// The complete catalogue is rendered in HTML. JavaScript only adds filters.
(() => {
  const list = document.querySelector(".construction-list");
  if (!list) return;
  const search = document.querySelector("#construction-search");
  const rank = document.querySelector("#construction-rank");
  const multiplicity = document.querySelector("#construction-m");
  const propertyRoot = document.querySelector("#construction-property-filters");
  const count = document.querySelector("#construction-count");
  const empty = document.querySelector("#construction-empty");
  const reset = document.querySelector("#construction-reset");
  const articles = [...list.querySelectorAll(".construction-entry")];

  try {
    if (![search, rank, multiplicity, propertyRoot, count, empty, reset].every(Boolean)) {
      throw new Error("Missing construction controls");
    }
    const entries = articles.map(article => ({
      article,
      id: article.dataset.id || article.id,
      rank: Number(article.dataset.rank),
      multiplicity: Number(article.dataset.multiplicity),
      search: `${article.dataset.id || article.id} ${article.dataset.search || article.textContent}`.toLocaleLowerCase("en"),
      properties: JSON.parse(article.dataset.properties || "{}"),
    })).sort((a, b) => a.rank - b.rank || a.multiplicity - b.multiplicity || a.id.localeCompare(b.id, "en", {numeric: true}));
    for (const entry of entries) list.append(entry.article);
    let propertyFilter;

    function render({writeUrl = true, clearHash = false} = {}) {
      const query = search.value.trim().toLocaleLowerCase("en");
      const exactM = Number(multiplicity.value);
      const validM = Number.isSafeInteger(exactM) && exactM > 0;
      let shown = 0;
      for (const entry of entries) {
        const matches = (!query || entry.search.includes(query)) &&
          (!rank.value || entry.rank === Number(rank.value)) &&
          (!validM || entry.multiplicity === exactM) && propertyFilter.matches(entry);
        entry.article.hidden = !matches;
        if (matches) shown++;
      }
      count.textContent = `Showing ${shown} of ${entries.length} examples`;
      empty.hidden = shown !== 0;
      reset.disabled = !(query || rank.value || validM || propertyFilter.size);
      if (writeUrl) {
        const url = new URL(location.href);
        for (const [key, value] of [["q", search.value.trim()], ["rank", rank.value], ["m", validM ? String(exactM) : ""]]) {
          if (value) url.searchParams.set(key, value); else url.searchParams.delete(key);
        }
        propertyFilter.applyParams(url.searchParams);
        if (clearHash) url.hash = "";
        history.replaceState(null, "", url);
      }
    }

    function mountProperties(params) {
      propertyFilter = RingProperties.mount(propertyRoot, "construction-property", () => render({clearHash: true}), params);
    }

    function clearFilters() {
      search.value = "";
      rank.value = "";
      multiplicity.value = "";
      mountProperties(new URLSearchParams());
    }

    function revealHash() {
      let id;
      try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
      if (!id) return;
      const entry = entries.find(item => item.article.id === id);
      if (!entry) return;
      if (entry.article.hidden) {
        clearFilters();
        render();
      }
      requestAnimationFrame(() => entry.article.scrollIntoView({block: "start", behavior: "auto"}));
    }

    function readURL() {
      const params = new URLSearchParams(location.search);
      search.value = (params.get("q") || "").slice(0, 500);
      const chosenRank = params.get("rank") || "";
      rank.value = [...rank.options].some(option => option.value === chosenRank) ? chosenRank : "";
      const chosenM = Number(params.get("m"));
      multiplicity.value = Number.isSafeInteger(chosenM) && chosenM > 0 ? String(chosenM) : "";
      mountProperties(params);
      render();
      revealHash();
    }

    for (const control of [search, rank, multiplicity]) {
      control.addEventListener("input", () => render({clearHash: true}));
    }
    reset.addEventListener("click", () => {
      clearFilters();
      render({clearHash: true});
      search.focus();
    });
    document.querySelector(".construction-toolbar")?.addEventListener("submit", event => event.preventDefault());
    window.addEventListener("popstate", readURL);
    window.addEventListener("hashchange", revealHash);
    readURL();
  } catch (error) {
    // Failure of an enhancement must never conceal the published catalogue.
    for (const article of articles) article.hidden = false;
    if (empty) empty.hidden = true;
    for (const control of [search, rank, multiplicity, reset]) if (control) control.disabled = true;
    if (propertyRoot) propertyRoot.hidden = true;
    if (count) count.textContent = `${articles.length} examples. All entries are displayed; filtering is unavailable.`;
    console.error("Construction catalogue filters:", error);
  }
})();
