// Created by: Claude
// Date: 2026-11-03
// Purpose: /medium-feed proxy to the Medium RSS feed (Netlify did this with a 200 rewrite), cached at the edge 30 min
// Owner: Syed Hadi
const FEED = 'https://medium.com/feed/@ssyedhadi';

export async function onRequest() {
  try {
    const r = await fetch(FEED, { headers: { 'User-Agent': 'syedcreates.com feed reader', Accept: 'application/rss+xml,application/xml,text/xml' }, cf: { cacheTtl: 1800, cacheEverything: true } });
    return new Response(await r.text(), { status: r.status, headers: { 'Content-Type': 'application/xml; charset=utf-8', 'Cache-Control': 'public, max-age=1800' } });
  } catch (e) {
    return new Response('<?xml version="1.0"?><rss version="2.0"><channel></channel></rss>', { status: 502, headers: { 'Content-Type': 'application/xml' } });
  }
}
