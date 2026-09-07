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

    /* One column to the left of the rail, vertically centred on the icon
       it belongs to, so the preview never sits over the toolbar. */
    /* The stage slides right while a preview is open, so an anchor measured
       mid-preview already carries the shift. Measure every icon up front,
       while nothing is open, and always place from those resting boxes. */
    // Fading .shell itself does nothing useful - it owns the backdrop-filter,
    // and Chrome keeps painting that. Fade its contents instead.
    var shellKids = document.querySelectorAll(".topbar, .content");
    var stage = document.querySelector(".stage");
    var SHIFT_PX = 150;
    var closeBtn = document.getElementById("peekClose");
    var restingBox = new WeakMap();

    function cacheBoxes() {
      if (document.body.classList.contains("is-peeking")) return;
      railItems.forEach(function (item) {
        var r = item.getBoundingClientRect();
        restingBox.set(item, { left: r.left, right: r.right, top: r.top,
                               height: r.height });
      });
    }

    cacheBoxes();
    window.addEventListener("load", cacheBoxes);

    /* The scenes sit inside display:none until hovered, so the browser has
       no reason to decode them until then - which stalls the first open.
       Decode them up front instead. */
    window.addEventListener("load", function () {
      peek.querySelectorAll(".peek-art").forEach(function (im) {
        if (im.decode) im.decode().catch(function () {});
      });
    });

    function anchorBox(anchor) {
      return restingBox.get(anchor) || anchor.getBoundingClientRect();
    }

    function placeItem(item, anchor) {
      var SHIFT = 150, EDGE = 16, OVERLAP = 26, STACK = 4;
      var art = item.querySelector(".peek-art");
      var body = item.querySelector(".peek-body");
      var a = anchorBox(anchor);

      var iconLeft = a.left + SHIFT;

      // The art's right edge runs under the icon, so the two touch.
      var artLeft = iconLeft + OVERLAP - art.offsetWidth;
      if (artLeft < EDGE) artLeft = EDGE;
      art.style.left = Math.round(artLeft) + "px";

      // Copy sits below the art, centred on it.
      var bodyLeft = artLeft + (art.offsetWidth - body.offsetWidth) / 2;
      body.style.left = Math.round(Math.max(bodyLeft, EDGE)) + "px";

      var total = art.offsetHeight + STACK + body.offsetHeight;
      var top = a.top + a.height / 2 - art.offsetHeight / 2;
      if (top + total > window.innerHeight - EDGE) {
        top = window.innerHeight - EDGE - total;
      }
      top = Math.min(Math.max(top, EDGE), window.innerHeight - total - EDGE);

      art.style.top = Math.round(top) + "px";
      body.style.top = Math.round(top + art.offsetHeight + STACK) + "px";

      if (closeBtn) {
        // Inside the artwork's top corner, clear of the rail beside it.
        closeBtn.style.left = Math.round(artLeft + art.offsetWidth - 64) + "px";
        closeBtn.style.top = Math.round(top + 2) + "px";
        closeBtn.style.setProperty("--hue",
          item.style.getPropertyValue("--hue"));
      }
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
      // Set inline so nothing in the cascade can get in the way. Both are
      // compositor-only properties, so this stays cheap.
      if (stage) stage.style.transform = "translateX(" + SHIFT_PX + "px)";
      shellKids.forEach(function (el) { el.style.opacity = "0.18"; });
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
      if (closeBtn) closeBtn.classList.remove("is-shown");
      document.body.classList.remove("is-peeking");
      if (stage) stage.style.transform = "";
      shellKids.forEach(function (el) { el.style.opacity = ""; });
      peek.setAttribute("aria-hidden", "true");
      openId = null;
      openAnchor = null;
    }

    var ptrX = 0, ptrY = 0;

    function scheduleClose() {
      clearTimeout(closeTimer);
      closeTimer = setTimeout(function () {
        // The icon may have slid out from under a stationary pointer.
        if (inSafeZone(ptrX, ptrY)) return scheduleClose();
        closePeek();
      }, 200);
    }

    /* The icon, the art and the copy are three separate boxes with gaps
       between them. Treat their union (plus a margin) as one hover zone,
       otherwise crossing a gap fires mouseleave and the preview flickers
       shut while the pointer is still heading for it. */
    function inSafeZone(x, y) {
      if (!openAnchor) return false;
      var pad = 34;
      var active = peek.querySelector(".peek-item.is-active");
      var ar = openAnchor.getBoundingClientRect();
      var boxes = [{ left: ar.left - 150, right: ar.right,
                     top: ar.top, bottom: ar.bottom },
                   { left: ar.left, right: ar.right,
                     top: ar.top, bottom: ar.bottom }];
      if (active) {
        boxes.push(active.querySelector(".peek-art").getBoundingClientRect());
        boxes.push(active.querySelector(".peek-body").getBoundingClientRect());
      }
      var l = Infinity, r = -Infinity, t = Infinity, b = -Infinity;
      boxes.forEach(function (bx) {
        l = Math.min(l, bx.left); r = Math.max(r, bx.right);
        t = Math.min(t, bx.top);  b = Math.max(b, bx.bottom);
      });
      return x >= l - pad && x <= r + pad && y >= t - pad && y <= b + pad;
    }

    document.addEventListener("mousemove", function (e) {
      ptrX = e.clientX;
      ptrY = e.clientY;
      if (!openId) return;
      var near = inSafeZone(ptrX, ptrY);
      if (closeBtn) closeBtn.classList.toggle("is-shown", near);
      if (near) clearTimeout(closeTimer);
      else scheduleClose();
    }, { passive: true });

    railItems.forEach(function (item) {
      var id = item.getAttribute("data-peek");
      item.addEventListener("mouseenter", function () { openPeek(id, item); });
      item.addEventListener("mouseleave", scheduleClose);
      item.addEventListener("focus", function () { openPeek(id, item); });
      item.addEventListener("blur", scheduleClose);
    });

    if (closeBtn) {
      closeBtn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        closePeek();
      });
    }

    peek.addEventListener("mouseenter", function () { clearTimeout(closeTimer); }, true);
    peek.addEventListener("mouseleave", scheduleClose, true);

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closePeek();
    });

    // Dropping below the breakpoint mid-session should not leave the
    // page stuck behind a blur.
    window.addEventListener("resize", function () {
      cacheBoxes();
      if (!openId) return;
      if (!peekEnabled()) return closePeek();
      var active = peek.querySelector(".peek-item.is-active");
      if (active && openAnchor) placeItem(active, openAnchor);
    });
  }

  /* ---------- Bento cards rise as they come into view ---------- */
  var bento = document.querySelector(".bento");
  if (bento && window.IntersectionObserver &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    bento.classList.add("is-revealing");
    var cards = bento.querySelectorAll(".bento-card");
    function reveal(card) {
      card.style.transitionDelay = (card.dataset.delay || "0") + "ms";
      card.classList.add("is-in");
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        reveal(entry.target);
        io.unobserve(entry.target);
      });
    }, { root: document.querySelector(".content"), threshold: 0.15 });

    cards.forEach(function (card, i) {
      card.dataset.delay = String(i * 70);
      io.observe(card);
    });

    // Hiding things up front is only safe with a way back: if the observer
    // never reports (some browsers with an unusual scroll root, a page that
    // opens already scrolled past), show them anyway rather than leave the
    // grid blank.
    setTimeout(function () {
      cards.forEach(function (card) {
        if (!card.classList.contains("is-in")) reveal(card);
      });
    }, 2500);
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

