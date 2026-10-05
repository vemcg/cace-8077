// Flashcard practice widget for the [[flashcards: deck.json]] directive (see
// scripts/build_decks.py and the README's "Review" section). The build embeds
// the deck as <script type="application/json" class="flashcards-data"> inside
// each <div class="flashcards">; this file turns every such div into a
// practice round. Progress lives in the student's own localStorage and never
// leaves the browser (Export/Import moves it between browsers).
//
// Scheduling is the Learn2X Leitner scheme: boxes 0-5, review gaps in DAYS.

(function () {
  var DAYS = [1, 2, 4, 8, 16];
  var DAY_MS = 24 * 60 * 60 * 1000;
  var PRACTICE_SIZE = 5;
  var STAR_LABELS = [
    "I don't understand this",
    "I got part of it",
    "I got most of it",
    "I got it completely",
  ];

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function button(label, className, onClick) {
    var b = el("button", "fc-btn " + (className || ""), label);
    b.type = "button";
    b.addEventListener("click", onClick);
    return b;
  }

  function shuffle(list) {
    var a = list.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i];
      a[i] = a[j];
      a[j] = t;
    }
    return a;
  }

  function clamp(n, lo, hi) {
    return Math.max(lo, Math.min(hi, n));
  }

  function parseDeck(host) {
    try {
      var script = host.querySelector("script.flashcards-data");
      var deck = JSON.parse(script.textContent);
      if (!deck || typeof deck.deckId !== "string" || !Array.isArray(deck.cards) || !deck.cards.length) {
        return null;
      }
      return deck;
    } catch (e) {
      return null;
    }
  }

  function describeWait(ms) {
    var days = Math.ceil(ms / DAY_MS);
    if (ms <= 0) return "now";
    if (ms < DAY_MS) return "later today";
    return "in " + days + (days === 1 ? " day" : " days");
  }

  function initWidget(host) {
    var root = el("div", "fc-root");
    var old = host.querySelector("noscript");
    if (old) old.remove();
    host.appendChild(root);

    var deck = parseDeck(host);
    if (!deck) {
      root.appendChild(
        el("p", "fc-message", "These flash cards couldn't be loaded (the deck data is missing or invalid).")
      );
      return;
    }

    var storageKey = "learn2x:progress:" + deck.deckId;
    var progress = loadProgress();
    var round = [];
    var pos = 0;
    var revealed = false;
    var practiceMode = false;
    var status = "";
    var userActed = false;

    function loadProgress() {
      try {
        var raw = window.localStorage.getItem(storageKey);
        var parsed = raw ? JSON.parse(raw) : {};
        return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : {};
      } catch (e) {
        return {};
      }
    }

    function saveProgress() {
      try {
        window.localStorage.setItem(storageKey, JSON.stringify(progress));
        return true;
      } catch (e) {
        return false;
      }
    }

    // --- Rounds -----------------------------------------------------------

    function groups() {
      var now = Date.now();
      var unseen = [];
      var due = [];
      var weak = [];
      deck.cards.forEach(function (card) {
        var rec = progress[card.id];
        if (!rec) unseen.push(card);
        else if (rec.stars <= 2) weak.push(card);
        else if (rec.due <= now) due.push(card);
      });
      return { unseen: unseen, due: due, weak: weak };
    }

    function startRound(practice) {
      var g = groups();
      practiceMode = practice;
      round = practice
        ? shuffle(g.weak).slice(0, PRACTICE_SIZE)
        : shuffle(g.unseen).concat(shuffle(g.due), shuffle(g.weak));
      pos = 0;
      revealed = false;
      userActed = true;
      render();
    }

    function rate(card, stars) {
      var rec = progress[card.id] || {};
      var prev = rec.box || 0;
      var now = Date.now();
      var box;
      var due;
      if (stars === 1) {
        box = 0;
        due = now;
      } else {
        box = clamp(prev + { 2: -1, 3: 1, 4: 2 }[stars], 0, 5);
        due = now + DAYS[Math.max(box, 1) - 1] * DAY_MS;
      }
      progress[card.id] = { box: box, due: due, lastReviewed: now, stars: stars };
      if (!saveProgress()) {
        status = "Couldn't save progress in this browser; it will last only until you reload.";
      }
      pos += 1;
      revealed = false;
      userActed = true;
      render();
    }

    // --- Export / import ----------------------------------------------------

    function exportProgress() {
      try {
        var blob = new Blob(
          [JSON.stringify({ deckId: deck.deckId, progress: progress }, null, 2)],
          { type: "application/json" }
        );
        var url = URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = "flashcards-progress-" + deck.deckId + ".json";
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(function () {
          URL.revokeObjectURL(url);
        }, 1000);
        status = "Progress exported.";
      } catch (e) {
        status = "Couldn't export progress.";
      }
      render();
    }

    function importProgress(file) {
      var reader = new FileReader();
      reader.onload = function () {
        try {
          var data = JSON.parse(reader.result);
          var incoming = data && data.progress && typeof data.progress === "object" ? data.progress : data;
          var known = {};
          deck.cards.forEach(function (c) {
            known[c.id] = true;
          });
          var count = 0;
          Object.keys(incoming).forEach(function (id) {
            var rec = incoming[id];
            if (!known[id] || !rec || typeof rec.stars !== "number" || typeof rec.due !== "number") return;
            var mine = progress[id];
            if (!mine || (rec.lastReviewed || 0) > (mine.lastReviewed || 0)) {
              progress[id] = {
                box: clamp(Math.round(rec.box || 0), 0, 5),
                due: rec.due,
                lastReviewed: rec.lastReviewed || 0,
                stars: rec.stars,
              };
              count += 1;
            }
          });
          saveProgress();
          status = count
            ? "Imported progress for " + count + (count === 1 ? " card." : " cards.")
            : "Nothing new to import from that file.";
        } catch (e) {
          status = "That file isn't a progress export.";
        }
        round = [];
        pos = 0;
        render();
      };
      reader.readAsText(file);
    }

    // --- Rendering ----------------------------------------------------------

    function renderFooter() {
      var footer = el("div", "fc-footer");
      var row = el("div", "fc-footer-row");
      row.appendChild(button("Export progress", "fc-small", exportProgress));
      var importBtn = button("Import progress", "fc-small", function () {
        input.click();
      });
      var input = el("input");
      input.type = "file";
      input.accept = "application/json,.json";
      input.style.display = "none";
      input.addEventListener("change", function () {
        if (input.files && input.files[0]) importProgress(input.files[0]);
      });
      row.appendChild(importBtn);
      row.appendChild(input);
      footer.appendChild(row);
      var note =
        "Your progress is saved only in this browser. The instructor can't see it.";
      if (window.location.protocol === "file:") {
        note += " (Opened from disk, so it's kept separately from the published site.)";
      }
      footer.appendChild(el("p", "fc-note", note));
      if (status) footer.appendChild(el("p", "fc-status", status));
      return footer;
    }

    function renderStart() {
      var g = groups();
      var panel = el("div", "fc-panel");
      panel.appendChild(el("p", "fc-title", deck.title));
      var ready = g.unseen.length + g.due.length;
      if (ready) {
        panel.appendChild(
          el(
            "p",
            "fc-message",
            deck.cards.length + " cards: " + g.unseen.length + " new, " + g.due.length +
              " due for review, " + g.weak.length + " to strengthen."
          )
        );
        var start = button("Start round (" + (ready + g.weak.length) + " cards)", "fc-primary", function () {
          startRound(false);
        });
        panel.appendChild(start);
      } else if (g.weak.length) {
        panel.appendChild(
          el("p", "fc-message", "Nothing new or due. A short practice round covers cards you found hard.")
        );
        panel.appendChild(
          button(
            "Practice " + Math.min(PRACTICE_SIZE, g.weak.length) + " weak cards",
            "fc-primary",
            function () {
              startRound(true);
            }
          )
        );
      } else {
        var next = Infinity;
        var now = Date.now();
        Object.keys(progress).forEach(function (id) {
          if (progress[id] && typeof progress[id].due === "number") next = Math.min(next, progress[id].due);
        });
        panel.appendChild(
          el(
            "p",
            "fc-message",
            "Nothing to practice yet: every card is rated 3 or 4 stars and none are due" +
              (next === Infinity ? "." : "; the next is due " + describeWait(next - now) + ".")
          )
        );
      }
      return panel;
    }

    function renderCard() {
      var card = round[pos];
      var panel = el("div", "fc-panel");
      var left = round.length - pos;
      panel.appendChild(
        el(
          "p",
          "fc-progress",
          (practiceMode ? "Practice · " : "") + left + (left === 1 ? " card" : " cards") + " left in this round"
        )
      );
      panel.appendChild(el("p", "fc-question", card.front));
      if (!revealed) {
        panel.appendChild(
          button("Show answer", "fc-primary", function () {
            revealed = true;
            userActed = true;
            render();
          })
        );
        return panel;
      }
      panel.appendChild(el("p", "fc-answer", card.back));
      if (card.source && card.source.title && /^https?:/i.test(card.source.url || "")) {
        var src = el("p", "fc-source");
        var a = el("a", "", card.source.title);
        a.href = card.source.url;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        src.appendChild(a);
        panel.appendChild(src);
      }
      var ratings = el("div", "fc-ratings");
      STAR_LABELS.forEach(function (label, i) {
        var stars = i + 1;
        var b = button("", "fc-rate", function () {
          rate(card, stars);
        });
        b.appendChild(el("span", "fc-stars", new Array(stars + 1).join("★")));
        b.appendChild(el("span", "fc-rate-label", stars + " – " + label));
        ratings.appendChild(b);
      });
      panel.appendChild(ratings);
      return panel;
    }

    function renderSummary() {
      var panel = el("div", "fc-panel");
      panel.appendChild(el("p", "fc-title", "Round complete"));
      panel.appendChild(
        el("p", "fc-message", "You went through " + round.length + (round.length === 1 ? " card." : " cards."))
      );
      panel.appendChild(
        button("Back to start", "fc-primary", function () {
          round = [];
          pos = 0;
          userActed = true;
          render();
        })
      );
      return panel;
    }

    function render() {
      root.textContent = "";
      var panel;
      if (round.length && pos < round.length) panel = renderCard();
      else if (round.length) panel = renderSummary();
      else panel = renderStart();
      root.appendChild(panel);
      root.appendChild(renderFooter());
      // Keep keyboard focus inside the widget after each action; otherwise the
      // re-render drops focus to <body> and Space/arrows would move the slide.
      if (userActed) {
        var primary = root.querySelector(".fc-primary") || root.querySelector(".fc-rate");
        if (primary) primary.focus({ preventScroll: true });
      }
    }

    // reveal.js and deck.js listen for keys on the document; stop them here so
    // Space/arrows/'f' don't change slides while a card is open.
    host.addEventListener("keydown", function (e) {
      e.stopPropagation();
      if (revealed && round.length && pos < round.length && /^[1-4]$/.test(e.key)) {
        e.preventDefault();
        rate(round[pos], parseInt(e.key, 10));
      }
    });

    render();
  }

  document.addEventListener("DOMContentLoaded", function () {
    Array.prototype.forEach.call(document.querySelectorAll(".flashcards"), initWidget);
  });
})();
