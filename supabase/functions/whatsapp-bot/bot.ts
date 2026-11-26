// Lógica do robô de WhatsApp da DE men: menu com botões + IA para perguntas livres.
// Não fala direto com WhatsApp/banco: recebe funções em "deps" (facilita testar).

export type Produto = { id: string; nome: string; marca: string; cat: string; sub: string; preco: string; tam: string[]; selo: string; desc: string; foto: string; link: string; esgotados?: string[]; semEstoque?: boolean };
const tamTxt = (p: Produto) => p.tam.map((t) => (p.esgotados || []).includes(t) ? `${t} (esgotado)` : t).join(", ");
export type Dados = { loja: any; produtos: Produto[] };
export type Saida =
  | { tipo: "texto"; texto: string }
  | { tipo: "lista"; corpo: string; botao: string; secoes: { titulo: string; linhas: { id: string; titulo: string; desc?: string }[] }[] }
  | { tipo: "botoes"; corpo: string; botoes: { id: string; titulo: string }[]; imagem?: string }
  | { tipo: "imagem"; url: string; legenda: string };
export type Entrada = { telefone: string; nome?: string; texto?: string; respostaId?: string };
export type Deps = {
  dados: Dados;
  pausadoAte: Date | null;
  agora: Date;
  historico: { direcao: "entrada" | "saida"; texto: string }[];
  ia?: (sistema: string, mensagens: { role: "user" | "assistant"; content: string }[]) => Promise<string>;
  iaUsosHoje: number;
  iaLimiteDia: number;
};
export type Resultado = { saidas: Saida[]; pausarHoras?: number; despausar?: boolean; usouIA?: boolean };

const corta = (s: string, n: number) => (s.length > n ? s.slice(0, n - 1) + "…" : s);
const norm = (s: string) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim();
const tem = (t: string, ...chaves: string[]) => chaves.some((c) => new RegExp(`(^|[^a-z])${c}`).test(t));

export function menu(dados: Dados, saudacao = ""): Saida {
  return {
    tipo: "lista",
    corpo: (saudacao ? saudacao + "\n\n" : "") + "Sou o assistente virtual da *DE men* 👔\nEscolha uma opção abaixo ou escreva sua dúvida (ex.: _tem polo M?_).",
    botao: "Ver opções",
    secoes: [
      { titulo: "Comprar", linhas: [
        { id: "catalogo", titulo: "Ver produtos", desc: "Escolha a categoria e veja fotos e tamanhos" },
        { id: "novidades", titulo: "Novidades", desc: "O que acabou de chegar" },
      ] },
      { titulo: "Dúvidas", linhas: [
        { id: "tamanhos", titulo: "Qual meu tamanho?", desc: "Guia de medidas e provador virtual" },
        { id: "frete", titulo: "Entrega e frete", desc: "Retirada, Sertânia e Correios" },
        { id: "pagamento", titulo: "Formas de pagamento", desc: "Pix, cartão à vista e parcelado" },
        { id: "trocas", titulo: "Trocas", desc: "Como trocar uma peça" },
        { id: "horario", titulo: "Horário e endereço", desc: corta(dados.loja.endereco || "", 72) },
      ] },
      { titulo: "Atendimento", linhas: [{ id: "atendente", titulo: "Falar com atendente", desc: "Uma pessoa da loja responde você" }] },
    ],
  };
}

// Texto + botões numa mensagem só (cada mensagem enviada conta na cota da Meta)
const comBotoes = (texto: string): Saida => texto.length > 980 ? { tipo: "texto", texto } : ({ tipo: "botoes", corpo: texto, botoes: [
  { id: "catalogo", titulo: "Ver produtos" }, { id: "menu", titulo: "Menu" }, { id: "atendente", titulo: "Falar com atendente" },
] });

