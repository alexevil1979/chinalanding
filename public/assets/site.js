document.addEventListener('DOMContentLoaded',function(){
  var b=document.querySelector('.menu-toggle'),n=document.querySelector('.main-nav');
  if(b&&n)b.addEventListener('click',function(){
    var open=b.getAttribute('aria-expanded')==='true';
    b.setAttribute('aria-expanded',String(!open));
    n.classList.toggle('is-open',!open);
    if(!open)aqTrack('menu_open');
  });

  var toc=document.querySelector('[data-toc]'),body=document.querySelector('.article-content');
  if(toc&&body){
    var hs=body.querySelectorAll('h2,h3');
    if(hs.length){
      var ul=document.createElement('ol');
      hs.forEach(function(h,i){
        if(!h.id)h.id='section-'+(i+1);
        var li=document.createElement('li'),a=document.createElement('a');
        a.href='#'+h.id;a.textContent=h.textContent;li.appendChild(a);ul.appendChild(li);
      });
      toc.appendChild(ul);
      toc.addEventListener('click',function(e){
        var a=e.target.closest('a');
        if(a)aqTrack('toc_click',a.getAttribute('href')||'');
      });
    }else toc.hidden=true;
  }

  var locale=(document.documentElement.getAttribute('lang')||'zh').slice(0,2);
  var path=location.pathname||'/';
  var queue=[];
  var flushTimer=null;
  function aqTrack(name,value){
    if(!name)return;
    queue.push({name:name,value:value||null,path:path,locale:locale});
    if(flushTimer)return;
    flushTimer=setTimeout(flush,800);
  }
  function flush(){
    flushTimer=null;
    if(!queue.length)return;
    var payload=JSON.stringify({events:queue.splice(0,queue.length)});
    try{
      if(navigator.sendBeacon){
        navigator.sendBeacon('/analytics/collect',new Blob([payload],{type:'application/json'}));
        return;
      }
    }catch(e){}
    fetch('/analytics/collect',{method:'POST',headers:{'Content-Type':'application/json'},body:payload,keepalive:true,credentials:'same-origin'}).catch(function(){});
  }
  window.addEventListener('pagehide',flush);
  document.addEventListener('visibilitychange',function(){if(document.visibilityState==='hidden')flush();});

  document.querySelectorAll('.lang-switch a').forEach(function(a){
    a.addEventListener('click',function(){aqTrack('lang_switch',a.getAttribute('hreflang')||a.textContent||'');});
  });

  var search=document.querySelector('.search-form');
  if(search)search.addEventListener('submit',function(){
    var q=(search.querySelector('input[name="q"]')||{}).value||'';
    aqTrack('search',String(q).slice(0,80));
    flush();
  });

  document.addEventListener('click',function(e){
    var a=e.target.closest('a');
    if(!a||!a.href)return;
    try{
      var u=new URL(a.href,location.origin);
      if(u.origin!==location.origin){
        aqTrack('outbound_click',u.host+(u.pathname||''));
      }else if(a.classList.contains('button')||a.classList.contains('button-dark')||a.classList.contains('button-light')){
        aqTrack('cta_click',u.pathname);
      }
    }catch(err){}
  });

  var marks={25:false,50:false,75:false,100:false};
  function onScroll(){
    var doc=document.documentElement;
    var max=Math.max(1,(doc.scrollHeight||0)-(window.innerHeight||0));
    var pct=Math.min(100,Math.round((window.scrollY||doc.scrollTop||0)/max*100));
    [25,50,75,100].forEach(function(m){
      if(!marks[m]&&pct>=m){marks[m]=true;aqTrack('scroll_depth',String(m));}
    });
  }
  window.addEventListener('scroll',onScroll,{passive:true});
  onScroll();
});
