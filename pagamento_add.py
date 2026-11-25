"""Aplica (uma vez) formas de pagamento e tipos de frete no fonte.html. Mantido para referência."""
import pathlib
P = pathlib.Path(__file__).parent / "fonte.html"
s = P.read_text(encoding="utf-8")
assert "pagamentos:" not in s, "já aplicado"

def troca(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)

# ---------- 1. Configuração na LOJA ----------
troca('''  fotoEquipe: ""                    // ex.: "fotos/equipe.jpg"
};''', '''  fotoEquipe: "",                   // ex.: "fotos/equipe.jpg"

  // Formas de pagamento. ativo:false esconde a opção. CONFIRMAR COM O DONO.
  pagamentos: {
    pix:      { ativo:true, desconto:"" },        // ex.: "5%" → mostra "5% de desconto no Pix". Vazio = sem desconto anunciado
    credito:  { ativo:true, parcelas:0, semJuros:true, parcelaMinima:"" }, // parcelas: ex.: 3 → "até 3x sem juros". 0 = "parcelado (condições no WhatsApp)"
    debito:   { ativo:true },
    dinheiro: { ativo:true }                        // só para quem retira na loja ou recebe em Sertânia
  },

  // Tipos de entrega. preco: texto livre ("Grátis", "R$ 10,00", "Calculado pelo CEP"). endereco:true pede CEP/endereço.
  fretes: [
    { nome:"Retirar na loja",    desc:"R. Floriano Peixoto, 70 — Sertânia. Pronto no mesmo dia.", preco:"Grátis", endereco:false },
    { nome:"Entrega em Sertânia", desc:"A loja leva até você na cidade.", preco:"A combinar", endereco:true, local:true }, // confirmar com o dono
    { nome:"Correios PAC",        desc:"Para todo o Brasil, mais econômico.", preco:"Calculado pelo CEP", endereco:true },
    { nome:"Correios SEDEX",      desc:"Para todo o Brasil, mais rápido.", preco:"Calculado pelo CEP", endereco:true }
  ]
};

// Textos de pagamento montados a partir de LOJA.pagamentos (usados no site todo)
(() => {
  const pg = LOJA.pagamentos || {}, c = pg.credito || {}, partes = [];
  if (pg.pix && pg.pix.ativo) partes.push('Pix' + (pg.pix.desconto ? ` (${pg.pix.desconto} de desconto)` : ''));
  if (c.ativo) partes.push(c.parcelas > 1 ? `cartão de crédito em até ${c.parcelas}x${c.semJuros ? ' sem juros' : ''} ou à vista` : 'cartão de crédito à vista ou parcelado');
  if (pg.debito && pg.debito.ativo) partes.push('débito');
  if (pg.dinheiro && pg.dinheiro.ativo) partes.push('dinheiro na loja');
  if (partes.length) LOJA.pagamento = partes.length > 1 ? partes.slice(0, -1).join(', ') + ' e ' + partes.at(-1) : partes[0];
  LOJA.pagamento = LOJA.pagamento.charAt(0).toUpperCase() + LOJA.pagamento.slice(1);
})();''')

