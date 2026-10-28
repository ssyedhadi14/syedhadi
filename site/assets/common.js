(function(){
  var root=document.documentElement, btn=document.getElementById('themeBtn');
  try{var saved=localStorage.getItem('theme'); if(saved) root.setAttribute('data-theme',saved);}catch(e){}
  if(btn) btn.addEventListener('click',function(){
    var cur=root.getAttribute('data-theme');
    var dark=cur? cur==='dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    var next=dark?'light':'dark'; root.setAttribute('data-theme',next);
    try{localStorage.setItem('theme',next);}catch(e){}
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
    b.addEventListener('click',function(e){e.stopPropagation();var d=b.parentElement,o=d.classList.toggle('open');b.setAttribute('aria-expanded',o);});
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
  var pmap={gtm:'portfolio',events:'portfolio',systems:'portfolio',recognition:'portfolio',playbook:'portfolio',tools:'tools'};
  if(pmap[page]){var g=document.querySelector('.dd-btn[data-group="'+pmap[page]+'"]'); if(g) g.classList.add('active');}
})();
