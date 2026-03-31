/**
 * HOME PAGE JS
 * Handles: Lightbox · Animated stat counters
 */

document.addEventListener('DOMContentLoaded', () => {
  initLightbox();
});

/* ═══════════════════════════════════════════════════════
   GALLERY LIGHTBOX
   ═══════════════════════════════════════════════════════ */
function initLightbox() {
  const lightbox       = document.getElementById('lightbox');
  const backdrop       = document.getElementById('lightboxBackdrop');
  const lightboxImg    = document.getElementById('lightboxImg');
  const lightboxCap    = document.getElementById('lightboxCaption');
  const closeBtn       = document.getElementById('lightboxClose');
  const prevBtn        = document.getElementById('lightboxPrev');
  const nextBtn        = document.getElementById('lightboxNext');

  if (!lightbox) return;

  // Collect all gallery items
  const items = Array.from(document.querySelectorAll('.gallery-item[data-src]'));
  let current = 0;

  function openLightbox(index) {
    current = index;
    const item = items[current];
    if (!item) return;

    lightboxImg.src = item.dataset.src;
    lightboxImg.alt = item.dataset.caption || '';
    if (lightboxCap) lightboxCap.textContent = item.dataset.caption || '';

    lightbox.hidden = false;
    backdrop.hidden = false;
    document.body.style.overflow = 'hidden';
    lightboxImg.style.opacity = '0';
    lightboxImg.style.transform = 'scale(0.95)';

    // Animate in
    requestAnimationFrame(() => {
      lightboxImg.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      lightboxImg.style.opacity = '1';
      lightboxImg.style.transform = 'scale(1)';
    });

    // Update nav button visibility
    if (prevBtn) prevBtn.style.display = items.length > 1 ? '' : 'none';
    if (nextBtn) nextBtn.style.display = items.length > 1 ? '' : 'none';
  }

  function closeLightbox() {
    lightboxImg.style.opacity = '0';
    lightboxImg.style.transform = 'scale(0.95)';
    setTimeout(() => {
      lightbox.hidden = true;
      backdrop.hidden = true;
      document.body.style.overflow = '';
      lightboxImg.src = '';
    }, 300);
  }

  function navigate(dir) {
    current = (current + dir + items.length) % items.length;
    lightboxImg.style.opacity = '0';
    lightboxImg.style.transform = `scale(0.95) translateX(${dir * 30}px)`;
    setTimeout(() => {
      const item = items[current];
      lightboxImg.src = item.dataset.src;
      lightboxImg.alt = item.dataset.caption || '';
      if (lightboxCap) lightboxCap.textContent = item.dataset.caption || '';
      lightboxImg.style.transform = `scale(0.95) translateX(${-dir * 30}px)`;
      requestAnimationFrame(() => {
        lightboxImg.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        lightboxImg.style.opacity = '1';
        lightboxImg.style.transform = 'scale(1) translateX(0)';
      });
    }, 200);
  }

  // Attach click to each gallery item
  items.forEach((item, i) => {
    item.addEventListener('click', () => openLightbox(i));
    item.setAttribute('role', 'button');
    item.setAttribute('tabindex', '0');
    item.setAttribute('aria-label', `View: ${item.dataset.caption || 'Image ' + (i + 1)}`);
    item.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLightbox(i); }
    });
  });

  // Controls
  if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
  if (backdrop) backdrop.addEventListener('click', closeLightbox);
  if (prevBtn)  prevBtn.addEventListener('click', () => navigate(-1));
  if (nextBtn)  nextBtn.addEventListener('click', () => navigate(1));

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (lightbox.hidden) return;
    if (e.key === 'Escape')     closeLightbox();
    if (e.key === 'ArrowLeft')  navigate(-1);
    if (e.key === 'ArrowRight') navigate(1);
  });

  // Touch/swipe support
  let touchStartX = 0;
  lightbox.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; }, { passive: true });
  lightbox.addEventListener('touchend', (e) => {
    const diff = touchStartX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 60) navigate(diff > 0 ? 1 : -1);
  });
}

/* ═══════════════════════════════════════════════════════
   ANIMATED STAT COUNTERS
   Counts from 0 to the target value when scrolled into view.
   Supports values like "12,000+" or "500+" etc.
   ═══════════════════════════════════════════════════════ */
