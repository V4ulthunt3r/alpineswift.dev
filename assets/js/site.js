// Alpine Swift · alpineswift.dev
// Hero: contour map that morphs from a mountain into an app icon while scrolling.
// Long haul: a flock of alpine swifts that follows the pointer.
// Altimeter: page "altitude" interpolated between sections' data-alt values.
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const lang = document.documentElement.lang || 'de';
  const fmt = n => n.toLocaleString(lang === 'de' ? 'de-DE' : 'en-US');
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const smooth = (a, b, x) => { const t = clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };

  function hash(x, y) {
    let h = (Math.imul(x, 374761393) + Math.imul(y, 668265263)) | 0;
    h = Math.imul(h ^ (h >>> 13), 1274126177);
    return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
  }
  function noise(x, y) {
    const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
    const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
    const a = hash(xi, yi), b = hash(xi + 1, yi), c = hash(xi, yi + 1), d = hash(xi + 1, yi + 1);
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
  }
  function setup(cv) {
    const dpr = Math.min(2, window.devicePixelRatio || 1), r = cv.getBoundingClientRect();
    cv.width = Math.max(1, Math.round(r.width * dpr));
    cv.height = Math.max(1, Math.round(r.height * dpr));
    const ctx = cv.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx, W: r.width, H: r.height };
  }
  // alpine swift silhouette, heading +x; f (0.6..1) is the wing sweep
  function swiftPath(ctx, f) {
    ctx.beginPath();
    ctx.moveTo(7, 0); ctx.quadraticCurveTo(3, -2, 0, -2);
    ctx.quadraticCurveTo(-2, -9 * f, -12, -17 * f); ctx.quadraticCurveTo(-4, -7 * f, -3, -1.5);
    ctx.lineTo(-9, -3); ctx.lineTo(-6, 0); ctx.lineTo(-9, 3); ctx.lineTo(-3, 1.5);
    ctx.quadraticCurveTo(-4, 7 * f, -12, 17 * f); ctx.quadraticCurveTo(-2, 9 * f, 0, 2);
    ctx.quadraticCurveTo(3, 2, 7, 0);
  }
  let colors = {};
  function readColors() {
    const cs = getComputedStyle(document.documentElement);
    for (const k of ['paper', 'ink', 'contour', 'contour-index', 'ice', 'route', 'logo-facet', 'grid', 'zenith', 'sky', 'haze']) colors[k] = cs.getPropertyValue('--' + k).trim();
  }
  readColors();

  /* ---------- Hero topo ---------- */
  const Topo = (() => {
    const hero = document.querySelector('.hero');
    const cv = document.getElementById('topo');
    if (!hero || !cv) return null;
    const hint = hero.querySelector('.hero-hint');
    // marching-squares segments per case; edges: 0 top, 1 right, 2 bottom, 3 left
    const SEG = [[], [3, 2], [2, 1], [3, 1], [0, 1], [3, 0, 2, 1], [0, 2], [3, 0], [3, 0], [0, 2], [0, 1, 3, 2], [0, 1], [3, 1], [2, 1], [3, 2], []];
    const trail = [[.34, 1.03], [.44, .9], [.55, .84], [.48, .76], [.6, .7], [.54, .62], [.64, .56]];
    let ctx, W = 0, H = 0, s, cols, rows, field, t = 0, m = 0, mouse = null, cx = .66;
    // intro: contours appear from the summit down, then the trail draws itself up
    let intro = reduce ? 1 : 0;
    // now and then a single swift crosses the map
    let flight = null, nextFlight = 2600;

    function resize() {
      ({ ctx, W, H } = setup(cv));
      s = Math.max(7, Math.round(W / 150));
      cols = Math.ceil(W / s) + 1;
      rows = Math.ceil(H / s) + 1;
      field = new Float32Array(cols * rows);
      // on narrow screens the peak sits above the copy card instead of beside it
      cx = W < 760 ? .5 : W < 1100 ? .72 : .66;
    }
    function height(u, v) {
      const a = W / H, px = (u - cx) * a, py = v - (W < 760 ? .25 : .44);
      let h = .92 * Math.exp(-(px * px * 1.3 + py * py) / .06)
        + .5 * Math.exp(-((px + .42) ** 2 + (py - .12) ** 2) / .045)
        + .38 * Math.exp(-((px - .3) ** 2 + (py + .2) ** 2) / .03)
        + .24 * Math.exp(-((px + .95) ** 2 + (py + .22) ** 2) / .08)
        + .16 * noise(u * 4 * a + t, v * 4) + .07 * noise(u * 10 * a, v * 10 + t * .5)
        + .09 * (1 - Math.abs(noise(u * 7 * a - t, v * 7) * 2 - 1)) * Math.exp(-(px * px + py * py) / .15);
      if (m > 0) {
        const b = W < 760 ? .15 : W < 1100 ? .27 : .32;
        const dx = Math.abs((u - cx) * a) / b, dy = Math.abs(v - (W < 760 ? .25 : .46)) / b;
        const d = Math.pow(dx ** 5 + dy ** 5, .2);
        const icon = Math.min(.9, Math.max(0, 1.02 - .62 * d)) + .02 * noise(u * 9 * a, v * 9 + t);
        h = h * (1 - m) + icon * m;
      }
      if (mouse) h += .09 * Math.exp(-(((u - mouse.u) * a) ** 2 + (v - mouse.v) ** 2) / .004);
      return h;
    }
    function edge(e, x0, y0, a, b, c, d, L) {
      switch (e) {
        case 0: return [x0 + s * (L - a) / (b - a), y0];
        case 1: return [x0 + s, y0 + s * (L - b) / (c - b)];
        case 2: return [x0 + s * (L - d) / (c - d), y0 + s];
        default: return [x0, y0 + s * (L - a) / (d - a)];
      }
    }
    function draw() {
      if (!W) return;
      let max = -1, mi = 0;
      for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
        const k = j * cols + i, h = height(i * s / W, j * s / H);
        field[k] = h;
        if (h > max) { max = h; mi = k; }
      }
      ctx.fillStyle = colors.paper; ctx.fillRect(0, 0, W, H);
      ctx.strokeStyle = colors.grid; ctx.lineWidth = 1; ctx.beginPath();
      for (let x = 120; x < W; x += 120) { ctx.moveTo(x + .5, 0); ctx.lineTo(x + .5, H); }
      for (let y = 120; y < H; y += 120) { ctx.moveTo(0, y + .5); ctx.lineTo(W, y + .5); }
      ctx.stroke();

      const thin = new Path2D(), idx = new Path2D(), ice = new Path2D(), iceIdx = new Path2D();
      const cut = (1 - intro) ** 3 * (max + .05);
      for (let lv = 1; lv * .05 < 1.25; lv++) {
        const L = lv * .05, p = L > .76 ? (lv % 5 ? ice : iceIdx) : (lv % 5 ? thin : idx);
        if (L < cut) continue;
        for (let j = 0; j < rows - 1; j++) for (let i = 0; i < cols - 1; i++) {
          const k = j * cols + i, a = field[k], b = field[k + 1], c = field[k + cols + 1], d = field[k + cols];
          const cs = (a > L ? 8 : 0) | (b > L ? 4 : 0) | (c > L ? 2 : 0) | (d > L ? 1 : 0);
          if (cs === 0 || cs === 15) continue;
          const sg = SEG[cs], x0 = i * s, y0 = j * s;
          for (let q = 0; q < sg.length; q += 2) {
            const p1 = edge(sg[q], x0, y0, a, b, c, d, L), p2 = edge(sg[q + 1], x0, y0, a, b, c, d, L);
            p.moveTo(p1[0], p1[1]); p.lineTo(p2[0], p2[1]);
          }
        }
      }
      ctx.lineCap = 'round';
      ctx.strokeStyle = colors.contour; ctx.lineWidth = .9; ctx.stroke(thin);
      ctx.strokeStyle = colors['contour-index']; ctx.lineWidth = 1.7; ctx.stroke(idx);
      ctx.globalAlpha = .6; ctx.strokeStyle = colors.ice; ctx.lineWidth = .9; ctx.stroke(ice);
      ctx.globalAlpha = 1; ctx.lineWidth = 1.7; ctx.stroke(iceIdx);

      const px = (mi % cols) * s, py = Math.floor(mi / cols) * s;
      const ta = 1 - smooth(0, .45, m), tp = smooth(.45, 1, intro);
      if (ta > .01 && tp > 0) {
        const sx = cx - .66, pts = trail.map(([u, v]) => [(u + sx) * W, v * H]).concat([[px, py]]);
        ctx.save(); ctx.globalAlpha = ta; ctx.lineJoin = 'round';
        partial(pts, tp);
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 6; ctx.stroke();
        ctx.strokeStyle = colors['logo-facet']; ctx.setLineDash([12, 12]); ctx.stroke();
        ctx.restore();
      }
      ctx.setLineDash([]);
      ctx.save();
      ctx.globalAlpha = smooth(.8, 1, intro);
      ctx.fillStyle = colors.ink;
      ctx.beginPath(); ctx.moveTo(px, py - 8); ctx.lineTo(px + 7, py + 5); ctx.lineTo(px - 7, py + 5); ctx.closePath(); ctx.fill();
      ctx.font = '600 11px "Spline Sans Mono", ui-monospace, monospace';
      // the hero summit is the same summit as the contact section (data-alt of the last stop)
      const label = m < .5 ? `${cv.dataset.peak}  ${fmt(summitAlt)} m` : cv.dataset.icon;
      const lw = ctx.measureText(label).width;
      ctx.fillText(label, px + 12 + lw > W - 8 ? px - 12 - lw : px + 12, py + 4);
      ctx.restore();

      if (flight) {
        const p = flight.t / flight.dur, q = 1 - p, [a, c, b] = flight.pts;
        const x = q * q * a[0] + 2 * q * p * c[0] + p * p * b[0], y = q * q * a[1] + 2 * q * p * c[1] + p * p * b[1];
        const dx = 2 * q * (c[0] - a[0]) + 2 * p * (b[0] - c[0]), dy = 2 * q * (c[1] - a[1]) + 2 * p * (b[1] - c[1]);
        const f = .8 + .2 * Math.sin(flight.ph) * (Math.sin(flight.ph * .11) > 0 ? 1 : .1);
        for (const shadow of [true, false]) {
          ctx.save();
          ctx.translate(x + (shadow ? 22 : 0), y + (shadow ? 30 : 0));
          ctx.rotate(Math.atan2(dy, dx)); ctx.scale(1.6, 1.6);
          ctx.globalAlpha = shadow ? .13 : 1;
          ctx.fillStyle = colors.ink;
          swiftPath(ctx, f); ctx.fill();
          ctx.restore();
        }
      }
    }
    function partial(pts, f) {
      const seg = [];
      let total = 0;
      for (let i = 0; i < pts.length - 1; i++) { const d = Math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]); seg.push(d); total += d; }
      let left = total * f;
      ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
      for (let i = 0; i < seg.length; i++) {
        if (left >= seg[i]) { ctx.lineTo(pts[i + 1][0], pts[i + 1][1]); left -= seg[i]; continue; }
        const k = left / seg[i];
        ctx.lineTo(pts[i][0] + (pts[i + 1][0] - pts[i][0]) * k, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * k);
        break;
      }
    }
    function fly(dt) {
      if (flight) {
        flight.t += dt; flight.ph += dt * .012;
        if (flight.t >= flight.dur) { flight = null; nextFlight = 9000 + Math.random() * 9000; }
        return;
      }
      if (intro < 1 || (nextFlight -= dt) > 0) return;
      const dir = Math.random() < .5 ? 1 : -1, y0 = H * (.15 + Math.random() * .45), y1 = H * (.15 + Math.random() * .45);
      flight = {
        t: 0, ph: 0, dur: 4200 + Math.random() * 1800,
        pts: [[dir > 0 ? -60 : W + 60, y0], [W * (.3 + Math.random() * .4), Math.min(y0, y1) - H * .2 * Math.random()], [dir > 0 ? W + 60 : -60, y1]]
      };
    }
    const stops = document.querySelectorAll('[data-alt]');
    const summitAlt = stops.length ? +stops[stops.length - 1].dataset.alt : 2962;
    function progress() {
      const r = hero.getBoundingClientRect(), span = r.height - innerHeight;
      return span > 0 ? clamp(-r.top / span, 0, 1) : 0;
    }
    function frame(dt) {
      const p = progress();
      m = smooth(.12, .8, p);
      if (hint) hint.style.opacity = p > .05 ? 0 : 1;
      intro = Math.min(1, intro + dt / 2200);
      fly(dt);
      t += dt * .00004;
      draw();
    }
    hero.addEventListener('pointermove', e => {
      if (e.pointerType !== 'mouse') return;
      const r = cv.getBoundingClientRect();
      mouse = { u: (e.clientX - r.left) / r.width, v: (e.clientY - r.top) / r.height };
      if (reduce) draw();
    });
    hero.addEventListener('pointerleave', () => { mouse = null; if (reduce) draw(); });
    return { el: hero, resize, frame, draw };
  })();

  /* ---------- Long haul flock ---------- */
  const Sky = (() => {
    const band = document.querySelector('.longhaul');
    const cv = document.getElementById('sky');
    if (!band || !cv) return null;
    const daysEl = document.getElementById('days');
    let ctx, W = 0, H = 0, birds = [], ridges = [], mouse = null, t = 0, days = reduce ? 200 : 0;

    function resize() {
      ({ ctx, W, H } = setup(cv));
      ridges = [0, 1, 2].map(L => {
        const pts = [], base = H * (.8 + L * .07), amp = H * (.22 - L * .05);
        for (let x = 0; x <= W + 8; x += 6) {
          const n = noise(x * .0035 * (1 + L * .5) + L * 17, L * 5.3);
          const r = 1 - Math.abs(noise(x * .011 + L * 9, 2 + L) * 2 - 1);
          pts.push(base - amp * (.72 * n + .28 * r));
        }
        return pts;
      });
      if (!birds.length) {
        const n = W < 640 ? 20 : 36;
        for (let i = 0; i < n; i++) {
          const a = Math.random() * Math.PI * 2;
          birds.push({
            x: W * (.3 + Math.random() * .6), y: H * (.12 + Math.random() * .3),
            vx: Math.cos(a) * 2, vy: Math.sin(a) * 2, z: .35 + Math.random() * .65,
            ph: Math.random() * 9, orb: 50 + Math.random() * 170, w: .6 + Math.random() * .9, o: Math.random() * 6.3
          });
        }
        birds.sort((a, b) => a.z - b.z);
      }
    }
    function bird(b) {
      const sc = .5 + .55 * b.z, f = .78 + .22 * Math.sin(b.ph) * (Math.sin(b.ph * .13) > 0 ? 1 : .15);
      const c = 1 - b.z;
      ctx.save();
      ctx.translate(b.x, b.y); ctx.rotate(Math.atan2(b.vy, b.vx)); ctx.scale(sc, sc);
      // white like the logo's swift; distant birds fade into the violet haze
      ctx.fillStyle = `rgba(${255 - c * 40 | 0},${255 - c * 50 | 0},255,${(.5 + .5 * b.z).toFixed(2)})`;
      swiftPath(ctx, f);
      ctx.fill();
      ctx.restore();
    }
    function draw() {
      if (!W) return;
      const g = ctx.createLinearGradient(0, 0, 0, H);
      g.addColorStop(0, colors.zenith); g.addColorStop(.55, colors.sky); g.addColorStop(.92, colors.haze);
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      const sun = ctx.createRadialGradient(W * .85, H * .72, 0, W * .85, H * .72, H * .6);
      sun.addColorStop(0, 'rgba(20,240,220,.22)'); sun.addColorStop(1, 'rgba(20,240,220,0)');
      ctx.fillStyle = sun; ctx.fillRect(0, 0, W, H);
      const shades = ['rgba(150,118,232,.85)', 'rgba(72,40,160,.95)', 'rgba(17,6,56,1)'];
      ridges.forEach((pts, L) => {
        ctx.fillStyle = shades[L]; ctx.beginPath(); ctx.moveTo(0, H);
        pts.forEach((y, i) => ctx.lineTo(i * 6, y));
        ctx.lineTo(W, H); ctx.closePath(); ctx.fill();
      });
      birds.forEach(bird);
    }
    function frame(dt) {
      t += dt;
      const k = dt / 16.7;
      const tx = mouse ? mouse.x : W * (.6 + .25 * Math.sin(t * .00021));
      const ty = mouse ? mouse.y : H * (.22 + .1 * Math.sin(t * .00037 + 1));
      for (const b of birds) {
        let sx = 0, sy = 0, ax = 0, ay = 0, n = 0;
        for (const o of birds) {
          if (o === b) continue;
          const dx = b.x - o.x, dy = b.y - o.y, d2 = dx * dx + dy * dy;
          if (d2 < 900) { sx += dx / (d2 + 1) * 30; sy += dy / (d2 + 1) * 30; }
          if (d2 < 4900) { ax += o.vx; ay += o.vy; n++; }
        }
        const a = t * .0011 * b.w + b.o;
        const dx = tx + Math.cos(a) * b.orb - b.x, dy = ty + Math.sin(a) * b.orb * .45 - b.y;
        const dist = Math.hypot(dx, dy) || 1, max = 2.1 + 1.6 * b.z;
        let fx = (dx / dist * max - b.vx) * .045 + sx * .5, fy = (dy / dist * max - b.vy) * .045 + sy * .5;
        if (n) { fx += (ax / n - b.vx) * .04; fy += (ay / n - b.vy) * .04; }
        b.vx += fx * k; b.vy += fy * k;
        const sp = Math.hypot(b.vx, b.vy) || 1, cl = clamp(sp, max * .55, max);
        b.vx *= cl / sp; b.vy *= cl / sp;
        b.x += b.vx * k; b.y += b.vy * k;
        b.ph += (.2 + .12 * b.z) * k;
      }
      if (days < 200 && daysEl) { days = Math.min(200, days + dt / 18); daysEl.textContent = Math.floor(days); }
      draw();
    }
    const setMouse = e => { const r = cv.getBoundingClientRect(); mouse = { x: e.clientX - r.left, y: e.clientY - r.top }; };
    band.addEventListener('pointermove', e => { if (e.pointerType === 'mouse') setMouse(e); });
    band.addEventListener('pointerdown', setMouse);
    band.addEventListener('pointerleave', () => { mouse = null; });
    band.addEventListener('pointerup', e => { if (e.pointerType !== 'mouse') mouse = null; });
    if (daysEl && !reduce) daysEl.textContent = '0';
    return { el: band, resize, frame, draw };
  })();


  /* ---------- Summit logo: the swift flies in once, then glides ---------- */
  (() => {
    const svg = document.querySelector('[data-logo-anim]');
    if (!svg || reduce || !('IntersectionObserver' in window)) return;
    const clipR = svg.querySelector('.la-clip'), mtn = svg.querySelector('.la-mtn'), facet = svg.querySelector('.la-facet');
    const glint = svg.querySelector('.la-glint'), bird = svg.querySelector('.la-bird'), wing = svg.querySelector('.la-wing');
    const END = 2300, CX = 891, CY = 465, HEADING = -25, BX = [-1050, -700, -260, 0], BY = [300, 700, 120, 0];
    let t = 0, idleT = 0, playing = false, seen = false, vis = false, raf = 0, last = 0;
    const seg = (a, b) => clamp((t - a) / (b - a), 0, 1);
    const outCubic = x => 1 - (1 - x) ** 3, outQuint = x => 1 - (1 - x) ** 5;
    const outBack = x => 1 + 2.5 * (x - 1) ** 3 + 1.5 * (x - 1) ** 2;
    const bez = (p, x) => { const u = 1 - x; return u * u * u * p[0] + 3 * u * u * x * p[1] + 3 * u * x * x * p[2] + x * x * x * p[3]; };
    const bezD = (p, x) => { const u = 1 - x; return 3 * u * u * (p[1] - p[0]) + 6 * u * x * (p[2] - p[1]) + 3 * x * x * (p[3] - p[2]); };
    function render() {
      const m = outCubic(seg(0, 900));
      clipR.setAttribute('y', 1100 - 540 * m);
      mtn.setAttribute('transform', `translate(0 ${(36 * (1 - m)).toFixed(1)})`);
      const f = seg(600, 1100);
      facet.setAttribute('transform', `translate(665 740) scale(${outBack(f).toFixed(3)}) translate(-665 -740)`);
      const g = seg(700, 1500);
      glint.setAttribute('stroke-dashoffset', 150 - 1500 * outCubic(g));
      glint.setAttribute('opacity', g > 0 && g < 1 ? Math.sin(Math.PI * g).toFixed(3) : 0);
      const bRaw = seg(600, END), b = outQuint(bRaw);
      const ang = Math.atan2(bezD(BY, b), bezD(BX, b)) * 180 / Math.PI;
      const rot = (ang - HEADING) * (1 - clamp((bRaw - .82) / .18, 0, 1));
      const sc = .55 + .45 * b, flick = 1 + .07 * Math.sin(t / 34) * (1 - b);
      let ix = 0, iy = 0, ir = 0;
      if (t >= END) { iy = -7 * Math.sin(idleT * 1.2); ir = 1.6 * Math.sin(idleT * 1.2 + .7); ix = 3 * Math.sin(idleT * .6); }
      bird.setAttribute('transform', `translate(${(bez(BX, b) + ix).toFixed(1)} ${(bez(BY, b) + iy).toFixed(1)}) rotate(${(rot + ir).toFixed(2)} ${CX} ${CY}) translate(${CX} ${CY}) scale(${(sc * flick).toFixed(3)} ${sc.toFixed(3)}) translate(${-CX} ${-CY})`);
      bird.setAttribute('opacity', Math.min(1, bRaw * 8));
      // the wing facet catches the light once the swift has landed, an echo of the glacier
      const w = seg(1950, 2300);
      wing.setAttribute('opacity', w.toFixed(3));
    }
    function tick(now) {
      const dt = last ? Math.min(64, now - last) : 16;
      last = now;
      if (playing) { t += dt; if (t >= END) { t = END; playing = false; } } else idleT += dt / 1000;
      render();
      raf = vis ? requestAnimationFrame(tick) : 0;
      if (!raf) last = 0;
    }
    render(); // start hidden until the summit comes into view
    new IntersectionObserver(es => es.forEach(e => {
      vis = e.isIntersecting;
      if (vis && !seen) { seen = true; t = 0; playing = true; }
      if (vis && !raf) raf = requestAnimationFrame(tick);
    }), { threshold: .35 }).observe(svg);
  })();

  /* ---------- Render loop: only animate what is on screen ---------- */
  const scenes = [Topo, Sky].filter(Boolean);  const visible = new Set();
  const io = new IntersectionObserver(es => es.forEach(e => {
    const sc = scenes.find(x => x.el === e.target);
    if (e.isIntersecting) visible.add(sc); else visible.delete(sc);
  }));
  scenes.forEach(sc => { sc.resize(); sc.draw(); io.observe(sc.el); });

  let rz;
  addEventListener('resize', () => {
    clearTimeout(rz);
    rz = setTimeout(() => scenes.forEach(sc => { sc.resize(); sc.draw(); }), 120);
  });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => { readColors(); scenes.forEach(sc => sc.draw()); });
  document.fonts && document.fonts.ready.then(() => Topo && Topo.draw());

  if (!reduce) {
    let last = performance.now();
    const loop = now => {
      const dt = Math.min(50, now - last);
      last = now;
      if (!document.hidden) visible.forEach(sc => sc.frame(dt));
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  /* ---------- Altimeter ---------- */
  const alti = document.querySelector('.altimeter');
  const stops = [...document.querySelectorAll('[data-alt]')];
  function updateAlti() {
    if (!alti || !stops.length) return;
    const y = scrollY + innerHeight * .5, tops = stops.map(el => el.getBoundingClientRect().top + scrollY);
    const atBottom = scrollY + innerHeight >= document.documentElement.scrollHeight - 4;
    let alt = +stops[0].dataset.alt;
    if (atBottom) alt = +stops[stops.length - 1].dataset.alt;
    else for (let i = 0; i < stops.length; i++) {
      if (y < tops[i]) break;
      const a = +stops[i].dataset.alt, next = stops[i + 1];
      alt = next ? a + (+next.dataset.alt - a) * clamp((y - tops[i]) / (tops[i + 1] - tops[i]), 0, 1) : a;
    }
    const lo = +stops[0].dataset.alt, hi = +stops[stops.length - 1].dataset.alt;
    alti.querySelector('b').textContent = fmt(Math.round(alt / 10) * 10);
    // hide over the footer, and on phones while the hero card (with its buttons) fills the screen
    const foot = document.querySelector('.site-footer');
    const inHero = innerWidth < 560 && Topo && Topo.el.getBoundingClientRect().bottom > innerHeight;
    alti.classList.toggle('away', (!!foot && foot.getBoundingClientRect().top < innerHeight) || !!inHero);
    alti.style.setProperty('--p', ((alt - lo) / (hi - lo) * 100).toFixed(1) + '%');
  }

  /* ---------- Header, nav, copy ---------- */
  const header = document.querySelector('.site-header');
  const navLinks = [...document.querySelectorAll('.nav a[href^="#"]')];
  function onScroll() {
    if (header) header.classList.toggle('scrolled', scrollY > 8);
    updateAlti();
    let current = null;
    for (const a of navLinks) {
      const sec = document.querySelector(a.getAttribute('href'));
      if (sec && sec.getBoundingClientRect().top < innerHeight * .4) current = a;
    }
    navLinks.forEach(a => a.setAttribute('aria-current', a === current ? 'true' : 'false'));
  }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const menuBtn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open);
    });
    nav.addEventListener('click', e => {
      if (e.target.closest('a')) { nav.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); }
    });
  }

  document.querySelectorAll('[data-copy]').forEach(btn => btn.addEventListener('click', async () => {
    const label = btn.querySelector('span'), orig = label.textContent;
    try { await navigator.clipboard.writeText(btn.dataset.copy); label.textContent = btn.dataset.done; }
    catch (e) { label.textContent = btn.dataset.copy; }
    setTimeout(() => { label.textContent = orig; }, 2200);
  }));

  /* ---------- Project filter ---------- */
  const filterBtns = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('.project[data-kind]')];
  filterBtns.forEach(btn => {
    const k = btn.dataset.filter, n = k === 'all' ? cards.length : cards.filter(c => c.dataset.kind === k).length;
    const count = btn.querySelector('small');
    if (count) count.textContent = n;
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.setAttribute('aria-pressed', b === btn));
      cards.forEach(c => {
        const show = k === 'all' || c.dataset.kind === k;
        c.classList.remove('enter');
        c.hidden = !show;
        if (show && !reduce) { void c.offsetWidth; c.classList.add('enter'); }
      });
    });
  });

  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
})();
