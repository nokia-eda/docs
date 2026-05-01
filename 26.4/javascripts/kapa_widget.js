(function () {
    var KAPA_SCRIPT_SRC = "https://widget.kapa.ai/kapa-widget.bundle.js";
    var SEARCH_HINT_HTML =
        'Type to start searching or press <span class="md-search__ai-keycap" role="img" aria-label="dot key">.</span> (dot) to search with AI';
    var isApplyingHint = false;
    var isModalCloseHookBound = false;

    function isHomePage() {
        return !!document.querySelector(".hero-banner");
    }

    function ensureKapaPreinitialized() {
        if (window.Kapa) {
            return;
        }

        var proxy = function () {
            proxy.c(arguments);
        };
        proxy.q = [];
        proxy.c = function (args) {
            proxy.q.push(args);
        };
        window.Kapa = proxy;
    }

    function callKapa(method, payload, option) {
        if (!window.Kapa) {
            return;
        }

        var hasPayload = typeof payload !== "undefined";
        var hasOption = typeof option !== "undefined";

        if (typeof window.Kapa[method] === "function") {
            if (hasOption) {
                window.Kapa[method](payload, option);
                return;
            }
            if (hasPayload) {
                window.Kapa[method](payload);
                return;
            }
            window.Kapa[method]();
            return;
        }

        if (typeof window.Kapa === "function") {
            if (hasOption) {
                window.Kapa(method, payload, option);
                return;
            }
            if (hasPayload) {
                window.Kapa(method, payload);
                return;
            }
            window.Kapa(method);
        }
    }

    function loadKapaScript() {
        if (document.querySelector('script[src="' + KAPA_SCRIPT_SRC + '"]')) {
            return;
        }

        var script = document.createElement("script");
        script.src = KAPA_SCRIPT_SRC;
        script.setAttribute("data-website-id", "1c088ecb-08f8-466b-b43c-1ba6952d5405");
        script.setAttribute("data-source-group-ids-include", "be674990-628a-4489-9b95-36f6052a9654");
        script.setAttribute("data-project-name", "Nokia EDA");
        script.setAttribute("data-color-scheme", "auto");
        script.setAttribute("data-modal-title", "Nokia Event-Driven Automation AI Assistant");
        script.setAttribute("data-project-color", "#005AFF");
        script.setAttribute("data-project-logo", "https://documentation.nokia.com/sr/releases/nokia_stars.png");
        script.setAttribute("data-render-on-load", "false");
        script.setAttribute("data-launcher-button-text", "");
        script.setAttribute("data-launcher-button-label-font-size", "0rem");
        script.setAttribute("data-launcher-button-height", "32px");
        script.setAttribute("data-launcher-button-width", "32px");
        script.setAttribute("data-launcher-button-image-height", "20px");
        script.setAttribute("data-launcher-button-image-width", "20px");
        script.setAttribute("data-uncertain-answer-callout", "AI tried its best, but couldn't find the definitive answer. Maybe it is time to talk to a real human being? Join our [Discord](https://eda.dev/discord) server and ask your question there.");
        script.setAttribute("data-scale-factor", "0.8");
        script.async = true;
        document.head.appendChild(script);
    }

    function mountKapaWidget() {
        callKapa("render");
    }

    function unmountKapaWidget() {
        callKapa("unmount");
    }

    function openKapaAi() {
        callKapa("open", { mode: "ai" });
    }

    function openKapaAiForCurrentPage() {
        if (isHomePage()) {
            openKapaAi();
            return;
        }

        renderAndOpenKapaAi();
    }

    function renderAndOpenKapaAi() {
        var opened = false;
        function openOnce() {
            if (opened) {
                return;
            }
            opened = true;
            openKapaAi();
        }

        callKapa("render", { onRender: openOnce });
        window.setTimeout(openOnce, 75);
    }

    function bindAiTriggerClicks() {
        var root = document.documentElement;
        if (root.dataset.kapaAiTriggerBound === "true") {
            return;
        }

        document.addEventListener("click", function (event) {
            var target = event.target;
            if (!target || !target.closest) {
                return;
            }

            var trigger = target.closest('[data-kapa-open="ai"]');
            if (!trigger) {
                return;
            }

            event.preventDefault();
            closeMaterialSearch();
            openKapaAiForCurrentPage();
        });

        root.dataset.kapaAiTriggerBound = "true";
    }

    function bindNonHomeModalCloseUnmount() {
        if (isModalCloseHookBound || !window.Kapa) {
            return;
        }

        var handleModalClose = function () {
            if (!isHomePage()) {
                unmountKapaWidget();
            }
        };

        if (typeof window.Kapa === "function") {
            window.Kapa("onModalClose", handleModalClose, "add");
            isModalCloseHookBound = true;
            return;
        }

        if (typeof window.Kapa.onModalClose === "function") {
            window.Kapa.onModalClose(handleModalClose);
            isModalCloseHookBound = true;
        }
    }

    function closeMaterialSearch() {
        var searchToggle = document.querySelector('[data-md-toggle="search"]');
        if (searchToggle) {
            searchToggle.checked = false;
            searchToggle.dispatchEvent(new Event("change", { bubbles: true }));
        }

        var input = document.querySelector('[data-md-component="search-query"]');
        if (input) {
            input.blur();
        }
    }

    function getSearchInput() {
        return document.querySelector('[data-md-component="search-query"]');
    }

    function getSearchMeta() {
        return document.querySelector(".md-search-result__meta");
    }

    function applyCustomSearchHint(meta) {
        if (!meta || meta.innerHTML === SEARCH_HINT_HTML) {
            return;
        }

        isApplyingHint = true;
        meta.innerHTML = SEARCH_HINT_HTML;
        meta.dataset.kapaHintActive = "true";
        isApplyingHint = false;
    }

    function syncSearchHint() {
        var input = getSearchInput();
        var meta = getSearchMeta();
        if (!input || !meta) {
            return;
        }

        if (input.value.trim() === "") {
            applyCustomSearchHint(meta);
            return;
        }

        if (meta.dataset.kapaHintActive === "true") {
            meta.dataset.kapaHintActive = "false";
        }
    }

    function bindSearchHintObserver(meta) {
        if (!meta || meta.dataset.kapaHintObserverBound === "true") {
            return;
        }

        var observer = new MutationObserver(function () {
            if (isApplyingHint) {
                return;
            }
            syncSearchHint();
        });
        observer.observe(meta, {
            childList: true,
            subtree: true,
            characterData: true,
        });

        meta.dataset.kapaHintObserverBound = "true";
    }

    function bindSearchInput(input) {
        if (!input || input.dataset.kapaAiBound === "true") {
            return;
        }

        var previousValue = input.value;
        input.addEventListener("input", function () {
            var currentValue = input.value;
            var shouldOpenAi = currentValue === "." && previousValue.trim() === "";

            if (shouldOpenAi) {
                input.value = "";
                previousValue = "";
                input.dispatchEvent(new Event("input", { bubbles: true }));
                closeMaterialSearch();
                openKapaAiForCurrentPage();
                return;
            }

            previousValue = currentValue;
            syncSearchHint();
        });

        input.addEventListener("focus", function () {
            previousValue = input.value;
            syncSearchHint();
        });

        input.dataset.kapaAiBound = "true";
    }

    function initSearchIntegration() {
        var input = getSearchInput();
        var meta = getSearchMeta();
        if (!input || !meta) {
            return;
        }

        bindSearchInput(input);
        bindSearchHintObserver(meta);
        syncSearchHint();
    }

    function initForCurrentPage() {
        ensureKapaPreinitialized();
        loadKapaScript();
        bindNonHomeModalCloseUnmount();
        bindAiTriggerClicks();
        initSearchIntegration();

        if (isHomePage()) {
            mountKapaWidget();
            return;
        }

        unmountKapaWidget();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initForCurrentPage);
    } else {
        initForCurrentPage();
    }

    if (typeof document$ !== "undefined" && typeof document$.subscribe === "function") {
        document$.subscribe(function () {
            initForCurrentPage();
        });
    }
})();