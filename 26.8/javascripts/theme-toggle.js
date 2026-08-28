function syncDataTheme() {
  var scheme = document.body.getAttribute("data-md-color-scheme");
  document.documentElement.setAttribute(
    "data-theme",
    scheme === "slate" ? "dark" : "light"
  );
}

new MutationObserver(syncDataTheme).observe(document.body, {
  attributes: true,
  attributeFilter: ["data-md-color-scheme"],
});

function relocateMikeVersion() {
  var target = document.querySelector(".md-header__version");
  if (!target) return;
  var picker = document.querySelector(".md-header .md-version");
  if (picker && !target.contains(picker)) {
    target.appendChild(picker);
  }
}

var mikeVersionObserver;
var mikeVersionObserverTarget;

// Material creates the mike version picker after loading versions.json; on
// refreshes with a hash, this can happen after our page init, so watch for it.
function watchMikeVersion() {
  var header = document.querySelector(".md-header");
  if (!header) return;

  if (mikeVersionObserver && mikeVersionObserverTarget === header) {
    return;
  }

  if (mikeVersionObserver) {
    mikeVersionObserver.disconnect();
  }

  mikeVersionObserverTarget = header;
  mikeVersionObserver = new MutationObserver(relocateMikeVersion);
  mikeVersionObserver.observe(header, { childList: true, subtree: true });
}

function bindThemeToggle() {
  var toggle = document.getElementById("theme-toggle");
  if (!toggle || toggle.getAttribute("data-nokia-theme-toggle-bound") === "1") {
    return;
  }
  toggle.setAttribute("data-nokia-theme-toggle-bound", "1");

  toggle.addEventListener("click", function () {
    var isDark = document.documentElement.getAttribute("data-theme") === "dark";
    document.documentElement.setAttribute(
      "data-theme",
      isDark ? "light" : "dark"
    );

    var form = document.querySelector("[data-md-component=palette]");
    if (!form) return;
    var label = form.querySelector("label:not([hidden])");
    if (!label) return;

    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        label.click();
      });
    });
  });
}

function initThemeTogglePage() {
  syncDataTheme();
  watchMikeVersion();
  relocateMikeVersion();
  bindThemeToggle();
}

if (typeof document$ !== "undefined" && document$.subscribe) {
  document$.subscribe(initThemeTogglePage);
} else {
  document.addEventListener("DOMContentLoaded", initThemeTogglePage);
}