# ---------- 2. CSS ----------
CSS = r"""
  /* ---------- Pagamento e frete ---------- */
  .sac-bloco{display:flex;flex-direction:column;gap:.45rem}
  .sac-bloco>small{font-size:.64rem;letter-spacing:.2em;text-transform:uppercase;color:var(--cinza)}
  .op-lista{display:flex;flex-direction:column;gap:.4rem}
  .op-lista label{display:grid;grid-template-columns:18px 1fr auto;gap:.6rem;align-items:center;border:1px solid var(--linha);padding:.6rem .7rem;cursor:pointer;font-size:.82rem}
  .op-lista label:has(input:checked){border-color:var(--areia);background:rgba(200,180,138,.06)}
  .op-lista input{accent-color:var(--areia);width:16px;height:16px;margin:0}
  .op-lista b{font-weight:500;display:block;line-height:1.25}
  .op-lista em{font-style:normal;font-size:.72rem;color:var(--cinza);display:block;line-height:1.3}
  .op-lista .preco-op{font-size:.72rem;color:var(--areia);text-align:right;white-space:nowrap}
  .op-lista label.desligado{opacity:.4;pointer-events:none}
  .parcelas-sel{display:flex;gap:.5rem;align-items:center;font-size:.78rem;color:var(--cinza)}
  .parcelas-sel select{background:var(--preto);border:1px solid var(--linha);color:var(--branco);padding:.5rem;font-family:var(--sans);font-size:.85rem}
  .sacola-rodape{max-height:62vh;overflow-y:auto}
  .pp-pagamento{display:flex;flex-wrap:wrap;gap:.35rem .9rem;font-size:.8rem;color:var(--cinza);margin:-.3rem 0 .2rem}
  .pp-pagamento span{display:inline-flex;align-items:center;gap:.35rem}
  .pp-pagamento svg{width:16px;height:16px;color:var(--areia)}
  .pag-faixa{border-top:1px solid var(--linha);background:var(--grafite);padding:3.2rem 0}
  .pag-grade{display:grid;grid-template-columns:1fr 1fr;gap:2.5rem}
  .pag-grade h3{font-family:var(--serif);font-weight:500;font-size:1.6rem;margin:.3rem 0 1rem}
  .pag-chips{display:flex;flex-wrap:wrap;gap:.6rem}
  .pag-chips div{display:flex;align-items:center;gap:.6rem;border:1px solid var(--linha);padding:.7rem .9rem;background:var(--preto);min-width:150px}
  .pag-chips svg{width:22px;height:22px;color:var(--areia);flex:none}
  .pag-chips b{display:block;font-weight:500;font-size:.88rem}
  .pag-chips small{display:block;font-size:.72rem;color:var(--cinza)}
  .frete-lista{display:flex;flex-direction:column;gap:.5rem}
  .frete-lista div{display:flex;justify-content:space-between;gap:1rem;border-bottom:1px solid var(--linha);padding:.55rem 0;font-size:.88rem}
  .frete-lista small{display:block;color:var(--cinza);font-size:.75rem}
  .frete-lista span{color:var(--areia);font-size:.78rem;white-space:nowrap}
  @media (max-width:860px){ .pag-grade{grid-template-columns:1fr;gap:2rem} .pag-chips div{min-width:0;flex:1 1 45%} }
"""
i = s.index("  /* ---------- Provador virtual ---------- */")
s = s[:i] + CSS + s[i:]

# ---------- 3. Sacola ----------
troca('''    <div class="opcoes-entrega">
      <label><input type="radio" name="entrega" value="Retirar na loja" checked><span>Retirar na loja</span></label>
      <label><input type="radio" name="entrega" value="Receber em casa"><span>Receber em casa</span></label>
    </div>
    <input class="campo" id="sacCidade" aria-label="Cidade ou CEP para o frete" placeholder="Cidade / CEP para o frete" hidden>''',
'''    <div class="sac-bloco"><small>Entrega</small><div class="op-lista" id="opFrete"></div></div>
    <input class="campo" id="sacCidade" aria-label="CEP e endereço para entrega" placeholder="CEP e endereço para entrega" autocomplete="postal-code" hidden>
    <div class="sac-bloco"><small>Pagamento</small><div class="op-lista" id="opPagamento"></div>
      <div class="parcelas-sel" id="parcelasSel" hidden><label for="sacParcelas">Parcelas</label><select id="sacParcelas"></select></div></div>''')

troca('''<p class="nota">Você não paga nada agora. A DE men confirma estoque, valor e frete pelo WhatsApp.</p>''',
      '''<p class="nota">Você não paga nada agora. A DE men confirma estoque, valor e frete pelo WhatsApp e envia o Pix ou o link do cartão.</p>''')

# ícones
troca("  const SVG = {\n", """  const SVG = {
    pix:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2.8l3.2 3.2-3.2 3.2L8.8 6 12 2.8zM12 14.8l3.2 3.2-3.2 3.2-3.2-3.2 3.2-3.2zM2.8 12L6 8.8 9.2 12 6 15.2 2.8 12zM14.8 12L18 8.8l3.2 3.2-3.2 3.2-3.2-3.2z"/></svg>',
    cartao:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2.5" y="5.5" width="19" height="13" rx="1.5"/><path d="M2.5 9.5h19M6 15h4"/></svg>',
    dinheiro:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2.5" y="6.5" width="19" height="11" rx="1"/><circle cx="12" cy="12" r="2.5"/><path d="M6 9.5v5M18 9.5v5"/></svg>',
    loja:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 9l1.5-5h13L20 9M4 9v11h16V9M4 9h16M9 20v-6h6v6"/></svg>',
""")

