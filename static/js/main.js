// Ramtin Tech Zone — category filter + live search (no dependencies).
//
// The home page is paginated server-side (12 posts per page), so the cards
// in the DOM are only the current page. When a filter or search is active,
// results come from assets/posts.json (the full index), so they cover all
// posts site-wide and the pagination hides. Clearing both restores the
// server-rendered page. If posts.json fails to load, filtering falls back
// to the cards on the current page.
(function () {
  var grid = document.getElementById("card-grid");
  if (!grid) return;
  var pagination = document.getElementById("pagination");
  var chips = document.querySelectorAll(".chip[data-filter]");
  var search = document.getElementById("search");
  var noResults = document.getElementById("no-results");
  // All URLs are root-absolute: the site lives at ramtin.zone (the
  // github.io subpath redirects there), so relative ../ paths buy nothing
  // and proved fragile. Server-rendered cards use the same form.
  var originalHTML = grid.innerHTML;
  var index = null;       // full post index, once loaded
  var indexFailed = false;
  var indexPromise = null;
  var activeFilter = "all";

  // Support ?cat=MikroTik deep links from post pages.
  var params = new URLSearchParams(window.location.search);
  var preset = params.get("cat");
  if (preset) {
    var match = document.querySelector('.chip[data-filter="' + preset + '"]');
    if (match) activeFilter = preset;
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function cardHTML(p) {
    var thumb = p.thumb_is_local ? "/" + p.thumb : p.thumb;
    var img = '<img src="' + esc(thumb) + '" alt="" loading="lazy"'
      + (p.thumb_is_local
        ? ""
        : ' onerror="this.onerror=null;this.src=\'' + esc(p.thumb_fallback) + '\';"')
      + ">";
    var dur = p.duration
      ? '<span class="card-duration">' + esc(p.duration) + "</span>"
      : "";
    var tags = p.categories
      .map(function (c) { return '<span class="tag">' + esc(c) + "</span>"; })
      .join("");
    var views = p.views ? "<span>" + esc(p.views) + " views</span>" : "";
    return '<article class="card">'
      + '<a class="card-thumb" href="/posts/' + esc(p.slug) + '/" aria-label="' + esc(p.title) + '">'
      + img + dur + "</a>"
      + '<div class="card-body"><div class="card-meta">' + tags
      + '<time datetime="' + esc(p.date) + '">' + esc(p.date_human) + "</time></div>"
      + '<h2 class="card-title"><a href="/posts/' + esc(p.slug) + '/">' + esc(p.title) + "</a></h2>"
      + '<p class="card-desc">' + esc(p.description) + "</p>"
      + '<div class="card-foot"><span>' + p.reading_time + " min read</span>" + views
      + '<a class="card-link" href="/posts/' + esc(p.slug) + '/">Read tutorial →</a></div>'
      + "</div></article>";
  }

  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch("/assets/posts.json")
        .then(function (r) {
          if (!r.ok) throw new Error("posts.json " + r.status);
          return r.json();
        })
        .then(function (data) { index = data; })
        .catch(function () { indexFailed = true; });
    }
    return indexPromise;
  }

  function renderFromIndex() {
    var q = (search ? search.value : "").trim().toLowerCase();
    var matches = index.filter(function (p) {
      var okFilter = activeFilter === "all" || p.categories.indexOf(activeFilter) !== -1;
      var hay = (p.title + " " + p.description).toLowerCase();
      return okFilter && (!q || hay.indexOf(q) !== -1);
    });
    grid.innerHTML = matches.map(cardHTML).join("");
    if (pagination) pagination.style.display = "none";
    if (noResults) noResults.hidden = matches.length !== 0;
  }

  // Fallback when posts.json is unavailable: filter only this page's cards.
  function filterCurrentPage() {
    var q = (search ? search.value : "").trim().toLowerCase();
    var visible = 0;
    Array.prototype.slice.call(grid.querySelectorAll(".card")).forEach(function (card) {
      var cats = (card.getAttribute("data-categories") || "").split(",");
      var hay = card.getAttribute("data-search") || "";
      var show =
        (activeFilter === "all" || cats.indexOf(activeFilter) !== -1) &&
        (!q || hay.indexOf(q) !== -1);
      card.style.display = show ? "" : "none";
      if (show) visible++;
    });
    // Filtering replaces the paginated view, so the pagination hides here
    // too — restorePage() brings it back when the filter is cleared.
    if (pagination) pagination.style.display = "none";
    if (noResults) noResults.hidden = visible !== 0;
  }

  function restorePage() {
    grid.innerHTML = originalHTML;
    if (pagination) pagination.style.display = "";
    if (noResults) noResults.hidden = true;
  }

  function apply() {
    var q = (search ? search.value : "").trim().toLowerCase();
    if (activeFilter === "all" && !q) {
      restorePage();
      return;
    }
    if (index) {
      renderFromIndex();
      return;
    }
    if (indexFailed) {
      filterCurrentPage();
      return;
    }
    loadIndex().then(function () {
      if (index) renderFromIndex();
      else filterCurrentPage();
    });
  }

  chips.forEach(function (chip) {
    if (chip.getAttribute("data-filter") === activeFilter) chip.classList.add("active");
    else chip.classList.remove("active");
    chip.addEventListener("click", function () {
      activeFilter = chip.getAttribute("data-filter");
      chips.forEach(function (c) { c.classList.toggle("active", c === chip); });
      apply();
    });
  });
  if (search) search.addEventListener("input", apply);
  apply();
})();
