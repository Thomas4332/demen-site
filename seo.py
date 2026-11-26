"""SEO do site DE men. Chamado pelo montar.py depois de gerar index.html, teste/index.html e produtos.json.

Faz:
  1. robots.txt  (LIBERAR_GOOGLE em montar.py decide se libera ou bloqueia)
  2. sitemap.xml (início, privacidade e uma página por produto)
  3. títulos e descrições únicos em cada página
  4. canonical em todas as páginas (o GitHub Pages não faz redirect 301; com domínio próprio ele redireciona http/www sozinho)
  6. dados estruturados JSON-LD: loja (ClothingStore), site, perguntas frequentes, produtos e trilha de navegação
  7. texto direto no HTML: vitrine, marcas, looks, catálogos, perguntas e endereço já vêm escritos (sem depender de JavaScript)
  8. nome, endereço e telefone iguais no site e nos dados estruturados
  9. fotos em WebP leve (os .jpg continuam para redes sociais e WhatsApp)
"""
import html, json, os, re, subprocess, sys, threading, time, urllib.parse
from datetime import date
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

RAIZ = Path(__file__).parent
SITE = "https://demen-loja.github.io/"
HOJE = date.today().isoformat()
LIBERAR_GOOGLE = os.environ.get("LIBERAR_GOOGLE") == "1"
esc = lambda t: html.escape(str(t or ""), quote=True)


# ---------- 9. WebP ----------
def gerar_webp():
    from PIL import Image
    n = 0
    for jpg in (RAIZ / "fotos").glob("*.jp*g"):
        webp = jpg.with_suffix(".webp")
        if webp.exists() and webp.stat().st_mtime >= jpg.stat().st_mtime:
            continue
        im = Image.open(jpg).convert("RGB")
        if im.width > 1400:
            im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        im.save(webp, "WEBP", quality=80, method=6)
        n += 1
    return n

def trocar_por_webp(s: str) -> str:
    def f(m):
        caminho = m.group(2)
        webp = re.sub(r"\.jpe?g$", ".webp", caminho)
        return m.group(1) + webp + m.group(3) if (RAIZ / webp.replace("../", "")).exists() else m.group(0)
    # só caminhos de fotos/ (as imagens de compartilhamento em img/ continuam .jpg)
    return re.sub(r"([\"'(])((?:\.\./)?fotos/[\w.\-]+\.jpe?g)([\"')])", f, s)


# ---------- 7. Texto direto no HTML (pré-renderização) ----------
PRERENDER = ["marcasGrade", "grade", "looksGrade", "catGrade", "faq", "pagChips", "freteLista", "endereco", "horario", "telefone"]