function categorias(dados: Dados): Saida {
  const cont: Record<string, number> = {};
  dados.produtos.forEach((p) => (cont[p.cat] = (cont[p.cat] || 0) + 1));
  const linhas = Object.entries(cont).sort((a, b) => b[1] - a[1]).slice(0, 10)
    .map(([c, n]) => ({ id: "cat:" + c, titulo: corta(c, 24), desc: `${n} ${n === 1 ? "peça" : "peças"}` }));
  return { tipo: "lista", corpo: "Qual categoria você quer ver?", botao: "Categorias", secoes: [{ titulo: "Categorias", linhas }] };
}

function listaProdutos(dados: Dados, titulo: string, prods: Produto[]): Saida {
  if (!prods.length) return { tipo: "texto", texto: "Não encontrei peças nessa categoria agora. Veja tudo no site: " + dados.loja.site };
  return { tipo: "lista", corpo: `*${titulo}* — escolha uma peça para ver a foto e os tamanhos:`, botao: "Ver peças", secoes: [{
    titulo: corta(titulo, 24),
    linhas: prods.slice(0, 10).map((p) => ({ id: "p:" + p.id, titulo: corta(p.nome, 24), desc: corta(`${p.marca}${p.preco ? " • " + p.preco : ""}${p.semEstoque ? " • ESGOTADO" : p.tam.length ? " • " + tamTxt(p) : ""}`, 72) })),
  }] };
}

function produto(dados: Dados, id: string): Saida[] {
  const p = dados.produtos.find((x) => x.id === id);
  if (!p) return [{ tipo: "texto", texto: "Essa peça não está mais na vitrine. Veja as disponíveis no site: " + dados.loja.site }];
  const legenda = [`*${p.nome}*`, p.marca, p.preco ? `💰 ${p.preco}` : "💰 Preço: o atendente confirma pra você", p.semEstoque ? "⛔ Esgotado no momento" : p.tam.length ? `📏 Tamanhos: ${tamTxt(p)}` : "", p.desc ? "\n" + p.desc : "", `\n🔗 ${p.link}`].filter(Boolean).join("\n");
  return [{ tipo: "botoes", imagem: p.foto, corpo: corta(legenda, 1024), botoes: [{ id: "quero:" + p.id, titulo: p.semEstoque ? "Avise-me" : "Quero este" }, { id: "cat:" + p.cat, titulo: "Ver parecidos" }, { id: "menu", titulo: "Menu" }] }];
}

function textoFrete(dados: Dados) {
  const f = (dados.loja.fretes || []).map((x: any) => `• *${x.nome}* — ${x.preco || "a combinar"}${x.desc ? "\n  " + x.desc : ""}`).join("\n");
  return `📦 *Entrega*\n${f || dados.loja.envio}\n\nPara calcular o frete pelos Correios, me mande seu *CEP* que um atendente confirma o valor.`;
}
function textoPagamento(dados: Dados) {
  const pg = dados.loja.pagamentos || {}, c = pg.credito || {}, l: string[] = [];
  if (pg.pix?.ativo) l.push(`• *Pix* — à vista${pg.pix.desconto ? `, com ${pg.pix.desconto} de desconto` : ""}`);
  if (c.ativo) l.push("• *Cartão de crédito à vista* (1x)");
  if (c.ativo) l.push(`• *Cartão de crédito parcelado*${c.parcelas > 1 ? ` — até ${c.parcelas}x${c.semJuros ? " sem juros" : ""}` : " — o atendente informa as condições"}`);
  if (pg.debito?.ativo) l.push("• *Débito*");
  if (pg.dinheiro?.ativo) l.push("• *Dinheiro* — na loja ou na entrega em Sertânia");
  return `💳 *Formas de pagamento*\n${l.join("\n") || dados.loja.pagamento}\n\nNo pedido online, enviamos a chave Pix ou o link do cartão aqui pelo WhatsApp.`;
}

