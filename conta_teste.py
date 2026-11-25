# Executado dentro de gerar_teste.py: adiciona ícones sociais, login, cadastro e área do cliente.
# Usa as variáveis/funções de gerar_teste.py: s (html) e troca().

# --- configuração do Supabase (preenchida depois de criar o projeto) ---
troca("const LOJA = {", """// Supabase (contas de clientes). A chave "anon/publishable" é pública por natureza;
// a segurança vem das regras RLS do banco (ver supabase_setup.sql).
window.SUPABASE_CONFIG = { url: "", chave: "" };

const LOJA = {""")

# --- ícones (Font Awesome, biblioteca livre) ---
troca('<link rel="preconnect" href="https://fonts.googleapis.com">',
      '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">\n<link rel="preconnect" href="https://fonts.googleapis.com">')

# --- topo: Instagram, WhatsApp e conta no lugar do "Fale conosco" ---
troca('    <a class="btn js-zap" target="_blank" rel="noopener">Fale conosco</a>\n    <button class="burger"',
      '''    <div class="topo-acoes">
      <a class="ico js-insta" target="_blank" rel="noopener" aria-label="Instagram da DE men"><i class="fa-brands fa-instagram"></i></a>
      <a class="ico js-zap" target="_blank" rel="noopener" aria-label="WhatsApp da DE men"><i class="fa-brands fa-whatsapp"></i></a>
      <button class="btn-conta" id="btnConta" aria-label="Entrar ou criar conta"><i class="fa-regular fa-user"></i><span id="btnContaTxt">Entrar</span></button>
    </div>
    <button class="burger"''')

# --- rodapé com redes ---
troca('    <span>Revenda autorizada • 100% originais</span>\n  </div>\n</footer>',
      '''    <div class="rodape-dir">
      <div class="redes">
        <a class="ico js-insta" target="_blank" rel="noopener" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
        <a class="ico js-zap" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fa-brands fa-whatsapp"></i></a>
      </div>
      <span>Revenda autorizada • 100% originais</span>
      <a href="privacidade.html" class="link-priv">Política de privacidade</a>
    </div>
  </div>
</footer>''')

# --- coração de favorito em cada produto ---
troca('${p.foto2 ? `<img class="foto2" src="${p.foto2}" alt="${p.nome} — outro ângulo" loading="lazy">` : ""}</div>',
      '${p.foto2 ? `<img class="foto2" src="${p.foto2}" alt="${p.nome} — outro ângulo" loading="lazy">` : ""}<button class="fav" data-fav="${p.nome}" aria-label="Salvar nos favoritos"><i class="fa-regular fa-heart"></i></button></div>')
troca('<a class="btn" target="_blank" rel="noopener"\n             href="${zap(`Olá, DE men! Tenho interesse em: ${p.nome} (${p.marca}). Tem disponível?`)}">',
      '<a class="btn js-quero" data-produto="${p.nome}" data-marca="${p.marca}" target="_blank" rel="noopener"\n             href="${zap(`Olá, DE men! Tenho interesse em: ${p.nome} (${p.marca}). Tem disponível?`)}">')

