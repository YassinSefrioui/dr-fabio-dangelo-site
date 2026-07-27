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

  /* contact form — no backend available; fall back to a pre-filled mailto so
     leads aren't silently discarded (see HANDOFF.md §3.1) */
  document.querySelectorAll('[data-contact-form]').forEach(function(form){
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var data = new FormData(form);
      var name = (data.get('name') || '').toString().trim();
      var email = (data.get('email') || '').toString().trim();
      var phone = (data.get('phone') || '').toString().trim();
      var message = (data.get('message') || '').toString().trim();
      var to = form.getAttribute('data-to') || 'info@footdelux.com';
      var lName = form.getAttribute('data-label-name') || 'Name';
      var lEmail = form.getAttribute('data-label-email') || 'Email';
      var lPhone = form.getAttribute('data-label-phone') || 'Phone';
      var lMessage = form.getAttribute('data-label-message') || 'Message';
      var subject = encodeURIComponent((form.getAttribute('data-subject') || 'Foot Delux — Contacto web') + (name ? ' · ' + name : ''));
      var lines = [];
      if (name) lines.push(lName + ': ' + name);
      if (email) lines.push(lEmail + ': ' + email);
      if (phone) lines.push(lPhone + ': ' + phone);
      if (message) { lines.push(''); lines.push(lMessage + ':'); lines.push(message); }
      var body = encodeURIComponent(lines.join('\n'));
      window.location.href = 'mailto:' + to + '?subject=' + subject + '&body=' + body;
      var ok = form.querySelector('.ok');
      if (ok) ok.style.display = 'block';
      form.reset();
    });
  });

})();
