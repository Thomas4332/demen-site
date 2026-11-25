"""Aplica (uma vez) o Provador virtual no fonte.html. Mantido para referência."""
import pathlib
P = pathlib.Path(__file__).parent / "fonte.html"
s = P.read_text(encoding="utf-8")
assert 'id="provador"' not in s, "provador já aplicado"

def troca(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)

CSS = r"""
  /* ---------- Provador virtual ---------- */
  #provador{background:var(--grafite)}
  .prov-grade{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:2rem;align-items:start}
  .prov-quadro{background:var(--preto);border:1px solid var(--linha);padding:1rem;display:flex;flex-direction:column;gap:.7rem}
  .prov-slot{display:grid;grid-template-columns:44px 112px 1fr 44px;align-items:center;gap:.8rem;border-bottom:1px solid var(--linha);padding-bottom:.7rem}
  .prov-slot:last-child{border-bottom:0;padding-bottom:0}
  .prov-slot .seta{width:44px;height:44px;border:1px solid var(--linha);background:none;color:var(--branco);font-size:1.3rem;cursor:pointer;display:grid;place-items:center}
  .prov-slot .seta:hover{border-color:var(--areia);color:var(--areia)}
  .prov-foto{width:112px;aspect-ratio:4/5;background:#fff;overflow:hidden;cursor:pointer;border:0;padding:0;display:block}
  .prov-foto img{width:100%;height:100%;object-fit:cover}
  .prov-foto.vazio{background:var(--grafite2);color:var(--cinza);font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;display:grid;place-items:center;cursor:default}
  .prov-txt small{display:block;font-size:.66rem;letter-spacing:.2em;text-transform:uppercase;color:var(--areia)}
  .prov-txt b{display:block;font-weight:400;font-size:.98rem;line-height:1.3;margin:.15rem 0}
  .prov-txt span{font-size:.78rem;color:var(--cinza)}
  .prov-txt .tam-mini{display:inline-flex;gap:.3rem;flex-wrap:wrap;margin-top:.35rem}
  .prov-txt .tam-mini button{min-width:34px;height:30px;padding:0 .45rem;background:none;border:1px solid var(--linha);color:var(--branco);font-size:.75rem;cursor:pointer;font-family:var(--sans)}
  .prov-txt .tam-mini button.ativo{background:var(--branco);color:var(--preto);border-color:var(--branco)}
  .prov-acoes{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:.4rem}
  .prov-acoes .btn{flex:1;justify-content:center;min-width:150px}
  .prov-lado{display:flex;flex-direction:column;gap:1.2rem}
  .prov-caixa{border:1px solid var(--linha);padding:1.3rem;background:var(--preto)}
  .prov-caixa h3{font-family:var(--serif);font-weight:500;font-size:1.5rem;margin:.2rem 0 .4rem}
  .prov-caixa p{color:var(--cinza);font-size:.88rem}
  .prov-form{display:grid;grid-template-columns:1fr 1fr;gap:.8rem;margin-top:1rem}
  .prov-form label{font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;color:var(--cinza);display:flex;flex-direction:column;gap:.35rem}
  .prov-form input,.prov-form select{background:var(--grafite);border:1px solid var(--linha);color:var(--branco);padding:.7rem .8rem;font-family:var(--sans);font-size:.95rem;outline:none;text-transform:none;letter-spacing:0;width:100%}
  .prov-form input:focus,.prov-form select:focus{border-color:var(--areia)}
  .prov-form .inteira{grid-column:1/-1}
  .prov-form details{grid-column:1/-1;font-size:.85rem;color:var(--cinza)}
  .prov-form details summary{cursor:pointer;color:var(--branco);font-size:.8rem;letter-spacing:.06em}
  .prov-form details .dois{display:grid;grid-template-columns:1fr 1fr;gap:.8rem;margin-top:.8rem}
  .prov-res{display:grid;grid-template-columns:repeat(4,1fr);gap:.5rem;margin-top:1rem}
  .prov-res div{border:1px solid var(--linha);padding:.7rem .4rem;text-align:center}
  .prov-res small{display:block;font-size:.6rem;letter-spacing:.16em;text-transform:uppercase;color:var(--cinza)}
  .prov-res b{font-family:var(--serif);font-size:1.6rem;font-weight:500;color:var(--areia)}
  .prov-nota{font-size:.76rem!important;margin-top:.8rem}
  .prov-nota a{text-decoration:underline}
  .tam-sugerido{font-size:.8rem;color:var(--cinza);margin-top:.6rem}
  .tam-sugerido b{color:var(--areia);font-weight:500}
  .tam-sugerido button{background:none;border:0;color:var(--branco);text-decoration:underline;cursor:pointer;font-size:.8rem;font-family:var(--sans);margin-left:.3rem}
  .tam-op button.sugerido{border-color:var(--areia)}
  .btn-provar{margin-top:.6rem;width:100%;justify-content:center}
  @media (max-width:860px){
    .prov-grade{grid-template-columns:1fr}
    .prov-slot{grid-template-columns:36px 88px 1fr 36px;gap:.55rem}
    .prov-slot .seta{width:36px;height:40px}
    .prov-foto{width:88px}
    .prov-form input,.prov-form select{font-size:16px}
    .prov-res b{font-size:1.35rem}
  }
"""
i = s.index("</style>")
s = s[:i] + CSS + s[i:]

