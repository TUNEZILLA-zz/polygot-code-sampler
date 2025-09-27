// VJ Desk Quirks - Platform-specific enhancements with A11y-first design
(() => {
  const q = new URLSearchParams(location.search);
  if (q.get('quirk') === 'off') return;

  const ua = navigator.userAgent.toLowerCase();
  const isIOS = /iphone|ipad|ipod/.test(ua);
  const isAndroid = /android/.test(ua);
  const isMac = /macintosh|mac os x/.test(ua) && !isIOS;
  const isWindows = /windows/.test(ua);
  const isLinux = /linux/.test(ua) && !isAndroid && !isChromeOS;
  const isSafari = /^((?!chrome|android).)*safari/.test(ua);
  const isFirefox = /firefox/.test(ua);
  const isEdge = /edg\//.test(ua);
  const isChrome = /chrome\//.test(ua) && !isEdge;

  const html = document.documentElement;

  // A11y-first feature checks
  const media = {
    reduced: matchMedia('(prefers-reduced-motion: reduce)').matches,
    contrast: matchMedia('(prefers-contrast: more)').matches,
    dark: matchMedia('(prefers-color-scheme: dark)').matches
  };
  if (media.reduced) html.classList.add('a11y-reduced');

  // Quirk classes (used by CSS + JS param maps)
  if (isMac && isSafari) html.classList.add('quirk-mac-safari');
  else if (isWindows && (isChrome || isEdge)) html.classList.add('quirk-win-lcd');
  else if (isLinux && isFirefox) html.classList.add('quirk-linux-ff');
  if (isIOS) html.classList.add('quirk-ios');
  if (isAndroid) html.classList.add('quirk-android');
  if (isEdge) html.classList.add('quirk-edge');

  // URL explicit quirk
  if (q.get('quirk')) html.classList.add('quirk-'+q.get('quirk'));

  // Expose a tiny API for your scripts
  window.QuirkProfile = {
    reduced: media.reduced,
    cls: Array.from(html.classList).filter(c=>c.startsWith('quirk-')),
    applyParams(p){ // mutate FX params tastefully
      if (media.reduced) {
        p.emit *= 0.6; p.motion *= 0.6; p.trails = Math.min(p.trails, 0.35);
      }
      if (html.classList.contains('quirk-mac-safari')) {
        p.glow = (p.glow ?? 0.8) * 1.1; p.easing = 'easeOutCubic';
      }
      if (html.classList.contains('quirk-win-lcd')) {
        p.scanlines = Math.max(p.scanlines ?? 0, 0.05);
        p.pixelSnap = true;
      }
      if (html.classList.contains('quirk-linux-ff')) {
        p.hudMono = true; p.asciiOverlay = p.asciiOverlay ?? 0.25;
      }
      if (html.classList.contains('quirk-ios')) {
        p.emit *= 0.75; p.halo *= 1.15; p.touchTarget = true;
      }
      if (html.classList.contains('quirk-android')) {
        p.amoled = true; p.sat = (p.sat ?? 1.0) * 1.12;
      }
      if (html.classList.contains('quirk-edge')) {
        p.acrylicHUD = true;
      }
      return p;
    }
  };

  // Log applied profile for debugging
  console.log('🎭 VJ Quirks:', window.QuirkProfile.cls.join(', ') || 'none', 
              media.reduced ? '(A11y reduced)' : '');

  // Telemetry crumb for monitoring
  if (window.gtag) {
    window.gtag('event', 'quirk_profile', {
      'name': window.QuirkProfile.cls[0] || 'auto',
      'reduced': media.reduced
    });
  }
  // Console telemetry for Grafana stream
  console.info('[telemetry] quirk_profile{name="' + (window.QuirkProfile.cls[0] || 'auto') + '"} 1');

  // Add compact FOH toggle
  if (!document.getElementById('quirkBtn')) {
    const btn = document.createElement('button');
    btn.id = 'quirkBtn';
    btn.className = 'hud';
    btn.innerHTML = '⚙️ Quirks';
    btn.style.cssText = `
      position:fixed;top:10px;right:10px;z-index:10000;
      background:rgba(0,0,0,0.8);color:#0f0;border:1px solid #333;
      padding:4px 8px;font:10px ui-monospace;cursor:pointer;
      border-radius:3px;opacity:0.7;transition:opacity 0.2s;
    `;
    document.body.appendChild(btn);

    // Cycle through quirk modes
    const modes = ['auto', 'off', 'mac-safari', 'win-lcd', 'linux-ff', 'ios', 'android', 'edge'];
    let i = modes.indexOf(q.get('quirk') || 'auto');
    if (i === -1) i = 0;

    btn.onclick = () => {
      i = (i + 1) % modes.length;
      const mode = modes[i];
      if (mode === 'auto') {
        const url = new URL(location);
        url.searchParams.delete('quirk');
        location.href = url.toString();
      } else {
        const url = new URL(location);
        url.searchParams.set('quirk', mode);
        location.href = url.toString();
      }
    };

    // Show current mode on hover
    btn.title = `Current: ${modes[i]} (click to cycle)`;
  }

  // Add tiny quirk badge (fades after 2s)
  if (!document.getElementById('quirk-badge')) {
    const badge = document.createElement('div');
    badge.id = 'quirk-badge';
    badge.innerHTML = window.QuirkProfile.cls[0] || 'auto';
    badge.style.cssText = `
      position:fixed;top:8px;right:8px;z-index:10001;
      background:rgba(0,255,0,0.9);color:#000;font:8px ui-monospace;
      padding:2px 4px;border-radius:2px;opacity:1;
      transition:opacity 0.5s ease-out;pointer-events:none;
      text-transform:uppercase;font-weight:bold;
    `;
    document.body.appendChild(badge);

    // Fade out after 2s
    setTimeout(() => {
      badge.style.opacity = '0';
      setTimeout(() => badge.remove(), 500);
    }, 2000);
  }
})();
