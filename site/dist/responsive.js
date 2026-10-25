"use strict";

// One address and one set of data; the layout follows the available screen.
for (const header of document.querySelectorAll(".site-header")) {
  const navigation = header.querySelector(".top-nav");
  if (!navigation) continue;
  navigation.id ||= "site-navigation";
  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "nav-toggle";
  toggle.textContent = "Menu";
  toggle.setAttribute("aria-controls", navigation.id);
  toggle.setAttribute("aria-expanded", "false");
  navigation.before(toggle);
  header.classList.add("nav-enhanced");
  const close = () => {
    header.classList.remove("is-nav-open");
    toggle.setAttribute("aria-expanded", "false");
  };
  toggle.addEventListener("click", () => {
    const open = header.classList.toggle("is-nav-open");
    toggle.setAttribute("aria-expanded", String(open));
  });
  navigation.addEventListener("click", event => {
    if (event.target.closest("a")) close();
  });
  header.addEventListener("keydown", event => {
    if (event.key === "Escape" && header.classList.contains("is-nav-open")) {
      close();
      toggle.focus();
    }
  });
  document.addEventListener("click", event => {
    if (!header.contains(event.target)) close();
  });
  window.matchMedia("(max-width: 800px)").addEventListener("change", close);
}

document.addEventListener("click", event => {
  if (!event.target.closest(".count-cell") || !window.matchMedia("(max-width: 800px)").matches) return;
  const panel = document.getElementById("cell-detail");
  if (panel) requestAnimationFrame(() => panel.scrollIntoView({
    block: "start", behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth"
  }));
});

// Keep exact matrices and wide tables intact, with their own touch/keyboard scroll.
const scrollSelector = ".table-scroll, .profile-table-scroll, .case-table-scroll, .theory-table-wrap";
const enhancedTables = new WeakSet();
let tableNumber = 0;
function enhanceTables() {
  for (const region of document.querySelectorAll(scrollSelector)) {
    if (enhancedTables.has(region)) continue;
    enhancedTables.add(region);
    const hint = document.createElement("p");
    hint.className = "table-scroll-hint";
    hint.id = `table-scroll-hint-${++tableNumber}`;
    hint.textContent = "Scroll sideways to see the full table.";
    region.before(hint);
    region.setAttribute("aria-describedby", [region.getAttribute("aria-describedby"), hint.id].filter(Boolean).join(" "));
    if (!region.hasAttribute("tabindex")) region.tabIndex = 0;
    const update = () => { hint.hidden = region.scrollWidth <= region.clientWidth + 2; };
    const observer = new ResizeObserver(update);
    observer.observe(region);
    const table = region.querySelector("table");
    if (table) observer.observe(table);
    update();
  }
}
enhanceTables();
let scheduled = false;
new MutationObserver(records => {
  const hasTable = records.some(record => [...record.addedNodes].some(node =>
    node.nodeType === 1 && (node.matches(`table, ${scrollSelector}`) || node.querySelector("table"))
  ));
  if (!hasTable || scheduled) return;
  scheduled = true;
  requestAnimationFrame(() => { scheduled = false; enhanceTables(); });
}).observe(document.body, {childList: true, subtree: true});
