/**
 * APEX UNIVERSITY - MAIN JS
 * Handles: Preloader, cursor, navbar, mobile menu, flash messages, footer year
 */

window.addEventListener('load', () => {
  initPreloader();
});

function initPreloader() {
  const preloader = document.getElementById('preloader');
  const fill = preloader?.querySelector('.preloader-fill');
  const percentEl = preloader?.querySelector('.preloader-percent');

  if (!preloader) {
    bootSite();
    return;
  }

  let progress = 0;
  const interval = setInterval(() => {
    progress += Math.random() * (progress < 60 ? 4 : progress < 85 ? 8 : 3);

    if (progress >= 100) {
      progress = 100;
      clearInterval(interval);
      finishPreloader();
    }

    if (fill) fill.style.width = progress + '%';
    if (percentEl) percentEl.textContent = Math.floor(progress) + '%';
  }, 40);

  function finishPreloader() {
    setTimeout(() => {
      preloader.classList.add('hidden');
      preloader.addEventListener(
        'transitionend',
        () => {
          preloader.remove();
          bootSite();
        },
        { once: true }
      );
    }, 300);
  }
}

function bootSite() {
  initCursor();
  initNavbar();
  initHamburger();
  initFlashMessages();
  initFooterYear();
}

function initCursor() {
  const cursor = document.getElementById('cursor');
  if (!cursor || window.matchMedia('(hover: none)').matches) return;

  const dot = cursor.querySelector('.cursor-dot');
  const ring = cursor.querySelector('.cursor-ring');

  let mouseX = 0;
  let mouseY = 0;
  let ringX = 0;
  let ringY = 0;

  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;

    if (dot) {
      dot.style.left = mouseX + 'px';
      dot.style.top = mouseY + 'px';
    }
  });

  function animateRing() {
    ringX += (mouseX - ringX) * 0.12;
    ringY += (mouseY - ringY) * 0.12;

    if (ring) {
      ring.style.left = ringX + 'px';
      ring.style.top = ringY + 'px';
    }

    requestAnimationFrame(animateRing);
  }

  animateRing();

  const hoverTargets = 'a, button, .blog-card, .gallery-item, .filter-btn, .nav-cta, .btn';
  document.querySelectorAll(hoverTargets).forEach((el) => {
    el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
    el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
  });
}

function initNavbar() {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;

  const threshold = 60;
  let ticking = false;

  window.addEventListener(
    'scroll',
    () => {
      if (ticking) return;

      requestAnimationFrame(() => {
        navbar.classList.toggle('scrolled', window.scrollY > threshold);
        ticking = false;
      });

      ticking = true;
    },
    { passive: true }
  );
}

function initHamburger() {
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobileMenu');
  if (!hamburger || !mobileMenu) return;

  let isOpen = false;

  hamburger.addEventListener('click', () => {
    isOpen = !isOpen;
    hamburger.classList.toggle('open', isOpen);
    hamburger.setAttribute('aria-expanded', String(isOpen));
    mobileMenu.classList.toggle('open', isOpen);
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  mobileMenu.querySelectorAll('.mobile-link').forEach((link) => {
    link.addEventListener('click', () => {
      isOpen = false;
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
      mobileMenu.classList.remove('open');
      document.body.style.overflow = '';
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isOpen) hamburger.click();
  });
}

function initFlashMessages() {
  document.querySelectorAll('.flash-close').forEach((btn) => {
    btn.addEventListener('click', () => {
      const flash = btn.closest('.flash');
      if (!flash) return;

      flash.style.opacity = '0';
      flash.style.transform = 'translateX(120%)';
      flash.style.transition = 'all 0.4s ease';
      setTimeout(() => flash.remove(), 400);
    });
  });

  document.querySelectorAll('.flash').forEach((flash, i) => {
    setTimeout(() => {
      if (!flash.parentNode) return;

      flash.style.opacity = '0';
      flash.style.transform = 'translateX(120%)';
      flash.style.transition = 'all 0.4s ease';
      setTimeout(() => flash.remove(), 400);
    }, 6000 + i * 500);
  });
}

function initFooterYear() {
  const el = document.getElementById('year');
  if (el) el.textContent = new Date().getFullYear();
}
