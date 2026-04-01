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

document.addEventListener("DOMContentLoaded", function () {
  syncDataTheme();

  var topic = document.querySelector(".md-header__topic");
  var versionTarget = document.querySelector(".md-header__version");
  if (topic && versionTarget) {
    new MutationObserver(function () {
      var versionEl = topic.querySelector(".md-version");
      if (versionEl) {
        versionTarget.appendChild(versionEl);
      }
    }).observe(topic, { childList: true });
  }

  var toggle = document.getElementById("theme-toggle");
  if (!toggle) return;

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
});
