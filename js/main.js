document.addEventListener('DOMContentLoaded', () => {
  const header = document.getElementById('site-header');
  if (header) {
    const alwaysSolid = header.classList.contains('solid');
    const updateHeader = () => header.classList.toggle('solid', alwaysSolid || window.scrollY > 40);
    window.addEventListener('scroll', updateHeader, { passive: true });
    updateHeader();

    const nav = header.querySelector('nav');
    const headerWrap = header.querySelector('.wrap');
    if (nav && headerWrap) {
      nav.id = nav.id || 'site-navigation';

      const menuToggle = document.createElement('button');
      menuToggle.className = 'menu-toggle';
      menuToggle.type = 'button';
      menuToggle.setAttribute('aria-controls', nav.id);
      menuToggle.setAttribute('aria-expanded', 'false');
      menuToggle.setAttribute('aria-label', 'Ouvrir le menu');
      for (let i = 0; i < 3; i += 1) menuToggle.appendChild(document.createElement('span'));
      headerWrap.insertBefore(menuToggle, nav);

      const setMenuOpen = (open) => {
        header.classList.toggle('menu-open', open);
        document.body.classList.toggle('menu-open', open);
        menuToggle.setAttribute('aria-expanded', String(open));
        menuToggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
      };

      menuToggle.addEventListener('click', () => setMenuOpen(!header.classList.contains('menu-open')));
      nav.addEventListener('click', (event) => {
        if (event.target.closest('a')) setMenuOpen(false);
      });
      document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && header.classList.contains('menu-open')) {
          setMenuOpen(false);
          menuToggle.focus();
        }
      });
      window.addEventListener('resize', () => {
        if (window.innerWidth > 1080) setMenuOpen(false);
      });

      const currentPage = window.location.pathname.split('/').pop() || 'index.html';
      const navLinks = [...nav.querySelectorAll('.nav-link')];
      const exactLink = navLinks.find((link) => {
        const linkPage = new URL(link.href, window.location.href).pathname.split('/').pop() || 'index.html';
        return linkPage === currentPage;
      });
      if (exactLink) {
        navLinks.forEach((link) => {
          const isCurrent = link === exactLink;
          link.classList.toggle('is-active', isCurrent);
          if (isCurrent) link.setAttribute('aria-current', 'page');
          else link.removeAttribute('aria-current');
        });
      }
    }
  }

  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if ('IntersectionObserver' in window && !reduceMotion) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
      }, { threshold: 0, rootMargin: '0px 0px -8% 0px' });
      revealEls.forEach((el) => {
        const isInitiallyVisible = el.getBoundingClientRect().top < window.innerHeight * 0.92;
        if (isInitiallyVisible) el.classList.add('in');
        else io.observe(el);
      });
    } else {
      revealEls.forEach(el => el.classList.add('in'));
    }
  }

  // Carte interactive de Sumba — le SVG d'origine reste visible si Leaflet ne charge pas.
  const mapElement = document.getElementById('sumba-map');
  const mapBlock = document.getElementById('dynamic-map-block');
  const mapNote = document.getElementById('sumba-map-note');
  const isWebProtocol = window.location.protocol === 'http:' || window.location.protocol === 'https:';
  if (mapElement && mapBlock && isWebProtocol && typeof window.L !== 'undefined') {
    try {
      const L = window.L;
      const islandBounds = [[-10.13, 118.82], [-9.20, 120.85]];
      const zoneBounds = {
        all: islandBounds,
        ouest: [[-9.86, 118.82], [-9.25, 119.35]],
        centre: [[-9.96, 119.25], [-9.27, 119.83]],
        est: [[-10.08, 119.76], [-9.18, 120.84]],
        sud: [[-10.14, 119.25], [-9.70, 120.46]]
      };

      const places = [
        { name: 'Tambolaka', type: 'city', label: 'Ville', position: [-9.4242221, 119.2447882], description: "Porte d'entrée de l'ouest de Sumba et point de départ idéal vers Kodi.", url: 'ville-tambolaka.html' },
        { name: 'Waikabubak', type: 'city', label: 'Ville', position: [-9.6355595, 119.4100521], description: "Capitale culturelle de l'ouest, entourée de villages traditionnels.", url: 'ville-waikabubak.html' },
        { name: 'Waingapu', type: 'city', label: 'Ville', position: [-9.6496672, 120.2637495], description: "Principale ville de l'est, entre savanes, plages et collines.", url: 'ville-waingapu.html' },
        { name: 'Lagon de Weekuri', type: 'place', label: 'Lieu à découvrir', position: [-9.4910861, 118.9598327], description: "Un lagon naturel aux eaux turquoise, séparé de l'océan par les rochers.", url: 'lieu-weekuri.html' },
        { name: 'Ratenggaro', type: 'place', label: 'Village traditionnel', position: [-9.6277210, 119.0030547], description: "Maisons aux toits vertigineux et tombeaux mégalithiques face à l'océan.", url: 'lieu-ratenggaro.html' },
        { name: 'Cascade de Lapopu', type: 'place', label: 'Cascade', position: [-9.6783249, 119.4929812], description: "Une cascade en gradins au cœur du parc national de Manupeu Tanah Daru.", url: 'lieu-lapopu.html' },
        { name: 'Collines de Wairinding', type: 'place', label: 'Panorama', position: [-9.6794624, 120.1000531], description: "Des vagues de savane qui changent de couleur au fil des saisons.", url: 'lieu-wairinding.html' },
        { name: 'Cascade de Tanggedu', type: 'place', label: 'Cascade', position: [-9.57484, 120.08837], description: "Un canyon minéral sculpté par une eau claire dans l'est de l'île.", url: 'lieu-tanggedu.html' },
        { name: 'Plage de Walakiri', type: 'place', label: 'Plage', position: [-9.6286074, 120.4275101], description: "Célèbre pour ses mangroves miniatures et ses couchers de soleil.", url: 'lieu-walakiri.html' },
        { name: 'Plage de Tarimbang', type: 'place', label: 'Plage', position: [-9.9583105, 119.9591754], description: "Une grande baie sauvage du sud, bordée de collines et appréciée des surfeurs.", url: 'lieu-tarimbang.html' },
        { name: 'Aéroport de Tambolaka', type: 'airport', label: 'Aéroport', position: [-9.4102269, 119.2433371], description: "Navette et transfert depuis l'aéroport de Tambolaka.", url: 'navette-tambolaka.html' },
        { name: 'Aéroport de Waingapu', type: 'airport', label: 'Aéroport', position: [-9.6677526, 120.3008069], description: "Navette et transfert depuis l'aéroport de Waingapu.", url: 'navette-waingapu.html' }
      ];

      // La carte doit être visible avant le calcul automatique de son cadrage.
      mapBlock.classList.add('map-enhanced');
      const map = L.map(mapElement, {
        zoomControl: false,
        scrollWheelZoom: false,
        minZoom: 7,
        maxBounds: [[-11, 118.15], [-8.35, 121.55]],
        maxBoundsViscosity: 0.75
      });

      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);
      L.control.zoom({ position: 'topright' }).addTo(map);
      L.control.scale({ position: 'bottomright', imperial: false, maxWidth: 110 }).addTo(map);

      const markerIcon = (type) => L.divIcon({
        className: 'sumba-marker-icon',
        html: `<span class="sumba-map-marker sumba-map-marker--${type}">${type === 'airport' ? '<span class="sumba-map-marker__plane" aria-hidden="true">✈</span>' : ''}</span>`,
        iconSize: [34, 42],
        iconAnchor: [17, 40],
        popupAnchor: [0, -36]
      });

      places.forEach((place) => {
        const popup = `
          <article class="sumba-map-popup">
            <span class="sumba-map-popup__type">${place.label}</span>
            <h3>${place.name}</h3>
            <p>${place.description}</p>
            <a href="${place.url}">Découvrir <span aria-hidden="true">→</span></a>
          </article>`;
        const marker = L.marker(place.position, {
          icon: markerIcon(place.type),
          title: place.name,
          alt: place.name,
          keyboard: true,
          riseOnHover: true
        }).addTo(map).bindPopup(popup, { maxWidth: 260, minWidth: 225 });

        if (place.type === 'city') {
          marker.bindTooltip(place.name, {
            permanent: true,
            direction: 'top',
            offset: [0, -34],
            className: 'sumba-city-label'
          });
        }
      });

      map.fitBounds(islandBounds, { padding: [28, 28] });
      if (mapNote) mapNote.textContent = 'Zoomez, déplacez la carte ou cliquez sur un marqueur pour ouvrir la fiche du lieu.';

      const zoneButtons = [...mapBlock.querySelectorAll('[data-map-zone]')];
      zoneButtons.forEach((button) => {
        button.addEventListener('click', () => {
          const zone = button.dataset.mapZone;
          if (!zoneBounds[zone]) return;
          zoneButtons.forEach((item) => {
            const active = item === button;
            item.classList.toggle('is-active', active);
            item.setAttribute('aria-pressed', String(active));
          });
          map.closePopup();
          map.flyToBounds(zoneBounds[zone], { padding: [34, 34], duration: 1.05 });
        });
      });

      window.requestAnimationFrame(() => map.invalidateSize());
    } catch (error) {
      mapBlock.classList.remove('map-enhanced');
      console.warn('La carte interactive n’a pas pu être initialisée.', error);
    }
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
