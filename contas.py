# Módulo de contas, avaliações e SAC. Executado por montar.py (site principal, PREFIXO="")
# e por gerar_teste.py (site de teste, PREFIXO="../"). Usa s (html), troca() e PREFIXO.

# --- configuração do Supabase (preenchida depois de criar o projeto) ---
troca("const LOJA = {", """// Supabase (contas de clientes). A chave "anon/publishable" é pública por natureza;
// a segurança vem das regras RLS do banco (ver supabase_setup.sql).
window.SUPABASE_CONFIG = { url: "https://ycoazbopchjxbmgxnqey.supabase.co", chave: "sb_publishable_omkx2to9vt-wEAtpVAC_Eg_hToTt9JE" };

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
  .modal-conta{position:fixed;inset:0;z-index:400;background:rgba(0,0,0,.72);backdrop-filter:blur(6px);display:grid;place-items:center;padding:1rem}
  .modal-conta[hidden],.area[hidden],.form-conta[hidden],.abas[hidden],[data-painel][hidden]{display:none !important}
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
  @media (max-width:860px){.form-conta input{font-size:16px!important}}
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
    .topo-acoes .ico{display:none}
    .btn-conta{width:38px;height:38px;border-color:var(--linha)}
    .topo-acoes{gap:.3rem;margin-left:auto;margin-right:.6rem}
    .rodape-dir{align-items:flex-start}.redes{justify-content:flex-start}
  }

  /* ================= SAC / CENTRAL DE AJUDA ================= */
  .ajuda{background:var(--grafite)}
  .ajuda-grade{display:grid;grid-template-columns:1.1fr 1fr;gap:3.5rem;margin-top:2.6rem;align-items:start}
  .faq details{border-bottom:1px solid var(--linha)}
  .faq summary{list-style:none;cursor:pointer;padding:1.15rem 2.2rem 1.15rem 0;font-family:var(--serif);font-size:1.3rem;position:relative}
  .faq summary::-webkit-details-marker{display:none}
  .faq summary::after{content:"+";position:absolute;right:.3rem;top:50%;transform:translateY(-50%);color:var(--areia);font-family:var(--sans);font-size:1.3rem;transition:transform .2s}
  .faq details[open] summary::after{transform:translateY(-50%) rotate(45deg)}
  .faq details p{color:#bdb8b0;font-size:.92rem;padding:0 0 1.2rem;line-height:1.6}
  .canais{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:1.6rem}
  .sac-caixa{background:var(--preto);border:1px solid var(--linha);padding:2rem}
  .sac-caixa h3{font-size:1.8rem;margin-bottom:.3rem}
  .sac-caixa .sub{font-size:.88rem;margin-bottom:1.2rem}
  .form-conta select,.form-conta textarea{background:var(--preto);border:1px solid var(--linha);color:var(--branco);padding:.8rem .9rem;font-family:var(--sans);font-size:.95rem;outline:none;text-transform:none;letter-spacing:0;width:100%}
  .form-conta textarea{min-height:120px;resize:vertical}
  .form-conta select:focus,.form-conta textarea:focus{border-color:var(--areia)}
  .duas{display:grid;grid-template-columns:1fr 1fr;gap:.85rem}
  .protocolo{border:1px dashed var(--areia);padding:1.2rem;text-align:center;margin-top:1rem}
  .protocolo b{display:block;font-family:var(--serif);font-size:1.8rem;color:var(--areia);letter-spacing:.12em}
  .status{display:inline-block;font-size:.6rem;letter-spacing:.16em;text-transform:uppercase;padding:.2rem .5rem;border:1px solid var(--linha);color:var(--cinza)}
  .status.resolvido{border-color:#3ccf6e;color:#3ccf6e}
  .status.andamento{border-color:var(--areia);color:var(--areia)}
  .chamado{padding:.9rem 0;border-bottom:1px solid var(--linha);font-size:.88rem}
  .chamado .resp{margin-top:.5rem;padding:.6rem .8rem;border-left:2px solid var(--areia);color:#cfcac2;font-size:.85rem}

  /* ================= AVALIAÇÕES ================= */
  .aval-pp{border-top:1px solid var(--linha);padding:2.6rem 0 0}
  .aval-resumo{display:flex;align-items:center;gap:1rem;margin:.6rem 0 1.4rem;flex-wrap:wrap}
  .aval-resumo .media{font-family:var(--serif);font-size:2.6rem;line-height:1}
  .aval-resumo .estrelas,.aval-item .estrelas,.estrelas-mini{color:var(--areia);letter-spacing:.12em}
  .aval-resumo small{color:var(--cinza)}
  .aval-lista{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem;margin-bottom:1.4rem}
  .aval-item{background:var(--grafite);padding:1.2rem 1.3rem;display:flex;flex-direction:column;gap:.5rem}
  .aval-item p{font-size:.92rem;color:#d8d3cb;line-height:1.5}
  .aval-item small{color:var(--cinza);font-size:.75rem}
  .aval-item .pend{color:var(--areia);font-size:.66rem;letter-spacing:.14em;text-transform:uppercase}
  .seletor-estrelas{display:flex;gap:.3rem}
  .seletor-estrelas button{background:none;border:0;font-size:2rem;color:#444;cursor:pointer;padding:0 .1rem;line-height:1}
  .seletor-estrelas button.on{color:var(--areia)}
  .estrelas-mini{font-size:.75rem}
  .card .nota-card{font-size:.72rem;color:var(--cinza);margin:-.2rem 0 .4rem}
  .card .nota-card b{color:var(--areia);font-weight:500}
  @media (max-width:860px){
    .ajuda-grade{grid-template-columns:1fr;gap:2rem}
    .duas{grid-template-columns:1fr}
    .sac-caixa{padding:1.4rem}
    .form-conta select,.form-conta textarea{font-size:16px}
  }
  .login-social[hidden],.btn-social[hidden]{display:none!important}
  .login-social{display:flex;flex-direction:column;gap:.6rem;margin:.4rem 0 1rem}
  .btn-social{display:flex;align-items:center;justify-content:center;gap:.7rem;width:100%;padding:.8rem 1rem;background:var(--branco);color:#1f1f1f;border:1px solid var(--branco);font-family:var(--sans);font-size:.9rem;font-weight:500;cursor:pointer}
  .btn-social:hover{background:#fff}
  .btn-social svg{width:20px;height:20px;flex:none}
  .btn-social[disabled]{opacity:.6;cursor:wait}
  .social-lgpd{font-size:.72rem;color:var(--cinza);text-align:center}
  .social-lgpd a{text-decoration:underline}
  .login-social .ou{display:flex;align-items:center;gap:.8rem;color:var(--cinza);font-size:.68rem;letter-spacing:.18em;text-transform:uppercase;margin-top:.3rem}
  .login-social .ou::before,.login-social .ou::after{content:"";flex:1;height:1px;background:var(--linha)}
  .isca{position:absolute!important;left:-9999px!important;width:1px;height:1px;overflow:hidden}
  .sac-caixa,.ajuda .wrap>*{min-width:0;max-width:100%}
  .form-conta .duas>*{min-width:0}
</style>
</head>""")

