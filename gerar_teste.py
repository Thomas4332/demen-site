"""Gera teste/index.html (versão com efeitos e 3D) a partir do index.html principal."""
from pathlib import Path

RAIZ = Path(__file__).parent
s = (RAIZ / "index.html").read_text(encoding="utf-8")

def troca(a, b, n=1):
    global s
    assert s.count(a) >= 1, f"não achei: {a[:60]}"
    s = s.replace(a, b) if n == 0 else s.replace(a, b, n)

# 1) caminhos relativos (a página fica numa subpasta)
for pasta in ("img/", "marcas/", "fotos/", "catalogos/"):
    s = s.replace(f'"{pasta}', f'"../{pasta}')

# 2) título e não indexar a página de teste
troca("<title>DE men | Moda Masculina Premium — Sertânia-PE</title>",
      "<title>DE men | Versão com efeitos (teste)</title>\n<meta name=\"robots\" content=\"noindex\">")

# 3) CSS dos efeitos
CSS = r"""
  /* ================= EFEITOS (versão teste) ================= */
  html.lenis, html.lenis body{height:auto}
  .lenis.lenis-smooth{scroll-behavior:auto !important}
  #intro{position:fixed;inset:0;z-index:300;background:var(--preto);display:grid;place-items:center;transition:opacity .9s ease,visibility .9s}
  #intro img{width:110px;animation:pulsa 1.8s ease-in-out infinite}
  #intro .barra{position:absolute;left:50%;bottom:22%;width:170px;height:1px;background:#2a2a2a;transform:translateX(-50%);overflow:hidden}
  #intro .barra i{display:block;height:100%;width:0;background:var(--areia);transition:width .35s ease}
  body.carregado #intro{opacity:0;visibility:hidden}
  @keyframes pulsa{50%{opacity:.55;transform:scale(.96)}}
  #progresso{position:fixed;top:0;left:0;height:2px;width:0;background:linear-gradient(90deg,var(--areia),#fff);z-index:130}
  .cursor-dot,.cursor-ring{position:fixed;top:0;left:0;pointer-events:none;z-index:250;border-radius:50%;transform:translate3d(-100px,-100px,0)}
  .cursor-dot{width:6px;height:6px;margin:-3px 0 0 -3px;background:var(--areia)}
  .cursor-ring{width:38px;height:38px;margin:-19px 0 0 -19px;border:1px solid rgba(200,180,138,.55);transition:width .25s,height .25s,margin .25s,background .25s}
  .cursor-ring.grande{width:72px;height:72px;margin:-36px 0 0 -36px;background:rgba(200,180,138,.08)}
  @media (hover:none){.cursor-dot,.cursor-ring{display:none}}
  .hero{isolation:isolate}
  #particulas{position:absolute;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}
  .hero .brilho{position:absolute;z-index:0;width:700px;height:700px;border-radius:50%;pointer-events:none;
    background:radial-gradient(circle,rgba(200,180,138,.13),transparent 62%);left:var(--mx,72%);top:var(--my,42%);transform:translate(-50%,-50%);transition:left .6s ease-out,top .6s ease-out}
  .hero .wrap{position:relative;z-index:1}
  .hero-3d{position:relative;width:100%;max-width:520px;aspect-ratio:1/1;justify-self:center;align-self:center}
  .hero-3d canvas{position:absolute;inset:0;width:100% !important;height:100% !important;display:block;cursor:grab;touch-action:pan-y}
  .hero-3d canvas:active{cursor:grabbing}
  .hero-3d .hero-logo{position:absolute;inset:0;margin:auto !important;width:78% !important}
  .hero-3d.ativo .hero-logo{display:none}
  .hero-3d .legenda{position:absolute;left:0;right:0;bottom:4%;text-align:center;font-size:.68rem;letter-spacing:.5em;color:#9b9488;opacity:0;transition:opacity 1s}
  .hero-3d.ativo .legenda{opacity:1}
  .hero-3d::after{content:"";position:absolute;left:18%;right:18%;bottom:9%;height:22px;border-radius:50%;background:radial-gradient(ellipse,rgba(200,180,138,.25),transparent 70%);filter:blur(6px)}
  .palavra{display:inline-block;overflow:hidden;vertical-align:top;padding-bottom:.08em}
  .palavra>span{display:inline-block;transform:translateY(110%)}
  .faixa{overflow:hidden;border-block:1px solid var(--linha);padding:1.3rem 0;background:var(--grafite)}
  .faixa-trilho{display:flex;gap:3.5rem;width:max-content;align-items:center;animation:desliza 32s linear infinite}
  .faixa:hover .faixa-trilho{animation-play-state:paused}
  .faixa-trilho span{font-family:var(--serif);font-size:1.55rem;letter-spacing:.14em;white-space:nowrap;color:#c9c2b6}
  .faixa-trilho i{color:var(--areia);font-style:normal;font-size:1rem}
  @keyframes desliza{to{transform:translateX(-50%)}}
  .numeros-sec{padding:4.5rem 0 0}
  .numeros{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--linha);border:1px solid var(--linha)}
  .numeros div{background:var(--preto);padding:2.3rem 1rem;text-align:center}
  .numeros b{display:block;font-family:var(--serif);font-size:clamp(2.2rem,4vw,3.4rem);font-weight:500;line-height:1.1}
  .numeros small{font-size:.68rem;letter-spacing:.22em;text-transform:uppercase;color:var(--cinza)}
  .grade,.marcas-grade,.cat-grade{perspective:1200px}
  .card,.cat-card,.marca-cel{transform-style:preserve-3d;transition:transform .18s ease-out,border-color .25s,background .25s;will-change:transform;position:relative}
  .brilho-card{position:absolute;inset:0;pointer-events:none;z-index:3;opacity:0;transition:opacity .3s;
    background:radial-gradient(circle at var(--gx,50%) var(--gy,50%),rgba(255,255,255,.16),transparent 45%)}
  .card:hover .brilho-card,.cat-card:hover .brilho-card,.marca-cel:hover .brilho-card{opacity:1}
  .card .foto img{transition:transform .9s cubic-bezier(.2,.7,.2,1)}
  .card:hover .foto img{transform:scale(1.08)}
  .card:hover{transform:none}
  .btn{will-change:transform;transition:background .2s,color .2s,transform .25s cubic-bezier(.2,.7,.2,1)}
  h2 .linha-ouro{display:block;width:0;height:1px;margin-top:.9rem;background:var(--areia);transition:width 1.2s cubic-bezier(.2,.7,.2,1)}
  h2.desenhada .linha-ouro{width:64px}
  .teste-selo{position:fixed;left:200px;top:24px;z-index:60;font-size:.58rem;letter-spacing:.2em;text-transform:uppercase;background:rgba(200,180,138,.12);color:var(--areia);border:1px solid rgba(200,180,138,.35);padding:.3rem .55rem;pointer-events:none}
  @media (max-width:860px){.teste-selo{display:none}}
  @media (max-width:860px){
    .hero-3d{max-width:250px;justify-self:start;grid-row:1;margin-top:4.5rem}
    .numeros{grid-template-columns:repeat(2,1fr)}
    .hero .brilho{width:420px;height:420px}
  }
  @media (prefers-reduced-motion: reduce){
    .faixa-trilho{animation:none}
    .palavra>span{transform:none}
  }
"""
troca("</style>\n</head>", CSS + "</style>\n</head>")