/* --- her eyes follow the pointer ------------------------------------- */
(function () {
  var eyes = [].slice.call(document.querySelectorAll(".deco-cut .eye"));
  if (!eyes.length) return;
  // touch has no pointer to follow, and the card's hover scale never fires
  if (!window.matchMedia("(hover: hover)").matches) return;

  var pupils = eyes.map(function (eye) { return eye.firstElementChild; });
  var ptrX = 0, ptrY = 0, queued = false, seen = false;

  // Reach: how far the pointer has to be before the pupils are looking as far
  // over as they go. Roughly a face's worth of screen.
  var REACH = 420;

  // how far past its socket an iris may slide, as a fraction of the socket
  var OVERSHOOT = 0.02;

  function paint() {
    queued = false;

    // Measured every frame rather than cached: the card lifts and scales on
    // hover, and the page scrolls, both of which move these boxes.
    var boxes = [], roomX = Infinity, roomY = Infinity, i;
    for (i = 0; i < eyes.length; i++) {
      var e = eyes[i].getBoundingClientRect();
      if (!e.width) return;
      var p = pupils[i].getBoundingClientRect();
      boxes.push(e);
      // Her sockets are drawn at different sizes, so each has a different
      // amount of slack. Both eyes take the smaller of the two, which is what
      // stops one drifting further than the other and breaking the pair.
      //
      // The iris is allowed a little past that, because her left eye is only
      // 35px tall against a 31px iris and would otherwise barely move at all.
      // Overshooting just lets the lid crop the iris at the extremes, which is
      // what a real eye does anyway.
      roomX = Math.min(roomX, (e.width - p.width) / 2 + e.width * OVERSHOOT);
      roomY = Math.min(roomY, (e.height - p.height) / 2 + e.height * OVERSHOOT);
    }
    roomX = Math.max(0, roomX);
    roomY = Math.max(0, roomY);

    for (i = 0; i < eyes.length; i++) {
      var b = boxes[i];
      var dx = ptrX - (b.left + b.width / 2);
      var dy = ptrY - (b.top + b.height / 2);
      var d = Math.sqrt(dx * dx + dy * dy) || 1;

      // ease-out on distance, so small movements near her face still read
      var k = Math.min(1, d / REACH);
      k = k * (2 - k);

      pupils[i].style.transform =
        "translate(-50%, -50%) translate(" +
        ((dx / d) * k * roomX).toFixed(2) + "px, " +
        ((dy / d) * k * roomY).toFixed(2) + "px)";
    }
  }

  function queue() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(paint);
  }

  document.addEventListener("mousemove", function (e) {
    ptrX = e.clientX;
    ptrY = e.clientY;
    seen = true;
    queue();
  }, { passive: true });

  // Pointer gone from the window, or the page moved under a still pointer.
  document.addEventListener("mouseleave", function () {
    for (var i = 0; i < pupils.length; i++) pupils[i].style.transform = "";
  });
  window.addEventListener("scroll", function () { if (seen) queue(); },
                          { passive: true });
  window.addEventListener("resize", function () { if (seen) queue(); });
})();