# --- link "Ajuda" no menu ---
troca('      <a href="#visite">Visite</a>\n    </nav>', '      <a href="#visite">Visite</a>\n      <a href="#ajuda">Ajuda</a>\n    </nav>')

# --- seção SAC / Central de ajuda (antes de "Visite") ---
troca('  <section class="visite" id="visite">', '''  <section class="ajuda" id="ajuda">
    <div class="wrap">
      <div class="revelar">
        <div class="eyebrow">SAC • Central de ajuda</div>
        <h2>Como podemos ajudar?</h2>
        <p class="sub">Respostas rápidas para as dúvidas mais comuns. Não achou? Fale com a gente — respondemos pelo WhatsApp ou e-mail.</p>
      </div>
      <div class="ajuda-grade">
        <div>
          <div class="faq" id="faq"></div>
          <div class="canais">
            <a class="btn zap js-zap" target="_blank" rel="noopener">WhatsApp</a>
            <button class="btn" id="abrirChat" type="button">Assistente virtual</button>
            <a class="btn js-insta" target="_blank" rel="noopener">Instagram</a>
          </div>
        </div>
        <div class="sac-caixa" id="sac">
          <h3>Fale com a gente</h3>
          <p class="sub">Dúvida, troca, problema com pedido, sugestão ou elogio. Você recebe um número de protocolo.</p>
          <form class="form-conta" id="formSac">
            <label class="isca" aria-hidden="true">Site<input type="text" name="site" tabindex="-1" autocomplete="off"></label>
            <div class="duas">
              <label>Nome<input type="text" name="nome" required minlength="2" maxlength="80" autocomplete="name"></label>
              <label>WhatsApp ou e-mail<input type="text" name="contato" required minlength="5" maxlength="120" autocomplete="email"></label>
            </div>
            <div class="duas">
              <label>Assunto<select name="assunto" required>
                <option value="">Escolha…</option>
                <option>Dúvida sobre produto</option><option>Pedido ou entrega</option><option>Troca ou devolução</option>
                <option>Problema com a compra</option><option>Elogio ou sugestão</option><option>Outro assunto</option>
              </select></label>
              <label>Nº do pedido (se tiver)<input type="text" name="pedido" maxlength="60"></label>
            </div>
            <label>Mensagem<textarea name="mensagem" required minlength="5" maxlength="2000"></textarea></label>
            <label class="check"><input type="checkbox" name="lgpd" required> <span>Autorizo a DE men a usar estes dados para responder ao meu atendimento (<a href="privacidade.html" target="_blank">Política de Privacidade</a>).</span></label>
            <button class="btn cheio" type="submit">Enviar mensagem</button>
          </form>
          <div id="sacOk" hidden></div>
          <p class="aviso" id="avisoSac" role="status"></p>
        </div>
      </div>
    </div>
  </section>

  <section class="visite" id="visite">''')