# 4) intro, barra de progresso, cursor
troca("<body>\n", """<body>
<div id="intro" aria-hidden="true"><img src="../img/monograma.svg" alt=""><div class="barra"><i></i></div></div>
<div id="progresso"></div>
<div class="cursor-dot"></div><div class="cursor-ring"></div>
<div class="teste-selo">Teste</div>
""")

# 5) capa: partículas, brilho que segue o mouse e logo 3D
troca('<section class="hero" id="inicio">\n    <div class="wrap">',
      '<section class="hero" id="inicio">\n    <canvas id="particulas"></canvas><div class="brilho"></div>\n    <div class="wrap">')
troca('<img src="../img/logo.svg" alt="Logo DE men" class="hero-logo">',
      '<div class="hero-3d" id="hero3d"><img src="../img/logo.svg" alt="Logo DE men" class="hero-logo"><div class="legenda">DE&nbsp;MEN</div></div>')

# 6) faixa deslizante + números, logo depois da capa
itens = ["CALVIN KLEIN", "RESERVA", "ADIDAS", "OGOCHI", "100% ORIGINAIS", "REVENDA AUTORIZADA", "ENVIAMOS PARA TODO O BRASIL"]
trilho = "".join(f"<span>{t}</span><i>✦</i>" for t in itens) * 2
troca('  <section class="marcas" id="marcas">', f'''  <div class="faixa" aria-hidden="true"><div class="faixa-trilho">{trilho}</div></div>

  <section class="numeros-sec">
    <div class="wrap numeros">
      <div><b data-conta="4">4</b><small>Marcas oficiais</small></div>
      <div><b data-conta="100" data-suf="%">100%</b><small>Peças originais</small></div>
      <div><b data-conta="3400" data-suf="+">3.400+</b><small>Seguidores no Instagram</small></div>
      <div><b data-conta="0" id="numPecas">—</b><small>Peças na vitrine</small></div>
    </div>
  </section>

  <section class="marcas" id="marcas">''')