troca('      <a href="#looks">Looks</a>\n', '      <a href="#looks">Looks</a>\n      <a href="#provador">Provador</a>\n')

SECAO = """  <section id="provador">
    <div class="wrap">
      <div class="topo-sec revelar">
        <div>
          <div class="eyebrow">Provador virtual</div>
          <h2>Monte o seu look e descubra seu tamanho</h2>
          <p class="sub">Troque as peças com as setas, veja como combinam e mande tudo para a sacola já com o tamanho certo.</p>
        </div>
      </div>
      <div class="prov-grade">
        <div>
          <div class="prov-quadro" id="provQuadro" aria-live="polite"></div>
          <div class="prov-acoes">
            <button class="btn" id="provSortear" type="button">Sortear look</button>
            <button class="btn cheio" id="provSacola" type="button">Look na sacola</button>
            <a class="btn zap" id="provZap" target="_blank" rel="noopener">Pedir no WhatsApp</a>
          </div>
        </div>
        <div class="prov-lado">
          <div class="prov-caixa">
            <div class="eyebrow">Meu tamanho</div>
            <h3>Qual tamanho eu visto?</h3>
            <p>Informe altura e peso. O provador sugere o tamanho de cada peça e marca ele na página do produto.</p>
            <form class="prov-form" id="provForm">
              <label>Altura (cm)<input name="altura" type="number" inputmode="numeric" min="140" max="215" placeholder="175" required></label>
              <label>Peso (kg)<input name="peso" type="number" inputmode="numeric" min="40" max="200" placeholder="75" required></label>
              <label>Como gosta de vestir<select name="caimento"><option value="0">Na medida</option><option value="-1">Mais justo</option><option value="1">Mais folgado</option></select></label>
              <label>Número do calçado<select name="pe"><option value="">Não sei</option><option>37</option><option>38</option><option>39</option><option>40</option><option>41</option><option>42</option><option>43</option><option>44</option><option>45</option></select></label>
              <details>
                <summary>Tenho fita métrica (mais preciso)</summary>
                <div class="dois">
                  <label>Tórax (cm)<input name="torax" type="number" inputmode="numeric" min="70" max="150" placeholder="102"></label>
                  <label>Cintura (cm)<input name="cintura" type="number" inputmode="numeric" min="60" max="140" placeholder="84"></label>
                </div>
              </details>
              <button class="btn cheio inteira" type="submit">Ver meu tamanho</button>
            </form>
            <div class="prov-res" id="provRes" hidden></div>
            <p class="prov-nota" id="provNota" hidden>É uma estimativa: o caimento muda de marca para marca. Confira o <a href="#" id="provGuia">guia de tamanhos</a> ou pergunte no <a class="js-zap" target="_blank" rel="noopener">WhatsApp</a>.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

"""
troca('  <section class="catalogos" id="catalogos">', SECAO + '  <section class="catalogos" id="catalogos">')