/* --- the lamp pull swaps the theme ------------------------------------ */
(function () {
  var lamp = document.getElementById("lampPull");
  if (!lamp) return;
  var root = document.documentElement;

  function current() {
    return root.getAttribute("data-theme") === "light" ? "light" : "dark";
  }

  function label() {
    var light = current() === "light";
    lamp.setAttribute("aria-pressed", light ? "true" : "false");
    lamp.setAttribute("aria-label",
      light ? "Switch to the dark theme" : "Switch to the light theme");
  }
  label();

  lamp.addEventListener("click", function () {
    var next = current() === "light" ? "dark" : "light";
    if (next === "light") {
      root.setAttribute("data-theme", "light");
    } else {
      root.removeAttribute("data-theme");
    }
    try {
      localStorage.setItem("theme", next);
    } catch (e) {
      // private browsing; the choice just will not outlive the tab
    }
    label();

    // restart the tug even on a second click in quick succession
    lamp.classList.remove("is-pulled");
    void lamp.offsetWidth;
    lamp.classList.add("is-pulled");
  });

  lamp.addEventListener("animationend", function () {
    lamp.classList.remove("is-pulled");
  });

  // Follow the system setting only while the reader has not chosen for
  // themselves; once they pull the cord, that is the answer.
  var mq = window.matchMedia("(prefers-color-scheme: light)");
  var onSystem = function (e) {
    try {
      if (localStorage.getItem("theme")) return;
    } catch (err) {
      return;
    }
    if (e.matches) {
      root.setAttribute("data-theme", "light");
    } else {
      root.removeAttribute("data-theme");
    }
    label();
  };
  if (mq.addEventListener) mq.addEventListener("change", onSystem);
  else if (mq.addListener) mq.addListener(onSystem);
})();
