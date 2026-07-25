// Province page renderer — reads data/provinces.json by window.SLUG
(async function () {
  const SLUG = window.SLUG;
  const content = document.getElementById('provinceContent');
  if (!content) return;
  let data, site = { social: {} };
  try {
    const res = await fetch('../data/provinces.json');
    if (!res.ok) throw new Error('fetch failed');
    data = await res.json();
  } catch (e) {
    console.warn('province fetch failed, using inline fallback:', e);
    const el = document.getElementById('province-data');
    data = el ? JSON.parse(el.textContent) : [];
  }
  try {
    const sres = await fetch('../data/site.json');
    if (sres.ok) site = await sres.json();
  } catch (e) { /* social optional */ }

  const p = data.find(x => x.slug === SLUG);
  if (!p) { content.innerHTML = '<p class="coming">Province not found.</p>'; return; }

  const videos = (p.videoIds || []).map(vid =>
    `<div class="province-video"><iframe width="100%" height="100%" src="https://www.youtube.com/embed/${vid}" title="${p.nameEn} video on YouTube" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>`
  ).join('');

  const kw = (p.keywords || []).map(k => `<span class="kw">${k}</span>`).join('');
  const related = (p.relatedProvinces || []).map(r => {
    const rp = data.find(x => x.slug === r);
    const label = rp ? rp.nameEn : r;
    return `<a class="rel" href="./${r}.html">${label}</a>`;
  }).join('');

  // NEW: travel guide (SEO long-form content)
  const guide = p.guide ? renderGuide(p.guide) : '';
  // NEW: affiliate "Plan your trip"
  const affiliate = p.affiliate ? renderAffiliate(p.affiliate) : '';
  // NEW: social matrix (from site.json)
  const social = renderSocial(site.social);
  // NEW: long-form guide CTA (option B) — links province page to guides/{slug}.html
  const guideCta = p.guideUrl ? renderGuideCta(p.guideUrl) : '';

  content.innerHTML = `
    <a href="../" class="back-link">&larr; Back to the map</a>
    <h1>${p.nameEn}</h1>
    <p class="zh">${p.nameZh || ''}</p>
    ${p.hook ? `<p class="hook">${p.hook}</p>` : ''}
    ${p.hookData ? `<p class="hookdata">${p.hookData}</p>` : ''}
    ${p.description ? `<p class="desc">${p.description}</p>` : ''}
    ${p.dataCards && p.dataCards.length ? `
    <div class="data-cards">
      ${p.dataCards.map(c => `
        <div class="dc">
          <div class="dc-label">${c.label}</div>
          <div class="dc-value">${c.value}</div>
          ${c.compare ? `<div class="dc-cmp">${c.compare}</div>` : ''}
        </div>`).join('')}
    </div>` : ''}
    ${p.summaryZh ? `<div class="zh-intro"><h3>中文简介</h3><p>${p.summaryZh}</p></div>` : ''}
    ${videos ? `<h2>Watch</h2>${videos}` : '<p class="coming">Video coming soon &mdash; paste YouTube IDs into provinces.json &rarr; videoIds</p>'}
    ${guideCta}
    ${guide}
    ${affiliate}
    ${kw ? `<div class="keywords">${kw}</div>` : ''}
    ${related ? `<div class="related"><span>Related:</span>${related}</div>` : ''}
    ${social}
  `;
  document.title = p.metaTitle || p.nameEn;

  function renderGuide(g) {
    const blocks = [];
    if (g.bestTime) blocks.push(block('Best time to visit', g.bestTime));
    if (g.getThere) blocks.push(block('How to get there', g.getThere));
    if (g.itinerary && g.itinerary.length) blocks.push(listBlock('Suggested itinerary', g.itinerary));
    if (g.food && g.food.length) blocks.push(listBlock("Food you can't miss", g.food));
    if (g.hiddenGems && g.hiddenGems.length) blocks.push(listBlock('Hidden gems only locals know', g.hiddenGems));
    if (!blocks.length) return '';
    return `<div class="guide"><h2>Travel guide</h2>${blocks.join('')}</div>`;
    function block(title, text) { return `<div class="guide-block"><h3>${title}</h3><p>${text}</p></div>`; }
    function listBlock(title, items) { return `<div class="guide-block"><h3>${title}</h3><ul>${items.map(i => `<li>${i}</li>`).join('')}</ul></div>`; }
  }

  function renderGuideCta(url) {
    return `<div class="guide-cta"><span class="gc-text">Read our full <strong>${p.nameEn}</strong> travel guide</span><a class="gc-link" href="../${url}">Read the guide &rarr;</a></div>`;
  }

  function renderAffiliate(a) {
    const cards = [];
    if (a.booking) cards.push(affCard('Book hotels', a.booking, 'Booking.com'));
    if (a.tripcom) cards.push(affCard('Tours & tickets', a.tripcom, 'Trip.com'));
    if (a.ctrip) cards.push(affCard('中国国内预订', a.ctrip, '携程 Ctrip'));
    if (!cards.length) return '';
    return `<div class="affiliate"><h2>Plan your trip</h2><p class="aff-intro">Support Deep in China — book through our partners at no extra cost to you.</p><div class="affiliate-cards">${cards.join('')}</div></div>`;
    function affCard(label, url, brand) { return `<a class="aff-card" href="${url}" target="_blank" rel="noopener sponsored">${label}<span>${brand} &rarr;</span></a>`; }
  }

  function renderSocial(social) {
    if (!social) return '';
    const items = [];
    if (social.youtube) items.push(soc('YouTube', social.youtube));
    if (social.tiktok) items.push(soc('TikTok', social.tiktok));
    if (social.instagram) items.push(soc('Instagram', social.instagram));
    if (social.xiaohongshu) items.push(soc('小红书', social.xiaohongshu));
    if (social.bilibili) items.push(soc('Bilibili', social.bilibili));
    if (social.douyin) items.push(soc('抖音', social.douyin));
    if (!items.length) return '';
    return `<div class="social-matrix"><h3>Follow Deep in China</h3><div class="social-links">${items.join('')}</div></div>`;
    function soc(name, url) { return `<a class="social-link" href="${url}" target="_blank" rel="noopener">${name}</a>`; }
  }
})();
