// Shared behavior for every session deck: reveal.js init sized to match the
// 1600x900 background photos (so the slide box fills the photo instead of
// letterboxing inside it), an 'f' fullscreen shortcut, and a bottom dot strip
// -- one dot per slide, red if that slide's content overflows the 900px
// slide height and needs trimming.

document.addEventListener("DOMContentLoaded", function () {
  Reveal.initialize({ hash: true, width: 1600, height: 900 });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "f" && e.key !== "F") return;
    if (document.fullscreenElement) {
      document.exitFullscreen();
    } else {
      document.documentElement.requestFullscreen().catch(function () {});
    }
  });

  var sections = Array.prototype.slice.call(
    document.querySelectorAll(".reveal .slides > section")
  );

  function measureOverflow() {
    var probe = document.createElement("div");
    probe.className = "reveal";
    probe.style.cssText =
      "position:absolute; visibility:hidden; top:-9999px; left:-9999px; width:1600px;";
    var slidesWrap = document.createElement("div");
    slidesWrap.className = "slides";
    slidesWrap.style.width = "1600px";
    probe.appendChild(slidesWrap);
    document.body.appendChild(probe);

    var flags = sections.map(function (section) {
      var clone = section.cloneNode(true);
      clone.style.display = "block";
      clone.style.position = "static";
      clone.style.width = "1600px";
      clone.style.boxSizing = "border-box";
      slidesWrap.innerHTML = "";
      slidesWrap.appendChild(clone);
      return clone.scrollHeight > 900;
    });

    probe.remove();
    return flags;
  }

  var overflowFlags = measureOverflow();

  var dotsWrap = document.createElement("div");
  dotsWrap.className = "slide-dots";
  sections.forEach(function (section, i) {
    var dot = document.createElement("button");
    dot.type = "button";
    dot.className = "slide-dot" + (overflowFlags[i] ? " overflow" : "");
    dot.setAttribute(
      "aria-label",
      "Slide " + (i + 1) + (overflowFlags[i] ? " (overflows, needs trimming)" : "")
    );
    dot.addEventListener("click", function () {
      Reveal.slide(i);
    });
    dotsWrap.appendChild(dot);
  });
  document.querySelector(".reveal").appendChild(dotsWrap);

  function syncActiveDot() {
    var idx = Reveal.getIndices().h;
    Array.prototype.forEach.call(dotsWrap.children, function (dot, i) {
      dot.classList.toggle("active", i === idx);
    });
  }

  Reveal.on("ready", syncActiveDot);
  Reveal.on("slidechanged", syncActiveDot);
});