# 7) bibliotecas (GSAP, ScrollTrigger, Lenis) + efeitos + 3D
JS = r"""
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.7/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.7/dist/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.18/dist/lenis.min.js"></script>
<script>
/* ================= EFEITOS ================= */
(() => {
  const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const toque = matchMedia('(hover: none)').matches;
  const temGsap = !!window.gsap;
  if (temGsap && window.ScrollTrigger) gsap.registerPlugin(ScrollTrigger);

  // número de peças na vitrine
  const np = document.getElementById('numPecas');
  if (np) { np.dataset.conta = PRODUTOS.length; np.textContent = PRODUTOS.length; }

  /* ---- título palavra por palavra ---- */
  const h1 = document.querySelector('.hero h1');
  (function quebra(el){
    [...el.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const f = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(w => {
          if (!w) return;
          if (/^\s+$/.test(w)) { f.appendChild(document.createTextNode(w)); return; }
          const o = document.createElement('span'); o.className = 'palavra';
          const i = document.createElement('span'); i.textContent = w; o.appendChild(i); f.appendChild(o);
        });
        n.replaceWith(f);
      } else if (n.nodeType === 1) quebra(n);
    });
  })(h1);

  /* ---- intro ---- */
  const barra = document.querySelector('#intro .barra i');
  let p = 0; const tk = setInterval(() => { p = Math.min(92, p + Math.random() * 22); barra.style.width = p + '%'; }, 160);
  let feito = false;
  function pronto(){
    if (feito) return; feito = true; clearInterval(tk); barra.style.width = '100%';
    setTimeout(() => { document.body.classList.add('carregado'); animaCapa(); }, 380);
  }
  addEventListener('load', pronto); setTimeout(pronto, 3500);

  function animaCapa(){
    if (!temGsap || reduz) { document.querySelectorAll('.palavra>span').forEach(s => s.style.transform = 'none'); return; }
    gsap.to('.palavra>span', { y: 0, duration: 1.15, ease: 'power4.out', stagger: .06 });
    gsap.from(['.hero .eyebrow', '.hero p', '.hero .acoes', '.hero .selos'], { opacity: 0, y: 30, duration: 1, ease: 'power3.out', stagger: .12, delay: .35 });
    gsap.from('#hero3d', { opacity: 0, scale: .75, duration: 1.8, ease: 'power3.out', delay: .15 });
  }

  /* ---- rolagem suave (Lenis) ---- */
  let lenis = null;
  if (window.Lenis && !reduz && !toque) {
    lenis = new Lenis({ lerp: .09, smoothWheel: true });
    if (window.ScrollTrigger) { lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
    else { const raf = t => { lenis.raf(t); requestAnimationFrame(raf); }; requestAnimationFrame(raf); }
    document.addEventListener('click', e => {
      const a = e.target.closest('a[href^="#"]'); if (!a) return;
      const id = a.getAttribute('href'); if (id.length < 2 || !document.querySelector(id)) return;
      e.preventDefault(); lenis.scrollTo(id, { offset: -70 });
    });
    const nativo = Element.prototype.scrollIntoView;
    Element.prototype.scrollIntoView = function(){ try { lenis.scrollTo(this, { offset: -70 }); } catch(_) { nativo.call(this); } };
  }

  /* ---- barra de progresso ---- */
  const prog = document.getElementById('progresso');
  const atualizaProg = () => { const h = document.documentElement.scrollHeight - innerHeight; prog.style.width = (h > 0 ? scrollY / h * 100 : 0) + '%'; };
  addEventListener('scroll', atualizaProg, { passive: true }); atualizaProg();

  /* ---- cursor personalizado ---- */
  if (!toque) {
    const dot = document.querySelector('.cursor-dot'), ring = document.querySelector('.cursor-ring');
    let mx = -100, my = -100, rx = -100, ry = -100;
    addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; dot.style.transform = `translate3d(${mx}px,${my}px,0)`; });
    (function loop(){ rx += (mx - rx) * .18; ry += (my - ry) * .18; ring.style.transform = `translate3d(${rx}px,${ry}px,0)`; requestAnimationFrame(loop); })();
    document.addEventListener('mouseover', e => { ring.classList.toggle('grande', !!e.target.closest('a,button,.card,.cat-card,.marca-cel,.chip,canvas')); });
  }

  /* ---- brilho dourado seguindo o mouse na capa ---- */
  const hero = document.querySelector('.hero');
  hero.addEventListener('mousemove', e => { const r = hero.getBoundingClientRect(); hero.style.setProperty('--mx', (e.clientX - r.left) + 'px'); hero.style.setProperty('--my', (e.clientY - r.top) + 'px'); });

  /* ---- partículas douradas na capa ---- */
  (function particulas(){
    const cv = document.getElementById('particulas'); if (!cv || reduz) return;
    const ctx = cv.getContext('2d'); let W, H, pts = [], visivel = true, px = 0, py = 0;
    const N = innerWidth < 860 ? 35 : 80, dpr = Math.min(devicePixelRatio, 2);
    function tam(){ W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr,0,0,dpr,0,0); }
    tam(); addEventListener('resize', tam);
    for (let i = 0; i < N; i++) pts.push({ x: Math.random() * W, y: Math.random() * H, r: Math.random() * 1.6 + .3, v: Math.random() * .35 + .08, a: Math.random() * .6 + .15, z: Math.random() * 1 + .3 });
    hero.addEventListener('mousemove', e => { px = (e.clientX / innerWidth - .5); py = (e.clientY / innerHeight - .5); });
    new IntersectionObserver(([en]) => visivel = en.isIntersecting).observe(hero);
    (function anda(){
      if (visivel) {
        ctx.clearRect(0, 0, W, H);
        for (const q of pts) {
          q.y -= q.v; if (q.y < -5) { q.y = H + 5; q.x = Math.random() * W; }
          ctx.beginPath(); ctx.arc(q.x - px * 30 * q.z, q.y - py * 20 * q.z, q.r, 0, 7);
          ctx.fillStyle = `rgba(200,180,138,${q.a})`; ctx.fill();
        }
      }
      requestAnimationFrame(anda);
    })();
  })();

  /* ---- inclinação 3D + brilho nos cards ---- */
  if (!toque && !reduz) {
    const SEL = '.card,.cat-card,.marca-cel';
    document.addEventListener('mousemove', e => {
      const c = e.target.closest(SEL); if (!c) return;
      const r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      const forca = c.classList.contains('marca-cel') ? 8 : 10;
      c.style.transform = `rotateY(${(x - .5) * forca}deg) rotateX(${(.5 - y) * forca}deg)`;
      c.style.setProperty('--gx', x * 100 + '%'); c.style.setProperty('--gy', y * 100 + '%');
      if (!c.querySelector(':scope > .brilho-card')) { const b = document.createElement('div'); b.className = 'brilho-card'; c.appendChild(b); }
    });
    document.addEventListener('mouseout', e => { const c = e.target.closest(SEL); if (c && !c.contains(e.relatedTarget)) c.style.transform = ''; });
  }

  /* ---- botões magnéticos ---- */
  if (!toque && !reduz) {
    document.addEventListener('mousemove', e => {
      const b = e.target.closest('.btn,.bot-botao'); if (!b) return;
      const r = b.getBoundingClientRect(), dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
      b.style.transform = `translate(${dx * .22}px,${dy * .3}px)`;
    });
    document.addEventListener('mouseout', e => { const b = e.target.closest('.btn,.bot-botao'); if (b && !b.contains(e.relatedTarget)) b.style.transform = ''; });
  }

  /* ---- animações ao rolar ---- */
  document.querySelectorAll('section h2').forEach(h => { const l = document.createElement('span'); l.className = 'linha-ouro'; h.appendChild(l); });
  const ioH2 = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('desenhada'); ioH2.unobserve(en.target); } }), { threshold: .6 });
  document.querySelectorAll('section h2').forEach(h => ioH2.observe(h));

  if (temGsap && window.ScrollTrigger && !reduz) {
    // parallax da capa
    gsap.to('.hero .wrap > div:first-child', { yPercent: -16, opacity: .25, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to('#hero3d', { yPercent: 22, scale: .82, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
    // contadores
    document.querySelectorAll('[data-conta]').forEach(el => {
      const fim = +el.dataset.conta, suf = el.dataset.suf || '', o = { v: 0 };
      el.textContent = '0' + suf;
      ScrollTrigger.create({ trigger: el, start: 'top 92%', once: true, onEnter: () =>
        gsap.to(o, { v: fim, duration: 2.2, ease: 'power2.out', onUpdate: () => el.textContent = Math.round(o.v).toLocaleString('pt-BR') + suf }) });
    });
    // marcas e catálogos
    gsap.fromTo('#marcasGrade', { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)', duration: 1.2, ease: 'power4.out', scrollTrigger: { trigger: '#marcasGrade', start: 'top 88%' } });
    gsap.fromTo('.marca-cel > *', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .9, stagger: .08, delay: .3, ease: 'power3.out', clearProps: 'opacity,transform', scrollTrigger: { trigger: '#marcasGrade', start: 'top 88%' } });
    document.querySelectorAll('.cat-card,.galeria .foto').forEach(e => e.classList.remove('revelar'));
    gsap.fromTo('.cat-card', { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 1, stagger: .1, ease: 'power3.out', clearProps: 'opacity,transform', scrollTrigger: { trigger: '#catGrade', start: 'top 88%' } });
    gsap.fromTo('.numeros > div > *', { opacity: 0, y: 25 }, { opacity: 1, y: 0, duration: .9, stagger: .06, ease: 'power3.out', clearProps: 'opacity,transform', scrollTrigger: { trigger: '.numeros', start: 'top 90%' } });
    gsap.fromTo('.galeria .foto', { opacity: 0, scale: .85 }, { opacity: 1, scale: 1, duration: .9, stagger: .07, ease: 'power3.out', clearProps: 'opacity,transform', scrollTrigger: { trigger: '#galeria', start: 'top 88%' } });

    // cards da vitrine: revelam a foto de baixo pra cima (inclusive depois de filtrar)
    const grade = document.getElementById('grade');
    const animaCards = () => {
      const cards = grade.querySelectorAll('.card:not(.animado)');
      cards.forEach(c => c.classList.add('animado'));
      ScrollTrigger.batch(cards, { start: 'top 92%', once: true, onEnter: lote => {
        gsap.fromTo(lote, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: .9, stagger: .08, ease: 'power3.out' });
        gsap.fromTo(lote.map(c => c.querySelector('.foto')), { clipPath: 'inset(100% 0 0 0)' }, { clipPath: 'inset(0% 0 0 0)', duration: 1.1, stagger: .08, ease: 'power4.out' });
      }});
      ScrollTrigger.refresh();
    };
    animaCards();
    new MutationObserver(animaCards).observe(grade, { childList: true });
  }
})();
</script>

<script type="importmap">
{ "imports": {
  "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
  "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"
} }
</script>
<script type="module">
/* ================= LOGO 3D (Three.js) ================= */
import * as THREE from 'three';
import { SVGLoader } from 'three/addons/loaders/SVGLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const caixa = document.getElementById('hero3d');
const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
try {
  const canvas = document.createElement('canvas');
  if (!(canvas.getContext('webgl2') || canvas.getContext('webgl'))) throw new Error('sem WebGL');
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, innerWidth < 860 ? 1.5 : 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const cena = new THREE.Scene();
  const pm = new THREE.PMREMGenerator(renderer);
  cena.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;

  const camera = new THREE.PerspectiveCamera(32, 1, .1, 100);
  camera.position.set(0, 0, 10);

  const svg = (await (await fetch('../img/monograma.svg')).text()).replaceAll('url(#prata)', '#dddddd');
  const dados = new SVGLoader().parse(svg);
  const grupo = new THREE.Group();
  const metal = new THREE.MeshPhysicalMaterial({ color: 0xe9e9e9, metalness: 1, roughness: .2, clearcoat: 1, clearcoatRoughness: .12 });
  dados.paths.forEach(path => SVGLoader.createShapes(path).forEach(forma => {
    const g = new THREE.ExtrudeGeometry(forma, { depth: 9, bevelEnabled: true, bevelThickness: 1.6, bevelSize: 1, bevelSegments: 4, curveSegments: 28 });
    grupo.add(new THREE.Mesh(g, metal));
  }));
  const bb = new THREE.Box3().setFromObject(grupo), tam = bb.getSize(new THREE.Vector3()), centro = bb.getCenter(new THREE.Vector3());
  grupo.children.forEach(m => m.geometry.translate(-centro.x, -centro.y, -centro.z));
  const esc = 4.6 / Math.max(tam.x, tam.y);
  grupo.scale.set(esc, -esc, esc);
  cena.add(grupo);

  const luzOuro = new THREE.PointLight(0xc8b48a, 60, 40); luzOuro.position.set(-4, 3, 5); cena.add(luzOuro);
  const luzBranca = new THREE.DirectionalLight(0xffffff, 1.4); luzBranca.position.set(3, 4, 6); cena.add(luzBranca);

  caixa.appendChild(canvas);
  caixa.classList.add('ativo');
  const ajusta = () => { const w = caixa.clientWidth, h = caixa.clientHeight; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); };
  ajusta(); addEventListener('resize', ajusta);

  // segue o mouse; no celular, gira arrastando com o dedo
  let alvoX = 0, alvoY = 0, arrastando = false, ultX = 0, giro = 0, vel = 0;
  addEventListener('pointermove', e => { if (e.pointerType === 'mouse') { alvoY = (e.clientX / innerWidth - .5) * .9; alvoX = (e.clientY / innerHeight - .5) * .5; } });
  canvas.addEventListener('pointerdown', e => { arrastando = true; ultX = e.clientX; canvas.setPointerCapture(e.pointerId); });
  canvas.addEventListener('pointermove', e => { if (!arrastando) return; vel = (e.clientX - ultX) * .012; ultX = e.clientX; giro += vel; });
  addEventListener('pointerup', () => arrastando = false);

  let visivel = true;
  new IntersectionObserver(([en]) => visivel = en.isIntersecting).observe(caixa);
  const relogio = new THREE.Clock();
  renderer.setAnimationLoop(() => {
    if (!visivel) return;
    const t = relogio.getElapsedTime();
    if (!arrastando) { vel *= .95; giro += vel; }
    const balanco = reduz ? 0 : Math.sin(t * .5) * .38;
    grupo.rotation.y += ((balanco + alvoY + giro) - grupo.rotation.y) * .06;
    grupo.rotation.x += (alvoX - grupo.rotation.x) * .06;
    grupo.position.y = reduz ? 0 : Math.sin(t * 1.1) * .09;
    luzOuro.position.x = Math.sin(t * .7) * 5;
    renderer.render(cena, camera);
  });
  window.__logo3d = true;
} catch (erro) {
  console.warn('Logo 3D indisponível — usando a logo normal.', erro);
}
</script>
"""
troca("</body>", JS + "</body>")

exec(open(RAIZ / "conta_teste.py", encoding="utf-8").read())

destino = RAIZ / "teste"
destino.mkdir(exist_ok=True)
(destino / "index.html").write_text(s, encoding="utf-8")
print("ok", len(s))
