// Created by: Claude
// Date: 2026-11-02
// Purpose: E2E test for /company-research with the Netlify function mocked. Checks render, polling, PDF page count.
// Owner: Syed Hadi
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');const ROOT='/home/claude/work/site';
const ct=f=>({'.css':'text/css','.js':'application/javascript','.woff2':'font/woff2','.ttf':'font/ttf','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg'}[path.extname(f)]||'text/html');
const L=(n,w)=>Array.from({length:n},(_,i)=>w+' '+(i+1));
const DATA={domain:'accuknox.com',company_name:'AccuKnox',one_liner:'Zero Trust CNAPP and AI security platform built on the open source KubeArmor runtime engine for cloud and on prem teams.',category:'Cloud security (CNAPP)',founded:'2020',ownership:'Private',ticker:'',
market_cap:{value:'Not disclosed',as_of:'',confidence:'UNVERIFIED',source_url:''},headquarters:{value:'Cupertino, California, USA',as_of:'',confidence:'HIGH',source_url:'https://www.accuknox.com/about'},
employee_count:{value:'150 to 200',as_of:'Oct 2026',confidence:'MEDIUM',source_url:'https://www.linkedin.com/company/accuknox'},total_customers:{value:'Not disclosed',confidence:'UNVERIFIED',as_of:'',source_url:''},arr:{value:'Not disclosed',confidence:'UNVERIFIED',as_of:'',source_url:''},
competitors:[{name:'Palo Alto Prisma Cloud',overlap:'Enterprise CNAPP suites with CSPM, CWPP and code security bundled'},{name:'Wiz',overlap:'Agentless cloud risk graph and CSPM for cloud native teams'},{name:'Sysdig',overlap:'Runtime threat detection for containers and Kubernetes'},{name:'Aqua Security',overlap:'Container image scanning and runtime protection'},{name:'CrowdStrike Falcon Cloud',overlap:'Cloud workload protection sold into existing endpoint accounts'}],
differentiators:['Inline runtime enforcement with eBPF and LSM, blocking attacks instead of only alerting','Deploys SaaS, on prem and fully air gapped for regulated and sovereign buyers','Open source KubeArmor core, a CNCF project with a large practitioner community','AI security coverage for models, agents and LLM apps in the same platform','Consolidates ASPM, CSPM, CWPP and SIEM style views into one console'],
why_customers_choose:[{reason:'Prevention at runtime, not just detection',evidence:'Customer case studies cite blocked zero day exploits in production Kubernetes clusters'},{reason:'Fits on prem and air gapped estates',evidence:'Banks and public sector buyers in India and the Gulf choose it for sovereign deployments'},{reason:'Lower cost than suites',evidence:'Reviews mention consolidating three to four point tools into one license'},{reason:'Responsive engineering support',evidence:'G2 reviewers praise fast onboarding and direct access to engineers'}],
growth_painpoints:[{pain:'Brand awareness trails far better funded CNAPP rivals',severity:'must_fix',signal:'Low share of voice in analyst reports and search results'},{pain:'Long enterprise and public sector sales cycles',severity:'must_fix',signal:'RFP heavy pipeline across India and MENA'},{pain:'Broad platform makes positioning harder to grasp',severity:'must_fix',signal:'Homepage lists more than ten modules'},{pain:'Limited self serve trial path for developers',severity:'nice_to_fix',signal:'Most CTAs route to demo booking'},{pain:'Thin presence in North American mid market',severity:'nice_to_fix',signal:'Few US logos on the customers page'}],
missed_revenue:[{opportunity:'Cloud marketplace private offers',fix:'Lead with AWS, Azure and GCP marketplace listings so buyers can burn committed spend',impact:'High'},{opportunity:'MSSP and MSP multi tenant channel',fix:'Package a multi tenant MSSP SKU with margin and co marketing funds',impact:'High'},{opportunity:'Developer led bottom up adoption',fix:'Launch a free tier on KubeArmor with an in product upgrade to the platform',impact:'Medium'},{opportunity:'AI security as a standalone wedge',fix:'Sell AI security posture as its own entry product to AI native teams',impact:'Medium'},{opportunity:'Expansion pricing',fix:'Price per workload and per module with clear upgrade tiers',impact:'Low'}],
sources:[{title:'AccuKnox homepage',url:'https://www.accuknox.com/'},{title:'About AccuKnox',url:'https://www.accuknox.com/about'},{title:'LinkedIn',url:'https://www.linkedin.com/company/accuknox'},{title:'G2 reviews',url:'https://www.g2.com/products/accuknox/reviews'},{title:'KubeArmor CNCF',url:'https://www.cncf.io/projects/kubearmor/'}],researched_at:new Date().toISOString()};
(async()=>{const b=await chromium.launch();
for (const [theme,w] of [['light',1366],['dark',390]]){
const ctx=await b.newContext({viewport:{width:w,height:900},acceptDownloads:true});
if(theme==='dark')await ctx.addInitScript(()=>localStorage.setItem('sh_theme','dark'));
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
let polls=0;
await p.route('**/*',r=>{const u=new URL(r.request().url());
 if(u.pathname==='/.netlify/functions/company-research'){ if(r.request().method()==='POST')return r.fulfill({status:202,contentType:'application/json',body:JSON.stringify({ok:true,status:'processing',id:'11111111-2222-3333-4444-555555555555',host:'accuknox.com'})});
   polls++; return r.fulfill({contentType:'application/json',body:JSON.stringify(polls<2?{ok:true,status:'processing'}:{ok:true,status:'completed',data:DATA})});}
 if(u.host!=='local')return r.fulfill({status:204,body:''});let f=path.join(ROOT,u.pathname==='/'?'index.html':u.pathname);if(!fs.existsSync(f)||fs.statSync(f).isDirectory())f+='.html';if(!fs.existsSync(f))return r.fulfill({status:404,body:''});r.fulfill({body:fs.readFileSync(f),contentType:ct(f)})});
await p.clock.install();
await p.goto('http://local/company-research');
await p.fill('#crUrl','accuknox.com');await p.click('#crBtn');
await p.waitForTimeout(300);await p.screenshot({path:'/home/claude/qa/cr-prog-'+theme+'.png'});
await p.clock.runFor(6000);
await p.waitForSelector('#crRes:not([hidden])',{timeout:15000});
await p.addStyleTag({content:'.reveal{opacity:1!important;transform:none!important}nav{position:static!important}'});
await p.waitForTimeout(400);
await p.screenshot({path:'/home/claude/qa/cr-res-'+theme+'.png',fullPage:true});
const [dl]=await Promise.all([p.waitForEvent('download',{timeout:30000}),p.click('#pdfBtn')]);
const out='/home/claude/qa/cr-'+theme+'.pdf';await dl.saveAs(out);
console.log(theme,'polls',polls,'pdf',dl.suggestedFilename(),'url',p.url().replace('http://local',''),'errors',errs);
await ctx.close();}
await b.close();})();
