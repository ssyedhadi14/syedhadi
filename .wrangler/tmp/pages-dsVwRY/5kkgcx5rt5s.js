// <define:__ROUTES__>
var define_ROUTES_default = {
  version: 1,
  include: [
    "/api/*",
    "/medium-feed",
    "/blog",
    "/blog.html",
    "/sitemap.xml",
    "/llms.txt",
    "/llms-full.txt",
    "/assets/search-index.json",
    "/gtm-plays-behind-0-to-10m",
    "/gtm-plays-behind-0-to-10m.html",
    "/ai-search-cnapp-240-percent",
    "/ai-search-cnapp-240-percent.html",
    "/fire-math-epf-ppf-nps",
    "/fire-math-epf-ppf-nps.html",
    "/one-line-positioning-test",
    "/one-line-positioning-test.html",
    "/partner-programs-that-ship-pipeline",
    "/partner-programs-that-ship-pipeline.html",
    "/2m-pipeline-100k-budget",
    "/2m-pipeline-100k-budget.html",
    "/23-content-types-5-that-sold",
    "/23-content-types-5-that-sold.html",
    "/salary-in-2046",
    "/salary-in-2046.html",
    "/gtm-lessons-from-leaders-2026",
    "/gtm-lessons-from-leaders-2026.html",
    "/0-to-10m-10-lessons",
    "/0-to-10m-10-lessons.html"
  ],
  exclude: []
};

// ../wr/node_modules/wrangler/templates/pages-dev-pipeline.ts
import worker from "/home/claude/syedhadi/.wrangler/tmp/pages-dsVwRY/functionsWorker-0.35681186779068463.mjs";
import { isRoutingRuleMatch } from "/home/claude/wr/node_modules/wrangler/templates/pages-dev-util.ts";
export * from "/home/claude/syedhadi/.wrangler/tmp/pages-dsVwRY/functionsWorker-0.35681186779068463.mjs";
var routes = define_ROUTES_default;
var pages_dev_pipeline_default = {
  fetch(request, env, context) {
    const { pathname } = new URL(request.url);
    for (const exclude of routes.exclude) {
      if (isRoutingRuleMatch(pathname, exclude)) {
        return env.ASSETS.fetch(request);
      }
    }
    for (const include of routes.include) {
      if (isRoutingRuleMatch(pathname, include)) {
        const workerAsHandler = worker;
        if (workerAsHandler.fetch === void 0) {
          throw new TypeError("Entry point missing `fetch` handler");
        }
        return workerAsHandler.fetch(request, env, context);
      }
    }
    return env.ASSETS.fetch(request);
  }
};
export {
  pages_dev_pipeline_default as default
};
//# sourceMappingURL=5kkgcx5rt5s.js.map