# lógica da sacola
troca('''    const entrega = document.querySelector('input[name="entrega"]:checked')?.value || '';
    const cidade = $('sacCidade').value.trim();''', '''    const fr = freteAtual(), pg = pagamentoAtual();
    const entrega = fr ? fr.nome : '';
    const cidade = $('sacCidade').value.trim();''')
troca('''      `Entrega: ${entrega}${entrega === 'Receber em casa' && cidade ? ' — ' + cidade : ''}`,''',
      '''      `Entrega: ${entrega}${fr && fr.endereco && cidade ? ' — ' + cidade : ''}`,
      pg ? `Pagamento: ${pg}` : '','''.replace("\n      pg ?", "\n      pg ?"))

troca('''  document.querySelectorAll('input[name="entrega"]').forEach(r => r.addEventListener('change', () => {
    $('sacCidade').hidden = document.querySelector('input[name="entrega"]:checked').value !== 'Receber em casa';
    atualizarLinkPedido();
  }));''', '''  /* frete e pagamento */
  const FRETES = (LOJA.fretes || []).filter(f => f && f.nome);
  const PG = LOJA.pagamentos || {}, CRED = PG.credito || {};
  $('opFrete').innerHTML = FRETES.map((f, i) => `<label><input type="radio" name="frete" value="${i}" ${i ? '' : 'checked'}><span><b>${esc(f.nome)}</b>${f.desc ? `<em>${esc(f.desc)}</em>` : ''}</span><span class="preco-op">${esc(f.preco || '')}</span></label>`).join('');
  const OPS_PG = [
    PG.pix && PG.pix.ativo && { id:'pix', nome:'Pix', desc:'À vista' + (PG.pix.desconto ? ` • ${PG.pix.desconto} de desconto` : ''), tag: PG.pix.desconto ? '-' + PG.pix.desconto : 'À vista' },
    CRED.ativo && { id:'credito-vista', nome:'Cartão de crédito à vista', desc:'1x no cartão', tag:'1x' },
    CRED.ativo && { id:'credito-parcelado', nome:'Cartão de crédito parcelado', desc: CRED.parcelas > 1 ? `Em até ${CRED.parcelas}x${CRED.semJuros ? ' sem juros' : ''}${CRED.parcelaMinima ? ' • parcela mínima ' + CRED.parcelaMinima : ''}` : 'Condições confirmadas no WhatsApp', tag: CRED.parcelas > 1 ? `até ${CRED.parcelas}x` : '' },
    PG.debito && PG.debito.ativo && { id:'debito', nome:'Cartão de débito', desc:'À vista', tag:'À vista' },
    PG.dinheiro && PG.dinheiro.ativo && { id:'dinheiro', nome:'Dinheiro', desc:'Na retirada ou na entrega em Sertânia', tag:'À vista', soLocal:true }
  ].filter(Boolean);
  $('opPagamento').innerHTML = OPS_PG.map((o, i) => `<label data-pg="${o.id}"><input type="radio" name="pagamento" value="${o.id}" ${i ? '' : 'checked'}><span><b>${esc(o.nome)}</b><em>${esc(o.desc)}</em></span><span class="preco-op">${esc(o.tag)}</span></label>`).join('');
  if (CRED.parcelas > 1) $('sacParcelas').innerHTML = Array.from({ length: CRED.parcelas - 1 }, (_, i) => i + 2).map(n => `<option value="${n}">${n}x${CRED.semJuros ? ' sem juros' : ''}</option>`).join('');
  function freteAtual() { const r = document.querySelector('input[name="frete"]:checked'); return r ? FRETES[+r.value] : null; }
  function pagamentoAtual() {
    const r = document.querySelector('input[name="pagamento"]:checked'); if (!r) return '';
    const o = OPS_PG.find(x => x.id === r.value); if (!o) return '';
    if (o.id === 'credito-parcelado') return CRED.parcelas > 1 ? `Cartão de crédito em ${$('sacParcelas').value}x${CRED.semJuros ? ' sem juros' : ''}` : 'Cartão de crédito parcelado (quero saber as condições)';
    return o.nome + (o.id === 'pix' && PG.pix.desconto ? ` (com ${PG.pix.desconto} de desconto)` : o.id === 'pix' || o.id === 'credito-vista' ? ' (à vista)' : '');
  }
  function atualizarOpcoes() {
    const fr = freteAtual();
    $('sacCidade').hidden = !(fr && fr.endereco);
    const local = fr && (!fr.endereco || fr.local);
    const din = document.querySelector('[data-pg="dinheiro"]');
    if (din) { din.classList.toggle('desligado', !local); if (!local && din.querySelector('input').checked) document.querySelector('input[name="pagamento"]').checked = true; }
    const r = document.querySelector('input[name="pagamento"]:checked');
    $('parcelasSel').hidden = !(r && r.value === 'credito-parcelado' && CRED.parcelas > 1);
    atualizarLinkPedido();
  }
  document.querySelectorAll('input[name="frete"], input[name="pagamento"]').forEach(r => r.addEventListener('change', atualizarOpcoes));
  $('sacParcelas').addEventListener('change', atualizarLinkPedido);
  atualizarOpcoes();''')

