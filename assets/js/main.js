/* Foot Delux — shared site script (burger menu, scroll reveal, nav shrink,
   hero entrance animation, stat counters, video play, contact form). */
(function(){
  'use strict';

  /* mobile burger menu */
  var burger = document.getElementById('burger');
  var menu = document.getElementById('menu');
  if (burger && menu) {
    burger.addEventListener('click', function(){
      var open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
    });
    menu.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){
        menu.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* nav shrink on scroll */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function(){
      if (window.scrollY > 40) header.classList.add('scrolled');
      else header.classList.remove('scrolled');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* hero: word-by-word rise-in for the headline + Ken Burns background */
  document.querySelectorAll('.hero h1').forEach(function(h1){
    if (h1.children.length) return;
    var words = h1.textContent.trim().split(/\s+/);
    h1.textContent = '';
    words.forEach(function(w, i){
      var span = document.createElement('span');
      span.className = 'fd-word';
      span.style.animationDelay = (0.12 + i * 0.08).toFixed(2) + 's';
      span.textContent = w;
      h1.appendChild(span);
      if (i < words.length - 1) h1.appendChild(document.createTextNode(' '));
    });
    h1.classList.add('fd-split');
  });
  var hero = document.querySelector('.hero');
  if (hero) {
    window.setTimeout(function(){ hero.classList.add('in-view'); }, 60);
  }

  /* stat counters (data-count="15" data-suffix="+") */
  var locale = document.documentElement.lang || 'es';
  function animateCount(el){
    var target = parseInt(el.getAttribute('data-count'), 10);
    if (isNaN(target)) return;
    var suffix = el.getAttribute('data-suffix') || '';
    var duration = 1400;
    var start = null;
    function tick(ts){
      if (start === null) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased).toLocaleString(locale) + suffix;
      if (p < 1) window.requestAnimationFrame(tick);
    }
    window.requestAnimationFrame(tick);
  }

  /* video play overlay */
  document.querySelectorAll('[data-play]').forEach(function(wrap){
    wrap.addEventListener('click', function(){
      var v = this.querySelector('video');
      if (!v) return;
      var o = this.querySelector('.play-overlay');
      if (o) o.style.display = 'none';
      v.controls = true;
      v.play().catch(function(){});
    });
  });

  /* YouTube click-to-load: no request reaches YouTube until the visitor asks
     for the video, and the player is then loaded from the no-cookie host. */
  document.querySelectorAll('.yt-facade').forEach(function(btn){
    btn.addEventListener('click', function(){
      var id = btn.getAttribute('data-yt-id');
      if (!id) return;
      var frame = document.createElement('iframe');
      frame.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
      frame.title = btn.getAttribute('data-yt-title') || '';
      frame.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
      frame.setAttribute('allowfullscreen', '');
      frame.style.cssText = 'position:absolute;top:0;left:0;width:100%;height:100%;border:0';
      btn.parentNode.replaceChild(frame, btn);
      frame.focus();
    });
  });

  /* scroll reveal + stat counters, shared observer */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in');
        if (entry.target.hasAttribute('data-animate')) {
          entry.target.querySelectorAll('[data-count]').forEach(animateCount);
        }
        io.unobserve(entry.target);
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal, [data-animate]').forEach(function(el){ io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function(el){ el.classList.add('in'); });
    document.querySelectorAll('[data-count]').forEach(animateCount);
  }

  /* contact form — posts to contact.php, which mails the practice (always in
     Spanish) and sends the patient an acknowledgement in the page's language */
  document.querySelectorAll('[data-contact-form]').forEach(function(form){
    form.addEventListener('submit', function(e){
      e.preventDefault();

      var endpoint = form.getAttribute('data-endpoint') || 'contact.php';
      var btn = form.querySelector('button[type="submit"]');
      var ok = form.querySelector('.ok');
      var err = form.querySelector('.err');
      var sendingLabel = form.getAttribute('data-sending') || '…';
      var idleLabel = btn ? btn.textContent : '';

      if (ok) ok.style.display = 'none';
      if (err) err.style.display = 'none';
      if (btn) { btn.disabled = true; btn.textContent = sendingLabel; }

      fetch(endpoint, { method: 'POST', body: new FormData(form) })
        .then(function(res){ return res.json().catch(function(){ return { ok: res.ok }; }); })
        .then(function(data){
          if (data && data.ok) {
            if (ok) ok.style.display = 'block';
            form.reset();
          } else {
            if (err) err.style.display = 'block';
          }
        })
        .catch(function(){
          if (err) err.style.display = 'block';
        })
        .then(function(){
          if (btn) { btn.disabled = false; btn.textContent = idleLabel; }
        });
    });
  });

})();
