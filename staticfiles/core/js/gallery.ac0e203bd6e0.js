/**
 * GALLERY PAGE JS
 * Reuses the same lightbox logic, applied to the full gallery page.
 */
document.addEventListener('DOMContentLoaded', () => {
  initGalleryLightbox();
});

function initGalleryLightbox() {
  const lightbox    = document.getElementById('lightbox');
  const backdrop    = document.getElementById('lightboxBackdrop');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxCap = document.getElementById('lightboxCaption');
  const closeBtn    = document.getElementById('lightboxClose');
  const prevBtn     = document.getElementById('lightboxPrev');
  const nextBtn     = document.getElementById('lightboxNext');

  if (!lightbox) return;

  const items  = Array.from(document.querySelectorAll('.gallery-item[data-src]'));
  let current  = 0;

  function openLightbox(index) {
    current = index;
    const item = items[current];
    if (!item) return;
    lightboxImg.src = item.dataset.src;
    lightboxImg.alt = item.dataset.caption || '';
    if (lightboxCap) lightboxCap.textContent = item.dataset.caption || '';
    lightbox.hidden  = false;
    backdrop.hidden  = false;
    document.body.style.overflow = 'hidden';
    lightboxImg.style.opacity   = '0';
    lightboxImg.style.transform = 'scale(0.95)';
    requestAnimationFrame(() => {
      lightboxImg.style.transition = 'opacity 0.4s, transform 0.4s';
      lightboxImg.style.opacity    = '1';
      lightboxImg.style.transform  = 'scale(1)';
    });
  }

  function closeLightbox() {
    lightboxImg.style.opacity   = '0';
    lightboxImg.style.transform = 'scale(0.95)';
    setTimeout(() => {
      lightbox.hidden = true;
      backdrop.hidden = true;
      document.body.style.overflow = '';
    }, 300);
  }

  function navigate(dir) {
    current = (current + dir + items.length) % items.length;
    lightboxImg.style.opacity   = '0';
    lightboxImg.style.transform = `scale(0.95) translateX(${dir * 40}px)`;
    setTimeout(() => {
      const item = items[current];
      lightboxImg.src = item.dataset.src;
      lightboxImg.alt = item.dataset.caption || '';
      if (lightboxCap) lightboxCap.textContent = item.dataset.caption || '';
      lightboxImg.style.transform = `scale(0.95) translateX(${-dir * 40}px)`;
      requestAnimationFrame(() => {
        lightboxImg.style.transition = 'opacity 0.3s, transform 0.3s';
        lightboxImg.style.opacity    = '1';
        lightboxImg.style.transform  = 'scale(1) translateX(0)';
      });
    }, 200);
  }

  items.forEach((item, i) => {
    item.addEventListener('click', () => openLightbox(i));
    item.setAttribute('role', 'button');
    item.setAttribute('tabindex', '0');
    item.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLightbox(i); }
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
  if (backdrop) backdrop.addEventListener('click', closeLightbox);
  if (prevBtn)  prevBtn.addEventListener('click', () => navigate(-1));
  if (nextBtn)  nextBtn.addEventListener('click', () => navigate(1));

  document.addEventListener('keydown', (e) => {
    if (lightbox.hidden) return;
    if (e.key === 'Escape')     closeLightbox();
    if (e.key === 'ArrowLeft')  navigate(-1);
    if (e.key === 'ArrowRight') navigate(1);
  });

  // Swipe support
  let startX = 0;
  lightbox.addEventListener('touchstart', e => { startX = e.touches[0].clientX; }, { passive: true });
  lightbox.addEventListener('touchend',   e => {
    const diff = startX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 60) navigate(diff > 0 ? 1 : -1);
  });
}
