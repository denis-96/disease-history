"use strict";

function openAccordion(e) {
  const content = e.target.closest(".control-record__content");
  content.classList.toggle("control-record_open");
  const contentBody = content.querySelector(".control-record__body");
  if (contentBody.style.height) {
    contentBody.style.height = window.getComputedStyle(contentBody).height;
    setTimeout(() => {
      contentBody.style.height = null;
    });
  } else {
    contentBody.style.height = contentBody.scrollHeight + "px";
    setTimeout(() => {
      contentBody.style.height = "auto";
    }, 200);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".control-record__title").forEach((el) => {
    el.addEventListener("click", openAccordion);
  });

  document.querySelectorAll(".rubrics-select__btn").forEach((el) => {
    el.addEventListener("click", (e) => {
      e.currentTarget.parentElement.classList.toggle("rubrics-select_active");
    });
    el.addEventListener("focusout", (e) => {
      e.currentTarget.parentElement.classList.remove("rubrics-select_active");
    });
  });

  document.querySelectorAll(".rubrics-select__item ul").forEach((el) => {
    el.addEventListener("click", (e) => {
      const rubricLi = e.target.closest("li");
      if (rubricLi) {
        const rubric = rubricLi.textContent;
        const rubricsSelect = rubricLi.closest(".rubrics-select__content");
        rubricsSelect.previousElementSibling.firstElementChild.innerHTML =
          rubric;
        rubricsSelect.parentElement.classList.toggle("rubrics-select_active");
      }
    });
  });
});