# --- estilos ---
troca("</style>\n</head>", r"""
  /* ================= CONTA / REDES ================= */
  .topo-acoes{display:flex;align-items:center;gap:.4rem}
  .ico{width:40px;height:40px;display:grid;place-items:center;border:1px solid var(--linha);border-radius:50%;font-size:1.05rem;color:var(--branco);transition:border-color .2s,color .2s,background .2s}
  .ico:hover{border-color:var(--areia);color:var(--areia)}
  .btn-conta{display:flex;align-items:center;gap:.5rem;height:40px;padding:0 1rem;border:1px solid var(--branco);background:none;color:var(--branco);font-family:var(--sans);font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;cursor:pointer;transition:background .2s,color .2s}
  .btn-conta:hover{background:var(--branco);color:var(--preto)}
  .btn-conta.logado{border-color:var(--areia);color:var(--areia)}
  .redes{display:flex;gap:.5rem;margin-bottom:.6rem;justify-content:flex-end}
  .rodape-dir{display:flex;flex-direction:column;align-items:flex-end;gap:.3rem}
  .link-priv{color:var(--cinza);border-bottom:1px solid var(--linha);font-size:.75rem}
  .card .foto{position:relative}
  .fav{position:absolute;top:10px;right:10px;z-index:4;width:38px;height:38px;border-radius:50%;border:0;background:rgba(13,13,13,.6);backdrop-filter:blur(6px);color:#fff;font-size:1rem;cursor:pointer;display:grid;place-items:center;transition:transform .2s,background .2s}
  .fav:hover{transform:scale(1.1)}
  .fav.ativo{color:#e0566a;background:rgba(255,255,255,.92)}
  .fav.ativo i{font-weight:900}
  .modal{position:fixed;inset:0;z-index:400;background:rgba(0,0,0,.72);backdrop-filter:blur(6px);display:grid;place-items:center;padding:1rem}
  .modal[hidden],.area[hidden],.form-conta[hidden],.abas[hidden],[data-painel][hidden]{display:none !important}
  .modal-caixa{position:relative;width:min(420px,100%);max-height:92vh;overflow:auto;background:var(--grafite);border:1px solid var(--linha);padding:2.2rem 1.8rem 1.6rem;animation:sobe .35s cubic-bezier(.2,.7,.2,1)}
  @keyframes sobe{from{opacity:0;transform:translateY(24px)}}
  .modal-x{position:absolute;top:10px;right:12px;background:none;border:0;color:var(--cinza);font-size:1.6rem;cursor:pointer}
  .modal-logo{height:42px;margin:0 auto 1.2rem}
  .abas{display:flex;border-bottom:1px solid var(--linha);margin-bottom:1.4rem}
  .abas button{flex:1;background:none;border:0;border-bottom:2px solid transparent;color:var(--cinza);padding:.8rem;font-family:var(--sans);font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;cursor:pointer}
  .abas button.ativa{color:var(--branco);border-color:var(--areia)}
  .form-conta{display:flex;flex-direction:column;gap:.85rem}
  .form-conta label{font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--cinza);display:flex;flex-direction:column;gap:.35rem}
  .form-conta input[type=text],.form-conta input[type=email],.form-conta input[type=password],.form-conta input[type=tel]{background:var(--preto);border:1px solid var(--linha);color:var(--branco);padding:.8rem .9rem;font-family:var(--sans);font-size:.95rem;outline:none;text-transform:none;letter-spacing:0}
  .form-conta input:focus{border-color:var(--areia)}
  .form-conta input[readonly]{opacity:.6}
  .form-conta .check{flex-direction:row;align-items:flex-start;gap:.6rem;text-transform:none;letter-spacing:0;font-size:.82rem;line-height:1.4}
  .form-conta .check a{color:var(--areia);border-bottom:1px solid var(--areia)}
  .form-conta .btn{justify-content:center;margin-top:.3rem}
  .link{background:none;border:0;color:var(--cinza);font-family:var(--sans);font-size:.8rem;cursor:pointer;text-decoration:underline;align-self:center}
  .aviso{min-height:1.2rem;font-size:.85rem;margin-top:.9rem;text-align:center;color:var(--areia)}
  .aviso.erro{color:#e57373}
  .area{position:fixed;top:0;right:0;bottom:0;z-index:380;width:min(440px,100%);background:var(--grafite);border-left:1px solid var(--linha);display:flex;flex-direction:column;animation:entra .35s cubic-bezier(.2,.7,.2,1)}
  @keyframes entra{from{transform:translateX(100%)}}
  .area-topo{display:flex;justify-content:space-between;align-items:flex-start;padding:1.6rem 1.5rem 1rem;border-bottom:1px solid var(--linha);position:relative}
  .area-topo small{font-size:.66rem;letter-spacing:.24em;text-transform:uppercase;color:var(--areia)}
  .area-topo h3{font-size:1.8rem;margin-top:.2rem}
  .area .abas{margin:0;padding:0 1rem}
  .area-corpo{flex:1;overflow:auto;padding:1.4rem 1.5rem}
  .mini{display:flex;gap:.9rem;align-items:center;padding:.8rem 0;border-bottom:1px solid var(--linha)}
  .mini img,.mini .sem{width:58px;height:72px;object-fit:cover;background:var(--preto);flex-shrink:0}
  .mini div{flex:1;font-size:.9rem}
  .mini small{display:block;color:var(--cinza);font-size:.72rem;letter-spacing:.12em;text-transform:uppercase}
  .mini button{background:none;border:0;color:var(--cinza);cursor:pointer;font-size:1rem}
  .vazio-area{color:var(--cinza);text-align:center;padding:2rem 0;font-size:.9rem}
  .area-rodape{display:flex;flex-direction:column;gap:.6rem;margin-top:1.6rem}
  @media (max-width:860px){
    .btn-conta span{display:none}
    .btn-conta{width:40px;padding:0;justify-content:center;border-radius:50%}
    .topo-acoes .ico{width:36px;height:36px}
    .topo-acoes{gap:.3rem;margin-left:auto;margin-right:.6rem}
    .rodape-dir{align-items:flex-start}.redes{justify-content:flex-start}
  }
</style>
</head>""")