# ---------- 4. Página do produto ----------
troca('''          <div class="preco">${esc(p.preco || 'Consulte o preço no WhatsApp')}</div>''',
'''          <div class="preco">${esc(p.preco || 'Consulte o preço no WhatsApp')}</div>
          ${pagLinha()}''')
troca("  function mostrarProduto(id) {", """  function pagLinha() {
    const pg = LOJA.pagamentos || {}, c = pg.credito || {}, it = [];
    if (pg.pix && pg.pix.ativo) it.push(`${SVG.pix}Pix${pg.pix.desconto ? ' com ' + esc(pg.pix.desconto) + ' off' : ' à vista'}`);
    if (c.ativo) it.push(`${SVG.cartao}${c.parcelas > 1 ? `Até ${c.parcelas}x${c.semJuros ? ' sem juros' : ''}` : 'Cartão à vista ou parcelado'}`);
    if (pg.debito && pg.debito.ativo) it.push(`${SVG.cartao}Débito`);
    return it.length ? `<div class="pp-pagamento">${it.map(x => `<span>${x}</span>`).join('')}</div>` : '';
  }
  function mostrarProduto(id) {""")

# ---------- 5. Faixa "Pagamento e entrega" antes do rodapé ----------
troca("<footer>", """<section class="pag-faixa" id="pagamento">
  <div class="wrap pag-grade">
    <div><div class="eyebrow">Formas de pagamento</div><h3>Pague como preferir</h3><div class="pag-chips" id="pagChips"></div></div>
    <div><div class="eyebrow">Entrega</div><h3>Receba ou retire</h3><div class="frete-lista" id="freteLista"></div></div>
  </div>
</section>

<footer>""")
troca("  /* ---------- 4. Looks ---------- */", """  /* ---------- Faixa de pagamento e entrega ---------- */
  (() => {
    const pg = LOJA.pagamentos || {}, c = pg.credito || {}, chips = [];
    if (pg.pix && pg.pix.ativo) chips.push([SVG.pix, 'Pix', pg.pix.desconto ? `${pg.pix.desconto} de desconto` : 'À vista, na hora']);
    if (c.ativo) chips.push([SVG.cartao, 'Crédito à vista', '1x no cartão']);
    if (c.ativo) chips.push([SVG.cartao, 'Crédito parcelado', c.parcelas > 1 ? `Até ${c.parcelas}x${c.semJuros ? ' sem juros' : ''}` : 'Consulte as condições']);
    if (pg.debito && pg.debito.ativo) chips.push([SVG.cartao, 'Débito', 'À vista']);
    if (pg.dinheiro && pg.dinheiro.ativo) chips.push([SVG.dinheiro, 'Dinheiro', 'Na loja ou em Sertânia']);
    if ($('pagChips')) $('pagChips').innerHTML = chips.map(([i, b, s]) => `<div>${i}<span><b>${b}</b><small>${esc(s)}</small></span></div>`).join('');
    if ($('freteLista')) $('freteLista').innerHTML = (LOJA.fretes || []).map(f => `<div><p>${esc(f.nome)}<small>${esc(f.desc || '')}</small></p><span>${esc(f.preco || '')}</span></div>`).join('');
  })();

  /* ---------- 4. Looks ---------- */""")

P.write_text(s, encoding="utf-8")
print("pagamento aplicado")
