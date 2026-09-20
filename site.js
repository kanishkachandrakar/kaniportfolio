/* Shared behaviour for every page: mobile menu, tabs, project modals. */
(function () {
  "use strict";

  /* ---------- Mobile menu ---------- */
  var menuBtn = document.querySelector(".menu-btn");
  var nav = document.querySelector(".nav");

  function setMenu(open) {
    if (!nav) return;
    nav.classList.toggle("is-open", open);
    // aria-expanded only. Which icon shows is CSS's job now: rewriting
    // innerHTML here threw away the icon element and built a new one on every
    // toggle, which means a style recalculation, a layout and a fresh glyph
    // lookup at exactly the moment the slide is trying to start.
    if (menuBtn) menuBtn.setAttribute("aria-expanded", String(open));
  }

  if (menuBtn) {
    menuBtn.addEventListener("click", function () {
      setMenu(!nav.classList.contains("is-open"));
    });
  }

  // The drawer's own close. The dismissal below ignores anything inside the
  // drawer, deliberately - clicking a link or the panel itself should not
  // count as clicking away - so this needs its own handler rather than
  // falling through to that one.
  var navClose = document.querySelector(".nav-close");
  if (navClose) {
    navClose.addEventListener("click", function () { setMenu(false); });
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

  // The previews belong to the rail, so they answer to the same switch it
  // does. Without this the whole module still runs while the rail is parked:
  // boxes measured on hidden icons, listeners bound to things nobody can
  // point at, and four scenes decoded for a panel that cannot open.
  function railOn() {
    return getComputedStyle(document.documentElement)
      .getPropertyValue("--rail").trim() === "flex";
  }

  if (peek && railItems.length && railOn()) {
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

    /* The scenes carry their file in data-src rather than src, so nothing
       fetches them until this runs - and this does not run while the rail is
       parked, which is the point. Four images that no one can open are four
       images that should not be on the wire.

       They sit inside display:none once loaded, so the browser has no reason
       to decode them until the first hover, which stalls that first open.
       Hence the decode here as well: fetched and decoded together, after the
       page itself is done loading and has stopped competing for the network. */
    window.addEventListener("load", function () {
      peek.querySelectorAll(".peek-art").forEach(function (im) {
        var file = im.getAttribute("data-src");
        if (file && !im.getAttribute("src")) im.setAttribute("src", file);
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

  // The theme-color metas are chosen by prefers-color-scheme, which cannot
  // see a choice made here. Once the cord is pulled, pin it directly.
  function paintChrome() {
    var tag = document.querySelector('meta[name="theme-color"]:not([media])');
    if (!tag) {
      tag = document.createElement("meta");
      tag.setAttribute("name", "theme-color");
      document.head.appendChild(tag);
    }
    tag.setAttribute("content",
      current() === "light" ? "#F3F1EA" : "#100D0B");
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
    paintChrome();

    // restart the tug even on a second click in quick succession
    lamp.classList.remove("is-pulled");
    void lamp.offsetWidth;
    lamp.classList.add("is-pulled");
  });

  lamp.addEventListener("animationend", function () {
    lamp.classList.remove("is-pulled");
  });

  // --- the chain sways -------------------------------------------------
  // A chain does not swing rigidly, so this is not one rotation. Each link
  // is a little spring hung off the one above it: the top moves first and
  // the movement travels down, which is what makes it read as a wave rather
  // than as a rotating stick. The knob, at the end of the run of lag, always
  // arrives last and overshoots the most.
  if (window.matchMedia("(hover: hover)").matches
      && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var line = lamp.querySelector(".lamp-line");
    var beadG = lamp.querySelector(".lamp-beads");
    var knob = lamp.querySelector(".lamp-knob");

    var LINKS = 7;          // beads between the ceiling and the knob
    var TOP = 4;            // where the cord leaves the top, in viewBox units
    var BOTTOM = 100;       // where the knob hangs from
    var REACH = 420;        // past this the chain has stopped caring
    var NEAR = 130;         // sideways offset that already means "fully over"
    var MAX = 15;           // viewBox units of lean at full pull

    var xs = [], vs = [], i;
    for (i = 0; i <= LINKS; i++) { xs.push(0); vs.push(0); }

    var beads = [];
    for (i = 1; i < LINKS; i++) {
      var e = document.createElementNS("http://www.w3.org/2000/svg", "ellipse");
      e.setAttribute("rx", "3.1");
      e.setAttribute("ry", "4.1");
      beadG.appendChild(e);
      beads.push(e);
    }

    var want = 0, ptrX = 0, ptrY = 0, running = false;

    function aim() {
      var b = lamp.getBoundingClientRect();
      if (!b.width) return;
      // measured from where it hangs, not from its middle - that is the
      // point it actually pivots around
      var dx = ptrX - (b.left + b.width / 2);
      var dy = ptrY - b.top;
      var d = Math.sqrt(dx * dx + dy * dy);
      var pull = Math.max(0, 1 - d / REACH);
      pull = pull * (2 - pull);          // ease out, so near counts most
      // Direction saturates well before distance does: a pointer a hand's
      // width to the left is already fully to the left, just not close.
      var side = Math.max(-1, Math.min(1, dx / NEAR));
      want = side * MAX * pull;
    }

    function step() {
      var share = want / LINKS;
      var moving = false;

      for (var j = 1; j <= LINKS; j++) {
        var target = xs[j - 1] + share;
        // Simulated before picking these. At 0.16/0.86 the tip overshot its
        // resting place by ten times the distance it had to travel and was
        // still wobbling four seconds later. This overshoots by about a
        // seventh and is done inside a second: enough follow-through to read
        // as weight on a chain, not enough to look loose.
        vs[j] += (target - xs[j]) * 0.12;   // spring towards the link above
        vs[j] *= 0.70;                      // damping, or it never settles
        xs[j] += vs[j];
        if (Math.abs(vs[j]) > 0.002 || Math.abs(target - xs[j]) > 0.002) {
          moving = true;
        }
      }

      var d = "M" + (20 + xs[0]).toFixed(2) + " " + TOP;
      for (j = 1; j <= LINKS; j++) {
        var y = TOP + (BOTTOM - TOP) * (j / LINKS);
        var py = TOP + (BOTTOM - TOP) * ((j - 1) / LINKS);
        var mx = 20 + (xs[j - 1] + xs[j]) / 2;
        // quadratic through the midpoints, so the cord curves between the
        // beads instead of kinking at each one
        d += " Q" + (20 + xs[j - 1]).toFixed(2) + " " + ((py + y) / 2).toFixed(2)
           + " " + mx.toFixed(2) + " " + y.toFixed(2);
        if (j < LINKS) {
          beads[j - 1].setAttribute("cx", (20 + xs[j]).toFixed(2));
          beads[j - 1].setAttribute("cy", y.toFixed(2));
        }
      }
      line.setAttribute("d", d);
      knob.setAttribute("cx", (20 + xs[LINKS]).toFixed(2));
      knob.setAttribute("cy", (BOTTOM + 10).toFixed(2));

      // Stops as soon as it has settled. An idle sway looked good and meant
      // a requestAnimationFrame loop that never ended, which is a frame of
      // work every 16ms for the life of the page whether or not anyone is
      // near it.
      if (moving) {
        requestAnimationFrame(step);
      } else {
        running = false;
      }
    }

    function wake() {
      if (running) return;
      running = true;
      requestAnimationFrame(step);
    }

    document.addEventListener("mousemove", function (e) {
      ptrX = e.clientX;
      ptrY = e.clientY;
      aim();
      wake();
    }, { passive: true });

    document.addEventListener("mouseleave", function () {
      want = 0;
      wake();
    });

    wake();
  }
})();

/* --- the portrait turns while the music plays ------------------------- */
(function () {
  var btn = document.getElementById("spinBtn");
  var audio = document.getElementById("spinAudio");
  if (!btn || !audio) return;
  var deck = btn.closest(".turntable");

  // The button ships hidden and is revealed only once the file reports that
  // it has loaded. The track is a placeholder meant to be swapped, and if one
  // is ever missing or in a format the browser will not take, the page should
  // simply not offer music rather than offer a button that does nothing.
  var nudge = document.getElementById("spinNudge");

  // Someone who has played the track once has been told. The hint and the ring
  // are both there to say the record is a record, and that is not news twice.
  // It is keyed on having played rather than on having visited: a visit where
  // nobody pressed the button is a visit where the hint did not land, and it
  // has earned another go.
  var HEARD = "spun";
  var heard = false;
  try { heard = localStorage.getItem(HEARD) === "1"; } catch (e) {}
  if (heard) deck.classList.add("is-heard");

  function reveal() {
    btn.hidden = false;
    if (nudge && !heard) nudge.hidden = false;
  }
  if (audio.readyState >= 1) reveal();          // already loaded from cache
  audio.addEventListener("loadedmetadata", reveal);

  function label(playing) {
    deck.classList.toggle("is-playing", playing);
    btn.setAttribute("aria-pressed", playing ? "true" : "false");
    btn.setAttribute("aria-label", playing ? "Pause music" : "Play music");
  }

  // The record follows the audio element rather than the click, so it stays
  // in step however playback stops - the track ending, another tab taking
  // the audio, the media keys on a keyboard. The click only asks.
  // The arrow has one job and it is finished the moment the music starts, so
  // it leaves. It does not come back when the track is paused: by then you
  // know what the button is, and a nudge that returns is not a nudge, it is
  // nagging.
  var spent = false;

  function spendNudge() {
    if (!nudge || spent) return;
    spent = true;

    // Nothing to unset first. The entrance animations are on the line and on
    // the two halves of the arrow; what fades here is the element around
    // them, and no animation is filling on that one to outrank the class.
    nudge.classList.add("is-out");

    setTimeout(function () { nudge.hidden = true; }, 450);
  }

  audio.addEventListener("play", function () {
    label(true);
    spendNudge();
    try { localStorage.setItem(HEARD, "1"); } catch (e) {}
  });
  audio.addEventListener("pause", function () { label(false); });
  audio.addEventListener("ended", function () { label(false); });

  // The arrow is about the button, so it may as well be the button. A 46px
  // circle in the corner of a photograph is a small thing to hit, and the
  // arrow under it is the larger half of the same invitation.
  if (nudge) {
    nudge.addEventListener("click", function () {
      if (!spent) btn.click();
    });
  }

  btn.addEventListener("click", function () {
    if (!audio.paused) {
      audio.pause();
      return;
    }
    // play() returns a promise that rejects if the browser refuses - only
    // claim it started once it actually has, or the record turns in silence
    var started = audio.play();
    if (started && started.catch) {
      // the play event covers the success case; this is only for a refusal
      started.catch(function () { label(false); });
    }
  });
})();

/* --- Contact: copy an address instead of opening a mail client --------
   A mailto on a machine with no mail client set up opens nothing at all, and
   a phone number on a desktop is not dialable. Both are things people copy.
   So a modifier-free click copies, and the link still works for anyone who
   wants it to - command or control click, middle click, or the context menu. */
(function () {
  var rows = document.querySelectorAll(".reach-row[data-copy]");
  if (!rows.length || !navigator.clipboard) return;

  rows.forEach(function (row) {
    row.addEventListener("click", function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      e.preventDefault();
      navigator.clipboard.writeText(row.getAttribute("data-copy")).then(function () {
        row.classList.add("is-copied");
        // Long enough to read, short enough that it is gone before the reader
        // wonders whether it is stuck.
        setTimeout(function () { row.classList.remove("is-copied"); }, 1600);
      }).catch(function () {
        // Clipboard refused - permissions, or an insecure origin. Fall back to
        // what the link was always going to do.
        window.location.href = row.getAttribute("href");
      });
    });
  });
})();

/* --- Contact: the message thread --------------------------------------
   The form asks three things, so the thread asks three things, one at a time.
   Each answer goes straight into the hidden input the endpoint reads, so the
   conversation is the form rather than a layer over one. */
(function () {
  var log = document.getElementById("threadLog");
  var form = document.getElementById("contact-form");
  var input = document.getElementById("composerInput");
  var send = document.getElementById("composerSend");
  if (!log || !form || !input || !send) return;

  var ENDPOINT = "https://script.google.com/macros/s/AKfycbxptlQB673K5Zj1cZU8GX2b_nqHctjAFgTgfP1xeSrhKJz8q4wmpk1sY_s8Eh-CJand/exec";

  var answers = {};
  var sndSent = document.getElementById("sndSent");
  var sndReply = document.getElementById("sndReply");

  // Both chimes are short and quiet, and either may be refused - a browser
  // will not play audio before the page has been interacted with, which is
  // exactly the state the first reply arrives in. A refusal is not an error
  // here, so the rejection is swallowed and the thread carries on in silence.
  function chime(el) {
    if (!el) return;
    try {
      el.currentTime = 0;
      var p = el.play();
      if (p && p.catch) p.catch(function () {});
    } catch (e) {}
  }

  // Lines are a function of what has been said already where it matters, so
  // she can use your name back at you rather than reading from a card.
  var SCRIPT = [
    { field: "fName",
      hint: "Your name",
      lines: ["Hi! Thanks for stopping by.", "What should I call you?"] },
    { field: "fEmail",
      hint: "you@example.com",
      lines: function (a) {
        return ["Good to meet you, " + a.fName + ".", "Where should I write back?"];
      },
      // Checked here rather than by the browser, because there is no visible
      // input with type=email any more - and a conversation should answer a
      // bad address the way a person would, by asking again.
      check: function (v) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)
          ? null
          : "That does not look like an email address. Try again?";
      } },
    { field: "fMessage",
      hint: "Your message",
      lines: ["Perfect. What would you like to say?"] }
  ];

  var step = -1;

  var label = document.getElementById("composerLabel");

  // Smooth, unless the reader has asked for less motion, in which case the jump
  // is the correct behaviour rather than a lesser one.
  var smooth = !window.matchMedia
    || !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function toBottom() {
    if (smooth && log.scrollTo) {
      log.scrollTo({ top: log.scrollHeight, behavior: "smooth" });
    } else {
      log.scrollTop = log.scrollHeight;
    }
  }

  function bubble(text, side) {
    var b = document.createElement("div");
    b.className = "bubble " + side;
    // Who said it, for anyone who cannot see which side it is on. The visual
    // cue here is alignment and colour, and neither reaches a screen reader.
    b.setAttribute("aria-label", (side === "in" ? "Kanishka: " : "You: ") + text);
    b.textContent = text;
    log.appendChild(b);
    toBottom();
    return b;
  }

  function note(text) {
    var n = document.createElement("div");
    n.className = "thread-note";
    n.textContent = text;
    log.appendChild(n);
    toBottom();
    return n;
  }

  // Three dots in a bubble while she is "typing". It is the whole reason the
  // replies land one after another rather than all at once: a thread where
  // every answer appears the instant you press send is a form with rounded
  // corners, and the pause is what makes it read as somebody answering.
  function typing() {
    var t = document.createElement("div");
    t.className = "bubble in is-typing";
    t.innerHTML = "<i></i><i></i><i></i>";
    t.setAttribute("aria-hidden", "true");
    log.appendChild(t);
    toBottom();
    return t;
  }

  // Longer lines take longer to type, within reason. A fixed delay on a
  // two-word line feels like a loading spinner.
  function beat(text) {
    return Math.min(1100, 320 + text.length * 16);
  }

  function say(lines, done) {
    var i = 0;
    (function next() {
      if (i >= lines.length) { if (done) done(); return; }
      var dots = typing();
      var line = lines[i++];
      setTimeout(function () {
        dots.remove();
        bubble(line, "in");
        chime(sndReply);
        next();
      }, beat(line));
    })();
  }

  function ask(i) {
    step = i;
    var s = SCRIPT[i];
    var lines = typeof s.lines === "function" ? s.lines(answers) : s.lines;
    input.disabled = true;
    send.disabled = true;
    say(lines, function () {
      busy = false;
      input.placeholder = s.hint;
      // The visible label for the composer is the question just asked, so the
      // field announces what it wants rather than "Your reply" three times.
      // A placeholder alone is not a label and disappears as soon as you type.
      if (label) {
        label.textContent = typeof s.lines === "function"
          ? (s.lines(answers).slice(-1)[0]) : s.lines[s.lines.length - 1];
      }
      input.disabled = false;
      input.focus();
    });
  }

  input.addEventListener("input", function () {
    send.disabled = !input.value.trim();
  });

  var busy = false;

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var text = input.value.trim();
    // step is -1 once the last answer is in, and busy covers the window while
    // she is typing. Without the second guard a fast return key can fire a
    // submit between the answer landing and the field being disabled, which
    // pushes the conversation a step out of sequence.
    if (!text || step < 0 || busy) return;
    busy = true;

    var s = SCRIPT[step];
    bubble(text, "out");
    chime(sndSent);
    input.value = "";
    send.disabled = true;

    // A rejected answer is still a message you sent, so it stays in the
    // thread and she replies to it. Clearing it would be the form telling you
    // it never happened.
    var problem = s.check ? s.check(text) : null;
    if (problem) {
      input.disabled = true;
      say([problem], function () {
        input.disabled = false;
        busy = false;
        input.focus();
      });
      return;
    }

    answers[s.field] = text;
    document.getElementById(s.field).value = text;

    if (step + 1 < SCRIPT.length) {
      ask(step + 1);
      return;
    }

    // Last answer in: close the composer and post the form that was underneath
    // this the whole time.
    step = -1;
    input.disabled = true;
    input.placeholder = "";
    deliver();
  });

  function deliver() {
    var receipt = note("Sending\u2026");

    // The same endpoint, the same FormData, the same no-cors post the old
    // form made. no-cors means the response is opaque - there is no status to
    // read - so a resolved promise means the request left, not that the sheet
    // accepted it. The receipt says "Delivered" rather than "Received" for
    // exactly that reason.
    fetch(form.action || ENDPOINT, {
      method: "POST",
      mode: "no-cors",
      body: new FormData(form)
    }).then(function () {
      receipt.textContent = "Delivered";
      say(["Got it, " + answers.fName + ".",
           "I will reply to " + answers.fEmail + ", usually the same day."]);
    }).catch(function () {
      receipt.remove();
      say(["Something went wrong sending that.",
           "Email me directly at kanishka.chandrakar02@gmail.com and it will reach me."]);
    });
  }

  ask(0);
})();

