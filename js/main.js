document.addEventListener('DOMContentLoaded', () => {
  const header = document.getElementById('site-header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('solid', window.scrollY > 40);
    });
  }

  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    revealEls.forEach(el => io.observe(el));
  }

  // simple filter chips (circuits hub) — client-side show/hide by data attributes
  const filterGroups = document.querySelectorAll('[data-filter-group]');
  filterGroups.forEach(group => {
    const chips = group.querySelectorAll('.filter-chip');
    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        chips.forEach(c => c.classList.remove('is-active'));
        chip.classList.add('is-active');
        const val = chip.getAttribute('data-filter-value');
        const targetGrid = document.querySelector(group.getAttribute('data-filter-target'));
        if (!targetGrid) return;
        targetGrid.querySelectorAll('[data-tags]').forEach(card => {
          const tags = card.getAttribute('data-tags').split(',');
          card.style.display = (val === 'all' || tags.includes(val)) ? '' : 'none';
        });
      });
    });
  });

  // interactive zone map (pin click)
  const pins = document.querySelectorAll('.pin');
  if (pins.length) {
    const panels = document.querySelectorAll('.zone-content');
    pins.forEach(pin => {
      pin.addEventListener('click', () => {
        const zone = pin.getAttribute('data-zone');
        pins.forEach(p => p.classList.remove('active'));
        pin.classList.add('active');
        panels.forEach(p => p.style.display = 'none');
        const target = document.getElementById('zone-' + zone);
        if (target) target.style.display = 'block';
      });
    });
    const first = document.querySelector('.pin[data-zone]');
    if (first) first.classList.add('active');
  }
});