# --- modal de login/cadastro e área do cliente ---
troca("<!-- Assistente virtual -->", """<!-- Conta do cliente -->
<div class="modal" id="modalConta" hidden>
  <div class="modal-caixa" data-lenis-prevent role="dialog" aria-modal="true" aria-label="Entrar ou criar conta">
    <button class="modal-x" data-fechar aria-label="Fechar">×</button>
    <img src="../img/monograma.svg" alt="DE men" class="modal-logo">
    <div class="abas" id="abasConta">
      <button data-aba="entrar" class="ativa">Entrar</button>
      <button data-aba="criar">Criar conta</button>
    </div>
    <form class="form-conta" id="formEntrar">
      <label>E-mail<input type="email" name="email" required autocomplete="email"></label>
      <label>Senha<input type="password" name="senha" required minlength="6" autocomplete="current-password"></label>
      <button class="btn cheio" type="submit">Entrar</button>
      <button class="link" type="button" id="esqueci">Esqueci minha senha</button>
    </form>
    <form class="form-conta" id="formCriar" hidden>
      <label>Nome<input type="text" name="nome" required autocomplete="name"></label>
      <label>E-mail<input type="email" name="email" required autocomplete="email"></label>
      <label>WhatsApp<input type="tel" name="whatsapp" placeholder="(87) 9 9999-9999" autocomplete="tel"></label>
      <label>Senha (mín. 6 caracteres)<input type="password" name="senha" required minlength="6" autocomplete="new-password"></label>
      <label class="check"><input type="checkbox" name="lgpd" required> <span>Li e aceito a <a href="privacidade.html" target="_blank">Política de Privacidade</a> e autorizo a DE men a usar meus dados para atendimento.</span></label>
      <button class="btn cheio" type="submit">Criar conta</button>
    </form>
    <form class="form-conta" id="formNovaSenha" hidden>
      <label>Nova senha<input type="password" name="senha" required minlength="6" autocomplete="new-password"></label>
      <button class="btn cheio" type="submit">Salvar nova senha</button>
    </form>
    <p class="aviso" id="avisoConta" role="status"></p>
  </div>
</div>

<aside class="area" id="areaCliente" hidden aria-label="Área do cliente">
  <div class="area-topo">
    <div><small>Área do cliente</small><h3 id="areaOla">Olá!</h3></div>
    <button class="modal-x" data-fechar-area aria-label="Fechar">×</button>
  </div>
  <div class="abas" id="abasArea">
    <button data-aba-area="dados" class="ativa">Meus dados</button>
    <button data-aba-area="favoritos">Favoritos</button>
    <button data-aba-area="pedidos">Meus pedidos</button>
  </div>
  <div class="area-corpo" data-lenis-prevent>
    <section data-painel="dados">
      <form class="form-conta" id="formPerfil">
        <label>Nome<input type="text" name="nome" autocomplete="name"></label>
        <label>WhatsApp<input type="tel" name="whatsapp" autocomplete="tel"></label>
        <label>Cidade<input type="text" name="cidade" autocomplete="address-level2"></label>
        <label>E-mail<input type="email" name="email" readonly></label>
        <button class="btn cheio" type="submit">Salvar dados</button>
      </form>
      <p class="aviso" id="avisoPerfil" role="status"></p>
      <div class="area-rodape">
        <button class="btn" id="sair" type="button">Sair da conta</button>
        <a class="link" id="excluirConta" target="_blank" rel="noopener">Pedir exclusão da minha conta e dados</a>
      </div>
    </section>
    <section data-painel="favoritos" hidden><div id="listaFav"></div></section>
    <section data-painel="pedidos" hidden><p class="sub" style="font-size:.82rem;margin-bottom:.6rem">Peças que você pediu pelo botão "Quero este".</p><div id="listaPed"></div></section>
  </div>
</aside>

<!-- Assistente virtual -->""")

