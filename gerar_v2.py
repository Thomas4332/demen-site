"""Gera v2/index.html: uma versão alternativa (editorial, clara) do mesmo site, para comparar.
Usa o mesmo fonte.html (produtos, sacola, provador, contas, pagamento etc.); muda só o visual.
Rode montar.py, que chama este arquivo."""
import os
from pathlib import Path

RAIZ = Path(__file__).parent
s = (RAIZ / "fonte.html").read_text(encoding="utf-8")


def troca(a, b, n=1):
    global s
    assert a in s, f"não achei: {a[:70]}"
    s = s.replace(a, b, n)


# 1) caminhos relativos (a página fica numa subpasta)
for pasta in ("img/", "marcas/", "fotos/", "catalogos/"):
    s = s.replace(f'"{pasta}', f'"../{pasta}')

# 2) título e não indexar esta versão
troca("<title>DE men | Moda Masculina Premium — Sertânia-PE</title>",
      "<title>DE men | Versão 2 (comparação)</title>\n<meta name=\"robots\" content=\"noindex\">")

# 3) abre no tema claro (quem já escolheu um tema continua com a escolha)
troca("if (t !== 'claro' && t !== 'escuro') t = (window.matchMedia && matchMedia('(prefers-color-scheme: light)').matches) ? 'claro' : 'escuro';",
      "if (t !== 'claro' && t !== 'escuro') t = 'claro';")

# 4) topo novo: texto à esquerda, mosaico de fotos reais da loja à direita
inicio = s.index('<section class="hero com-video" id="inicio">')
fim = s.index("</section>", inicio) + len("</section>")
HERO = '''<section class="hero2" id="inicio">
    <div class="wrap hero2-grade">
      <div class="hero2-texto">
        <h1><span class="eyebrow h1-local">Moda masculina premium · Sertânia-PE</span>Elegância não precisa de esforço. Está nos <em>detalhes.</em></h1>
        <p>Calvin Klein, Reserva, Adidas e Ogochi originais, escolhidos peça por peça para o homem que se veste bem sem complicar.</p>
        <div class="acoes">
          <a href="#vitrine" class="btn cheio">Ver a vitrine</a>
          <button class="btn" id="abrirLookbook">Ver lookbook</button>
        </div>
        <ul class="hero2-fatos">
          <li><b>Revenda</b><span>autorizada</span></li>
          <li><b>100%</b><span>originais</span></li>
          <li><b>Brasil</b><span>enviamos para todo</span></li>
        </ul>
      </div>
      <div class="hero2-mosaico" aria-hidden="true">
        <figure class="m1"><video src="img/topo-modelo.mp4" poster="img/topo-modelo-capa.jpg" autoplay muted loop playsinline preload="metadata"></video></figure>
        <figure class="m2"><video src="img/topo-jaqueta.mp4" poster="img/topo-jaqueta-capa.jpg" autoplay muted loop playsinline preload="metadata"></video></figure>
        <figure class="m3"><video src="img/topo-samba.mp4" poster="img/topo-samba-capa.jpg" autoplay muted loop playsinline preload="metadata"></video></figure>
        <span class="hero2-selo">Peças<br>originais</span>
      </div>
    </div>
  </section>
  <div class="faixa2" aria-hidden="true"><div class="faixa2-trilho">
    <span>Calvin Klein</span><i>✦</i><span>Reserva</span><i>✦</i><span>Adidas</span><i>✦</i><span>Ogochi</span><i>✦</i><span>Retire na loja</span><i>✦</i><span>Pix e cartão</span><i>✦</i>
    <span>Calvin Klein</span><i>✦</i><span>Reserva</span><i>✦</i><span>Adidas</span><i>✦</i><span>Ogochi</span><i>✦</i><span>Retire na loja</span><i>✦</i><span>Pix e cartão</span><i>✦</i>
  </div></div>'''
HERO = HERO.replace('"fotos/', '"../fotos/').replace('"img/', '"../img/')
s = s[:inicio] + HERO + s[fim:]

# o script que coloca a foto de capa procura .hero; aqui não existe
troca("if (LOJA.fotoCapa) { const h = document.querySelector('.hero');",
      "if (LOJA.fotoCapa && document.querySelector('.hero')) { const h = document.querySelector('.hero');")

# 5) rodapé com a marca grande
# (a marca grande do rodapé agora vem do fonte.html)

CLARO = ("--preto:#f7f4ef; --grafite:#ffffff; --grafite2:#efeae2; --cinza:#6b655c; --linha:#e2dbd0;"
         "--branco:#161514; --areia:#836a3a; --texto2:#3b3833; --texto3:#514c45; --vidro:247,244,239; color:var(--branco);")

