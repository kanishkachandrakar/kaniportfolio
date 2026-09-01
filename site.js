/* Shared behaviour for every page: mobile menu, tabs, project modals. */
(function () {
  "use strict";

  /* ---------- Mobile menu ---------- */
  var menuBtn = document.querySelector(".menu-btn");
  var nav = document.querySelector(".nav");

  function setMenu(open) {
    if (!nav) return;
    nav.classList.toggle("is-open", open);
    if (menuBtn) {
      menuBtn.setAttribute("aria-expanded", String(open));
      menuBtn.innerHTML = open
        ? '<i class="fa-solid fa-xmark"></i>'
        : '<i class="fa-solid fa-bars"></i>';
    }
  }

  if (menuBtn) {
    menuBtn.addEventListener("click", function () {
      setMenu(!nav.classList.contains("is-open"));
    });
  }

  document.addEventListener("click", function (e) {
    if (!nav || !nav.classList.contains("is-open")) return;
    if (nav.contains(e.target) || (menuBtn && menuBtn.contains(e.target))) return;
    setMenu(false);
  });

  /* ---------- Tabs ---------- */
  var tabs = document.querySelectorAll("[data-tab]");
  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      var id = tab.getAttribute("data-tab");
      tabs.forEach(function (t) { t.classList.remove("is-active"); });
      document.querySelectorAll(".tabpanel").forEach(function (p) {
        p.classList.remove("is-active");
      });
      tab.classList.add("is-active");
      var panel = document.getElementById(id);
      if (panel) panel.classList.add("is-active");
    });
  });

  /* ---------- Modals ---------- */
  var lastFocused = null;

  function openModal(id) {
    var modal = document.getElementById(id);
    if (!modal) return;
    lastFocused = document.activeElement;
    modal.classList.add("is-open");
    document.body.style.overflow = "hidden";
    var close = modal.querySelector(".modal-close");
    if (close) close.focus();
  }

  function closeModals() {
    document.querySelectorAll(".modal.is-open").forEach(function (m) {
      m.classList.remove("is-open");
    });
    document.body.style.overflow = "";
    if (lastFocused && lastFocused.focus) lastFocused.focus();
  }

  document.addEventListener("click", function (e) {
    var opener = e.target.closest("[data-modal]");
    if (opener) {
      openModal(opener.getAttribute("data-modal"));
      return;
    }
    if (e.target.closest(".modal-close")) {
      closeModals();
      return;
    }
    // Click on the dimmed area outside the box closes the modal.
    var modal = e.target.closest(".modal");
    if (modal && !e.target.closest(".modal-box")) closeModals();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      closeModals();
      setMenu(false);
    }
  });
})();
