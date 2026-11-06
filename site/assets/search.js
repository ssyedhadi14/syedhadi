/* syedcreates.com global search. Index: /assets/search-index.json */
(function(){
  'use strict';
  var VER='20261106b', IDX=null, loading=null, ov, inp, res, items=[], sel=0, lastFocus=null, timer;
  var isMac=/Mac|iPhone|iPad/.test(navigator.platform||navigator.userAgent);
  var SYN={emi:['loan','home loan','car loan','prepayment'],loan:['emi'],khums:['qums','khumus','khoms'],qums:['khums'],khumus:['khums'],
    mileage:['fuel','petrol','car','kmpl'],fuel:['mileage','petrol'],petrol:['fuel','mileage'],sip:['mutual fund','returns'],mf:['mutual fund'],
    retire:['fire','retirement'],retirement:['fire'],fire:['retire','early retirement'],weight:['bmi'],bmi:['weight','health'],
    salary:['ctc','hike','pay'],ctc:['salary'],hike:['salary'],aeo:['ai visibility','answer engine','seo'],geo:['ai visibility','aeo'],
    seo:['aeo','score','audit'],chatgpt:['ai visibility','aeo'],gtm:['go to market','growth'],pmm:['product marketing'],
    partner:['channel','partnership','alliances'],channel:['partner'],research:['company research','competitors'],competitors:['company research'],
    meeting:['schedule meeting','book a call','contact'],contact:['schedule meeting'],hire:['schedule meeting','services'],calculator:['calculators','calc'],calc:['calculator']};
  var ICON={'Calculators':'<path d="M7 3h10a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M8 7h8M8 12h2M14 12h2M8 16h2M14 16h2"/>',
    'Free tools':'<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18v3h3l6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
    'Growth in a box':'<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
    'Work':'<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
    'Articles':'<path d="M4 4h12l4 4v12H4z"/><path d="M8 10h8M8 14h8M8 18h5"/>',
    'Section':'<path d="M4 9h16M4 15h16M10 3 8 21M16 3l-2 18"/>',
    'Pages':'<path d="M3 11 12 3l9 8v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    'Recent':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'};
  ICON['Writing and guides']=ICON['Articles'];
  var ORDER=['Calculators','Free tools','Growth in a box','Work','Pages','Writing and guides','Section','Articles'];

  function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
  function norm(s){return String(s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9\u0900-\u097f\u0600-\u06ff]+/g,' ').trim();}
  function store(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k)||'null');localStorage.setItem(k,JSON.stringify(v));}catch(e){return null;}}
  function track(a,q){try{if(window.shTrack)window.shTrack(a,{label:q});}catch(e){}}

  function load(){
    if(IDX)return Promise.resolve(IDX); if(loading)return loading;
    loading=fetch('/assets/search-index.json?v='+VER).then(function(r){if(!r.ok)throw new Error(r.status);return r.json();}).then(function(d){
      IDX=d.pages.map(function(p){p._t=norm(p.t+' '+p.s);p._h=norm(p.h.map(function(x){return x[0];}).join(' '));p._k=norm(p.k+' '+p.c);p._d=norm(p.d);p._b=p.b||'';p._tw=p._t.split(' ');p._all=(p._t+' '+p._h+' '+p._k+' '+p._d+' '+p._b).split(' ');return p;});
      IDX.popular=d.popular||[]; return IDX;
    }).catch(function(e){loading=null;throw e;});
    return loading;
  }

  function lev(a,b,max){
    if(Math.abs(a.length-b.length)>max)return max+1;
    var prev=[],i,j; for(j=0;j<=b.length;j++)prev[j]=j;
    for(i=1;i<=a.length;i++){var cur=[i],best=i;for(j=1;j<=b.length;j++){cur[j]=Math.min(prev[j]+1,cur[j-1]+1,prev[j-1]+(a[i-1]===b[j-1]?0:1));if(cur[j]<best)best=cur[j];}if(best>max)return max+1;prev=cur;}
    return prev[b.length];
  }
  function tokScore(tok,words,str,strict){
    if(!str)return 0;
    if((' '+str+' ').indexOf(' '+tok+' ')>-1)return 1;
    var i,w,best=0;
    for(i=0;i<words.length;i++){w=words[i];if(!w)continue;
      if(w.indexOf(tok)===0){best=Math.max(best,tok.length>=3?.85:.6);}
      else if(strict){continue;}
      else if(tok.length>=4&&w.indexOf(tok)>0){best=Math.max(best,.5);}
      else if(tok.length>=4&&w.length>=4&&best<.45){var m=tok.length>=7?2:1;if(lev(tok,w,m)<=m)best=.45;}
    }
    return best;
  }
  function search(q){
    var nq=norm(q); if(!nq)return [];
    var toks=nq.split(' ').filter(function(t){return t.length>1||/\d/.test(t);}); if(!toks.length)toks=[nq];
    var phrase=nq.length>3?nq:null, out=[];
    IDX.forEach(function(p){
      var total=0,hits=0;
      toks.forEach(function(t){
        var alts=[t].concat(SYN[t]||[]),best=0;
        alts.forEach(function(a,ai){
          var damp=ai?.7:1, parts=norm(a).split(' '), s=0;
          parts.forEach(function(pt){
            var f=Math.max(tokScore(pt,p._tw,p._t)*10,tokScore(pt,p._h.split(' '),p._h)*5,tokScore(pt,p._k.split(' '),p._k)*4,tokScore(pt,p._d.split(' '),p._d,1)*3,tokScore(pt,p._b.split(' '),p._b,1)*1.2);
            s+=f/parts.length;
          });
          best=Math.max(best,s*damp);
        });
        if(best>0)hits++; total+=best;
      });
      if(!hits)return;
      var cover=hits/toks.length; total*=cover*cover;
      if(phrase&&p._t.indexOf(phrase)>-1)total+=8; else if(phrase&&(p._d.indexOf(phrase)>-1||p._h.indexOf(phrase)>-1))total+=3;
      if(p.c==='Calculators'||p.c==='Free tools')total*=1.15; if(p.x)total*=.85; if(p.u==='/calculator'||p.u==='/tools'||p.u==='/')total*=.72;
      if(total>1.2)out.push({p:p,s:total,full:hits===toks.length});
      if(p.h&&p.h.length&&hits){
        p.h.forEach(function(h){var hn=norm(h[0]),hs=0,hh=0;toks.forEach(function(t){var v=tokScore(t,hn.split(' '),hn);if(!v)(SYN[t]||[]).forEach(function(a){v=Math.max(v,tokScore(norm(a),hn.split(' '),hn)*.7);});if(v)hh++;hs+=v;});
          if(hh===toks.length&&hs>=toks.length*.8)out.push({p:{u:p.u+'#'+h[1],t:h[0],d:'Section in '+p.t,c:'Section'},s:hs*6*(p.c==='Calculators'?1.1:1),full:true});});
      }
    });
    var full=out.filter(function(r){return r.full;}); if(full.length)out=full.concat(out.filter(function(r){return !r.full&&r.s>6;}));
    out.sort(function(a,b){return b.s-a.s;});
    var seen={},res=[]; out.forEach(function(r){if(!seen[r.p.u]&&res.length<14){seen[r.p.u]=1;res.push(r.p);}});
    return res;
  }
  function hl(text,q){
    var t=esc(text),toks=norm(q).split(' ').filter(function(x){return x.length>1;}).sort(function(a,b){return b.length-a.length;});
    if(!toks.length)return t;
    try{return t.replace(new RegExp('('+toks.map(function(x){return x.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}).join('|')+')','gi'),'<mark>$1</mark>');}catch(e){return t;}
  }
  function row(p,q,cat){
    var ext=/^https?:/.test(p.u);
    return '<a class="srch-it" role="option" href="'+esc(p.u)+'"'+(ext?' target="_blank" rel="noopener"':'')+' data-u="'+esc(p.u)+'"><span class="srch-ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'+(ICON[cat||p.c]||ICON.Pages)+'</svg></span><span class="srch-tx"><b>'+hl(p.t,q)+'</b><small>'+hl(p.d||p.s||'',q)+'</small></span><span class="srch-go" aria-hidden="true">'+(ext?'&#8599;':'&#8629;')+'</span></a>';
  }
  function render(q){
    var html='';
    if(!IDX){res.innerHTML='<div class="srch-empty">Loading search&hellip;</div>';return;}
    if(!q.trim()){
      var rec=(store('sh_recent')||[]).slice(0,4);
      if(rec.length){html+='<div class="srch-g">Recent searches</div>';rec.forEach(function(r){html+='<a class="srch-it" role="option" href="#" data-q="'+esc(r)+'"><span class="srch-ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">'+ICON.Recent+'</svg></span><span class="srch-tx"><b>'+esc(r)+'</b></span><span class="srch-go" aria-hidden="true">&#8629;</span></a>';});}
      html+='<div class="srch-g">Popular</div>';
      IDX.popular.forEach(function(u){var p=IDX.filter(function(x){return x.u===u;})[0];if(p)html+=row(p,'');});
    } else {
      var r=search(q);
      if(!r.length){
        html='<div class="srch-empty">No results for <b>'+esc(q)+'</b>. Try a broader word, or one of these.<div class="srch-chips">'+['EMI','SIP returns','Company research','SEO score','Salary','Khums'].map(function(c){return '<button type="button" data-q="'+c+'">'+c+'</button>';}).join('')+'</div></div>';
        track('search_empty',q);
      } else {
        var groups={}; r.forEach(function(p){(groups[p.c]=groups[p.c]||[]).push(p);});
        var first=r[0].c; var order=[first].concat(ORDER.filter(function(c){return c!==first;}));
        order.forEach(function(c){if(groups[c]){html+='<div class="srch-g">'+(c==='Section'?'Jump to section':esc(c))+'</div>';groups[c].forEach(function(p){html+=row(p,q);});}});
      }
    }
    res.innerHTML=html;
    items=[].slice.call(res.querySelectorAll('.srch-it')); sel=0; mark();
  }
  function mark(){items.forEach(function(el,i){el.classList.toggle('sel',i===sel);el.setAttribute('aria-selected',i===sel?'true':'false');el.id='srch-o'+i;});
    if(items[sel]){inp.setAttribute('aria-activedescendant','srch-o'+sel);items[sel].scrollIntoView({block:'nearest'});}else inp.removeAttribute('aria-activedescendant');}
  function remember(q){q=q.trim();if(q.length<2)return;var r=(store('sh_recent')||[]).filter(function(x){return x.toLowerCase()!==q.toLowerCase();});r.unshift(q);store('sh_recent',r.slice(0,6));}
  function go(el){
    if(!el)return; var dq=el.getAttribute('data-q'); if(dq){inp.value=dq;render(dq);inp.focus();return;}
    var q=inp.value; remember(q); track('search_select',q+' > '+el.getAttribute('data-u'));
    var u=el.getAttribute('data-u'); if(/^https?:/.test(u)){window.open(u,'_blank','noopener');close();return;}
    var same=u.split('#')[0]===location.pathname.replace(/\.html$/,'')||(u.split('#')[0]==='/'&&location.pathname==='/');
    close(); if(same&&u.indexOf('#')>-1){location.hash=u.split('#')[1];var t=document.getElementById(u.split('#')[1]);if(t)t.scrollIntoView({behavior:'smooth',block:'start'});} else location.href=u;
  }
  function build(){
    ov=document.createElement('div'); ov.className='srch-ov'; ov.hidden=true;
    ov.innerHTML='<div class="srch-dlg" role="dialog" aria-modal="true" aria-label="Search syedcreates.com"><div class="srch-top"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input class="srch-in" type="search" placeholder="Search calculators, tools, case studies, articles" autocomplete="off" autocorrect="off" spellcheck="false" enterkeyhint="go" role="combobox" aria-expanded="true" aria-controls="srch-list" aria-autocomplete="list"><button class="srch-x" type="button" aria-label="Close search">Esc</button></div><div class="srch-res" id="srch-list" role="listbox" aria-label="Search results"></div><div class="srch-ft"><span><kbd>&uarr;</kbd><kbd>&darr;</kbd>to move</span><span><kbd>Enter</kbd>to open</span><span><kbd>Esc</kbd>to close</span><span>'+(isMac?'&#8984;':'Ctrl')+' K anywhere</span></div></div>';
    document.body.appendChild(ov);
    inp=ov.querySelector('.srch-in'); res=ov.querySelector('.srch-res');
    inp.addEventListener('input',function(){clearTimeout(timer);var v=inp.value;timer=setTimeout(function(){render(v);},60);});
    inp.addEventListener('keydown',function(e){
      if(e.key==='ArrowDown'){e.preventDefault();if(items.length){sel=(sel+1)%items.length;mark();}}
      else if(e.key==='ArrowUp'){e.preventDefault();if(items.length){sel=(sel-1+items.length)%items.length;mark();}}
      else if(e.key==='Enter'){e.preventDefault();go(items[sel]);}
      else if(e.key==='Escape'){e.preventDefault();if(inp.value){inp.value='';render('');}else close();}
      else if(e.key==='Tab'){e.preventDefault();}
    });
    ov.addEventListener('mousedown',function(e){if(e.target===ov)close();});
    ov.querySelector('.srch-x').addEventListener('click',close);
    res.addEventListener('click',function(e){var b=e.target.closest('[data-q]');var a=e.target.closest('.srch-it');if(b&&!a){e.preventDefault();inp.value=b.getAttribute('data-q');render(inp.value);inp.focus();return;}if(a&&!(e.metaKey||e.ctrlKey||e.shiftKey)){e.preventDefault();go(a);}});
    res.addEventListener('mousemove',function(e){var a=e.target.closest('.srch-it');if(a){var i=items.indexOf(a);if(i>-1&&i!==sel){sel=i;mark();}}});
  }
  function open(q){
    if(!ov)build(); if(!ov.hidden&&q==null){inp.focus();return;}
    lastFocus=document.activeElement; ov.hidden=false; document.documentElement.classList.add('srch-lock');
    requestAnimationFrame(function(){ov.classList.add('on');});
    inp.value=q||''; inp.focus(); render(inp.value);
    load().then(function(){render(inp.value);}).catch(function(){res.innerHTML='<div class="srch-empty">Search could not load. Check your connection and try again.</div>';});
    track('search_open',q||'');
  }
  function close(){
    if(!ov||ov.hidden)return; ov.classList.remove('on'); document.documentElement.classList.remove('srch-lock');
    setTimeout(function(){ov.hidden=true;},160); if(lastFocus&&lastFocus.focus)try{lastFocus.focus();}catch(e){}
  }
  function typing(el){return el&&(el.isContentEditable||/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName));}
  document.addEventListener('keydown',function(e){
    if((e.key==='k'||e.key==='K')&&(e.metaKey||e.ctrlKey)&&!e.altKey){e.preventDefault();ov&&!ov.hidden?close():open();}
    else if(e.key==='/'&&!typing(e.target)&&!e.metaKey&&!e.ctrlKey&&(!ov||ov.hidden)){e.preventDefault();open();}
  });
  function init(){
    var b=document.getElementById('srchBtn');
    if(b){var k=b.querySelector('.srch-k');if(k&&isMac)k.textContent='\u2318K';
      b.addEventListener('click',function(){open();});
      ['pointerenter','focus','touchstart'].forEach(function(ev){b.addEventListener(ev,function(){load().catch(function(){});},{once:true,passive:true});});}
    var m=location.search.match(/[?&](?:q|search)=([^&]+)/);
    if(m){try{open(decodeURIComponent(m[1].replace(/\+/g,' ')));}catch(e){}}
  }
  window.siteSearch={open:open,close:close};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