export function sistemaIA(dados: Dados) {
  const prods = dados.produtos.map((p) => `- ${p.nome} | ${p.marca} | ${p.cat}${p.sub ? "/" + p.sub : ""} | preço: ${p.preco || "não informado"} | tamanhos: ${tamTxt(p) || "único"}${p.semEstoque ? " | ESGOTADO" : ""}${p.selo === "novo" ? " | novidade" : ""} | ${p.link}`).join("\n");
  return `Você é o assistente virtual da DE men, loja de moda masculina premium em Sertânia-PE (revenda autorizada Calvin Klein, Reserva, Adidas e Ogochi), respondendo clientes no WhatsApp.

Regras:
- Responda em português do Brasil, curto (até 5 linhas), simpático e direto, no estilo WhatsApp. Pode usar *negrito* e no máximo 1 emoji.
- Use SOMENTE as informações abaixo. Nunca invente preço, estoque, desconto, prazo, cor ou tamanho que não estejam listados.
- Se o preço for "não informado", diga que o atendente confirma o valor. Tamanhos marcados "(esgotado)" ou peças ESGOTADO não estão disponíveis: ofereça o aviso quando chegar (um atendente anota). Para os outros tamanhos, o atendente confirma a disponibilidade.
- Ao citar uma peça, mande o link dela.
- Se o cliente quiser fechar compra, reclamar, trocar, negociar, ou se a pergunta não puder ser respondida com estas informações, diga que vai chamar um atendente e termine a resposta com a marca [ATENDENTE].
- Não fale de assuntos fora da loja; traga a conversa de volta para as peças com educação.
- Nunca peça dados de cartão, senhas ou documentos.

Loja: endereço ${dados.loja.endereco}; horário ${dados.loja.horario}; site ${dados.loja.site}; Instagram ${dados.loja.instagram}.
Pagamento: ${dados.loja.pagamento}.
Entrega: ${(dados.loja.fretes || []).map((f: any) => `${f.nome} (${f.preco || "a combinar"})`).join("; ") || dados.loja.envio}.
Trocas: ${dados.loja.trocas}.
${dados.loja.cupom ? `Cupom de primeira compra: ${dados.loja.cupom.codigo} — ${dados.loja.cupom.titulo}.` : ""}

Produtos na vitrine:
${prods}`;
}

const SAUDACOES = ["oi", "ola", "bom dia", "boa tarde", "boa noite", "eai", "e ai", "opa", "menu", "inicio", "comecar", "hello", "hi"];

