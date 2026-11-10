// Ramtin Tech Zone — category filter + live search (no dependencies).
(function () {
  var grid = document.getElementById("card-grid");
  if (!grid) return;
  var cards = Array.prototype.slice.call(grid.querySelectorAll(".card"));
  var chips = document.querySelectorAll(".chip[data-filter]");
  var search = document.getElementById("search");
  var noResults = document.getElementById("no-results");
  var activeFilter = "all";

  // Support ?cat=MikroTik deep links from post pages.
  var params = new URLSearchParams(window.location.search);
  var preset = params.get("cat");
  if (preset) {
    var match = document.querySelector('.chip[data-filter="' + preset + '"]');
    if (match) activeFilter = preset;
  }

  function apply() {
    var q = (search ? search.value : "").trim().toLowerCase();
    var visible = 0;
    cards.forEach(function (card) {
      var cats = (card.getAttribute("data-categories") || "").split(",");
      var hay = card.getAttribute("data-search") || "";
      var okFilter = activeFilter === "all" || cats.indexOf(activeFilter) !== -1;
      var okSearch = !q || hay.indexOf(q) !== -1;
      var show = okFilter && okSearch;
      card.style.display = show ? "" : "none";
      if (show) visible++;
    });
    if (noResults) noResults.hidden = visible !== 0;
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