# --- modal de login/cadastro, avaliação e área do cliente ---
troca("<!-- Assistente virtual -->", """<!-- Conta do cliente -->
<div class="modal-conta" id="modalConta" hidden>
  <div class="modal-caixa" data-lenis-prevent role="dialog" aria-modal="true" aria-label="Entrar ou criar conta">
    <button class="modal-x" data-fechar aria-label="Fechar">×</button>
    <img src="__P__img/monograma.svg" alt="DE men" class="modal-logo">
    <div class="login-social" id="loginSocial" hidden>
      <button type="button" class="btn-social" data-provedor="google" hidden><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.4h6.5a5.6 5.6 0 0 1-2.4 3.6v3h3.9c2.3-2.1 3.5-5.2 3.5-8.7z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 8-2.9l-3.9-3c-1.1.7-2.5 1.2-4.1 1.2-3.1 0-5.8-2.1-6.7-5H1.3v3.1A12 12 0 0 0 12 24z"/><path fill="#FBBC05" d="M5.3 14.3a7.2 7.2 0 0 1 0-4.6V6.6H1.3a12 12 0 0 0 0 10.8l4-3.1z"/><path fill="#EA4335" d="M12 4.8c1.8 0 3.3.6 4.6 1.8l3.4-3.4A12 12 0 0 0 1.3 6.6l4 3.1c.9-2.9 3.6-4.9 6.7-4.9z"/></svg>Continuar com Google</button>
      <button type="button" class="btn-social" data-provedor="facebook" hidden><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#1877F2" d="M24 12a12 12 0 1 0-13.9 11.9v-8.4H7.1V12h3V9.4c0-3 1.8-4.7 4.5-4.7 1.3 0 2.7.2 2.7.2v3h-1.5c-1.5 0-2 .9-2 1.9V12h3.4l-.5 3.5h-2.9v8.4A12 12 0 0 0 24 12z"/></svg>Continuar com Facebook</button>
      <p class="social-lgpd">Ao continuar, você aceita a <a href="__P__privacidade.html" target="_blank">Política de Privacidade</a>.</p>
      <div class="ou"><span>ou com e-mail</span></div>
    </div>
    <div class="abas" id="abasConta">
      <button data-aba="entrar" class="ativa">Entrar</button>
      <button data-aba="criar">Criar conta</button>
    </div>
    <form class="form-conta" id="formEntrar">
      <label>E-mail<input type="email" name="email" required autocomplete="email"></label>
      <label>Senha<input type="password" name="senha" required minlength="8" autocomplete="current-password"></label>
      <button class="btn cheio" type="submit">Entrar</button>
      <button class="link" type="button" id="esqueci">Esqueci minha senha</button>
    </form>
    <form class="form-conta" id="formCriar" hidden>
      <label>Nome<input type="text" name="nome" required maxlength="80" autocomplete="name"></label>
      <label>E-mail<input type="email" name="email" required autocomplete="email"></label>
      <label>WhatsApp<input type="tel" name="whatsapp" maxlength="30" placeholder="(87) 9 9999-9999" autocomplete="tel"></label>
      <label>Senha (mín. 8 caracteres, com letras e números)<input type="password" name="senha" required minlength="8" autocomplete="new-password"></label>
      <label class="check"><input type="checkbox" name="lgpd" required> <span>Li e aceito a <a href="privacidade.html" target="_blank">Política de Privacidade</a> e autorizo a DE men a usar meus dados para atendimento.</span></label>
      <button class="btn cheio" type="submit">Criar conta</button>
    </form>
    <form class="form-conta" id="formNovaSenha" hidden>
      <label>Nova senha<input type="password" name="senha" required minlength="8" autocomplete="new-password"></label>
      <button class="btn cheio" type="submit">Salvar nova senha</button>
    </form>
    <p class="aviso" id="avisoConta" role="status"></p>
  </div>
</div>

<!-- Avaliar produto ou loja -->
<div class="modal-conta" id="modalAval" hidden>
  <div class="modal-caixa" data-lenis-prevent role="dialog" aria-modal="true" aria-label="Avaliar">
    <button class="modal-x" data-fechar aria-label="Fechar">×</button>
    <div class="eyebrow" style="text-align:center">Sua avaliação</div>
    <h3 id="avalTitulo" style="text-align:center;font-size:1.7rem;margin:.3rem 0 1.2rem"></h3>
    <form class="form-conta" id="formAval">
      <input type="hidden" name="produto"><input type="hidden" name="produto_nome">
      <div class="seletor-estrelas" id="seletorEstrelas" role="radiogroup" aria-label="Nota">
        <button type="button" data-nota="1" aria-label="1 estrela">★</button><button type="button" data-nota="2" aria-label="2 estrelas">★</button><button type="button" data-nota="3" aria-label="3 estrelas">★</button><button type="button" data-nota="4" aria-label="4 estrelas">★</button><button type="button" data-nota="5" aria-label="5 estrelas">★</button>
      </div>
      <label>Conte como foi<textarea name="texto" required minlength="3" maxlength="1000" placeholder="Qualidade, tamanho, atendimento, entrega…"></textarea></label>
      <label>Sua cidade (opcional)<input type="text" name="cidade" maxlength="60" autocomplete="address-level2"></label>
      <button class="btn cheio" type="submit">Enviar avaliação</button>
      <p class="nota" style="text-align:center">Sua avaliação aparece no site depois que a loja conferir.</p>
    </form>
    <p class="aviso" id="avisoAval" role="status"></p>
  </div>
</div>

<aside class="area" id="areaCliente" hidden aria-label="Área do cliente">
  <div class="area-topo">
    <div><small>Área do cliente</small><h3 id="areaOla">Olá!</h3></div>
    <button class="modal-x" data-fechar-area aria-label="Fechar">×</button>
  </div>
  <div class="abas" id="abasArea">
    <button data-aba-area="dados" class="ativa">Dados</button>
    <button data-aba-area="favoritos">Favoritos</button>
    <button data-aba-area="pedidos">Pedidos</button>
    <button data-aba-area="sac">Atendimentos</button>
  </div>
  <div class="area-corpo" data-lenis-prevent>
    <section data-painel="dados">
      <form class="form-conta" id="formPerfil">
        <label>Nome<input type="text" name="nome" maxlength="80" autocomplete="name"></label>
        <label>WhatsApp<input type="tel" name="whatsapp" maxlength="30" autocomplete="tel"></label>
        <label>Cidade<input type="text" name="cidade" maxlength="80" autocomplete="address-level2"></label>
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
    <section data-painel="pedidos" hidden><p class="sub" style="font-size:.82rem;margin-bottom:.6rem">Peças que você pediu pelo site (botão Pedir ou sacola).</p><div id="listaPed"></div></section>
    <section data-painel="sac" hidden><div id="listaSac"></div><a class="btn" href="#sac" data-fechar-area style="margin-top:1.2rem">Abrir novo atendimento</a></section>
  </div>
</aside>

<!-- Assistente virtual -->""".replace("__P__", PREFIXO))

