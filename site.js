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

  /* ---------- Rail preview ----------
     Hover a rail icon and the page blurs back while that section's card
     rises. A short close delay lets the pointer travel from the icon to
     the card without the card vanishing on the way. */
  var peek = document.getElementById("peek");
  var railItems = document.querySelectorAll(".rail-item");

  if (peek && railItems.length) {
    var closeTimer = null;
    var openId = null;
    var openAnchor = null;

    function peekEnabled() {
      return window.matchMedia("(min-width: 1301px) and (hover: hover)").matches;
    }

    /* Place the art above the icon and the copy below it, both centred
       on the icon and nudged back inside the viewport if they would spill. */
    function placeItem(item, anchor) {
      var W = 322, EDGE = 18, GAP = 16;
      var art = item.querySelector(".peek-art");
      var body = item.querySelector(".peek-body");
      var a = anchor.getBoundingClientRect();

      var cx = a.left + a.width / 2;

      function centre(el, w) {
        return Math.min(Math.max(cx - w / 2, EDGE), window.innerWidth - w - EDGE);
      }

      body.style.left = Math.round(centre(body, W)) + "px";

      // The art keeps its own aspect, so measure it before centring.
      art.style.left = "0px";
      art.style.top = "0px";
      art.style.left = Math.round(centre(art, art.offsetWidth)) + "px";
      art.style.top = Math.round(Math.max(a.top - GAP - art.offsetHeight, EDGE)) + "px";

      var bodyTop = a.bottom + GAP;
      var overflow = bodyTop + body.offsetHeight - (window.innerHeight - EDGE);
      if (overflow > 0) bodyTop -= overflow;
      body.style.top = Math.round(bodyTop) + "px";
    }

    function openPeek(id, anchor) {
      if (!peekEnabled() || id === openId) return;
      clearTimeout(closeTimer);

      var active = null;
      peek.querySelectorAll(".peek-item").forEach(function (c) {
        var on = c.getAttribute("data-peek") === id;
        c.classList.toggle("is-active", on);
        if (on) active = c;
      });
      railItems.forEach(function (r) {
        r.classList.toggle("is-peeked", r === anchor);
      });

      if (active) placeItem(active, anchor);
      document.body.classList.add("is-peeking");
      peek.setAttribute("aria-hidden", "false");
      openId = id;
      openAnchor = anchor;
    }

    function closePeek() {
      clearTimeout(closeTimer);
      peek.querySelectorAll(".peek-item").forEach(function (c) {
        c.classList.remove("is-active");
      });
      railItems.forEach(function (r) { r.classList.remove("is-peeked"); });
      document.body.classList.remove("is-peeking");
      peek.setAttribute("aria-hidden", "true");
      openId = null;
      openAnchor = null;
    }

    function scheduleClose() {
      clearTimeout(closeTimer);
      closeTimer = setTimeout(closePeek, 180);
    }

    railItems.forEach(function (item) {
      var id = item.getAttribute("data-peek");
      item.addEventListener("mouseenter", function () { openPeek(id, item); });
      item.addEventListener("mouseleave", scheduleClose);
      item.addEventListener("focus", function () { openPeek(id, item); });
      item.addEventListener("blur", scheduleClose);
    });

    peek.addEventListener("mouseenter", function () { clearTimeout(closeTimer); }, true);
    peek.addEventListener("mouseleave", scheduleClose, true);

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closePeek();
    });

    // Dropping below the breakpoint mid-session should not leave the
    // page stuck behind a blur.
    window.addEventListener("resize", function () {
      if (!openId) return;
      if (!peekEnabled()) return closePeek();
      var active = peek.querySelector(".peek-item.is-active");
      if (active && openAnchor) placeItem(active, openAnchor);
    });
  }

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