CSS = r"""
  /* ================= VERSÃO 2 — editorial ================= */
  :root[data-tema="claro"] header:not(.solid):not(:has(.menu.aberto)){__CLARO__}
  :root[data-tema="claro"] header .logo-img{filter:brightness(.32) contrast(1.2)}
  h2{font-size:clamp(2.4rem,5vw,4.2rem);letter-spacing:-.01em;line-height:1}

  /* Topo */
  .hero2{padding:calc(72px + 3.5rem) 0 3.5rem;background:var(--preto);position:relative;overflow:hidden}
  body.com-promo .hero2{padding-top:calc(108px + 3.5rem)}
  .hero2-grade{display:grid;grid-template-columns:1.05fr 1fr;gap:4rem;align-items:center}
  .hero2 h1{font-size:clamp(3rem,6.4vw,6rem);line-height:.98;letter-spacing:-.015em;margin:0 0 1.6rem}
  .hero2 h1 em{font-style:italic;color:var(--areia)}
  .hero2 p{color:var(--texto2);max-width:44ch;font-size:1.05rem;margin-bottom:2rem}
  .hero2 .acoes{display:flex;gap:.8rem;flex-wrap:wrap}
  .hero2-fatos{list-style:none;display:flex;gap:2.4rem;margin-top:3rem;padding-top:1.6rem;border-top:1px solid var(--linha)}
  .hero2-fatos li{display:flex;flex-direction:column;gap:.15rem}
  .hero2-fatos b{font-family:var(--serif);font-weight:500;font-size:1.7rem;line-height:1}
  .hero2-fatos span{font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--cinza)}
  .hero2-mosaico{position:relative;display:grid;grid-template-columns:1.25fr 1fr;grid-template-rows:1fr 1fr;gap:14px;height:min(78vh,680px)}
  .hero2-mosaico figure{overflow:hidden;background:var(--mini);margin:0}
  .hero2-mosaico .m1{grid-row:1 / 3}
  .hero2-mosaico img,.hero2-mosaico video{width:100%;height:100%;object-fit:cover;display:block}
  .hero2-mosaico .m1 video{object-position:50% 0%}
  .hero2-mosaico img{animation:zoomlento 18s ease-in-out infinite alternate}
  .hero2-mosaico .m2 img{animation-delay:-6s}
  .hero2-mosaico .m3{background:#fff}
  .hero2-mosaico .m3 img{object-fit:contain;padding:12%;animation-delay:-12s}
  .hero2-mosaico .m3 video{object-fit:cover}
  @keyframes zoomlento{from{transform:scale(1)}to{transform:scale(1.08)}}
  .hero2-selo{position:absolute;left:-46px;bottom:38px;width:112px;height:112px;border-radius:50%;background:var(--areia);color:#fff;display:grid;place-items:center;text-align:center;
    font-family:var(--serif);font-size:1.15rem;line-height:1.05;font-style:italic;box-shadow:0 12px 30px rgba(0,0,0,.18);animation:gira 24s linear infinite}
  @keyframes gira{50%{transform:rotate(8deg)}}
  @media (prefers-reduced-motion:reduce){.hero2-mosaico img,.hero2-selo,.faixa2-trilho{animation:none}}

  /* Faixa de marcas */
  .faixa2{overflow:hidden;border-block:1px solid var(--linha);padding:1.15rem 0;background:var(--grafite)}
  .faixa2-trilho{display:flex;gap:2.6rem;width:max-content;align-items:center;animation:desliza2 40s linear infinite}
  .faixa2-trilho span{font-family:var(--serif);font-size:1.6rem;white-space:nowrap;letter-spacing:.04em}
  .faixa2-trilho i{color:var(--areia);font-style:normal;font-size:.8rem}
  @keyframes desliza2{to{transform:translateX(-50%)}}

  /* Vitrine: cards mais limpos */
  .card{background:transparent!important;border:0!important}
  .card .foto{background:#fff;transition:none}
  .card .foto img{transition:transform .8s cubic-bezier(.2,.7,.2,1)}
  .card:hover .foto img{transform:scale(1.045)}
  .card h3{font-size:1.25rem}

  @media (max-width:900px){
    .hero2{padding-top:calc(64px + 1.8rem)}
    body.com-promo .hero2{padding-top:calc(100px + 1.8rem)}
    .hero2-grade{grid-template-columns:1fr;gap:2.2rem}
    .hero2-mosaico{height:auto;aspect-ratio:1/.82;order:-1}
    .hero2-selo{left:auto;right:14px;bottom:-26px;width:88px;height:88px;font-size:.95rem}
    .hero2-fatos{gap:1.4rem;margin-top:2rem}
    .hero2-fatos b{font-size:1.35rem}
  }
""".replace("__CLARO__", CLARO)

troca("</style>", CSS + "\n  .movimento{display:none!important}\n</style>")

# 6) contas/SAC/avaliações (mesmo módulo do site principal)
PREFIXO = "../"
if not os.environ.get("SEM_CONTAS"):
    exec(open(RAIZ / "contas.py", encoding="utf-8").read())

(RAIZ / "v2").mkdir(exist_ok=True)
(RAIZ / "v2" / "index.html").write_text(s, encoding="utf-8")
print("v2/index.html gerado")
