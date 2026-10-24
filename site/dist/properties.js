"use strict";
// All flags come from exact, source-bound tensor calculations at build time.
globalThis.RingProperties = (() => {
  const fields = [["integral", "Integral"], ["weakly_integral", "Weakly integral"], ["simple", "Simple"], ["perfect", "Perfect"], ["pointed", "Pointed"], ["commutative", "Commutative"], ["self_dual", "Self-dual"], ["multiplicity_free", "Multiplicity-free"]];
  const allowed = new Set(fields.map(([key]) => `p_${key}`));
  function mount(root, prefix, onChange, params = new URLSearchParams(location.search)) {
    const selected = new Map();
    if (!root) throw new Error("Missing ring-property controls");
    const details = document.createElement("details"); details.className = "property-panel";
    const summary = document.createElement("summary"); summary.textContent = "Ring properties";
    const intro = document.createElement("p"); intro.className = "property-note";
    intro.append("Combine exact ring properties. “No” selects the complementary class. ");
    const theory = document.createElement("a"); theory.href = "./theory.html#filters"; theory.textContent = "Definitions and examples →"; intro.append(theory);
    const grid = document.createElement("div"); grid.className = "property-grid";
    for (const [key, label] of fields) {
      const field = document.createElement("div"), name = document.createElement("label"), select = document.createElement("select");
      select.id = `${prefix}-${key}`; name.htmlFor = select.id; name.textContent = label;
      for (const [value, text] of [["", "Any"], ["yes", "Yes"], ["no", "No"]]) {const option = document.createElement("option"); option.value = value; option.textContent = text; select.append(option);}
      const value = params.get(`p_${key}`); select.value = ["yes", "no"].includes(value) ? value : "";
      if (select.value) selected.set(key, select.value);
      select.addEventListener("change", () => {if (select.value) selected.set(key, select.value); else selected.delete(key); update(); onChange();});
      field.append(name, select); grid.append(field);
    }
    const reset = document.createElement("button"); reset.type = "button"; reset.className = "property-reset"; reset.textContent = "Clear ring properties";
    reset.addEventListener("click", () => {selected.clear(); for (const select of grid.querySelectorAll("select")) select.value = ""; update(); onChange();});
    const update = () => {summary.textContent = `Ring properties${selected.size ? ` · ${selected.size} active` : ""}`; reset.hidden = !selected.size;};
    details.open = selected.size > 0; details.append(summary, intro, grid, reset); root.replaceChildren(details); update();
    return {
      matches: ring => [...selected].every(([key, value]) => typeof ring.properties?.[key] === "boolean" && ring.properties[key] === (value === "yes")),
      applyParams: query => {for (const key of allowed) query.delete(key); for (const [key, value] of selected) query.set(`p_${key}`, value); return query;},
      get size() {return selected.size;},
    };
  }
  return {mount, fields};
})();
