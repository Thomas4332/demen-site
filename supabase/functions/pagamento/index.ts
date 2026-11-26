// Pagamento online da DE men com Mercado Pago (Checkout Pro: Pix, cartão à vista ou parcelado).
// POST /pagamento            → cria o pedido e devolve o link de pagamento do Mercado Pago
// POST /pagamento?acao=aviso → o Mercado Pago avisa quando o pagamento muda (pago, recusado...)
// Segredos: MP_ACCESS_TOKEN (obrigatório), MP_WEBHOOK_SECRET (opcional, confere a assinatura do aviso),
//           mais os do frete (MELHORENVIO_TOKEN...) para cobrar o envio pelos Correios/transportadoras.
import { createClient } from "npm:@supabase/supabase-js@2";
import { cors, cotar, dados, json, precoNum, SITE, soDigitos, validarItens } from "./envio.ts";

const env = (k: string) => Deno.env.get(k) ?? "";
const sb = createClient(env("SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const MP = "https://api.mercadopago.com";
const limpa = (s: unknown, n: number) => String(s ?? "").replace(/[<>]/g, "").trim().slice(0, n);
const codigo = () => "DM" + new Date().toISOString().slice(2, 10).replaceAll("-", "") + "-" + crypto.randomUUID().slice(0, 5).toUpperCase();

async function criar(req: Request) {
  const token = env("MP_ACCESS_TOKEN");
  if (!token) return json(req, { erro: "Pagamento online ainda não está ativo", configurado: false }, 503);
  const b = await req.json();
  const d = await dados();
  const itens = validarItens(d, b.itens);
  const semPreco = itens.filter((i) => i.preco === null).map((i) => i.p.nome);
  if (semPreco.length) return json(req, { erro: "Estas peças ainda não têm preço no site: " + semPreco.join(", ") }, 400);

  // limite simples contra abuso
  const { count } = await sb.from("pedidos").select("id", { count: "exact", head: true }).gte("criado_em", new Date(Date.now() - 10 * 60_000).toISOString());
  if ((count ?? 0) > 40) return json(req, { erro: "Muitos pedidos agora, tente em alguns minutos" }, 429);

  // frete recalculado aqui no servidor
  const f = b.frete || {};
  let frete = 0, freteDesc = "Retirar na loja", cep = "", endereco = "";
  if (f.tipo === "envio") {
    cep = soDigitos(f.cep);
    if (cep.length !== 8) return json(req, { erro: "CEP inválido" }, 400);
    const r = await cotar(d, cep, itens);
    const op = r.opcoes.find((o) => o.id === String(f.servico));
    if (!op) return json(req, { erro: "Opção de frete indisponível, calcule de novo" }, 400);
    frete = op.preco; freteDesc = `${op.nome}${op.prazo ? ` (${op.prazo} dias úteis)` : ""}`;
    endereco = limpa(f.endereco, 300);
    if (endereco.length < 8) return json(req, { erro: "Informe o endereço completo para entrega" }, 400);
  } else if (f.tipo === "local") {
    const local = (d.loja.fretes || []).find((x: any) => x.local);
    const pl = local ? precoNum(local.preco) : null;
    if (pl === null) return json(req, { erro: "Entrega em Sertânia é combinada pelo WhatsApp" }, 400);
    frete = pl; freteDesc = local.nome; cep = soDigitos(f.cep); endereco = limpa(f.endereco, 300);
  } else if (f.tipo !== "retirada") return json(req, { erro: "Escolha a forma de entrega" }, 400);

  const subtotal = Math.round(itens.reduce((t, i) => t + (i.preco as number) * i.qtd, 0) * 100) / 100;
  const total = Math.round((subtotal + frete) * 100) / 100;
  const cod = codigo();
  const nome = limpa(b.cliente?.nome, 80), contato = limpa(b.cliente?.contato, 120);

  const { error: e1 } = await sb.from("pedidos").insert({
    codigo: cod, subtotal, frete, frete_desc: freteDesc, total, cliente_nome: nome || null, cliente_contato: contato || null,
    cep: cep || null, endereco: endereco || null,
    itens: itens.map((i) => ({ id: i.p.id, nome: i.p.nome, marca: i.p.marca, tam: i.tam, qtd: i.qtd, preco: i.preco })),
  });
  if (e1) throw new Error("pedido: " + e1.message);

  const parcelas = Number(d.loja.pagamentos?.credito?.parcelas) || 0;
  const volta = (s: string) => `${SITE}?pedido=${cod}&pagamento=${s}`;
  const pref = {
    items: [
      ...itens.map((i) => ({ id: i.p.id, title: `${i.p.nome} (${i.p.marca})${i.tam ? " - tam. " + i.tam : ""}`.slice(0, 250), quantity: i.qtd, unit_price: i.preco, currency_id: "BRL", picture_url: i.p.foto, category_id: "fashion" })),
      ...(frete > 0 ? [{ id: "frete", title: "Frete: " + freteDesc, quantity: 1, unit_price: frete, currency_id: "BRL" }] : []),
    ],
    payer: nome ? { name: nome } : undefined,
    external_reference: cod,
    back_urls: { success: volta("aprovado"), pending: volta("pendente"), failure: volta("recusado") },
    auto_return: "approved",
    notification_url: `${env("SUPABASE_URL")}/functions/v1/pagamento?acao=aviso`,
    statement_descriptor: "DEMEN",
    payment_methods: parcelas > 1 ? { installments: parcelas } : undefined,
    metadata: { pedido: cod },
  };
  const r = await fetch(MP + "/checkout/preferences", {
    method: "POST", headers: { Authorization: "Bearer " + token, "Content-Type": "application/json", "X-Idempotency-Key": cod }, body: JSON.stringify(pref),
  });
  if (!r.ok) { const t = await r.text(); console.error("MP", r.status, t); await sb.from("pedidos").update({ status: "cancelado" }).eq("codigo", cod); return json(req, { erro: "Não foi possível abrir o pagamento agora" }, 502); }
  const p = await r.json();
  await sb.from("pedidos").update({ mp_preferencia: p.id }).eq("codigo", cod);
  return json(req, { codigo: cod, total, url: p.init_point });
}

async function assinaturaOk(req: Request, dataId: string) {
  const segredo = env("MP_WEBHOOK_SECRET");
  if (!segredo) return true; // sem segredo: a confirmação real vem da consulta ao Mercado Pago abaixo
  const sig = req.headers.get("x-signature") || "", rid = req.headers.get("x-request-id") || "";
  const partes = Object.fromEntries(sig.split(",").map((x) => x.trim().split("=")));
  if (!partes.ts || !partes.v1) return false;
  const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(segredo), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const h = new Uint8Array(await crypto.subtle.sign("HMAC", k, new TextEncoder().encode(`id:${dataId.toLowerCase()};request-id:${rid};ts:${partes.ts};`)));
  return [...h].map((x) => x.toString(16).padStart(2, "0")).join("") === partes.v1;
}

async function aviso(req: Request, url: URL) {
  let b: any = {}; try { b = await req.json(); } catch { /* aviso antigo vem só na URL */ }
  const tipo = b.type || b.topic || url.searchParams.get("type") || url.searchParams.get("topic");
  const id = String(b.data?.id || url.searchParams.get("data.id") || url.searchParams.get("id") || "");
  if (tipo !== "payment" || !id) return new Response("ok");
  if (!(await assinaturaOk(req, id))) return new Response("assinatura inválida", { status: 401 });
  // a fonte da verdade é o próprio Mercado Pago
  const r = await fetch(`${MP}/v1/payments/${encodeURIComponent(id)}`, { headers: { Authorization: "Bearer " + env("MP_ACCESS_TOKEN") } });
  if (!r.ok) return new Response("ok");
  const pg = await r.json();
  const mapa: Record<string, string> = { approved: "pago", authorized: "pendente", pending: "pendente", in_process: "pendente", in_mediation: "pendente", rejected: "recusado", cancelled: "cancelado", refunded: "reembolsado", charged_back: "reembolsado" };
  const status = mapa[pg.status] || "pendente";
  if (pg.external_reference) {
    await sb.from("pedidos").update({ status, mp_pagamento: String(pg.id), atualizado_em: new Date().toISOString() })
      .eq("codigo", String(pg.external_reference)).neq("status", "enviado").neq("status", "entregue");
  }
  return new Response("ok");
}

Deno.serve(async (req) => {
  const url = new URL(req.url);
  if (req.method === "OPTIONS") return new Response(null, { headers: cors(req) });
  try {
    if (url.searchParams.get("acao") === "aviso") return await aviso(req, url);
    if (req.method !== "POST") return json(req, { erro: "use POST" }, 405);
    return await criar(req);
  } catch (e) {
    const m = String((e as Error).message || e);
    console.error("pagamento", m);
    const doCliente = /esgotado|inválid|não encontrado|quantidade/.test(m);
    return json(req, { erro: doCliente ? m : "Não foi possível abrir o pagamento agora" }, doCliente ? 400 : 500);
  }
});
