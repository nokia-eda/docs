// Restore draw.io diagram embeds after they become visible inside Material tabs.
// GraphViewer.createViewerForElement is exposed by viewer-static.min.js and accepts the .mxgraph div.
// viewer-static.min.js renders ordinary diagrams automatically; this script only handles tab switches.
(function () {
    const MAX_RETRIES = 50;
    const RETRY_INTERVAL = 200;
    const RETRY_ON_VISIBLE_ONLY = true;

    function restoreMxGraph(el) {
        const viewer = el.__mxgraphViewer;
        if (!viewer || !viewer.graph || !viewer.graph.view) {
            return false;
        }

        const config = JSON.parse(el.getAttribute('data-mxgraph') || '{}');
        const zoom = Number(config.zoom);
        viewer.graph.view.setScale(Number.isFinite(zoom) && zoom > 0 ? zoom : 1);
        if (typeof viewer.positionGraph === 'function') {
            viewer.positionGraph();
        }
        return true;
    }

    function resetMxGraphElement(el) {
        if (typeof ResizeSensor !== 'undefined' && typeof ResizeSensor.detach === 'function') {
            ResizeSensor.detach(el);
        }
        if (window.mxEvent && typeof mxEvent.release === 'function') {
            mxEvent.release(el);
        }

        el.replaceChildren();
        [
            'width',
            'height',
            'min-width',
            'overflow',
            'position',
            'touch-action',
            'color-scheme',
            'cursor',
        ].forEach((property) => el.style.removeProperty(property));
    }

    function initMxGraphs(scope) {
        if (!window.GraphViewer || typeof GraphViewer.createViewerForElement !== 'function') {
            return false;
        }

        (scope || document)
            .querySelectorAll('.mxgraph')
            .forEach((el) => {
                if (RETRY_ON_VISIBLE_ONLY && !isVisible(el)) {
                    return;
                }

                if (restoreMxGraph(el) || el.hasAttribute('data-mxgraph-initializing')) {
                    return;
                }

                try {
                    resetMxGraphElement(el);
                    el.setAttribute('data-mxgraph-initializing', '1');
                    GraphViewer.createViewerForElement(el, (viewer) => {
                        el.__mxgraphViewer = viewer;
                        el.removeAttribute('data-mxgraph-initializing');
                        el.setAttribute('data-mxgraph-ready', '1');
                    });
                } catch (err) {
                    el.removeAttribute('data-mxgraph-initializing');
                    el.removeAttribute('data-mxgraph-ready');
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
        host.querySelectorAll('.tabbed-set').forEach(watchTabs);
    }

    function onRender() {
        boot();
    }

    if (typeof document$ !== 'undefined') {
        document$.subscribe(onRender);
    } else {
        document.addEventListener('DOMContentLoaded', onRender);
    }
})();