export async function responder(e: Entrada, d: Deps): Promise<Resultado> {
  const { dados } = d;
  const id = e.respostaId || "";
  const t = norm(e.texto || "");
  const primeiroNome = (e.nome || "").split(" ")[0];

  // Atendente cuidando da conversa: robô fica quieto, a não ser que o cliente peça o menu
  if (d.pausadoAte && d.pausadoAte > d.agora) {
    if (id === "menu" || t === "menu") return { saidas: [menu(dados)], despausar: true };
    return { saidas: [] };
  }

  // Botões e listas
  if (id) {
    if (id === "menu") return { saidas: [menu(dados)] };
    if (id === "catalogo") return { saidas: [categorias(dados)] };
    if (id === "novidades") return { saidas: [listaProdutos(dados, "Novidades", dados.produtos.filter((p) => p.selo === "novo").concat(dados.produtos.filter((p) => p.selo !== "novo")).slice(0, 10))] };
    if (id.startsWith("cat:")) { const c = id.slice(4); return { saidas: [listaProdutos(dados, c, dados.produtos.filter((p) => p.cat === c))] }; }
    if (id.startsWith("p:")) return { saidas: produto(dados, id.slice(2)) };
    if (id.startsWith("quero:")) {
      const p = dados.produtos.find((x) => x.id === id.slice(6));
      if (p?.semEstoque) return { pausarHoras: 12, saidas: [{ tipo: "texto", texto: `Anotado${primeiroNome ? ", " + primeiroNome : ""}! 🔔\nA *${p.nome}* está esgotada agora. Me diga o *tamanho* que você quer e a loja te avisa aqui assim que chegar.` }] };
      return { pausarHoras: 12, saidas: [{ tipo: "texto", texto: `Ótima escolha${primeiroNome ? ", " + primeiroNome : ""}! 🙌\nAnotei: *${p ? p.nome : "a peça"}*.\nMe diga o *tamanho* e se prefere *retirar na loja* ou *receber em casa* (com o CEP). Um atendente já vai confirmar estoque, valor e pagamento aqui mesmo.` }] };
    }
    if (id === "tamanhos") return { saidas: [comBotoes(`📏 *Qual meu tamanho?*\nNo site tem o *provador virtual*: você informa altura e peso e ele sugere seu tamanho de camisa, calça, bermuda e calçado.\n👉 ${dados.loja.site}#provador\n\nSe preferir, me diga sua altura, peso e a peça que te ajudo.`)] };
    if (id === "frete") return { saidas: [comBotoes(textoFrete(dados))] };
    if (id === "pagamento") return { saidas: [comBotoes(textoPagamento(dados))] };
    if (id === "trocas") return { saidas: [comBotoes(`🔄 *Trocas*\n${dados.loja.trocas}\nPara trocar, é só falar com um atendente.`)] };
    if (id === "horario") return { saidas: [comBotoes(`📍 *${dados.loja.endereco}*\n🕒 ${dados.loja.horario}\n\nInstagram: ${dados.loja.instagram}`)] };
    if (id === "atendente") return { pausarHoras: 12, saidas: [{ tipo: "texto", texto: `Pronto${primeiroNome ? ", " + primeiroNome : ""}! Chamei um atendente da DE men, ele responde aqui mesmo. 🕒 Horário: ${dados.loja.horario}.\n(Para voltar ao menu automático, envie *menu*.)` }] };
  }

  // Texto livre
  if (!t) return { saidas: [menu(dados)] };
  if (SAUDACOES.includes(t) || (t.length <= 12 && SAUDACOES.some((s) => t.startsWith(s)))) {
    return { saidas: [menu(dados, `Olá${primeiroNome ? ", " + primeiroNome : ""}! 👋`)] };
  }
  if (tem(t, "atendente", "humano", "pessoa", "vendedor", "falar com")) return responder({ ...e, respostaId: "atendente" }, d);

  // Perguntas livres → IA (com limite diário por número)
  if (d.ia && d.iaUsosHoje < d.iaLimiteDia) {
    const hist = d.historico.slice(-6).map((m) => ({ role: (m.direcao === "entrada" ? "user" : "assistant") as "user" | "assistant", content: m.texto }));
    while (hist.length && hist[0].role !== "user") hist.shift();
    const msgs = [...hist, { role: "user" as const, content: e.texto || "" }];
    try {
      let r = (await d.ia(sistemaIA(dados), msgs)).trim();
      const chamar = r.includes("[ATENDENTE]");
      r = r.replace(/\s*\[ATENDENTE\]\s*/g, " ").trim();
      if (r) return { usouIA: true, pausarHoras: chamar ? 12 : undefined, saidas: chamar ? [{ tipo: "texto", texto: r }] : [comBotoes(r)] };
    } catch (_err) { /* cai nas palavras-chave abaixo */ }
  }

  // Sem IA (ou IA falhou): palavras-chave
  if (tem(t, "frete", "entrega", "correio", "envia", "sedex", "pac", "cep")) return responder({ ...e, respostaId: "frete" }, d);
  if (tem(t, "pix", "pagamento", "pagar", "cartao", "parcel", "credito", "debito", "a vista")) return responder({ ...e, respostaId: "pagamento" }, d);
  if (tem(t, "troca", "devolu")) return responder({ ...e, respostaId: "trocas" }, d);
  if (tem(t, "horario", "endereco", "onde fica", "abre", "fecha", "localiza")) return responder({ ...e, respostaId: "horario" }, d);
  if (tem(t, "tamanho", "medida", "numero", "veste")) return responder({ ...e, respostaId: "tamanhos" }, d);
  const achados = dados.produtos.filter((p) => t.split(/[^a-z0-9]+/).filter((w) => w.length > 3).some((w) => norm(`${p.nome} ${p.marca} ${p.cat} ${p.sub}`).includes(w)));
  if (achados.length) return { saidas: [listaProdutos(dados, "Encontrei estas peças", achados)] };
  return { saidas: [menu(dados, "Não entendi muito bem 🤔 Escolha uma opção ou chame um atendente:")] };
}
