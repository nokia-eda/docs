// Re-initialize draw.io diagram embeds when they become visible inside Material tabs.
// GraphViewer.createViewerForElement is exposed by viewer-static.min.js and accepts the .mxgraph div.
// The script runs on each page render (document$.subscribe) and when tabs are switched.
// The [data-mxgraph-ready] guard prevents double-instantiating the same viewer.
(function () {
    const MAX_RETRIES = 50;
    const RETRY_INTERVAL = 200;
    const RETRY_ON_VISIBLE_ONLY = true;

    function initMxGraphs(scope) {
        if (!window.GraphViewer || typeof GraphViewer.createViewerForElement !== 'function') {
            return false;
        }

        (scope || document)
            .querySelectorAll('.mxgraph:not([data-mxgraph-ready])')
            .forEach((el) => {
                if (RETRY_ON_VISIBLE_ONLY && !isVisible(el)) {
                    return;
                }
                try {
                    GraphViewer.createViewerForElement(el);
                    el.setAttribute('data-mxgraph-ready', '1');
                } catch (err) {
                    console.warn('mxgraph init failed', err);
                }
            });

        return true;
    }

    function isVisible(el) {
        const rect = el.getBoundingClientRect();
        return (rect.width > 0 && rect.height > 0);
    }

    function retryInit(scope, remaining) {
        if (initMxGraphs(scope)) {
            return;
        }

        if (remaining <= 0) {
            return;
        }

        setTimeout(() => retryInit(scope, remaining - 1), RETRY_INTERVAL);
    }

    function findPanelForInput(input) {
        let node = input.nextElementSibling;
        while (node) {
            if (node.classList && node.classList.contains('tabbed-content')) {
                return node;
            }
            node = node.nextElementSibling;
        }
        return null;
    }

    function watchTabs(tabSet) {
        if (!tabSet || tabSet.dataset.mxgraphTabsReady) {
            return;
        }

        tabSet.dataset.mxgraphTabsReady = '1';

        const inputs = tabSet.querySelectorAll('input[type="radio"], .tabbed-labels > label');

        inputs.forEach((target) => {
            const handler = () => {
                let input = null;

                if (target.matches('input')) {
                    input = target;
                } else {
                    const forAttr = target.getAttribute('for');
                    if (forAttr) {
                        input = tabSet.querySelector(`#${CSS.escape(forAttr)}`);
                    }
                }

                if (!input) {
                    return;
                }

                const panel =
                    tabSet.querySelector(`[data-tabs-target="${input.id}"]`) ||
                    tabSet.querySelector(`#${CSS.escape(input.id)}-tab`) ||
                    findPanelForInput(input);

                requestAnimationFrame(() => retryInit(panel || tabSet, MAX_RETRIES));
            };

            if (target.matches('input')) {
                target.addEventListener('change', handler, { passive: true });
            } else {
                target.addEventListener('click', handler, { passive: true });
                target.addEventListener('keydown', (event) => {
                    if (event.key === 'Enter' || event.key === ' ') {
                        handler();
                    }
                });
            }
        });
    }

    function boot(scope) {
        const host = scope || document;
        retryInit(host, MAX_RETRIES);
        host.querySelectorAll('.tabbed-set').forEach(watchTabs);
    }

    function onRender() {
        boot();
    }

    if (window.document && window.document.subscribe) {
        document$.subscribe(onRender);
    } else {
        document.addEventListener('DOMContentLoaded', onRender);
    }
})();
