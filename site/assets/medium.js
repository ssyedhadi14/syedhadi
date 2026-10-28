/* Medium posts for syedcreates.com
   Static archive (medium-archive.js) renders instantly, then the live RSS feed
   is merged in so new Medium posts appear without a redeploy. */
(function(){
  var FEED_LOCAL='/medium-feed';
  var FEED_FALLBACK='https://api.rss2json.com/v1/api.json?rss_url='+encodeURIComponent('https://medium.com/feed/@ssyedhadi');
  var TRAVEL=/mecca|medina|najaf|karbala|majlis|iran|skydive/i;
  var CAREER=/scrum|remote workday|pm metrics|job offers|year of work|years of startup|learnt product marketing/i;
  var MONTHS=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

  var posts=(window.MEDIUM_ARCHIVE||[]).slice();

  function cat(t){return TRAVEL.test(t)?'Travel and Life':CAREER.test(t)?'Career':'Security and GTM'}
  function key(u){var m=String(u).split('?')[0].match(/-([0-9a-f]{8,})\/?$/);return m?m[1]:String(u).split('?')[0]}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function fmt(d){var p=d.split('-');return MONTHS[+p[1]-1]+' '+(+p[2])+', '+p[0]}
  function iso(d){var x=new Date(d);if(isNaN(x))return '';return x.toISOString().slice(0,10)}
  function imgUrl(i){if(!i)return '';return /^https?:/.test(i)?i:'https://miro.medium.com/v2/resize:fill:800:450/'+i}
  function imgFromHtml(h){var m=String(h||'').match(/<img[^>]+src="(https:\/\/(?:cdn-images-\d\.medium\.com|miro\.medium\.com)[^"]+)"/);if(!m)return '';var id=m[1].split('/').pop();return /stat\?event/.test(m[1])?'':id}

  function card(p){
    var cover=p.i?'<img src="'+esc(imgUrl(p.i))+'" alt="" loading="lazy" decoding="async" onerror="this.parentNode.classList.add(\'noimg\');this.remove()">':'';
    return '<a class="mpost reveal in" href="'+esc(p.u)+'" target="_blank" rel="noopener" data-cat="'+esc(p.c)+'">'+
      '<span class="mcover'+(p.i?'':' noimg')+'"><span class="mfall">'+esc(p.c)+'</span>'+cover+'</span>'+
      '<span class="mbody"><span class="mmeta"><span>'+esc(p.c)+'</span><span>'+fmt(p.d)+'</span></span>'+
      '<h3>'+esc(p.t)+'</h3><span class="read">Read on Medium &rarr;</span></span></a>';
  }

  function render(){
    document.querySelectorAll('[data-medium-latest]').forEach(function(el){
      var n=+el.getAttribute('data-medium-latest')||3;
      el.innerHTML=posts.slice(0,n).map(card).join('');
    });
    var blog=document.querySelector('[data-medium-blog]');
    if(blog){
      var active=blog.getAttribute('data-filter')||'All';
      var list=active==='All'?posts:posts.filter(function(p){return p.c===active});
      blog.innerHTML=list.map(card).join('');
      var count=document.getElementById('blogCount');
      if(count)count.textContent=list.length+' of '+posts.length+' posts';
      var bar=document.getElementById('blogFilters');
      if(bar&&!bar.childElementCount){
        ['All','Security and GTM','Career','Travel and Life'].forEach(function(c){
          var b=document.createElement('button');b.type='button';b.textContent=c;b.className='fchip'+(c===active?' on':'');
          b.addEventListener('click',function(){blog.setAttribute('data-filter',c);bar.querySelectorAll('.fchip').forEach(function(x){x.classList.toggle('on',x===b)});render()});
          bar.appendChild(b);
        });
      }
    }
  }

  function merge(items){
    var have={},added=0;
    posts.forEach(function(p){have[key(p.u)]=p});
    items.forEach(function(it){
      if(!it.t||!it.u||!it.d)return;
      var k=key(it.u),ex=have[k];
      if(ex){if(!ex.i&&it.i){ex.i=it.i;added++}return}
      it.c=cat(it.t);posts.push(it);have[k]=it;added++;
    });
    if(added){posts.sort(function(a,b){return a.d<b.d?1:a.d>b.d?-1:0});render()}
  }

  function fromXml(text){
    var doc=new DOMParser().parseFromString(text,'text/xml');
    if(doc.getElementsByTagName('parsererror').length)throw new Error('bad xml');
    return [].map.call(doc.getElementsByTagName('item'),function(n){
      function g(t){var e=n.getElementsByTagName(t)[0];return e?e.textContent:''}
      var enc=n.getElementsByTagNameNS('http://purl.org/rss/1.0/modules/content/','encoded')[0];
      return {t:g('title').trim(),u:g('link').split('?')[0],d:iso(g('pubDate')),i:imgFromHtml(enc?enc.textContent:'')};
    });
  }

  function fromJson(j){
    if(!j||j.status!=='ok')throw new Error('feed error');
    return j.items.map(function(x){
      var i=imgFromHtml(x.content||x.description)||(x.thumbnail&&!/stat\?event/.test(x.thumbnail)?x.thumbnail.split('/').pop():'');
      return {t:String(x.title||'').trim(),u:String(x.link||'').split('?')[0],d:iso(String(x.pubDate).replace(' ','T')+'Z'),i:i};
    });
  }

  render();
  if(!window.fetch||!window.DOMParser)return;
  fetch(FEED_LOCAL,{cache:'no-store'})
    .then(function(r){if(!r.ok)throw new Error(r.status);return r.text()})
    .then(function(t){merge(fromXml(t))})
    .catch(function(){
      return fetch(FEED_FALLBACK).then(function(r){if(!r.ok)throw new Error(r.status);return r.json()}).then(function(j){merge(fromJson(j))});
    })
    .catch(function(err){if(window.console)console.info('Medium live feed unavailable, showing archive',err)});
})();
