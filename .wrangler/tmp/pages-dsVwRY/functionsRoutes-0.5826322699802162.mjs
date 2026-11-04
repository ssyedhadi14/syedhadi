import { onRequest as __api_company_research_js_onRequest } from "/home/claude/syedhadi/functions/api/company-research.js"
import { onRequest as __api_salary_report_js_onRequest } from "/home/claude/syedhadi/functions/api/salary-report.js"
import { onRequest as __api_seo_aeo_score_js_onRequest } from "/home/claude/syedhadi/functions/api/seo-aeo-score.js"
import { onRequest as __medium_feed_js_onRequest } from "/home/claude/syedhadi/functions/medium-feed.js"
import { onRequest as ___middleware_js_onRequest } from "/home/claude/syedhadi/functions/_middleware.js"

export const routes = [
    {
      routePath: "/api/company-research",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_company_research_js_onRequest],
    },
  {
      routePath: "/api/salary-report",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_salary_report_js_onRequest],
    },
  {
      routePath: "/api/seo-aeo-score",
      mountPath: "/api",
      method: "",
      middlewares: [],
      modules: [__api_seo_aeo_score_js_onRequest],
    },
  {
      routePath: "/medium-feed",
      mountPath: "/",
      method: "",
      middlewares: [],
      modules: [__medium_feed_js_onRequest],
    },
  {
      routePath: "/",
      mountPath: "/",
      method: "",
      middlewares: [___middleware_js_onRequest],
      modules: [],
    },
  ]