def prerender(arquivo: str):
    """Abre a página num navegador sem tela e copia o que o JavaScript escreveu para dentro do HTML."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  (pulei o texto direto no HTML: instale com  pip install playwright && playwright install chromium)")
        return {}, []
    class Quieto(SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    srv = ThreadingHTTPServer(("127.0.0.1", 0), partial(Quieto, directory=str(RAIZ)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}/"
    try:
        with sync_playwright() as p:
            br = p.chromium.launch()
            pg = br.new_page(viewport={"width": 1366, "height": 900})
            # sem internet: nada de banco, planilha ou contador durante a geração
            pg.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
            pg.add_init_script("try{localStorage.clear()}catch(e){}")
            pg.goto(base + arquivo)
            pg.wait_for_timeout(1500)
            partes = pg.evaluate("ids => Object.fromEntries(ids.map(i => [i, document.getElementById(i) ? document.getElementById(i).innerHTML.trim() : '']))", PRERENDER)
            faq = pg.evaluate("[...document.querySelectorAll('#faq details')].map(d => [d.querySelector('summary').innerText.trim(), d.querySelector('p').innerText.trim()])")
            br.close()
    finally:
        srv.shutdown()
    return partes, faq

def injetar(s: str, partes: dict) -> str:
    for i, conteudo in partes.items():
        if not conteudo:
            continue
        m = re.search(rf'(<(\w+)\b[^>]*\bid="{i}"[^>]*>)(</\2>)', s)
        if m:
            s = s[: m.end(1)] + conteudo + s[m.start(3):]
    return s


# ---------- 6. Dados estruturados ----------
def exemplo(n):
    return bool(re.fullmatch(r"55\d{2}90{6,}", re.sub(r"\D", "", n or "")))

def telefone_e164(n):
    d = re.sub(r"\D", "", n)
    return "+" + d if d and not exemplo(n) else ""

def jsonld_inicio(dados, faq):
    loja, prods = dados["loja"], dados["produtos"]
    end = loja["endereco"]  # "R. Floriano Peixoto, 70 — Sertânia - PE"
    rua = end.split("—")[0].strip().replace("R. ", "Rua ", 1)
    org = {
        "@type": "ClothingStore", "@id": SITE + "#loja", "name": "DE men",
        "description": "Moda masculina premium em Sertânia-PE. Revenda autorizada Calvin Klein, Reserva, Adidas e Ogochi.",
        "url": SITE, "image": SITE + "img/og-demen.jpg", "logo": SITE + "img/logo-ig.jpg",
        "telephone": telefone_e164(loja.get("whatsapp", "")),
        "address": {"@type": "PostalAddress", "streetAddress": rua, "addressLocality": "Sertânia", "addressRegion": "PE", "postalCode": "56600-000", "addressCountry": "BR"},
        "geo": {"@type": "GeoCoordinates", "latitude": -8.0764307, "longitude": -37.2668626},
        "hasMap": "https://www.google.com/maps/search/?api=1&query=-8.0764307%2C-37.2668626",
        "areaServed": [{"@type": "City", "name": "Sertânia"}, {"@type": "Country", "name": "Brasil"}],
        "sameAs": [loja["instagram"]],
        "brand": [{"@type": "Brand", "name": b} for b in ["Calvin Klein", "Reserva", "Adidas", "Ogochi"]],
        "paymentAccepted": loja.get("pagamento", ""), "currenciesAccepted": "BRL",
    }
    if not org["telephone"]:
        del org["telephone"]  # número ainda é de exemplo
    grafo = [org, {"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": "DE men", "inLanguage": "pt-BR", "publisher": {"@id": SITE + "#loja"}},
             {"@type": "ItemList", "name": "Vitrine DE men", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": p["link"], "name": p["nome"]} for i, p in enumerate(prods)]}]
    if faq:
        grafo.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faq]})
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False) + "</script>"

def preco_num(t):
    m = re.search(r"(\d{1,3}(?:\.\d{3})*|\d+),(\d{2})", t or "")
    return f"{m.group(1).replace('.', '')}.{m.group(2)}" if m else None


# ---------- Páginas de produto (texto no HTML, um título e uma descrição por produto) ----------
CSS_PRODUTO = """
:root{--preto:#0d0d0d;--grafite:#1a1a1a;--cinza:#8a8a8a;--linha:#2a2a2a;--branco:#f5f3ef;--areia:#c8b48a;--serif:'Cormorant Garamond',Georgia,serif;--sans:'Inter',system-ui,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}body{background:var(--preto);color:var(--branco);font-family:var(--sans);font-weight:300;line-height:1.6}
a{color:inherit;text-decoration:none}img{max-width:100%;display:block}.wrap{width:min(1100px,92%);margin:0 auto}
header{border-bottom:1px solid var(--linha)}header .wrap{display:flex;justify-content:space-between;align-items:center;height:68px}
.logo{display:flex;align-items:center;gap:.6rem;font-size:.78rem;letter-spacing:.35em;text-transform:uppercase}.logo img{height:36px;width:auto}
.voltar{font-size:.8rem;color:var(--cinza)}.voltar:hover{color:var(--branco)}
nav.migalha{font-size:.75rem;color:var(--cinza);margin:1.6rem 0 1.2rem}nav.migalha ol{list-style:none;display:flex;flex-wrap:wrap;gap:.4rem}nav.migalha li+li::before{content:"›";margin-right:.4rem}nav.migalha a:hover{color:var(--branco)}
.produto{display:grid;grid-template-columns:1.1fr 1fr;gap:2.5rem;align-items:start;padding-bottom:3rem}
.galeria{display:grid;gap:.6rem}.galeria img{background:#fff;aspect-ratio:4/5;object-fit:cover;width:100%}.galeria .mini{display:grid;grid-template-columns:repeat(4,1fr);gap:.6rem}
.eyebrow{font-size:.72rem;letter-spacing:.3em;text-transform:uppercase;color:var(--areia);font-weight:500}
h1{font-family:var(--serif);font-weight:500;font-size:clamp(2.1rem,4vw,3rem);line-height:1.1;margin:.4rem 0 .8rem}
h2{font-family:var(--serif);font-weight:500;font-size:1.6rem;margin:2.4rem 0 1rem}
.preco{font-size:1.25rem;color:var(--areia);margin-bottom:1rem}.desc{color:#cfcac2;margin:1rem 0}
.tams{display:flex;flex-wrap:wrap;gap:.4rem;margin:.6rem 0 1.4rem}.tams .esg{text-decoration:line-through;opacity:.45}.esgotado{color:var(--areia);margin:-.6rem 0 1.2rem}.esgotado a{text-decoration:underline}.tams span{border:1px solid var(--linha);padding:.35rem .7rem;font-size:.82rem}
.btn{display:inline-flex;justify-content:center;align-items:center;gap:.5rem;padding:.95rem 1.4rem;border:1px solid var(--branco);font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;font-weight:500}
.btn.cheio{background:var(--branco);color:var(--preto)}.acoes{display:flex;flex-wrap:wrap;gap:.6rem}
.info-lista{margin-top:1.6rem;border-top:1px solid var(--linha)}.info-lista p{border-bottom:1px solid var(--linha);padding:.7rem 0;font-size:.88rem;color:#cfcac2}.info-lista b{color:var(--branco);font-weight:500}
.rel{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;padding-bottom:3rem}.rel a{display:block}.rel img{background:#fff;aspect-ratio:4/5;object-fit:cover;margin-bottom:.5rem}.rel small{color:var(--cinza);font-size:.72rem;text-transform:uppercase;letter-spacing:.14em}.rel h3{font-weight:400;font-size:.92rem;line-height:1.3}
footer{border-top:1px solid var(--linha);padding:2rem 0;font-size:.82rem;color:var(--cinza)}footer b{color:var(--branco);font-weight:500}footer p+p{margin-top:.3rem}
@media(max-width:820px){.galeria>img{max-height:70vh;object-fit:contain}.produto{grid-template-columns:1fr;gap:1.4rem}.rel{grid-template-columns:repeat(2,1fr)}}
"""

def zap(numero, texto):
    return f"https://wa.me/{re.sub(r'\D', '', numero)}?text={urllib.parse.quote(texto)}"

def pagina_produto(p, dados, csp, ga_head):
    loja = dados["loja"]
    url = SITE + f"produto/{p['id']}.html"
    fotos = [trocar_por_webp(f'"../{f}"')[1:-1] for f in p["fotosRel"]]
    fotos_jpg = [SITE + f for f in p["fotosRel"]]
    tit = f"{p['nome']} {p['marca']} | DE men Sertânia-PE"
    descricao = (p["desc"] or f"{p['nome']} {p['marca']}, original e com revenda autorizada.").rstrip(".")
    descricao = f"{descricao}. {('Tamanhos ' + ', '.join(p['tam']) + '. ') if p['tam'] else ''}Na DE men, em Sertânia-PE, com envio para todo o Brasil."[:300]
    rel = [x for x in dados["produtos"] if x["cat"] == p["cat"] and x["id"] != p["id"]][:4]
    pedido = zap(loja["whatsapp"], f"Olá, DE men! Tenho interesse em: {p['nome']} ({p['marca']}). Tem disponível?\n{url}")
    tel = re.sub(r"\D", "", loja["whatsapp"]).removeprefix("55")
    tel_fmt = f"({tel[:2]}) {tel[2:-4]}-{tel[-4:]}"
    pn = preco_num(p["preco"])
    prod_ld = {"@type": "Product", "@id": url + "#produto", "name": p["nome"], "description": descricao, "image": fotos_jpg, "sku": p["id"],
               "brand": {"@type": "Brand", "name": p["marca"]}, "category": p["cat"] + (" > " + p["sub"] if p["sub"] else ""), "url": url}
    if pn:
        prod_ld["offers"] = {"@type": "Offer", "price": pn, "priceCurrency": "BRL", "url": url, "seller": {"@id": SITE + "#loja"},
                             **({"availability": "https://schema.org/OutOfStock"} if p.get("semEstoque") else {})}
    trilha = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": p["cat"], "item": SITE + "#vitrine"},
        {"@type": "ListItem", "position": 3, "name": p["nome"], "item": url}]}
    ld = json.dumps({"@context": "https://schema.org", "@graph": [prod_ld, trilha]}, ensure_ascii=False)
    galeria = f'<img src="{esc(fotos[0])}" alt="{esc(p["nome"])} — {esc(p["marca"])}" width="800" height="1000">'
    if len(fotos) > 1:
        galeria += '<div class="mini">' + "".join(f'<img src="{esc(f)}" alt="{esc(p["nome"])} — foto {i + 2}" loading="lazy" width="200" height="250">' for i, f in enumerate(fotos[1:])) + "</div>"
    rel_html = "".join(
        f'<a href="{x["id"]}.html"><img src="{esc(trocar_por_webp(chr(34) + "../" + x["fotosRel"][0] + chr(34))[1:-1])}" alt="{esc(x["nome"])}" loading="lazy" width="400" height="500"><small>{esc(x["marca"])}</small><h3>{esc(x["nome"])}</h3></a>'
        for x in rel)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{csp}
<title>{esc(tit)}</title>
<meta name="description" content="{esc(descricao)}">
{ga_head}<link rel="canonical" href="{url}">
<meta property="og:type" content="product"><meta property="og:site_name" content="DE men"><meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{esc(tit)}"><meta property="og:description" content="{esc(descricao)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{fotos_jpg[0]}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../img/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#0d0d0d">
<script type="application/ld+json">{ld}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>{CSS_PRODUTO}</style>
</head>
<body>
<header><div class="wrap"><a class="logo" href="../"><img src="../img/logo-branco.png" alt="DE men" width="36" height="36"><span>DE men</span></a><a class="voltar" href="../#vitrine">← Ver toda a vitrine</a></div></header>
<main class="wrap">
  <nav class="migalha" aria-label="Você está em"><ol><li><a href="../">Início</a></li><li><a href="../#vitrine">{esc(p['cat'])}</a></li><li aria-current="page">{esc(p['nome'])}</li></ol></nav>
  <article class="produto">
    <div class="galeria">{galeria}</div>
    <div>
      <div class="eyebrow">{esc(p['marca'])}</div>
      <h1>{esc(p['nome'])}</h1>
      <div class="preco">{esc(p['preco'] or 'Preço sob consulta no WhatsApp')}</div>
      {('<p class="desc">' + esc(p['desc']) + '</p>') if p['desc'] else ''}
      {('<h2 style="font-size:1rem;font-family:var(--sans);margin:1rem 0 .2rem;font-weight:500">Tamanhos</h2><div class="tams">' + ''.join(f'<span class="esg" title="Esgotado">{esc(t)}</span>' if t in p.get('esgotados', []) else f'<span>{esc(t)}</span>' for t in p['tam']) + '</div>') if p['tam'] else ''}
      {'<p class="esgotado">Esgotado no momento. <a href="../#p/' + p['id'] + '">Peça para ser avisado quando chegar →</a></p>' if p.get('semEstoque') else ''}
      <div class="acoes"><a class="btn cheio" href="{esc(pedido)}" target="_blank" rel="noopener">Pedir no WhatsApp</a><a class="btn" href="../#p/{p['id']}">Ver na loja online</a></div>
      <div class="info-lista">
        <p><b>Original:</b> revenda autorizada {esc(p['marca'])}.</p>
        <p><b>Pagamento:</b> {esc(loja.get('pagamento', ''))}.</p>
        <p><b>Entrega:</b> retirada grátis na loja em Sertânia ou envio para todo o Brasil.</p>
        <p><b>Trocas:</b> {esc(loja.get('trocas', ''))}</p>
      </div>
    </div>
  </article>
  {('<section><h2>Você também pode gostar</h2><div class="rel">' + rel_html + '</div></section>') if rel else ''}
</main>
<footer><div class="wrap">
  <p><b>DE men</b> — moda masculina premium</p>
  <p>{esc(loja['endereco'])} · <a href="{esc(zap(loja['whatsapp'], 'Olá, DE men!'))}" target="_blank" rel="noopener">WhatsApp{'' if exemplo(loja['whatsapp']) else ' ' + esc(tel_fmt)}</a></p>
  <p>{esc(loja['horario'])} · <a href="{esc(loja['instagram'])}" target="_blank" rel="noopener">Instagram</a> · <a href="../privacidade.html">Privacidade</a></p>
</div></footer>
</body>
</html>
"""


# ---------- 1. robots.txt e 2. sitemap.xml ----------
ROBOS_IA = ["Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Claude-SearchBot", "Claude-User", "Applebot"]

def robots():
    if not LIBERAR_GOOGLE:
        return ("# Site em construção: bloqueado para buscadores.\n"
                "# Para liberar, rode:  LIBERAR_GOOGLE=1 python3 montar.py\n"
                "User-agent: *\nDisallow: /\n")
    linhas = ["# DE men — liberado para buscadores e robôs de busca com IA", ""]
    for r in ROBOS_IA:
        linhas += [f"User-agent: {r}", "Allow: /", "Disallow: /teste/", ""]
    linhas += ["User-agent: *", "Allow: /", "Disallow: /teste/", "", f"Sitemap: {SITE}sitemap.xml", ""]
    return "\n".join(linhas)

def sitemap(dados):
    urls = [(SITE, "1.0", "weekly", [SITE + "img/og-demen.jpg"]), (SITE + "privacidade.html", "0.2", "yearly", [])]
    urls += [(p["link"], "0.8", "weekly", [SITE + f for f in p["fotosRel"]]) for p in dados["produtos"]]
    corpo = "".join(
        f"  <url><loc>{esc(u)}</loc><lastmod>{HOJE}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority>"
        + "".join(f"<image:image><image:loc>{esc(i)}</image:loc></image:image>" for i in imgs) + "</url>\n"
        for u, pr, cf, imgs in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + corpo + "</urlset>\n")


def main():
    dados = json.loads((RAIZ / "produtos.json").read_text(encoding="utf-8"))
    print("  webp novos:", gerar_webp())

    # página inicial
    ini = (RAIZ / "index.html").read_text(encoding="utf-8")
    ini = trocar_por_webp(ini)
    (RAIZ / "index.html").write_text(ini, encoding="utf-8")
    partes, faq = prerender("index.html")
    ini = injetar(ini, partes)
    ini = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: jsonld_inicio(dados, faq), ini, count=1, flags=re.S)
    (RAIZ / "index.html").write_text(ini, encoding="utf-8")
    print(f"  texto no HTML: {sum(1 for v in partes.values() if v)} blocos, {len(faq)} perguntas no FAQ")

    # versão de teste (fica fora do Google de propósito)
    t = RAIZ / "teste" / "index.html"
    if t.exists():
        t.write_text(trocar_por_webp(t.read_text(encoding="utf-8")), encoding="utf-8")

    # privacidade: título, descrição e canonical próprios (indexável)
    pv = RAIZ / "privacidade.html"
    s = pv.read_text(encoding="utf-8")
    s = s.replace('<meta name="robots" content="noindex">\n', "").replace('<meta name="robots" content="noindex">', "")
    if 'rel="canonical"' not in s:
        s = s.replace("</title>", '</title>\n<meta name="description" content="Como a DE men, loja de moda masculina em Sertânia-PE, usa e protege os dados de quem compra pelo site e pelo WhatsApp.">\n'
                      f'<link rel="canonical" href="{SITE}privacidade.html">', 1)
    pv.write_text(s, encoding="utf-8")

    # páginas de produto
    csp = re.search(r'<meta http-equiv="Content-Security-Policy"[^>]*>\n?<meta name="referrer"[^>]*>', ini)
    csp = csp.group(0) if csp else ""
    pasta = RAIZ / "produto"
    pasta.mkdir(exist_ok=True)
    ids = set()
    for p in dados["produtos"]:
        (pasta / f"{p['id']}.html").write_text(pagina_produto(p, dados, csp, ""), encoding="utf-8")
        ids.add(p["id"] + ".html")
    for velho in pasta.glob("*.html"):
        if velho.name not in ids:
            velho.unlink()
    print("  páginas de produto:", len(ids))

    (RAIZ / "sitemap.xml").write_text(sitemap(dados), encoding="utf-8")
    (RAIZ / "robots.txt").write_text(robots(), encoding="utf-8")
    print("  robots.txt:", "LIBERADO para o Google" if LIBERAR_GOOGLE else "bloqueado (site em construção)")


if __name__ == "__main__":
    main()