troca("  window.abrirProduto = abrirProduto;\n", "  window.abrirProduto = abrirProduto;\n  window.addSacola = (p, tam, qtd, silencioso) => addSacola(p, tam, qtd, silencioso);\n  window.abrirGuia = p => abrirGuia(p);\n")

JS = r"""<script>
/* ---------- Provador virtual: montar look + descobrir tamanho ---------- */
(() => {
  const $ = id => document.getElementById(id);
  if (!$('provQuadro')) return;
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[c]));
  const lerLS = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k)); return v ?? d; } catch (e) { return d; } };
  const gravarLS = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const LETRAS = ['P', 'M', 'G', 'GG'];
  const NUM_BAIXO = ['38', '40', '42', '44', '46'];
  const limita = (i, n) => Math.max(0, Math.min(n - 1, i));

  /* --- tamanho --- */
  function calcular(m) {
    const alt = +m.altura, peso = +m.peso, aj = +m.caimento || 0;
    if (!alt || !peso) return null;
    let cima;
    if (+m.torax) cima = +m.torax <= 100 ? 0 : +m.torax <= 106 ? 1 : +m.torax <= 112 ? 2 : 3;
    else { cima = peso <= 65 ? 0 : peso <= 78 ? 1 : peso <= 90 ? 2 : 3; if (alt >= 186 && cima < 3) cima++; }
    cima = limita(cima + aj, 4);
    let baixo;
    if (+m.cintura) baixo = +m.cintura <= 80 ? 0 : +m.cintura <= 84 ? 1 : +m.cintura <= 88 ? 2 : +m.cintura <= 92 ? 3 : 4;
    else baixo = peso <= 60 ? 0 : peso <= 68 ? 1 : peso <= 77 ? 2 : peso <= 86 ? 3 : 4;
    const cint = +m.cintura || [78, 82, 86, 90, 94][baixo];
    const cinto = String(Math.max(90, Math.min(110, Math.round((cint + 10) / 5) * 5)));
    return { cima: LETRAS[cima], baixoNum: NUM_BAIXO[baixo], baixoLetra: LETRAS[limita(baixo === 4 ? 3 : baixo, 4)], pe: m.pe || '', cinto };
  }
  let medidas = lerLS('demen_medidas', null);
  let rec = medidas ? calcular(medidas) : null;
  const ehBaixo = p => ['Calças', 'Bermudas'].includes(p.cat);
  const ehPe = p => ['Calçados', 'Sandálias'].includes(p.cat);
  function tamPara(p) {
    if (!rec || !p || !p.tam || !p.tam.length) return '';
    const opcoes = ehPe(p) ? [rec.pe] : ehBaixo(p) ? [rec.baixoNum, rec.baixoLetra] : p.sub === 'Cintos' ? [rec.cinto] : [rec.cima];
    return opcoes.find(t => t && p.tam.includes(t)) || '';
  }

  /* --- look --- */
  const comFoto = f => PRODUTOS.filter(p => p.foto && f(p));
  const SLOTS = [
    { id: 'cabeca', nome: 'Cabeça', itens: comFoto(p => ['Bonés', 'Gorros'].includes(p.sub)), opcional: true },
    { id: 'cima', nome: 'Parte de cima', itens: comFoto(p => ['Camisas', 'Casacos'].includes(p.cat)) },
    { id: 'baixo', nome: 'Parte de baixo', itens: comFoto(ehBaixo) },
    { id: 'pes', nome: 'Pés', itens: comFoto(ehPe) }
  ].filter(s => s.itens.length);
  const salvo = lerLS('demen_provador', {});
  const pos = {}, tamEscolhido = {};
  SLOTS.forEach(s => {
    const i = s.itens.findIndex(p => p.id === salvo[s.id]);
    pos[s.id] = i >= 0 ? i : salvo[s.id] === null && s.opcional ? -1 : 0;
  });
  const atual = s => pos[s.id] >= 0 ? s.itens[pos[s.id]] : null;
  const guardar = () => gravarLS('demen_provador', Object.fromEntries(SLOTS.map(s => [s.id, atual(s) ? atual(s).id : null])));

  function slotHTML(s) {
    const p = atual(s);
    const t = p ? (tamEscolhido[p.id] ?? tamPara(p)) : '';
    return `<div class="prov-slot" data-slot="${s.id}">
      <button class="seta" type="button" data-passo="-1" aria-label="${esc(s.nome)}: peça anterior">‹</button>
      ${p ? `<button class="prov-foto" type="button" data-ver="${esc(p.id)}" aria-label="Ver ${esc(p.nome)}"><img src="${esc(p.foto)}" alt="${esc(p.nome)}" loading="lazy"></button>`
          : `<div class="prov-foto vazio">Sem peça</div>`}
      <div class="prov-txt"><small>${esc(s.nome)}</small>
        ${p ? `<b>${esc(p.nome)}</b><span>${esc(p.marca)}${p.preco ? ' • ' + esc(p.preco) : ''}</span>
          ${p.tam.length ? `<div class="tam-mini">${p.tam.map(x => `<button type="button" data-t="${esc(x)}" class="${x === t ? 'ativo' : ''}">${esc(x)}</button>`).join('')}</div>` : ''}`
          : `<b>Nenhum</b><span>Use as setas para escolher</span>`}
      </div>
      <button class="seta" type="button" data-passo="1" aria-label="${esc(s.nome)}: próxima peça">›</button>
    </div>`;
  }
  function pecas() { return SLOTS.map(s => ({ s, p: atual(s) })).filter(x => x.p).map(x => ({ ...x, t: tamEscolhido[x.p.id] ?? tamPara(x.p) })); }
  function desenhar() {
    $('provQuadro').innerHTML = SLOTS.map(slotHTML).join('');
    const lista = pecas();
    const linhas = lista.map((x, n) => `${n + 1}. ${x.p.nome} (${x.p.marca})${x.t ? ' — tam. ' + x.t : ' — tamanho a combinar'}`);
    $('provZap').href = zap(['Olá, DE men! Montei este look no provador do site:', '', ...linhas,
      rec ? `\nMinhas medidas: ${medidas.altura} cm, ${medidas.peso} kg.` : '', 'Tem disponível?'].filter(x => x !== '').join('\n'));
    $('provSacola').disabled = !lista.length;
  }
  $('provQuadro').addEventListener('click', e => {
    const slot = e.target.closest('[data-slot]'); if (!slot) return;
    const s = SLOTS.find(x => x.id === slot.dataset.slot);
    const passo = e.target.closest('[data-passo]');
    if (passo) {
      const n = s.itens.length, min = s.opcional ? -1 : 0;
      let i = pos[s.id] + +passo.dataset.passo;
      if (i >= n) i = min; if (i < min) i = n - 1;
      pos[s.id] = i; guardar(); desenhar(); return;
    }
    const t = e.target.closest('[data-t]');
    if (t) { const p = atual(s); tamEscolhido[p.id] = tamEscolhido[p.id] === t.dataset.t ? '' : t.dataset.t; desenhar(); return; }
    const ver = e.target.closest('[data-ver]');
    if (ver && window.abrirProduto) window.abrirProduto(ver.dataset.ver);
  });
  // arrastar a foto para o lado também troca a peça (celular)
  let toque = null;
  $('provQuadro').addEventListener('touchstart', e => { const sl = e.target.closest('[data-slot]'); if (sl) toque = { sl, x: e.touches[0].clientX }; }, { passive: true });
  $('provQuadro').addEventListener('touchend', e => {
    if (!toque) return; const dx = e.changedTouches[0].clientX - toque.x;
    if (Math.abs(dx) > 45) toque.sl.querySelector(`[data-passo="${dx < 0 ? 1 : -1}"]`).click();
    toque = null;
  });
  $('provSortear').addEventListener('click', () => {
    SLOTS.forEach(s => { pos[s.id] = s.opcional && Math.random() < .3 ? -1 : Math.floor(Math.random() * s.itens.length); });
    guardar(); desenhar();
  });
  $('provSacola').addEventListener('click', () => {
    const lista = pecas(); if (!lista.length || !window.addSacola) return;
    lista.forEach((x, i) => window.addSacola(x.p, x.t, 1, i < lista.length - 1));
    if (window.rastrear) window.rastrear('provador', lista.map(x => x.p.id).join(','));
  });

  /* --- formulário de medidas --- */
  const f = $('provForm');
  function mostrarRes() {
    if (!rec) return;
    $('provRes').innerHTML = [['Camisas', rec.cima], ['Calças', rec.baixoNum], ['Bermudas', rec.baixoNum + ' / ' + rec.baixoLetra], ['Calçados', rec.pe || '—']]
      .map(([a, b]) => `<div><small>${a}</small><b>${esc(b)}</b></div>`).join('');
    $('provRes').hidden = false; $('provNota').hidden = false;
  }
  if (medidas) { ['altura', 'peso', 'caimento', 'pe', 'torax', 'cintura'].forEach(k => { if (f[k] && medidas[k] != null) f[k].value = medidas[k]; }); mostrarRes(); }
  f.addEventListener('submit', e => {
    e.preventDefault();
    medidas = Object.fromEntries(['altura', 'peso', 'caimento', 'pe', 'torax', 'cintura'].map(k => [k, f[k].value]));
    rec = calcular(medidas); if (!rec) return;
    gravarLS('demen_medidas', medidas);
    Object.keys(tamEscolhido).forEach(k => delete tamEscolhido[k]);
    mostrarRes(); desenhar();
    if (window.rastrear) window.rastrear('provador-tamanho', rec.cima + '/' + rec.baixoNum);
  });
  $('provGuia').addEventListener('click', e => { e.preventDefault(); window.abrirGuia && window.abrirGuia(null); });

  /* --- na página do produto --- */
  const slotDe = p => SLOTS.find(s => s.itens.includes(p));
  function irParaProvador() {
    const fechar = document.querySelector('#ppConteudo [data-fechar]');
    if (fechar) fechar.click();
    setTimeout(() => $('provador').scrollIntoView({ behavior: 'smooth' }), 350);
  }
  window.addEventListener('produto-aberto', e => {
    const p = e.detail, caixa = document.getElementById('ppConteudo'); if (!caixa) return;
    const tams = caixa.querySelector('#ppTams'), sug = tamPara(p);
    if (tams) {
      const linha = document.createElement('p'); linha.className = 'tam-sugerido';
      if (sug) {
        linha.innerHTML = `Seu tamanho sugerido: <b>${esc(sug)}</b><button type="button">alterar medidas</button>`;
        tams.querySelector(`[data-tam="${CSS.escape(sug)}"]`)?.classList.add('sugerido');
      } else if (!rec && (slotDe(p) || p.cat === 'Cuecas')) linha.innerHTML = `Não sabe seu tamanho?<button type="button">Descobrir no provador</button>`;
      if (linha.innerHTML) { tams.after(linha); linha.querySelector('button').addEventListener('click', irParaProvador); }
    }
    const s = slotDe(p), acoes = caixa.querySelector('.pp-acoes');
    if (s && acoes) {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'btn btn-provar';
      b.textContent = 'Experimentar no provador';
      b.addEventListener('click', () => { pos[s.id] = s.itens.indexOf(p); guardar(); desenhar(); irParaProvador(); });
      acoes.after(b);
    }
  });

  desenhar();
})();
</script>
"""
troca("</body>", JS + "</body>")
P.write_text(s, encoding="utf-8")
print("provador aplicado")
