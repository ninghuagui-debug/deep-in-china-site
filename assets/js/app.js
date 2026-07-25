// Deep in China — Main Application (data-driven, single source: data/provinces.json)
const SITE_CONFIG = {
  brand: 'Deep in China',
  slogan: 'Go deeper than any tourist ever goes',
  youtubeUrl: 'https://www.youtube.com/@DeepinChina-n'
};

let PROVINCES = [];
const PROVINCE_BY_MAPNAME = {};

document.addEventListener('DOMContentLoaded', () => {
  fetch('data/provinces.json')
    .then(r => {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(data => afterData(data))
    .catch(err => {
      console.warn('provinces.json fetch failed, using inline fallback:', err);
      const el = document.getElementById('province-data');
      afterData(el ? JSON.parse(el.textContent) : []);
    });
  initNavScroll();
});

function afterData(data) {
  PROVINCES = data;
  PROVINCES.forEach(p => { PROVINCE_BY_MAPNAME[p.mapName] = p; });
  initMap();
  initVideoGrid();
}

function initMap() {
  const mapContainer = document.getElementById('chinaMap');
  const tooltip = document.getElementById('provinceTooltip');
  const panel = document.getElementById('provincePanel');

  // SVG 已内联进 index.html，直接绑定事件，无需运行时 fetch
  bindMapEvents(mapContainer, tooltip, panel);

  document.getElementById('panelClose').addEventListener('click', () => {
    panel.classList.add('hidden');
    document.querySelectorAll('#china-map-real .province.active').forEach(p => p.classList.remove('active'));
  });
}

function bindMapEvents(mapContainer, tooltip, panel) {
  mapContainer.querySelectorAll('#china-map-real .province').forEach(path => {
    const mapName = path.dataset.name;
    const province = PROVINCE_BY_MAPNAME[mapName];
    if (province && province.hotspot && province.hotspot.title) path.classList.add('has-hotspot');

    path.addEventListener('mouseenter', (e) => {
      if (province) {
        const hs = province.hotspot;
        if (hs && hs.title) {
          tooltip.innerHTML = `<div class="tip-media"><img src="${hs.image || ''}" alt=""></div><div class="tip-title">${hs.title}</div><div class="tip-summary">${hs.summary || ''}</div><div class="tip-cta">▶ Watch the real video</div>`;
        } else {
          tooltip.innerHTML = `<div class="tip-name">${province.nameEn}</div><div class="tip-hook">${province.hook}</div>`;
        }
        tooltip.classList.remove('hidden');
        positionTooltip(e, tooltip);
      }
    });

    path.addEventListener('mousemove', (e) => positionTooltip(e, tooltip));

    path.addEventListener('mouseleave', () => tooltip.classList.add('hidden'));

    path.addEventListener('click', () => {
      if (province) showProvincePanel(province, path);
    });
  });
}

function positionTooltip(e, tooltip) {
  const rect = document.querySelector('.map-wrapper').getBoundingClientRect();
  let left = e.clientX - rect.left + 12;
  let top = e.clientY - rect.top + 12;
  const tipRect = tooltip.getBoundingClientRect();
  if (left + tipRect.width > rect.width) left = e.clientX - rect.left - tipRect.width - 12;
  if (top + tipRect.height > rect.height) top = e.clientY - rect.top - tipRect.height - 12;
  tooltip.style.left = left + 'px';
  tooltip.style.top = top + 'px';
}

function showProvincePanel(province, path) {
  const panel = document.getElementById('provincePanel');
  document.querySelectorAll('#china-map-real .province.active').forEach(p => p.classList.remove('active'));
  path.classList.add('active');

  document.getElementById('panelTitle').textContent = province.nameEn;
  document.getElementById('panelHook').textContent = province.hook;
  document.getElementById('panelDesc').textContent = province.description;
  // Phase 2 独立省页；当前点击会 404，待 /province/<slug>.html 生成
  document.getElementById('panelLink').href = `/province/${province.slug}.html`;
  document.getElementById('panelVideos').innerHTML = province.videoIds && province.videoIds.length > 0
    ? province.videoIds.map(vid =>
        `<div class="panel-video-item"><iframe width="340" height="190" src="https://www.youtube.com/embed/${vid}" title="${province.nameEn} video on YouTube" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>`
      ).join('')
    : '<p style="color:var(--text-secondary);font-size:13px;">Video coming soon — paste YouTube video IDs into provinces.json → videoIds</p>';

  const affEl = document.getElementById('panelAffiliate');
  if (affEl) {
    affEl.innerHTML = `<div class="affiliate">
      <h2>Plan your trip to ${province.nameEn}</h2>
      <p class="aff-intro">As an affiliate, we may earn from partner links at no extra cost to you.</p>
      <div class="affiliate-cards">
        <a class="aff-card" href="https://www.booking.com" target="_blank" rel="noopener">Hotels &amp; Stays <span>Booking.com</span></a>
        <a class="aff-card" href="https://www.trip.com" target="_blank" rel="noopener">Flights &amp; Tours <span>Trip.com</span></a>
        <a class="aff-card" href="https://www.amazon.com" target="_blank" rel="noopener">Travel Gear <span>Amazon</span></a>
      </div>
    </div>`;
  }

  const dcEl = document.getElementById('panelDataCards');
  if (dcEl) {
    dcEl.innerHTML = province.dataCards && province.dataCards.length
      ? province.dataCards.map(c => `<div class="dc"><div class="dc-label">${c.label}</div><div class="dc-value">${c.value}</div>${c.compare ? `<div class="dc-cmp">${c.compare}</div>` : ''}</div>`).join('')
      : '';
  }

  panel.classList.remove('hidden');
}

function openProvinceByMapName(mapName) {
  const path = document.querySelector(`#china-map-real .province[data-name="${mapName}"]`);
  const province = PROVINCE_BY_MAPNAME[mapName];
  if (path && province) showProvincePanel(province, path);
}

function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function initVideoGrid() {
  const grid = document.getElementById('videoGrid');
  if (!grid) return;
  // 读频道最新视频流 (由 scripts/update_site_videos.py 自动生成 data/videos.json)
  fetch('data/videos.json')
    .then(r => r.ok ? r.json() : [])
    .then(videos => {
      if (!Array.isArray(videos) || videos.length === 0) return; // 保留 HTML 静态占位
      grid.innerHTML = '';
      videos.slice(0, 12).forEach(v => {
        const card = document.createElement('a');
        card.className = 'video-card';
        card.href = v.url || ('https://www.youtube.com/watch?v=' + v.id);
        card.target = '_blank';
        card.rel = 'noopener';
        const thumb = v.thumbnail || ('https://i.ytimg.com/vi/' + v.id + '/hqdefault.jpg');
        card.innerHTML = `
          <div class="video-thumb">
            <img src="${escapeHtml(thumb)}" alt="${escapeHtml(v.title)}" loading="lazy" style="width:100%;height:180px;object-fit:cover;display:block;">
          </div>
          <div class="video-info">
            <h3>${escapeHtml(v.title)}</h3>
            <p class="video-province">${escapeHtml(v.published || 'New')}</p>
          </div>`;
        grid.appendChild(card);
      });
    })
    .catch(() => { /* 读取失败时保留静态占位 */ });
}

function initNavScroll() {
  const nav = document.querySelector('.nav');
  window.addEventListener('scroll', () => {
    nav.style.boxShadow = window.scrollY > 100 ? '0 2px 12px rgba(0,0,0,0.1)' : 'none';
  });
}