/* --- Ask KaniGPT: the dialog ------------------------------------------
   The panel used to be a section at the foot of the page that the header
   label scrolled you to. It opens over the page now, from the same label.

   Inner pages still link to index.html#ask, so the hash is honoured on load:
   they arrive here and the dialog is already open, which is what the link
   promised them. */
(function () {
  var box = document.getElementById("askBox");
  if (!box) return;

  var input = document.getElementById("askInput");

  // Where the keyboard was when this opened, so it can be put back. Without
  // it, closing drops focus onto <body> and the next Tab starts again from
  // the top of the page rather than from the label that was just used.
  var returnTo = null;

  function reachable() {
    return box.querySelectorAll("button, [href], textarea, input, select");
  }

  function open(from) {
    if (!box.hidden) return;
    returnTo = from || document.activeElement;
    box.hidden = false;
    // One of the ways in is the link inside the drawer, and the drawer's own
    // dismissal ignores clicks landing inside itself - so without this it
    // stays open behind the scrim, and closing the dialog reveals it again.
    var drawer = document.querySelector(".nav.is-open");
    if (drawer) drawer.classList.remove("is-open");
    document.body.classList.add("is-asking");
    // Into the box you came here to type in. The chips are one tab away and
    // read out as the alternative; landing on them first would put five
    // buttons between the reader and the question they arrived with.
    if (input) input.focus();
  }

  function close() {
    if (box.hidden) return;
    box.hidden = true;
    document.body.classList.remove("is-asking");
    // The hash is what opened it, so it has to go, or the next reload opens
    // the dialog again over a page the reader had just closed it on.
    if (location.hash === "#ask") {
      history.replaceState(null, "", location.pathname + location.search);
    }
    if (returnTo && returnTo.focus) returnTo.focus();
    returnTo = null;
  }

  document.querySelectorAll("[data-ask-open]").forEach(function (el) {
    el.addEventListener("click", function (e) {
      e.preventDefault();
      open(el);
    });
  });

  box.addEventListener("click", function (e) {
    if (e.target.closest("[data-ask-close]")) close();
  });

  document.addEventListener("keydown", function (e) {
    if (box.hidden) return;

    if (e.key === "Escape") {
      close();
      return;
    }

    // Tab is held inside the panel while it is open. A modal that lets the
    // keyboard wander out onto a page nobody can see is a modal in name only:
    // focus goes somewhere behind the scrim and the reader has no way to tell
    // where, short of closing it.
    if (e.key !== "Tab") return;
    var list = reachable();
    if (!list.length) return;

    var first = list[0];
    var last = list[list.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });

  if (location.hash === "#ask") open();
})();

/* --- Ask KaniGPT ------------------------------------------------------ */
(function () {
  var form = document.getElementById("askForm");
  var data = document.getElementById("askData");
  if (!form || !data) return;

  var ANSWERS, MISS;
  try {
    var parsed = JSON.parse(data.textContent);
    ANSWERS = parsed.answers;
    MISS = parsed.miss;
  } catch (e) {
    return;                       // malformed data: leave the box inert
  }

  // Words that appear in almost any question and would otherwise decide the
  // match on their own.
  var STOP = (" a an and are as at be by can do does for from has have he her "
            + "hers him his how i in is it its me much of on or she so tell "
            + "that the their them there they this to was what when where "
            + "which who whom whose why will with you your ")
            .split(" ");

  function words(text) {
    return text.toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/)
      .filter(function (w) { return w && STOP.indexOf(w) < 0; });
  }

  // Scored rather than first-match: "what has she built with" reaches both
  // projects and skills, and the one sharing more of the question should win.
  function bestMatch(question) {
    var asked = words(question);
    if (!asked.length) return null;
    var best = null, bestScore = 0;

    ANSWERS.forEach(function (entry) {
      var keys = entry.keys.split(" ");
      var score = 0;
      asked.forEach(function (w) {
        keys.forEach(function (k) {
          if (k === w) score += 2;
          // a prefix, so "projects" reaches "project" and "coding" reaches
          // "code" without carrying a stemmer around
          else if (k.length > 3 && (w.indexOf(k) === 0 || k.indexOf(w) === 0)) {
            score += 1;
          }
        });
      });
      if (score > bestScore) {
        bestScore = score;
        best = entry;
      }
    });
    return best;
  }

  var thread = document.getElementById("askThread");
  var input = document.getElementById("askInput");

  function esc(text) {
    var d = document.createElement("div");
    d.textContent = text;
    return d.innerHTML;
  }

  function answer(question) {
    // Nothing matched is still an answer. Saying so is the honest reply, and
    // it beats both silence and guessing at one of the seven.
    var hit = bestMatch(question) || MISS;

    var turn = document.createElement("div");
    turn.className = "ask-turn";
    // The question is escaped; it is whatever the reader typed. The answer is
    // not, because it is written in the build and carries entities and markup
    // of its own.
    turn.innerHTML = '<p class="ask-q">' + esc(question) + "</p>"
      + '<div class="ask-a"><span class="ask-dots"><i></i><i></i><i></i></span></div>';
    thread.appendChild(turn);
    turn.scrollIntoView({ block: "nearest", behavior: "smooth" });

    // A beat before the answer. The lookup is instant, and an answer that
    // appears the moment you press the button reads as a page jumping rather
    // than as a reply - the pause is what makes it one.
    var body = turn.querySelector(".ask-a");
    setTimeout(function () {
      body.innerHTML = hit.a
        + (hit.more ? '<br><a class="ask-more" href="' + hit.more[0] + '">'
                      + hit.more[1] + " &rarr;</a>" : "");
      turn.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }, 480);
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var q = input.value.trim();
    if (!q) return;
    answer(q);
    input.value = "";
  });

  // A chip asks its own question, so it behaves the same as typing it
  document.querySelectorAll(".ask-chip").forEach(function (chip) {
    chip.addEventListener("click", function () {
      answer(chip.textContent.trim());
    });
  });

  // Enter asks; shift+enter is a new line, as anywhere else that takes a
  // question in a textarea
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(
        new Event("submit", { cancelable: true }));
    }
  });
})();
