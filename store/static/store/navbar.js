const hamburger = document.getElementById('hamburger');
  const panel = document.getElementById('mobilePanel');
  const scrim = document.getElementById('scrim');

  function closeMenu() {
    hamburger.classList.remove('open');
    hamburger.setAttribute('aria-expanded', 'false');
    panel.classList.remove('open');
    scrim.classList.remove('open');
  }

  function toggleMenu() {
    const isOpen = hamburger.classList.toggle('open');
    hamburger.setAttribute('aria-expanded', String(isOpen));
    panel.classList.toggle('open', isOpen);
    scrim.classList.toggle('open', isOpen);
  }

  hamburger.addEventListener('click', toggleMenu);
  scrim.addEventListener('click', closeMenu);
  panel.querySelectorAll('a, button').forEach(el => el.addEventListener('click', closeMenu));
  window.addEventListener('resize', () => { if (window.innerWidth > 900) closeMenu(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });