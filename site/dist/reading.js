"use strict";
// Native dialogs supply focus management, Escape and an explicit close button.
for (const trigger of document.querySelectorAll("[data-open-dialog]")) {
  trigger.addEventListener("click", () => document.getElementById(trigger.dataset.openDialog)?.showModal());
}
for (const dialog of document.querySelectorAll("dialog.reading-dialog")) {
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      const box = dialog.getBoundingClientRect();
      if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
    }
  });
  for (const anchor of dialog.querySelectorAll('a[href^="#"]')) {
    anchor.addEventListener("click", () => dialog.close());
  }
}
// A direct link to a folded section also opens its containing disclosures.
function revealHash() {
  if (!location.hash) return;
  let target;
  try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch { return; }
  if (!target) return;
  for (let node = target; node; node = node.parentElement) {
    if (node.tagName === "DETAILS") node.open = true;
  }
  target.scrollIntoView({block:"start"});
}
document.addEventListener("click", (event) => {
  const anchor = event.target.closest('a[href^="#"]');
  if (anchor) setTimeout(revealHash, 0);
});
window.addEventListener("hashchange", revealHash);
revealHash();