# --- script: contas, avaliações e SAC ---
CONTA_JS = r"""
<script>
/* abre a janela de conta mesmo antes do Supabase carregar */
(() => {
  const m = document.getElementById('modalConta');
  document.getElementById('btnConta').addEventListener('click', () => { if (!window.__contaPronta) { m.hidden = false; const a = document.getElementById('avisoConta'); a.className = 'aviso'; a.textContent = window.SUPABASE_CONFIG.url ? 'Carregando…' : 'As contas de cliente estão sendo ativadas. Volte em breve!'; } });
  document.querySelectorAll('.modal-conta').forEach(md => md.addEventListener('click', e => { if (e.target === md || e.target.closest('[data-fechar]')) md.hidden = true; }));
})();
</script>
<script type="module">
/* ================= CONTAS, AVALIAÇÕES E SAC (Supabase) ================= */
const cfg = window.SUPABASE_CONFIG || {};
const $ = id => document.getElementById(id);
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[c]));
const estrelas = n => '★★★★★'.slice(0, Math.round(n)) + '☆☆☆☆☆'.slice(0, 5 - Math.round(n));
const avisa = (el, txt, erro) => { el.className = 'aviso' + (erro ? ' erro' : ''); el.textContent = txt; };
const dataBR = d => new Date(d).toLocaleDateString('pt-BR');
const ras = (a, b) => window.rastrear && window.rastrear(a, b);
let sb = null, usuario = null, perfil = null;
if (cfg.url && cfg.chave) {
  try { const { createClient } = await import('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'); sb = createClient(cfg.url, cfg.chave); }
  catch (e) { console.warn('Supabase não carregou', e); }
}
const msgErro = e => {
  const m = (e && e.message || '').toLowerCase();
  if (m.includes('invalid login')) return 'E-mail ou senha incorretos.';
  if (m.includes('not confirmed')) return 'Confirme seu e-mail antes de entrar (veja sua caixa de entrada).';
  if (m.includes('already registered') || m.includes('already been registered')) return 'Este e-mail já tem conta. Use "Entrar".';
  if (m.includes('duplicate') || m.includes('unique')) return 'Você já avaliou este item. Obrigado!';
  if (m.includes('limite')) return 'Muitas tentativas por hoje. Tente de novo mais tarde.';
  if (m.includes('password') || m.includes('weak')) return 'Use uma senha com pelo menos 8 caracteres, misturando letras e números.';
  if (m.includes('rate limit') || m.includes('security purposes')) return 'Muitas tentativas. Espere um pouco e tente de novo.';
  return 'Não deu certo agora. Tente de novo em instantes.';
};
const senhaBoa = v => v.length >= 8 && /[a-zA-Z]/.test(v) && /\d/.test(v);
const modal = $('modalConta'), aviso = $('avisoConta');
function mostraAba(nome) {
  document.querySelectorAll('#abasConta button').forEach(b => b.classList.toggle('ativa', b.dataset.aba === nome));
  $('formEntrar').hidden = nome !== 'entrar'; $('formCriar').hidden = nome !== 'criar'; $('formNovaSenha').hidden = nome !== 'nova';
  $('abasConta').hidden = nome === 'nova'; avisa(aviso, '');
}
const abreModal = (aba = 'entrar', txt = '') => { mostraAba(aba); if (txt) avisa(aviso, txt); modal.hidden = false; };
$('abasConta').addEventListener('click', e => { const b = e.target.closest('[data-aba]'); if (b) mostraAba(b.dataset.aba); });

/* ---------- SAC: perguntas frequentes ---------- */
const FAQ = [
  ['As peças são originais?', 'Sim. A DE men é revenda autorizada Calvin Klein, Reserva, Adidas e Ogochi. Todas as peças têm etiqueta e tag da marca, e você pode pedir a nota fiscal da sua compra.'],
  ['Como faço um pedido pelo site?', 'Escolha as peças, coloque na sacola (ou toque em "Pedir") e envie pelo WhatsApp. A loja confirma estoque, valor e frete antes de você pagar. Você não paga nada no site.'],
  ['Quais as formas de pagamento?', LOJA.pagamento + '.'],
  ['Entregam na minha cidade? Qual o prazo?', LOJA.envio + ' Em Sertânia, você também pode retirar na loja.'],
  ['Como funciona a troca?', LOJA.trocas + ' Para trocar, abra um atendimento aqui ou chame no WhatsApp com o número do pedido.'],
  ['Não sei meu tamanho. E agora?', 'Use o "Guia de tamanhos" na página de cada peça. Se ficar em dúvida, mande suas medidas no WhatsApp que a gente mede a peça para você.'],
  ['Qual o horário da loja?', LOJA.horario + '. Endereço: ' + LOJA.endereco + '.'],
  ['Preciso criar conta para comprar?', 'Não. A conta é opcional e serve para salvar favoritos, ver seus pedidos e atendimentos e avaliar produtos.'],
  ['Como excluir minha conta e meus dados?', 'Na Área do cliente, toque em "Pedir exclusão da minha conta e dados", ou abra um atendimento aqui. Atendemos conforme a LGPD.']
];
$('faq').innerHTML = FAQ.map(([p, r]) => `<details><summary>${esc(p)}</summary><p>${esc(r)}</p></details>`).join('');
$('abrirChat').addEventListener('click', () => $('botBotao').click());
document.querySelectorAll('#ajuda .js-zap').forEach(a => a.href = zap('Olá, DE men! Preciso de ajuda com: '));
document.querySelectorAll('#ajuda .js-insta').forEach(a => a.href = LOJA.instagram);

/* ---------- SAC: formulário com protocolo ---------- */
const gerarProtocolo = () => 'DM' + new Date().toISOString().slice(2, 10).replaceAll('-', '') + '-' + Math.random().toString(36).slice(2, 6).toUpperCase();
$('formSac').addEventListener('submit', async e => {
  e.preventDefault(); const f = e.target, bt = f.querySelector('button[type=submit]');
  if (!f.lgpd.checked) return avisa($('avisoSac'), 'Marque a autorização para podermos responder.', true);
  if (f.site.value) return; // robô preencheu o campo invisível: ignora
  if (Date.now() - (window.__sacUltimo || 0) < 30000) return avisa($('avisoSac'), 'Aguarde alguns segundos para enviar outra mensagem.', true);
  window.__sacUltimo = Date.now();
  const dados = { nome: f.nome.value.trim(), contato: f.contato.value.trim(), assunto: f.assunto.value, pedido: f.pedido.value.trim() || null, mensagem: f.mensagem.value.trim() };
  const protocolo = gerarProtocolo();
  const textoZap = `Olá, DE men! Atendimento ${protocolo}\nAssunto: ${dados.assunto}${dados.pedido ? '\nPedido: ' + dados.pedido : ''}\nNome: ${dados.nome}\n\n${dados.mensagem}`;
  bt.disabled = true; avisa($('avisoSac'), 'Enviando…');
  let salvo = false;
  if (sb) { const { error } = await sb.from('chamados').insert({ ...dados, protocolo }); salvo = !error; if (error) console.warn(error); }
  bt.disabled = false; avisa($('avisoSac'), '');
  ras('sac', dados.assunto);
  if (salvo) {
    f.hidden = true;
    $('sacOk').hidden = false;
    $('sacOk').innerHTML = `<div class="protocolo"><small class="eyebrow">Recebemos sua mensagem</small><b>${protocolo}</b><p class="nota" style="margin-top:.6rem">Guarde este protocolo. Respondemos pelo contato que você informou${usuario ? ' e você acompanha em Área do cliente → Atendimentos' : ''}.</p></div>
      <div class="canais"><a class="btn zap" target="_blank" rel="noopener" href="${zap(textoZap)}">Agilizar pelo WhatsApp</a><button class="btn" type="button" id="sacNovo">Nova mensagem</button></div>`;
    $('sacNovo').onclick = () => { f.reset(); f.hidden = false; $('sacOk').hidden = true; preencherSac(); };
  } else {
    window.open(zap(textoZap), '_blank', 'noopener');
    avisa($('avisoSac'), 'Abrimos o WhatsApp com sua mensagem pronta. É só enviar!');
  }
});
function preencherSac() {
  const f = $('formSac'); if (!usuario) return;
  if (!f.nome.value) f.nome.value = (perfil && perfil.nome) || '';
  if (!f.contato.value) f.contato.value = (perfil && perfil.whatsapp) || usuario.email || '';
}

/* ---------- Avaliações ---------- */
const mAval = $('modalAval'); let notaEscolhida = 0;
const pintaEstrelas = n => $('seletorEstrelas').querySelectorAll('button').forEach(b => b.classList.toggle('on', +b.dataset.nota <= n));
$('seletorEstrelas').addEventListener('click', e => { const b = e.target.closest('[data-nota]'); if (b) { notaEscolhida = +b.dataset.nota; pintaEstrelas(notaEscolhida); } });
function abrirAvaliacao(produto, produtoNome) {
  if (!sb) { window.open(zap(`Olá, DE men! Quero avaliar ${produto === 'loja' ? 'a loja' : produtoNome}: `), '_blank', 'noopener'); return; }
  if (!usuario) return abreModal('entrar', 'Entre ou crie sua conta para avaliar.');
  const f = $('formAval'); f.reset(); f.hidden = false; notaEscolhida = 0; pintaEstrelas(0); avisa($('avisoAval'), '');
  f.produto.value = produto; f.produto_nome.value = produtoNome;
  if (perfil && perfil.cidade) f.cidade.value = perfil.cidade;
  $('avalTitulo').textContent = produto === 'loja' ? 'Como foi comprar na DE men?' : produtoNome;
  mAval.hidden = false;
}
$('formAval').addEventListener('submit', async e => {
  e.preventDefault(); const f = e.target;
  if (!notaEscolhida) return avisa($('avisoAval'), 'Escolha de 1 a 5 estrelas.', true);
  const primeiro = ((perfil && perfil.nome) || usuario.email.split('@')[0]).trim().split(/\s+/);
  const nome = primeiro[0] + (primeiro[1] ? ' ' + primeiro[1][0] + '.' : '');
  const { error } = await sb.from('avaliacoes').insert({ produto: f.produto.value, produto_nome: f.produto_nome.value, nota: notaEscolhida, texto: f.texto.value.trim(), cidade: f.cidade.value.trim() || null, nome });
  if (error) return avisa($('avisoAval'), msgErro(error), true);
  ras('avaliacao', f.produto.value);
  f.hidden = true; avisa($('avisoAval'), 'Obrigado! Sua avaliação vai aparecer depois que a loja conferir.');
  setTimeout(() => { mAval.hidden = true; }, 2200);
  if (f.produto.value !== 'loja') pintarAvalProduto({ id: f.produto.value, nome: f.produto_nome.value });
});
// avaliações na página do produto
async function pintarAvalProduto(p) {
  const raiz = $('ppConteudo'); if (!raiz) return;
  let box = raiz.querySelector('.aval-pp');
  if (!box) {
    box = document.createElement('div'); box.className = 'aval-pp';
    const antes = raiz.querySelector('.complete-look, .relacionados, .pp-barra'); raiz.insertBefore(box, antes);
  }
  box.innerHTML = `<div class="eyebrow">Avaliações</div><h2>O que dizem desta peça</h2><div class="aval-resumo">Carregando…</div>`;
  let lista = [];
  if (sb) { const { data } = await sb.from('avaliacoes').select('nota, texto, nome, cidade, criado_em, aprovado, user_id').eq('produto', p.id).order('criado_em', { ascending: false }).limit(30); lista = data || []; }
  const ok = lista.filter(a => a.aprovado);
  const media = ok.length ? ok.reduce((t, a) => t + a.nota, 0) / ok.length : 0;
  box.innerHTML = `<div class="eyebrow">Avaliações</div><h2>O que dizem desta peça</h2>
    <div class="aval-resumo">${ok.length ? `<span class="media">${media.toFixed(1).replace('.', ',')}</span><span class="estrelas">${estrelas(media)}</span><small>${ok.length} ${ok.length === 1 ? 'avaliação' : 'avaliações'}</small>` : '<small>Ainda sem avaliações. Comprou esta peça? Seja o primeiro a avaliar.</small>'}</div>
    ${lista.length ? `<div class="aval-lista">${lista.map(a => `<div class="aval-item"><span class="estrelas">${estrelas(a.nota)}</span><p>${esc(a.texto)}</p><small>${esc(a.nome || 'Cliente')}${a.cidade ? ' • ' + esc(a.cidade) : ''} • ${dataBR(a.criado_em)}</small>${a.aprovado ? '' : '<span class="pend">Sua avaliação • aguardando a loja</span>'}</div>`).join('')}</div>` : ''}
    <button class="btn" type="button" data-avaliar="${esc(p.id)}" data-avaliar-nome="${esc(p.nome)}">Avaliar esta peça</button>`;
}
window.addEventListener('produto-aberto', e => pintarAvalProduto(e.detail));
document.addEventListener('click', e => {
  const b = e.target.closest('[data-avaliar]'); if (!b) return;
  e.preventDefault(); abrirAvaliacao(b.dataset.avaliar, b.dataset.avaliarNome || '');
});
// "Já comprou? Conte como foi" avalia a loja
const btnLoja = $('btnAvaliar');
if (btnLoja && sb) { btnLoja.removeAttribute('target'); btnLoja.href = '#clientes'; btnLoja.dataset.avaliar = 'loja'; btnLoja.dataset.avaliarNome = 'DE men'; }
// avaliações reais no lugar dos exemplos + estrelas nos cards
async function avaliacoesReais() {
  if (!sb) return;
  const { data } = await sb.from('avaliacoes').select('produto, produto_nome, nota, texto, nome, cidade').eq('aprovado', true).order('criado_em', { ascending: false }).limit(200);
  if (!data || !data.length) return;
  const destaque = data.filter(a => a.nota >= 4).slice(0, 6);
  if (destaque.length) $('avalGrade').innerHTML = destaque.map(a => `
    <figure class="aval"><div class="estrelas">${estrelas(a.nota)}</div><p>“${esc(a.texto)}”</p>
    <figcaption class="quem"><i>${esc((a.nome || '?')[0])}</i><span>${esc(a.nome || 'Cliente')}<small>${esc(a.cidade || '')}${a.produto !== 'loja' && a.produto_nome ? (a.cidade ? ' • ' : '') + 'comprou ' + esc(a.produto_nome) : ''}</small></span></figcaption></figure>`).join('');
  const porProduto = {};
  data.filter(a => a.produto !== 'loja').forEach(a => { (porProduto[a.produto] ||= []).push(a.nota); });
  window.__notas = porProduto;
  const marcarCards = () => document.querySelectorAll('.card[data-id]').forEach(c => {
    const n = porProduto[c.dataset.id]; if (!n || c.querySelector('.nota-card')) return;
    const m = n.reduce((t, x) => t + x, 0) / n.length;
    c.querySelector('.preco')?.insertAdjacentHTML('beforebegin', `<div class="nota-card"><b>★ ${m.toFixed(1).replace('.', ',')}</b> (${n.length})</div>`);
  });
  marcarCards(); new MutationObserver(marcarCards).observe(document.body, { childList: true, subtree: true });
}
avaliacoesReais();

/* ================= CONTAS ================= */
if (sb) {
  const area = $('areaCliente'); let favs = new Set();
  const voltaAqui = () => location.origin + location.pathname;
  window.__contaPronta = true;
  $('btnConta').addEventListener('click', () => usuario ? abreArea() : abreModal());

  $('formCriar').addEventListener('submit', async e => {
    e.preventDefault(); const f = e.target, bt = f.querySelector('button[type=submit]');
    if (!f.lgpd.checked) return avisa(aviso, 'Para criar a conta, aceite a Política de Privacidade.', true);
    if (!senhaBoa(f.senha.value)) return avisa(aviso, 'Use uma senha com pelo menos 8 caracteres, misturando letras e números.', true);
    bt.disabled = true; avisa(aviso, 'Criando sua conta…');
    const { data, error } = await sb.auth.signUp({ email: f.email.value.trim(), password: f.senha.value,
      options: { data: { nome: f.nome.value.trim(), whatsapp: f.whatsapp.value.trim() }, emailRedirectTo: voltaAqui() } });
    bt.disabled = false;
    if (error) return avisa(aviso, msgErro(error), true);
    ras('conta', 'criada');
    if (!data.session) { f.reset(); return avisa(aviso, 'Conta criada! Enviamos um e-mail de confirmação. Clique no link e depois entre aqui.'); }
    modal.hidden = true;
  });
  // Login com Google e Facebook: os botões só aparecem se o provedor estiver ligado no Supabase
  fetch(cfg.url + '/auth/v1/settings', { headers: { apikey: cfg.chave } }).then(r => r.ok ? r.json() : null).then(c => {
    const ext = (c && c.external) || {}; let algum = false;
    document.querySelectorAll('[data-provedor]').forEach(b => { const on = !!ext[b.dataset.provedor]; b.hidden = !on; algum = algum || on; });
    $('loginSocial').hidden = !algum;
  }).catch(() => {});
  $('loginSocial').addEventListener('click', async e => {
    const b = e.target.closest('[data-provedor]'); if (!b) return;
    b.disabled = true; avisa(aviso, 'Abrindo ' + (b.dataset.provedor === 'google' ? 'o Google' : 'o Facebook') + '…');
    ras('conta', 'login-' + b.dataset.provedor);
    const { error } = await sb.auth.signInWithOAuth({ provider: b.dataset.provedor, options: { redirectTo: voltaAqui() } });
    if (error) { b.disabled = false; avisa(aviso, 'Não foi possível entrar agora. Tente pelo e-mail.', true); }
  });
  $('formEntrar').addEventListener('submit', async e => {
    e.preventDefault(); const f = e.target, bt = f.querySelector('button[type=submit]');
    bt.disabled = true; avisa(aviso, 'Entrando…');
    const { error } = await sb.auth.signInWithPassword({ email: f.email.value.trim(), password: f.senha.value });
    bt.disabled = false;
    if (error) return avisa(aviso, msgErro(error), true);
    f.reset(); modal.hidden = true;
  });
  $('esqueci').addEventListener('click', async () => {
    const email = $('formEntrar').email.value.trim();
    if (!email) return avisa(aviso, 'Digite seu e-mail acima e clique de novo em "Esqueci minha senha".', true);
    const { error } = await sb.auth.resetPasswordForEmail(email, { redirectTo: voltaAqui() });
    avisa(aviso, error ? msgErro(error) : 'Se o e-mail tiver conta, enviamos um link para criar uma nova senha.', !!error);
  });
  $('formNovaSenha').addEventListener('submit', async e => {
    e.preventDefault();
    if (!senhaBoa(e.target.senha.value)) return avisa(aviso, 'Use uma senha com pelo menos 8 caracteres, misturando letras e números.', true);
    const { error } = await sb.auth.updateUser({ password: e.target.senha.value });
    if (error) return avisa(aviso, msgErro(error), true);
    avisa(aviso, 'Senha alterada! Você já está conectado.'); setTimeout(() => modal.hidden = true, 1500);
  });

  function abreArea(aba = 'dados') { mostraPainel(aba); area.hidden = false; }
  function mostraPainel(nome) {
    document.querySelectorAll('#abasArea button').forEach(b => b.classList.toggle('ativa', b.dataset.abaArea === nome));
    document.querySelectorAll('[data-painel]').forEach(p => p.hidden = p.dataset.painel !== nome);
    if (nome === 'favoritos') listaFavoritos();
    if (nome === 'pedidos') listaPedidos();
    if (nome === 'sac') listaChamados();
  }
  $('abasArea').addEventListener('click', e => { const b = e.target.closest('[data-aba-area]'); if (b) mostraPainel(b.dataset.abaArea); });
  area.addEventListener('click', e => { if (e.target.closest('[data-fechar-area]')) area.hidden = true; });
  addEventListener('keydown', e => { if (e.key === 'Escape') { modal.hidden = true; area.hidden = true; mAval.hidden = true; } });

  $('formPerfil').addEventListener('submit', async e => {
    e.preventDefault(); const f = e.target;
    const dados = { nome: f.nome.value.trim(), whatsapp: f.whatsapp.value.trim(), cidade: f.cidade.value.trim() };
    const { error } = await sb.from('perfis').update(dados).eq('id', usuario.id);
    if (error) return avisa($('avisoPerfil'), msgErro(error), true);
    perfil = { ...perfil, ...dados }; atualizaTopo(); avisa($('avisoPerfil'), 'Dados salvos!');
  });
  $('sair').addEventListener('click', async () => { await sb.auth.signOut(); area.hidden = true; });

  const produto = chave => PRODUTOS.find(p => p.nome === chave || p.id === chave) || { nome: chave, marca: '', foto: '' };
  const linhaMini = (p, extra, botao) => {
    const d = document.createElement('div'); d.className = 'mini';
    d.innerHTML = (p.foto ? `<img src="${esc(p.foto)}" alt="">` : '<span class="sem"></span>') + '<div><small></small><b></b><small class="data"></small></div>' + (botao || '');
    d.querySelector('small').textContent = p.marca; d.querySelector('b').textContent = p.nome;
    d.querySelector('.data').textContent = extra || '';
    if (p.id) { d.style.cursor = 'pointer'; d.addEventListener('click', ev => { if (ev.target.closest('button')) return; area.hidden = true; window.abrirProduto && window.abrirProduto(p.id); }); }
    return d;
  };
  function listaFavoritos() {
    const box = $('listaFav'); box.innerHTML = '';
    if (!favs.size) { box.innerHTML = '<p class="vazio-area">Toque no ♡ das peças da vitrine para salvar aqui.</p>'; return; }
    [...favs].forEach(nome => {
      const l = linhaMini(produto(nome), '', '<button title="Remover"><i class="fa-solid fa-xmark"></i></button>');
      l.querySelector('button').onclick = () => alternaFav(nome);
      box.appendChild(l);
    });
  }
  async function listaPedidos() {
    const box = $('listaPed'); box.innerHTML = '<p class="vazio-area">Carregando…</p>';
    const { data, error } = await sb.from('interesses').select('produto, marca, tamanho, qtd, criado_em').order('criado_em', { ascending: false }).limit(50);
    box.innerHTML = '';
    if (error) { box.innerHTML = '<p class="vazio-area">Não foi possível carregar agora.</p>'; return; }
    if (!data.length) { box.innerHTML = '<p class="vazio-area">Você ainda não pediu nenhuma peça pelo site.</p>'; return; }
    data.forEach(r => box.appendChild(linhaMini(produto(r.produto), `${dataBR(r.criado_em)}${r.tamanho ? ' • tam. ' + r.tamanho : ''}${r.qtd > 1 ? ' • ' + r.qtd + 'x' : ''}`,
      `<button title="Avaliar" data-avaliar="${esc(produto(r.produto).id || r.produto)}" data-avaliar-nome="${esc(produto(r.produto).nome)}" style="font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:var(--areia)">Avaliar</button>`)));
  }
  async function listaChamados() {
    const box = $('listaSac'); box.innerHTML = '<p class="vazio-area">Carregando…</p>';
    const { data, error } = await sb.from('chamados').select('protocolo, assunto, mensagem, status, resposta, criado_em').order('criado_em', { ascending: false }).limit(30);
    if (error) { box.innerHTML = '<p class="vazio-area">Não foi possível carregar agora.</p>'; return; }
    if (!data.length) { box.innerHTML = '<p class="vazio-area">Você ainda não abriu nenhum atendimento.</p>'; return; }
    box.innerHTML = data.map(c => `<div class="chamado"><div style="display:flex;justify-content:space-between;gap:.6rem"><b>${esc(c.protocolo)}</b><span class="status ${c.status === 'resolvido' ? 'resolvido' : c.status === 'em andamento' ? 'andamento' : ''}">${esc(c.status)}</span></div>
      <small style="color:var(--cinza)">${esc(c.assunto)} • ${dataBR(c.criado_em)}</small>
      <p style="margin-top:.4rem;color:#cfcac2">${esc(c.mensagem.slice(0, 160))}${c.mensagem.length > 160 ? '…' : ''}</p>${c.resposta ? `<div class="resp"><b style="color:var(--areia)">Resposta da loja:</b> ${esc(c.resposta)}</div>` : ''}</div>`).join('');
  }

  function marcaCoracoes() {
    document.querySelectorAll('.fav').forEach(b => {
      const on = favs.has(b.dataset.fav); b.classList.toggle('ativo', on);
      const i = b.querySelector('i'); if (i) i.className = on ? 'fa-solid fa-heart' : 'fa-regular fa-heart';
    });
  }
  async function alternaFav(nome) {
    if (favs.has(nome)) { favs.delete(nome); marcaCoracoes(); await sb.from('favoritos').delete().eq('produto', nome).eq('user_id', usuario.id); }
    else { favs.add(nome); marcaCoracoes(); await sb.from('favoritos').insert({ produto: nome }); ras('favorito', nome); }
    if (!area.hidden) listaFavoritos();
  }
  document.addEventListener('click', e => {
    const b = e.target.closest('.fav'); if (!b) return;
    e.preventDefault(); e.stopPropagation();
    if (!usuario) return abreModal('entrar', 'Entre ou crie sua conta para salvar favoritos.');
    alternaFav(b.dataset.fav);
  }, true);
  new MutationObserver(marcaCoracoes).observe(document.body, { childList: true, subtree: true });

  // pedidos: botão "Pedir" do card e envio da sacola ficam salvos em "Pedidos"
  document.addEventListener('click', e => {
    if (!usuario) return;
    const a = e.target.closest('.js-quero');
    if (a) { sb.from('interesses').insert({ produto: a.dataset.produto, marca: a.dataset.marca, origem: 'pedir' }).then(() => {}); return; }
    if (e.target.closest('#sacEnviar')) {
      let itens = []; try { itens = JSON.parse(localStorage.getItem('demen_sacola')) || []; } catch {}
      if (itens.length) sb.from('interesses').insert(itens.map(i => ({ produto: i.nome, marca: i.marca, tamanho: i.tam || null, qtd: Math.min(50, i.qtd || 1), origem: 'sacola' }))).then(() => {});
    }
  });

  function atualizaTopo() {
    const bt = $('btnConta'), nome = (perfil && perfil.nome) || (usuario && usuario.email) || '';
    $('btnContaTxt').textContent = usuario ? nome.split(/[ @]/)[0] : 'Entrar';
    bt.classList.toggle('logado', !!usuario);
    $('areaOla').textContent = usuario ? `Olá, ${nome.split(/[ @]/)[0]}!` : 'Olá!';
  }
  async function carrega() {
    if (!usuario) { perfil = null; favs = new Set(); atualizaTopo(); marcaCoracoes(); return; }
    const [{ data: p }, { data: fv }] = await Promise.all([
      sb.from('perfis').select('nome, whatsapp, cidade').eq('id', usuario.id).maybeSingle(),
      sb.from('favoritos').select('produto')
    ]);
    perfil = p || {}; favs = new Set((fv || []).map(r => r.produto));
    const f = $('formPerfil'); f.nome.value = perfil.nome || ''; f.whatsapp.value = perfil.whatsapp || ''; f.cidade.value = perfil.cidade || ''; f.email.value = usuario.email;
    $('excluirConta').href = `https://wa.me/${LOJA.whatsapp}?text=${encodeURIComponent('Olá, DE men! Quero excluir minha conta e meus dados do site. Meu e-mail: ' + usuario.email)}`;
    atualizaTopo(); marcaCoracoes(); preencherSac();
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
