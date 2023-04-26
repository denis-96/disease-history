function openAccordion(e) {
  e.target.closest(".content").classList.toggle("content_open");
}

document.querySelectorAll(".content_head").forEach((el) => {
  el.addEventListener("click", openAccordion);
});
