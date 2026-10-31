(function(){
  var root=document.documentElement, btn=document.getElementById('themeBtn');
  try{var saved=localStorage.getItem('sh_theme'); root.setAttribute('data-theme',saved==='dark'?'dark':'light');}catch(e){root.setAttribute('data-theme','light')}
  function sync(){if(btn)btn.setAttribute('aria-checked',root.getAttribute('data-theme')==='dark'?'true':'false')}
  sync();
  if(btn) btn.addEventListener('click',function(){
    var next=root.getAttribute('data-theme')==='dark'?'light':'dark'; root.setAttribute('data-theme',next); sync();
    try{localStorage.setItem('sh_theme',next);}catch(e){}
  });
  var els=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.1});
    els.forEach(function(el){io.observe(el)});
  } else els.forEach(function(el){el.classList.add('in')});
  var y=document.getElementById('yr'); if(y) y.textContent=new Date().getFullYear();
  var page=document.body.getAttribute('data-page');
  document.querySelectorAll('.nav-links a, .dd-menu a').forEach(function(a){ if(a.getAttribute('data-p')===page) a.classList.add('active'); });

  // dropdown + mobile menu
  var mb=document.getElementById('menuBtn'), nl=document.getElementById('navLinks');
  if(mb&&nl) mb.addEventListener('click',function(){var o=nl.classList.toggle('open');mb.setAttribute('aria-expanded',o);});
  document.querySelectorAll('.dd-btn').forEach(function(b){
    b.addEventListener('click',function(e){e.stopPropagation();var d=b.parentElement;document.querySelectorAll('.dd.open').forEach(function(x){if(x!==d){x.classList.remove('open');var xb=x.querySelector('.dd-btn');if(xb)xb.setAttribute('aria-expanded','false');}});var o=d.classList.toggle('open');b.setAttribute('aria-expanded',o);});
  });
  document.addEventListener('click',function(e){document.querySelectorAll('.dd.open').forEach(function(d){if(!d.contains(e.target)){d.classList.remove('open');d.querySelector('.dd-btn').setAttribute('aria-expanded','false');}});});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){document.querySelectorAll('.dd.open').forEach(function(d){d.classList.remove('open')});if(nl)nl.classList.remove('open');}});
  

  // work mega: hover a service to swap the detail panel
  document.querySelectorAll('.mw-item').forEach(function(it){
    it.addEventListener('mouseenter',function(){
      var k=it.dataset.k, root=it.closest('.mm-work');
      root.querySelectorAll('.mw-item').forEach(function(x){x.classList.toggle('on',x===it)});
      root.querySelectorAll('.mw-panel').forEach(function(p){p.classList.toggle('on',p.dataset.k===k)});
    });
  });
  // portfolio group active state
  var pmap={gtm:'portfolio',events:'portfolio',systems:'portfolio',recognition:'portfolio',playbook:'portfolio',tools:'tools',about:'tools',blog:'tools',posts:'tools',jobs:'tools',skillpack:'tools',salary:'calc',salarycalc:'calc',fire:'calc',mf:'calc',khums:'calc',tool_ai:'calc',tool_gtm:'calc',tool_partner:'calc',cases:'portfolio',gtmbox:'growth',pmmbox:'growth',seobox:'growth',contentbox:'growth',growthbox:'growth',partnerbox:'growth'};
  if(pmap[page]){var g=document.querySelector('.dd-btn[data-group="'+pmap[page]+'"]'); if(g) g.classList.add('active');}

  // scroll progress bar
  var bar=document.createElement('div'); bar.className='scroll-bar'; document.body.appendChild(bar);
  var ticking=false;
  function prog(){var h=document.documentElement; var max=h.scrollHeight-h.clientHeight; bar.style.transform='scaleX('+(max>0?h.scrollTop/max:0)+')'; ticking=false;}
  window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(prog);}},{passive:true}); prog();
})();

/* ===== Lead event tracking =====
   Set GA4_ID to your Google Analytics 4 measurement ID (G-XXXXXXX) to send events to GA4.
   Until then every event is still pushed to window.dataLayer, ready for Google Tag Manager. */
(function(){
  var GA4_ID = '';
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function(){ dataLayer.push(arguments); };
  if (GA4_ID) {
    var s = document.createElement('script'); s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID; document.head.appendChild(s);
    gtag('js', new Date()); gtag('config', GA4_ID);
  }
  window.shTrack = function(name, params){
    params = params || {}; params.page = location.pathname;
    try { gtag('event', name, params); } catch (e) {}
    try { if (window.plausible) plausible(name, { props: params }); } catch (e) {}
  };
  var rules = [
    ['a[href*="schedule-meeting"]', 'schedule_click'], ['a[href*="wa.me"]', 'whatsapp_click'],
    ['a[href^="mailto:"]', 'email_click'], ['a[href*="buy.polar.sh"]', 'skill_pack_checkout'],
    ['.jb-apply', 'job_apply_click'], ['a[href*="linkedin.com/in/"]', 'linkedin_click']
  ];
  document.addEventListener('click', function(ev){
    var a = ev.target.closest && ev.target.closest('a');
    if (!a) return;
    for (var i = 0; i < rules.length; i++) { if (a.matches(rules[i][0])) { shTrack(rules[i][1], { label: (a.textContent || '').trim().slice(0, 60) }); break; } }
  }, true);
  var forms = [['.op-gate', 'one_pager_request'], ['.au-form', 'audit_request'], ['#gateForm', 'salary_guide_request'], ['.nl-form', 'newsletter_signup']];
  document.addEventListener('submit', function(ev){
    for (var i = 0; i < forms.length; i++) { if (ev.target.matches(forms[i][0])) { shTrack(forms[i][1]); break; } }
  }, true);
  window.addEventListener('message', function(ev){
    if (ev.origin.indexOf('calendly.com') > -1 && ev.data && ev.data.event === 'calendly.event_scheduled') shTrack('meeting_booked');
  });
})();

/* Keep the page chrome clean: remove third party badges injected after our markup. */
(function(){
  function sweep(){
    var f=document.getElementById('nl-badge-frame'); if(f&&f.parentNode) f.parentNode.removeChild(f);
    var s=document.querySelectorAll('script[src*="/.netlify/scripts/hud"]'); for(var i=0;i<s.length;i++){ if(s[i].parentNode) s[i].parentNode.removeChild(s[i]); }
  }
  sweep();
  if(window.MutationObserver){ new MutationObserver(sweep).observe(document.documentElement,{childList:true,subtree:true}); }
  document.addEventListener('DOMContentLoaded',sweep); window.addEventListener('load',sweep);
})();
