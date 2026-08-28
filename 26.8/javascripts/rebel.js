/**
 * Home page easter egg: type "eda" or "echidna" (outside form fields).
 * Matrix backdrop, mascot A zoom intro, letters fly into EDA / .DEV, lower third.
 */
(function () {
    var CODES = ["eda", "echidna"];
    var BUFFER_RESET_MS = 1500;
    var COOLDOWN_MS = 10000;
    var INTRO_MS = 1200;
    var FLY_STAGGER_MS = 95;
    var FLY_DURATION_MS = 520;
    var LOWER_HOLD_MS = 5000;
    var TEARDOWN_MS = 480;
    var REDUCED_HOLD_MS = 5000;
    var LOWER_STATS_PREFIX = "JOIN THE COMMUNITY";
    var LOWER_STATS_SUFFIX = " · HTTPS://EDA.DEV/DISCORD";
    var LOWER_STATS_TYPE_MS = 40;
    var LOWER_TYPEWRITER_DELAY_MS = 400;

    var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function mascotSrc(path) {
        try {
            return new URL(path, document.baseURI).href;
        } catch (err) {
            return path;
        }
    }

    var mascotUrl = mascotSrc("images/eda.svg");

    var FLY_CHARS = ["E", "D", "A", ".", "D", "E", "V"];
    var FLY_FROM = [
        { fx: -5.5, fy: 0 },
        { fx: 5.5, fy: -1.5 },
        { fx: 0, fy: 3.5 },
        { fx: -4.5, fy: 2 },
        { fx: 5, fy: -2 },
        { fx: -4, fy: 2.5 },
        { fx: 5.5, fy: 1.2 }
    ];

    var codeBuffers = { eda: "", echidna: "" };
    var lastKeyTime = 0;
    var cooldownUntil = 0;

    function typingInField(target) {
        if (!target || !target.tagName) {
            return false;
        }
        var tag = target.tagName.toUpperCase();
        if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") {
            return true;
        }
        if (target.isContentEditable) {
            return true;
        }
        if (target.closest && target.closest("input, textarea, select, [contenteditable='true']")) {
            return true;
        }
        return false;
    }

    function fillMatrix(matrixEl) {
        var cw = 5.5;
        var ch = 11;
        var cols = Math.min(200, Math.ceil(window.innerWidth / cw));
        var rows = Math.min(120, Math.ceil(window.innerHeight / ch));
        var frag = document.createDocumentFragment();
        for (var r = 0; r < rows; r += 1) {
            var line = document.createElement("div");
            line.className = "eda-egg-matrix-row";
            var bits = "";
            for (var c = 0; c < cols; c += 1) {
                bits += Math.random() < 0.5 ? "0" : "1";
            }
            line.textContent = bits;
            frag.appendChild(line);
        }
        matrixEl.appendChild(frag);
    }

    function removeOverlay(overlay) {
        if (!overlay || !overlay.parentNode) {
            return;
        }
        overlay.classList.add("eda-egg-overlay--out");
        window.setTimeout(function () {
            if (overlay.parentNode) {
                overlay.parentNode.removeChild(overlay);
            }
        }, TEARDOWN_MS);
    }

    function fillLowerStatsFull(overlay) {
        var stats = overlay.querySelector(".eda-egg-lower-stats");
        if (stats) {
            stats.textContent = LOWER_STATS_PREFIX + LOWER_STATS_SUFFIX;
        }
    }

    function startLowerStatsTypewriter(overlay) {
        var stats = overlay.querySelector(".eda-egg-lower-stats");
        if (!stats) {
            return;
        }
        if (prefersReducedMotion) {
            fillLowerStatsFull(overlay);
            return;
        }
        stats.textContent = "";
        stats.classList.add("eda-egg-lower-stats--typing");
        function tick(i) {
            if (!overlay.parentNode) {
                stats.classList.remove("eda-egg-lower-stats--typing");
                return;
            }
            var len = LOWER_STATS_PREFIX.length;
            if (i < len) {
                stats.textContent = LOWER_STATS_PREFIX.slice(0, i + 1);
                window.setTimeout(function () {
                    tick(i + 1);
                }, LOWER_STATS_TYPE_MS);
            } else {
                stats.textContent = LOWER_STATS_PREFIX + LOWER_STATS_SUFFIX;
                stats.classList.remove("eda-egg-lower-stats--typing");
            }
        }
        window.setTimeout(function () {
            if (!overlay.parentNode) {
                stats.classList.remove("eda-egg-lower-stats--typing");
                return;
            }
            tick(0);
        }, LOWER_TYPEWRITER_DELAY_MS);
    }

    function buildOverlay() {
        var el = document.createElement("div");
        el.className = "eda-egg-overlay";
        el.setAttribute("aria-hidden", "true");
        el.innerHTML =
            '<div class="eda-egg-matrix"></div>' +
            '<div class="eda-egg-backdrop"></div>' +
            '<div class="eda-egg-hero">' +
            '<img class="eda-egg-mascot" alt="" src="' +
            mascotUrl +
            '"/>' +
            "</div>" +
            '<div class="eda-egg-kinetic"></div>' +
            '<div class="eda-egg-lockup">' +
            '<div class="eda-egg-lockup-main">EDA</div>' +
            '<div class="eda-egg-lockup-sub">.DEV</div>' +
            "</div>" +
            '<div class="eda-egg-lower">' +
            '<img class="eda-egg-lower-logo" alt="" src="' +
            mascotUrl +
            '"/>' +
            '<div class="eda-egg-lower-body">' +
            '<div class="eda-egg-lower-title">EDA</div>' +
            '<div class="eda-egg-lower-stats" aria-live="polite"></div>' +
            "</div></div>";
        fillMatrix(el.querySelector(".eda-egg-matrix"));
        return el;
    }

    function startEasterEggReduced() {
        cooldownUntil = Date.now() + COOLDOWN_MS;
        var overlay = buildOverlay();
        overlay.classList.add("eda-egg-overlay--reduced");
        overlay.classList.add("eda-egg-phase-intro");
        document.body.appendChild(overlay);
        fillLowerStatsFull(overlay);
        window.setTimeout(function () {
            removeOverlay(overlay);
        }, REDUCED_HOLD_MS + 500);
    }

    function startEasterEgg() {
        cooldownUntil = Date.now() + COOLDOWN_MS;
        var overlay = buildOverlay();
        var kineticHost = overlay.querySelector(".eda-egg-kinetic");

        function t(fn, ms) {
            window.setTimeout(fn, ms);
        }

        document.body.appendChild(overlay);
        window.requestAnimationFrame(function () {
            window.requestAnimationFrame(function () {
                overlay.classList.add("eda-egg-phase-intro");
            });
        });

        function runKinetic() {
            overlay.classList.add("eda-egg-phase-kinetic");
            var wrap = document.createElement("div");
            wrap.className = "eda-egg-fly-lockup";
            wrap.style.setProperty("--fly-ms", String(FLY_DURATION_MS));
            var rowMain = document.createElement("div");
            rowMain.className = "eda-egg-fly-row eda-egg-fly-row--main";
            var rowSub = document.createElement("div");
            rowSub.className = "eda-egg-fly-row eda-egg-fly-row--sub";

            function addChar(idx) {
                var sp = document.createElement("span");
                sp.className = "eda-egg-fly-char";
                sp.textContent = FLY_CHARS[idx];
                sp.style.setProperty("--fx", String(FLY_FROM[idx].fx));
                sp.style.setProperty("--fy", String(FLY_FROM[idx].fy));
                sp.style.setProperty("--stagger", String(idx * FLY_STAGGER_MS));
                return sp;
            }

            for (var a = 0; a < 3; a += 1) {
                rowMain.appendChild(addChar(a));
            }
            for (var b = 3; b < 7; b += 1) {
                rowSub.appendChild(addChar(b));
            }
            wrap.appendChild(rowMain);
            wrap.appendChild(rowSub);
            kineticHost.innerHTML = "";
            kineticHost.appendChild(wrap);

            var kineticDoneMs = FLY_STAGGER_MS * 6 + FLY_DURATION_MS + 220;
            t(function () {
                overlay.classList.remove("eda-egg-phase-kinetic");
                overlay.classList.add("eda-egg-phase-lower");
                if (prefersReducedMotion) {
                    fillLowerStatsFull(overlay);
                } else {
                    startLowerStatsTypewriter(overlay);
                }
                t(function () {
                    removeOverlay(overlay);
                }, LOWER_HOLD_MS);
            }, kineticDoneMs);
        }

        t(runKinetic, INTRO_MS);
    }

    document.addEventListener("keydown", function (e) {
        if (Date.now() < cooldownUntil) {
            return;
        }
        if (typingInField(e.target)) {
            return;
        }
        if (e.ctrlKey || e.metaKey || e.altKey) {
            return;
        }

        if (e.repeat) {
            return;
        }

        if (Date.now() - lastKeyTime > BUFFER_RESET_MS) {
            codeBuffers.eda = "";
            codeBuffers.echidna = "";
        }
        lastKeyTime = Date.now();

        if (e.key.length !== 1) {
            return;
        }

        var ch = e.key.toLowerCase();
        var triggered = false;

        for (var i = 0; i < CODES.length; i += 1) {
            var code = CODES[i];
            var buffer = codeBuffers[code];
            var next = code[buffer.length];
            if (ch === next) {
                buffer += ch;
                codeBuffers[code] = buffer;
                if (buffer === code) {
                    triggered = true;
                }
            } else {
                codeBuffers[code] = ch === code[0] ? code[0] : "";
            }
        }

        if (triggered) {
            codeBuffers.eda = "";
            codeBuffers.echidna = "";
            if (prefersReducedMotion) {
                startEasterEggReduced();
            } else {
                startEasterEgg();
            }
        }
    });
})();