# --- script das contas (Supabase) ---
CONTA_JS = r"""
<script>
/* abre a janela de conta mesmo antes do Supabase carregar */
(() => {
  const m = document.getElementById('modalConta');
  document.getElementById('btnConta').addEventListener('click', () => { if (!window.__contaPronta) { m.hidden = false; const a = document.getElementById('avisoConta'); a.className = 'aviso'; a.textContent = window.SUPABASE_CONFIG.url ? 'Carregando…' : 'As contas de cliente estão sendo ativadas. Volte em breve!'; } });
  m.addEventListener('click', e => { if (e.target === m || e.target.closest('[data-fechar]')) m.hidden = true; });
})();
</script>
<script type="module">
/* ================= CONTAS DE CLIENTE (Supabase) ================= */
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm';
const cfg = window.SUPABASE_CONFIG || {};
if (cfg.url && cfg.chave) {
  const sb = createClient(cfg.url, cfg.chave);
  const $ = id => document.getElementById(id);
  const modal = $('modalConta'), area = $('areaCliente'), aviso = $('avisoConta');
  let usuario = null, perfil = null, favs = new Set();

  const msgErro = e => {
    const m = (e && e.message || '').toLowerCase();
    if (m.includes('invalid login')) return 'E-mail ou senha incorretos.';
    if (m.includes('not confirmed')) return 'Confirme seu e-mail antes de entrar (veja sua caixa de entrada).';
    if (m.includes('already registered') || m.includes('already been registered')) return 'Este e-mail já tem conta. Use "Entrar".';
    if (m.includes('password')) return 'A senha precisa ter pelo menos 6 caracteres.';
    if (m.includes('rate limit') || m.includes('security purposes')) return 'Muitas tentativas. Espere um pouco e tente de novo.';
    return 'Não deu certo agora. Tente de novo em instantes.';
  };
  const avisa = (el, txt, erro) => { el.className = 'aviso' + (erro ? ' erro' : ''); el.textContent = txt; };
  const voltaAqui = () => location.origin + location.pathname;

  function mostraAba(nome){
    document.querySelectorAll('#abasConta button').forEach(b => b.classList.toggle('ativa', b.dataset.aba === nome));
    $('formEntrar').hidden = nome !== 'entrar'; $('formCriar').hidden = nome !== 'criar'; $('formNovaSenha').hidden = nome !== 'nova';
    $('abasConta').hidden = nome === 'nova'; avisa(aviso, '');
  }
  const abreModal = (aba = 'entrar', txt = '') => { mostraAba(aba); if (txt) avisa(aviso, txt); modal.hidden = false; };
  $('abasConta').addEventListener('click', e => { const b = e.target.closest('[data-aba]'); if (b) mostraAba(b.dataset.aba); });

  // botão do topo
  window.__contaPronta = true;
  $('btnConta').addEventListener('click', () => usuario ? abreArea() : abreModal());

  // criar conta
  $('formCriar').addEventListener('submit', async e => {
    e.preventDefault(); const f = e.target, bt = f.querySelector('button[type=submit]');
    if (!f.lgpd.checked) return avisa(aviso, 'Para criar a conta, aceite a Política de Privacidade.', true);
    bt.disabled = true; avisa(aviso, 'Criando sua conta…');
    const { data, error } = await sb.auth.signUp({ email: f.email.value.trim(), password: f.senha.value,
      options: { data: { nome: f.nome.value.trim(), whatsapp: f.whatsapp.value.trim() }, emailRedirectTo: voltaAqui() } });
    bt.disabled = false;
    if (error) return avisa(aviso, msgErro(error), true);
    if (!data.session) { f.reset(); return avisa(aviso, 'Conta criada! Enviamos um e-mail de confirmação. Clique no link e depois entre aqui.'); }
    modal.hidden = true;
  });

  // entrar
  $('formEntrar').addEventListener('submit', async e => {
    e.preventDefault(); const f = e.target, bt = f.querySelector('button[type=submit]');
    bt.disabled = true; avisa(aviso, 'Entrando…');
    const { error } = await sb.auth.signInWithPassword({ email: f.email.value.trim(), password: f.senha.value });
    bt.disabled = false;
    if (error) return avisa(aviso, msgErro(error), true);
    f.reset(); modal.hidden = true;
  });

  // esqueci a senha
  $('esqueci').addEventListener('click', async () => {
    const email = $('formEntrar').email.value.trim();
    if (!email) return avisa(aviso, 'Digite seu e-mail acima e clique de novo em "Esqueci minha senha".', true);
    const { error } = await sb.auth.resetPasswordForEmail(email, { redirectTo: voltaAqui() });
    avisa(aviso, error ? msgErro(error) : 'Se o e-mail tiver conta, enviamos um link para criar uma nova senha.', !!error);
  });
  $('formNovaSenha').addEventListener('submit', async e => {
    e.preventDefault();
    const { error } = await sb.auth.updateUser({ password: e.target.senha.value });
    if (error) return avisa(aviso, msgErro(error), true);
    avisa(aviso, 'Senha alterada! Você já está conectado.'); setTimeout(() => modal.hidden = true, 1500);
  });

  // área do cliente
  function abreArea(aba = 'dados'){ mostraPainel(aba); area.hidden = false; }
  function mostraPainel(nome){
    document.querySelectorAll('#abasArea button').forEach(b => b.classList.toggle('ativa', b.dataset.abaArea === nome));
    document.querySelectorAll('[data-painel]').forEach(p => p.hidden = p.dataset.painel !== nome);
    if (nome === 'favoritos') listaFavoritos();
    if (nome === 'pedidos') listaPedidos();
  }
  $('abasArea').addEventListener('click', e => { const b = e.target.closest('[data-aba-area]'); if (b) mostraPainel(b.dataset.abaArea); });
  area.addEventListener('click', e => { if (e.target.closest('[data-fechar-area]')) area.hidden = true; });
  addEventListener('keydown', e => { if (e.key === 'Escape') { modal.hidden = true; area.hidden = true; } });

  $('formPerfil').addEventListener('submit', async e => {
    e.preventDefault(); const f = e.target;
    const dados = { nome: f.nome.value.trim(), whatsapp: f.whatsapp.value.trim(), cidade: f.cidade.value.trim() };
    const { error } = await sb.from('perfis').update(dados).eq('id', usuario.id);
    if (error) return avisa($('avisoPerfil'), msgErro(error), true);
    perfil = { ...perfil, ...dados }; atualizaTopo(); avisa($('avisoPerfil'), 'Dados salvos!');
  });
  $('sair').addEventListener('click', async () => { await sb.auth.signOut(); area.hidden = true; });

  const produto = nome => PRODUTOS.find(p => p.nome === nome) || { nome, marca: '', foto: '' };
  const linhaMini = (p, extra, botao) => {
    const d = document.createElement('div'); d.className = 'mini';
    d.innerHTML = (p.foto ? `<img src="${p.foto}" alt="">` : '<span class="sem"></span>') + '<div><small></small><b></b><small class="data"></small></div>' + (botao || '');
    d.querySelector('small').textContent = p.marca; d.querySelector('b').textContent = p.nome;
    d.querySelector('.data').textContent = extra || '';
    return d;
  };
  async function listaFavoritos(){
    const box = $('listaFav'); box.innerHTML = '';
    if (!favs.size) { box.innerHTML = '<p class="vazio-area">Toque no ♡ das peças da vitrine para salvar aqui.</p>'; return; }
    [...favs].forEach(nome => {
      const l = linhaMini(produto(nome), '', '<button title="Remover"><i class="fa-solid fa-xmark"></i></button>');
      l.querySelector('button').onclick = () => alternaFav(nome);
      box.appendChild(l);
    });
  }
  async function listaPedidos(){
    const box = $('listaPed'); box.innerHTML = '<p class="vazio-area">Carregando…</p>';
    const { data, error } = await sb.from('interesses').select('produto, marca, criado_em').order('criado_em', { ascending: false }).limit(50);
    box.innerHTML = '';
    if (error) { box.innerHTML = '<p class="vazio-area">Não foi possível carregar agora.</p>'; return; }
    if (!data.length) { box.innerHTML = '<p class="vazio-area">Você ainda não pediu nenhuma peça.</p>'; return; }
    data.forEach(r => box.appendChild(linhaMini(produto(r.produto), new Date(r.criado_em).toLocaleDateString('pt-BR'))));
  }

  // favoritos (coração nos cards)
  function marcaCoracoes(){
    document.querySelectorAll('.fav').forEach(b => {
      const on = favs.has(b.dataset.fav); b.classList.toggle('ativo', on);
      b.querySelector('i').className = on ? 'fa-solid fa-heart' : 'fa-regular fa-heart';
    });
  }
  async function alternaFav(nome){
    if (favs.has(nome)) { favs.delete(nome); marcaCoracoes(); await sb.from('favoritos').delete().eq('produto', nome).eq('user_id', usuario.id); }
    else { favs.add(nome); marcaCoracoes(); await sb.from('favoritos').insert({ produto: nome }); }
    if (!area.hidden) listaFavoritos();
  }
  document.addEventListener('click', e => {
    const b = e.target.closest('.fav'); if (!b) return;
    e.preventDefault(); e.stopPropagation();
    if (!usuario) return abreModal('entrar', 'Entre ou crie sua conta para salvar favoritos.');
    alternaFav(b.dataset.fav);
  });
  new MutationObserver(marcaCoracoes).observe(document.getElementById('grade'), { childList: true });

  // "Quero este" fica salvo em Meus pedidos
  document.addEventListener('click', e => {
    const a = e.target.closest('.js-quero'); if (!a || !usuario) return;
    sb.from('interesses').insert({ produto: a.dataset.produto, marca: a.dataset.marca }).then(() => {});
  });

  // estado da sessão
  function atualizaTopo(){
    const bt = $('btnConta'), nome = (perfil && perfil.nome) || (usuario && usuario.email) || '';
    $('btnContaTxt').textContent = usuario ? nome.split(/[ @]/)[0] : 'Entrar';
    bt.classList.toggle('logado', !!usuario);
    $('areaOla').textContent = usuario ? `Olá, ${nome.split(/[ @]/)[0]}!` : 'Olá!';
  }
  async function carrega(){
    if (!usuario) { perfil = null; favs = new Set(); atualizaTopo(); marcaCoracoes(); return; }
    const [{ data: p }, { data: fv }] = await Promise.all([
      sb.from('perfis').select('nome, whatsapp, cidade').eq('id', usuario.id).maybeSingle(),
      sb.from('favoritos').select('produto')
    ]);
    perfil = p || {}; favs = new Set((fv || []).map(r => r.produto));
    const f = $('formPerfil'); f.nome.value = perfil.nome || ''; f.whatsapp.value = perfil.whatsapp || ''; f.cidade.value = perfil.cidade || ''; f.email.value = usuario.email;
    $('excluirConta').href = `https://wa.me/${LOJA.whatsapp}?text=${encodeURIComponent('Olá, DE men! Quero excluir minha conta e meus dados do site. Meu e-mail: ' + usuario.email)}`;
    atualizaTopo(); marcaCoracoes();
  }
  sb.auth.onAuthStateChange((evento, sessao) => {
    usuario = sessao ? sessao.user : null;
    if (evento === 'PASSWORD_RECOVERY') abreModal('nova', 'Crie sua nova senha.');
    setTimeout(carrega, 0);
  });
  const { data: { session } } = await sb.auth.getSession();
  usuario = session ? session.user : null; carrega();
}
</script>
"""
troca("</body>", CONTA_JS + "</body>")
