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
  relocateMikeVersion();
  bindThemeToggle();
}

if (typeof document$ !== "undefined" && document$.subscribe) {
  document$.subscribe(initThemeTogglePage);
} else {
  document.addEventListener("DOMContentLoaded", initThemeTogglePage);
}
